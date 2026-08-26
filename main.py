from pathlib import Path
import subprocess
import yt_dlp


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/151.0.0.0 Safari/537.36"
)


# ---------------------------------------------------------
# Download Video
# ---------------------------------------------------------

def download_video(url: str) -> Path:
    """
    Download the video using yt-dlp and return the
    downloaded video path.
    """

    output_template = str(
        DOWNLOAD_DIR / "%(title)s.%(ext)s"
    )

    ydl_opts = {
        # Use the best single format available.
        # This is the configuration that worked
        # with the OK.ru downloader.
        "format": "best",

        # Save using the video's title.
        "outtmpl": output_template,

        # Ignore SSL certificate verification.
        "nocheckcertificate": True,

        # Browser-like User-Agent.
        "http_headers": {
            "User-Agent": USER_AGENT
        },

        # Do not download playlists.
        "noplaylist": True,

        # Show download progress.
        "quiet": False,
    }

    print("\n[1/2] Downloading video...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=True
            )

            # Get the actual downloaded filename.
            file_path = Path(
                ydl.prepare_filename(info)
            )

            # In case yt-dlp modifies the extension,
            # locate the actual downloaded file.
            if not file_path.exists():

                possible_files = list(
                    DOWNLOAD_DIR.glob(
                        f"{Path(file_path).stem}.*"
                    )
                )

                if possible_files:
                    file_path = possible_files[0]

            if not file_path.exists():
                raise FileNotFoundError(
                    "yt-dlp completed but the downloaded "
                    "video file could not be found."
                )

        print("\nDownload successful!")
        print(f"Video saved to: {file_path}")

        return file_path

    except Exception as e:
        raise RuntimeError(
            f"Video download failed: {e}"
        )


# ---------------------------------------------------------
# Extract Audio
# ---------------------------------------------------------

def extract_audio(video_path: Path) -> Path:
    """
    Extract the audio from the downloaded video.

    The audio is converted to MP3 with:
        - 16 kHz sample rate
        - mono channel

    This file will be uploaded to Google Colab
    for Whisper transcription.
    """

    audio_path = DOWNLOAD_DIR / "audio.mp3"

    print("\n[2/2] Extracting audio...")

    command = [
        "ffmpeg",

        # Overwrite existing audio.mp3.
        "-y",

        # Input video.
        "-i",
        str(video_path),

        # Disable video.
        "-vn",

        # MP3 encoder.
        "-acodec",
        "libmp3lame",

        # Whisper-friendly sample rate.
        "-ar",
        "16000",

        # Mono audio.
        "-ac",
        "1",

        # Output.
        str(audio_path),
    ]

    try:

        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    except FileNotFoundError:
        raise RuntimeError(
            "FFmpeg was not found. "
            "Make sure FFmpeg is installed and added "
            "to your system PATH."
        )

    except subprocess.CalledProcessError:
        raise RuntimeError(
            "FFmpeg failed while extracting audio."
        )

    if not audio_path.exists():
        raise FileNotFoundError(
            "Audio extraction failed. "
            "audio.mp3 was not created."
        )

    print(f"Audio saved to: {audio_path}")

    return audio_path


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    url = input(
        "Enter OK.ru video URL: "
    ).strip()

    if not url:
        print("Video URL cannot be empty.")
        return

    try:

        # -------------------------------------------------
        # Step 1: Download video
        # -------------------------------------------------

        video_path = download_video(url)

        # -------------------------------------------------
        # Step 2: Extract audio
        # -------------------------------------------------

        audio_path = extract_audio(
            video_path
        )

        # -------------------------------------------------
        # Final output
        # -------------------------------------------------

        print("\n========================================")
        print("VIDEO EXTRACTION COMPLETE")
        print("========================================")

        print(f"Video : {video_path}")
        print(f"Audio : {audio_path}")

        print("\nNext step:")
        print("Upload audio.mp3 to Google Colab.")
        print("Run Whisper Large-v3-Turbo.")
        print("Download word_transcribe.json back into Quest1.")

        print("========================================")

    except Exception as e:

        print(f"\nPipeline failed: {e}")


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()