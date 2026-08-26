import json
from pathlib import Path

from rank_bm25 import BM25Okapi

from retrieval.preprocess import preprocess_text


class BM25Retriever:
    """
    BM25-based retriever for the timestamped Whisper transcript.

    Responsibilities:
    1. Load transcript.json
    2. Extract timestamped transcript segments
    3. Preprocess each segment
    4. Build the BM25 index
    5. Retrieve the most relevant segments
    6. Find the earliest relevant segment
    """

    def __init__(self, transcript_path: str):

        self.transcript_path = Path(transcript_path)

        # -----------------------------------------------------
        # Load transcript
        # -----------------------------------------------------

        with open(self.transcript_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # transcript.json stores segments inside "segments"
        self.segments = data["segments"]

        if not self.segments:
            raise ValueError("Transcript contains no segments.")

        # -----------------------------------------------------
        # Preprocess transcript segments
        # -----------------------------------------------------

        self.tokenized_segments = [
            preprocess_text(segment["text"])
            for segment in self.segments
        ]

        # -----------------------------------------------------
        # Create BM25 index
        # -----------------------------------------------------

        self.bm25 = BM25Okapi(self.tokenized_segments)

        print("BM25 index created successfully.")
        print(f"Indexed segments: {len(self.segments)}")

    # =========================================================
    # SEARCH
    # =========================================================

    def search(self, query: str, top_k: int = 10):
        """
        Search the timestamped transcript using BM25.

        Returns the top_k most relevant transcript segments.
        """

        query_tokens = preprocess_text(query)

        if not query_tokens:
            return []

        # Calculate BM25 score for every segment
        scores = self.bm25.get_scores(query_tokens)

        # Rank segments by relevance
        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        results = []

        for index in ranked_indices[:top_k]:

            segment = self.segments[index]

            results.append(
                {
                    "id": segment["id"],
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"],
                    "score": float(scores[index])
                }
            )

        return results

    # =========================================================
    # EARLIEST RELEVANT MATCH
    # =========================================================

    def get_first_match(self, query: str, top_k: int = 20):
        """
        Retrieve BM25 candidates and return the earliest
        sufficiently relevant transcript segment.

        BM25 determines relevance.

        The timestamp determines chronological order.
        """

        results = self.search(query, top_k=top_k)

        if not results:
            return None

        query_tokens = set(preprocess_text(query))

        if not query_tokens:
            return None

        relevant_results = []

        for result in results:

            document_tokens = set(
                preprocess_text(result["text"])
            )

            matched_tokens = query_tokens.intersection(
                document_tokens
            )

            coverage = (
                len(matched_tokens) / len(query_tokens)
            )

            result["coverage"] = coverage

            # Require at least 50% query-word coverage
            if coverage >= 0.5:
                relevant_results.append(result)

        if not relevant_results:
            return None

        # Earliest relevant occurrence
        relevant_results.sort(
            key=lambda result: result["start"]
        )

        return relevant_results[0]