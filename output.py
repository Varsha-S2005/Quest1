import json
from pathlib import Path
import cv2
from PIL import Image


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

WORD_TRANSCRIPT = Path("outputs/word_transcribe.json")
FRAME_PATH = Path("outputs/final_dialogue_frame.jpg")
VIDEO_PATH = Path("downloads/video.mp4")


# ---------------------------------------------------------
# Convert seconds to HH:MM:SS.sss
# ---------------------------------------------------------

def seconds_to_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"


# ---------------------------------------------------------
# Get video FPS
# ---------------------------------------------------------

def get_video_fps(video_path):

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)

    cap.release()

    if fps <= 0:
        raise RuntimeError("Could not determine video FPS.")

    return fps


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    # Load word-level transcript
    if not WORD_TRANSCRIPT.exists():
        print(f"Error: File not found: {WORD_TRANSCRIPT}")
        return

    with open(WORD_TRANSCRIPT, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Get dialogue start/end
    start_time = float(data["source_start"])
    end_time = float(data["source_end"])

    # Calculate midpoint
    midpoint = (start_time + end_time) / 2

    # Extract dialogue
    words = data.get("words", [])

    dialogue_text = " ".join(
        word["word"].strip()
        for word in words
    )

    # -----------------------------------------------------
    # Get actual FPS
    # -----------------------------------------------------

    fps = get_video_fps(VIDEO_PATH)

    # Calculate frame number corresponding to midpoint
    frame_number = round(midpoint * fps)

    # -----------------------------------------------------
    # Final output
    # -----------------------------------------------------

    print("=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)

    print(f"Timestamp : {seconds_to_timestamp(midpoint)}")
    print(f"Frame     : {frame_number}")
    print(f'Text      : "{dialogue_text}"')

    print("\nCorresponding Video Frame:")
    print(f"Image Path: {FRAME_PATH}")

    print("=" * 60)

    # -----------------------------------------------------
    # Display image
    # -----------------------------------------------------

    if FRAME_PATH.exists():
        image = Image.open(FRAME_PATH)
        image.show()
    else:
        print(f"Error: Image not found: {FRAME_PATH}")


if __name__ == "__main__":
    main()