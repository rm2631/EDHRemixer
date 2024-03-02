# from utils.Card import Card
from utils.Card import Card
from itertools import groupby
import pandas as pd
from io import BytesIO
import copy
from collections import Counter


class Remixer:
    def __init__(self):
        self.ditch = []
        self.buy = []
        self.allocated = []

    def add_deck(self, cards, source_deck: bool):
        def _add_to_list(source_deck: bool, card: Card):
            cards = []
            for _ in range(1, card["quantity"] + 1):
                new_card = card.copy()
                new_card["quantity"] = 1
                cards.append(Card(**new_card))

            if source_deck:
                self.ditch.extend(cards)
            else:
                self.buy.extend(cards)

        for card in cards:
            card = card.__dict__
            if source_deck:
                card["source_deck_name"] = card["deck"]
            else:
                card["target_deck_name"] = card["deck"]
            _add_to_list(source_deck, card)

        self.source_decks = [
            (key, list(group))
            for key, group in groupby(self.ditch, key=lambda x: x.source_deck_name)
        ]
        self.target_decks = [
            (key, list(group))
            for key, group in groupby(self.buy, key=lambda x: x.target_deck_name)
        ]

        self.pre_allocation = copy.deepcopy(self.ditch + self.buy)

    def _compare_decks(self, deck1, deck2):
        """
        This method compares two decks and returns the similar cards.
        :param deck1: list of cards
        :param deck2: list of cards
        :return: list of similar cards
        """
        deck1_cards = Counter([c.card_name for c in deck1[1]])
        deck2_cards = Counter([c.card_name for c in deck2[1]])
        intersection = (deck1_cards & deck2_cards).elements()
        result = list(intersection)
        return result

    def _reallocate_from_source_to_target(self, source_deck, target_deck, cards):
        pass

    def _reallocate_cards(self):
        print(sum([len(deck[1]) for deck in self.source_decks]))

        combinations = [
            (source_deck, target_deck, self._compare_decks(source_deck, target_deck))
            for source_deck in self.source_decks
            for target_deck in self.target_decks
        ]

        combinations = [c for c in combinations if len(c[2]) != 0]
        if len(combinations) == 0:
            self.reallocated = True
            return

        combinations = sorted(
            combinations,
            key=lambda x: (x[0][0] != "Collection", len(x[2])),
            reverse=True,
        )

        optimal_reallocation = combinations[0]
        ## get the dict from self.sources and self.targets that matches the optimal_reallocation
        pass

        source_deck = [
            deck for deck in self.source_decks if deck == optimal_reallocation[0]
        ][0]
        target_deck = [
            deck for deck in self.target_decks if deck == optimal_reallocation[1]
        ][0]

        for card_name in optimal_reallocation[2]:
            card = [c for c in source_deck[1] if c.card_name == card_name][0]
            card.target_deck_name = target_deck[0]
            card.reshuffled = True
            self.allocated.append(card)
            source_idx = next(
                index
                for index, card in enumerate(source_deck[1])
                if card.card_name == card_name
            )
            source_deck[1].pop(source_idx)

            target_idx = next(
                index
                for index, card in enumerate(target_deck[1])
                if card.card_name == card_name
            )
            target_deck[1].pop(target_idx)

    def reshuffle(self):
        """
        Move cards from sources to targets
        After the sources are depleted or the targets, or you can no longer move cards, add the missing cards to the buylist
        """
        # create a list of tuples containing the deck name and the cards in the deck
        self.reallocated = False
        while not self.reallocated:
            self._reallocate_cards()

        self.ditch = [c for deck in self.source_decks for c in deck[1]]
        self.buy = [c for deck in self.target_decks for c in deck[1]]

        self._check_quantities(
            self.pre_allocation, self.allocated + self.buy + self.ditch
        )
        return self._get_excel([self.allocated, self.buy, self.ditch])

    def _check_quantities(
        self, pre_allocation: list[Card], post_allocation: list[Card]
    ):
        # check sources
        unallocated_sources = len(
            [c for c in pre_allocation if c.source_deck_name != ""]
        )
        allocated_sources = len(
            [c for c in post_allocation if c.source_deck_name != ""]
        )
        assert unallocated_sources == allocated_sources

        # check targets
        unallocated_targets = len(
            [c for c in pre_allocation if c.target_deck_name != ""]
        )
        allocated_targets = len(
            [c for c in post_allocation if c.target_deck_name != ""]
        )
        assert unallocated_targets == allocated_targets

    def _get_excel(self, lists):
        ## convert the list of cards to a list of dicts
        cards_as_dicts = []
        for list in lists:
            for card in list:
                cards_as_dicts.append(card.to_dict())
        df = pd.DataFrame(cards_as_dicts)
        with BytesIO() as buffer:
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="Sheet1")
                writer.close()  # This will save the content to the buffer
            return buffer.getvalue()  # Returns the Excel file in memory
