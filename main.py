# Import necessary libraries
from models import Collection
from services.shuffle_manager import ShuffleManager
from services.moxfield_connector import MoxfieldConnector
from typing import List


def get_deck_name(url: str) -> str:
    """
    Extracts and returns the deck name from a given Moxfield URL.
    """
    id = url.split("/")[-1]
    deck_name = MoxfieldConnector.get_deck_name(id)
    return deck_name


def run(inputs: List[dict]):
    """
    Function to run the shuffle manager with given inputs.
    Returns the reshuffled xlsx file.
    """
    inputs = [Collection(**input_data) for input_data in inputs]
    if not all(["moxfield" in input_data.url for input_data in inputs]):
        raise ValueError("All URLs must be from Moxfield.")
    manager = ShuffleManager(inputs)
    file = manager.reshuffle()
    return file
