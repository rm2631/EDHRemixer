# from utils.Card import Card
from Card import Card
from itertools import groupby
import pandas as pd
from io import BytesIO


class Remixer:
    def __init__(self):
        self.cards = []

    def add_deck(self, cards, source_deck: bool):
        ## If directory is empty, raise Exception
        for card in cards:
            card = card.__dict__
            if source_deck:
                card["source_deck_name"] = card["deck"]
            else:
                card["target_deck_name"] = card["deck"]
            ## Create a card object for each card in the deck
            for _ in range(1, card["quantity"] + 1):
                new_card = card.copy()
                new_card["quantity"] = 1
                self.cards.append(Card(**new_card))

    def reallocate(self):
        reallocate_list = []
        buy_list = []
        ditch_list = []

        self.cards = sorted(self.cards, key=lambda x: x.card_name)
        for card, group in groupby(self.cards, lambda x: x.card_name):
            group_cards = list(group)
            held_cards = [card for card in group_cards if card.held]
            needed_cards = [card for card in group_cards if not card.held]
            for needed_card in needed_cards:
                if len(held_cards) > 0:
                    held_card = held_cards.pop()
                    held_card.target_deck_name = needed_card.target_deck_name
                    reallocate_list.append(held_card)
                else:
                    buy_list.append(needed_card)
            for held_card in held_cards:
                ditch_list.append(held_card)
        return self._get_excel([reallocate_list, buy_list, ditch_list])

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
