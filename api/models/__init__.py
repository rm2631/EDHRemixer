from pydantic import BaseModel
from typing import List, Union


class Collection(BaseModel):
    name: str
    url: str
    is_source: bool

    @property
    def id(self) -> str:
        return self.url.split("/")[-1]

    @property
    def is_deck(self) -> bool:
        return "deck" in self.url.lower()

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Movement(BaseModel):
    source: Collection
    target: Collection
    intersection: int
    intersection_cards: List[str]


class Card(BaseModel):
    uniqueCardId: str
    name: str
    source: Union[Collection, None]
    target: Union[Collection, None]
    type_line: str
    color_identity: List[str]
    price_usd: float

    @property
    def basic_land(self):
        basic_land_names = [
            "plains",
            "island",
            "swamp",
            "mountain",
            "forest",
        ]
        return self.name.lower() in basic_land_names
