#!/usr/bin/env bash
# Usage: scripts/prep.sh "/path/to/CLAUDE VIDEO/video 1"
# Trims + transcodes source footage into public/clips (30fps H.264, cleaned & loudness-normalised audio).
set -euo pipefail
SRC="$1"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"; OUT="$ROOT/public/clips"; mkdir -p "$OUT"
AF="highpass=f=90,afftdn=nf=-30,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000"
python3 - "$ROOT/scripts/edit.json" <<'PY' | while IFS=$'\t' read -r kind id file in dur; do
import json,sys
e=json.load(open(sys.argv[1]))
for c in e["aroll"]: print("a",c["id"],c["file"],c["in"],round(c["out"]-c["in"],3),sep="\t")
for b in e["broll"]: print("b",b["id"],b["file"],b["in"],b["dur"],sep="\t")
PY
  if [ "$kind" = a ]; then
    ffmpeg -nostdin -v error -y -ss "$in" -t "$dur" -i "$SRC/$file" -r 30 -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p -af "$AF" -c:a aac -b:a 192k "$OUT/a$id.mp4"
  else
    ffmpeg -nostdin -v error -y -ss "$in" -t "$dur" -i "$SRC/$file" -r 30 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "$OUT/$id.mp4"
  fi
  echo "prepped $kind $id"
done
