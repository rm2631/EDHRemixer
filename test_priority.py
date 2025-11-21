"""
Test script to verify priority system works correctly
"""

from models import Collection


def test_priority_default():
    """Test that collections get default priority of 3"""
    c = Collection(
        name="Test Collection", url="https://www.moxfield.com/decks/abc", is_source=True
    )
    assert c.priority == 3, f"Expected priority 3, got {c.priority}"
    print("✓ Default priority is 3")


def test_priority_custom():
    """Test that collections can have custom priority"""
    c = Collection(
        name="Test Collection",
        url="https://www.moxfield.com/decks/abc",
        is_source=True,
        priority=5,
    )
    assert c.priority == 5, f"Expected priority 5, got {c.priority}"
    print("✓ Custom priority works")


def test_priority_sorting():
    """Test that collections are sorted by priority correctly"""
    collections = [
        Collection(
            name="Low",
            url="https://www.moxfield.com/decks/a",
            is_source=True,
            priority=1,
        ),
        Collection(
            name="High",
            url="https://www.moxfield.com/decks/b",
            is_source=True,
            priority=5,
        ),
        Collection(
            name="Medium",
            url="https://www.moxfield.com/decks/c",
            is_source=True,
            priority=3,
        ),
    ]

    # Sort by priority (highest first)
    sorted_collections = sorted(collections, key=lambda c: c.priority, reverse=True)

    assert sorted_collections[0].name == "High", "High priority should be first"
    assert sorted_collections[1].name == "Medium", "Medium priority should be second"
    assert sorted_collections[2].name == "Low", "Low priority should be last"
    print("✓ Priority sorting works (highest to lowest)")


def test_priority_range():
    """Test that priority can be set to all valid values (1-5)"""
    for priority in range(1, 6):
        c = Collection(
            name=f"Priority {priority}",
            url=f"https://www.moxfield.com/decks/p{priority}",
            is_source=True,
            priority=priority,
        )
        assert c.priority == priority, f"Expected priority {priority}, got {c.priority}"
    print("✓ All priority values 1-5 work")


if __name__ == "__main__":
    print("Testing priority system...")
    test_priority_default()
    test_priority_custom()
    test_priority_sorting()
    test_priority_range()
    print("\n✅ All priority tests passed!")
