import cv2
from pathlib import Path


VIDEO_PATH = Path("downloads/sherlock.mp4")

START_TIME = 321.700
END_TIME = 327.780

DIALOGUE_TEXT = "My mind rebels at stagnation"

OUTPUT_PATH = Path("final_dialogue_frame.jpg")


def extract_midpoint_frame():

    # Calculate midpoint
    midpoint = (START_TIME + END_TIME) / 2

    cap = cv2.VideoCapture(str(VIDEO_PATH))

    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open video: {VIDEO_PATH}"
        )

    # Get video FPS
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        cap.release()
        raise RuntimeError("Could not determine video FPS.")

    # Calculate exact frame number
    frame_number = round(midpoint * fps)

    # Seek directly to that frame
    cap.set(
        cv2.CAP_PROP_POS_FRAMES,
        frame_number
    )

    success, frame = cap.read()

    cap.release()

    if not success:
        raise RuntimeError(
            "Could not extract midpoint frame."
        )

    # Save frame
    cv2.imwrite(
        str(OUTPUT_PATH),
        frame
    )

    actual_timestamp = frame_number / fps

    print("\n========================================")
    print("FINAL DIALOGUE FRAME")
    print("========================================")

    print(f"Text      : \"{DIALOGUE_TEXT}\"")
    print(f"Start     : {START_TIME:.3f}s")
    print(f"End       : {END_TIME:.3f}s")
    print(f"Midpoint  : {midpoint:.3f}s")
    print(f"Timestamp : {actual_timestamp:.3f}s")
    print(f"Frame     : {frame_number}")
    print(f"Image     : {OUTPUT_PATH}")

    print("========================================")

    return {
        "text": DIALOGUE_TEXT,
        "start_timestamp": START_TIME,
        "end_timestamp": END_TIME,
        "midpoint": midpoint,
        "timestamp": actual_timestamp,
        "frame_number": frame_number,
        "image": str(OUTPUT_PATH)
    }


if __name__ == "__main__":
    extract_midpoint_frame()