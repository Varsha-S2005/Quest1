import re


def normalize_word(word):
    """
    Normalize a single word so that small formatting
    differences do not prevent a match.

    Example:

        "REBELS,"  -> "rebels"
        "Stagnation." -> "stagnation"
        "MY" -> "my"
    """

    # Convert to lowercase.
    word = word.lower()

    # Remove punctuation and keep only letters/numbers.
    word = re.sub(r"[^\w]", "", word)

    return word


def normalize_query(query):
    """
    Convert the user's query into normalized tokens.

    Example:

        "MY MIND REBELS, AT STAGNATION!!"

    becomes:

        ["my", "mind", "rebels", "at", "stagnation"]
    """

    words = query.split()

    return [
        normalize_word(word)
        for word in words
        if normalize_word(word)
    ]


def find_first_phrase_occurrence(words, query):
    """
    Find the FIRST complete sequential occurrence of a query
    inside a list of timestamped Whisper words.

    Parameters
    ----------
    words:
        List of Whisper word objects.

        Example:

        [
            {
                "word": "My",
                "start": 344.10,
                "end": 344.30
            },
            ...
        ]

    query:
        User's search text.

    Returns
    -------
    Dictionary containing:

        start
        end
        matched_words

    or None if no complete occurrence is found.
    """

    # Normalize the query.
    query_words = normalize_query(query)

    if not query_words:
        return None

    # Normalize transcript words.
    transcript_words = [
        normalize_word(item["word"])
        for item in words
    ]

    query_length = len(query_words)

    # -----------------------------------------------------
    # Scan through the transcript from beginning to end.
    #
    # Because we scan chronologically, the first complete
    # match will automatically be the earliest occurrence.
    # -----------------------------------------------------

    for i in range(len(transcript_words) - query_length + 1):

        # Take the same number of words as the query.
        candidate = transcript_words[
            i:i + query_length
        ]

        # Check whether the complete sequence matches.
        if candidate == query_words:

            first_word = words[i]

            last_word = words[
                i + query_length - 1
            ]

            return {
                "start": first_word["start"],
                "end": last_word["end"],
                "matched_words": words[
                    i:i + query_length
                ]
            }

    # No complete sequence found.
    return None