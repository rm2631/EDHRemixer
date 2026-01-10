from services.edhrec_extended import EDHRecExtended
from pydantic import BaseModel

edhrec = EDHRecExtended()


class Card(BaseModel):
    count: str
    name: str
    basic_land: bool


class Deck(BaseModel):
    name: str
    cards: list[Card]


def get_average_deck(commander_name: str) -> Deck:
    average_deck = edhrec.get_commanders_average_deck(commander_name)
    basics = ["Plains", "Island", "Swamp", "Mountain", "Forest"]
    cards = [
        Card(
            count=card.split(" ", 1)[0],
            name=card.split(" ", 1)[1],
            basic_land=card.split(" ", 1)[1] in basics,
        )
        for card in average_deck["decklist"]
    ]
    return Deck(name=commander_name, cards=cards)


def get_card_overall_inclusion(card_name: str) -> dict:
    """
    Get the overall inclusion percentage for a card across all Commander decks.

    Args:
        card_name: Name of the card (e.g., "Sol Ring")

    Returns:
        Dictionary with overall inclusion data or None if not found
    """
    return edhrec.get_overall_card_inclusion(card_name)


def get_card_commander_inclusion(card_name: str, commander_name: str) -> dict:
    """
    Get the inclusion percentage for a card in a specific commander's decks.

    Args:
        card_name: Name of the card
        commander_name: Name of the commander

    Returns:
        Dictionary with commander-specific inclusion data or None if not found
    """
    commander_cards = edhrec.get_commander_cards(commander_name)

    for category, cards in commander_cards.items():
        for card in cards:
            if card["name"] == card_name:
                inclusion_percent = (card["num_decks"] / card["potential_decks"]) * 100
                return {
                    "card_name": card["name"],
                    "commander": commander_name,
                    "category": category,
                    "inclusion_percentage": round(inclusion_percent, 2),
                    "num_decks": card["num_decks"],
                    "potential_decks": card["potential_decks"],
                    "synergy": card["synergy"],
                }
    return None
