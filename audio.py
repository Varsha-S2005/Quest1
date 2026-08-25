import subprocess
from pathlib import Path

# Find the downloaded MP4 file in the downloads folder
videos = list(Path("downloads").glob("*.mp4"))

if not videos:
    print("No video found in downloads/")
    exit()

video = videos[0]

# Create the MP3 output path using the same filename
audio = video.with_suffix(".mp3")

try:
    # Extract the audio from the local MP4 using FFmpeg
    subprocess.run(
        ["ffmpeg", "-i", str(video), "-vn", "-q:a", "0", str(audio)],
        check=True
    )

    print("\nAudio extraction successful!")
    print(f"Saved file: {audio}")

except subprocess.CalledProcessError as e:
    print(f"\nAudio extraction failed: {e}")