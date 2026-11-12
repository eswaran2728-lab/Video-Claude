# Audio: the two clips' own sound (songs) at full length, each normalised to -14 LUFS; the AI voice on the three MG parts;
# music "What About Action?" (Diego Nava, Mixkit #474, Mixkit Stock Music Free License) only under the MG parts, ducked under
# the voice; SFX (edit-video pack, Apache-2.0) on reveals and wipes. -> edit/assets/mix.wav
import json, subprocess, numpy as np, soundfile as sf, scipy.signal as ss
C = json.load(open("edit/cues.json")); SR = 48000; L = int(round(C["total"] * SR)); db = lambda g: 10 ** (g / 20)
SFX = "/root/.claude/skills/edit-video/assets/sfx/"


def dec(path, ss_=0, t=None, af="anull"):
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", str(ss_)] + (["-t", str(t)] if t else []) + ["-i", path, "-af", af, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)


def lufs_gain(x, target=-14.0):
    sf.write("vo/_tmp.wav", x, SR, subtype="FLOAT")
    o = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", "vo/_tmp.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    i = float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1]); return db(target - i)


mix = np.zeros((L, 2))
def put(x, t0, fade_in=0.05, fade_out=0.3):
    x = x.copy(); fi, fo = int(fade_in * SR), int(fade_out * SR)
    if fi: x[:fi] *= np.linspace(0, 1, fi)[:, None]
    if fo: x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    i = int(round(t0 * SR)); n = min(len(x), L - i); mix[i:i + n] += x[:n]


o = dec("src/original_scene_2.44.44PM.mp4", 0, 17.4); put(o * lufs_gain(o), C["orig"][0], 0.08, 0.35)
r = dec("src/recreated_3.14.20PM.mp4"); r = r[: int((C["rec"][1] - C["rec"][0]) * SR)]; put(r * lufs_gain(r), C["rec"][0], 0.08, 0.5)
vo = np.zeros(L)
for part, t0 in C["vo"].items():
    a, sr = sf.read(f"vo/{part}.wav"); a = ss.resample_poly(a, SR, sr); i = int(round(t0 * SR)); vo[i:i + len(a)] += a[:L - i]
sf.write("vo/vo_full.wav", vo, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "vo/vo_full.wav", "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=120:makeup=2,alimiter=limit=0.8:level=false",
                "-ar", str(SR), "-c:a", "pcm_f32le", "vo/vo_proc.wav"], check=True)
v, _ = sf.read("vo/vo_proc.wav"); v = np.pad(v, (0, max(0, L - len(v))))[:L]; v *= lufs_gain(np.stack([v, v], 1)[v != 0].reshape(-1, 2) if (v != 0).any() else np.zeros((10, 2)), -14)
mus = dec("music/mixkit_474_what_about_action.mp3")
h = SR // 50; e = np.array([np.sqrt(np.mean(v[i:i + h] ** 2)) for i in range(0, L, h)])
act = np.convolve((20 * np.log10(e + 1e-9) > -42).astype(float), np.ones(20), "same") > 0
g = np.repeat(np.where(act, db(-22), db(-12)), h)[:L]; g = np.pad(g, (0, L - len(g)), mode="edge"); g = np.convolve(g, np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
off = 0.0
for sec in ("intro", "mid", "cta"):
    a, b = C[sec]; n = int((b - a) * SR); seg = mus[int(off * SR): int(off * SR) + n]; off += (b - a)
    seg = seg * g[int(a * SR): int(a * SR) + len(seg), None]; put(seg, a, 0.15, 0.6 if sec != "cta" else 1.2)
mix += v[:, None]
fx = np.zeros(L)
for c in C["cues"]:
    x, s2 = sf.read(SFX + c["sfx"]); x = x if x.ndim == 1 else x.mean(1)
    if s2 != SR: x = ss.resample_poly(x, SR, s2)
    pk = int(np.argmax(np.abs(x))); i0 = int(round(c["t"] * SR)) - pk; x = x[max(0, -i0):] * db(c["gain_db"]); i0 = max(0, i0); n = min(len(x), L - i0); fx[i0:i0 + n] += x[:n]
mix += fx[:, None]; pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
sf.write("edit/assets/mix.wav", mix, SR, subtype="PCM_24"); print("mix", C["total"], "peak", round(pk, 3))
