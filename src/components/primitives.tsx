import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, FONT} from '../theme';

/** Springs children in at `from` and fades/scales them out at `to` (absolute frames). */
export const Pop: React.FC<{
  from: number;
  to: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
  dir?: 'up' | 'down' | 'left' | 'none';
}> = ({from, to, children, style, dir = 'up'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (frame < from || frame >= to) return null;
  const s = spring({frame: frame - from, fps, config: {damping: 13, stiffness: 180, mass: 0.7}});
  const out = interpolate(frame, [to - 6, to], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const off = (1 - s) * 60;
  const tr = dir === 'up' ? `translateY(${off}px)` : dir === 'down' ? `translateY(${-off}px)` : dir === 'left' ? `translateX(${-off * 2}px)` : '';
  return (
    <div style={{...style, opacity: Math.min(1, s * 1.5) * out, transform: `${tr} scale(${0.7 + 0.3 * s - (1 - out) * 0.1})`}}>
      {children}
    </div>
  );
};

export const Card: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <div
    style={{
      background: C.glass,
      borderRadius: 28,
      padding: '22px 34px',
      boxShadow: '0 18px 50px rgba(0,0,0,0.45)',
      border: '2px solid rgba(255,255,255,0.10)',
      fontFamily: FONT,
      color: C.white,
      ...style,
    }}
  >
    {children}
  </div>
);

export const Chip: React.FC<{children: React.ReactNode; color?: string; textColor?: string; style?: React.CSSProperties}> = ({
  children,
  color = C.white,
  textColor = C.ink,
  style,
}) => (
  <div
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 12,
      background: color,
      color: textColor,
      fontFamily: FONT,
      fontWeight: 900,
      fontSize: 34,
      letterSpacing: 0.5,
      padding: '12px 24px',
      borderRadius: 999,
      boxShadow: '0 10px 30px rgba(0,0,0,0.35)',
      textTransform: 'uppercase',
      whiteSpace: 'nowrap',
      ...style,
    }}
  >
    {children}
  </div>
);

export const Check: React.FC<{size?: number; color?: string; progress?: number}> = ({size = 40, color = C.green, progress = 1}) => (
  <svg width={size} height={size} viewBox="0 0 40 40">
    <circle cx="20" cy="20" r="19" fill={color} />
    <path
      d="M11 21 L18 28 L30 13"
      fill="none"
      stroke={C.ink}
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
    <circle cx="20" cy="20" r="19" fill={C.red} />
    <path d="M13 13 L27 27 M27 13 L13 27" stroke={C.white} strokeWidth="5" strokeLinecap="round" />
  </svg>
);

export const Arrow: React.FC<{size?: number; color?: string}> = ({size = 60, color = C.yellow}) => (
  <svg width={size} height={size * 0.6} viewBox="0 0 60 36">
    <path d="M4 18 H48 M34 4 L52 18 L34 32" fill="none" stroke={color} strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

/** A line that draws across its parent (for strike-throughs / underlines). */
export const DrawLine: React.FC<{from: number; color?: string; top?: string | number; thickness?: number; dur?: number}> = ({
  from,
  color = C.red,
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
        boxShadow: '0 4px 14px rgba(0,0,0,0.4)',
      }}
    />
  );
};
