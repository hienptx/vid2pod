#!/usr/bin/env python3
"""
youtube_comments.py

Fetch top‑level comments for a YouTube video and save them to a
plain‑text file.

Usage (bash):

    $ pip install google-api-python-client python-dotenv
    $ export GOOGLE_APIKEY="your‑key"           # or use a .env file
    $ python youtube_comments.py uLsAhwJzQoI    # video ID
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List

from googleapiclient.discovery import build
from dotenv import load_dotenv


class YouTubeCommentFetcher:
    """
    Lightweight wrapper around the YouTube Data API v3 for pulling
    top‑level comments. Designed for easy reuse in larger codebases.
    """

    def __init__(self, api_key: str, max_results: int = 100) -> None:
        """
        Parameters
        ----------
        api_key : str
            Google API key enabled for YouTube Data API v3.
        max_results : int, default 100
            Max comments to return per API page (allowed range 1‑100).
        """
        self.max_results = max_results
        self.service = build("youtube", "v3", developerKey=api_key)

    def fetch_comments(self, video_id: str, limit: int | None = None) -> List[str]:
        """
        Retrieve top‑level comments.

        Parameters
        ----------
        video_id : str
            The 11‑character YouTube video ID.
        limit : int | None
            Hard cap on total comments returned.  None ⇒ fetch all available
            (subject to quota / pagination).

        Returns
        -------
        List[str]
            List of comment bodies in display order.
        """
        comments: List[str] = []
        request = self.service.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=self.max_results,
            textFormat="plainText",
        )

        while request:
            response = request.execute()
            for item in response.get("items", []):
                comment = (
                    item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    .replace("\u2028", "\n")  # keep newlines portable
                )
                comments.append(comment)
                if limit and len(comments) >= limit:
                    return comments

            request = self.service.commentThreads().list_next(request, response)

        return comments

    @staticmethod
    def save(comments: List[str], outfile: Path | str) -> None:
        """
        Write one comment per line to `outfile` (UTF‑8).

        Existing file will be overwritten.
        """
        path = Path(outfile)
        path.write_text("\n\n".join(comments), encoding="utf-8")
        print(f"✔ Saved {len(comments)} comments → {path.resolve()}")


def main() -> None:
    # 1️⃣  Load config
    load_dotenv()  # optional .env file
    api_key = os.getenv("GOOGLE_APIKEY")
    if not api_key:
        raise RuntimeError("GOOGLE_APIKEY env var not set")

    # 2️⃣  Parse CLI
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch YouTube top‑level comments to a text file"
    )
    # parser.add_argument("video_id", help="YouTube video ID (e.g. dQw4w9WgXcQ)")

    parser.add_argument(
        "video_id",
        nargs="?",
        default="uLsAhwJzQoI",            # ← your chosen default
        help="YouTube video ID (default: %(default)s)"
    )

    parser.add_argument(
        "-o",
        "--outfile",
        default="comments.txt",
        help="Output file path (default: comments.txt)",
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=None,
        help="Maximum number of comments to save (default: all available)",
    )

    parser.add_argument(
        "-t", "--top-comments",
        action="store_true",
        help="Fetch relevance‑ranked (top) comments instead of most recent"
    )
    args = parser.parse_args()

    # 3️⃣  Run
    fetcher = YouTubeCommentFetcher(api_key)
    comments = fetcher.fetch_comments(args.video_id, limit=args.limit)

    
    fetcher.save(comments, args.outfile)


if __name__ == "__main__":
    main()
