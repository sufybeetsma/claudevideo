import React from 'react';
import {AbsoluteFill} from 'remotion';
import {SAFE} from '../theme';

/** Debug overlay: shades the areas covered by Instagram Reels / TikTok UI. */
export const SafeZone: React.FC = () => {
  const shade = 'rgba(255,0,60,0.28)';
  const label: React.CSSProperties = {color: '#fff', font: '700 26px sans-serif', padding: 12};
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: SAFE.top, background: shade, ...label}}>TOP UI (tabs / header)</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: SAFE.bottom, bottom: 0, background: shade, ...label}}>
        BOTTOM UI (username, caption, audio, nav)
      </div>
      <div style={{position: 'absolute', left: SAFE.right, right: 0, top: SAFE.top, bottom: 1920 - SAFE.bottom, background: shade, ...label, writingMode: 'vertical-rl'}}>
        ACTION BUTTONS
      </div>
      <div style={{position: 'absolute', left: 0, width: SAFE.left, top: SAFE.top, bottom: 1920 - SAFE.bottom, background: 'rgba(255,200,0,0.25)'}} />
      <div
        style={{
          position: 'absolute',
          left: SAFE.left,
          top: SAFE.top,
          width: SAFE.right - SAFE.left,
          height: SAFE.bottom - SAFE.top,
          border: '4px dashed #00ff88',
        }}
      />
    </AbsoluteFill>
  );
};
