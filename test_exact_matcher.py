from retrieval.exact_matcher import ExactMatcher


# ---------------------------------------------------------
# Path to our word-level Whisper transcription
# ---------------------------------------------------------

TRANSCRIPT_PATH = "word_transcribe.json"


# ---------------------------------------------------------
# Create the matcher
# ---------------------------------------------------------

matcher = ExactMatcher(TRANSCRIPT_PATH)


# ---------------------------------------------------------
# Ask the user for a query
# ---------------------------------------------------------

query = input("\nEnter the dialogue to find: ")


# ---------------------------------------------------------
# Search for the first complete occurrence
# ---------------------------------------------------------

result = matcher.find_first_occurrence(query)


# ---------------------------------------------------------
# Display the result
# ---------------------------------------------------------

if result is None:

    print("\nNo exact sequential occurrence found.")

else:

    print("\n========== EXACT OCCURRENCE ==========")

    print(f"Text          : {result['text']}")

    print(
        f"Start time    : "
        f"{result['start']:.3f} seconds"
    )

    print(
        f"End time      : "
        f"{result['end']:.3f} seconds"
    )

    print(
        f"First word    : "
        f"{result['start_word']}"
    )

    print(
        f"Last word     : "
        f"{result['end_word']}"
    )

    print(
        f"Word indexes  : "
        f"{result['word_index_start']} "
        f"→ "
        f"{result['word_index_end']}"
    )