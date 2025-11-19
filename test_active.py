"""
Test script to verify active attribute works correctly
"""
from api.models import Collection

def test_active_default():
    """Test that collections get default active status of True"""
    c = Collection(
        name="Test Collection",
        url="https://www.moxfield.com/decks/abc",
        is_source=True
    )
    assert c.active == True, f"Expected active True, got {c.active}"
    print("✓ Default active status is True")

def test_active_explicit():
    """Test that collections can be explicitly set to inactive"""
    c = Collection(
        name="Test Collection",
        url="https://www.moxfield.com/decks/abc",
        is_source=True,
        active=False
    )
    assert c.active == False, f"Expected active False, got {c.active}"
    print("✓ Explicit inactive status works")

def test_active_with_priority():
    """Test that active works alongside priority"""
    c = Collection(
        name="Test Collection",
        url="https://www.moxfield.com/decks/abc",
        is_source=True,
        priority=5,
        active=False
    )
    assert c.priority == 5, f"Expected priority 5, got {c.priority}"
    assert c.active == False, f"Expected active False, got {c.active}"
    print("✓ Active and priority work together")

def test_filter_inactive_collections():
    """Test that inactive collections can be filtered out"""
    collections = [
        Collection(name="Active", url="https://www.moxfield.com/decks/a", is_source=True, active=True),
        Collection(name="Inactive", url="https://www.moxfield.com/decks/b", is_source=True, active=False),
        Collection(name="Active2", url="https://www.moxfield.com/decks/c", is_source=False, active=True),
    ]
    
    # Filter active collections
    active_collections = [c for c in collections if c.active]
    
    assert len(active_collections) == 2, f"Expected 2 active collections, got {len(active_collections)}"
    assert all(c.active for c in active_collections), "All filtered collections should be active"
    assert "Inactive" not in [c.name for c in active_collections], "Inactive collection should be filtered out"
    print("✓ Filtering inactive collections works")

if __name__ == "__main__":
    print("Testing active attribute system...")
    test_active_default()
    test_active_explicit()
    test_active_with_priority()
    test_filter_inactive_collections()
    print("\n✅ All active attribute tests passed!")
