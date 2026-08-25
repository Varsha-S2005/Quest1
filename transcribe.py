import json
import time
from pathlib import Path
from transformers import pipeline
import torch

MODEL_NAME = "openai/whisper-large-v3-turbo"

audios = list(Path("downloads").glob("*.mp3"))
if not audios:
    print("No audio file found in downloads/. Run audio.py first.")
    exit()
audio_path = audios[0]
print(f"Using audio file: {audio_path}")

device = 0 if torch.cuda.is_available() else -1
print(f"Using {'GPU' if device == 0 else 'CPU'} for inference")

asr = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    device=device,
)

start_time = time.time()
result = asr(
    str(audio_path),
    return_timestamps=True,
    chunk_length_s=30,
    stride_length_s=5,
)
elapsed = time.time() - start_time

segments = [
    {"id": i, "start": c["timestamp"][0], "end": c["timestamp"][1], "text": c["text"].strip()}
    for i, c in enumerate(result["chunks"])
    if c["timestamp"][0] is not None and c["timestamp"][1] is not None
]

transcript_path = audio_path.with_suffix(".json")
with open(transcript_path, "w", encoding="utf-8") as f:
    json.dump(segments, f, indent=2, ensure_ascii=False)

print(f"\nTranscription successful!")
print(f"Saved transcript: {transcript_path}")
print(f"Segments found: {len(segments)}")