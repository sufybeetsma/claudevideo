import React from 'react';
import {AbsoluteFill, interpolate, OffthreadVideo, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import timeline from './data/timeline.json';
import {Captions} from './components/Captions';
import {Graphics} from './components/Graphics';
import {SafeZone} from './components/SafeZone';
import {Sfx} from './components/Sfx';
import {at} from './theme';

/** Extra punch-in zooms (absolute frame -> added scale) on emphasis words. */
const PUNCHES: {frame: number; amount: number}[] = [
  {frame: at(1, 'three'), amount: 0.12},
  {frame: at(5, 'usable'), amount: 0.08},
  {frame: at(7, 'worthwhile'), amount: 0.1},
  {frame: at(10, 'equity'), amount: 0.1},
  {frame: at(12, 'dm'), amount: 0.08},
];

const ARoll: React.FC<{src: string; from: number; dur: number; zoom: number}> = ({src, from, dur, zoom}) => {
  const frame = useCurrentFrame(); // local to the Sequence
  const {fps} = useVideoConfig();
  const abs = frame + from;
  let scale = zoom + 0.04 * (frame / dur); // slow push-in
  for (const p of PUNCHES) {
    if (p.frame >= from && p.frame < from + dur && abs >= p.frame) {
      scale += p.amount * spring({frame: abs - p.frame, fps, config: {damping: 16, stiffness: 200}});
    }
  }
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <OffthreadVideo
        src={staticFile(src)}
        style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${scale})`, transformOrigin: '50% 32%'}}
      />
    </AbsoluteFill>
  );
};

const BRoll: React.FC<{src: string; dur: number}> = ({src, dur}) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, dur], [1.04, 1.12]);
  const flash = interpolate(frame, [0, 5], [0.7, 0], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <OffthreadVideo muted src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${scale})`}} />
      {/* subtle darkening so the checklist panel reads well */}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.25) 100%)'}} />
      <AbsoluteFill style={{background: '#fff', opacity: flash}} />
    </AbsoluteFill>
  );
};

/** Hard-cut flash between A-roll clips. */
const CutFlash: React.FC = () => {
  const frame = useCurrentFrame();
  return <AbsoluteFill style={{background: '#fff', opacity: interpolate(frame, [0, 3], [0.18, 0], {extrapolateRight: 'clamp'})}} />;
};

export const Main: React.FC<{showSafeZone: boolean}> = ({showSafeZone}) => (
  <AbsoluteFill style={{background: '#000'}}>
    {timeline.aroll.map((c) => (
      <Sequence key={c.id} from={c.from} durationInFrames={c.dur} name={`A-roll ${c.id}`}>
        <ARoll src={c.src} from={c.from} dur={c.dur} zoom={c.zoom} />
        {c.from > 0 && !c.voiceover ? <CutFlash /> : null}
      </Sequence>
    ))}
    {timeline.broll.map((b) => (
      <Sequence key={b.src} from={b.from} durationInFrames={b.dur} name={`B-roll ${b.src}`}>
        <BRoll src={b.src} dur={b.dur} />
      </Sequence>
    ))}
    <Graphics />
    <Captions />
    <Sfx />
    {showSafeZone ? <SafeZone /> : null}
  </AbsoluteFill>
);
