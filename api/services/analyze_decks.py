from edhrec import get_average_deck
import pandas as pd
from typing import Dict, Set
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def calculate_deck_similarity(deck1_cards: Set[str], deck2_cards: Set[str]) -> float:
    """
    Calculate Jaccard similarity coefficient between two decks.
    Returns a value between 0 and 1, where 1 means identical decks.
    """
    if not deck1_cards or not deck2_cards:
        return 0.0

    intersection = len(deck1_cards & deck2_cards)
    union = len(deck1_cards | deck2_cards)

    return intersection / union if union > 0 else 0.0


def analyze_commander_redundancy(
    commanders: list[str], debug: bool = False
) -> pd.DataFrame:
    """
    Analyze redundancy across commanders by calculating pairwise similarity.
    Returns a DataFrame matrix showing similarity scores.
    """
    print("Fetching average decks from EDHREC...")

    # Fetch all decks
    decks: Dict[str, Set[str]] = {}
    for commander in commanders:
        try:
            print(f"  Fetching deck for: {commander}")
            deck = get_average_deck(commander)
            # Store non-basic land card names as a set
            decks[commander] = {card.name for card in deck.cards if not card.basic_land}
            print(f"    ✓ Fetched {len(decks[commander])} cards")

            if debug and decks[commander]:
                sample_cards = list(decks[commander])[:5]
                print(f"    Sample cards: {', '.join(sample_cards)}")
        except Exception as e:
            print(f"    ✗ Error fetching {commander}: {e}")
            decks[commander] = set()

    # Create pairwise similarity matrix
    print("\nCalculating pairwise similarities...")

    # Filter out failed fetches
    failed_commanders = [cmd for cmd, cards in decks.items() if not cards]
    if failed_commanders:
        print(
            f"\n⚠️  WARNING: {len(failed_commanders)} commander(s) failed to fetch and will show 0% similarity:"
        )
        for cmd in failed_commanders:
            print(f"   - {cmd}")

    # Check for common cards across all successful decks
    if debug:
        successful_decks = {k: v for k, v in decks.items() if v}
        if len(successful_decks) >= 2:
            all_cards = set.intersection(*successful_decks.values())
            print(
                f"\nCards in ALL {len(successful_decks)} successful decks: {len(all_cards)}"
            )
            if all_cards:
                common_cards = sorted(all_cards)
                print(f"Universal cards: {', '.join(common_cards)}")

    n = len(commanders)
    similarity_matrix = []

    for i, cmd1 in enumerate(commanders):
        row = []
        for j, cmd2 in enumerate(commanders):
            if i == j:
                # Diagonal: same commander
                similarity = 1.0
            else:
                similarity = calculate_deck_similarity(decks[cmd1], decks[cmd2])
            row.append(similarity)
        similarity_matrix.append(row)

    # Create DataFrame
    df = pd.DataFrame(similarity_matrix, index=commanders, columns=commanders)

    return df


def plot_redundancy_heatmap(
    redundancy_matrix: pd.DataFrame,
    output_file: str = "commander_redundancy_heatmap.png",
):
    """
    Create a heatmap visualization of the commander redundancy matrix.
    """
    # Set up the matplotlib figure
    plt.figure(figsize=(12, 10))

    # Create a mask for the diagonal to hide 1.0 values
    mask = np.eye(len(redundancy_matrix), dtype=bool)

    # Calculate max value excluding diagonal for better color scaling
    max_similarity = redundancy_matrix.values[~mask].max()

    # Create the heatmap
    sns.heatmap(
        redundancy_matrix,
        annot=True,  # Show values in cells
        fmt=".3f",  # Format numbers to 3 decimal places
        cmap="YlOrRd",  # Yellow-Orange-Red colormap
        square=True,  # Make cells square
        linewidths=0.5,  # Add gridlines
        cbar_kws={"label": "Jaccard Similarity"},
        vmin=0,
        vmax=max_similarity,  # Adaptive max based on actual data
        mask=mask,  # Hide diagonal values (1.0)
    )

    plt.title(
        "Commander Deck Redundancy Matrix\n(Jaccard Similarity Index)",
        fontsize=16,
        pad=20,
    )
    plt.xlabel("Commander", fontsize=12)
    plt.ylabel("Commander", fontsize=12)

    # Rotate labels for better readability
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save the figure
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"\n📊 Heatmap saved to: {output_file}")

    # Display the plot
    plt.show()


if __name__ == "__main__":
    # Example usage - Add more commanders to see better redundancy analysis
    commanders = [
        "Hashaton, Scarab's Fist",
        "Henzie 'Toolbox' Torre",
        "Clavileno, First of the Blessed",
        "Cloud, Ex-SOLDIER",
        "Tidus, Yuna's Guardian",
        "Vraska, the Silencer",
        "Aragorn, the Uniter",
        "Captain America, First Avenger",
        "Octavia, Living Thesis",
        "Ovika, Enigma Goliath",
        "Shilgengar, Sire of Famine",
        "Zurgo Stormrender",
        "Lightning, Army of One",
        "Gisa, the Hellraiser",
    ]

    # Analyze redundancy
    redundancy_matrix = analyze_commander_redundancy(commanders, debug=True)

    # Display results
    print("\n" + "=" * 80)
    print("COMMANDER REDUNDANCY MATRIX")
    print("=" * 80)
    print("\nPairwise Similarity Scores (Jaccard Index):")
    print("1.0 = Identical decks, 0.0 = No overlap\n")

    # Format for better readability
    print(redundancy_matrix.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 80)
    print("\nSummary Statistics:")
    print("=" * 80)

    # Get upper triangle (excluding diagonal) for summary stats
    import numpy as np

    mask = np.triu(np.ones_like(redundancy_matrix, dtype=bool), k=1)
    similarities = redundancy_matrix.where(mask).stack().values

    if len(similarities) > 0:
        print(f"Average similarity: {similarities.mean():.3f}")
        print(f"Maximum similarity: {similarities.max():.3f}")
        print(f"Minimum similarity: {similarities.min():.3f}")

        # Find most and least similar pairs
        max_idx = similarities.argmax()
        min_idx = similarities.argmin()

        pairs = [
            (commanders[i], commanders[j])
            for i in range(len(commanders))
            for j in range(i + 1, len(commanders))
        ]

        print(
            f"\nMost similar pair: {pairs[max_idx][0]} <-> {pairs[max_idx][1]} ({similarities[max_idx]:.3f})"
        )
        print(
            f"Least similar pair: {pairs[min_idx][0]} <-> {pairs[min_idx][1]} ({similarities[min_idx]:.3f})"
        )

    # Generate heatmap visualization
    plot_redundancy_heatmap(redundancy_matrix)
