import React from 'react';
import {Composition} from 'remotion';
import {Main} from './Main';
import timeline from './data/timeline.json';
import './fonts';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="Main"
      component={Main}
      durationInFrames={timeline.total}
      fps={timeline.fps}
      width={1080}
      height={1920}
      defaultProps={{showSafeZone: false}}
    />
    {/* Same edit with the Instagram/TikTok UI safe-zone overlay drawn on top, for checking layout */}
    <Composition
      id="SafeZonePreview"
      component={Main}
      durationInFrames={timeline.total}
      fps={timeline.fps}
      width={1080}
      height={1920}
      defaultProps={{showSafeZone: true}}
    />
  </>
);
