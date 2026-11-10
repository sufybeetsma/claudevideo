import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import timeline from '../data/timeline.json';
import {at, C, extrude, FONT, SAFE, SAFE_CX, SAFE_W} from '../theme';
import {Arrow, Card, Check, Chip, Cross, DrawLine, Pop} from './primitives';

const clip = (id: number) => {
  const c = timeline.aroll.find((x) => x.id === id)!;
  return {start: c.from, end: c.from + c.dur};
};

/** Every graphic lives in this top band of the safe zone (above faces), except the B-roll panel. */
const TOP = SAFE.top + 20;
const band: React.CSSProperties = {
  position: 'absolute',
  left: SAFE.left,
  width: SAFE_W,
  top: TOP,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  gap: 16,
};
const H = (size: number, color: string = C.ink, depth = 0): React.CSSProperties => ({
  fontFamily: FONT,
  textShadow: depth ? extrude(color === C.cream ? C.maroonDark : color === C.maroon ? C.maroonDark : C.creamEdge, depth, false) : undefined,
  fontWeight: 900,
  fontSize: size,
  lineHeight: 1.02,
  color,
  textTransform: 'uppercase',
  textAlign: 'center',
  letterSpacing: -0.5,
});

// ---------- timings (all derived from the transcript) ----------
export const T = {
  c1: clip(1), c2: clip(2), c3: clip(3), c4: clip(4), c5: clip(5), c6: clip(6), c7: clip(7), c8: clip(8),
  c9: clip(9), c10: clip(10), c11: clip(11), c12: clip(12),
  hook: at(1, 'three'),
  hdb: at(2, 'hdb'),
  equity2: at(2, 'equity'),
  condo3: at(3, 'condo'),
  afford: at(3, 'afford', 0, 'end'),
  three4: at(4, 'three'),
  loan: at(5, 'loan'), cpf: at(5, 'cpf'), selling: at(5, 'selling'),
  monthly: at(6, 'monthly'), buffer: at(6, 'buffer'),
  exit7: at(7, 'exit'), worth: at(7, 'worthwhile'),
  numbers8: at(8, 'numbers'), props8: at(8, 'properties'),
  entry: at(9, 'entry'), surrounding: at(9, 'surrounding'), unit: at(9, 'unit-specific'), future: at(9, 'future'),
  eventually: at(9, 'eventually'), entry2: at(9, 'entry', 1), growth: at(9, 'growth'), financing: at(9, 'financing'),
  hdb10: at(10, 'hdb'), condo10: at(10, 'condo', 0, 'end'), its10: at(10, "it's"), equity10: at(10, 'equity'), harder: at(10, 'harder'),
  hdb11: at(11, 'hdb'),
  dm: at(12, 'dm'), send: at(12, 'send'),
};

// ---------- sound design ----------
export const SFX: {frame: number; file: string; volume: number}[] = [
  {frame: T.c1.start + 2, file: 'whoosh', volume: 0.35},
  {frame: T.hook, file: 'boom', volume: 0.55},
  {frame: T.hdb, file: 'whoosh', volume: 0.35},
  {frame: T.equity2, file: 'coin', volume: 0.35},
  {frame: T.condo3 - 2, file: 'whoosh', volume: 0.35},
  {frame: T.afford, file: 'buzz', volume: 0.22},
  {frame: T.three4, file: 'pop', volume: 0.5},
  {frame: T.three4 + 5, file: 'pop', volume: 0.5},
  {frame: T.three4 + 10, file: 'pop', volume: 0.5},
  {frame: T.c5.start, file: 'whoosh', volume: 0.4},
  {frame: T.loan, file: 'pop', volume: 0.45},
  {frame: T.cpf, file: 'pop', volume: 0.45},
  {frame: T.selling, file: 'pop', volume: 0.45},
  {frame: T.c6.start, file: 'whoosh', volume: 0.4},
  {frame: T.monthly, file: 'pop', volume: 0.45},
  {frame: T.buffer, file: 'coin', volume: 0.35},
  {frame: T.c7.start, file: 'whoosh', volume: 0.4},
  {frame: T.exit7, file: 'pop', volume: 0.45},
  {frame: T.worth, file: 'boom', volume: 0.35},
  {frame: T.numbers8, file: 'ding', volume: 0.35},
  {frame: T.props8, file: 'pop', volume: 0.45},
  ...timeline.broll.map((b) => ({frame: b.from, file: 'whoosh', volume: 0.35})),
  {frame: T.entry, file: 'tick', volume: 0.6},
  {frame: T.surrounding, file: 'tick', volume: 0.6},
  {frame: T.unit, file: 'tick', volume: 0.6},
  {frame: T.future, file: 'tick', volume: 0.6},
  {frame: T.entry2, file: 'ding', volume: 0.3},
  {frame: T.growth, file: 'ding', volume: 0.3},
  {frame: T.financing, file: 'ding', volume: 0.3},
  {frame: T.hdb10, file: 'whoosh', volume: 0.35},
  {frame: T.condo10, file: 'buzz', volume: 0.18},
  {frame: T.equity10, file: 'coin', volume: 0.35},
  {frame: T.hdb11, file: 'whoosh', volume: 0.35},
  {frame: T.dm - 26, file: 'riser', volume: 0.35},
  {frame: T.dm, file: 'ding', volume: 0.45},
  {frame: T.send, file: 'pop', volume: 0.45},
];

// ---------- scenes ----------
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const u = interpolate(frame, [T.hook + 6, T.hook + 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      <Pop from={T.c1.start + 2} to={T.hook} style={band}>
        <Chip>Insider tip</Chip>
      </Pop>
      <Pop from={T.hook} to={T.c1.end} style={band}>
        <Card style={{display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '26px 40px'}}>
          <div style={H(124, C.maroon, 7)}>3 numbers</div>
          <div style={{height: 10, width: `${u * 100}%`, background: C.maroon, borderRadius: 8, boxShadow: `0 4px 0 ${C.maroonDark}`, margin: '10px 0 14px'}} />
          <div style={H(46, C.grey)}>I check before my clients upgrade</div>
        </Card>
      </Pop>
    </>
  );
};

const EquityBars: React.FC<{from: number}> = ({from}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const hs = [40, 62, 88, 120];
  return (
    <div style={{display: 'flex', alignItems: 'flex-end', gap: 12, height: 124}}>
      {hs.map((h, i) => {
        const s = spring({frame: frame - from - 4 - i * 4, fps, config: {damping: 12}});
        return <div key={i} style={{width: 34, height: h * s, borderRadius: 8, background: i === 3 ? C.maroon : C.grey, boxShadow: `6px 0 0 ${i === 3 ? C.maroonDark : '#3E383B'}`}} />;
      })}
    </div>
  );
};

const HdbEquity: React.FC = () => (
  <Pop from={T.hdb} to={T.c2.end} style={band}>
    <Card style={{display: 'flex', alignItems: 'center', gap: 30}}>
      <EquityBars from={T.hdb} />
      <div>
        <div style={{...H(40, C.grey), textAlign: 'left'}}>HDB</div>
        <div style={{...H(72, C.maroon, 5), textAlign: 'left'}}>Equity</div>
        <div style={{...H(34, C.grey), textAlign: 'left'}}>already built up</div>
      </div>
    </Card>
  </Pop>
);

const WrongQuestion: React.FC = () => (
  <Pop from={T.condo3 - 2} to={T.c3.end} style={band}>
    <Card style={{position: 'relative'}}>
      <div style={{position: 'relative'}}>
        <div style={H(58)}>“What condo can they afford?”</div>
        <DrawLine from={T.afford - 4} />
      </div>
    </Card>
    <Pop from={T.afford} to={T.c3.end} dir="none">
      <Chip>
        <Cross size={36} /> Wrong question
      </Chip>
    </Pop>
  </Pop>
);

const ThreeChecks: React.FC = () => (
  <Pop from={T.three4 - 4} to={T.c4.end} style={band}>
    <div style={H(96, C.cream, 7)}>3 checks</div>
    <div style={{display: 'flex', gap: 30}}>
      {[1, 2, 3].map((n, i) => (
        <Pop key={n} from={T.three4 + i * 5} to={T.c4.end} dir="none">
          <div
            style={{
              ...H(76, C.cream, 4),
              width: 128,
              height: 128,
              borderRadius: 64,
              background: `radial-gradient(circle at 35% 30%, #C25A88, ${C.maroon} 60%)`,
              border: `4px solid ${C.cream}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: `0 10px 0 ${C.maroonDark}, 0 24px 34px rgba(0,0,0,0.45)`,
            }}
          >
            {n}
          </div>
        </Pop>
      ))}
    </div>
  </Pop>
);

const STEPS = ['Equity', 'Monthly', 'Exit'];
const Tracker: React.FC<{active: number}> = ({active}) => (
  <div style={{display: 'flex', gap: 14}}>
    {STEPS.map((s, i) => (
      <div
        key={s}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '10px 20px',
          borderRadius: 999,
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: 32,
          textTransform: 'uppercase',
          background: i === active ? C.maroon : C.cream,
          color: i === active ? C.cream : i < active ? C.maroon : C.grey,
          boxShadow: `0 6px 0 ${i === active ? C.maroonDark : C.creamEdge}, 0 14px 22px rgba(0,0,0,0.35)`,
        }}
      >
        {i < active ? <Check size={28} /> : <span>{i + 1}</span>}
        {s}
      </div>
    ))}
  </div>
);

const Step: React.FC<{
  n: number;
  title: string;
  range: {start: number; end: number};
  chips: {from: number; label: string; color: string; text?: string}[];
}> = ({n, title, range, chips}) => (
  <div style={band}>
    <Tracker active={n - 1} />
    <Pop from={range.start} to={range.end} dir="left">
      <Card style={{display: 'flex', alignItems: 'center', gap: 22, padding: '16px 32px'}}>
        <div style={H(78, C.maroon, 5)}>0{n}</div>
        <div style={H(54)}>{title}</div>
      </Card>
    </Pop>
    <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 12}}>
      {chips.map((c) => (
        <Pop key={c.label} from={c.from} to={range.end}>
          <Chip color={c.color} textColor={c.text ?? C.cream}>
            {c.label}
          </Chip>
        </Pop>
      ))}
    </div>
  </div>
);

const Checks: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame < T.c5.start || frame >= T.c7.end) return null;
  if (frame < T.c5.end)
    return (
      <Step
        n={1}
        title="Usable equity"
        range={T.c5}
        chips={[
          {from: T.loan, label: '– Loan', color: C.grey},
          {from: T.cpf, label: '– CPF refund', color: C.grey},
          {from: T.selling, label: '– Selling costs', color: C.grey},
        ]}
      />
    );
  if (frame < T.c6.end)
    return (
      <Step
        n={2}
        title="Monthly comfort"
        range={T.c6}
        chips={[
          {from: T.monthly, label: 'Sustainable commitment', color: C.grey},
          {from: T.buffer, label: '+ Healthy buffer', color: C.maroon},
        ]}
      />
    );
  return (
    <Step
      n={3}
      title="Exit potential"
      range={T.c7}
      chips={[
        {from: T.exit7, label: 'Value at exit', color: C.grey},
        {from: T.worth, label: 'Worth the move?', color: C.maroon},
      ]}
    />
  );
};

const NumbersFirst: React.FC = () => (
  <Pop from={T.numbers8} to={T.c8.end} style={band}>
    <Card style={{display: 'flex', flexDirection: 'column', gap: 14}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
        <Check size={60} />
        <div style={H(60, C.maroon, 5)}>Numbers first</div>
      </div>
      <Pop from={T.props8} to={T.c8.end} dir="left">
        <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
          <Arrow size={60} />
          <div style={H(60, C.grey, 4)}>Then properties</div>
        </div>
      </Pop>
    </Card>
  </Pop>
);

const Row: React.FC<{from: number; label: string; tick: number}> = ({from, label, tick}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [tick, tick + 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <Pop from={from} to={T.c9.end} dir="left">
      <div style={{display: 'flex', alignItems: 'center', gap: 20, padding: '8px 0'}}>
        <Check size={50} progress={p} color={p > 0 ? C.maroon : C.creamEdge} />
        <div style={{...H(44, C.ink), textAlign: 'left'}}>{label}</div>
      </div>
    </Pop>
  );
};

const Panel: React.FC<{title: string; titleColor: string; from: number; to: number; rows: {label: string; at: number}[]}> = ({
  title,
  titleColor,
  from,
  to,
  rows,
}) => (
  <Pop from={from} to={to} style={{position: 'absolute', left: SAFE.left + 30, width: SAFE_W - 60, top: TOP + 60}}>
    <Card style={{padding: '30px 38px'}}>
      <div style={{...H(56, titleColor, 5), textAlign: 'left', marginBottom: 12}}>{title}</div>
      {rows.map((r) => (
        <Row key={r.label} from={r.at - 3} tick={r.at} label={r.label} />
      ))}
    </Card>
  </Pop>
);

const Compared: React.FC = () => (
  <>
    <Panel
      title="What we compared"
      titleColor={C.maroon}
      from={T.c9.start}
      to={T.eventually}
      rows={[
        {label: 'Entry prices', at: T.entry},
        {label: 'Surrounding transactions', at: T.surrounding},
        {label: 'Unit-specific factors', at: T.unit},
        {label: 'Future exit potential', at: T.future},
      ]}
    />
    <Panel
      title="The one we found"
      titleColor={C.maroon}
      from={T.eventually}
      to={T.c9.end}
      rows={[
        {label: 'Entry made sense', at: T.entry2},
        {label: 'Clear growth drivers', at: T.growth},
        {label: 'Comfortable financing', at: T.financing},
      ]}
    />
  </>
);

const NotJustCondo: React.FC = () => (
  <>
    <Pop from={T.hdb10} to={T.its10} style={band}>
      <Card style={{display: 'flex', alignItems: 'center', gap: 26, position: 'relative'}}>
        <div style={H(76, C.grey, 5)}>HDB</div>
        <Arrow size={70} />
        <div style={H(76, C.grey, 5)}>Condo</div>
        <DrawLine from={T.condo10 - 2} thickness={12} />
      </Card>
    </Pop>
    <Pop from={T.equity10 - 4} to={T.c10.end} style={band}>
      <Card style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
        <div style={H(46, C.grey)}>Make your</div>
        <div style={H(92, C.maroon, 7)}>Equity</div>
        <Pop from={T.harder - 2} to={T.c10.end} dir="none">
          <div style={{...H(64, C.cream, 3), background: C.maroon, padding: '6px 24px', borderRadius: 14, boxShadow: `0 8px 0 ${C.maroonDark}, 0 18px 26px rgba(0,0,0,0.4)`}}>Work harder</div>
        </Pop>
      </Card>
    </Pop>
  </>
);

const DoneItsJob: React.FC = () => {
  const frame = useCurrentFrame();
  const bob = Math.sin((frame - T.hdb11) / 5) * 6;
  return (
    <Pop from={T.hdb11 - 2} to={T.c11.end} style={band}>
      <Card style={{display: 'flex', alignItems: 'center', gap: 24}}>
        <div style={{...H(140, C.maroon, 8), transform: `translateY(${bob}px) rotate(${bob}deg)`}}>?</div>
        <div>
          <div style={{...H(44, C.grey), textAlign: 'left'}}>Has your HDB</div>
          <div style={{...H(64, C.maroon, 5), textAlign: 'left'}}>done its job?</div>
        </div>
      </Card>
    </Pop>
  );
};

const CTA: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = 1 + 0.045 * Math.sin((frame - T.dm) / 4);
  return (
    <Pop from={T.dm} to={T.c12.end + 1} style={band}>
      <div
        style={{
          ...H(84, C.cream, 5),
          background: `linear-gradient(180deg, #B4537F 0%, ${C.maroon} 55%)`,
          padding: '24px 48px',
          borderRadius: 999,
          transform: `scale(${pulse}) rotateX(${8 * Math.sin((frame - T.dm) / 9)}deg)`,
          boxShadow: `0 12px 0 ${C.maroonDark}, 0 0 0 10px rgba(243,240,236,0.35), 0 34px 50px rgba(0,0,0,0.5)`,
        }}
      >
        DM me “HOME”
      </div>
      <Pop from={T.send} to={T.c12.end + 1}>
        <Card style={{padding: '14px 30px'}}>
          <div style={H(38, C.maroon)}>Get my exact 3-number checklist</div>
        </Card>
      </Pop>
    </Pop>
  );
};

export const Graphics: React.FC = () => (
  <AbsoluteFill>
    <Hook />
    <HdbEquity />
    <WrongQuestion />
    <ThreeChecks />
    <Checks />
    <NumbersFirst />
    <Compared />
    <NotJustCondo />
    <DoneItsJob />
    <CTA />
  </AbsoluteFill>
);

export {SAFE_CX};
