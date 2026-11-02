# Audio: the creator's isolated voice (src/vo_iso.wav) cut by plan14.VO (12 ms fades), cleaned (80 Hz HPF, gentle 2-stage
# compression, -3 dBFS limiter); music "Epical Drums 05" (Grigoriy Nuzhny, Mixkit #680, Mixkit Stock Music Free License)
# ducked 16 dB under speech; SFX from the edit-video pack (Apache-2.0) on visible events, transient on the event frame.
# -> edit/assets/mix.wav (stereo 48 kHz) + edit/cues.json
import json, subprocess, numpy as np, soundfile as sf
import plan14 as P
SR = 48000; L = int(round(P.TOTAL * SR)); SFX = "/root/.claude/skills/edit-video/assets/sfx/"
db = lambda g: 10 ** (g / 20)
a, sr = sf.read("src/vo_iso.wav"); assert sr == SR
vo = np.zeros(L); F = int(0.012 * SR)
for o, s0, s1 in P._out:
    x = a[int(s0 * SR):int(s1 * SR)].copy(); x[:F] *= np.linspace(0, 1, F); x[-F:] *= np.linspace(1, 0, F)
    i = int(round(o * SR)); vo[i:i + len(x)] += x[:L - i]
sf.write("src/vo_cut.wav", vo, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "src/vo_cut.wav", "-af",
                "highpass=f=80,acompressor=threshold=-24dB:ratio=3:attack=8:release=120:makeup=4,acompressor=threshold=-14dB:ratio=4:attack=3:release=80,"
                "alimiter=limit=0.708:level=false", "-ar", str(SR), "-c:a", "pcm_f32le", "src/vo_proc.wav"], check=True)
v, _ = sf.read("src/vo_proc.wav"); v = np.pad(v, (0, max(0, L - len(v))))[:L]
# speech activity -> duck curve
h = SR // 50; e = np.array([np.sqrt(np.mean(v[i:i + h] ** 2)) for i in range(0, L, h)])
act = np.convolve((20 * np.log10(e + 1e-9) > -40).astype(float), np.ones(15), "same") > 0
g = np.repeat(np.where(act, db(-17), db(-7)), h)[:L]; g = np.convolve(g, np.ones(int(0.15 * SR)) / int(0.15 * SR), "same")
mus = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", "1.0", "-i", "music/mixkit_680_epical_drums_05.mp3", "-t", str(P.TOTAL + 1),
                                    "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).astype(np.float64)[:L]
mus = np.pad(mus, (0, L - len(mus))) * g; fo = int(0.9 * SR); mus[-fo:] *= np.linspace(1, 0, fo)
W = P.W; S = {s["name"]: s for s in P.SCENES}; rv = S["print"]["reveal"]
CUES = [(0.0, "curated/hook-impact.wav", -12), (rv[0], "curated/zoom-swish.wav", -14), (rv[1], "thock.wav", -8),
        (W["inches"] + 0.05, "ratchet.wav", -14), (W["inches"] + 1.1, "curated/ui-pop.wav", -12), (W["inches"] + 1.6, "curated/ui-pop.wav", -12),
        (S["compare"]["t0"], "curated/camera-shutter-light.wav", -14), (W["design"], "curated/ui-pop.wav", -13),
        (W["colour"] + 0.9, "clean-ding.wav", -12), (S["want"]["t0"] + 0.1, "curated/zoom-swish.wav", -14),
        (S["want"]["t0"] + 1.2, "curated/ui-pop.wav", -13), (S["want"]["t0"] + 1.5, "curated/ui-pop.wav", -13), (S["want"]["t0"] + 1.8, "curated/ui-pop.wav", -13),
        (S["end"]["t0"] + 0.2, "sub-impact.wav", -10), (S["end"]["t0"] + 0.9, "curated/ui-click.wav", -12)]
t = rv[0] + 0.1                                              # printer-like ticks while the layers build
while t < rv[1] - 0.05: CUES.append((round(t, 3), "typing-tick.wav", -22)); t += 0.11
fx = np.zeros(L)
for tt, name, gain in CUES:
    x, s2 = sf.read(SFX + name); x = x if x.ndim == 1 else x.mean(1); pk = int(np.argmax(np.abs(x)))
    i0 = int(round(tt * SR)) - pk; x = x[max(0, -i0):] * db(gain); i0 = max(0, i0); n = min(len(x), L - i0); fx[i0:i0 + n] += x[:n]
mix = v * db(1) + mus + fx; pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
sf.write("edit/assets/mix.wav", np.stack([mix, mix], 1), SR, subtype="PCM_24")
json.dump({"cues": [{"t": round(a, 3), "sfx": b, "gain_db": c} for a, b, c in CUES]}, open("edit/cues.json", "w"), indent=1)
print("mix", P.TOTAL, "cues", len(CUES))
