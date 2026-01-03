"""
Quick test script for EDHRec overall inclusion functionality.
"""

from api.services.edhrec import get_card_overall_inclusion

# Test: Get overall inclusion for any card
card_name = "Sol Ring"
data = get_card_overall_inclusion(card_name)

if data:
    print(f"\n{'='*60}")
    print(f"Overall Inclusion for '{card_name}'")
    print(f"{'='*60}")
    print(f"Inclusion: {data['inclusion_percentage']}%")
    print(f"Used in: {data['num_decks']} decks")
    print(f"Total decks: {data['total_decks']} decks")
    print(f"URL: {data['url']}")
    print(f"{'='*60}\n")
else:
    print(f"Could not find data for '{card_name}'")
