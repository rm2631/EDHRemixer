from api.services.edhrec import get_average_deck
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add the api directory to the path so we can import the moxfield connector
from api.services.moxfield_connector import MoxfieldConnector


def get_my_collection(binder_ids: list[str]) -> tuple[set[str], list[dict]]:
    """
    Fetch all cards from the given Moxfield binder IDs and return a set of card names
    and the full card data for legendary creatures.
    """
    collection = set()
    all_cards_data = []

    for binder_id in binder_ids:
        print(f"Fetching binder: {binder_id}")
        cards = MoxfieldConnector.get_binder_content(binder_id)

        for card in cards:
            # Get the card name from the binder response
            card_name = card.get("card", {}).get("name", "")
            if card_name:
                collection.add(card_name)

            # Store full card data for filtering legendary creatures later
            all_cards_data.append(card)

        print(f"  Added {len(cards)} cards")

    print(f"\nTotal unique cards in collection: {len(collection)}")
    return collection, all_cards_data


def get_legendary_creatures(cards_data: list[dict]) -> list[str]:
    """
    Filter cards to get unique legendary creatures that can be commanders.
    """
    legendary_creatures = set()

    for card_entry in cards_data:
        card = card_entry.get("card", {})
        type_line = card.get("type_line", "").lower()

        # Check if it's a legendary creature
        if "legendary" in type_line and "creature" in type_line:
            card_name = card.get("name", "")
            if card_name:
                legendary_creatures.add(card_name)

    return sorted(list(legendary_creatures))


def analyze_commander(commander_name: str, my_collection: set[str]) -> dict:
    """
    Analyze a single commander against your collection.
    Returns simplified results with just the key metrics.
    """
    try:
        average_deck = get_average_deck(commander_name)

        owned_count = 0
        total_count = 0

        for card in average_deck.cards:
            if card.basic_land:
                continue

            total_count += 1
            if card.name in my_collection:
                owned_count += 1

        completion_percentage = (
            round(owned_count / total_count * 100, 2) if total_count > 0 else 0
        )

        return {
            "commander": commander_name,
            "total_cards": total_count,
            "owned_count": owned_count,
            "missing_count": total_count - owned_count,
            "completion_percentage": completion_percentage,
            "success": True,
        }
    except Exception as e:
        return {"commander": commander_name, "error": str(e), "success": False}


def find_missing_cards(commander_name: str, my_collection: set[str]) -> dict:
    """
    Compare the EDHREC average deck for a commander against your collection
    and return which cards you're missing.
    """
    average_deck = get_average_deck(commander_name)

    missing_cards = []
    owned_cards = []

    for card in average_deck.cards:
        if card.basic_land:
            # Skip basic lands
            continue

        if card.name not in my_collection:
            missing_cards.append(card)
        else:
            owned_cards.append(card)

    return {
        "commander": commander_name,
        "total_cards": len([c for c in average_deck.cards if not c.basic_land]),
        "owned_count": len(owned_cards),
        "missing_count": len(missing_cards),
        "missing_cards": missing_cards,
        "owned_cards": owned_cards,
        "completion_percentage": (
            round(
                len(owned_cards)
                / len([c for c in average_deck.cards if not c.basic_land])
                * 100,
                2,
            )
            if average_deck.cards
            else 0
        ),
    }


def analyze_commanders_parallel(
    commanders: list[str], my_collection: set[str], max_workers: int = 10
) -> list[dict]:
    """
    Analyze multiple commanders in parallel using ThreadPoolExecutor.
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_commander = {
            executor.submit(analyze_commander, commander, my_collection): commander
            for commander in commanders
        }

        # Process completed tasks as they finish
        for future in as_completed(future_to_commander):
            commander = future_to_commander[future]
            try:
                result = future.result()
                results.append(result)

                if result["success"]:
                    print(
                        f"✓ Analyzed: {commander} ({result['completion_percentage']}% owned)"
                    )
                else:
                    print(
                        f"✗ Failed: {commander} - {result.get('error', 'Unknown error')}"
                    )
            except Exception as e:
                print(f"✗ Exception for {commander}: {str(e)}")
                results.append(
                    {"commander": commander, "error": str(e), "success": False}
                )

    return results


if __name__ == "__main__":
    # Your Moxfield binder IDs
    binder_ids = ["ARQDBqtjJ0a-MnEQM6YTag", "t6czXPnSHUaskiLumeDzgg"]

    # Fetch your collection
    print("=" * 60)
    print("Fetching your collection from Moxfield...")
    print("=" * 60)
    my_collection, all_cards_data = get_my_collection(binder_ids)

    # Find all legendary creatures in the collection
    print("\n" + "=" * 60)
    print("Finding legendary creatures in your collection...")
    print("=" * 60)
    legendary_creatures = get_legendary_creatures(all_cards_data)
    print(f"Found {len(legendary_creatures)} unique legendary creatures")

    # Limit to top 10 for now
    commanders_to_analyze = legendary_creatures

    print(f"\nAnalyzing top {len(commanders_to_analyze)} commanders:")
    for i, commander in enumerate(commanders_to_analyze, 1):
        print(f"  {i}. {commander}")

    # Analyze commanders in parallel
    print("\n" + "=" * 60)
    print("Analyzing commanders (parallelized)...")
    print("=" * 60)
    results = analyze_commanders_parallel(commanders_to_analyze, my_collection)

    # Filter successful results and sort by completion percentage
    successful_results = [r for r in results if r["success"]]
    successful_results.sort(key=lambda x: x["completion_percentage"], reverse=True)

    # Display results
    print("\n" + "=" * 60)
    print("RESULTS - SORTED BY COMPLETION %")
    print("=" * 60)
    print(f"{'Rank':<6}{'Commander':<35}{'Owned':<8}{'Total':<8}{'Complete':<10}")
    print("-" * 60)

    for i, result in enumerate(successful_results, 1):
        print(
            f"{i:<6}"
            f"{result['commander']:<35}"
            f"{result['owned_count']:<8}"
            f"{result['total_cards']:<8}"
            f"{result['completion_percentage']}%"
        )

    # Show failures if any
    failed_results = [r for r in results if not r["success"]]
    if failed_results:
        print("\n" + "=" * 60)
        print("FAILED ANALYSES")
        print("=" * 60)
        for result in failed_results:
            print(f"  {result['commander']}: {result.get('error', 'Unknown error')}")
