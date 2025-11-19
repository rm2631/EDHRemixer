"""
Test script to verify ShuffleManager respects active attribute
"""
from api.models import Collection
from api.services.shuffle_manager import ShuffleManager
from unittest.mock import MagicMock

def test_shuffle_manager_filters_inactive():
    """Test that ShuffleManager ignores inactive collections"""
    # Create mock collections
    active_source = Collection(
        name="Active Source",
        url="https://www.moxfield.com/decks/active_source",
        is_source=True,
        active=True
    )
    
    inactive_source = Collection(
        name="Inactive Source",
        url="https://www.moxfield.com/decks/inactive_source",
        is_source=True,
        active=False
    )
    
    active_target = Collection(
        name="Active Target",
        url="https://www.moxfield.com/decks/active_target",
        is_source=False,
        active=True
    )
    
    inactive_target = Collection(
        name="Inactive Target",
        url="https://www.moxfield.com/decks/inactive_target",
        is_source=False,
        active=False
    )
    
    # Mock the moxfield connector to avoid actual API calls
    mock_connector = MagicMock()
    mock_connector.get_deck_content = MagicMock(return_value=[])
    
    # Create ShuffleManager with both active and inactive collections
    collections = [active_source, inactive_source, active_target, inactive_target]
    manager = ShuffleManager(inputs=collections, moxfield_connector=mock_connector)
    
    # Verify that get_deck_content was only called for active collections
    assert mock_connector.get_deck_content.call_count == 2, \
        f"Expected 2 calls (only active collections), got {mock_connector.get_deck_content.call_count}"
    
    print("✓ ShuffleManager only processes active collections")

def test_shuffle_manager_all_active():
    """Test that ShuffleManager processes all collections when all are active"""
    collections = [
        Collection(name="Source1", url="https://www.moxfield.com/decks/s1", is_source=True, active=True),
        Collection(name="Source2", url="https://www.moxfield.com/decks/s2", is_source=True, active=True),
        Collection(name="Target1", url="https://www.moxfield.com/decks/t1", is_source=False, active=True),
    ]
    
    mock_connector = MagicMock()
    mock_connector.get_deck_content = MagicMock(return_value=[])
    
    manager = ShuffleManager(inputs=collections, moxfield_connector=mock_connector)
    
    assert mock_connector.get_deck_content.call_count == 3, \
        f"Expected 3 calls (all active), got {mock_connector.get_deck_content.call_count}"
    
    print("✓ ShuffleManager processes all collections when all are active")

def test_shuffle_manager_all_inactive():
    """Test that ShuffleManager handles all inactive collections gracefully"""
    collections = [
        Collection(name="Source1", url="https://www.moxfield.com/decks/s1", is_source=True, active=False),
        Collection(name="Target1", url="https://www.moxfield.com/decks/t1", is_source=False, active=False),
    ]
    
    mock_connector = MagicMock()
    mock_connector.get_deck_content = MagicMock(return_value=[])
    
    manager = ShuffleManager(inputs=collections, moxfield_connector=mock_connector)
    
    assert mock_connector.get_deck_content.call_count == 0, \
        f"Expected 0 calls (all inactive), got {mock_connector.get_deck_content.call_count}"
    
    print("✓ ShuffleManager handles all inactive collections (processes none)")

if __name__ == "__main__":
    print("Testing ShuffleManager with active attribute...")
    test_shuffle_manager_filters_inactive()
    test_shuffle_manager_all_active()
    test_shuffle_manager_all_inactive()
    print("\n✅ All ShuffleManager active attribute tests passed!")
