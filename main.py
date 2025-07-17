# Import necessary libraries
from models import Collection
from services.shuffle_manager import ShuffleManager
from typing import List


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
