from services.shuffle_manager import ShuffleManager
from models import Collection


def test_shuffle_manager():
    source_1 = Collection(
        name="Anzrag",
        url="https://www.moxfield.com/decks/c78MLCfSKEifjtEGU-Ty5A",
        is_source=False,
    )
    source_2 = Collection(
        name="A1",
        url="https://www.moxfield.com/binders/Zfx1zY2E8Eid4MbARdh6Gw",
        is_source=True,
    )

    shuffle_manager = ShuffleManager(inputs=[source_1, source_2])
    file = shuffle_manager.reshuffle()


if __name__ == "__main__":
    test_shuffle_manager()
