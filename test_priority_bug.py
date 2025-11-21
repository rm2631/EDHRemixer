"""
Test to reproduce the exact priority bug:
- High priority source with NO matching cards
- Low priority source with matching cards
- After checking high priority (no match), should continue to low priority
"""

from services.shuffle_manager import ShuffleManager
from api.models import Collection
from unittest.mock import MagicMock


def test_priority_bug_no_intersection():
    """
    Bug scenario:
    - High priority source (5) has cards X, Y (no match with target)
    - Low priority source (1) has cards A, B (matches with target)
    - Target needs cards A, B

    Expected: Cards A, B allocated from low priority source
    Actual Bug: Algorithm stops after checking high priority source (0 intersection)
    """

    mock_connector = MagicMock()

    # High priority source has cards that DON'T match target
    def get_binder_side_effect(id):
        if id == "high_priority_source":
            return [
                {
                    "quantity": 1,
                    "card": {
                        "uniqueCardId": "card_x",
                        "name": "Card X",
                        "type_line": "Creature",
                        "color_identity": [],
                        "prices": {"usd": "1.0"},
                    },
                },
                {
                    "quantity": 1,
                    "card": {
                        "uniqueCardId": "card_y",
                        "name": "Card Y",
                        "type_line": "Creature",
                        "color_identity": [],
                        "prices": {"usd": "1.0"},
                    },
                },
            ]
        elif id == "low_priority_source":
            return [
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
            ]

    mock_connector.get_binder_content.side_effect = get_binder_side_effect

    # Target needs cards A and B (which are in low priority source)
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
    print(f"\n=== Results ===")
    print(f"Allocated cards: {len(manager.allocated_cards)}")
    print(f"Available cards remaining: {len(manager.available_cards)}")
    print(f"Required cards remaining: {len(manager.required_cards)}")

    if manager.allocated_cards:
        print(f"\nAllocated:")
        for card in manager.allocated_cards:
            print(f"  ✓ {card.name} from {card.source.name} to {card.target.name}")

    if manager.available_cards:
        print(f"\nStill available (not allocated):")
        for card in manager.available_cards:
            print(f"  • {card.name} from {card.source.name}")

    if manager.required_cards:
        print(f"\nStill required (not fulfilled):")
        for card in manager.required_cards:
            print(f"  ✗ {card.name} for {card.target.name}")

    # Should allocate cards A and B from low priority source
    if len(manager.allocated_cards) == 2:
        print("\n✅ Test passed: Cards allocated from low priority source")
    else:
        print(
            f"\n❌ BUG REPRODUCED: Expected 2 allocated cards, got {len(manager.allocated_cards)}"
        )
        print(
            "The algorithm stopped after checking high priority source with 0 intersection!"
        )


if __name__ == "__main__":
    test_priority_bug_no_intersection()
