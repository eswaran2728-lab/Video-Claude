# Audio for work21 v01 -> edit/assets/mix.wav
#  music: "Driving Ambition" (Ahjay Stelino, Mixkit #32, Mixkit Stock Music Free License) from 29.08 s, drop on output beat 16, faded out by the end;
#  venue sound from the performance clips kept low underneath (stick swishes, room); none under the slow motion;
#  SFX (edit-video pack, Apache-2.0) placed so each transient lands on its visual cue (edit/cues.json); light limiter.
import json, subprocess, numpy as np, soundfile as sf, scipy.signal as ss
import os, importlib
VERSION = os.environ.get("VERSION", "v01"); P = importlib.import_module("plan21" if VERSION == "v01" else f"plan21_{VERSION}"); O = getattr(P, "OUT", "edit")
MUSIC = getattr(P, "MUSIC", "music/mixkit_32_driving_ambition.mp3")
SR = 48000; L = int(P.TOTAL * SR); db = lambda g: 10 ** (g / 20)
def load(cmd):
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout; return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
mus = load(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(P.MUSIC_IN), "-t", str(P.TOTAL + 0.5), "-i", MUSIC, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"])[:L]
mus = np.pad(mus, ((0, L - len(mus)), (0, 0)))
fo = int(getattr(P, "FADE", 2.6) * SR); mus[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5; mus[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
mix = mus * db(-3)
for s in P.SEGS:                                          # venue sound under its own picture, low
    if s.get("speed", 1) < 1: continue
    t0, t1 = P.b(s["k0"]), P.b(s["k1"]); n = int((t1 - t0) * SR)
    a = load(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(s["src"]), "-t", f"{t1 - t0:.3f}", "-i", f"src/mov/{s['clip']}.MOV", "-af", "highpass=f=120", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"])[:n]
    f = int(0.04 * SR); env = np.ones(len(a)); env[:f] = np.linspace(0, 1, f); env[-f:] = np.linspace(1, 0, f)
    i0 = int(t0 * SR); mix[i0:i0 + len(a)] += a * env[:, None] * db(-17)
SFX = "/home/user/Video-Claude/.claude/skills/edit-video/assets/sfx/"
for c in json.load(open(f"{O}/cues.json"))["cues"]:
    x, s2 = sf.read(SFX + c["sfx"]); x = x if x.ndim == 1 else x.mean(1)
    if s2 != SR: x = ss.resample_poly(x, SR, s2)
    pk = int(np.argmax(np.abs(x))) if "riser" not in c["sfx"] else len(x) - 1     # riser: its end lands on the cue
    i0 = int(round(c["t"] * SR)) - pk; x = x[max(0, -i0):] * db(c["gain_db"]); i0 = max(0, i0); m = min(len(x), L - i0)
    mix[i0:i0 + m] += x[:m, None]
pk = np.abs(mix).max(); mix *= min(1, 0.9 / pk)
sf.write(f"{O}/assets/mix_pre.wav", mix, SR, subtype="PCM_24")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{O}/assets/mix_pre.wav", "-af", "alimiter=limit=0.7:attack=3:release=60:level=false", "-ar", str(SR), "-c:a", "pcm_s24le", f"{O}/assets/mix.wav"], check=True)
os.remove(f"{O}/assets/mix_pre.wav"); print("mix", P.TOTAL, "s")
