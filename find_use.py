from pyedhrec import EDHRec
import json
import requests
from bs4 import BeautifulSoup


edhrec = EDHRec()

# Let's try to inspect the EDHRec API calls directly
card_to_find = "Sol Ring"

# First, let's see what URL EDHRec uses
card_url = edhrec.get_card_link(card_to_find)
print(f"Card URL: {card_url}")

# Check if we can access the card page directly
print(f"\nAttempting to scrape overall inclusion from EDHREC page...")
try:
    # If the URL already starts with https, use it as is, otherwise prepend the domain
    full_url = (
        card_url if card_url.startswith("http") else f"https://edhrec.com{card_url}"
    )
    print(f"Fetching: {full_url}")

    response = requests.get(full_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # The page structure shows: "83.8%inclusion6.45M decks7.70M decks"
    # Let's find this data
    page_text = soup.get_text()

    # Look for percentage pattern
    import re

    inclusion_pattern = (
        r"([\d.]+)%\s*inclusion\s*([\d.]+[MK]?)\s*decks\s*([\d.]+[MK]?)\s*decks"
    )
    match = re.search(inclusion_pattern, page_text)

    if match:
        print(f"\n{'='*60}")
        print(f"OVERALL INCLUSION DATA FOR '{card_to_find}':")
        print(f"{'='*60}")
        print(f"Inclusion: {match.group(1)}%")
        print(f"Used in: {match.group(2)} decks")
        print(f"Total decks: {match.group(3)} decks")
        print(f"{'='*60}")
    else:
        print("Could not find inclusion pattern in page")
except Exception as e:
    print(f"Error scraping: {e}")

print("\n" + "=" * 80 + "\n")

# Now try the old method for comparison
commander = "Atraxa, Praetors' Voice"
print(f"Getting card data for '{commander}' (commander-specific)...\n")
commander_cards = edhrec.get_commander_cards(commander)

# Search for our card in all categories
found = False
for category, cards in commander_cards.items():
    for card in cards:
        if card["name"] == card_to_find:
            found = True
            print(f"Found '{card_to_find}' in category: {category}")
            print(f"\nCard data:")
            print(json.dumps(card, indent=2))

            # Calculate inclusion percentage
            inclusion_percent = (card["num_decks"] / card["potential_decks"]) * 100
            print(f"\n{'='*60}")
            print(f"INCLUSION PERCENTAGE: {inclusion_percent:.2f}%")
            print(f"{'='*60}")
            print(
                f"Used in {card['num_decks']:,} out of {card['potential_decks']:,} decks"
            )
            print(f"Synergy score: {card['synergy']:.2f}")
            break
    if found:
        break

if not found:
    print(f"\n'{card_to_find}' not found in top cards for this commander.")
    print("It might be in the average decklist. Let me check...")

    avg_deck = edhrec.get_commanders_average_deck(commander)
    if any(card_to_find in card for card in avg_deck["decklist"]):
        print(f"✓ '{card_to_find}' is in the average decklist")
        print(
            "\nNote: Inclusion % is only available for cards in the 'top cards' lists,"
        )
        print("not for cards in the basic average decklist.")
