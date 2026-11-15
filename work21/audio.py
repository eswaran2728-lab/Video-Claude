"""Audio for the Deepavali reel: one continuous bed from a single source clip + three synthesized accents.
Usage: python3 audio.py v01"""
import json, os, sys, subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

ROOT = os.path.dirname(os.path.abspath(__file__))
V = sys.argv[1] if len(sys.argv) > 1 else 'v01'
P = json.load(open(os.path.join(ROOT, V, 'edit-plan.json')))
T = P['total']; SR = 48000
out = os.path.join(ROOT, V, 'assets', 'audio'); os.makedirs(out, exist_ok=True)
a = P['audio']
# bed: loudness-normalised, limited (source peaks are clipped), fade in 0.12 s, fade out over the end card
fo = P['endcard']['start'] + 0.6
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(a['bed_in']), '-t', str(T), '-i', os.path.join(ROOT, 'source', a['bed_clip'] + '.mp4'),
                '-vn', '-af', f"highpass=f=40,loudnorm=I=-16:TP=-2:LRA=9,afade=t=in:d=0.12,afade=t=out:st={fo}:d={T-fo-0.15}",
                '-ar', str(SR), '-ac', '2', os.path.join(out, 'bed.wav')], check=True)

rng = np.random.default_rng(7)
N = int(T * SR); fx = np.zeros((N, 2), np.float32)
def put(x, t0, g):
    s = int(t0 * SR); e = min(N, s + len(x)); fx[s:e] += (x[: e - s] * g)[:, None]
def whoosh(d=0.55):
    n = int(d * SR); t = np.arange(n) / SR
    w = rng.standard_normal(n)
    lo = sosfilt(butter(2, [300, 2500], 'band', fs=SR, output='sos'), w)
    hi = sosfilt(butter(2, [1500, 7000], 'band', fs=SR, output='sos'), w)
    m = (t / d)[:, None].ravel()
    x = lo * (1 - m) + hi * m
    env = np.sin(np.pi * t / d) ** 2
    return (x * env / np.abs(x).max()).astype(np.float32)
def boom(d=0.7):
    n = int(d * SR); t = np.arange(n) / SR
    f = 95 * np.exp(-t * 5) + 42
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)
    x[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    return x.astype(np.float32)
def shimmer(d=1.8):
    n = int(d * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (2.2 + i * 0.5)) * w for i, (f, w) in enumerate(((1318.5, 1), (1975.5, .6), (2637, .4), (3951, .2))))
    x[: int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))
    return (x / np.abs(x).max()).astype(np.float32)

sh = {s['id']: s for s in P['shots']}; at = {}; t = 0
for s in P['shots']: at[s['id']] = t; t += s['dur']
put(boom(), at['s01'] + 0.72, 0.5)             # the leap in the hook
for x in P['flashes']: put(whoosh(), x - 0.3, 0.16)   # act changes
put(boom(), at['s08'] + 1.05, 0.38)
if 'n11' in at: put(boom(), at['n11'] + 0.72, 0.36)            # takedown punch-in
put(shimmer(), P['endcard']['start'] + 0.45, 0.2)     # end card
sf.write(os.path.join(out, 'sfx.wav'), fx, SR, subtype='PCM_16')
print('bed + sfx written; sfx peak', float(np.abs(fx).max()))
