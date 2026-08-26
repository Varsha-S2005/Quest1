from pathlib import Path
from PIL import Image


def seconds_to_timestamp(seconds):
    """Convert seconds to HH:MM:SS.sss."""

    seconds = float(seconds)

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def print_output(midpoint_seconds, frame_number, dialogue_text, image_path):
    """Print the final retrieval result and display the frame."""

    timestamp = seconds_to_timestamp(midpoint_seconds)

    print("=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)

    print(f"Timestamp : {timestamp}")
    print(f"Frame     : {frame_number}")
    print(f'Text      : "{dialogue_text}"')

    print("\nCorresponding Video Frame:")
    print(f"Image Path: {image_path}")

    print("=" * 60)

    # Display the corresponding JPG
    image_path = Path(image_path)

    if image_path.exists():
        image = Image.open(image_path)
        image.show()
    else:
        print(f"Error: Image not found: {image_path}")