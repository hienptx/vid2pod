import yt_dlp

def download_audio(url: str, output_dir: str = "storage") -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".mp3")
    return filename

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=SA7bKo4HRTg"
    path = download_audio(test_url)
    print(f"Downloaded audio to: {path}")