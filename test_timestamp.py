from retrieval.bm25_retriever import BM25Retriever


# =========================================================
# PATH TO OUR TRANSCRIPT
# =========================================================

TRANSCRIPT_PATH = "transcript.json"


# =========================================================
# CREATE BM25 RETRIEVER
# =========================================================

retriever = BM25Retriever(TRANSCRIPT_PATH)


# =========================================================
# ASK THE USER FOR A SEARCH QUERY
# =========================================================

query = input("\nEnter the text you want to find: ")


# =========================================================
# FIND THE EARLIEST RELEVANT MATCH
# =========================================================

result = retriever.get_first_match(query)


# =========================================================
# DISPLAY THE RESULT
# =========================================================

print("\n========== FIRST OCCURRENCE ==========\n")


if result is None:

    print("No relevant match found.")

else:

    print(f"Transcript ID : {result['id']}")
    print(f"Start time    : {result['start']:.2f} seconds")
    print(f"End time      : {result['end']:.2f} seconds")
    print(f"BM25 score    : {result['score']:.4f}")
    print(f"Coverage      : {result['coverage'] * 100:.1f}%")
    print(f"Text          : {result['text']}")