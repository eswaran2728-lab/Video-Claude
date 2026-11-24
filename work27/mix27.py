# Audio: voice (Kokoro af_heart) + an original cheerful background track synthesized here (marimba-style plucks, warm bass,
# soft claps, 112 bpm, I–vi–IV–V in G; no third-party music), ducked under the voice + soft SFX (edit-video pack, Apache-2.0).
import os, json, subprocess, numpy as np, soundfile as sf, scipy.signal as ss
T = json.load(open("timing.json")); SR = 48000; L = int(round(T["total"] * SR)); db = lambda g: 10 ** (g / 20)
vo = np.zeros(L)
for sc in T["scenes"]:
    a, sr = sf.read(f"vo/{sc['id']}.wav"); a = ss.resample_poly(a, SR, sr); i = int(round(sc["start"] * SR)); vo[i:i + len(a)] += a[:L - i]
sf.write("vo/vo_full.wav", vo, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "vo/vo_full.wav", "-af",
                "highpass=f=80,equalizer=f=3200:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=120:makeup=2,alimiter=limit=0.8:level=false",
                "-ar", str(SR), "-c:a", "pcm_f32le", "vo/vo_proc.wav"], check=True)
v, _ = sf.read("vo/vo_proc.wav"); v = np.pad(v, (0, max(0, L - len(v))))[:L]
rng = np.random.default_rng(5); bpm = 112; beat = 60 / bpm; N = lambda m: 440 * 2 ** ((m - 69) / 12)
CH = [[43, 67, 71, 74], [40, 64, 67, 71], [36, 60, 64, 67], [38, 62, 66, 69]]          # G Em C D
mus = np.zeros((L, 2))
def mar(f, d):
    n = int(d * SR); t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 30)) * np.exp(-t * 7); x[:120] *= np.linspace(0, 1, 120); return x
def put(x, t0, g, pan=0):
    i = int(t0 * SR); e = min(L, i + len(x))
    if e > i: mus[i:e, 0] += x[:e - i] * g * (1 - max(0, pan)); mus[i:e, 1] += x[:e - i] * g * (1 + min(0, pan))
t = 0.0; bar = 0
pat = [0, 2, 1, 2, 3, 2, 1, 2]
while t < T["total"]:
    ch = CH[(bar // 2) % 4]
    for s8 in range(8):                                   # eighth-note marimba arpeggio
        m = ch[1 + pat[s8] % 3] + (12 if pat[s8] == 3 else 0); put(mar(N(m), .5), t + s8 * beat / 2, .16, (-.3, .3)[s8 % 2])
    for b in (0, 2.5):                                    # bass
        n = int(beat * 1.2 * SR); tt = np.arange(n) / SR; x = np.sin(2 * np.pi * N(ch[0]) * tt) * np.exp(-tt * 3.5); put(x, t + b * beat, .3)
    for b in (1, 3):                                      # soft clap
        n = int(.12 * SR); x = ss.sosfilt(ss.butter(2, [900, 4000], 'band', fs=SR, output='sos'), rng.standard_normal(n)) * np.exp(-np.arange(n) / SR * 35); put(x, t + b * beat, .07)
    t += 4 * beat; bar += 1
vr = np.sqrt(np.mean(v[np.abs(v) > .02] ** 2)); mus *= vr / np.sqrt(np.mean(mus ** 2)) * db(-19)
h = SR // 50; e = np.array([np.sqrt(np.mean(v[i:i + h] ** 2)) for i in range(0, L, h)])
act = np.convolve((20 * np.log10(e + 1e-9) > -40).astype(float), np.ones(16), "same") > 0
g = np.repeat(np.where(act, db(-8), db(0)), h)[:L]; g = np.pad(g, (0, L - len(g)), mode="edge"); g = np.convolve(g, np.ones(int(.35 * SR)) / int(.35 * SR), "same")
ta = np.arange(L) / SR; fade = np.minimum(1, np.minimum(ta / 1.0, (T["total"] - ta) / 2.0)); mus *= (g * fade)[:, None]
fx = np.zeros(L)
for c in json.load(open("video_" + os.environ.get("ORIENT","h") + "/cues.json"))["cues"]:
    x, s2 = sf.read("sfx/" + c["sfx"]); x = x if x.ndim == 1 else x.mean(1)
    if s2 != SR: x = ss.resample_poly(x, SR, s2)
    pk = int(np.argmax(np.abs(x))); i0 = int(round(c["t"] * SR)) - pk; x = x[max(0, -i0):] * db(c["gain_db"] - 4); i0 = max(0, i0)
    n = min(len(x), L - i0)
    if n > 0: fx[i0:i0 + n] += x[:n]
mix = v[:, None] + mus + fx[:, None]; pk = np.abs(mix).max(); mix *= min(1, .89 / pk)
sf.write(f"video_{os.environ.get('ORIENT','h')}/assets/mix.wav", mix, SR, subtype="PCM_24"); print("mix", T["total"], "peak", round(pk, 3))
