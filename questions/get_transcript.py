#!/usr/bin/env python3
"""
transcript.py

Fetch a YouTube video’s transcript (auto‑ or manually‑generated captions)
and save it to transcript.txt.

Usage:
    $ pip install youtube-transcript-api
    $ python transcript.py
"""

from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_id: str, languages: list[str] = ['en']) -> str:
    """
    Fetch the transcript for `video_id` in the given language(s).

    Returns
    -------
    str
        The full transcript as one string, with each caption snippet
        on its own line.
    """
    api = YouTubeTranscriptApi()
    fetched = api.fetch(video_id, languages=languages)
    # Each `snippet` has a `.text` attribute
    return "\n".join(snippet.text for snippet in fetched)


if __name__ == "__main__":
    # ① Change this to your target video ID (or extend to use argparse)
    video = "uLsAhwJzQoI"

    # ② Fetch and save
    transcript = get_transcript(video)
    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"✔ Saved transcript for {video} → transcript.txt")
