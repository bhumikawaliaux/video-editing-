"""Transcribe audio/video with word-level timestamps.

Usage: python3 scripts/transcribe.py input.mp4 [out.json] [--model small]
Writes JSON in Remotion's Caption shape: [{text, startMs, endMs, timestampMs, confidence}].
"""
import argparse
import json
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel


def load_audio(path):
    # Decode with the ffmpeg CLI rather than PyAV, whose newer releases break faster-whisper.
    raw = subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", path,
         "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(raw, np.float32)


p = argparse.ArgumentParser()
p.add_argument("input")
p.add_argument("output", nargs="?")
p.add_argument("--model", default="small")
p.add_argument("--language", default=None)
args = p.parse_args()

model = WhisperModel(args.model, device="cpu", compute_type="int8")
segments, info = model.transcribe(load_audio(args.input),word_timestamps=True, language=args.language)

captions = []
for seg in segments:
    for w in seg.words:
        start, end = round(w.start * 1000), round(w.end * 1000)
        captions.append({
            "text": w.word,
            "startMs": start,
            "endMs": end,
            "timestampMs": (start + end) // 2,
            "confidence": round(w.probability, 3),
        })

out = json.dumps(captions, indent=2, ensure_ascii=False)
if args.output:
    with open(args.output, "w") as f:
        f.write(out)
    print(f"{len(captions)} words, language={info.language} -> {args.output}", file=sys.stderr)
else:
    print(out)
