# Video editing workflow

## Storyboard first — no rendering without approval
Before editing or rendering any footage:
1. Transcribe it with `python3 scripts/transcribe.py <video> <captions.json>` (word-level timestamps).
2. Write a storyboard as a table, one row per beat, with columns:
   **Time** (start–end) | **Exact words** (verbatim from the transcript, never paraphrased) | **On screen** | **Tool** (FFmpeg / Remotion / Whisper / yt-dlp).
3. Show it to the user and wait for explicit approval. Do not render or export anything until they approve.

## Tools
- `remotion/` — Remotion project (`npx remotion render src/index.ts <Composition> out/<file>.mp4`).
- `scripts/transcribe.py` — faster-whisper, outputs Remotion `Caption` JSON.
- FFmpeg and yt-dlp on PATH. If faster-whisper or yt-dlp are missing (the container resets), reinstall:
  `pip install --break-system-packages yt-dlp faster-whisper`.
- YouTube refuses downloads from this cloud environment; ask the user to upload the file instead.
