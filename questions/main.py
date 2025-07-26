#!/usr/bin/env python3
"""
main.py

Fetch both the transcript and comments for a YouTube video,
with a programmatic entrypoint `main(video_id, ...)`.
This version reads video_id from --video-id flag or VIDEO_ID env var,
so no positional argument is required.
"""

import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi
from get_comments import YouTubeCommentFetcher
from get_transcript import get_transcript


def main(
    video_id: str,
    transcript_out: str = "transcript.txt",
    comments_out: str = "comments.txt",
    languages: list[str] = ["en"],
):
    """
    Core logic: fetch transcript and comments for the given video_id.
    """
    # 1️⃣ Load config
    load_dotenv()
    api_key = os.getenv("GOOGLE_APIKEY")
    if not api_key:
        raise RuntimeError("GOOGLE_APIKEY env var not set")

    # 2️⃣ Fetch transcript
    print(f"Fetching transcript for video {video_id} …")
    transcript = get_transcript(video_id, languages=languages)
    Path(transcript_out).write_text(transcript, encoding="utf-8")
    print(f"✔ Saved transcript → {Path(transcript_out).resolve()}")

    # 3️⃣ Fetch comments
    print(f"Fetching comments for video {video_id} …")
    fetcher = YouTubeCommentFetcher(api_key)
    comments = fetcher.fetch_comments(
        video_id=video_id,
    )
    fetcher.save(comments, comments_out)


# if __name__ == "__main__":
#     load_dotenv()
#     # Preload video_id from env if set
#     default_vid = "uLsAhwJzQoI"
#     main(default_vid)
    # parser = argparse.ArgumentParser(
    #     description="Fetch transcript and comments for a YouTube video"
    # )
    # parser.add_argument(
    #     "-v", "--video-id",
    #     default=default_vid,
    #     help="YouTube video ID (e.g. dQw4w9WgXcQ). Can also set VIDEO_ID env var."
    # )
    # parser.add_argument(
    #     "-t", "--transcript-out",
    #     default="transcript.txt",
    #     help="Path to save the transcript"
    # )
    # parser.add_argument(
    #     "-c", "--comments-out",
    #     default="comments.txt",
    #     help="Path to save the comments"
    # )
    # parser.add_argument(
    #     "-n", "--limit",
    #     type=int,
    #     default=None,
    #     help="Max number of comments to fetch"
    # )
    # parser.add_argument(
    #     "-l", "--languages",
    #     nargs="+",
    #     default=["en"],
    #     help="Preferred transcript languages"
    # )
    # parser.add_argument(
    #     "--top-comments",
    #     action="store_true",
    #     help="Fetch relevance-ranked (top) comments instead of most recent"
    # )
    # args = parser.parse_args()

    # if not args.video_id:
    #     parser.error("--video-id is required (or set VIDEO_ID env var)")

    # main(
    #     video_id=args.video_id,
    #     transcript_out=args.transcript_out,
    #     comments_out=args.comments_out,
    #     languages=args.languages,
    # )