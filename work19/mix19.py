# (work19: same as work16/mix16.py) Audio for the training video: the AI voiceover (Kokoro af_heart, vo/sNN.wav laid end to end per timing.json), clear and
# centred; music only on the opening title and the closing cards ("Motivating Mornings", Ahjay Stelino, Mixkit #33,
# Mixkit Stock Music Free License), ducked under the voice; soft SFX (edit-video pack, Apache-2.0) on reveals from edit/cues.json.
# -> edit/assets/mix.wav (48 kHz stereo)
import json, subprocess, numpy as np, soundfile as sf, scipy.signal as ss
T = json.load(open("timing.json")); SR = 48000; L = int(round(T["total"] * SR)); db = lambda g: 10 ** (g / 20)
SFX = "/root/.claude/skills/edit-video/assets/sfx/"
vo = np.zeros(L)
for sc in T["scenes"]:
    a, sr = sf.read(f"vo/{sc['id']}.wav"); a = ss.resample_poly(a, SR, sr); i = int(round(sc["start"] * SR)); vo[i:i + len(a)] += a[:L - i]
sf.write("vo/vo_full.wav", vo, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "vo/vo_full.wav", "-af",
                "highpass=f=70,equalizer=f=3500:t=q:w=1.2:g=1.5,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=120:makeup=2,alimiter=limit=0.8:level=false",
                "-ar", str(SR), "-c:a", "pcm_f32le", "vo/vo_proc.wav"], check=True)
v, _ = sf.read("vo/vo_proc.wav"); v = np.pad(v, (0, max(0, L - len(v))))[:L]
mus_src = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "music/mixkit_33_motivating_mornings.mp3", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                                       capture_output=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)
mus = np.zeros((L, 2)); S = {s["id"]: s for s in T["scenes"]}
cue = lambda sid, i: S[sid]["start"] + S[sid]["lines"][i]["t0"]


def place(t0, t1, src_off, fin, fout):
    i0, i1 = int(t0 * SR), min(L, int(t1 * SR)); x = mus_src[int(src_off * SR): int(src_off * SR) + (i1 - i0)].copy()
    n = len(x); f1, f2 = int(fin * SR), int(fout * SR); x[:f1] *= np.linspace(0, 1, f1)[:, None]; x[-f2:] *= np.linspace(1, 0, f2)[:, None]; mus[i0:i0 + n] += x


place(0.0, cue("s01", 2) + 1.0, 0.0, 0.8, 3.0)                                          # opening title card
place(cue("s30", 6) - 1.0, T["total"], 20.0, 1.5, 3.0)                                   # practise / closing card
h = SR // 50; e = np.array([np.sqrt(np.mean(v[i:i + h] ** 2)) for i in range(0, L, h)])   # duck under the voice
act = np.convolve((20 * np.log10(e + 1e-9) > -42).astype(float), np.ones(25), "same") > 0
g = np.repeat(np.where(act, db(-24), db(-12)), h)[:L]; g = np.pad(g, (0, L - len(g)), mode="edge")
g = np.convolve(g, np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
fx = np.zeros(L)
for c in json.load(open("edit/cues.json"))["cues"]:
    x, s2 = sf.read(SFX + c["sfx"]); x = x if x.ndim == 1 else x.mean(1)
    if s2 != SR: x = ss.resample_poly(x, SR, s2)
    pk = int(np.argmax(np.abs(x))); i0 = int(round(c["t"] * SR)) - pk; x = x[max(0, -i0):] * db(c["gain_db"] - 4); i0 = max(0, i0)
    n = min(len(x), L - i0); fx[i0:i0 + n] += x[:n]
mix = v[:, None] + mus * g[:, None] + fx[:, None]; pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
sf.write("edit/assets/mix.wav", mix, SR, subtype="PCM_24"); print("mix", T["total"], "peak", round(pk, 3))
# work19: the voice-heavy mix sits at about -16.7 LUFS with transient peaks; a gentle limiter (-4.5 dBFS ceiling) lets the
# master's +2.7 dB loudness gain land at -14 LUFS with the true peak under -1.5 dBTP.
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "edit/assets/mix.wav", "-af", "alimiter=limit=0.595:attack=3:release=60:level=false",
                "-ar", str(SR), "-c:a", "pcm_s24le", "vo/mix_lim.wav"], check=True)
import shutil; shutil.move("vo/mix_lim.wav", "edit/assets/mix.wav"); print("limited")
