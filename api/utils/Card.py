BASIC_LANDS = ["Plains", "Island", "Swamp", "Mountain", "Forest"]


class Card:
    def __init__(
        self,
        quantity: int,
        card_name: str,
        source_deck_name: str = "",
        target_deck_name: str = "",
        **kwargs,
    ):
        self.count = quantity
        self.card_name = card_name
        self.quantity_card_name = f"{quantity} {card_name}"
        self.source_deck_name = source_deck_name
        self.target_deck_name = target_deck_name
        self.basic_land = card_name in BASIC_LANDS
        if self.source_deck_name != "" and self.target_deck_name != "":
            self.reshuffled = True
        else:
            self.reshuffled = False

        if source_deck_name != "":
            self.held = True
        else:
            self.held = False

    def to_dict(self):
        return {
            "count": self.count,
            "card_name": self.card_name,
            "quantity_card_name": self.quantity_card_name,
            "source_deck_name": self.source_deck_name,
            "target_deck_name": self.target_deck_name,
            "basic_land": self.basic_land,
            "held": self.held,
            "reshuffled": self.reshuffled,
        }
