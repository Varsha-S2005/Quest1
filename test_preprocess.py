from retrieval.preprocess import preprocess_text


# ---------------------------------------------------------
# Create a sample sentence.
#
# We deliberately include:
# - uppercase letters
# - punctuation
# - multiple spaces
# ---------------------------------------------------------

text = "Hello, TODAY we're learning Machine Learning!"


# ---------------------------------------------------------
# Send the sentence to our preprocessing function.
# ---------------------------------------------------------

result = preprocess_text(text)


# ---------------------------------------------------------
# Print the original sentence.
# ---------------------------------------------------------

print("Original text:")
print(text)


# ---------------------------------------------------------
# Print the processed result.
# ---------------------------------------------------------

print("\nProcessed text:")
print(result)