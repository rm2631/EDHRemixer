from utils.Card import Card
import re

class Deck():
    def __init__(self, deck_name: str, source_deck: bool, card_string: str = "", card_list: list[Card] = []):
        self.deck_name = deck_name
        self.source_deck = source_deck
        if card_list:
            self.cards = card_list
        if card_string:
            self.cards = self._card_string_to_card(source_deck, card_string)

    def _extract_count_and_name(self, input_string):
        ## find the integer at the start of the string
        count_match = re.search(r"^\d+", input_string)
        count = count_match.group(0)
        ## find all the string after the integer and before "(" if any
        name_match = re.search(r"^\d+ (.*)", input_string)
        name = name_match.group(1)
        name = name.split("(")[0].strip()
        return count, name

    def _card_string_to_card(self, source_deck, card_string) -> list[Card]:
        """
        Convert a string of cards to a list of Card objects.
        """
        card_list = []
        card_string_list = card_string.split("\n")
        for card in card_string_list:
            count, name = self._extract_count_and_name(card)
            if source_deck:
                held = True
            else:
                held = False
            for _ in range(int(count)):
                card_list.append(Card(1, name, held, self.deck_name))
        return card_list

    def export_deck_list(self):
        deck_list = []
        for card in self.cards:
            string = f"{card.count} {card.card_name}\n"
            deck_list.append(string)
        ## write the deck list to a file
        with open(f"reallocated/{self.deck_name}.txt", "w") as f:
            f.writelines(deck_list)