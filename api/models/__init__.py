from pydantic import BaseModel
from typing import List


class CardModel(BaseModel):
    deck: str
    card_name: str
    quantity: int = 1


class DeckListModel(BaseModel):
    source: List[CardModel]
    target: List[CardModel]
