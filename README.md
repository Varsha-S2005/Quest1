# Video Dialogue Retrieval System

A modular video-processing pipeline that takes a video URL and a natural-language dialogue query as input and returns a representative video frame corresponding to the requested dialogue.

## System Overview

The system follows a sequential pipeline:

Video URL
→ Video & Audio Extraction
→ Whisper Transcription
→ BM25 Retrieval
→ Word-Level Matching
→ Frame Extraction
→ Final Dialogue Frame

## Architecture

### 1. Video and Audio Extraction

The user provides a video URL.

The video is downloaded locally using `yt-dlp`. The audio is then extracted from the downloaded video using FFmpeg.

The extracted files are used as inputs for the transcription stage.

### 2. Speech Transcription

The extracted audio is uploaded to Google Colab, where GPU acceleration is used for efficient transcription.

We evaluated different transcription approaches and created separate experimental branches to compare their performance. Based on these experiments, **Whisper Large-v3-Turbo** was selected for the final pipeline.

The model is obtained from **Hugging Face** and accessed through the `transformers` library.

Two types of transcription are generated:

- `transcript.json` — segment-level transcript containing dialogue text and timestamps.
- `word_transcribe.json` — word-level transcript containing individual words and their timestamps.

The segment-level transcript is used for initial dialogue-range retrieval, while the word-level transcript is used only after the relevant range has been identified.

### 3. BM25 Retrieval

The segment-level transcript is indexed using **BM25** through the `rank-bm25` library.

The user's dialogue query is preprocessed using the same preprocessing function as the transcript.

BM25 ranks transcript segments according to their textual relevance to the query.

For example:

    Query:
    My mind rebels at stagnation

    BM25 result:
    Start: 324.94 seconds
    End:   327.78 seconds

This provides the approximate dialogue range in the video.

### 4. Word-Level Matching

After BM25 identifies the relevant dialogue range, the word-level transcript is used for more precise timestamp identification.

`WordMatcher` searches for the exact sequential occurrence of the requested dialogue.

For example:

    My
    mind
    rebels
    at
    stagnation

The matcher returns the timestamp of the first word and the timestamp of the last word.

This gives us a more precise dialogue boundary than the segment-level BM25 result.

### 5. Frame Extraction

Once the exact dialogue start and end timestamps are available, the midpoint of the dialogue interval is calculated:

    midpoint = (start + end) / 2

OpenCV is then used to extract the video frame corresponding to this timestamp.

The resulting frame is saved as:

    final_dialogue_frame.jpg

## Project Structure

    Quest1/
    │
    ├── retrieval/
    │   ├── __init__.py
    │   ├── bm25_retriever.py
    │   ├── frame_extractor.py
    │   ├── preprocess.py
    │   └── word_matcher.py
    │
    ├── tests/
    │   ├── __init__.py
    │   ├── test_bm25.py
    │   ├── test_frame_extractor.py
    │   └── test_word_matcher.py
    │
    ├── downloads/
    │   ├── audio.mp3
    │   └── video.mp4
    │
    ├── audio.py
    ├── main.py
    ├── transcribe.py
    ├── word_transcribe.py
    ├── requirements.txt
    └── README.md

## Technologies Used

- Python
- yt-dlp
- FFmpeg
- OpenCV
- Hugging Face Transformers
- Whisper Large-v3-Turbo
- BM25
- rank-bm25
- Google Colab
- CUDA GPU acceleration

## Execution Workflow

### Step 1 — Download Video and Extract Audio

Run:

    python main.py

Enter the video URL when prompted.

The video and audio are saved locally in the `downloads/` directory.

### Step 2 — Transcription

Upload the extracted audio to Google Colab.

Run the Whisper transcription workflow using the Hugging Face `openai/whisper-large-v3-turbo` model.

Generate:

    transcript.json

Download the generated transcript and place it in the project root.

### Step 3 — BM25 Retrieval

Run:

    python -m tests.test_bm25

Enter the dialogue query.

BM25 returns the most relevant transcript segments and their timestamps.

### Step 4 — Word-Level Matching

Generate the word-level transcript for the required audio/dialogue range in Google Colab.

Download:

    word_transcribe.json

Place it in the project root.

Run:

    python -m tests.test_word_matcher

The exact dialogue occurrence and word-level timestamps are returned.

### Step 5 — Frame Extraction

Use the identified start and end timestamps with the frame extractor.

Run:

    python -m tests.test_frame_extractor

The representative frame is saved as:

    final_dialogue_frame.jpg

## Why Two Transcription Levels?

The system deliberately separates transcript retrieval from precise timestamp matching.

### Segment-level transcript

Used for:

- BM25 indexing
- Fast retrieval
- Finding the approximate dialogue location

### Word-level transcript

Used for:

- Exact sequential dialogue matching
- Precise start timestamp
- Precise end timestamp

This avoids generating and processing a large word-level transcript when it is not required for the initial retrieval stage.

## Output

Given a query such as:

    My mind rebels at stagnation

the system identifies the relevant dialogue and ultimately produces:

    final_dialogue_frame.jpg

representing a frame from the corresponding portion of the video.

## Notes

Large generated files such as downloaded videos, audio files, transcripts, and extracted frames are excluded from Git using `.gitignore`.

The transcription stage is performed using Google Colab GPU acceleration because Whisper Large-v3-Turbo is computationally expensive for local CPU execution.