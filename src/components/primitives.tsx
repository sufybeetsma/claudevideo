import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, FONT} from '../theme';

/**
 * Springs children in at `from` with a 3D flip (perspective rotateX/rotateY), keeps a gentle
 * 3D "float" while on screen, and flips/fades out at `to` (absolute frames).
 */
export const Pop: React.FC<{
  from: number;
  to: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
  dir?: 'up' | 'down' | 'left' | 'none';
  float?: boolean;
}> = ({from, to, children, style, dir = 'up', float = true}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (frame < from || frame >= to) return null;
  const s = spring({frame: frame - from, fps, config: {damping: 12, stiffness: 150, mass: 0.8}});
  const out = interpolate(frame, [to - 7, to], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const inv = 1 - s;
  const rx = dir === 'up' ? 75 * inv : dir === 'down' ? -75 * inv : 25 * inv;
  const ry = dir === 'left' ? -80 * inv : dir === 'none' ? 35 * inv : 0;
  const lf = frame - from;
  const fx = float ? Math.sin(lf / 22) * 4 : 0;
  const fy = float ? Math.cos(lf / 27) * 6 : 0;
  const tz = -200 * inv - 250 * out;
  return (
    <div style={{...style, perspective: 1200}}>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: (style?.gap as number) ?? 0,
          opacity: Math.min(1, s * 1.6) * (1 - out),
          transformStyle: 'preserve-3d',
          transform: `translateZ(${tz}px) rotateX(${rx + fx - out * 50}deg) rotateY(${ry + fy}deg) scale(${0.75 + 0.25 * s})`,
        }}
      >
        {children}
      </div>
    </div>
  );
};

/** Cream card with a maroon "slab" edge underneath so it reads as a 3D tile. */
export const Card: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <div
    style={{
      background: `linear-gradient(160deg, #FFFFFF 0%, ${C.cream} 55%, #E6E0DA 100%)`,
      borderRadius: 28,
      padding: '22px 34px',
      boxShadow: `0 4px 0 ${C.creamEdge}, 0 12px 0 ${C.maroon}, 0 16px 0 ${C.maroonDark}, 0 34px 50px rgba(0,0,0,0.5)`,
      fontFamily: FONT,
      color: C.ink,
      ...style,
    }}
  >
    {children}
  </div>
);

/** Pill "button" with a darker bottom edge (3D keycap look). */
export const Chip: React.FC<{children: React.ReactNode; color?: string; textColor?: string; edge?: string; style?: React.CSSProperties}> = ({
  children,
  color = C.maroon,
  textColor = C.cream,
  edge,
  style,
}) => (
  <div
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 12,
      background: `linear-gradient(180deg, rgba(255,255,255,0.18), rgba(255,255,255,0) 60%), ${color}`,
      color: textColor,
      fontFamily: FONT,
      fontWeight: 900,
      fontSize: 34,
      letterSpacing: 0.5,
      padding: '12px 26px',
      borderRadius: 999,
      boxShadow: `0 7px 0 ${edge ?? (color === C.maroon ? C.maroonDark : '#3E383B')}, 0 18px 30px rgba(0,0,0,0.4)`,
      textTransform: 'uppercase',
      whiteSpace: 'nowrap',
      ...style,
    }}
  >
    {children}
  </div>
);

export const Check: React.FC<{size?: number; color?: string; progress?: number}> = ({size = 40, color = C.maroon, progress = 1}) => (
  <svg width={size} height={size * 1.1} viewBox="0 0 40 44" style={{overflow: 'visible'}}>
    <circle cx="20" cy="24" r="19" fill={C.maroonDark} />
    <circle cx="20" cy="20" r="19" fill={color} />
    <path
      d="M11 21 L18 28 L30 13"
      fill="none"
      stroke={C.cream}
      strokeWidth="5"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeDasharray="30"
      strokeDashoffset={30 * (1 - progress)}
    />
  </svg>
);

export const Cross: React.FC<{size?: number}> = ({size = 40}) => (
  <svg width={size} height={size} viewBox="0 0 40 40">
    <circle cx="20" cy="20" r="19" fill={C.cream} />
    <path d="M13 13 L27 27 M27 13 L13 27" stroke={C.maroon} strokeWidth="5" strokeLinecap="round" />
  </svg>
);

export const Arrow: React.FC<{size?: number; color?: string}> = ({size = 60, color = C.maroon}) => (
  <svg width={size} height={size * 0.7} viewBox="0 0 60 42" style={{overflow: 'visible'}}>
    <path d="M4 22 H48 M34 8 L52 22 L34 36" fill="none" stroke={C.maroonDark} strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M4 18 H48 M34 4 L52 18 L34 32" fill="none" stroke={color} strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

/** A line that draws across its parent (for strike-throughs / underlines). */
export const DrawLine: React.FC<{from: number; color?: string; top?: string | number; thickness?: number; dur?: number}> = ({
  from,
  color = C.maroon,
  top = '50%',
  thickness = 10,
  dur = 8,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [from, from + dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div
      style={{
        position: 'absolute',
        left: -10,
        top,
        height: thickness,
        width: `calc(${p * 100}% + ${p * 20}px)`,
        background: color,
        borderRadius: thickness,
        transform: 'rotate(-3deg)',
        boxShadow: `0 4px 0 ${C.maroonDark}, 0 8px 14px rgba(0,0,0,0.4)`,
      }}
    />
  );
};
