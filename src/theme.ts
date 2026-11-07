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

export const C = {
  yellow: '#FFD84D',
  green: '#4CFF8F',
  red: '#FF4D5E',
  white: '#FFFFFF',
  ink: '#0E0F14',
  glass: 'rgba(14,15,20,0.82)',
};

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
