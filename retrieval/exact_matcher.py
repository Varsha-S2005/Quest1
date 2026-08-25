import json
import re


class ExactMatcher:
    """
    Finds an exact phrase inside a word-level Whisper transcript.

    Example:

        Query:
        "My mind rebels at stagnation"

        Transcript:
        My
        mind
        rebels
        at
        stagnation

    The matcher returns:

        Start timestamp = timestamp of "My"
        End timestamp   = timestamp of "stagnation"
    """

    def __init__(self, transcript_path):
        """
        Load the word-level transcript.

        transcript_path:
            Path to word_transcribe.json
        """

        self.transcript_path = transcript_path

        # Open the JSON file
        with open(self.transcript_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Our JSON stores the actual words inside the "words" key
        self.words = data["words"]

        print("Word-level transcript loaded successfully.")
        print(f"Total words: {len(self.words)}")

    def normalize_word(self, word):
        """
        Normalize a word before comparing it.

        Example:

            "My"       -> "my"
            "mind,"    -> "mind"
            "STAGNATION!" -> "stagnation"

        We do this because punctuation and capitalization
        should not prevent a valid match.
        """

        # Convert to lowercase
        word = word.lower()

        # Keep only letters and numbers
        word = re.sub(r"[^a-z0-9]", "", word)

        return word

    def find_first_occurrence(self, query):
        """
        Find the first complete sequential occurrence
        of the query.

        Example:

            Query:
            my mind rebels at stagnation

        We search for:

            my
            ↓
            mind
            ↓
            rebels
            ↓
            at
            ↓
            stagnation

        The words MUST occur consecutively and in order.
        """

        # Convert the query into individual words
        query_words = query.split()

        # Normalize every query word
        query_words = [
            self.normalize_word(word)
            for word in query_words
        ]

        # Remove empty values
        query_words = [
            word for word in query_words
            if word
        ]

        if not query_words:
            return None

        # Normalize the entire transcript once
        transcript_words = [
            self.normalize_word(word["word"])
            for word in self.words
        ]

        # Number of words in the query
        query_length = len(query_words)

        # Search through the transcript
        #
        # Example:
        #
        # query:
        # ["my", "mind", "rebels", "at", "stagnation"]
        #
        # We check:
        #
        # transcript[0:5]
        # transcript[1:6]
        # transcript[2:7]
        # ...
        for i in range(len(transcript_words) - query_length + 1):

            # Extract the same number of words as the query
            candidate = transcript_words[
                i:i + query_length
            ]

            # Check whether ALL words match
            if candidate == query_words:

                # First matched word
                first_word = self.words[i]

                # Last matched word
                last_word = self.words[
                    i + query_length - 1
                ]

                # Return the exact result
                return {
                    "start": first_word["start"],
                    "end": last_word["end"],
                    "text": " ".join(
                        word["word"]
                        for word in self.words[
                            i:i + query_length
                        ]
                    ),
                    "start_word": first_word["word"],
                    "end_word": last_word["word"],
                    "word_index_start": i,
                    "word_index_end": i + query_length - 1
                }

        # No complete occurrence found
        return None