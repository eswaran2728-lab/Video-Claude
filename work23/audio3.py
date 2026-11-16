"""Original music bed + sound effects for the work23 reel (synthesized here; no third-party audio).
Music: warm tanpura-style drone and soft hand-drum pulse, lifted on the hook, the reveal and the end card,
ducked 12 dB under the voice. SFX: risers/whooshes on transitions, a sub hit + shimmer on gold reveals,
soft pops on labels, UI ticks on the settings panel. usage: python3 audio3.py v01"""
import json, os, sys, subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve
ROOT = os.path.dirname(os.path.abspath(__file__)); V = sys.argv[1]
P = json.load(open(os.path.join(ROOT, V, 'edit-plan.json'))); M = json.load(open(os.path.join(ROOT, V, 'timing-map.json')))
SR = 48000; CUT = M['cut_end']; T = CUT + P['tail_card']; N = int(T * SR) + SR
rng = np.random.default_rng(23)
bp = lambda x, lo, hi: sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def put(buf, x, t0, g=1.0, pan=0.0):
    s = int(t0 * SR); e = min(len(buf), s + len(x))
    if e > s: buf[s:e, 0] += x[:e - s] * g * (1 - max(0, pan)); buf[s:e, 1] += x[:e - s] * g * (1 + min(0, pan))
SA = 130.81
def pluck(f, d=3.0):
    n = int(d * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * h * t * (1 + 0.0006 * h)) / h ** 0.9 * np.exp(-t * (0.7 + 0.22 * h)) for h in range(1, 12))
    x[:240] *= np.linspace(0, 1, 240); return x.astype(np.float32)
def drum(kind):
    if kind == 'low':
        n = int(.5 * SR); t = np.arange(n) / SR; f = 65 + 55 * np.exp(-t * 28)
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8)).astype(np.float32)
    n = int(.12 * SR); t = np.arange(n) / SR
    return (bp(rng.standard_normal(n), 1800, 7000) * np.exp(-t * 60)).astype(np.float32)
def whoosh(d=.6):
    n = int(d * SR); t = np.arange(n) / SR; w = rng.standard_normal(n)
    x = bp(w, 250, 2200) * (1 - t / d) + bp(w, 1500, 8000) * (t / d)
    return (x * np.sin(np.pi * t / d) ** 2 / np.abs(x).max()).astype(np.float32)
def riser(d=1.2):
    n = int(d * SR); t = np.arange(n) / SR; w = rng.standard_normal(n)
    x = bp(w, 400, 6000) * (t / d) ** 2.5
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / d) ** 2) / SR) * (t / d) ** 3 * 0.3
    return ((x / np.abs(x).max()) * .7 + tone).astype(np.float32)
def hit():
    n = int(1.2 * SR); t = np.arange(n) / SR; f = 50 + 70 * np.exp(-t * 18)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5)).astype(np.float32)
def shimmer(d=2.0):
    n = int(d * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (2 + i * .6)) * w for i, (f, w) in enumerate(((1567.98, 1), (2093, .7), (2637, .5), (3136, .35), (4186, .2))))
    x[:480] *= np.linspace(0, 1, 480); return (x / np.abs(x).max()).astype(np.float32)
def pop():
    n = int(.09 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * (900 - 500 * t / .09) * t) * np.exp(-t * 45)).astype(np.float32)
def tick():
    n = int(.03 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 200)).astype(np.float32)

mus = np.zeros((N, 2), np.float32)
notes = [SA * 1.5, SA * 2, SA * 2, SA]
tt, k = 0.0, 0
while tt < T - 1.5:
    put(mus, pluck(notes[k % 4] / (2 if k % 4 == 3 else 1)), tt, .5, pan=[-.3, .2, .3, -.1][k % 4]); k += 1; tt += .66
beat, tt, i = .66, 0.0, 0
while tt < T - 2.0:
    put(mus, drum('low' if i % 4 in (0, 3) else 'ki'), tt, .55 if i % 4 in (0, 3) else .18); tt += beat / 2; i += 1
ir_n = int(1.5 * SR); ir = rng.standard_normal((ir_n, 2)) * np.exp(-np.arange(ir_n) / SR / .4)[:, None] * .02
mus = mus + np.stack([fftconvolve(mus[:, c], ir[:, c])[:N] for c in range(2)], 1).astype(np.float32) * .6
fo = int((T - 1.8) * SR); mus[fo:] *= (np.linspace(1, 0, N - fo) ** 1.5)[:, None]

fx = np.zeros((N, 2), np.float32)
G = P['gfx']
hook = next(g for g in G if g['kind'] == 'hook')
put(fx, whoosh(.5), hook['b_at'] - .32, .5); put(fx, hit(), hook['b_at'], .55); put(fx, shimmer(), hook['b_at'] + .02, .25)
for g in G:
    st = g['t'][0]
    if g['kind'] == 'big':
        put(fx, riser(1.0), st - 1.0, .22); put(fx, hit(), st, .5)
        if g.get('shine'): put(fx, shimmer(2.4), st + .05, .3)
    elif g['kind'] in ('card', 'tag'): put(fx, whoosh(.45), st - .2, .22); put(fx, pop(), st + .05, .25)
    elif g['kind'] == 'chips':
        for j in range(len(g['items'])): put(fx, pop(), st + j * g.get('stagger', .35) + .05, .3, pan=(j - 1) * .3)
    elif g['kind'] == 'slicer':
        put(fx, whoosh(.5), st - .25, .25)
        for j in range(18): put(fx, tick(), st + .5 + j * .09, .18)
        put(fx, shimmer(1.0), st + .5 + len(g['moves']) * .25 + .8, .18)
for t in P.get('flashes', []): put(fx, whoosh(.6), t - .35, .35)
put(fx, whoosh(.7), CUT - .6, .3); put(fx, shimmer(2.6), CUT + .1, .3)

voice, _ = sf.read(os.path.join(ROOT, V, 'assets', 'audio', 'voice.wav'))
env = np.abs(voice.mean(1)); k_ = int(.05 * SR)
env = np.convolve(env, np.ones(k_) / k_, 'same')[:N] if len(env) >= N else np.pad(np.convolve(env, np.ones(k_) / k_, 'same'), (0, N - len(env)))
talk = (env > np.percentile(env[env > 0], 30) * 1.0).astype(np.float32)
k2 = int(.35 * SR); talk = np.minimum(1, np.convolve(talk, np.ones(k2) / k2 * 3, 'same'))
duck = 1 - talk * (1 - 10 ** (-12 / 20))
mus *= duck[:, None]; fx *= (.6 + .4 * duck)[:, None]
out = os.path.join(ROOT, V, 'assets', 'audio')
for name, x in (('music', mus), ('sfx', fx)):
    x = x[:int(T * SR)]; sf.write(os.path.join(out, name + '_raw.wav'), x / (np.abs(x).max() + 1e-9) * .9, SR, subtype='PCM_24')
subprocess.run(['ffmpeg', '-nostdin', '-y', '-v', 'error', '-i', os.path.join(out, 'music_raw.wav'), '-af', 'volume=-17dB', os.path.join(out, 'music.wav')], check=True)
subprocess.run(['ffmpeg', '-nostdin', '-y', '-v', 'error', '-i', os.path.join(out, 'sfx_raw.wav'), '-af', 'volume=-11dB', os.path.join(out, 'sfx.wav')], check=True)
print('music + sfx written', round(T, 2))
