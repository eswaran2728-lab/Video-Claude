"""Original soundtrack for the statue reel, synthesized here (no third-party audio, no licence needed).
Music: tanpura-style drone + mridangam-style percussion + temple-bell accents. SFX: printer motor, brush swish,
callout ticks, whooshes. usage: python3 audio.py v01"""
import json, os, sys, subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

ROOT = os.path.dirname(os.path.abspath(__file__))
V = sys.argv[1] if len(sys.argv) > 1 else 'v01'
P = json.load(open(os.path.join(ROOT, V, 'edit-plan.json')))
at, t = {}, 0.0
for s in P['shots']: at[s['id']] = t; t += s['dur']
T = t; SR = 48000; N = int(T * SR) + SR
rng = np.random.default_rng(22)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, hz): return sosfilt(butter(2, hz, 'low', fs=SR, output='sos'), x)
def env(n, a, d): t = np.arange(n) / SR; e = np.exp(-t / d); k = int(a * SR); e[:k] *= np.linspace(0, 1, k) if k else 1; return e
def put(buf, x, t0, g=1.0, pan=0.0):
    s = int(t0 * SR); e = min(len(buf), s + len(x))
    if e <= s: return
    buf[s:e, 0] += x[: e - s] * g * (1 - max(0, pan)); buf[s:e, 1] += x[: e - s] * g * (1 + min(0, pan))

SA = 138.59
def pluck(f, dur=2.8):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * h * t * (1 + 0.0007 * h) + 0.3 * np.sin(2 * np.pi * 0.7 * t * h)) / h ** 0.9 * np.exp(-t * (0.8 + 0.25 * h)) for h in range(1, 14))
    return (x * env(n, 0.01, 1.6)).astype(np.float32)
def drum(kind):
    if kind == 'tha':
        n = int(0.5 * SR); t = np.arange(n) / SR; f = 70 + 60 * np.exp(-t * 30)
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)).astype(np.float32)
    if kind == 'nam':
        n = int(0.7 * SR); t = np.arange(n) / SR
        x = sum(np.sin(2 * np.pi * SA * 2 * r * t) * a * np.exp(-t * d) for r, a, d in ((1, 1, 5), (2.0, .5, 7), (3.01, .3, 9), (4.2, .15, 14)))
        x += bp(rng.standard_normal(n), 1500, 5000) * np.exp(-t * 80) * 0.4
        return x.astype(np.float32)
    n = int(0.08 * SR); t = np.arange(n) / SR       # 'ki' click
    return (bp(rng.standard_normal(n), 2500, 8000) * np.exp(-t * 90)).astype(np.float32)
def bell(f=1046.5, dur=3.5):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * r * t) * a * np.exp(-t * d) for r, a, d in ((1, 1, 1.0), (2.76, .5, 1.8), (5.4, .3, 3), (8.93, .15, 5), (0.5, .4, 0.8)))
    k = int(0.004 * SR); x[:k] *= np.linspace(0, 1, k)
    return x.astype(np.float32)

mus = np.zeros((N, 2), np.float32)
# drone from the start, swelling at the paint step, holding under the end card
tp = [SA * 1.5, SA * 2, SA * 2, SA]
k = 0; tt = 0.0
while tt < T - 1.0:
    g = 0.25 if tt < 2.3 else 0.55
    put(mus, pluck(tp[k % 4] / (2 if k % 4 == 3 else 1)), tt, g, pan=[-.3, .2, .3, -.1][k % 4]); k += 1; tt += 0.62
# percussion: enters with the details, doubles at the reveal, final hit on the end card
beat = 0.6
pat = ['tha', 'ki', 'nam', 'ki', 'tha', 'nam', 'ki', 'nam']
s0, s1, s2 = at['d1'], at['rv'], at['ec']
tt = s0; i = 0
while tt < s2 - 0.05:
    sub = beat / 2 if tt < s1 else beat / 4
    kind = pat[i % 8]
    g = {'tha': .9, 'nam': .45, 'ki': .25}[kind] * (1.0 if tt < s1 else 1.15)
    put(mus, drum(kind), tt, g, pan=(-.15 if kind == 'nam' else .1)); tt += sub; i += 1
put(mus, drum('tha'), s2, 1.3); put(mus, drum('nam'), s2, .7)
put(mus, bell(), at['p1'] + 2.3, .32, -.2)      # colour starts
put(mus, bell(1396.9, 4.0), s2 + 0.05, .4, .2)  # end card
# room: short synthetic reverb
ir_n = int(1.6 * SR); ir = rng.standard_normal((ir_n, 2)) * np.exp(-np.arange(ir_n) / SR / 0.45)[:, None] * 0.02
wet = np.stack([fftconvolve(mus[:, c], ir[:, c])[:N] for c in range(2)], 1)
mus = mus + wet.astype(np.float32) * 0.6
fo = int((T - 1.6) * SR); mus[fo:] *= np.linspace(1, 0, len(mus) - fo)[:, None] ** 1.5

fx = np.zeros((N, 2), np.float32)
pr = P['shots'][0]['print']
# printer: stepper whine stepping in pitch while the scan line climbs
n = int((pr['scan'][1] - pr['scan'][0]) * SR); t = np.arange(n) / SR
steps = 420 + 260 * np.floor(np.abs(np.sin(np.floor(t / 0.11) * 1.7)) * 4) / 4
ph = np.cumsum(steps) / SR
motor = np.sign(np.sin(2 * np.pi * ph)) * 0.5 + np.sin(2 * np.pi * ph * 2) * 0.3
motor = lp(motor, 2200) * (0.6 + 0.4 * np.sin(2 * np.pi * t * 9)) * np.minimum(1, t / 0.05) * np.minimum(1, (t[-1] - t) / 0.15 + 1e-3)
put(fx, motor.astype(np.float32), pr['scan'][0], 0.06)
for k2 in range(int(n / SR / 0.11)):
    put(fx, drum('ki'), pr['scan'][0] + k2 * 0.11, 0.05)
# brush swish across the paint reveal
b0, b1 = pr['paint']; n = int((b1 - b0 + 0.2) * SR); t = np.arange(n) / SR
w = rng.standard_normal(n); sw = bp(w, 800, 4000) * np.sin(np.pi * t / t[-1]) ** 1.5
put(fx, (sw / np.abs(sw).max()).astype(np.float32), b0, 0.22, -.3)
# callout ticks
for c in P['callouts']:
    put(fx, drum('ki'), at[c['shot']] + 0.15, 0.5); put(fx, drum('nam') * 0.4, at[c['shot']] + 0.15, 0.25)
def whoosh(d=0.6):
    n = int(d * SR); t = np.arange(n) / SR; w = rng.standard_normal(n)
    x = bp(w, 300, 2500) * (1 - t / d) + bp(w, 1500, 7000) * (t / d)
    return (x * np.sin(np.pi * t / d) ** 2 / np.abs(x).max()).astype(np.float32)
for k3 in ('d1', 'rv', 'ec'):
    put(fx, whoosh(), at[k3] - 0.35, 0.22)

out = os.path.join(ROOT, V, 'assets', 'audio'); os.makedirs(out, exist_ok=True)
for name, x in (('music', mus), ('sfx', fx)):
    x = x[: int(T * SR)]
    sf.write(os.path.join(out, name + '_raw.wav'), x / (np.abs(x).max() + 1e-9) * 0.9, SR, subtype='PCM_24')
# levels: music to -17 LUFS, effects mixed relative to it
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(out, 'music_raw.wav'), '-af', 'loudnorm=I=-17:TP=-2:LRA=9', '-ar', str(SR), os.path.join(out, 'music.wav')], check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(out, 'sfx_raw.wav'), '-af', 'volume=-9dB', '-ar', str(SR), os.path.join(out, 'sfx.wav')], check=True)
print('audio written', round(T, 2), 's')
