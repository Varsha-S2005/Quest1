import re


def preprocess_text(text: str) -> list[str]:
    """
    Clean and tokenize text before sending it to BM25.

    The same function will be used for:
    1. Transcript segments
    2. User search queries

    This is important because the transcript and query
    need to be processed in the same way.
    """

    # ---------------------------------------------------------
    # 1. Check whether the input is empty
    # ---------------------------------------------------------
    # If text is None or an empty string, there is nothing
    # to preprocess.
    #
    # Example:
    # "" -> []
    # ---------------------------------------------------------

    if not text:
        return []

    # ---------------------------------------------------------
    # 2. Convert text to lowercase
    # ---------------------------------------------------------
    # This makes our search case-insensitive.
    #
    # Example:
    # "Machine Learning"
    # becomes:
    # "machine learning"
    # ---------------------------------------------------------

    text = text.lower()

    # ---------------------------------------------------------
    # 3. Remove punctuation and special characters
    # ---------------------------------------------------------
    #
    # We want to keep:
    # - lowercase letters: a-z
    # - numbers: 0-9
    # - whitespace
    #
    # Everything else is replaced with a space.
    #
    # Example:
    # "Hello, world!"
    # becomes:
    # "hello  world "
    # ---------------------------------------------------------

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # ---------------------------------------------------------
    # 4. Remove unnecessary multiple spaces
    # ---------------------------------------------------------
    #
    # Example:
    # "hello     world"
    #
    # becomes:
    # "hello world"
    # ---------------------------------------------------------

    text = re.sub(r"\s+", " ", text).strip()

    # ---------------------------------------------------------
    # 5. Tokenize the text
    # ---------------------------------------------------------
    #
    # Tokenization means splitting a sentence into individual
    # words.
    #
    # Example:
    #
    # "machine learning is useful"
    #
    # becomes:
    #
    # ["machine", "learning", "is", "useful"]
    # ---------------------------------------------------------

    tokens = text.split()

    return tokens