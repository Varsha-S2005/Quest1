import cv2
from pathlib import Path


class FrameExtractor:
    """
    Extracts a representative frame from a video using
    the midpoint of a dialogue timestamp range.
    """

    def __init__(
        self,
        video_path: str,
        output_path: str = "final_dialogue_frame.jpg",
    ):
        self.video_path = Path(video_path)
        self.output_path = Path(output_path)

    def extract_midpoint_frame(
        self,
        start_time: float,
        end_time: float,
    ):
        """
        Extract the frame at the midpoint between start_time
        and end_time.
        """

        if start_time < 0:
            raise ValueError("Start timestamp cannot be negative.")

        if end_time <= start_time:
            raise ValueError(
                "End timestamp must be greater than start timestamp."
            )

        # -----------------------------------------------------
        # Calculate midpoint
        # -----------------------------------------------------

        midpoint = (start_time + end_time) / 2

        # -----------------------------------------------------
        # Open video
        # -----------------------------------------------------

        cap = cv2.VideoCapture(str(self.video_path))

        if not cap.isOpened():
            raise RuntimeError(
                f"Could not open video: {self.video_path}"
            )

        # -----------------------------------------------------
        # Get FPS
        # -----------------------------------------------------

        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            cap.release()
            raise RuntimeError(
                "Could not determine video FPS."
            )

        # -----------------------------------------------------
        # Calculate frame number
        # -----------------------------------------------------

        frame_number = round(midpoint * fps)

        # -----------------------------------------------------
        # Seek to frame
        # -----------------------------------------------------

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_number,
        )

        success, frame = cap.read()

        cap.release()

        if not success:
            raise RuntimeError(
                "Could not extract midpoint frame."
            )

        # -----------------------------------------------------
        # Save frame
        # -----------------------------------------------------

        success = cv2.imwrite(
            str(self.output_path),
            frame,
        )

        if not success:
            raise RuntimeError(
                f"Could not save frame to: {self.output_path}"
            )

        # -----------------------------------------------------
        # Calculate actual timestamp
        # -----------------------------------------------------

        actual_timestamp = frame_number / fps

        print("\n========================================")
        print("FINAL DIALOGUE FRAME")
        print("========================================")

        print(f"Start     : {start_time:.3f}s")
        print(f"End       : {end_time:.3f}s")
        print(f"Midpoint  : {midpoint:.3f}s")
        print(f"Timestamp : {actual_timestamp:.3f}s")
        print(f"Frame     : {frame_number}")
        print(f"Image     : {self.output_path}")

        print("========================================")

        return {
            "start_timestamp": start_time,
            "end_timestamp": end_time,
            "midpoint": midpoint,
            "timestamp": actual_timestamp,
            "frame_number": frame_number,
            "image": str(self.output_path),
        }
