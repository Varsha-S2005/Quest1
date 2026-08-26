from retrieval.frame_extractor import FrameExtractor


VIDEO_PATH = "downloads/video.mp4"
OUTPUT_PATH = "final_dialogue_frame.jpg"

START_TIME = 324.940
END_TIME = 327.760


extractor = FrameExtractor(
    video_path=VIDEO_PATH,
    output_path=OUTPUT_PATH,
)


result = extractor.extract_midpoint_frame(
    start_time=START_TIME,
    end_time=END_TIME,
)


print("\nFrame extraction successful.")
print(f"Output: {result['image']}")