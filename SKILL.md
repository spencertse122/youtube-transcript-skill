---
name: youtube-transcript
description: Extract spoken content and captions from a YouTube video URL or video ID using youtube-transcript-api. Use for video summaries, content questions, or verifying a video's title or thumbnail claim; not for downloading video or audio.
---

# YouTube Transcript

Retrieve the transcript first when a user's question concerns the content of a specific YouTube video. Accept a full YouTube URL or a video ID. Do not imply that a transcript is a complete record of visuals, on-screen text, edits, or demonstrations.

## Retrieve

Use `scripts/fetch_transcript.py` for reliable URL/ID parsing and clean output. Run it with a Python environment that has the packages in `requirements.txt` installed. If the dependency is missing, explain the setup command in the repository README and ask before installing it on the user's behalf.

```bash
python3 scripts/fetch_transcript.py 'https://www.youtube.com/watch?v=VIDEO_ID' --languages en
```

The default output is plain text. Use `--timestamps` when temporal evidence matters and `--format json` when the timestamps or transcript metadata need to be processed further. Pass languages in preference order, for example `--languages vi,en`; omit the flag to prefer English as provided by the library.

If the desired language is unavailable, rerun with alternatives only when that serves the user's goal. The API prefers manual captions over generated captions when both are available.

## Answer from the transcript

- State that the answer is based on the transcript, especially for clickbait/title verification.
- Distinguish what the speaker actually says from an inference. Quote or cite timestamps when useful.
- For a clickbait question, give the direct answer first, then the short supporting passage and any important caveat.
- Say when the transcript cannot establish a visual-only claim; inspect the video separately only if a suitable tool and authorization are available.
- Do not fabricate missing portions. Mention whether captions were generated when that would affect confidence.

## Handle failures

Report the actionable cause from the script. Common cases are disabled/unavailable captions, an invalid or private video, age restrictions, and YouTube blocking the current IP. Do not repeatedly retry a blocked request. Proxy configuration can have privacy and cost implications, so ask before using a user-supplied or paid proxy.

The library accesses an undocumented YouTube endpoint and may occasionally break after YouTube changes it. For API details and updates, consult the project's PyPI page: <https://pypi.org/project/youtube-transcript-api/>.
