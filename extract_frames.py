import cv2
import json
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

VIDEO_PATH = Path("downloads/sherlock.mp4")

START_TIME = 321.700
END_TIME = 327.780

QUERY_TEXT = "My mind rebels at stagnation"

SAMPLE_FPS = 5

OUTPUT_DIR = Path("extracted_frames")
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# FRAME EXTRACTION
# ============================================================

def extract_frames(video_path, start_time, end_time, sample_fps, output_dir):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if video_fps <= 0:
        cap.release()
        raise RuntimeError("Could not determine video FPS.")

    duration = total_frames / video_fps

    print("\n========== VIDEO INFO ==========")
    print(f"Video FPS    : {video_fps}")
    print(f"Total frames : {total_frames}")
    print(f"Duration     : {duration:.3f}s")
    print(f"Start time   : {start_time:.3f}s")
    print(f"End time     : {end_time:.3f}s")
    print(f"Sample FPS   : {sample_fps}")

    # --------------------------------------------------------
    # Convert timestamps to frame positions
    # --------------------------------------------------------

    start_frame = max(0, int(start_time * video_fps))
    end_frame = min(
        total_frames - 1,
        int(end_time * video_fps)
    )

    # --------------------------------------------------------
    # Seek directly to the beginning.
    # We DO NOT process the entire video.
    # --------------------------------------------------------

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    sample_interval = 1.0 / sample_fps

    frames = []

    next_sample_time = start_time

    while True:

        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        if current_frame > end_frame:
            break

        ret, frame = cap.read()

        if not ret:
            break

        timestamp = current_frame / video_fps

        # Only save frames at requested sampling interval
        if timestamp >= next_sample_time:

            filename = f"frame_{len(frames):05d}.jpg"
            frame_path = output_dir / filename

            success = cv2.imwrite(
                str(frame_path),
                frame
            )

            if not success:
                print(f"WARNING: Could not save {frame_path}")
            else:

                frame_info = {
                    "frame_index": current_frame,
                    "timestamp": round(timestamp, 3),
                    "image": str(frame_path),
                }

                frames.append(frame_info)

                print(
                    f"Saved frame {len(frames)-1:05d} | "
                    f"video frame = {current_frame} | "
                    f"timestamp = {timestamp:.3f}s"
                )

                next_sample_time += sample_interval

    cap.release()

    return frames, video_fps


# ============================================================
# MAIN
# ============================================================

def main():

    frames, video_fps = extract_frames(
        VIDEO_PATH,
        START_TIME,
        END_TIME,
        SAMPLE_FPS,
        OUTPUT_DIR
    )

    if not frames:
        print("\nERROR: No frames were extracted.")
        return

    # --------------------------------------------------------
    # Pick the first extracted frame as the initial candidate.
    #
    # Later, the image-analysis stage will determine which
    # frame actually contains the dialogue.
    # --------------------------------------------------------

    first_frame = frames[0]

    last_frame = frames[-1]

    result = {
        "query": QUERY_TEXT,

        "timestamp_range": {
            "start": START_TIME,
            "end": END_TIME
        },

        "video": str(VIDEO_PATH),

        "video_fps": video_fps,

        "frames_extracted": len(frames),

        "frames": frames,

        # Initial extraction result
        "first_extracted_frame": {
            "frame_number": first_frame["frame_index"],
            "timestamp": first_frame["timestamp"],
            "image": first_frame["image"]
        },

        "last_extracted_frame": {
            "frame_number": last_frame["frame_index"],
            "timestamp": last_frame["timestamp"],
            "image": last_frame["image"]
        }
    }

    # --------------------------------------------------------
    # Save machine-readable result
    # --------------------------------------------------------

    result_path = Path("frame_extraction_result.json")

    with open(
        result_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=2,
            ensure_ascii=False
        )

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    print("\n")
    print("========================================")
    print("FRAME EXTRACTION COMPLETE")
    print("========================================")

    print(f"Dialogue       : {QUERY_TEXT}")
    print(f"Start time     : {START_TIME:.3f}s")
    print(f"End time       : {END_TIME:.3f}s")

    print(f"Frames saved   : {len(frames)}")

    print("\nFirst extracted frame:")
    print(f"Frame number   : {first_frame['frame_index']}")
    print(f"Timestamp      : {first_frame['timestamp']:.3f}s")
    print(f"Image          : {first_frame['image']}")

    print("\nLast extracted frame:")
    print(f"Frame number   : {last_frame['frame_index']}")
    print(f"Timestamp      : {last_frame['timestamp']:.3f}s")
    print(f"Image          : {last_frame['image']}")

    print("\nResult JSON:")
    print(result_path)

    print("\n========================================")


if __name__ == "__main__":
    main()