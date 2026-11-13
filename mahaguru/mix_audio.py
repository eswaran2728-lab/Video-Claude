"""Build the ambience / music / effects stems for the Mahaguru film on the film's own clock.
Reads timing.json (from build_film.py). Writes film/assets/audio/{ambience,music,effects}.wav (48 kHz stereo)."""
import json, os
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly

ROOT = os.path.dirname(os.path.abspath(__file__))
SR = 48000
tm = json.load(open(os.path.join(ROOT, 'timing.json')))
C0, T, END, TOTAL = tm['C0'], tm['T'], tm['FILM_END'], tm['TOTAL']
N = int(TOTAL * SR) + SR
rng = np.random.default_rng(11)   # seeded: same mix every run


def load(path):
    a, sr = sf.read(path, always_2d=True, dtype='float32')
    if a.shape[1] == 1:
        a = np.repeat(a, 2, axis=1)
    if sr != SR:
        a = resample_poly(a, SR, sr, axis=0).astype(np.float32)
    return a[:, :2]


def db(x):
    return 10 ** (x / 20)


def lp(a, hz):
    return sosfilt(butter(2, hz, 'low', fs=SR, output='sos'), a, axis=0).astype(np.float32)


def hp(a, hz):
    return sosfilt(butter(2, hz, 'high', fs=SR, output='sos'), a, axis=0).astype(np.float32)


def rms_norm(a, target_db):
    r = np.sqrt(np.mean(a ** 2)) + 1e-9
    return a * (db(target_db) / r)


def looped(src, n, xf=1.5):
    """Loop src to n samples with equal crossfades, starting at a seeded random offset."""
    x = min(int(xf * SR), len(src) // 3)
    off = int(rng.integers(0, max(1, len(src) - 2 * x)))
    out = src[off:].copy()
    ramp = np.linspace(0, 1, x, dtype=np.float32)[:, None]
    while len(out) < n:
        nxt = src.copy()
        out[-x:] = out[-x:] * (1 - ramp) + nxt[:x] * ramp
        out = np.concatenate([out, nxt[x:]])
    return out[:n]


def place(dst, src, t0, gain_db=0.0, fade_in=0.5, fade_out=0.5, length=None):
    s = int(t0 * SR)
    a = src if length is None else src[: int(length * SR)]
    a = a * db(gain_db)
    fi, fo = int(fade_in * SR), int(fade_out * SR)
    a = a.copy()
    if fi: a[:fi] *= np.linspace(0, 1, fi)[:, None]
    if fo: a[-fo:] *= np.linspace(1, 0, fo)[:, None]
    e = min(len(dst), s + len(a))
    dst[s:e] += a[: e - s]


def bed(dst, src, t0, t1, gain_db, fade=0.8, filt=None):
    a = looped(src, int((t1 - t0) * SR))
    if filt: a = filt(a)
    place(dst, a, t0, gain_db, fade, fade)


def noise(n, color='pink'):
    w = rng.standard_normal((n, 2)).astype(np.float32)
    if color == 'brown':
        w = np.cumsum(w, axis=0); w -= np.mean(w, axis=0); w = hp(w, 20)
    else:
        w = lp(w, 1200)
    return w / (np.abs(w).max() + 1e-9)


def span(a, b):           # first clip of a .. end of slot b (film clock)
    nxt = {k: v for k, v in T.items()}
    keys = sorted(T, key=lambda k: T[k])
    i = keys.index(b)
    end = T[keys[i + 1]] if i + 1 < len(keys) else END
    return T[a], end


SRC = os.path.join(ROOT, 'audio', 'src')
forest = rms_norm(load(os.path.join(SRC, 'amb_walk.wav')), -24)
cicada = rms_norm(hp(load(os.path.join(SRC, 'cicada2.wav')), 300), -24)
room = rms_norm(noise(SR * 20), -24)
rumble = rms_norm(lp(noise(SR * 20, 'brown'), 160), -24)

amb = np.zeros((N, 2), np.float32)
# chapter 1: open hall in the morning (birds through the open side, quiet room)
a, b = span('1A', '1A'); bed(amb, forest, a, b + 0.3, -15, filt=lambda x: lp(x, 5000)); bed(amb, room, a, b + 0.3, -26)
a, b = span('1B', '1D'); bed(amb, forest, a - 0.2, b, -15, filt=lambda x: lp(x, 5000)); bed(amb, room, a - 0.2, b, -26)
# title: near silence, a little room
a, b = span('TITLE', 'TITLE'); bed(amb, room, a, b, -30, fade=1.5)
# chapters 2-3: the estate, cicadas and forest
a, b = span('2A', '3D'); bed(amb, forest, a - 0.3, b + 0.6, -11); bed(amb, cicada, a - 0.3, b - 3.0, -16, fade=2.0)
# chapter 4: teaching yard
a, b = span('4A', '4D'); bed(amb, forest, a - 0.3, b + 0.5, -13)
# chapter 5: roadside idle, the bus ride, then the new yard
a, b = span('5A', '5A'); bed(amb, rumble, a - 0.5, b, -15); bed(amb, forest, a - 0.5, b, -16)
a, b = span('5B', '5B'); bed(amb, rumble, a, b + 0.8, -10); bed(amb, lp(noise(SR * 20), 2500) * 0.3, a, b + 0.8, -30)
a, b = span('5C', '5D'); bed(amb, forest, a - 0.3, b, -12)
# chapter 6: pavilion stage at dusk, low room and a soft hush
a, b = span('6A', '6D'); bed(amb, room, a, b + 0.6, -22); bed(amb, forest, a, b + 0.6, -24, filt=lambda x: lp(x, 3000))
# chapter 7: researcher's courtyard, insects and footfalls only
a, b = span('7A', '7D'); bed(amb, cicada, a, b, -18); bed(amb, forest, a, b + 0.4, -16)
# chapter 8: recognition hall, then the yard again
a, b = span('8A', '8C'); bed(amb, room, a - 0.4, b, -21)
a, b = span('8D', '8D'); bed(amb, forest, a - 0.3, b + 0.5, -14)
# chapters 9-10: present-day court, softer outdoor tone with a distant city
a, b = span('9A', '10C'); bed(amb, forest, a, b, -19, fade=1.2, filt=lambda x: lp(x, 6000)); bed(amb, rumble, a, b, -27, fade=1.2)
a, b = span('10D', '10D'); bed(amb, room, a, b - 1.0, -32, fade=1.5)

# ---- effects: one dry bamboo touch on 1A
fx = np.zeros((N, 2), np.float32)
def knock(freq=720, dur=0.18):
    t = np.arange(int(dur * SR)) / SR
    tone = sum(np.sin(2 * np.pi * f * t) * w for f, w in ((freq, 1), (freq * 2.71, 0.35), (freq * 5.1, 0.12)))
    burst = rng.standard_normal(len(t)) * np.exp(-t * 180) * 0.6
    env = np.exp(-t * 32)
    x = ((tone * 0.6 + burst) * env).astype(np.float32)
    return np.stack([x, x * 0.92], 1) / np.abs(x).max()
place(fx, knock(), C0['1A'] + 1.1, -14, 0, 0.02)

# ---- music
mus = np.zeros((N, 2), np.float32)
MD = os.path.join(ROOT, 'audio', 'music')
def m(name):
    p = os.path.join(MD, name + '.wav')
    return rms_norm(load(p), -20) if os.path.exists(p) else None
flute, veena, drone = m('flute_alap'), m('veena_refrain'), m('drone_bed')
if drone is not None:
    drone = drone[int(5 * SR):]   # skip the low thump at its start
if flute is not None:
    place(mus, flute, C0['TITLE'] + 0.8, -3, 1.2, 2.0, length=9.0)                  # title: breathy flute
    place(mus, flute[int(10 * SR):], C0['9C'] + 1.0, -9, 1.5, 2.5, length=17.0)     # 9C-9D restrained flute
    place(mus, flute[-int(11 * SR):], C0['10D'] + 0.6, -3, 1.0, 3.0, length=8.4)    # 10D flute tail, ends ~1 s before the cut
if drone is not None:
    place(mus, drone, C0['3D'] + 5.0, -12, 2.5, 3.0, length=14.0)                  # 3D into 4A dissolve
    place(mus, drone, C0['8C'] + 0.5, -14, 2.0, 2.5, length=9.5)                    # archive table
if veena is not None:
    place(mus, veena, C0['5D'] + 6.6, -10, 0.6, 2.0, length=5.0)                   # 5D after the VO
    place(mus, veena, C0['10B'] + 2.0, -8, 3.0, 2.5, length=min(len(veena) / SR, 17.5))  # 10B-10C refrain

# duck music and ambience under every spoken line
duck = np.ones(N, np.float32)
for v in tm['voice']:
    s, e = int((v['start'] - 0.25) * SR), int((v['start'] + v['dur'] + 0.3) * SR)
    duck[max(0, s):e] = np.minimum(duck[max(0, s):e], db(-7))
k = int(0.25 * SR)
cs = np.concatenate([[0], np.cumsum(duck, dtype=np.float64)])
idx = np.arange(N)
lo, hi = np.clip(idx - k // 2, 0, N), np.clip(idx + k // 2, 0, N)
duck = ((cs[hi] - cs[lo]) / np.maximum(1, hi - lo)).astype(np.float32)
mus *= duck[:, None]
amb *= (1 - (1 - duck) * 0.45)[:, None]     # ambience dips less
# 10A: no score, ambience pulled down so his voice and breath carry
s, e = int(T['10A'] * SR), int(T['10B'] * SR)
mus[s:e] = 0
amb[s:e] *= db(-6)

out = os.path.join(ROOT, 'film', 'assets', 'audio')
os.makedirs(out, exist_ok=True)
for name, a in (('ambience', amb), ('music', mus), ('effects', fx)):
    a = a[: int(TOTAL * SR)]
    peak = np.abs(a).max()
    if peak > 0.89: a = a * (0.89 / peak)
    sf.write(os.path.join(out, name + '.wav'), a, SR, subtype='PCM_16')
    print(name, 'peak', round(float(np.abs(a).max()), 3), 'music' if name == 'music' and not peak else '')
print('music cues:', [n for n, x in (('flute', flute), ('veena', veena), ('drone', drone)) if x is not None])
