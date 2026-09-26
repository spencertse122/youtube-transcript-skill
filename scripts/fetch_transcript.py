#!/usr/bin/env python3
"""Fetch a YouTube transcript as readable text or structured JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import parse_qs, urlparse


def video_id_from(value: str) -> str:
    """Accept a YouTube URL or a raw video identifier."""
    value = value.strip()
    parsed = urlparse(value)
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    video_id = ""

    if host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        else:
            match = re.match(r"^/(?:shorts|embed|live)/([^/?#]+)", parsed.path)
            if match:
                video_id = match.group(1)
    elif host == "youtu.be":
        video_id = parsed.path.lstrip("/").split("/")[0]
    elif not parsed.scheme and not parsed.netloc:
        video_id = value

    if not re.fullmatch(r"[A-Za-z0-9_-]{6,64}", video_id):
        raise ValueError("Provide a valid YouTube watch, short, embed, or youtu.be URL, or a video ID.")
    return video_id


def format_timestamp(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:d}:{seconds:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="YouTube URL or video ID")
    parser.add_argument(
        "--languages",
        nargs="+",
        metavar="LANG",
        default=["en"],
        help="Preferred language codes, in order (default: en)",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--timestamps", action="store_true", help="Prefix text output with timestamps")
    parser.add_argument("--preserve-formatting", action="store_true")
    args = parser.parse_args()

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("Missing dependency: install it with `python3 -m pip install youtube-transcript-api`.", file=sys.stderr)
        return 2

    try:
        video_id = video_id_from(args.video)
        transcript = YouTubeTranscriptApi().fetch(
            video_id,
            languages=args.languages,
            preserve_formatting=args.preserve_formatting,
        )
    except ValueError as exc:
        print(f"Invalid video input: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # Library exceptions vary between releases.
        print(f"Could not fetch the transcript: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps({
            "video_id": transcript.video_id,
            "language": transcript.language,
            "language_code": transcript.language_code,
            "is_generated": transcript.is_generated,
            "snippets": transcript.to_raw_data(),
        }, ensure_ascii=False, indent=2))
        return 0

    for snippet in transcript:
        prefix = f"[{format_timestamp(snippet.start)}] " if args.timestamps else ""
        print(f"{prefix}{snippet.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
