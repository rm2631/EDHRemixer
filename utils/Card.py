


class Card():
    def __init__(self, 
                    count: int, 
                    card_name: str, 
                    source_deck_name: str = None, 
                    target_deck_name: str = None
                ):
        
        self.count = count
        self.card_name = card_name
        self.source_deck_name = source_deck_name
        self.target_deck_name = target_deck_name

        if source_deck_name:
            self.held = True
        else:
            self.held = False

    def to_dict(self):
        return {
            "count": self.count,
            "card_name": self.card_name,
            "source_deck_name": self.source_deck_name,
            "target_deck_name": self.target_deck_name,
            "held": self.held,
        }