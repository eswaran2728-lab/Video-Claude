import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {C, CAP, CARD, FONT, M, PANEL} from './theme';
import {
  FPS, SECTIONS, SlideT, alertAt, chipsOf, chunksOf, framesOf, sectionOf, starts, timeline, ChipT,
} from './meta';

const pad = (n: number) => String(n).padStart(2, '0');
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/* ---------------- background ---------------- */
const Background: React.FC = () => {
  const f = useCurrentFrame();
  const blobs = [
    {x: 220, y: 200, r: 360, c: 'rgba(228,0,43,0.16)', s: 0.004},
    {x: 1500, y: 800, r: 420, c: 'rgba(77,163,255,0.13)', s: 0.003},
    {x: 900, y: 1000, r: 300, c: 'rgba(124,92,255,0.12)', s: 0.005},
  ];
  return (
    <AbsoluteFill style={{background: `linear-gradient(135deg, ${C.bg1}, ${C.bg2})`}}>
      <AbsoluteFill
        style={{
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)',
          backgroundSize: '60px 60px',
          backgroundPosition: `${(f * 0.35) % 60}px ${(f * 0.2) % 60}px`,
        }}
      />
      {blobs.map((b, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: b.x + Math.sin(f * b.s + i) * 120 - b.r,
            top: b.y + Math.cos(f * b.s * 1.3 + i) * 80 - b.r,
            width: b.r * 2, height: b.r * 2, borderRadius: '50%',
            background: `radial-gradient(circle, ${b.c}, transparent 70%)`,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

/* ---------------- header + journey (global) ---------------- */
const Plane: React.FC<{size?: number}> = ({size = 26}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill={C.text}>
    <path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" />
  </svg>
);

const Chrome: React.FC<{cur: SlideT; local: number}> = ({cur, local}) => {
  const sec = sectionOf(cur.n);
  return (
    <>
      {/* header */}
      <div style={{position: 'absolute', left: M, top: 16, right: M, height: 52, display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontFamily: FONT}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 14}}>
          <div style={{width: 44, height: 44, borderRadius: 12, background: C.red, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 24px rgba(228,0,43,0.5)'}}>
            <div style={{transform: `rotate(${Math.sin(local / 40) * 6 + 45}deg)`}}><Plane /></div>
          </div>
          <div>
            <div style={{color: C.text, fontSize: 22, fontWeight: 800, letterSpacing: 2}}>AVSEC STAFF TRAINING</div>
            <div style={{color: C.dim, fontSize: 15, fontWeight: 500}}>AA/SEC/F/042 · High-Lift Escort eForm</div>
          </div>
        </div>
        <div style={{color: C.dim, fontSize: 18, fontWeight: 600, letterSpacing: 1}}>
          SLIDE <span style={{color: C.text}}>{pad(cur.n)}</span> / 39
        </div>
      </div>
      {/* panel frame */}
      <div style={{position: 'absolute', left: PANEL.x, top: PANEL.y, width: PANEL.w, height: PANEL.h, borderRadius: 22, background: C.panel, border: `1px solid ${C.line}`, backdropFilter: 'blur(6px)'}} />
      {/* journey */}
      <div style={{position: 'absolute', left: PANEL.x + 22, top: PANEL.y + 18, width: PANEL.w - 44, fontFamily: FONT}}>
        <div style={{color: C.dim, fontSize: 14, fontWeight: 700, letterSpacing: 3, marginBottom: 8}}>YOUR JOURNEY</div>
        {SECTIONS.map((s, i) => {
          const done = i < sec, now = i === sec;
          const frac = now ? (cur.n - s.from + 1) / (s.to - s.from + 1) : done ? 1 : 0;
          return (
            <div key={s.name} style={{height: 40, display: 'flex', alignItems: 'center', gap: 12, padding: '0 10px', borderRadius: 10, background: now ? 'rgba(228,0,43,0.18)' : 'transparent', position: 'relative'}}>
              <div style={{width: 22, height: 22, borderRadius: 11, flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: done ? C.green : now ? C.red : 'rgba(255,255,255,0.12)', color: '#fff', fontSize: 13, fontWeight: 800,
                boxShadow: now ? `0 0 ${10 + Math.sin(local / 5) * 6}px ${C.red}` : 'none'}}>
                {done ? '✓' : i + 1}
              </div>
              <div style={{color: now ? C.text : done ? '#c7cde8' : C.dim, fontSize: 19, fontWeight: now ? 800 : 600}}>{s.name}</div>
              <div style={{position: 'absolute', left: 10, right: 10, bottom: 2, height: 3, borderRadius: 2, background: now ? 'rgba(255,255,255,0.12)' : 'transparent'}}>
                <div style={{width: `${frac * 100}%`, height: '100%', borderRadius: 2, background: C.red}} />
              </div>
            </div>
          );
        })}
      </div>
    </>
  );
};

/* ---------------- side-panel callouts ---------------- */
const KIND: Record<ChipT['kind'], {c: string; icon: string}> = {
  yes: {c: C.green, icon: '✓'}, no: {c: C.redSoft, icon: '✕'}, tap: {c: C.blue, icon: '☝'},
  sample: {c: C.amber, icon: '✎'}, info: {c: C.blue, icon: 'i'}, warn: {c: C.amber, icon: '!'}, req: {c: C.redSoft, icon: '*'},
};

const Chip: React.FC<{chip: ChipT; t: number}> = ({chip, t}) => {
  const frame = useCurrentFrame();
  const p = spring({frame: frame - Math.round(chip.at * FPS), fps: FPS, config: {damping: 13, stiffness: 140}});
  const k = KIND[chip.kind];
  const glow = interpolate(frame - Math.round(chip.at * FPS), [0, 10, 40], [1, 1, 0], clamp);
  return (
    <div style={{
      transform: `translateX(${(1 - p) * 90}px) scale(${0.85 + 0.15 * p})`, opacity: Math.min(1, p * 1.5),
      display: 'flex', alignItems: 'center', gap: 14, padding: '12px 14px', borderRadius: 16, marginTop: 10,
      background: 'rgba(10,14,29,0.75)', border: `2px solid ${k.c}`, boxShadow: `0 0 ${28 * glow}px ${k.c}66`,
    }}>
      <div style={{width: 40, height: 40, borderRadius: 12, background: k.c, color: '#0a0e1d', fontSize: 24, fontWeight: 900, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>{k.icon}</div>
      <div style={{minWidth: 0}}>
        <div style={{fontSize: chip.kind === 'sample' ? 15 : 21, fontWeight: 800, lineHeight: 1.15, color: chip.kind === 'sample' ? k.c : C.text}}>{chip.label}</div>
        {chip.sub && <div style={{color: chip.kind === 'sample' ? C.text : C.dim, fontSize: chip.kind === 'sample' ? 24 : 15, fontWeight: chip.kind === 'sample' ? 800 : 500, marginTop: 2, wordBreak: 'break-word'}}>{chip.sub}</div>}
      </div>
    </div>
  );
};

const AlertBox: React.FC<{at: number}> = ({at}) => {
  const frame = useCurrentFrame();
  const p = spring({frame: frame - Math.round(at * FPS), fps: FPS, config: {damping: 12, stiffness: 120}});
  const pulse = 0.5 + 0.5 * Math.sin(frame / 6);
  return (
    <div style={{
      position: 'absolute', left: PANEL.x + 16, width: PANEL.w - 32, bottom: 1080 - (PANEL.y + PANEL.h) + 16, borderRadius: 18, padding: '14px 16px',
      background: `linear-gradient(135deg, ${C.red}, #a30020)`, transform: `translateY(${(1 - p) * 140}px)`, opacity: p,
      boxShadow: `0 0 ${14 + pulse * 26}px rgba(228,0,43,${0.35 + pulse * 0.3})`, fontFamily: FONT,
    }}>
      <div style={{display: 'flex', alignItems: 'center', gap: 10, color: '#fff'}}>
        <svg width="34" height="34" viewBox="0 0 24 24"><path d="M12 2 1 21h22L12 2z" fill="#fff" /><path d="M11 9h2v6h-2zM11 16.5h2v2h-2z" fill={C.red} /></svg>
        <div style={{fontSize: 17, fontWeight: 900, letterSpacing: 1.5}}>ABNORMALITY?</div>
      </div>
      <div style={{color: '#fff', fontSize: 21, fontWeight: 700, marginTop: 6, lineHeight: 1.2}}>Report immediately to the Duty Security Executive</div>
    </div>
  );
};

/* ---------------- captions ---------------- */
const KEYWORDS = /(Duty Security Executive|Nil Discrepancy|Discrepancy Identified|YES|NO|Submit|Next|Back|ETD|AM|PM|mandatory|immediately)/g;
const Caption: React.FC<{slide: SlideT; t: number}> = ({slide, t}) => {
  const frame = useCurrentFrame();
  const chunks = React.useMemo(() => chunksOf(slide), [slide]);
  const idx = chunks.findIndex((c) => t >= c.start && t < c.end + 0.04);
  const ch = idx >= 0 ? chunks[idx] : null;
  const local = ch ? frame - Math.round(ch.start * FPS) : 0;
  const op = ch ? interpolate(local, [0, 6], [0, 1], clamp) : 0;
  const prog = interpolate(t, [0, slide.duration], [0, 1], clamp);
  return (
    <div style={{position: 'absolute', left: CAP.x, top: CAP.y, width: CAP.w, height: CAP.h, borderRadius: 22, background: 'rgba(5,8,20,0.82)', border: `1px solid ${C.line}`, overflow: 'hidden', fontFamily: FONT}}>
      <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: 8, background: C.red}} />
      <div style={{position: 'absolute', inset: '0 48px 0 40px', display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center'}}>
        {ch && (
          <div style={{opacity: op, transform: `translateY(${(1 - op) * 10}px)`, color: C.text, fontSize: 36, fontWeight: 600, lineHeight: 1.28}}>
            {ch.text.split(KEYWORDS).map((part, i) =>
              i % 2 === 1 ? <span key={i} style={{color: part === 'YES' ? C.green : part === 'NO' ? C.redSoft : C.amber, fontWeight: 800}}>{part}</span> : <React.Fragment key={i}>{part}</React.Fragment>
            )}
          </div>
        )}
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 5, background: 'rgba(255,255,255,0.08)'}}>
        <div style={{width: `${prog * 100}%`, height: '100%', background: `linear-gradient(90deg, ${C.red}, ${C.redSoft})`}} />
      </div>
    </div>
  );
};

/* ---------------- one slide scene ---------------- */
const Scene: React.FC<{slide: SlideT; idx: number}> = ({slide, idx}) => {
  const frame = useCurrentFrame();
  const dur = framesOf(slide);
  const t = frame / FPS;
  const enter = spring({frame, fps: FPS, config: {damping: 18, stiffness: 110}, durationInFrames: 22});
  const exit = interpolate(frame, [dur - 8, dur], [1, 0], clamp);
  const kb = interpolate(frame, [0, dur], [1, 1.045], {easing: Easing.inOut(Easing.quad), ...clamp});
  const origin = ['30% 40%', '70% 45%', '50% 60%', '40% 35%'][idx % 4];
  const chips = chipsOf(slide);
  const alertT = alertAt(slide);
  const visible = chips.filter((c) => c.at <= t);
  const maxChips = alertT !== null && alertT <= t ? 2 : 3;
  const shown = visible.slice(-maxChips);
  const sec = SECTIONS[sectionOf(slide.n)];
  const nowP = spring({frame: frame - 4, fps: FPS, config: {damping: 16}});

  return (
    <AbsoluteFill style={{opacity: exit}}>
      <Audio src={staticFile(`audio/s${pad(slide.n)}.mp3`)} />
      {/* slide card */}
      <div style={{position: 'absolute', left: CARD.x, top: CARD.y, width: CARD.w, height: CARD.h, borderRadius: 22, overflow: 'hidden', background: '#fff',
        boxShadow: '0 24px 70px rgba(0,0,0,0.55)', opacity: enter, transform: `translateX(${(1 - enter) * 70}px) scale(${0.97 + 0.03 * enter})`}}>
        <Img src={staticFile(`slides/s-${pad(slide.n)}.png`)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${kb})`, transformOrigin: origin}} />
        {/* sheen sweep on entry */}
        <div style={{position: 'absolute', top: 0, bottom: 0, width: 260, left: interpolate(frame, [0, 26], [-300, CARD.w + 100], clamp), transform: 'skewX(-18deg)',
          background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.35), transparent)'}} />
        {/* accent border draws in */}
        <div style={{position: 'absolute', left: 0, top: 0, height: 5, background: C.red, width: `${interpolate(frame, [0, 24], [0, 100], clamp)}%`}} />
      </div>
      {/* now card in panel */}
      <div style={{position: 'absolute', left: PANEL.x + 22, top: PANEL.y + 18 + 24 + 7 * 40 + 14, width: PANEL.w - 44, fontFamily: FONT, opacity: nowP, transform: `translateY(${(1 - nowP) * 18}px)`}}>
        <div style={{height: 1, background: C.line, marginBottom: 12}} />
        <div style={{display: 'flex', alignItems: 'center', gap: 10}}>
          <div style={{background: C.red, color: '#fff', fontSize: 14, fontWeight: 900, letterSpacing: 2, padding: '4px 10px', borderRadius: 8}}>SLIDE {pad(slide.n)}</div>
          <div style={{color: C.dim, fontSize: 14, fontWeight: 700, letterSpacing: 2}}>{sec.name.toUpperCase()}</div>
        </div>
        <div style={{color: C.text, fontSize: 21, fontWeight: 700, marginTop: 10, lineHeight: 1.2}}>{slide.title}</div>
        <div style={{marginTop: 6}}>{shown.map((c) => <Chip key={c.label} chip={c} t={t} />)}</div>
      </div>
      {alertT !== null && t >= alertT - 0.05 && <AlertBox at={alertT} />}
      <Caption slide={slide} t={t} />
    </AbsoluteFill>
  );
};

/* ---------------- composition ---------------- */
export const Training: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  let cur = 0;
  for (let i = 0; i < timeline.length; i++) if (frame >= starts[i]) cur = i;
  const fadeIn = interpolate(frame, [0, 20], [0, 1], clamp);
  const fadeOut = interpolate(frame, [durationInFrames - 30, durationInFrames], [1, 0], clamp);
  return (
    <AbsoluteFill style={{background: C.bg1, opacity: fadeIn * fadeOut}}>
      <Background />
      <Chrome cur={timeline[cur]} local={frame - starts[cur]} />
      {timeline.map((s, i) => (
        <Sequence key={s.n} from={starts[i]} durationInFrames={framesOf(s)} layout="none">
          <Scene slide={s} idx={i} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
