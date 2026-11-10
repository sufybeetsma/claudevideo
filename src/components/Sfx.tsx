import React from 'react';
import {Audio, Sequence, staticFile} from 'remotion';
import {SFX} from './Graphics';

export const Sfx: React.FC = () => (
  <>
    {SFX.map((s, i) => (
      <Sequence key={i} from={Math.max(0, s.frame)} durationInFrames={60} name={`sfx ${s.file}`}>
        <Audio src={staticFile(`sfx/${s.file}.wav`)} volume={s.volume} />
      </Sequence>
    ))}
  </>
);
