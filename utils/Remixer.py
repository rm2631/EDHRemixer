import re
import os
from utils.Card import Card
from itertools import groupby
import pandas as pd


class Remixer:
    cards = []

    def add_deck(self, directory_name: str, source_deck: bool):
        ## If directory is empty, raise Exception
        if not os.listdir(directory_name):
            raise Exception(f"Directory {directory_name} is empty")

        for file in os.listdir(directory_name):
            if file.endswith(".txt"):
                with open(os.path.join(directory_name, file), "r") as file_data:
                    card_list = self._card_string_to_card(
                        file_data.read(), file.split(".")[0], source_deck
                    )
                    self.cards.extend(card_list)

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
        self._export_deck_list(buy_list)
        self._produce_excel([reallocate_list, buy_list, ditch_list])
        print(f"Reallocated {len(reallocate_list)} cards")
        print(f"Need to buy {len(buy_list)} cards")
        print(f"Need to ditch {len(ditch_list)} cards")

    def _produce_excel(self, lists):
        ## convert the list of cards to a list of dicts
        cards_as_dicts = []
        for list in lists:
            for card in list:
                cards_as_dicts.append(card.to_dict())
        df = pd.DataFrame(cards_as_dicts)
        df.to_excel("output.xlsx")

    def _export_deck_list(self, card_list):
        deck_list = []
        for card in card_list:
            string = f"{card.count} {card.card_name}\n"
            deck_list.append(string)
        ## write the deck list to a file
        with open(f"buy.txt", "w") as f:
            f.writelines(deck_list)

    def _card_string_to_card(
        self, deck_content_string, deck_name, source_deck
    ) -> [Card]:
        """
        Convert a string of cards to a list of Card objects.
        """
        card_list = []
        card_string_list = deck_content_string.split("\n")
        for card in card_string_list:
            count, name = self._extract_count_and_name(card)
            for _ in range(int(count)):
                if source_deck:
                    card_list.append(
                        Card(
                            1,
                            name,
                            source_deck_name=deck_name,
                        )
                    )
                else:
                    card_list.append(
                        Card(
                            1,
                            name,
                            target_deck_name=deck_name,
                        )
                    )
        return card_list

    def _extract_count_and_name(self, input_string):
        ## find the integer at the start of the string
        count_match = re.search(r"^\d+", input_string)
        count = count_match.group(0)
        ## find all the string after the integer and before "(" if any
        name_match = re.search(r"^\d+ (.*)", input_string)
        name = name_match.group(1)
        name = name.split("(")[0].strip()
        return count, name
