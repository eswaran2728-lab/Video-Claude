# Audio for the RevLog explainer -> project/assets/mix.wav
#  voice: each line's HyperFrames TTS clip (trimmed to speech) at its laid-out time; light high-pass + gentle compression
#  music: "Motivating Mornings" (Mixkit #33, Mixkit Stock Music Free License), looped with crossfades,
#         about 22 dB under the voice while it speaks, a little higher in the pauses, faded in and out
#  sfx: a soft click on taps and a camera shutter on mock-up photos (edit-video pack, Apache-2.0), kept quiet
import json, subprocess, numpy as np, soundfile as sf, scipy.signal as ss
SR = 48000; Lt = json.load(open("layout.json")); TOTAL = Lt["total"]; N = int(TOTAL * SR); db = lambda g: 10 ** (g / 20)
vo = np.zeros(N)
for l in Lt["lines"]:
    if not l["file"]: continue
    a, sr = sf.read(l["file"]); a = a if a.ndim == 1 else a.mean(1); a = a[max(0, l["i0"] - int(0.02 * sr)):]
    a = ss.resample_poly(a, SR, sr); i = int(round(l["t0"] * SR)) - int(0.02 * SR); i = max(0, i); vo[i:i + len(a)] += a[:N - i]
sf.write("vo/vo_laid.wav", vo, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "vo/vo_laid.wav", "-af", "highpass=f=80,acompressor=threshold=-22dB:ratio=2.2:attack=8:release=150:makeup=2,loudnorm=I=-17:TP=-3:LRA=7",
                "-ar", str(SR), "-c:a", "pcm_f32le", "vo/vo_proc.wav"], check=True)
v, _ = sf.read("vo/vo_proc.wav"); v = np.pad(v, (0, max(0, N - len(v))))[:N]
m = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "music/mixkit_33_motivating_mornings.mp3", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).astype(np.float64).reshape(-1, 2)
m = m[int(1.0 * SR):]; xf = int(3.0 * SR); bed = m.copy()
while len(bed) < N:                                      # loop with a 3 s equal-power crossfade
    r = np.linspace(0, 1, xf)[:, None]; bed = np.concatenate([bed[:-xf], bed[-xf:] * np.cos(r * np.pi / 2) + m[:xf] * np.sin(r * np.pi / 2), m[xf:]])
bed = bed[:N]; bed[:int(1.5 * SR)] *= np.linspace(0, 1, int(1.5 * SR))[:, None]; fo = int(2.5 * SR); bed[-fo:] *= np.linspace(1, 0, fo)[:, None]
# ducking: music ~22 dB under the voice during speech, ~14 dB under it in the pauses
h = SR // 50; ve = np.array([np.sqrt(np.mean(v[i:i + h] ** 2)) for i in range(0, N, h)]); vdb = 20 * np.log10(np.percentile(ve[ve > 1e-4], 70))
me = np.sqrt(np.mean(bed ** 2)); mdb = 20 * np.log10(me + 1e-9)
act = np.convolve((20 * np.log10(ve + 1e-9) > vdb - 20).astype(float), np.ones(20), "same") > 0
g = np.repeat(np.where(act, db(vdb - 22 - mdb), db(vdb - 14 - mdb)), h)[:N]; g = np.pad(g, (0, N - len(g)), mode="edge")
g = np.convolve(g, np.ones(int(0.35 * SR)) / int(0.35 * SR), "same")
mix = v[:, None] + bed * g[:, None]
SFX = "/home/user/Video-Claude/.claude/skills/edit-video/assets/sfx/"; FX = {"tap": ("curated/ui-click.wav", -26), "shutter": ("curated/camera-shutter-light.wav", -22)}
for t, kind in Lt["cues"]:
    if kind not in FX: continue
    f, gain = FX[kind]; x, s2 = sf.read(SFX + f); x = x if x.ndim == 1 else x.mean(1); x = ss.resample_poly(x, SR, s2) if s2 != SR else x
    pk = int(np.argmax(np.abs(x))); i0 = int(round(t * SR)) - pk; x = x[max(0, -i0):] * db(gain); i0 = max(0, i0); k = min(len(x), N - i0); mix[i0:i0 + k] += x[:k, None]
mix *= min(1, 0.9 / np.abs(mix).max()); sf.write("project/assets/mix_pre.wav", mix, SR, subtype="PCM_24")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "project/assets/mix_pre.wav", "-af", "alimiter=limit=0.7:attack=3:release=60:level=false", "-ar", str(SR), "-c:a", "pcm_s24le", "project/assets/mix.wav"], check=True)
import os; os.remove("project/assets/mix_pre.wav")
print("mix", TOTAL, "s; voice ref", round(vdb, 1), "dBFS; music", round(mdb, 1), "dBFS before gain")
