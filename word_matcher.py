
import json
import re


class WordMatcher:
    """
    Finds an exact sequential occurrence of a query
    inside a word-level Whisper transcript.

    Example:

        Query:
        "My mind rebels at stagnation"

        Transcript words:
        ... my -> mind -> rebels -> at -> stagnation ...

    The matcher makes sure the words occur in this
    exact order.
    """

    def __init__(self, transcript_path):
        """
        Load the word-level transcript JSON.

        The JSON is expected to have this structure:

        {
            "words": [
                {
                    "id": 0,
                    "word": "I",
                    "start": 0.0,
                    "end": 1.74
                },
                ...
            ]
        }
        """

        self.transcript_path = transcript_path

        # Open the JSON file.
        with open(transcript_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract the actual word list.
        self.words = data["words"]

        print(f"Loaded {len(self.words)} word timestamps.")

    def normalize(self, text):
        """
        Normalize a word before comparing it.

        Example:

            "MY"       -> "my"
            "stagnation!" -> "stagnation"
            "rebels,"  -> "rebels"

        This allows punctuation and capitalization
        differences without changing the actual words.
        """

        text = text.lower()

        # Keep only letters and numbers.
        text = re.sub(r"[^a-z0-9']", "", text)

        return text

    def find_first_occurrence(self, query):
        """
        Find the FIRST complete sequential occurrence
        of the query.

        Example:

            Query:
            "My mind rebels at stagnation"

        We are NOT simply searching for the first "my".

        Instead we check:

            my
            ↓
            mind
            ↓
            rebels
            ↓
            at
            ↓
            stagnation

        consecutively in the transcript.

        Returns:
            Dictionary containing:
                query
                start_time
                end_time
                matched_words

        Returns None if the complete phrase isn't found.
        """

        # Normalize the query.
        query_words = [
            self.normalize(word)
            for word in query.split()
        ]

        # Remove empty values.
        query_words = [
            word for word in query_words
            if word
        ]

        if not query_words:
            return None

        # Normalize every transcript word.
        transcript_words = [
            self.normalize(item["word"])
            for item in self.words
        ]

        # Number of words in the query.
        query_length = len(query_words)

        # Slide through the transcript one word at a time.
        #
        # Example:
        #
        # transcript:
        # ... my mind rebels at stagnation ...
        #
        # query:
        # my mind rebels at stagnation
        #
        # When the window starts at "my",
        # we compare the complete sequence.
        for start_index in range(
            len(transcript_words) - query_length + 1
        ):

            # Extract a window of the same size as the query.
            window = transcript_words[
                start_index:start_index + query_length
            ]

            # Check whether the COMPLETE sequence matches.
            if window == query_words:

                # The first matched word.
                first_word = self.words[start_index]

                # The final matched word.
                last_word = self.words[
                    start_index + query_length - 1
                ]

                return {
                    "query": query,

                    # Timestamp where the FIRST query word starts.
                    "start_time": first_word["start"],

                    # Timestamp where the LAST query word ends.
                    "end_time": last_word["end"],

                    # Useful for debugging and explanation.
                    "matched_words": self.words[
                        start_index:start_index + query_length
                    ]
                }

        # Complete sequence was not found.
        return None
