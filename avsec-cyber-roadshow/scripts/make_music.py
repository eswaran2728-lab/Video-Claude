"""Original instrumental bed for the AVSEC Cyber Roadshow recap.

Composed in code for this film, so it is owned outright (no third-party
licence). 120 BPM, D major, 35 s. Section changes sit on the film's cuts:

  0-5   intro groove        13    payoff (3rd place)     25-29  breakdown
  5     drop (light switch) 20.5  full energy (1st)      29-33  finale
  10-13 build + drop-out    33-35 IV-V-I resolve, ring-out

Run:  python3 scripts/make_music.py   ->  assets/audio/music.wav
Needs numpy and scipy.
"""

import wave
from pathlib import Path

import numpy as np
from scipy import signal

SR = 48000
DUR = 35.0
N = int(SR * DUR)
BPM = 120
BEAT = 60 / BPM
t_all = np.arange(N) / SR
rng = np.random.default_rng(20261027)

NOTE = {"D2": 73.42, "G2": 98.00, "A2": 110.00, "B2": 123.47,
        "C#4": 277.18, "D4": 293.66, "E4": 329.63, "F#4": 369.99, "G4": 392.00,
        "A4": 440.00, "B4": 493.88, "C#5": 554.37, "D5": 587.33, "F#5": 739.99, "A5": 880.00}
CHORDS = {
    "D": (["D4", "F#4", "A4"], "D2"),
    "A": (["C#4", "E4", "A4"], "A2"),
    "Bm": (["D4", "F#4", "B4"], "B2"),
    "G": (["D4", "G4", "B4"], "G2"),
}
# Bars are 2 s long and start on odd seconds so every cut lands on a bar line.
BARS = [(-1, "D"), (1, "Bm"), (3, "G"), (5, "D"), (7, "A"), (9, "G"), (11, "A"),
        (13, "D"), (15, "A"), (17, "Bm"), (19, "G"), (21, "D"), (23, "A"),
        (25, "Bm"), (27, "G"), (29, "D"), (31, "A"), (33, "D")]


def chord_at(t):
    name = BARS[0][1]
    for start, c in BARS:
        if t >= start:
            name = c
    return name


def env_exp(n, decay):
    return np.exp(-np.arange(n) / SR / decay)


def add(buf, start_s, x, gain=1.0):
    i = int(round(start_s * SR))
    if i >= len(buf):
        return
    j = min(len(buf), i + len(x))
    if i < 0:
        x = x[-i:]
        i = 0
    buf[i:j] += gain * x[: j - i]


def saw(freq, n, phase=0.0):
    ph = (phase + freq * np.arange(n) / SR) % 1.0
    return 2 * ph - 1


def lp(x, fc, order=2):
    sos = signal.butter(order, fc, "low", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def hp(x, fc, order=2):
    sos = signal.butter(order, fc, "high", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def bp(x, lo, hi):
    sos = signal.butter(2, [lo, hi], "band", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def section(t):
    if t < 1.0: return "intro0"
    if t < 5.0: return "intro"
    if t < 10.0: return "drop"
    if t < 12.6: return "build"
    if t < 13.0: return "gap"
    if t < 20.5: return "groove"
    if t < 25.0: return "full"
    if t < 29.0: return "break"
    if t < 33.0: return "finale"
    return "resolve"


# ---------------------------------------------------------------- drums
kick = np.zeros(N); clap = np.zeros(N); hats = np.zeros(N); crash = np.zeros(N); roll = np.zeros(N)

def kick_hit():
    n = int(0.5 * SR)
    tt = np.arange(n) / SR
    f = 48 + 110 * np.exp(-tt / 0.03)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env_exp(n, 0.28)
    click = hp(rng.standard_normal(n), 2500) * env_exp(n, 0.004) * 0.35
    return np.tanh(2.2 * (body + click)) * 0.9

def clap_hit():
    n = int(0.35 * SR)
    noise = bp(rng.standard_normal(n), 900, 3200)
    e = np.zeros(n)
    for k, off in enumerate([0, 0.011, 0.022]):
        i = int(off * SR)
        e[i:] += env_exp(n - i, 0.012 if k < 2 else 0.11)
    return noise * e * 0.6

def hat_hit(open_=False):
    n = int((0.2 if open_ else 0.06) * SR)
    return hp(rng.standard_normal(n), 7500, 4) * env_exp(n, 0.07 if open_ else 0.018) * 0.5

def crash_hit():
    n = int(2.2 * SR)
    x = hp(rng.standard_normal(n), 3800, 2) * env_exp(n, 0.65)
    return x * 0.5

def snare_hit():
    n = int(0.16 * SR)
    tt = np.arange(n) / SR
    tone = np.sin(2 * np.pi * 190 * tt) * env_exp(n, 0.04)
    noise = bp(rng.standard_normal(n), 1200, 6000) * env_exp(n, 0.06)
    return (0.5 * tone + noise) * 0.6

K = kick_hit()
nbeats = int(DUR / BEAT)
kick_times = []
for b in range(nbeats + 1):
    t = b * BEAT
    s = section(t)
    if s in ("intro", "drop", "groove", "full", "finale") or (s == "build" and t < 12.0):
        add(kick, t, K); kick_times.append(t)
    # Claps on 2 and 4 of each bar (bars start on odd seconds -> backbeats on even + .0? use beat parity)
    bar_pos = ((t - 1.0) / BEAT) % 4
    if s in ("drop", "groove", "full", "finale") and int(round(bar_pos)) in (1, 3):
        add(clap, t, clap_hit())
    if s == "break" and int(round(bar_pos)) in (1, 3):
        add(clap, t, clap_hit(), 0.35)

for k in range(int(DUR / (BEAT / 4)) + 1):
    t = k * BEAT / 4
    s = section(t)
    sixteenth = k % 4
    if s in ("intro",) and sixteenth == 2:
        add(hats, t, hat_hit(), 0.8)
    elif s in ("drop", "groove", "finale"):
        add(hats, t, hat_hit(open_=(sixteenth == 2)), 0.9 if sixteenth == 2 else 0.45)
    elif s == "full":
        add(hats, t, hat_hit(open_=(sixteenth == 2)), 1.0 if sixteenth == 2 else 0.6)
    elif s == "break" and sixteenth in (2,):
        add(hats, t, hat_hit(), 0.35)

for t in (5.0, 13.0, 20.5, 29.0):
    add(crash, t, crash_hit())

# Snare roll accelerating into the drop-out (10.0 -> 12.6).
t = 10.0
while t < 12.6:
    prog = (t - 10.0) / 2.6
    step = BEAT / 2 if prog < 0.35 else (BEAT / 4 if prog < 0.75 else BEAT / 8)
    add(roll, t, snare_hit(), 0.25 + 0.75 * prog)
    t += step

# Sidechain pump driven by the kicks.
pump = np.ones(N)
for kt in kick_times:
    i = int(kt * SR); n = int(0.28 * SR)
    seg = 1 - 0.5 * np.exp(-np.arange(n) / SR / 0.09)
    j = min(N, i + n)
    pump[i:j] = np.minimum(pump[i:j], seg[: j - i])

# ---------------------------------------------------------------- tonal parts
padL = np.zeros(N); padR = np.zeros(N); bass = np.zeros(N); arp = np.zeros(N); keys = np.zeros(N)

for bi, (start, cname) in enumerate(BARS):
    end = BARS[bi + 1][0] if bi + 1 < len(BARS) else DUR
    s0, s1 = max(0.0, start), min(DUR, end)
    if s1 <= s0:
        continue
    n = int((s1 - s0) * SR)
    notes, root = CHORDS[cname]
    # Pad: 3 detuned saws per note, spread L/R.
    for nm in notes:
        f = NOTE[nm]
        for d, pan in ((-0.12, 0.2), (0.0, 0.5), (0.13, 0.8)):
            v = saw(f * 2 ** (d / 12), n, phase=rng.random()) * 0.11
            padL[int(s0 * SR): int(s0 * SR) + n] += v * (1 - pan)
            padR[int(s0 * SR): int(s0 * SR) + n] += v * pan
    # Bass: 8th-note pulse with a sub.
    fb = NOTE[root]
    for k in range(int((s1 - s0) / (BEAT / 2)) + 1):
        tt0 = s0 + k * BEAT / 2
        sec = section(tt0)
        if tt0 >= s1 or sec in ("intro0", "gap", "resolve"):
            continue
        if sec == "break" and k % 2 == 1:
            continue
        m = int(BEAT / 2 * SR * 0.92)
        x = 0.7 * saw(fb, m) + 0.3 * np.sin(2 * np.pi * fb * np.arange(m) / SR)
        x *= np.minimum(1, np.arange(m) / (0.004 * SR)) * env_exp(m, 0.2)
        add(bass, tt0, x, 0.32)
    # Arp: 16ths over chord tones an octave up.
    pattern = [0, 1, 2, 1, 2, 0, 1, 2]
    for k in range(int((s1 - s0) / (BEAT / 4)) + 1):
        tt0 = s0 + k * BEAT / 4
        sec = section(tt0)
        if tt0 >= s1 or sec in ("gap", "resolve", "build"):
            continue
        if sec in ("intro0", "intro", "break") and k % 2 == 1:
            continue
        f = NOTE[notes[pattern[k % 8]]] * 2
        m = int(0.22 * SR)
        sq = np.sign(np.sin(2 * np.pi * f * np.arange(m) / SR)) * 0.5 + saw(f * 1.004, m) * 0.5
        x = sq * env_exp(m, 0.07)
        gain = {"intro0": 0.09, "intro": 0.12, "drop": 0.14, "groove": 0.13, "full": 0.16, "break": 0.13, "finale": 0.16}.get(sec, 0.12)
        add(arp, tt0, x, gain)
    # Breakdown keys: soft chord stabs on each beat.
    if section(s0) == "break":
        for k in range(int((s1 - s0) / BEAT)):
            tt0 = s0 + k * BEAT
            m = int(0.9 * SR)
            x = np.zeros(m)
            for nm in notes:
                f = NOTE[nm]
                tt = np.arange(m) / SR
                x += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * env_exp(m, 0.35)
            add(keys, tt0, x, 0.16)

# Final resolve: rising arpeggio and a long tonic chord.
res = np.zeros(N)
for i, nm in enumerate(["D4", "F#4", "A4", "D5", "F#5", "A5"]):
    f = NOTE[nm]; m = int(2.0 * SR); tt = np.arange(m) / SR
    x = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt) + 0.1 * np.sin(2 * np.pi * 3 * f * tt)) * env_exp(m, 0.9)
    add(res, 33.0 + i * 0.09, x, 0.16)
add(kick, 33.0, K)
add(crash, 33.0, crash_hit(), 0.8)

# ---------------------------------------------------------------- automation
def curve(points):
    xs, ys = zip(*points)
    return np.interp(t_all, xs, ys)

bright = curve([(0, 0), (1, 0.2), (4.9, 0.35), (5.0, 0.75), (9.9, 0.75), (10.0, 0.3), (12.6, 1.0), (13.0, 0.7),
                (20.4, 0.75), (20.5, 1.0), (24.9, 1.0), (25.0, 0.35), (28.9, 0.5), (29.0, 1.0), (35, 1.0)])
pad_gain = curve([(0, 0), (0.6, 0.8), (12.55, 1.0), (12.6, 0.25), (12.95, 0.25), (13.0, 1.0), (24.9, 1.0), (25.0, 1.6), (28.9, 1.6), (29.0, 1.0), (35, 1.0)])

def bright_lp(x):
    dark, light = lp(x, 900), lp(x, 4200)
    return dark * (1 - bright) + light * bright

padL = bright_lp(padL) * pad_gain * (0.55 + 0.45 * pump)
padR = bright_lp(padR) * pad_gain * (0.55 + 0.45 * pump)
bass = hp(lp(bass, 1400), 50) * (0.4 + 0.6 * pump)
arp = bright_lp(arp) * (0.7 + 0.3 * pump)

# Simple stereo delay on the arp (dotted 8th).
dly = int(BEAT * 0.75 * SR)
arpL = arp.copy(); arpR = arp.copy()
arpR[dly:] += 0.35 * arp[:-dly]
arpL[2 * dly:] += 0.2 * arp[: -2 * dly]

# Small hall: exponentially decaying noise IR.
ir_n = int(1.4 * SR)
ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR / 0.35)
ir = lp(ir, 5000); ir /= np.sqrt(np.sum(ir ** 2))
wet_src = 0.5 * (padL + padR) + arp + keys + res
wet = signal.fftconvolve(wet_src, ir)[:N] * 0.18

drums = hp(kick, 38) * 0.42 + clap * 0.7 + hats * 0.75 + crash * 0.4 + roll * 0.6
mono = bass + drums + keys + res
L = mono + padL + arpL + wet
R = mono + padR + arpR + wet

# Drop-out gap 12.6-13.0 and final fade 34.2-35.0.
master = curve([(0, 1), (12.6, 1), (12.62, 0.12), (12.98, 0.12), (13.0, 1), (34.2, 1), (35.0, 0)])
L *= master; R *= master
# Gentle mix-bus saturation, then peak headroom.
L = np.tanh(1.3 * L) / 1.3; R = np.tanh(1.3 * R) / 1.3
peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.7 / peak; R *= 0.7 / peak

out = Path(__file__).resolve().parent.parent / "assets" / "audio" / "music.wav"
out.parent.mkdir(parents=True, exist_ok=True)
pcm = (np.stack([L, R], axis=1) * 32767).astype(np.int16)
with wave.open(str(out), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote", out, f"{DUR}s")
