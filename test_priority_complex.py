"""
Comprehensive test for priority-based allocation with edge cases
"""

from services.shuffle_manager import ShuffleManager
from models import Collection
from unittest.mock import MagicMock


def test_complex_priority_scenario():
    """
    Test a complex scenario with multiple sources at different priorities:
    - Source P5 (priority 5): Cards X, Y (no match)
    - Source P4 (priority 4): Cards A, B (matches target 1)
    - Source P2 (priority 2): Cards C, D (matches target 2)
    - Target 1 (priority 5): needs A, B
    - Target 2 (priority 3): needs C, D

    Expected behavior:
    1. Check P5 source first (highest priority) - no match, skip
    2. Check P4 source - matches T1, allocate A, B
    3. Check P2 source - matches T2, allocate C, D

    All cards should be allocated despite P5 having no matches.
    """

    mock_connector = MagicMock()

    def get_binder_side_effect(id):
        return {
            "source_p5": [
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
            ],
            "source_p4": [
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
            "source_p2": [
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

    def get_deck_side_effect(id, include_sideboard):
        return {
            "target_1": [
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
            "target_2": [
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

    mock_connector.get_binder_content.side_effect = get_binder_side_effect
    mock_connector.get_deck_content.side_effect = get_deck_side_effect

    source_p5 = Collection(
        name="Source P5",
        url="https://www.moxfield.com/binders/source_p5",
        is_source=True,
        priority=5,
    )

    source_p4 = Collection(
        name="Source P4",
        url="https://www.moxfield.com/binders/source_p4",
        is_source=True,
        priority=4,
    )

    source_p2 = Collection(
        name="Source P2",
        url="https://www.moxfield.com/binders/source_p2",
        is_source=True,
        priority=2,
    )

    target_1 = Collection(
        name="Target 1",
        url="https://www.moxfield.com/decks/target_1",
        is_source=False,
        priority=5,
    )

    target_2 = Collection(
        name="Target 2",
        url="https://www.moxfield.com/decks/target_2",
        is_source=False,
        priority=3,
    )

    manager = ShuffleManager(
        inputs=[source_p5, source_p4, source_p2, target_1, target_2],
        moxfield_connector=mock_connector,
    )

    manager.reshuffle()

    print("\n=== Complex Priority Scenario Results ===")
    print(f"Total allocated: {len(manager.allocated_cards)}")
    print(f"Still available: {len(manager.available_cards)}")
    print(f"Still required: {len(manager.required_cards)}")

    print("\nAllocations by source:")
    for source in [source_p5, source_p4, source_p2]:
        allocated_from_source = [
            c for c in manager.allocated_cards if c.source == source
        ]
        print(
            f"  {source.name} (P{source.priority}): {len(allocated_from_source)} cards"
        )
        for card in allocated_from_source:
            print(f"    → {card.name} to {card.target.name}")

    print("\nUnallocated cards:")
    for card in manager.available_cards:
        print(f"  • {card.name} from {card.source.name} (unused)")

    # Verify results
    assert (
        len(manager.allocated_cards) == 4
    ), f"Expected 4 allocated, got {len(manager.allocated_cards)}"
    assert (
        len(manager.available_cards) == 2
    ), f"Expected 2 available (X, Y), got {len(manager.available_cards)}"
    assert (
        len(manager.required_cards) == 0
    ), f"Expected 0 required, got {len(manager.required_cards)}"

    # Verify P4 allocated before P2 (respecting priority)
    p4_cards = [c for c in manager.allocated_cards if c.source == source_p4]
    p2_cards = [c for c in manager.allocated_cards if c.source == source_p2]
    assert len(p4_cards) == 2, "Should allocate 2 cards from P4"
    assert len(p2_cards) == 2, "Should allocate 2 cards from P2"

    print("\n✅ Complex priority test passed!")
    print("   • High-priority source with no matches was correctly skipped")
    print("   • Medium-priority and low-priority sources were both processed")
    print("   • All available matches were allocated")


if __name__ == "__main__":
    test_complex_priority_scenario()
