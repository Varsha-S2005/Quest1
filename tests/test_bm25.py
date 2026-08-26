from retrieval.bm25_retriever import BM25Retriever


TRANSCRIPT_PATH = "transcript.json"


retriever = BM25Retriever(TRANSCRIPT_PATH)

query = input("\nEnter your search query: ").strip()

if not query:
    print("Query cannot be empty.")
    exit()


# =========================================================
# BM25 SEARCH
# =========================================================

results = retriever.search(
    query,
    top_k=10
)


print("\n========== BM25 RESULTS ==========\n")


if not results:

    print("No results found.")

else:

    for result in results:

        print(f"ID       : {result['id']}")
        print(f"Start    : {result['start']:.2f} seconds")
        print(f"End      : {result['end']:.2f} seconds")
        print(f"Score    : {result['score']:.4f}")
        print(f"Text     : {result['text']}")

        print("-" * 80)