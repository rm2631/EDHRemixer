from pydantic import BaseModel, computed_field
from typing import List, Union


class Collection(BaseModel):
    name: str
    url: str
    is_source: bool
    priority: int = 3
    active: bool = True

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

    @computed_field
    @property
    def basic_land(self) -> bool:
        basic_land_names = [
            "plains",
            "island",
            "swamp",
            "mountain",
            "forest",
        ]
        return self.name.lower() in basic_land_names

    @computed_field
    @property
    def reshuffled(self) -> bool:
        return self.source is not None and self.target is not None

    @computed_field
    @property
    def ditched(self) -> bool:
        return self.source is not None and self.target is None

    @computed_field
    @property
    def buylist(self) -> bool:
        return self.source is None and self.target is not None
