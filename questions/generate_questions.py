#!/usr/bin/env python3
"""
generate_questions.py

Read audience comments and a video transcript, then use the DeepSeek 
chat/completions endpoint to generate a list of interesting questions
the audience asked—or might ask—based on those inputs.

Usage:
    $ pip install requests python-dotenv
    $ export DEEPSEEK_API_KEY="your_key_here"    # or put it in a .env file
    $ python generate_questions.py \
          --comments comments.txt \
          --transcript transcript.txt \
          --output questions.txt \
          --max 20
"""

import os
import argparse
from pathlib import Path
import requests
from dotenv import load_dotenv

class DeepSeekClient:
    """
    Wrapper around DeepSeek's chat/completions API.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def generate_questions(
        self,
        comments: str,
        transcript: str,
        max_questions: int = 10,
        model: str = "deepseek-chat",
        temperature: float = 0.7,
    ) -> list[str]:
        """
        Calls DeepSeek's /chat/completions to produce audience questions.

        Parameters
        ----------
        comments : str
            The raw comments text.
        transcript : str
            The raw transcript text.
        max_questions : int
            How many questions to ask for.
        model : str
            Which model to use.
        temperature : float
            Sampling temperature.

        Returns
        -------
        list[str]
            Parsed list of questions.
        """
        endpoint = f"{self.base_url}/chat/completions"
        with open("questions/prompts/system.md", "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()

        with open("questions/prompts/prompt.md", "r", encoding="utf-8") as f:
            user_prompt = f.read().strip()

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
                        f"Generate up to {max_questions} numbered questions."
                        f"\n\n{user_prompt}"
                    )
                }
            ]
        }

        resp = self.session.post(endpoint, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # Expect: { "choices": [ { "message": { "content": "1. ...\n2. ..." } } ], ... }
        text = data["choices"][0]["message"]["content"]
        # Split on lines, strip out leading "1. ", etc.
        questions = [
            line.strip().lstrip("0123456789. ").strip()
            for line in text.splitlines()
            if line.strip()
        ]
        return questions


def read_file(path: Path) -> str:
    """Load the entire contents of a text file as UTF-8."""
    return path.read_text(encoding="utf-8")


def save_questions(questions: list[str], outfile: Path) -> None:
    """Write each question on its own line, numbered."""
    lines = [f"{q}" for q in questions]
    outfile.write_text("\n".join(lines), encoding="utf-8")
    print(f"✔ Saved {len(questions)} questions to {outfile.resolve()}")


def main() -> None:
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_APIKEY")
    if not api_key:
        raise RuntimeError("Please set DEEPSEEK_APIKEY in your env or .env file")

    parser = argparse.ArgumentParser(
        description="Generate audience questions via DeepSeek chat/completions"
    )
    parser.add_argument(
        "--comments", "-c",
        type=Path,
        default=Path("comments.txt"),
        help="Path to your comments.txt"
    )
    parser.add_argument(
        "--transcript", "-t",
        type=Path,
        default=Path("transcript.txt"),
        help="Path to your transcript.txt"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("questions.txt"),
        help="Where to write the generated questions"
    )
    parser.add_argument(
        "--max", "-m",
        type=int,
        default=10,
        help="Maximum number of questions to generate"
    )
    args = parser.parse_args()

    comments_text = read_file(args.comments)
    transcript_text = read_file(args.transcript)

    client = DeepSeekClient(api_key)
    questions = client.generate_questions(
        comments=comments_text,
        transcript=transcript_text,
        max_questions=args.max
    )

    if not questions:
        print("⚠️  No questions returned by DeepSeek.")
    else:
        save_questions(questions, args.output)


if __name__ == "__main__":
    main()
