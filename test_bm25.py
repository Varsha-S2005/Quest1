from retrieval.bm25_retriever import BM25Retriever


# =========================================================
# PATH TO OUR WHISPER TRANSCRIPT
# =========================================================
#
# transcribe.py created this file from the audio:
#
# downloads/transcript.json
#
# This JSON contains all of our timestamped Whisper
# transcript segments.
# =========================================================

TRANSCRIPT_PATH = "transcript.json"


# =========================================================
# CREATE THE BM25 RETRIEVER
# =========================================================
#
# When we create this object, BM25Retriever will:
#
# 1. Open transcript.json
# 2. Load all transcript segments
# 3. Preprocess the text
# 4. Create the BM25 index
#
# We will see how many segments were indexed in the
# terminal.
# =========================================================

retriever = BM25Retriever(TRANSCRIPT_PATH)


# =========================================================
# GET THE USER'S SEARCH QUERY
# =========================================================
#
# Example:
#
# Enter your search query: machine learning
#
# This query will also go through our preprocessing
# function before BM25 searches for it.
# =========================================================

query = input("\nEnter your search query: ")


# =========================================================
# SEARCH USING BM25
# =========================================================
#
# top_k=10 means:
#
# "Give me the 10 transcript segments that BM25 considers
# the most relevant to my query."
#
# IMPORTANT:
# At this stage we are NOT finding the earliest timestamp.
# We are only testing whether BM25 retrieves sensible
# transcript segments.
# =========================================================

results = retriever.search(query, top_k=10)


# =========================================================
# DISPLAY THE RESULTS
# =========================================================

print("\n========== BM25 RESULTS ==========\n")


# ---------------------------------------------------------
# Check whether BM25 returned anything.
# ---------------------------------------------------------

if not results:

    print("No results found.")


# ---------------------------------------------------------
# If results exist, display each one.
# ---------------------------------------------------------

else:

    for result in results:

        print(f"ID      : {result['id']}")
        print(f"Start   : {result['start']:.2f} seconds")
        print(f"End     : {result['end']:.2f} seconds")
        print(f"Score   : {result['score']:.4f}")
        print(f"Text    : {result['text']}")

        print("-" * 80)