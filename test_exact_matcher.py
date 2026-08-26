import json
from pathlib import Path

from word_matcher import WordMatcher


# --------------------------------------------------
# Configuration
# --------------------------------------------------

TRANSCRIPT_PATH = Path("word_transcribe.json")

QUERY = "My mind rebels at stagnation"


# --------------------------------------------------
# Load matcher
# --------------------------------------------------

matcher = WordMatcher(TRANSCRIPT_PATH)


# --------------------------------------------------
# Search
# --------------------------------------------------

result = matcher.find_first_occurrence(QUERY)


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("\n========== EXACT WORD MATCH ==========\n")

if result is None:

    print("No complete occurrence found.")

else:

    print(f"Query        : {result['query']}")
    print(f"Matched text : {result['matched_text']}")

    print(f"\nStart word   : {result['start_word']}")
    print(f"Start time   : {result['start']:.3f} seconds")

    print(f"\nEnd word     : {result['end_word']}")
    print(f"End time     : {result['end']:.3f} seconds")

    print(f"\nWord count   : {result['word_count']}")
    print(f"Word IDs     : {result['word_ids']}")

    print("\n======================================")