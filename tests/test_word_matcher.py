from retrieval.word_matcher import WordMatcher


# =========================================================
# PATH TO WORD-LEVEL TRANSCRIPT
# =========================================================

WORD_TRANSCRIPT_PATH = "word_transcribe.json"


# =========================================================
# CREATE WORD MATCHER
# =========================================================

matcher = WordMatcher(WORD_TRANSCRIPT_PATH)


# =========================================================
# GET USER QUERY
# =========================================================

query = input("\nEnter your search query: ").strip()


# =========================================================
# FIND EXACT WORD SEQUENCE
# =========================================================

result = matcher.find_first_occurrence(query)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("\n========== WORD MATCH RESULT ==========\n")

if result is None:

    print("Exact dialogue not found.")

else:

    print(f"Query       : {result['query']}")
    print(f"Matched text: {result['matched_text']}")
    print(f"Start       : {result['start']:.3f} seconds")
    print(f"End         : {result['end']:.3f} seconds")
    print(f"Start word  : {result['start_word']}")
    print(f"End word    : {result['end_word']}")
    print(f"Word count  : {result['word_count']}")
    print(f"Word IDs    : {result['word_ids']}")