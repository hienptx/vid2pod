#!/usr/bin/env python3
"""
generate_podcast.py

Read audience comments and a video transcript, then use the DeepSeek
chat/completions endpoint to generate a podcast-style dialogue.

Usage:
    $ pip install requests python-dotenv
    $ export DEEPSEEK_APIKEY="your_key_here"    # or put it in a .env file
    $ python generate_podcast.py \
          --comments comments.txt \
          --transcript transcript.txt \
          --system-prompt prompts/system.md \
          --user-prompt prompts/prompt.md \
          --output dialogue.txt \
          --max 1500
"""

import os
import argparse
from pathlib import Path
import requests
from dotenv import load_dotenv

class DeepSeekClient:
    """
    Minimal wrapper around DeepSeek's chat/completions API.
    """
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def generate_dialogue(
        self,
        comments: str,
        transcript: str,
        system_prompt: str,
        user_prompt: str,
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 1500,
        timeout: int = 60,
    ) -> str:
        """
        Call DeepSeek's /chat/completions endpoint to produce podcast dialogue.

        Returns the generated dialogue text.
        """
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "temperature": temperature,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": (
                        f"Comments:\n{comments}\n\n"
                        f"Transcript:\n{transcript}\n\n"
                        f"\n\n{user_prompt}"
                    )
                }
            ]
        }
        resp = self.session.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()


def read_file(path: Path) -> str:
    """Load text file contents, ensure file exists."""
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8")


def save_to_file(text: str, path: Path) -> None:
    """Write output text to file."""
    path.write_text(text, encoding="utf-8")
    print(f"✔ Saved to {path.resolve()}")


def main():
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_APIKEY")
    if not api_key:
        raise RuntimeError("Please set DEEPSEEK_APIKEY in your environment or .env file")

    parser = argparse.ArgumentParser(
        description="Generate podcast dialogue via DeepSeek"
    )
    parser.add_argument(
        "-c", "--comments",
        type=Path,
        default=Path("comments.txt"),
        help="Path to comments.txt"
    )
    parser.add_argument(
        "-t", "--transcript",
        type=Path,
        default=Path("transcript.txt"),
        help="Path to transcript.txt"
    )
    parser.add_argument(
        "-s", "--system-prompt",
        type=Path,
        default=Path("questions/prompts/system.md"),
        help="Path to system prompt template"
    )
    parser.add_argument(
        "-u", "--user-prompt",
        type=Path,
        default=Path("questions/prompts/prompt.md"),
        help="Path to user prompt template"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("dialogue.txt"),
        help="Output file for generated dialogue"
    )
    parser.add_argument(
        "-m", "--max",
        type=int,
        default=1500,
        help="Max tokens to generate (default: 1500)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="HTTP timeout in seconds (default: 60)"
    )
    args = parser.parse_args()

    # Load inputs
    comments = read_file(args.comments)
    transcript = read_file(args.transcript)
    system_prompt = read_file(args.system_prompt)
    user_template = read_file(args.user_prompt)

    # Build user prompt by injecting content
    user_prompt = user_template.format(
        comments=comments,
        transcript=transcript
    )

    # Generate dialogue
    client = DeepSeekClient(api_key)
    try:
        dialogue = client.generate_dialogue(
            comments=comments,
            transcript=transcript,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=args.max,
            timeout=args.timeout
        )
    except requests.exceptions.Timeout:
        raise RuntimeError(
            f"Request timed out after {args.timeout}s. "
            "Consider increasing --timeout or reducing --max tokens."
        )

    if not dialogue:
        print("⚠️  No dialogue returned.")
    else:
        save_to_file(dialogue, args.output)


if __name__ == "__main__":
    main()
