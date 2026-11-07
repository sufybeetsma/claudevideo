import React from 'react';
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import captions from '../data/captions.json';
import {C, extrude, FONT, SAFE, SAFE_W} from '../theme';

/** Word-by-word animated captions, kept inside the IG/TikTok safe zone (lower-middle of the frame). */
export const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const page = captions.pages.find((p) => frame >= p.start && frame < p.end);
  if (!page) return null;
  const enter = spring({frame: frame - page.start, fps, config: {damping: 14, stiffness: 220}});

  return (
    <div
      style={{
        position: 'absolute',
        left: SAFE.left,
        width: SAFE_W,
        top: 1170,
        height: 260,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        alignContent: 'center',
        columnGap: 34,
        rowGap: 4,
        transform: `scale(${0.85 + 0.15 * enter})`,
        opacity: enter,
      }}
    >
      {page.words.map((w) => {
        const active = frame >= w.start && frame < Math.max(w.end, w.start + 4);
        const spoken = frame >= w.start;
        const pop = active ? spring({frame: frame - w.start, fps, config: {damping: 10, stiffness: 300}}) : 0;
        const color = active ? C.cream : w.key ? C.maroonLight : C.cream;
        return (
          <span
            key={`${w.clip}-${w.i}`}
            style={{
              fontFamily: FONT,
              fontWeight: 900,
              fontSize: 78,
              lineHeight: 1.12,
              textTransform: 'uppercase',
              color,
              opacity: spoken ? 1 : 0.6,
              WebkitTextStroke: active ? '0px transparent' : `11px ${C.ink}`,
              paintOrder: 'stroke fill',
              // 3D extruded lettering
              textShadow: active ? extrude(C.maroonDark, 5) : extrude(w.key ? C.maroon : C.ink, 7),
              display: 'inline-block',
              padding: active ? '0 16px' : '0 0',
              margin: active ? '0 -16px' : 0,
              borderRadius: 16,
              background: active ? `linear-gradient(180deg, #B4537F 0%, ${C.maroon} 60%)` : 'transparent',
              boxShadow: active ? `0 9px 0 ${C.maroonDark}, 0 20px 28px rgba(0,0,0,0.45)` : 'none',
              transform: `perspective(600px) rotateX(${12 * (1 - pop)}deg) scale(${1 + 0.08 * pop}) translateY(${-6 * pop}px)`,
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};
