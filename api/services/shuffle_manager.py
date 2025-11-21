from typing import List, ByteString, Dict, Set
from models import Collection, Card, Movement
from services.moxfield_connector import MoxfieldConnector
from collections import Counter, defaultdict
import pandas as pd
from io import BytesIO


class ShuffleManager:

    def __init__(
        self,
        inputs: List[Collection],
        moxfield_connector: MoxfieldConnector = MoxfieldConnector(),
    ):
        self._handle_card_extractions(inputs, moxfield_connector)

    def _handle_card_extractions(self, inputs, moxfield_connector) -> None:
        # Filter out inactive collections
        active_inputs = [input for input in inputs if input.active]

        cards = []
        for input in active_inputs:
            if input.is_deck:
                deck_cards = moxfield_connector.get_deck_content(
                    input.moxfield_id, input.include_sideboard
                )
            else:
                deck_cards = moxfield_connector.get_binder_content(input.moxfield_id)
            for card in deck_cards:
                for _ in range(card["quantity"]):
                    cards.append(
                        Card(
                            source=input if input.is_source else None,
                            target=input if not input.is_source else None,
                            price_usd=card["card"].get("prices").get("usd", 0),
                            **card["card"],
                        )
                    )

        self.initially_available_cards = [
            card for card in cards if card.source is not None
        ]
        self.initially_required_cards = [card for card in cards if card.source is None]
        self.available_cards = self.initially_available_cards.copy()
        self.required_cards = self.initially_required_cards.copy()
        self.allocated_cards = []

        # Build indexes for fast lookups
        self._build_indexes()

    def _build_indexes(self):
        """Build indexes for O(1) lookups instead of O(n) filters"""
        self.available_by_source: Dict[Collection, List[Card]] = defaultdict(list)
        self.required_by_target: Dict[Collection, List[Card]] = defaultdict(list)

        for card in self.available_cards:
            if card.source:
                self.available_by_source[card.source].append(card)

        for card in self.required_cards:
            if card.target:
                self.required_by_target[card.target].append(card)

        # Pre-compute Counters for each collection
        self.available_counters: Dict[Collection, Counter] = {}
        self.required_counters: Dict[Collection, Counter] = {}

        for source, cards in self.available_by_source.items():
            self.available_counters[source] = Counter([c.uniqueCardId for c in cards])

        for target, cards in self.required_by_target.items():
            self.required_counters[target] = Counter([c.uniqueCardId for c in cards])

    def _find_intersection(self, deck_1: List[Card], deck_2: List[Card]) -> List[str]:
        """
        This method compares two decks and returns the number of similar cards between them
        :param deck1: list of cards
        :param deck2: list of cards
        :return: int - number of similar cards
        """
        deck1_cards = Counter([c.uniqueCardId for c in deck_1])
        deck2_cards = Counter([c.uniqueCardId for c in deck_2])
        intersection = (deck1_cards & deck2_cards).elements()
        result = list(intersection)
        return result

    def _find_intersection_fast(
        self, source: Collection, target: Collection
    ) -> List[str]:
        """Fast intersection using pre-computed Counters"""
        source_counter = self.available_counters.get(source, Counter())
        target_counter = self.required_counters.get(target, Counter())
        intersection = (source_counter & target_counter).elements()
        return list(intersection)

    def _find_optimal_movement(
        self, available_cards: List[Card], required_cards: List[Card]
    ):
        # Use pre-built indexes instead of filtering
        source_collections = list(self.available_by_source.keys())
        target_collections = list(self.required_by_target.keys())

        # Sort sources by priority (highest first)
        source_collections.sort(key=lambda c: c.priority, reverse=True)
        # Sort targets by priority (highest first)
        target_collections.sort(key=lambda c: c.priority, reverse=True)

        best_movement = None
        best_score = (
            -float("inf"),
            -float("inf"),
            -float("inf"),
        )  # (source_priority, target_priority, intersection_count)

        # Iterate through all combinations to find the best one
        for source_collection in source_collections:
            for target_collection in target_collections:
                # Use fast intersection with pre-computed Counters
                intersection = self._find_intersection_fast(
                    source_collection, target_collection
                )
                intersection_count = len(intersection)

                # Skip combinations with no matches
                if intersection_count == 0:
                    continue

                # Score: higher priority and higher intersection count is better
                current_score = (
                    source_collection.priority,
                    target_collection.priority,
                    intersection_count,
                )

                # If this is better than our best, update
                if current_score > best_score:
                    best_score = current_score
                    best_movement = Movement(
                        source=source_collection,
                        target=target_collection,
                        intersection=intersection_count,
                        intersection_cards=intersection,
                    )

        return best_movement

    def _validate_shuffling(self):
        assert len(self.initially_available_cards) == (
            len(self.available_cards) + len(self.allocated_cards)
        )
        assert len(self.initially_required_cards) == (
            len(self.required_cards) + len(self.allocated_cards)
        )

    def _update_indexes_after_movement(
        self, source: Collection, target: Collection, card_ids: List[str]
    ):
        """Update indexes after moving cards - more efficient than rebuilding"""
        # Update available_by_source
        if source in self.available_by_source:
            self.available_by_source[source] = [
                card
                for card in self.available_by_source[source]
                if card.uniqueCardId not in card_ids
            ]
            if not self.available_by_source[source]:
                del self.available_by_source[source]
                del self.available_counters[source]
            else:
                # Update counter
                self.available_counters[source] = Counter(
                    [c.uniqueCardId for c in self.available_by_source[source]]
                )

        # Update required_by_target
        if target in self.required_by_target:
            self.required_by_target[target] = [
                card
                for card in self.required_by_target[target]
                if card.uniqueCardId not in card_ids
            ]
            if not self.required_by_target[target]:
                del self.required_by_target[target]
                del self.required_counters[target]
            else:
                # Update counter
                self.required_counters[target] = Counter(
                    [c.uniqueCardId for c in self.required_by_target[target]]
                )

    def reshuffle(self):
        while True:
            if not self.available_cards or not self.required_cards:
                break
            best_movement = self._find_optimal_movement(
                self.available_cards, self.required_cards
            )
            if not best_movement or best_movement.intersection == 0:
                break

            # Batch process all cards in the intersection
            cards_to_move = set(best_movement.intersection_cards)

            # Use the INDEX to get cards, not the main lists (which may be out of sync)
            available_source_cards = self.available_by_source.get(
                best_movement.source, []
            )
            required_target_cards = self.required_by_target.get(
                best_movement.target, []
            )

            # Build lookup dictionaries from the indexed cards
            available_by_id = {
                card.uniqueCardId: card for card in available_source_cards
            }
            required_by_id = {card.uniqueCardId: card for card in required_target_cards}

            for card_id in cards_to_move:
                if card_id in available_by_id and card_id in required_by_id:
                    available_card = available_by_id[card_id]
                    required_card = required_by_id[card_id]

                    self.available_cards.remove(available_card)
                    self.required_cards.remove(required_card)
                    available_card.target = best_movement.target
                    self.allocated_cards.append(available_card)

            # Update indexes incrementally
            self._update_indexes_after_movement(
                best_movement.source, best_movement.target, list(cards_to_move)
            )

        self._validate_shuffling()
        return self._build_excel_file()

    def _build_excel_file(self) -> ByteString:
        cards = self.allocated_cards + self.required_cards + self.available_cards
        cards.sort(key=lambda x: x.name)
        df = pd.DataFrame(
            [
                {
                    **card.model_dump(),
                    "source": card.source.name if card.source is not None else None,
                    "target": card.target.name if card.target is not None else None,
                }
                for card in cards
            ]
        )
        with BytesIO() as buffer:
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:  # type: ignore
                df.to_excel(writer, sheet_name="Sheet1")
                writer.close()  # This will save the content to the buffer
            return buffer.getvalue()  # Returns the Excel file in memory
