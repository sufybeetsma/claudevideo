#!/usr/bin/env bash
# Usage: scripts/prep.sh "/path/to/CLAUDE VIDEO/video 1"
# Trims + transcodes source footage into public/clips (30fps H.264, cleaned & loudness-normalised audio).
set -euo pipefail
SRC="$1"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"; OUT="$ROOT/public/clips"; mkdir -p "$OUT"
AF="highpass=f=90,afftdn=nf=-30,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000"
python3 - "$ROOT/scripts/edit.json" <<'PY' | while IFS=$'\t' read -r kind id file in dur cut; do
import json,sys
e=json.load(open(sys.argv[1]))
for c in e["aroll"]:
    cut = "+".join(f"between(t,{a-c['in']:.3f},{b-c['in']:.3f})" for a, b in c.get("cuts", [])) or "0"
    print("a",c["id"],c["file"],c["in"],round(c["out"]-c["in"],3),cut,sep="\t")
for b in e["broll"]: print("b",b["id"],b["file"],b["in"],b["dur"],"0",sep="\t")
PY
  if [ "$kind" = a ]; then
    # internal cuts (pauses) are removed with select/aselect, then timestamps are rebuilt
    ffmpeg -nostdin -v error -y -ss "$in" -t "$dur" -i "$SRC/$file" \
      -vf "select='not($cut)',setpts=N/FRAME_RATE/TB,fps=30" -af "aselect='not($cut)',asetpts=N/SR/TB,$AF" \
      -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p -c:a aac -b:a 192k "$OUT/a$id.mp4"
  else
    ffmpeg -nostdin -v error -y -ss "$in" -t "$dur" -i "$SRC/$file" -r 30 -an -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p "$OUT/$id.mp4"
  fi
  echo "prepped $kind $id"
done
