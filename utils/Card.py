


class Card():
    def __init__(self, count: int, card_name: str, held:bool, source_deck_name: bool):
        self.count = count
        self.card_name = card_name
        self.held = held
        self.source_deck_name = source_deck_name
    
        ##To set
        self.target_deck = None