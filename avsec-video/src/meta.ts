import timelineJson from '../data/timeline.json';

export const FPS = 30;
export const W = 1920;
export const H = 1080;

export type Sentence = {text: string; start: number; end: number};
export type SlideT = {n: number; title: string; duration: number; sentences: Sentence[]};
export const timeline = timelineJson as SlideT[];

export const SECTIONS = [
  {name: 'Get Started', from: 1, to: 5},
  {name: 'Flight Details', from: 6, to: 13},
  {name: 'Security Checks', from: 14, to: 19},
  {name: 'Truck & Remarks', from: 20, to: 25},
  {name: 'Sign-Offs', from: 26, to: 32},
  {name: 'Submit', from: 33, to: 36},
  {name: 'After Submit', from: 37, to: 39},
];
export const sectionOf = (n: number) => SECTIONS.findIndex((s) => n >= s.from && n <= s.to);

// ---- scene frame layout ----
export const starts: number[] = [];
let acc = 0;
for (const s of timeline) {
  starts.push(acc);
  acc += Math.round(s.duration * FPS);
}
export const TOTAL_FRAMES = acc;
export const framesOf = (s: SlideT) => Math.round(s.duration * FPS);

// ---- captions: split long sentences so they fit in two lines ----
export type Chunk = {text: string; start: number; end: number};
const MAX = 120;
function split(text: string): string[] {
  if (text.length <= MAX) return [text];
  const mid = text.length / 2;
  let best = -1;
  for (let i = 0; i < text.length; i++) {
    if (text[i] === ',' && i >= 35 && text.length - i >= 35 && (best < 0 || Math.abs(i - mid) < Math.abs(best - mid))) best = i;
  }
  if (best < 0) {
    best = text.indexOf(' ', Math.floor(mid));
    if (best < 0) return [text];
  }
  const a = text.slice(0, best + (text[best] === ',' ? 1 : 0)).trim();
  const b = text.slice(best + 1).trim();
  return [...split(a), ...split(b)];
}
export function chunksOf(s: SlideT): Chunk[] {
  const out: Chunk[] = [];
  for (const sen of s.sentences) {
    const parts = split(sen.text);
    const total = parts.reduce((a, p) => a + p.length, 0);
    let t = sen.start;
    for (const p of parts) {
      const d = ((sen.end - sen.start) * p.length) / total;
      out.push({text: p, start: t, end: t + d});
      t += d;
    }
  }
  return out;
}

// ---- callouts shown in the side panel, driven by what is being said ----
export type ChipKind = 'yes' | 'no' | 'tap' | 'sample' | 'info' | 'warn' | 'req';
export type ChipT = {kind: ChipKind; label: string; sub?: string; at: number};

const SAMPLE: Record<number, [RegExp, string, string]> = {
  7: [/enter 10:00 AM/, 'Start time', '10:00 AM'],
  8: [/TEST-AK01/, 'Flight No.', 'TEST-AK01'],
  9: [/11:30 AM/, 'ETD', '11:30 AM'],
  11: [/KUL-TEST/, 'Sector', 'KUL-TEST'],
  21: [/TEST-HL01/, 'Hi-Lift No.', 'TEST-HL01'],
  22: [/TEST-0001/, 'Seal No.', 'TEST-0001'],
  27: [/TEST USER/, 'Name', 'TEST USER'],
  28: [/TEST001/, 'Staff ID', 'TEST001'],
  29: [/10:30 AM/, 'End time', '10:30 AM'],
  32: [/TEST USER 2/, 'Sample data', 'TEST USER 2 · TEST002 · 10:45'],
};

type Rule = {re: RegExp; chip: Omit<ChipT, 'at'>; only?: number[]};
const RULES: Rule[] = [
  {re: /one form for each/, chip: {kind: 'info', label: 'One form per escort'}},
  {re: /QR code displayed/, chip: {kind: 'info', label: 'Tap link or scan QR', sub: 'Opens in your browser'}},
  {re: /no need to download/, chip: {kind: 'yes', label: 'No app needed'}},
  {re: /title reads/, chip: {kind: 'info', label: 'AA/SEC/F/042', sub: 'Hi-lift Escort Checklist'}},
  {re: /red asterisk symbol/, chip: {kind: 'req', label: 'Red * = mandatory'}},
  {re: /AM or PM option|AM or PM dropdown|whether it is AM or PM/, chip: {kind: 'info', label: 'Check AM / PM'}},
  {re: /Select AM for morning/, chip: {kind: 'info', label: 'AM = morning', sub: 'PM = afternoon & night'}},
  {re: /required question/, chip: {kind: 'req', label: '"This is a required question."'}},
  {re: /physically carry out|physically confirming|physically conduct/, chip: {kind: 'warn', label: 'Check first, then answer'}},
  {re: /select YES|selecting YES/, chip: {kind: 'yes', label: 'Select YES', sub: 'Only after the real check'}},
  {re: /must select NO|select NO\b/, chip: {kind: 'no', label: 'Select NO', sub: 'Then explain why'}},
  {re: /select Nil Discrepancy/, chip: {kind: 'yes', label: 'Nil Discrepancy', sub: 'Nothing wrong found'}},
  {re: /select Discrepancy Identified/, chip: {kind: 'no', label: 'Discrepancy Identified', sub: 'Report first, email sent'}},
  {re: /may leave it empty/, chip: {kind: 'info', label: 'Optional field'}},
  {re: /typing your full name/, chip: {kind: 'info', label: 'Signature = type full name'}},
  {re: /Staff No\./, chip: {kind: 'info', label: 'Label here: Staff No.'}},
  {re: /tap Back/, chip: {kind: 'tap', label: 'Tap Back', sub: 'Answers stay filled in'}},
  {re: /tap Submit|Tap Submit/, chip: {kind: 'tap', label: 'Tap Submit'}},
  {re: /cannot be edited|cannot edit/, chip: {kind: 'warn', label: 'No edits after Submit'}},
  {re: /Your response has been recorded/, chip: {kind: 'yes', label: 'Response recorded'}},
  {re: /central Google Sheet/, chip: {kind: 'info', label: 'Saved to Google Sheet', sub: 'One new row per form'}, only: [37]},
  {re: /System Unit/, chip: {kind: 'info', label: 'Escalate to System Unit'}},
  {re: /approved by the Head of Department/, chip: {kind: 'warn', label: 'Manual form needs HOD approval'}},
  {re: /tap Next|tap Next again|tap Next to/, chip: {kind: 'tap', label: 'Tap Next'}},
];

export function chipsOf(s: SlideT): ChipT[] {
  const out: ChipT[] = [];
  const seen = new Set<string>();
  const sam = SAMPLE[s.n];
  for (const sen of s.sentences) {
    if (sam && sam[0].test(sen.text) && !seen.has('sample')) {
      seen.add('sample');
      out.push({kind: 'sample', label: sam[1] === 'Sample data' ? 'Sample data' : 'Sample data · ' + sam[1], sub: sam[2], at: sen.start});
    }
    for (const r of RULES) {
      if (r.only && !r.only.includes(s.n)) continue;
      if (r.re.test(sen.text) && !seen.has(r.chip.label)) {
        seen.add(r.chip.label);
        out.push({...r.chip, at: sen.start});
      }
    }
  }
  return out;
}

export function alertAt(s: SlideT): number | null {
  for (const sen of s.sentences) {
    if (/Duty Security Executive|report the issue to your respective supervisor|inform your supervisor immediately/.test(sen.text)) return sen.start;
  }
  return null;
}
