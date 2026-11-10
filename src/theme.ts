import captions from './data/captions.json';

/**
 * Safe zone for a 1080x1920 frame that works for BOTH Instagram Reels and TikTok:
 *  - top 220px: status bar / "Following | For You" tabs / Reels header
 *  - bottom 420px: username, caption, music ticker, nav bar
 *  - right 140px: like / comment / share / profile button rail
 *  - left 60px: breathing room
 * All text and graphics stay inside this rectangle.
 */
export const SAFE = {top: 220, bottom: 1500, left: 60, right: 940} as const;
export const SAFE_W = SAFE.right - SAFE.left; // 880
export const SAFE_CX = SAFE.left + SAFE_W / 2; // 500

/** Brand palette */
export const C = {
  maroon: '#963F66',
  maroonDark: '#5E2440',
  maroonLight: '#E3A3C1', // light tint of the maroon, for legible caption keywords on video
  cream: '#F3F0EC',
  creamEdge: '#CFC8C2',
  grey: '#60585D',
  ink: '#2B2528',
  glass: 'rgba(243,240,236,0.96)',
};

/** Stacked text-shadow that extrudes text into 3D. */
export const extrude = (color: string, depth = 6, shadow = true) =>
  [...Array(depth)].map((_, i) => `0 ${i + 1}px 0 ${color}`).join(', ') +
  (shadow ? `, 0 ${depth + 6}px ${depth * 2 + 8}px rgba(0,0,0,0.45)` : '');

export const FONT = "'Montserrat', 'Inter', sans-serif";

type Word = (typeof captions.words)[number];
const bare = (s: string) => s.toLowerCase().replace(/[^a-z0-9-]/g, '');

/** Frame at which `text` is spoken in A-roll clip `clip` (nth occurrence). */
export const at = (clip: number, text: string, nth = 0, edge: 'start' | 'end' = 'start'): number => {
  const hits = captions.words.filter((w: Word) => w.clip === clip && bare(w.text).startsWith(bare(text)));
  const w = hits[nth];
  if (!w) throw new Error(`word "${text}" (#${nth}) not found in clip ${clip}`);
  return w[edge];
};
