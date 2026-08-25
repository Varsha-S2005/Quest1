import json
from pathlib import Path

from rank_bm25 import BM25Okapi

from retrieval.preprocess import preprocess_text


class BM25Retriever:
    """
    BM25-based search engine for our Whisper transcript.

    This class is responsible for:

    1. Loading the Whisper transcript JSON
    2. Preprocessing every transcript segment
    3. Creating the BM25 index
    4. Searching the transcript
    """

    def __init__(self, transcript_path: str):
        """
        Create a BM25 retriever.

        transcript_path:
            Location of our Whisper-generated JSON file.
        """

        # Convert the string path into a Path object.
        self.transcript_path = Path(transcript_path)

        # -----------------------------------------------------
        # Open the transcript JSON file.
        # -----------------------------------------------------

        with open(self.transcript_path, "r", encoding="utf-8") as f:

            # json.load() converts the JSON file into Python
            # objects.
            #
            # Our transcript is a list of dictionaries:
            #
            # [
            #     {
            #         "id": 0,
            #         "start": 0.0,
            #         "end": 5.0,
            #         "text": "Hello..."
            #     },
            #     ...
            # ]
            self.segments = json.load(f)

        # -----------------------------------------------------
        # Preprocess every transcript segment.
        # -----------------------------------------------------
        #
        # We only send the "text" field to our preprocessing
        # function.
        #
        # Example:
        #
        # "Machine Learning is AMAZING!"
        #
        # becomes:
        #
        # ["machine", "learning", "is", "amazing"]
        # -----------------------------------------------------

        self.tokenized_segments = [
            preprocess_text(segment["text"])
            for segment in self.segments
        ]

        # -----------------------------------------------------
        # Create the BM25 index.
        # -----------------------------------------------------
        #
        # Every transcript segment is treated as a document.
        #
        # BM25 will later compare the user's query against
        # these documents and calculate a relevance score.
        # -----------------------------------------------------

        self.bm25 = BM25Okapi(self.tokenized_segments)

        print("BM25 index created successfully.")
        print(f"Indexed segments: {len(self.segments)}")

    def search(self, query: str, top_k: int = 10):
        """
        Search the transcript using BM25.

        query:
            The text entered by the user.

        top_k:
            Number of results we want back.

            For example:
            top_k=10 → return the 10 highest-scoring segments.
        """

        # -----------------------------------------------------
        # Preprocess the user's query using the SAME function
        # we used for the transcript.
        # -----------------------------------------------------

        query_tokens = preprocess_text(query)

        # If the query becomes empty after preprocessing,
        # there is nothing to search.
        if not query_tokens:
            return []

        # -----------------------------------------------------
        # Calculate BM25 scores.
        # -----------------------------------------------------
        #
        # BM25 calculates one score for every transcript
        # segment.
        #
        # Example:
        #
        # Segment 0 → 0.0
        # Segment 1 → 4.2
        # Segment 2 → 10.8
        # ...
        # -----------------------------------------------------

        scores = self.bm25.get_scores(query_tokens)

        # -----------------------------------------------------
        # Get the indices of the segments and sort them by
        # their BM25 score.
        #
        # reverse=True means highest score comes first.
        # -----------------------------------------------------

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        # This list will contain our final search results.
        results = []

        # -----------------------------------------------------
        # Take only the top_k highest-scoring segments.
        # -----------------------------------------------------

        for index in ranked_indices[:top_k]:

            segment = self.segments[index]

            # Store the useful information from the transcript
            # together with the BM25 score.
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

    def get_first_match(self, query: str, top_k: int = 20):
        """
        Find the earliest transcript segment that is relevant
        to the user's query.

        BM25 ranks results by RELEVANCE.

        We then use the timestamps stored in the transcript
        to determine which relevant result happened FIRST.
        """

        # -----------------------------------------------------
        # Step 1:
        # Search BM25 and get the top candidates.
        #
        # We use more than one result because the highest
        # BM25 score is not necessarily the earliest occurrence.
        # -----------------------------------------------------

        results = self.search(query, top_k=top_k)

        if not results:
            return None

        # -----------------------------------------------------
        # Step 2:
        # Preprocess the user's query.
        #
        # Example:
        #
        # "MY MIND REBELS, AT STAGNATION!!"
        #
        # becomes:
        #
        # ["my", "mind", "rebels", "at", "stagnation"]
        # -----------------------------------------------------

        query_tokens = set(preprocess_text(query))

        if not query_tokens:
            return None

        relevant_results = []

        # -----------------------------------------------------
        # Step 3:
        # Check how many query words occur in each result.
        # -----------------------------------------------------

        for result in results:

            # Preprocess the transcript text.
            document_tokens = set(
                preprocess_text(result["text"])
            )

            # Find which query words are present.
            matched_tokens = query_tokens.intersection(
                document_tokens
            )

            # Calculate how much of the query matched.
            coverage = len(matched_tokens) / len(query_tokens)

            # Save the coverage value.
            result["coverage"] = coverage

            # -------------------------------------------------
            # Keep the result if at least 50% of the unique
            # query words occur in the transcript segment.
            #
            # Example:
            #
            # Query has 4 words.
            # 4/4 → 100% → keep
            # 3/4 → 75%  → keep
            # 2/4 → 50%  → keep
            # 1/4 → 25%  → reject
            # -------------------------------------------------

            if coverage >= 0.5:
                relevant_results.append(result)

        # -----------------------------------------------------
        # If nothing passed our relevance check, return None.
        # -----------------------------------------------------

        if not relevant_results:
            return None

        # -----------------------------------------------------
        # Step 4:
        # Sort the relevant results by their START timestamp.
        #
        # This is the important part:
        #
        # BM25 → relevance
        # start → chronological order
        # -----------------------------------------------------

        relevant_results.sort(
            key=lambda result: result["start"]
        )

        # -----------------------------------------------------
        # Step 5:
        # The first result is now the earliest relevant
        # transcript segment.
        # -----------------------------------------------------

        return relevant_results[0]