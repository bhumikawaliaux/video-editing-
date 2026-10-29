"""Transcribe audio/video with word-level timestamps.

Usage: python3 scripts/transcribe.py input.mp4 [out.json] [--model small]
Writes JSON in Remotion's Caption shape: [{text, startMs, endMs, timestampMs, confidence}].
"""
import argparse
import json
import sys

from faster_whisper import WhisperModel

p = argparse.ArgumentParser()
p.add_argument("input")
p.add_argument("output", nargs="?")
p.add_argument("--model", default="small")
p.add_argument("--language", default=None)
args = p.parse_args()

model = WhisperModel(args.model, device="cpu", compute_type="int8")
segments, info = model.transcribe(args.input, word_timestamps=True, language=args.language)

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
