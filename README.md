# HDB upgrade reel — Remotion edit

A 63-second 1080×1920 30fps vertical edit for Instagram Reels and TikTok, built with Remotion.
The render is at `out/final.mp4`.

## Pipeline

1. **Transcribe**: OpenAI Whisper (`small`, word timestamps) over every A-roll clip. A `medium` pass was
   used to check unclear phrases. The raw output is in `scripts/transcript.raw.json`, and the corrected
   transcript is in `transcript.txt`.
2. **Edit decisions**: `scripts/edit.json` holds the clip order, trim points (dead air removed), punch-in
   zooms, B-roll picks over the voiceover (clip 9), and transcript corrections.
3. **Prep footage**: `scripts/prep.sh "<path to 'video 1' folder>"` trims and transcodes the clips into
   `public/clips/` (gitignored). It also high-passes, denoises and loudness-normalises the audio to -14 LUFS.
4. **Build data**: `python3 scripts/build_data.py` writes `src/data/timeline.json` and `src/data/captions.json`.
5. **SFX**: `python3 scripts/make_sfx.py` synthesises the whoosh, pop, ding, tick, boom, coin, buzz and
   riser sounds into `public/sfx/`, so there are no licensing issues.
6. **Render**:
   ```bash
   npm install
   npx remotion render src/index.ts Main out/final.mp4
   ```
   Use `npx remotion studio` to preview. Set `REMOTION_BROWSER=/path/to/chrome-headless-shell` to use a
   local browser.

## Safe zone (IG Reels + TikTok)

Defined in `src/theme.ts`. All captions and graphics stay inside x 60–940 and y 220–1500:
- **Top 220px**: status bar, tabs, Reels header.
- **Bottom 420px**: username, caption, audio and nav bar.
- **Right 140px**: like, comment, share and profile buttons.

Render the `SafeZonePreview` composition to see these areas shaded over the edit.

## Motion graphics

| Clip | Graphic |
|---|---|
| 1 | "Insider tip", then a **3 NUMBERS** hook card with a boom and a punch-in |
| 2 | Rising HDB equity bar chart |
| 3 | "What condo can they afford?", struck out as **WRONG QUESTION** |
| 4 | 3 CHECKS: 1, 2, 3 bubbles |
| 5–7 | Step tracker (Equity / Monthly / Exit) with a title card and keyword chips timed to speech |
| 8 | Numbers first, then properties |
| 9 | B-roll montage with animated checklists ("What we compared", then "The one we found") |
| 10 | HDB to condo, struck out, then "Make your equity WORK HARDER" |
| 11 | "Has your HDB done its job?" |
| 12 | Pulsing **DM me "HOME"** call to action |

Captions highlight each word as it's spoken (yellow), and keywords are shown in green.

## HyperFrames version

`hyperframes/` holds the same edit rebuilt with [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP → MP4).
It's generated from the same edit data as the Remotion version, so the cut, captions, brand colours, 3D graphics,
music and sound effects all match.

```bash
python3 scripts/build_hyperframes.py      # regenerate hyperframes/index.html from src/data/*.json
mkdir -p hyperframes/assets/clips && cp public/clips/*.mp4 hyperframes/assets/clips/   # after scripts/prep.sh
cd hyperframes
npx --yes hyperframes@0.9.29 check          # lint, runtime, layout and contrast checks
npx --yes hyperframes@0.9.29 render -o "renders/video 1 edited.mp4" --quality delivery
```

Edit `scripts/build_hyperframes.py`, not the generated `index.html`.
