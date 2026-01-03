# EDHRec Extended - Overall Inclusion Support

## Summary

The `pyedhrec` library doesn't directly provide **overall inclusion percentages** (the big metric shown on EDHRec card pages). I've extended it to support this functionality.

## What I Created

### 1. **EDHRecExtended Class** ([edhrec_extended.py](api/services/edhrec_extended.py))

A new class that extends `pyedhrec.EDHRec` with methods to scrape overall inclusion data from EDHRec card pages.

**Key Methods:**
- `get_overall_card_inclusion(card_name)` - Gets overall inclusion % across ALL decks
- `get_card_full_stats(card_name, commander_name)` - Gets both overall and commander-specific data
- `parse_deck_count(deck_str)` - Helper to convert "6.45M" to 6,450,000

### 2. **Updated edhrec.py** ([edhrec.py](api/services/edhrec.py))

Added convenience functions:
- `get_card_overall_inclusion(card_name)` - Get overall inclusion %
- `get_card_commander_inclusion(card_name, commander_name)` - Get commander-specific inclusion %

### 3. **Example File** ([get_inclusion_example.py](get_inclusion_example.py))

Demonstrates how to use the new functionality with 3 examples.

## Usage

```python
from api.services.edhrec import get_card_overall_inclusion, get_card_commander_inclusion

# Get overall inclusion (what you wanted!)
data = get_card_overall_inclusion("Sol Ring")
print(f"{data['card_name']}: {data['inclusion_percentage']}%")
# Output: Sol Ring: 83.8%

# Get commander-specific inclusion
cmd_data = get_card_commander_inclusion("Sol Ring", "Atraxa, Praetors' Voice")
print(f"Atraxa inclusion: {cmd_data['inclusion_percentage']}%")
# Output: Atraxa inclusion: 85.05%
```

## How It Works

The library **scrapes the EDHRec card page** to extract the inclusion data shown at the top:
- Uses `requests` to fetch the page
- Uses `BeautifulSoup` to parse HTML
- Extracts: `"83.8%inclusion6.45M decks7.70M decks"` pattern with regex

This reuses the `pyedhrec` library's URL generation and session management.

## Key Differences

| Metric | Commander-Specific | Overall |
|--------|-------------------|---------|
| **Source** | `get_commander_cards()` API | Web scraping |
| **Example** | Sol Ring in Atraxa: **85.05%** | Sol Ring overall: **83.8%** |
| **Scope** | One commander's decks | All Commander decks |
| **Also Returns** | Synergy score, category | Total deck counts |

## Dependencies

Added to project:
- `beautifulsoup4` - HTML parsing
- `requests` - Already included with pyedhrec

## Test Results

```
Sol Ring:
  Overall Inclusion: 83.8% (6.45M / 7.70M decks) ✓
  Atraxa-Specific: 85.05% (33,104 / 38,924 decks) ✓

Mana Crypt:
  Overall Inclusion: 2.4% (185K decks) ✓
```

## Notes

- The web scraping approach is necessary because the pyedhrec API doesn't expose overall inclusion data
- The EDHRec website structure is stable, but changes could break scraping
- All existing pyedhrec functionality is preserved - this only adds new features
- The extended class inherits all methods from the base `EDHRec` class
