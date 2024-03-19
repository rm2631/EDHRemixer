from pydantic import BaseModel
from typing import List, Union


class CardModel(BaseModel):
    deck: str
    card_name: str
    quantity: int = 1


class DeckReshuffleModel(BaseModel):
    source: List[CardModel]
    target: List[CardModel]


class UnprocessedCardModel(BaseModel):
    quantity: int = 1
    card_name: str


class ProcessedCardModel(BaseModel):
    quantity: int = 1
    card_id: int
    card_name: str
    color_identity: List[str]
    error: str = None


class DeckModel(BaseModel):
    cards: Union[List[UnprocessedCardModel], List[ProcessedCardModel]]
