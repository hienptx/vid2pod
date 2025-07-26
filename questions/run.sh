#!/usr/bin/env bash
# run.sh — fetch transcript and comments for a YouTube video
# Usage: ./run.sh VIDEO_ID [TRANSCRIPT_OUT] [COMMENTS_OUT]

set -euo pipefail

# Load environment variables from .env if present
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

VIDEO_ID="uLsAhwJzQoI"
TRANSCRIPT_OUT="transcript.txt"
COMMENTS_OUT="comments.txt"

rm -f "$TRANSCRIPT_OUT" "$COMMENTS_OUT"

echo "📥 Fetching transcript to ${TRANSCRIPT_OUT}"
python questions/main.py \
   "$VIDEO_ID"

echo "✅ Done!"