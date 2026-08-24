import yt_dlp

# Ask the user to enter the OK.ru video URL
url = input("Enter OK.ru video URL: ")

# Configure yt-dlp
ydl_opts = {
    # Save the downloaded video inside the downloads folder
    "outtmpl": "downloads/%(title)s.%(ext)s",

    # Select the highest-quality HLS stream available
    "format": "best",

    # Ignore the SSL certificate issue in our local environment
    "nocheckcertificate": True,

    # Use a browser-like User-Agent
    "http_headers": {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        )
    },
}

try:
    # Create the yt-dlp downloader
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        # Extract information and download the video
        info = ydl.extract_info(url, download=True)

        # Get the downloaded file path
        file_path = ydl.prepare_filename(info)

        print("\nDownload successful!")
        print(f"Saved file: {file_path}")

except Exception as e:
    # Display a clear error message
    print(f"\nDownload failed: {e}")