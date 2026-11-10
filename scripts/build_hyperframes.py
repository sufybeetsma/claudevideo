"""Generates hyperframes/index.html: the HyperFrames version of the "video 1" edit.

It reads the same edit data as the Remotion version (src/data/timeline.json and
src/data/captions.json, produced by scripts/build_data.py), so both builds share
one cut, one transcript and one set of timings.

Run:  python3 scripts/build_hyperframes.py   (then: cd hyperframes && npm run render)
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(f"{ROOT}/src/data/timeline.json"))
CAP = json.load(open(f"{ROOT}/src/data/captions.json"))
FPS = TL["fps"]
TOTAL = TL["total"] / FPS

# ---------------------------------------------------------------- brand + safe zone
C = dict(maroon="#963F66", maroonDark="#5E2440", maroonLight="#E3A3C1", cream="#F3F0EC",
         creamEdge="#CFC8C2", grey="#60585D", ink="#2B2528")
# Instagram Reels + TikTok safe zone on 1080x1920: clear of top 220, bottom 420, right 140, left 60
SAFE = dict(top=220, bottom=1500, left=60, right=940)
SAFE_W = SAFE["right"] - SAFE["left"]
TOP = SAFE["top"] + 20


def extrude(color, depth=6, shadow=True):
    s = ", ".join(f"0 {i + 1}px 0 {color}" for i in range(depth))
    return s + (f", 0 {depth + 6}px {depth * 2 + 8}px rgba(0,0,0,0.45)" if shadow else "")


def sec(f):
    return round(f / FPS, 3)


def bare(s):
    return re.sub(r"[^a-z0-9-]", "", s.lower())


def at(clip, text, nth=0, edge="start"):
    hits = [w for w in CAP["words"] if w["clip"] == clip and bare(w["text"]).startswith(bare(text))]
    return sec(hits[nth][edge])


def clip(cid):
    c = next(x for x in TL["aroll"] if x["id"] == cid)
    return sec(c["from"]), sec(c["from"] + c["dur"])


els, js, uid = [], [], [0]


def nid(prefix):
    uid[0] += 1
    return f"{prefix}{uid[0]}"


# ---------------------------------------------------------------- GSAP helpers (emitted JS)
def pop(el_id, start, end, d="up", float_=True):
    """3D flip-in at `start`, gentle 3D float while on screen, flip-out before `end`."""
    rx, ry = {"up": (75, 0), "down": (-75, 0), "left": (25, -80), "none": (25, 35)}[d]
    js.append(
        f'tl.fromTo("#{el_id} > .p", {{opacity:0, rotationX:{rx}, rotationY:{ry}, z:-200, scale:0.75}},'
        f' {{opacity:1, rotationX:0, rotationY:0, z:0, scale:1, duration:0.55, ease:"back.out(1.7)"}}, {start});')
    js.append(
        f'tl.to("#{el_id} > .p", {{opacity:0, rotationX:-50, z:-250, duration:0.22, ease:"power2.in"}}, {max(start + 0.3, end - 0.24)});')
    if float_ and end - start > 1.2:
        n = int((end - start) / 1.6)
        js.append(
            f'tl.fromTo("#{el_id} .f", {{rotationY:-4, rotationX:3}}, {{rotationY:4, rotationX:-3, duration:0.8,'
            f' ease:"sine.inOut", yoyo:true, repeat:{max(1, n * 2 - 1)}}}, {start});')


def graphic(start, end, inner, style="", d="up", float_=True, cls="band"):
    gid = nid("g")
    els.append(
        f'<div id="{gid}" class="clip g {cls}" data-start="{start}" data-duration="{round(end - start, 3)}" style="{style}">'
        f'<div class="p"><div class="f">{inner}</div></div></div>')
    pop(gid, start, end, d, float_)
    return gid


def sub_pop(start, inner, d="up"):
    """An element inside a graphic that pops in later (stays until the parent ends)."""
    sid = nid("s")
    rx = {"up": 70, "none": 0, "left": 20}[d]
    ry = {"up": 0, "none": 40, "left": -70}[d]
    js.append(f'tl.fromTo("#{sid}", {{opacity:0, rotationX:{rx}, rotationY:{ry}, scale:0.6}},'
              f' {{opacity:1, rotationX:0, rotationY:0, scale:1, duration:0.45, ease:"back.out(2)"}}, {start});')
    return f'<div id="{sid}" class="sp">{inner}</div>'


def H(size, color=C["ink"], depth=0, extra=""):
    ec = C["maroonDark"] if color in (C["cream"], C["maroon"]) else C["creamEdge"]
    ts = f"text-shadow:{extrude(ec, depth, False)};" if depth else ""
    return f'class="h" style="font-size:{size}px;color:{color};{ts}{extra}"'


CHECK = ('<svg class="chk" width="{s}" height="{h}" viewBox="0 0 40 44"><circle cx="20" cy="24" r="19" fill="#5E2440"/>'
         '<circle cx="20" cy="20" r="19" fill="#963F66"/><path id="{id}" d="M11 21 L18 28 L30 13" fill="none" stroke="#F3F0EC"'
         ' stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="30" stroke-dashoffset="{off}"/></svg>')


def check(size=40, draw_at=None):
    cid = nid("c")
    if draw_at is not None:
        js.append(f'tl.fromTo("#{cid}", {{attr:{{"stroke-dashoffset":30}}}}, {{attr:{{"stroke-dashoffset":0}}, duration:0.27, ease:"power2.out"}}, {draw_at});')
    return CHECK.format(s=size, h=round(size * 1.1), id=cid, off=30 if draw_at is not None else 0)


CROSS = ('<svg width="36" height="36" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="#F3F0EC"/>'
         '<path d="M13 13 L27 27 M27 13 L13 27" stroke="#963F66" stroke-width="5" stroke-linecap="round"/></svg>')


def arrow(size=60):
    return (f'<svg width="{size}" height="{round(size * .7)}" viewBox="0 0 60 42" style="overflow:visible">'
            '<path d="M4 22 H48 M34 8 L52 22 L34 36" fill="none" stroke="#5E2440" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M4 18 H48 M34 4 L52 18 L34 32" fill="none" stroke="#963F66" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def strike(at_s, thickness=10):
    lid = nid("l")
    js.append(f'tl.fromTo("#{lid}", {{scaleX:0}}, {{scaleX:1, duration:0.27, ease:"power2.out"}}, {at_s});')
    return f'<div id="{lid}" class="strike" style="height:{thickness}px"></div>'


def chip(label, color=C["maroon"], text=C["cream"]):
    edge = C["maroonDark"] if color == C["maroon"] else "#3E383B"
    return (f'<div class="chip" style="background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(255,255,255,0) 60%),{color};'
            f'color:{text};box-shadow:0 7px 0 {edge},0 18px 30px rgba(0,0,0,.4)">{label}</div>')


def card(inner, style=""):
    return f'<div class="card" style="{style}">{inner}</div>'


SFX = []


def sfx(t, name, vol):
    SFX.append((round(max(0, t), 3), name, vol))


# ---------------------------------------------------------------- footage
PUNCHES = {1: (at(1, "three"), .12), 5: (at(5, "usable"), .08), 7: (at(7, "worthwhile"), .10),
           10: (at(10, "equity"), .10), 12: (at(12, "dm"), .08)}
for c in TL["aroll"]:
    s, d = sec(c["from"]), sec(c["dur"])
    vid = f"a{c['id']}"
    els.append(f'<video id="{vid}" class="clip vid" src="assets/{c["src"]}" data-start="{s}" '
               f'data-duration="{d}" data-media-start="0" data-has-audio="true" playsinline></video>')
    z0, z1 = c["zoom"], c["zoom"] + 0.04
    if c["id"] in PUNCHES:  # slow push-in, with a springy punch-in on the emphasis word
        pt, amt = PUNCHES[c["id"]]
        mid = z0 + 0.04 * (pt - s) / d
        js.append(f'tl.fromTo("#{vid}", {{scale:{z0}}}, {{scale:{mid:.4f}, duration:{pt - s:.3f}, ease:"none"}}, {s});')
        js.append(f'tl.to("#{vid}", {{scale:{mid + amt:.4f}, duration:0.3, ease:"back.out(2)"}}, {pt});')
        rest = s + d - pt - 0.3
        if rest > 0:
            js.append(f'tl.to("#{vid}", {{scale:{z1 + amt:.4f}, duration:{rest:.3f}, ease:"none"}}, {pt + 0.3:.3f});')
    else:
        js.append(f'tl.fromTo("#{vid}", {{scale:{z0}}}, {{scale:{z1}, duration:{d}, ease:"none"}}, {s});')
    if c["from"] > 0 and not c["voiceover"]:  # soft cream flash on each jump cut
        fid = nid("fl")
        els.append(f'<div id="{fid}" class="clip flash" data-start="{s}" data-duration="0.12"></div>')
        js.append(f'tl.fromTo("#{fid}", {{opacity:0.18}}, {{opacity:0, duration:0.1}}, {s});')

vo = next(c for c in TL["aroll"] if c["voiceover"])
els.append(f'<div id="bwrap" class="brollwrap">')  # untimed wrapper: only gives the 3D perspective
for i, b in enumerate(TL["broll"]):
    s, d = sec(b["from"]), sec(b["dur"])
    bid = f"b{i + 1}"
    els.append(f'<video id="{bid}" class="clip vid broll" src="assets/{b["src"]}" data-start="{s}" data-duration="{d}" '
               f'data-media-start="0" muted playsinline data-layout-allow-overflow></video>')
    # 3D swing-in: the new shot turns in on its Y axis like a panel, then drifts in slowly
    js.append(f'tl.fromTo("#{bid}", {{rotationY:-55, scale:1.29}}, {{rotationY:0, scale:1.06, duration:0.6, ease:"power3.out"}}, {s});')
    js.append(f'tl.to("#{bid}", {{scale:1.12, duration:{max(0.1, d - 0.6):.3f}, ease:"none"}}, {s + 0.6:.3f});')
    fid = nid("fl")
    els.append(f'<div id="{fid}" class="clip flash" data-start="{s}" data-duration="0.2"></div>')
    js.append(f'tl.fromTo("#{fid}", {{opacity:0.35}}, {{opacity:0, duration:0.17}}, {s});')
    sfx(s, "whoosh", .35)

els.append("</div>")
els.append(f'<div id="bshade" class="clip shade" data-start="{sec(vo["from"])}" data-duration="{sec(vo["dur"])}"></div>')

# ---------------------------------------------------------------- motion graphics
c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12 = (clip(i) for i in range(1, 13))
hook = at(1, "three")

# 1 · hook
graphic(c1[0] + 0.07, hook, chip("Insider tip"))
sfx(c1[0] + .07, "whoosh", .35)
ul = nid("u")
js.append(f'tl.fromTo("#{ul}", {{scaleX:0}}, {{scaleX:1, duration:0.4, ease:"power2.out"}}, {hook + 0.2:.3f});')
graphic(hook, c1[1], card(
    f'<div {H(124, C["maroon"], 7)}>3 numbers</div>'
    f'<div id="{ul}" class="uline"></div>'
    f'<div {H(46, C["grey"])}>I check before my clients upgrade</div>', "align-items:center;padding:26px 40px"))
sfx(hook, "boom", .55)

# 2 · HDB equity bars
hdb = at(2, "hdb")
bars = "".join(
    f'<div id="{nid("bar")}" class="bar" style="height:{h}px;background:{C["maroon"] if i == 3 else C["grey"]};'
    f'box-shadow:6px 0 0 {C["maroonDark"] if i == 3 else "#3E383B"}"></div>' for i, h in enumerate([40, 62, 88, 120]))
graphic(hdb, c2[1], card(
    f'<div class="row" style="gap:30px"><div class="bars">{bars}</div><div>'
    f'<div {H(40, C["grey"], extra="text-align:left")}>HDB</div>'
    f'<div {H(72, C["maroon"], 5, "text-align:left")}>Equity</div>'
    f'<div {H(34, C["grey"], extra="text-align:left")}>already built up</div></div></div>'))
js.append(f'tl.fromTo(".bar", {{scaleY:0}}, {{scaleY:1, duration:0.5, ease:"back.out(2)", stagger:0.13}}, {hdb + 0.13:.3f});')
sfx(hdb, "whoosh", .35)
sfx(at(2, "equity"), "coin", .35)

# 3 · wrong question
condo, afford = at(3, "condo"), at(3, "afford", 0, "end")
graphic(condo - 0.07, c3[1],
        card(f'<div style="position:relative"><div {H(58)}>“What condo can they afford?”</div>{strike(afford - 0.13)}</div>')
        + sub_pop(afford, chip(f"{CROSS} Wrong question"), "none"))
sfx(condo - .07, "whoosh", .35)
sfx(afford, "buzz", .22)

# 4 · three checks
t4 = at(4, "three")
balls = "".join(sub_pop(t4 + i * 0.17, f'<div {H(76, C["cream"], 4).replace('class="h"', 'class="h ball"')}>{n}</div>', "none") for i, n in enumerate([1, 2, 3]))
graphic(t4 - 0.13, c4[1], f'<div {H(96, C["cream"], 7)}>3 checks</div><div class="row" style="gap:30px">{balls}</div>')
for i in range(3):
    sfx(t4 + i * .17, "pop", .5)

# 5-7 · step tracker + title + keyword chips
STEPS = ["Equity", "Monthly", "Exit"]


def tracker(active):
    out = []
    for i, s in enumerate(STEPS):
        bg = C["maroon"] if i == active else C["cream"]
        col = C["cream"] if i == active else C["maroon"] if i < active else C["grey"]
        edge = C["maroonDark"] if i == active else C["creamEdge"]
        icon = check(28) if i < active else f"<span>{i + 1}</span>"
        out.append(f'<div class="pill" style="background:{bg};color:{col};box-shadow:0 6px 0 {edge},0 14px 22px rgba(0,0,0,.35)">{icon}{s}</div>')
    return '<div class="row" style="gap:14px">' + "".join(out) + "</div>"


def step(n, title, rng, chips):
    s, e = rng
    gid = nid("st")
    chips_html = "".join(sub_pop(t, chip(lbl, col)) for t, lbl, col in chips)
    title_html = card(f'<div class="row" style="gap:22px"><div {H(78, C["maroon"], 5)}>0{n}</div><div {H(54)}>{title}</div></div>', "padding:16px 32px")
    els.append(f'<div id="{gid}" class="clip g band" data-start="{s}" data-duration="{round(e - s, 3)}">'
               f'{tracker(n - 1)}'
               f'<div class="p" style="perspective:1200px">{title_html}</div>'
               f'<div class="row wrap" style="gap:14px">{chips_html}</div></div>')
    js.append(f'tl.fromTo("#{gid} > .p", {{opacity:0, rotationY:-80, rotationX:25, z:-200, scale:.75}},'
              f' {{opacity:1, rotationY:0, rotationX:0, z:0, scale:1, duration:0.55, ease:"back.out(1.7)"}}, {s});')
    js.append(f'tl.to("#{gid}", {{opacity:0, duration:0.2}}, {e - 0.2:.3f});')
    sfx(s, "whoosh", .4)


step(1, "Usable equity", c5, [(at(5, "loan"), "– Loan", C["grey"]), (at(5, "cpf"), "– CPF refund", C["grey"]),
                              (at(5, "selling"), "– Selling costs", C["grey"])])
step(2, "Monthly comfort", c6, [(at(6, "monthly"), "Sustainable commitment", C["grey"]), (at(6, "buffer"), "+ Healthy buffer", C["maroon"])])
step(3, "Exit potential", c7, [(at(7, "exit"), "Value at exit", C["grey"]), (at(7, "worthwhile"), "Worth the move?", C["maroon"])])
for w, f in [(at(5, "loan"), "pop"), (at(5, "cpf"), "pop"), (at(5, "selling"), "pop"), (at(6, "monthly"), "pop"),
             (at(6, "buffer"), "coin"), (at(7, "exit"), "pop"), (at(7, "worthwhile"), "boom")]:
    sfx(w, f, .45 if f == "pop" else .35)

# 8 · numbers first
n8, p8 = at(8, "numbers"), at(8, "properties")
graphic(n8, c8[1], card(
    f'<div class="row" style="gap:18px">{check(60)}<div {H(60, C["maroon"], 5)}>Numbers first</div></div>'
    + sub_pop(p8, f'<div class="row" style="gap:18px;margin-top:14px">{arrow()}<div {H(60, C["grey"], 4)}>Then properties</div></div>', "left")))
sfx(n8, "ding", .35)
sfx(p8, "pop", .45)


# 9 · B-roll checklists
def panel(title, s, e, rows):
    rows_html = "".join(sub_pop(t - 0.1, f'<div class="row" style="gap:20px;padding:8px 0;justify-content:flex-start">{check(50, t)}'
                                         f'<div {H(44, C["ink"], extra="text-align:left")}>{lbl}</div></div>', "left") for lbl, t in rows)
    graphic(s, e, card(f'<div {H(56, C["maroon"], 5, "text-align:left;margin-bottom:12px")}>{title}</div>{rows_html}',
                       "padding:30px 38px;align-items:flex-start"),
            style=f"left:{SAFE['left'] + 30}px;width:{SAFE_W - 60}px;top:{TOP + 60}px", cls="panel")


ev = at(9, "eventually")
r1 = [("Entry prices", at(9, "entry")), ("Surrounding transactions", at(9, "surrounding")),
      ("Unit-specific factors", at(9, "unit-specific")), ("Future exit potential", at(9, "future"))]
r2 = [("Entry made sense", at(9, "entry", 1)), ("Clear growth drivers", at(9, "growth")), ("Comfortable financing", at(9, "financing"))]
panel("What we compared", c9[0], ev, r1)
panel("The one we found", ev, c9[1], r2)
for _, t in r1:
    sfx(t, "tick", .6)
for _, t in r2:
    sfx(t, "ding", .3)

# 10 · HDB → condo, then equity work harder
h10, cd10, its10, eq10, hard = at(10, "hdb"), at(10, "condo", 0, "end"), at(10, "it's"), at(10, "equity"), at(10, "harder")
graphic(h10, its10, card(f'<div class="row" style="gap:26px;position:relative"><div {H(76, C["grey"], 5)}>HDB</div>{arrow(70)}'
                         f'<div {H(76, C["grey"], 5)}>Condo</div>{strike(cd10 - 0.07, 12)}</div>'))
graphic(eq10 - 0.13, c10[1], card(
    f'<div {H(46, C["grey"])}>Make your</div><div {H(92, C["maroon"], 7)}>Equity</div>'
    + sub_pop(hard - 0.07, f'<div {H(64, C["cream"], 3, "background:#963F66;padding:6px 24px;border-radius:14px;box-shadow:0 8px 0 #5E2440,0 18px 26px rgba(0,0,0,.4)")}>Work harder</div>', "none"),
    "align-items:center;gap:6px"))
sfx(h10, "whoosh", .35)
sfx(cd10, "buzz", .18)
sfx(eq10, "coin", .35)

# 11 · question
h11 = at(11, "hdb")
qid = nid("q")
graphic(h11 - 0.07, c11[1], card(
    f'<div class="row" style="gap:24px"><div id="{qid}" {H(140, C["maroon"], 8)}>?</div><div>'
    f'<div {H(44, C["grey"], extra="text-align:left")}>Has your HDB</div>'
    f'<div {H(64, C["maroon"], 5, "text-align:left")}>done its job?</div></div></div>'))
js.append(f'tl.fromTo("#{qid}", {{y:-6, rotation:-6}}, {{y:6, rotation:6, duration:0.5, ease:"sine.inOut", yoyo:true, repeat:5}}, {h11:.3f});')
sfx(h11, "whoosh", .35)

# 12 · CTA
dm, send = at(12, "dm"), at(12, "send")
btn = nid("cta")
graphic(dm, TOTAL, f'<div id="{btn}" {H(84, C["cream"], 5, "background:linear-gradient(180deg,#B4537F 0%,#963F66 55%);padding:24px 48px;border-radius:999px;box-shadow:0 12px 0 #5E2440,0 0 0 10px rgba(243,240,236,.35),0 34px 50px rgba(0,0,0,.5)")}>DM me “HOME”</div>'
        + sub_pop(send, card(f'<div {H(38, C["maroon"])}>Get my exact 3-number checklist</div>', "padding:14px 30px;margin-top:16px")),
        float_=False)
js.append(f'tl.fromTo("#{btn}", {{scale:1, rotationX:-6}}, {{scale:1.05, rotationX:6, duration:0.42, ease:"sine.inOut", yoyo:true, repeat:{int((TOTAL - dm) / .42)}}}, {dm + 0.5:.3f});')
sfx(dm - 26 / FPS, "riser", .35)
sfx(dm, "ding", .45)
sfx(send, "pop", .45)

# ---------------------------------------------------------------- captions (word-by-word, 3D, in the safe zone)
cap_els = []
for k, p in enumerate(CAP["pages"]):
    s, e = sec(p["start"]), sec(min(p["end"], TL["total"]))
    if k == len(CAP["pages"]) - 1:
        e = round(TOTAL, 3)  # hold the closing line to the end
    pid = f"cap{k}"
    words = []
    for w in p["words"]:
        wid = f"w{w['clip']}_{w['i']}"
        cls = "w key" if w["key"] else "w"
        words.append(f'<span id="{wid}" class="{cls}">{html.escape(w["text"])}</span>')
        ws, we = sec(w["start"]), sec(max(w["end"], w["start"] + 4))
        we = max(we, round(ws + 0.2, 3))
        js.append(f'tl.set("#{wid}", {{attr:{{class:"{cls} on"}}}}, {ws});')
        off = round(min(we, e), 3)
        pd = round(max(0.03, min(0.18, off - ws - 0.02)), 3)
        js.append(f'tl.fromTo("#{wid}", {{rotationX:12, scale:1, y:0}}, {{rotationX:0, scale:1.08, y:-6, duration:{pd}, ease:"back.out(3)"}}, {ws});')
        js.append(f'tl.set("#{wid}", {{attr:{{class:"{cls} done"}}, scale:1, y:0}}, {off});')
    cap_els.append(f'<div id="{pid}" class="clip cap" data-start="{s}" data-duration="{round(e - s, 3)}">{"".join(words)}</div>')
    js.append(f'tl.fromTo("#{pid}", {{opacity:0, scale:0.85}}, {{opacity:1, scale:1, duration:0.2, ease:"back.out(2)"}}, {s});')
els += cap_els

# ---------------------------------------------------------------- audio
audio = [f'<audio id="music" class="clip" src="assets/music/bed.mp3" data-start="0" data-duration="{TOTAL:.3f}" '
         f'data-media-start="0" data-volume="0.11" data-fade-in="0.5" data-fade-out="1.5"></audio>']
for i, (t, name, vol) in enumerate(sorted(SFX)):
    dur = {"ding": 1.0, "riser": 0.9, "boom": 0.9, "coin": 0.6, "whoosh": 0.5, "buzz": 0.35, "pop": 0.14, "tick": 0.05}[name]
    dur = round(min(dur, TOTAL - t), 3)
    if dur <= 0:
        continue
    audio.append(f'<audio id="sfx{i}" class="clip" src="assets/sfx/{name}.wav" data-start="{t}" data-duration="{dur}" '
                 f'data-media-start="0" data-volume="{vol}"></audio>')

CSS = f"""
@font-face {{ font-family: 'Montserrat'; font-weight: 800; src: url('assets/fonts/montserrat-latin-800-normal.woff2') format('woff2'); }}
@font-face {{ font-family: 'Montserrat'; font-weight: 900; src: url('assets/fonts/montserrat-latin-900-normal.woff2') format('woff2'); }}
:root {{ --maroon:{C['maroon']}; --maroon-dark:{C['maroonDark']}; --maroon-light:{C['maroonLight']}; --cream:{C['cream']};
  --cream-edge:{C['creamEdge']}; --grey:{C['grey']}; --ink:{C['ink']}; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:'Montserrat', sans-serif; }}
.clip {{ position:absolute; }}
.vid {{ inset:0; width:1080px; height:1920px; object-fit:cover; transform-origin:50% 32%; }}
.brollwrap {{ position:absolute; inset:0; overflow:hidden; perspective:1400px; }}
.broll {{ transform-origin:0% 50%; }}
.shade {{ inset:0; background:linear-gradient(180deg, rgba(0,0,0,.35) 0%, rgba(0,0,0,0) 45%, rgba(0,0,0,.25) 100%); }}
.flash {{ inset:0; background:var(--cream); opacity:0; }}
.g {{ display:flex; flex-direction:column; align-items:center; gap:16px; }}
.band {{ left:{SAFE['left']}px; width:{SAFE_W}px; top:{TOP}px; }}
.p {{ display:flex; flex-direction:column; align-items:center; perspective:1200px; transform-style:preserve-3d; }}
.f {{ display:flex; flex-direction:column; align-items:center; gap:16px; transform-style:preserve-3d; }}
.sp {{ display:flex; justify-content:center; }}
.row {{ display:flex; align-items:center; justify-content:center; }}
.wrap {{ flex-wrap:wrap; }}
.h {{ font-family:'Montserrat', sans-serif; font-weight:900; line-height:1.02; text-transform:uppercase; text-align:center; letter-spacing:-0.5px; }}
.card {{ display:flex; flex-direction:column; background:linear-gradient(160deg, #FFFFFF 0%, var(--cream) 55%, #E6E0DA 100%);
  border-radius:28px; padding:22px 34px; color:var(--ink);
  box-shadow:0 4px 0 var(--cream-edge), 0 12px 0 var(--maroon), 0 16px 0 var(--maroon-dark), 0 34px 50px rgba(0,0,0,.5); }}
.chip {{ display:inline-flex; align-items:center; gap:12px; font-weight:900; font-size:34px; letter-spacing:.5px; padding:12px 26px;
  border-radius:999px; text-transform:uppercase; white-space:nowrap; }}
.pill {{ display:flex; align-items:center; gap:8px; padding:10px 20px; border-radius:999px; font-weight:900; font-size:32px; text-transform:uppercase; }}
.uline {{ height:10px; width:100%; background:var(--maroon); border-radius:8px; box-shadow:0 4px 0 var(--maroon-dark); margin:10px 0 14px; transform-origin:0 50%; }}
.strike {{ position:absolute; left:-10px; right:-10px; top:50%; background:var(--maroon); border-radius:12px; transform-origin:0 50%;
  rotate:-3deg; box-shadow:0 4px 0 var(--maroon-dark), 0 8px 14px rgba(0,0,0,.4); }}
.bars {{ display:flex; align-items:flex-end; gap:12px; height:124px; }}
.bar {{ width:34px; border-radius:8px; transform-origin:50% 100%; }}
.ball {{ width:128px; height:128px; border-radius:64px; display:flex; align-items:center; justify-content:center;
  background:radial-gradient(circle at 35% 30%, #C25A88, var(--maroon) 60%); border:4px solid var(--cream);
  box-shadow:0 10px 0 var(--maroon-dark), 0 24px 34px rgba(0,0,0,.45); }}
.panel {{ align-items:stretch; }}
.cap {{ left:{SAFE['left']}px; width:{SAFE_W}px; top:1170px; height:260px; display:flex; flex-wrap:wrap; justify-content:center;
  align-content:center; column-gap:34px; row-gap:4px; perspective:600px; }}
.w {{ display:inline-block; font-weight:900; font-size:78px; line-height:1.12; text-transform:uppercase; color:var(--cream); opacity:.6;
  -webkit-text-stroke:11px var(--ink); paint-order:stroke fill; border-radius:16px; text-shadow:{extrude(C['ink'], 7)}; }}
.w.key {{ color:var(--maroon-light); text-shadow:{extrude(C['maroon'], 7)}; }}
.w.done {{ opacity:1; }}
.w.on {{ opacity:1; color:var(--cream); -webkit-text-stroke:0 transparent; padding:0 16px; margin:0 -16px;
  background:linear-gradient(180deg, #B4537F 0%, var(--maroon) 60%); text-shadow:{extrude(C['maroonDark'], 5)};
  box-shadow:0 9px 0 var(--maroon-dark), 0 20px 28px rgba(0,0,0,.45); }}
"""

DOC = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>video 1 edited</title>
    <!-- Generated by scripts/build_hyperframes.py — edit that, not this file. -->
    <script src="assets/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920" data-fps="{FPS}">
      {chr(10).join('      ' + e for e in els).strip()}
      {chr(10).join('      ' + a for a in audio).strip()}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set(".p, .sp, .w, .cap", {{ transformPerspective: 1200 }});
      {(chr(10) + '      ').join(js)}
      tl.set({{}}, {{}}, {TOTAL:.3f});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
out = os.path.join(ROOT, "hyperframes", "index.html")
open(out, "w").write(DOC)
print(f"wrote {out}: {len(els)} visual clips, {len(audio)} audio clips, {len(js)} timeline calls, {TOTAL:.2f}s")
