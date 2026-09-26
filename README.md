# YouTube Transcript skill

A Codex skill that retrieves captions from a YouTube video and answers questions from the transcript. It includes a small command-line helper for YouTube URL parsing and transcript output as text or JSON.

## Install the dependency

Use a virtual environment if you do not already have an environment for this tool:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Use the helper

```bash
python scripts/fetch_transcript.py 'https://www.youtube.com/watch?v=VIDEO_ID' --languages en
```

Useful options include `--timestamps`, `--format json`, `--preserve-formatting`, and `--languages vi en`.

To use it as a Codex skill, place this repository's skill folder in your Codex skills directory (commonly `~/.codex/skills/youtube-transcript`) and install the dependency in the Python environment used to run the helper. Read [SKILL.md](SKILL.md) for transcript handling guidance and limitations.

The helper relies on the [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/) package and YouTube's caption availability. It does not download video or audio and cannot establish claims visible only in the video.
