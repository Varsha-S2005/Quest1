import json
import time
from pathlib import Path

import torch
from transformers import pipeline


# =========================================================
# MODEL CONFIGURATION
# =========================================================

MODEL_NAME = "openai/whisper-large-v3-turbo"


# =========================================================
# FIND THE AUDIO FILE
# =========================================================
#
# Look inside the downloads folder for MP3 files.
#

audios = list(Path("downloads").glob("*.mp3"))

if not audios:
    print("No audio file found in downloads/. Run audio.py first.")
    exit()

# Use the first MP3 file found.
audio_path = audios[0]

print(f"Using audio file: {audio_path}")


# =========================================================
# SELECT GPU OR CPU
# =========================================================
#
# If CUDA/GPU is available, use GPU.
# Otherwise, run on CPU.
#

device = 0 if torch.cuda.is_available() else -1

print(
    f"Using {'GPU' if device == 0 else 'CPU'} for inference"
)


# =========================================================
# LOAD WHISPER MODEL
# =========================================================

asr = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    device=device,
)


# =========================================================
# START TRANSCRIPTION
# =========================================================

start_time = time.time()


# =========================================================
# TRANSCRIBE WITH WORD-LEVEL TIMESTAMPS
# =========================================================
#
# return_timestamps="word" tells Whisper to return
# timestamps for individual words.
#
# Example conceptual output:
#
# {
#     "text": " My",
#     "timestamp": (344.10, 344.30)
# }
#

result = asr(
    str(audio_path),
    return_timestamps="word",
    chunk_length_s=30,
    stride_length_s=5,
)


# Calculate total transcription time.
elapsed = time.time() - start_time


# =========================================================
# INSPECT WHISPER OUTPUT
# =========================================================
#
# Print the first 10 entries so we can verify the exact
# structure returned by your Whisper/Transformers version.
#

print("\nFirst 10 Whisper word entries:\n")

for chunk in result["chunks"][:10]:
    print(chunk)


# =========================================================
# CREATE WORD-LEVEL TRANSCRIPT
# =========================================================
#
# Each entry in transcript.json will contain:
#
# id    -> unique word ID
# start -> word start timestamp
# end   -> word end timestamp
# text  -> the actual word
#

words = []

for i, chunk in enumerate(result["chunks"]):

    # Get the timestamp tuple/list.
    timestamp = chunk.get("timestamp")

    # Skip entries without valid timestamps.
    if (
        timestamp is None
        or timestamp[0] is None
        or timestamp[1] is None
    ):
        continue

    # Save the word and its timestamps.
    words.append(
        {
            "id": i,
            "start": timestamp[0],
            "end": timestamp[1],
            "text": chunk["text"].strip(),
        }
    )


# =========================================================
# SAVE WORD-LEVEL TRANSCRIPT
# =========================================================
#
# We are saving it directly as:
#
# transcript.json
#
# inside the Quest1 folder.
#

transcript_path = Path("transcript.json")

with open(transcript_path, "w", encoding="utf-8") as f:
    json.dump(
        words,
        f,
        indent=2,
        ensure_ascii=False,
    )


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\nTranscription successful!")

print(f"Saved transcript: {transcript_path}")

print(f"Words found: {len(words)}")

print(f"Transcription time: {elapsed:.2f} seconds")