# Audio for v01: the creator's voice cut to plan16 (from the original PCM for M, the MP4 for L), cleaned and level-matched;
# music "Love is Eternal" (Ahjay Stelino, Mixkit #37, Mixkit Stock Music Free License) ducked under speech, dipped
# before the lamp reveal and lifted on it, a beat placed on the reveal frame; SFX from the edit-video pack (Apache-2.0)
# with each transient on its event frame. → edit/assets/mix.wav (48 kHz stereo) + edit/cues.json
# v03 (VERSION>=v03): voice from DeepFilterNet3-isolated tracks (analysis/voice/*_df.wav, tools/voice_isolate.py) with a
# vocal EQ (de-mud, presence, air, de-ess); score "A New Life" (Eugenio Mininni, Mixkit #543, Mixkit Stock Music Free
# License) placed so its swell (24.62 s in the track) hits the lamp reveal, levels set against the voice; cinematic SFX
# (riser into the reveal, impacts, soft whooshes on the smooth camera moves, lights-off thock).
import json, subprocess, numpy as np, soundfile as sf
import plan16 as P
SR = 48000; L = int(round(P.TOTAL * SR)); SFX = "../.claude/skills/edit-video/assets/sfx/"
db = lambda g: 10 ** (g / 20)

def dec(path, ss=None, t=None, stream="0:a:0"):
    cmd = ["ffmpeg", "-nostdin", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + ["-i", path, "-map", stream] + \
          (["-t", str(t)] if t else []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).astype(np.float64)

def clean(x):
    p = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                        "highpass=f=85,afftdn=nf=-32:nr=8,equalizer=f=3200:t=q:w=1.2:g=2", "-f", "f64le", "-"],
                       input=x.tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float64)

V3 = P.VERSION >= "v03"
def vocal(x):
    p = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                        "highpass=f=80,equalizer=f=250:t=q:w=1.0:g=-2.5,equalizer=f=3500:t=q:w=1.0:g=2.5,highshelf=f=9000:g=1.5,"
                        "deesser=i=0.35", "-f", "f64le", "-"], input=x.tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float64)
if V3:
    RAW = {k: vocal(sf.read(f"analysis/voice/{k}_df.wav")[0].astype(np.float64)) for k in ("M", "L")}
else:
    RAW = {"M": clean(dec("src/drive/IMG_6792.MOV")), "L": clean(dec("src/drive/fa799ce5e58a49c29107dcd042ded275.mp4"))}
def speech_rms(x):
    h = SR // 50; e = np.array([np.sqrt(np.mean(x[i:i + h] ** 2)) for i in range(0, len(x) - h, h)]); return np.percentile(e, 80)
GAIN = {k: 0.06 / speech_rms(v) for k, v in RAW.items()}           # match the two microphones' speech level

vo = np.zeros(L); F = int(0.025 * SR)
for s in P.OUT:
    if not s["vo"]: continue
    src, a, b = (s["src"], s["a"], s["b"]) if s["vo"] is True else s["vo"]
    x = RAW[src][int(a * SR):int(b * SR)].copy() * GAIN[src]
    x[:F] *= np.linspace(0, 1, F); x[-F:] *= np.linspace(1, 0, F)
    i = int(round(s["o0"] * SR)); n = min(len(x), int(round(s["o1"] * SR)) - i); vo[i:i + n] += x[:n]
sf.write("seg/vo_cut.wav", vo, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "seg/vo_cut.wav", "-af",
                "acompressor=threshold=-24dB:ratio=3:attack=8:release=120:makeup=3,acompressor=threshold=-12dB:ratio=4:attack=3:release=80,"
                "alimiter=limit=0.70:level=false", "-ar", str(SR), "-c:a", "pcm_f32le", "seg/vo_proc.wav"], check=True)
v, _ = sf.read("seg/vo_proc.wav"); v = np.pad(v, (0, max(0, L - len(v))))[:L]

# --- music: choose the start offset so a strong beat lands on the reveal frame
R = P.out_t("reveal", P.REVEAL_SRC); R = int(round(R * P.FPS)) / P.FPS
MUSIC = "music/mixkit_543_a_new_life.mp3" if V3 else "music/mixkit_37_love_is_eternal.mp3"
full = dec(MUSIC)
n, hop = 2048, 512
spec = np.abs(np.array([np.fft.rfft(full[i:i + n] * np.hanning(n)) for i in range(0, len(full) - n, hop)]))
flux = np.maximum(0, np.diff(np.log1p(spec[:, :60]), axis=0)).sum(1)          # low-band onsets (kick/bass)
ons = (np.arange(len(flux)) + 1) * hop / SR
cand = [(flux[i], ons[i]) for i in range(1, len(flux) - 1) if flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1] and R + 1 < ons[i] < 60]
strength, t_on = max(cand)
if V3: t_on = 24.619                                                       # the score's swell (measured: −40 → −18 dB)
m0 = t_on - R
if m0 >= 0: mus = full[int(m0 * SR):int(m0 * SR) + L]
else:       mus = np.concatenate([np.zeros(int(-m0 * SR)), full])[:L]   # the score starts after the opening line
mus = np.pad(mus, (0, L - len(mus)))

h = SR // 50; e = np.array([np.sqrt(np.mean(v[i:i + h] ** 2)) for i in range(0, L, h)])
act = np.convolve((20 * np.log10(e + 1e-9) > -38).astype(float), np.ones(20), "same") > 0
gdb = np.where(act, -22.0, -13.0)                                         # under speech / in pauses
tt = np.arange(len(gdb)) * h / SR
pre0 = P.S["reveal"]["o0"]
gdb[(tt >= pre0) & (tt < R - 0.05)] = -27.0                               # quieter build while he turns the lamp
gdb[(tt >= R - 0.05) & (tt < P.S["glow"]["o1"])] = -8.0                   # lift on the lamp lighting up, through the glow hold
gdb[tt >= P.S["end"]["o0"]] = -9.0                                        # end card
if V3:   # set the score's level against the voice: ~13 dB under speech, forward on the reveal, glow and end card
    me = np.array([np.sqrt(np.mean(mus[max(0, i - SR // 2):i + SR // 2] ** 2)) for i in range(0, L, h)])
    mdb = 20 * np.log10(me + 1e-9)
    tgt = np.where(act, -33.0, -25.0)
    tgt[(tt >= pre0) & (tt < R - 0.05)] = -31.0                           # the score's own build under "hold the lamp, turn it"
    post = (tt >= R - 0.05) & (tt < P.S["glow"]["o1"])
    tgt[post] = np.where(act[post], -27.0, -15.0)                         # swell once his last word ("…on") has finished
    tgt[tt >= P.S["end"]["o0"]] = -16.0
    gdb = np.clip(tgt - mdb, -30, 8)
    gdb[tt < -m0] = 0
g = np.repeat(db(gdb), h)[:L]; k = int((0.35 if V3 else 0.12) * SR); g = np.convolve(g, np.ones(k) / k, "same")
mus = mus * g
fi = int(0.35 * SR); mus[:fi] *= np.linspace(0.3, 1, fi)
fo = int(1.6 * SR); mus[-fo:] *= np.linspace(1, 0, fo) ** 1.5

# --- SFX on their frames (transient = first point reaching half the peak)
fr = lambda t: int(round(t * P.FPS)) / P.FPS
CUES_V3 = [(0.0, "sparkle.wav", -18, "hook title lands"),
        (P.S["story"]["o0"], "thock.wav", -9, "lights-off dip into the unlit frame"),
        (P.out_t("story", 11.575), "curated/zoom-swish.wav", -19, "ease back: 'just a frame' (peak mid-move)"),
        (P.out_t("story", 15.03), "curated/zoom-swish.wav", -19, "ease in to the faces (peak mid-move)"),
        (P.out_t("story", 18.70), "curated/zoom-swish.wav", -19, "ease out as the frame is lowered"),
        (P.out_t("story", 19.65), "curated/zoom-swish.wav", -16, "push in to the key hooks (peak mid-move)"),
        (P.S["howto"]["o0"] + 0.12, "curated/zoom-swish.wav", -16, "light-leak transition to the lamp question"),
        (R, "curated/metallic-riser.wav", -20, "riser peaks on the reveal"),
        (R, "shimmer.wav", -12, "lamp lights up (peak)"),
        (R, "sub-impact.wav", -13, "lamp lights up"),
        (P.S["end"]["o0"], "curated/hook-impact.wav", -15, "letterbox bars close for the end card")]
CUES = CUES_V3 if V3 else [(0.0, "sparkle.wav", -16, "hook title lands"),
        (P.S["story"]["o0"], "thock.wav", -11, "cut from lit flash-forward to the unlit frame"),
        (P.out_t("story", 11.34), "curated/camera-shutter-light.wav", -14, "punch out to wide: 'just a frame'"),
        (P.out_t("story", 14.72), "curated/camera-shutter-light.wav", -14, "punch in: initials / customer"),
        (P.out_t("story", 19.65), "curated/zoom-swish.wav", -15, "push in to the key hooks (peak mid-move)"),
        (P.S["howto"]["o0"], "curated/camera-shutter-light.wav", -14, "cut to the lamp question"),
        (R, "shimmer.wav", -9, "lamp lights up (peak)"),
        (R, "sub-impact.wav", -15, "lamp lights up")]
CUES = list(CUES)
CUES += [tuple(c) for c in json.load(open("edit/gfx_cues.json"))]   # graphics + end-card cues written by build16.py
try:
    tags = json.load(open("edit/hook_tags.json"))["pops"]
    CUES += [(t + 1 / P.FPS, "tick.wav", -13, f"key hook tag {i + 1}") for i, t in enumerate(tags)]   # tag first shows a frame after its pop starts
except FileNotFoundError:
    pass
fx = np.zeros(L); SWELL = {"shimmer.wav", "curated/zoom-swish.wav", "curated/metallic-riser.wav"}
for t, name, gain, _ in CUES:
    x, s2 = sf.read(SFX + name); x = x if x.ndim == 1 else x.mean(1); a = np.abs(x)
    sync = int(np.argmax(a)) if name in SWELL else int(np.argmax(a >= 0.5 * a.max()))
    i0 = int(round(fr(t) * SR)) - sync; x = x[max(0, -i0):] * db(gain); i0 = max(0, i0); m = min(len(x), L - i0); fx[i0:i0 + m] += x[:m]
mix = v + mus + fx; pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
sf.write("edit/assets/mix.wav", np.stack([mix, mix], 1), SR, subtype="PCM_24")
json.dump({"fps": P.FPS, "total": P.TOTAL, "version": P.VERSION, "music": {"file": MUSIC, "start_in_track": round(m0, 3),
           "beat_on_reveal": round(t_on, 3), "reveal_out": R},
           "cues": [{"t": round(fr(a), 3), "frame": int(round(a * P.FPS)), "sound": b, "gain_db": c, "label": d} for a, b, c, d in CUES]},
          open("edit/cues.json", "w"), indent=1)
print("mix", round(P.TOTAL, 3), "s; music from", round(m0, 2), "s; reveal", R, "; cues", len(CUES), "; gains", {k: round(20 * np.log10(g), 1) for k, g in GAIN.items()})
