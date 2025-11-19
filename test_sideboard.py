"""
Test script to verify include_sideboard attribute works correctly
"""
from api.models import Collection

def test_sideboard_default():
    """Test that collections get default include_sideboard status of False"""
    c = Collection(
        name="Test Collection",
        url="https://www.moxfield.com/decks/abc",
        is_source=True
    )
    assert c.include_sideboard == False, f"Expected include_sideboard False, got {c.include_sideboard}"
    print("✓ Default include_sideboard status is False")

def test_sideboard_explicit_true():
    """Test that collections can be explicitly set to include sideboard"""
    c = Collection(
        name="Test Collection",
        url="https://www.moxfield.com/decks/abc",
        is_source=True,
        include_sideboard=True
    )
    assert c.include_sideboard == True, f"Expected include_sideboard True, got {c.include_sideboard}"
    print("✓ Explicit include_sideboard True works")

def test_sideboard_with_other_fields():
    """Test that include_sideboard works alongside other fields"""
    c = Collection(
        name="Test Collection",
        url="https://www.moxfield.com/decks/abc",
        is_source=True,
        priority=5,
        active=True,
        include_sideboard=True
    )
    assert c.priority == 5, f"Expected priority 5, got {c.priority}"
    assert c.active == True, f"Expected active True, got {c.active}"
    assert c.include_sideboard == True, f"Expected include_sideboard True, got {c.include_sideboard}"
    print("✓ Include_sideboard works with priority and active")

def test_filter_sideboard_collections():
    """Test that collections with sideboard enabled can be filtered"""
    collections = [
        Collection(name="No Sideboard", url="https://www.moxfield.com/decks/a", is_source=True, include_sideboard=False),
        Collection(name="With Sideboard", url="https://www.moxfield.com/decks/b", is_source=True, include_sideboard=True),
        Collection(name="Default", url="https://www.moxfield.com/decks/c", is_source=False),
    ]
    
    # Filter collections with sideboard
    with_sideboard = [c for c in collections if c.include_sideboard]
    
    assert len(with_sideboard) == 1, f"Expected 1 collection with sideboard, got {len(with_sideboard)}"
    assert with_sideboard[0].name == "With Sideboard", "Wrong collection filtered"
    print("✓ Filtering sideboard-enabled collections works")

if __name__ == "__main__":
    print("Testing include_sideboard attribute system...")
    test_sideboard_default()
    test_sideboard_explicit_true()
    test_sideboard_with_other_fields()
    test_filter_sideboard_collections()
    print("\n✅ All include_sideboard tests passed!")
