"""Builds src/data/timeline.json and src/data/captions.json from edit.json + transcript.raw.json.

Word timestamps from Whisper are relative to each raw clip; they are corrected,
shifted by the trim point and laid onto the final edit timeline.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
edit = json.load(open(f"{ROOT}/scripts/edit.json"))
raw = json.load(open(f"{ROOT}/scripts/transcript.raw.json"))
FPS = edit["fps"]

# Words rendered in the accent colour in captions
KEYWORDS = {"three", "3", "numbers", "hdb", "equity", "condo", "cpf", "refund", "monthly",
            "buffer", "exit", "worthwhile", "upgrade", "upgrading", "harder", "home", "properties",
            "first", "second", "third", "comfortable", "growth", "job", "usable"}

timeline, words_out = [], []
t = 0
for clip in edit["aroll"]:
    cid = str(clip["id"])
    cuts = [c for c in clip.get("cuts", [])]
    removed = sum(b - a for a, b in cuts)

    def to_clip(t):  # source time -> time inside the trimmed clip (with internal cuts removed)
        t = min(max(t, clip["in"]), clip["out"])
        for a, b in cuts:
            if t >= b:
                t -= b - a
            elif t > a:
                t = a
        return t - clip["in"]

    dur_f = round((clip["out"] - clip["in"] - removed) * FPS)
    start_f = t
    timeline.append({"id": clip["id"], "src": f"clips/a{clip['id']}.mp4", "from": start_f,
                     "dur": dur_f, "zoom": clip["zoom"], "voiceover": clip.get("voiceover", False)})
    words = [dict(w) for w in raw[cid]["words"]]
    for w, (ws, we) in zip(words, edit.get("word_times", {}).get(cid, [])):
        w["s"], w["e"] = ws, we
    corr = edit["corrections"].get(cid, {})
    fixed = []
    for i, w in enumerate(words):
        txt = corr.get(str(i), w["w"])
        if txt == "":
            fixed[-1]["e"] = w["e"]
            continue
        parts = txt.split()
        span = (w["e"] - w["s"]) / len(parts)
        for k, p in enumerate(parts):
            fixed.append({"w": p, "s": w["s"] + k * span, "e": w["s"] + (k + 1) * span})
    for i, w in enumerate(fixed):
        s = to_clip(w["s"])
        e = to_clip(w["e"])
        bare = re.sub(r"[^a-z0-9]", "", w["w"].lower())
        words_out.append({"clip": clip["id"], "i": i, "text": w["w"],
                          "start": round(start_f + s * FPS), "end": max(round(start_f + e * FPS), round(start_f + s * FPS) + 3),
                          "key": bare in KEYWORDS})
    t += dur_f

# B-roll laid over the voiceover clip
vo = next(c for c in timeline if c["voiceover"])
bt, broll = vo["from"], []
for b in edit["broll"]:
    d = round(b["dur"] * FPS)
    d = min(d, vo["from"] + vo["dur"] - bt)
    broll.append({"src": f"clips/{b['id']}.mp4", "from": bt, "dur": d})
    bt += d

# Group words into short caption pages (max 3 words, break on punctuation / clip change)
pages, cur = [], []
for w in words_out:
    if cur and (len(cur) == 3 or cur[-1]["clip"] != w["clip"] or re.search(r"[.,?!]$", cur[-1]["text"])
                or sum(len(x["text"]) for x in cur) + len(w["text"]) > 18):
        pages.append(cur); cur = []
    cur.append(w)
pages.append(cur)
cap_pages = []
for k, p in enumerate(pages):
    nxt = pages[k + 1][0]["start"] if k + 1 < len(pages) else p[-1]["end"] + 10
    end = min(nxt, p[-1]["end"] + 12)
    cap_pages.append({"start": p[0]["start"], "end": end, "words": p})

os.makedirs(f"{ROOT}/src/data", exist_ok=True)
json.dump({"fps": FPS, "total": t, "aroll": timeline, "broll": broll}, open(f"{ROOT}/src/data/timeline.json", "w"), indent=1)
json.dump({"words": words_out, "pages": cap_pages}, open(f"{ROOT}/src/data/captions.json", "w"), indent=1)
open(f"{ROOT}/transcript.txt", "w").write(
    "\n".join(" ".join(w["text"] for w in words_out if w["clip"] == c["id"]) for c in timeline) + "\n")
print("total frames", t, "=", t / FPS, "s;", len(cap_pages), "caption pages")
