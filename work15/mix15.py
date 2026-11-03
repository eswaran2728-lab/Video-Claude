# Audio for the recap (no usable speech in the clips - only crowd and a short unclear announcement; transcripts.json):
#  - music "Driving Ambition" (Ahjay Stelino, Mixkit #32, Mixkit Stock Music Free License) from music 13.46 s, so its drop
#    (38.46 s) lands on the results (25.0 s) and its outro on the end card; 0.3 s fade in, 2.5 s fade out to 80 s.
#  - the clips' own sound low underneath (crowd, stick clacks in the bouts); slow motion is silent apart from SFX.
#  - SFX from the edit-video pack (Apache-2.0) on the graphic events in edit/cues.json (transient on the event frame).
# -> edit/assets/mix.wav (stereo 48 kHz)
import json, subprocess, numpy as np, soundfile as sf
import plan15 as P
SR = 48000; L = int(round(P.TOTAL * SR)); SFX = "/root/.claude/skills/edit-video/assets/sfx/"
db = lambda g: 10 ** (g / 20)
def dec(path, ss, t, ch=2):
    return np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(ss), "-t", str(t), "-i", path, "-ac", str(ch),
                                         "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, ch).astype(np.float64)
mus = dec("music/mixkit_32_driving_ambition.mp3", P.M, P.TOTAL + 1)[:L]; mus = np.pad(mus, ((0, L - len(mus)), (0, 0)))
fi = int(0.3 * SR); mus[:fi] *= np.linspace(0, 1, fi)[:, None]; fo = int(2.5 * SR); mus[-fo:] *= np.linspace(1, 0, fo)[:, None]
CLIPGAIN = {"hook_bout": -8, "hook_bg": -22, "arena": -16, "athletes": -15, "march": -17, "bout": -9, "bout_slow": None, "results_bg": -24}
amb = np.zeros((L, 2)); F = int(0.08 * SR)
for s in P.SEGS:
    g = CLIPGAIN[s["id"]]
    if g is None: continue
    d = s["t1"] - s["t0"]; x = dec(f"proxy/{s['clip']}.mp4", s["src_in"], d * s["speed"])
    if s["speed"] != 1:                                       # stretch by resampling (crowd bed only)
        n = int(d * SR); x = np.stack([np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x[:, c]) for c in (0, 1)], 1)
    x = x[: int(d * SR)].copy(); f = min(F, len(x) // 2); x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int(round(s["t0"] * SR)); amb[i:i + len(x)] += x * db(g)
fx = np.zeros(L)
for c in json.load(open("edit/cues.json"))["cues"]:
    x, s2 = sf.read(SFX + c["sfx"]); x = x if x.ndim == 1 else x.mean(1); pk = int(np.argmax(np.abs(x)))
    i0 = int(round(c["t"] * SR)) - pk; x = x[max(0, -i0):] * db(c["gain_db"]); i0 = max(0, i0); n = min(len(x), L - i0); fx[i0:i0 + n] += x[:n]
mix = mus * db(-3) + amb + fx[:, None]; pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
sf.write("edit/assets/mix.wav", mix, SR, subtype="PCM_24"); print("mix", P.TOTAL, "peak", round(pk, 3))
