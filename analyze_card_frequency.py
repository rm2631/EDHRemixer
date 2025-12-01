"""
Script to analyze card frequencies across multiple Moxfield decks.
Excludes basic lands and shows which cards appear most frequently.
"""

from collections import Counter
from api.services.moxfield_connector import MoxfieldConnector

# List of basic land names to exclude
BASIC_LANDS = ["plains", "island", "swamp", "mountain", "forest"]


def analyze_card_frequency(
    deck_urls: list[str], include_sideboard: bool = False, min_frequency: int = 2
):
    """
    Analyze card frequencies across multiple decks.

    Args:
        deck_urls: List of Moxfield deck URLs
        include_sideboard: Whether to include sideboard cards in the analysis
        min_frequency: Minimum number of decks a card must appear in to be included

    Returns:
        Tuple of (Counter object with card names and frequencies, dict of card prices)
    """
    card_counter = Counter()
    card_prices = {}

    for url in deck_urls:
        # Extract deck ID from URL (last part after '/')
        deck_id = url.strip().split("/")[-1]

        try:
            print(f"Fetching deck: {deck_id}")
            deck_content = MoxfieldConnector.get_deck_content(
                deck_id, include_sideboard=include_sideboard
            )

            # Count each card (excluding basic lands)
            for card in deck_content:
                card_name = card["card"]["name"]
                if card_name.lower() not in BASIC_LANDS:
                    card_counter[card_name] += 1
                    # Store the price (will be the same for all instances)
                    if card_name not in card_prices:
                        price = card["card"].get("prices", {}).get("usd")
                        card_prices[card_name] = float(price) if price else 0.0

        except Exception as e:
            print(f"Error fetching deck {deck_id}: {e}")
            continue

    # Filter by minimum frequency
    filtered_counter = Counter(
        {k: v for k, v in card_counter.items() if v >= min_frequency}
    )

    return filtered_counter, card_prices


def print_top_cards(
    card_counter: Counter, card_prices: dict, top_n: int = 20, min_price: float = 0.0
):
    """Print the top N most frequent cards with prices."""
    print(f"\n{'='*80}")
    print(
        f"Top {top_n} Most Frequent Cards (excluding basic lands, min price: ${min_price:.2f})"
    )
    print(f"{'='*80}")
    print(f"{'Rank':<6} {'Count':<8} {'Price':<10} {'Card Name'}")
    print(f"{'-'*80}")

    printed_count = 0
    for card_name, count in card_counter.most_common():
        price = card_prices.get(card_name, 0.0)
        if price >= min_price:
            printed_count += 1
            print(f"{printed_count:<6} {count:<8} ${price:<9.2f} {card_name}")
            if printed_count >= top_n:
                break

    print(f"{'='*80}")
    print(f"Total unique cards (excluding basics, min freq): {len(card_counter)}")
    print(f"Total decks analyzed: {len(deck_urls)}")


if __name__ == "__main__":
    # Example deck URLs - Replace with your actual deck URLs
    deck_urls = [
        "https://moxfield.com/decks/OAn68gPqOkia62Is5U-MOw",
        "https://moxfield.com/decks/uU2g5R0GlUe4EC0dNGhFvA",
        "https://moxfield.com/decks/TXgOSSTqMEOilP-EObo_jQ",
        "https://moxfield.com/decks/MByVMsEgdkuGPu9tQ6FBbg",
        "https://moxfield.com/decks/xAcE-WdHqUqqxnHdjgLVWQ",
        "https://moxfield.com/decks/8Tj0hXVVcUO57xXTtmj2wA",
        "https://moxfield.com/decks/DROEU8URUk69Rqbl60k6Dg",
        "https://moxfield.com/decks/kGm5YIO4F0W1pGKiL2Sstw",
        "https://moxfield.com/decks/N7qnCL5PiEyjAQg2tWFh2g",
        "https://moxfield.com/decks/38J5tSDvG0Gy-A7zrhcu0g",
        "https://moxfield.com/decks/SHi_Z3wJTEKNRdRILLQ5UA",
    ]

    # Configuration
    MIN_FREQUENCY = 2  # Minimum number of decks a card must appear in
    MIN_PRICE = 5.0  # Minimum price in USD to consider a card "valuable"
    TOP_N = 30  # Number of top cards to show

    # Run the analysis
    print("Starting card frequency analysis...")
    card_counter, card_prices = analyze_card_frequency(
        deck_urls, include_sideboard=False, min_frequency=MIN_FREQUENCY
    )

    # Print results sorted by frequency
    print_top_cards(card_counter, card_prices, top_n=TOP_N, min_price=MIN_PRICE)
