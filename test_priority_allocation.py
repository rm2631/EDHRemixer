"""
Test to verify that priority allocation continues after high-priority source is exhausted
"""

from services.shuffle_manager import ShuffleManager
from models import Collection, Card
from unittest.mock import MagicMock


def test_multi_priority_allocation():
    """
    Test scenario:
    - High priority source (5) with 2 cards
    - Low priority source (1) with 2 cards
    - Target needs 4 cards (2 from high, 2 from low)

    Expected: All 4 cards should be allocated (2 from high priority, then 2 from low priority)
    Bug: After high priority source exhausted, low priority cards not allocated
    """

    # Create mock connector
    mock_connector = MagicMock()

    # High priority source has Card A and Card B
    mock_connector.get_binder_content.side_effect = lambda id: {
        "high_priority_source": [
            {
                "quantity": 1,
                "card": {
                    "uniqueCardId": "card_a",
                    "name": "Card A",
                    "type_line": "Creature",
                    "color_identity": [],
                    "prices": {"usd": "1.0"},
                },
            },
            {
                "quantity": 1,
                "card": {
                    "uniqueCardId": "card_b",
                    "name": "Card B",
                    "type_line": "Creature",
                    "color_identity": [],
                    "prices": {"usd": "1.0"},
                },
            },
        ],
        "low_priority_source": [
            {
                "quantity": 1,
                "card": {
                    "uniqueCardId": "card_c",
                    "name": "Card C",
                    "type_line": "Creature",
                    "color_identity": [],
                    "prices": {"usd": "1.0"},
                },
            },
            {
                "quantity": 1,
                "card": {
                    "uniqueCardId": "card_d",
                    "name": "Card D",
                    "type_line": "Creature",
                    "color_identity": [],
                    "prices": {"usd": "1.0"},
                },
            },
        ],
    }[id]

    # Target needs all 4 cards
    mock_connector.get_deck_content.return_value = [
        {
            "quantity": 1,
            "card": {
                "uniqueCardId": "card_a",
                "name": "Card A",
                "type_line": "Creature",
                "color_identity": [],
                "prices": {"usd": "1.0"},
            },
        },
        {
            "quantity": 1,
            "card": {
                "uniqueCardId": "card_b",
                "name": "Card B",
                "type_line": "Creature",
                "color_identity": [],
                "prices": {"usd": "1.0"},
            },
        },
        {
            "quantity": 1,
            "card": {
                "uniqueCardId": "card_c",
                "name": "Card C",
                "type_line": "Creature",
                "color_identity": [],
                "prices": {"usd": "1.0"},
            },
        },
        {
            "quantity": 1,
            "card": {
                "uniqueCardId": "card_d",
                "name": "Card D",
                "type_line": "Creature",
                "color_identity": [],
                "prices": {"usd": "1.0"},
            },
        },
    ]

    high_priority_source = Collection(
        name="High Priority Source",
        url="https://www.moxfield.com/binders/high_priority_source",
        is_source=True,
        priority=5,
    )

    low_priority_source = Collection(
        name="Low Priority Source",
        url="https://www.moxfield.com/binders/low_priority_source",
        is_source=True,
        priority=1,
    )

    target = Collection(
        name="Target Deck",
        url="https://www.moxfield.com/decks/target",
        is_source=False,
        priority=3,
    )

    manager = ShuffleManager(
        inputs=[high_priority_source, low_priority_source, target],
        moxfield_connector=mock_connector,
    )

    manager.reshuffle()

    # Check allocations
    print(f"\nAllocated cards: {len(manager.allocated_cards)}")
    print(f"Available cards remaining: {len(manager.available_cards)}")
    print(f"Required cards remaining: {len(manager.required_cards)}")

    for card in manager.allocated_cards:
        print(f"  - {card.name} from {card.source.name} to {card.target.name}")

    print(f"\nRemaining available:")
    for card in manager.available_cards:
        print(f"  - {card.name} from {card.source.name}")

    print(f"\nRemaining required:")
    for card in manager.required_cards:
        print(f"  - {card.name} for {card.target.name}")

    # All 4 cards should be allocated
    assert (
        len(manager.allocated_cards) == 4
    ), f"Expected 4 allocated cards, got {len(manager.allocated_cards)}"
    assert (
        len(manager.available_cards) == 0
    ), f"Expected 0 available cards, got {len(manager.available_cards)}"
    assert (
        len(manager.required_cards) == 0
    ), f"Expected 0 required cards, got {len(manager.required_cards)}"

    print("\n✅ Test passed: All cards allocated correctly across priority levels")


if __name__ == "__main__":
    test_multi_priority_allocation()
