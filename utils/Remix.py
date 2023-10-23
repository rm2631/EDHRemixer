from utils.Deck import Deck
from utils.Card import Card
from itertools import groupby

class Remix():
    def __init__(self):
        self.decks = []
        self.reallocated_deck = []

    def add_deck(self, 
                 deck_name: str, 
                 source_deck: bool, 
                 card_string: str = "",
                 ):
        self.decks.append(
            Deck(
                deck_name, 
                source_deck, 
                card_string=card_string
                ))
        
    def reallocate_cards(self):
        cards = []
        ditch_list = []
        reallocate_list = []
        buy_list = []

        for deck in self.decks:
            cards.extend(deck.cards)

        cards.sort(key=lambda x: x.held, reverse=True)
        cards.sort(key=lambda x: x.card_name)
        for card, group in groupby(cards, lambda x: x.card_name):
            group_cards = list(group)
            held_cards = [card for card in group_cards if card.held]
            needed_cards = [card for card in group_cards if not card.held]
            for needed_card in needed_cards:
                if len(held_cards) > 0:
                    held_card = held_cards.pop()
                    held_card.target_deck = needed_card.source_deck_name
                    reallocate_list.append(held_card)
                else:
                    needed_card.target_deck = needed_card.source_deck_name
                    buy_list.append(needed_card)
            for held_card in held_cards:
                held_card.target_deck = None
                ditch_list.append(held_card)
        pass

        self.reallocated_deck.append(Deck("buy", False, card_list=buy_list))
        self.reallocated_deck.append(Deck("ditch", False, card_list=ditch_list))
        self.reallocated_deck.append(Deck("reallocate", False, card_list=reallocate_list))

        for deck in self.reallocated_deck:
            deck.export_deck_list()