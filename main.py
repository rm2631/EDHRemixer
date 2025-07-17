# Import necessary libraries
from models import Collection
from services.shuffle_manager import ShuffleManager
from typing import List


def run(inputs: List[Collection]):
    """
    Function to run the shuffle manager with given inputs.
    Returns the reshuffled xlsx file.
    """

    manager = ShuffleManager(inputs)
    file = manager.reshuffle()
    return file
