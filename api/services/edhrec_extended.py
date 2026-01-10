"""
Extended EDHRec utilities for getting overall card inclusion statistics.

This module extends the pyedhrec library to provide overall inclusion percentages
for cards across all Commander decks, not just for specific commanders.
"""

import re
from typing import Optional, Dict
import requests
from bs4 import BeautifulSoup
from pyedhrec import EDHRec


class EDHRecExtended(EDHRec):
    """
    Extended EDHRec class that adds methods for getting overall card statistics.
    """

    def get_overall_card_inclusion(self, card_name: str) -> Optional[Dict]:
        """
        Get the overall inclusion percentage for a card across all Commander decks.

        This scrapes the EDHRec card page to extract the overall inclusion data
        that appears at the top of each card page.

        Args:
            card_name: Name of the card (e.g., "Sol Ring")

        Returns:
            Dictionary with overall inclusion data:
            {
                'card_name': str,
                'inclusion_percentage': float,
                'num_decks': str,  # e.g., "6.45M"
                'total_decks': str,  # e.g., "7.70M"
                'url': str
            }
            Returns None if the data cannot be found.

        Example:
            >>> edhrec = EDHRecExtended()
            >>> data = edhrec.get_overall_card_inclusion("Sol Ring")
            >>> print(f"{data['card_name']}: {data['inclusion_percentage']}%")
            Sol Ring: 83.8%
        """
        try:
            # Handle double-sided cards - only use the first part for URL
            card_name_for_url = card_name.split(" // ")[0].strip()

            # Get the card URL using the parent class method
            card_url = self.get_card_link(card_name_for_url)

            full_url = (
                card_url
                if card_url.startswith("http")
                else f"https://edhrec.com{card_url}"
            )

            # Fetch the page
            response = requests.get(full_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            page_text = soup.get_text()

            # Look for the pattern: "XX.X%inclusionX.XXM decksX.XXM decks"
            # The format is: percentage% inclusion num_decks decks total_decks decks
            inclusion_pattern = (
                r"([\d.]+)%\s*inclusion\s*([\d.]+[MK]?)\s*decks\s*([\d.]+[MK]?)\s*decks"
            )
            match = re.search(inclusion_pattern, page_text)

            if match:
                return {
                    "card_name": card_name,
                    "inclusion_percentage": float(match.group(1)),
                    "num_decks": match.group(2),
                    "total_decks": match.group(3),
                    "url": full_url,
                }
            else:
                print(
                    f"Warning: Could not find inclusion data for '{card_name}'. Continuing..."
                )
                return None

        except requests.RequestException as e:
            print(
                f"Error fetching data from EDHRec for '{card_name}': {e}. Continuing..."
            )
            return None
        except Exception as e:
            print(
                f"Unexpected error getting inclusion for '{card_name}': {e}. Continuing..."
            )
            return None

    def get_card_full_stats(
        self, card_name: str, commander_name: Optional[str] = None
    ) -> Dict:
        """
        Get comprehensive card statistics including both overall and commander-specific data.

        Args:
            card_name: Name of the card
            commander_name: Optional commander name for commander-specific stats

        Returns:
            Dictionary with both overall and commander-specific data (if commander provided)
        """
        result = {
            "card_name": card_name,
            "overall": self.get_overall_card_inclusion(card_name),
            "commander_specific": None,
        }

        if commander_name:
            # Get commander-specific data
            try:
                commander_cards = self.get_commander_cards(commander_name)
                for category, cards in commander_cards.items():
                    for card in cards:
                        if card["name"] == card_name:
                            inclusion_percent = (
                                card["num_decks"] / card["potential_decks"]
                            ) * 100
                            result["commander_specific"] = {
                                "commander": commander_name,
                                "category": category,
                                "inclusion_percentage": round(inclusion_percent, 2),
                                "num_decks": card["num_decks"],
                                "potential_decks": card["potential_decks"],
                                "synergy": card["synergy"],
                            }
                            break
                    if result["commander_specific"]:
                        break
            except Exception as e:
                print(f"Error getting commander-specific data: {e}")

        return result


def parse_deck_count(deck_str: str) -> int:
    """
    Parse deck count strings like "6.45M" or "170K" into integers.

    Args:
        deck_str: String like "6.45M", "170K", or "1234"

    Returns:
        Integer representation of the deck count

    Example:
        >>> parse_deck_count("6.45M")
        6450000
        >>> parse_deck_count("170K")
        170000
    """
    deck_str = deck_str.strip()
    if deck_str.endswith("M"):
        return int(float(deck_str[:-1]) * 1_000_000)
    elif deck_str.endswith("K"):
        return int(float(deck_str[:-1]) * 1_000)
    else:
        return int(deck_str)


# Example usage
if __name__ == "__main__":
    edhrec = EDHRecExtended()

    # Test 1: Get overall inclusion for a card
    print("=" * 70)
    print("Test 1: Overall Inclusion")
    print("=" * 70)
    card = "Sol Ring"
    data = edhrec.get_overall_card_inclusion(card)
    if data:
        print(f"Card: {data['card_name']}")
        print(f"Overall Inclusion: {data['inclusion_percentage']}%")
        print(f"Used in: {data['num_decks']} decks")
        print(f"Total decks: {data['total_decks']} decks")
        print(f"URL: {data['url']}")

        # Parse the deck counts
        num_decks = parse_deck_count(data["num_decks"])
        total_decks = parse_deck_count(data["total_decks"])
        print(f"\nParsed: {num_decks:,} / {total_decks:,} decks")

    print("\n" + "=" * 70)
    print("Test 2: Full Stats (Overall + Commander-Specific)")
    print("=" * 70)
    commander = "Atraxa, Praetors' Voice"
    full_stats = edhrec.get_card_full_stats(card, commander)

    print(f"\nCard: {full_stats['card_name']}")
    if full_stats["overall"]:
        print(f"\nOverall Inclusion: {full_stats['overall']['inclusion_percentage']}%")
        print(
            f"  ({full_stats['overall']['num_decks']} / {full_stats['overall']['total_decks']} decks)"
        )

    if full_stats["commander_specific"]:
        cs = full_stats["commander_specific"]
        print(f"\n{cs['commander']} Specific:")
        print(f"  Inclusion: {cs['inclusion_percentage']}%")
        print(f"  ({cs['num_decks']:,} / {cs['potential_decks']:,} decks)")
        print(f"  Synergy: {cs['synergy']:.2f}")
        print(f"  Category: {cs['category']}")
