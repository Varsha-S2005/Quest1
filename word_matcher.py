import json
import re
from pathlib import Path


class WordMatcher:

    def __init__(self, transcript_path):
        self.transcript_path = Path(transcript_path)

        with open(self.transcript_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.words = data["words"]

    @staticmethod
    def normalize(word):
        """
        Normalize a word so that small transcription/query
        formatting differences do not prevent matching.

        Examples:
            "My"       -> "my"
            "stagnation." -> "stagnation"
            "STAGNATION!" -> "stagnation"
        """

        word = word.lower().strip()

        # Remove punctuation from beginning/end
        word = re.sub(r"^[^\w]+|[^\w]+$", "", word)

        return word

    def find_first_occurrence(self, query):
        """
        Find the first complete sequential occurrence of the query.

        Example:

            Query:
            My mind rebels at stagnation

            Transcript:
            ...
            My
            mind
            rebels
            at
            stagnation
            ...

        Returns:
            {
                "query": ...,
                "matched_text": ...,
                "start": ...,
                "end": ...,
                "start_word": ...,
                "end_word": ...,
                "word_count": ...
            }

        Returns None if no complete occurrence is found.
        """

        query_words = [
            self.normalize(word)
            for word in query.split()
        ]

        query_words = [word for word in query_words if word]

        if not query_words:
            return None

        normalized_transcript = [
            self.normalize(item["word"])
            for item in self.words
        ]

        query_length = len(query_words)

        # Sliding window over the entire word-level transcript
        for i in range(len(normalized_transcript) - query_length + 1):

            window = normalized_transcript[
                i:i + query_length
            ]

            # Exact sequential comparison
            if window == query_words:

                matched_words = self.words[
                    i:i + query_length
                ]

                return {
                    "query": query,
                    "matched_text": " ".join(
                        word["word"] for word in matched_words
                    ),
                    "start": matched_words[0]["start"],
                    "end": matched_words[-1]["end"],
                    "start_word": matched_words[0]["word"],
                    "end_word": matched_words[-1]["word"],
                    "word_count": len(matched_words),
                    "word_ids": [
                        word["id"] for word in matched_words
                    ]
                }

        return None