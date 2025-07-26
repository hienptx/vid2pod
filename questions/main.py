#!/usr/bin/env python3
"""
main.py

Fetch both the transcript and top‑level comments for a YouTube video,
and save them to separate text files.
"""

import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Import the pieces from your other scripts:
from youtube_transcript_api import YouTubeTranscriptApi
from get_comments import YouTubeCommentFetcher
from get_transcript import get_transcript

def main():
    # 1️⃣ Load config
    load_dotenv()  # optional .env support
    api_key = os.getenv("GOOGLE_APIKEY")
    if not api_key:
        raise RuntimeError("GOOGLE_APIKEY env var not set")

    # 2️⃣ Parse CLI
    parser = argparse.ArgumentParser(
        description="Fetch transcript and comments for a YouTube video"
    )
    parser.add_argument(
        "video_id",
        help="YouTube video ID (e.g. dQw4w9WgXcQ)"
    )
    parser.add_argument(
        "-t", "--transcript-out",
        default="transcript.txt",
        help="Path to save the transcript (default: transcript.txt)"
    )
    parser.add_argument(
        "-c", "--comments-out",
        default="comments.txt",
        help="Path to save the comments (default: comments.txt)"
    )
    parser.add_argument(
        "-n", "--limit",
        type=int,
        default=None,
        help="Max number of comments to fetch (default: all available)"
    )
    parser.add_argument(
        "-l", "--languages",
        nargs="+",
        default=["en"],
        help="Preferred transcript languages, in order (default: en)"
    )
    parser.add_argument(
        "--top-comments",
        action="store_true",
        help="Fetch relevance‑ranked (top) comments instead of most recent"
    )
    args = parser.parse_args()

    # 3️⃣ Fetch transcript
    print(f"Fetching transcript for video {args.video_id} …")
    transcript = get_transcript(args.video_id, languages=args.languages)
    Path(args.transcript_out).write_text(transcript, encoding="utf-8")
    print(f"✔ Saved transcript → {Path(args.transcript_out).resolve()}")

    # 4️⃣ Fetch comments
    print(f"Fetching comments for video {args.video_id} …")
    fetcher = YouTubeCommentFetcher(api_key)
    comments = fetcher.fetch_comments(
        video_id=args.video_id,
        limit=args.limit,
    )
    fetcher.save(comments, args.comments_out)

if __name__ == "__main__":
    main()
