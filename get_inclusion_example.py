"""
Example of using the extended EDHRec functionality to get card inclusion data.
"""

from api.services.edhrec import get_card_overall_inclusion, get_card_commander_inclusion


def main():
    # Example 1: Get overall inclusion across all decks
    print("=" * 70)
    print("Example 1: Overall Inclusion (All Decks)")
    print("=" * 70)

    card = "Sol Ring"
    overall_data = get_card_overall_inclusion(card)

    if overall_data:
        print(f"Card: {overall_data['card_name']}")
        print(f"Overall Inclusion: {overall_data['inclusion_percentage']}%")
        print(f"Used in: {overall_data['num_decks']} decks")
        print(f"Total decks: {overall_data['total_decks']} decks")
        print(f"URL: {overall_data['url']}")
    else:
        print(f"Could not find data for '{card}'")

    # Example 2: Get commander-specific inclusion
    print("\n" + "=" * 70)
    print("Example 2: Commander-Specific Inclusion")
    print("=" * 70)

    commander = "Atraxa, Praetors' Voice"
    commander_data = get_card_commander_inclusion(card, commander)

    if commander_data:
        print(f"Card: {commander_data['card_name']}")
        print(f"Commander: {commander_data['commander']}")
        print(f"Inclusion: {commander_data['inclusion_percentage']}%")
        print(
            f"Used in {commander_data['num_decks']:,} of {commander_data['potential_decks']:,} decks"
        )
        print(f"Synergy: {commander_data['synergy']:.2f}")
        print(f"Category: {commander_data['category']}")
    else:
        print(f"'{card}' not found in top cards for '{commander}'")

    # Example 3: Compare multiple cards
    print("\n" + "=" * 70)
    print("Example 3: Comparing Multiple Cards")
    print("=" * 70)

    cards_to_compare = ["Sol Ring", "Arcane Signet", "Command Tower", "Mana Crypt"]

    print(f"{'Card':<20} {'Overall %':>12} {'Decks':>15}")
    print("-" * 70)

    for card_name in cards_to_compare:
        data = get_card_overall_inclusion(card_name)
        if data:
            print(
                f"{card_name:<20} {data['inclusion_percentage']:>11.1f}% {data['num_decks']:>15}"
            )


if __name__ == "__main__":
    main()
