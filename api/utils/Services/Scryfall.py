import requests

SCRYFALL = "https://api.scryfall.com/cards/search"


def get_card_from_query(query):
    response = requests.get(SCRYFALL, params={"q": query})
    return response.json()


async def get_card_data(card):
    card_name = card.card_name
    print("Handling card:", card_name)
    response = get_card_from_query(card_name)
    if response.get("object") == "error":
        return {
            "quantity": card.quantity,
            "card_name": card_name,
            "error": "Card not found",
        }

    data = response["data"]
    exact_match = [card for card in data if card["name"] == card_name]
    idx = 0 if len(exact_match) == 0 else data.index(exact_match[0])

    card_id = data[idx][
        "oracle_id"
    ]  ## Is the real unique identifier of a card regardless of the print
    card_name = data[idx]["name"]
    color_identity = data[idx]["color_identity"]
    return {
        "quantity": card.quantity,
        "card_id": card_id,
        "card_name": card_name,
        "color_identity": color_identity,
    }
