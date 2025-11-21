from typing import List, ByteString
from models import Collection, Card, Movement
from services.moxfield_connector import MoxfieldConnector
from collections import Counter
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
                    input.id, input.include_sideboard
                )
            else:
                deck_cards = moxfield_connector.get_binder_content(input.id)
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

    def _find_optimal_movement(
        self, available_cards: List[Card], required_cards: List[Card]
    ):
        source_collections = list(
            set([card.source for card in available_cards if card.source is not None])
        )
        # Sort sources by priority (highest first)
        source_collections.sort(key=lambda c: c.priority, reverse=True)

        target_collections = list(
            set([card.target for card in required_cards if card.target is not None])
        )
        # Sort targets by priority (highest first)
        target_collections.sort(key=lambda c: c.priority, reverse=True)

        combinations = [
            (source_collection, target_collection)
            for source_collection in source_collections
            for target_collection in target_collections
        ]
        intersections = []

        for source_collection, target_collection in combinations:
            source_deck = [
                card for card in available_cards if card.source == source_collection
            ]
            target_deck = [
                card for card in required_cards if card.target == target_collection
            ]
            intersection = self._find_intersection(source_deck, target_deck)
            intersections.append((len(intersection), intersection))

        zipped = list(zip(combinations, intersections))
        # Filter out combinations with zero intersection before sorting
        # This ensures we skip high-priority sources with no matching cards
        zipped_with_cards = [z for z in zipped if z[1][0] > 0]

        # If no combinations have matching cards, return the first combination with 0 intersection
        if not zipped_with_cards:
            zipped.sort(key=lambda x: (-x[0][0].priority, -x[0][1].priority, -x[1][0]))
            optimal = zipped[0]
        else:
            # Sort by priority and intersection count, only considering combinations with cards
            zipped_with_cards.sort(
                key=lambda x: (-x[0][0].priority, -x[0][1].priority, -x[1][0])
            )
            optimal = zipped_with_cards[0]

        return Movement(
            source=optimal[0][0],
            target=optimal[0][1],
            intersection=optimal[1][0],
            intersection_cards=optimal[1][1],
        )

    def _validate_shuffling(self):
        assert len(self.initially_available_cards) == (
            len(self.available_cards) + len(self.allocated_cards)
        )
        assert len(self.initially_required_cards) == (
            len(self.required_cards) + len(self.allocated_cards)
        )

    def reshuffle(self):
        while True:
            if not self.available_cards or not self.required_cards:
                break
            best_source = self._find_optimal_movement(
                self.available_cards, self.required_cards
            )
            if best_source.intersection == 0:
                break
            for card_id in best_source.intersection_cards:
                available_card = next(
                    card
                    for card in self.available_cards
                    if card.uniqueCardId == card_id
                    and card.source == best_source.source
                )
                self.available_cards.remove(available_card)
                required_card = next(
                    card
                    for card in self.required_cards
                    if card.uniqueCardId == card_id
                    and card.target == best_source.target
                )
                self.required_cards.remove(required_card)
                available_card.target = best_source.target
                self.allocated_cards.append(available_card)
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
