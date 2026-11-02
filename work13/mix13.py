# Audio for each part, on the ACTUAL frame timeline of the rendered plate (segments.json frame counts):
#  - clip sound: real-speed segments only; spoken lines at full level, everything else (stage music, crowd, hits) low under the
#    music; slow-motion segments are silent (their sound is the swish + boom on the impact frame)
#  - music: "Epical Drums 02" (Mixkit #677) for Part 1, its drop (56.5-57.8 s) on the hammer raise and the next hit (58.0)
#    on the brick impact; "Epical Drums 01" (Mixkit #676) for Part 2. Both Mixkit Stock Music Free License. Ducked under speech.
#  - SFX (edit-video pack): zoom-swish into each slow motion, sub-impact + hook-impact on each impact frame
# -> edit/assets/part{1,2}_mix.wav, edit/part{1,2}_audio.json (impact / line times for the graphics)
import json, subprocess, numpy as np, soundfile as sf
import plan13 as P
SR = 48000; SFX = "/root/.claude/skills/edit-video/assets/sfx/"
db = lambda g: 10 ** (g / 20)
SEG = json.load(open("segments.json"))
# speech lines kept loud: (clip, src_in, src_out)
LINES = [("v_215628", 0.6, 4.6), ("v_213143", 0.0, 2.0), ("v_213120", 1.0, 4.7), ("v_215631", 0.0, 1.5)]
IMPACTS = {"part1": [("v_215609", 33.95, "SMASH"), ("v_215613", 24.0, "UNBREAKABLE"), ("v_225624", 28.6, None), ("v_225554", 20.5, None)],
           "part2": [("v_225618", 19.45, "AGAIN"), ("v_225545", 8.5, "TAKEDOWN"), ("v_225554", 20.5, None)]}


def load(path, ss=0.0, dur=None):
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", str(ss)] + (["-t", str(dur)] if dur else []) + ["-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)


def sfx(name):
    a, sr = sf.read(SFX + name, always_2d=True); a = a if a.shape[1] == 2 else np.repeat(a, 2, 1); return a


def place(buf, clip, t, gain, align_peak=True):
    i0 = int(round(t * SR)) - (int(np.argmax(np.abs(clip).sum(1))) if align_peak else 0)
    c = clip[max(0, -i0):] * db(gain); i0 = max(0, i0); n = min(len(c), len(buf) - i0)
    if n > 0: buf[i0:i0 + n] += c[:n]


def mix(part):
    segs = SEG[part]["segments"]; N = sum(s["frames"] for s in segs); T = N / 30; L = int(round(T * SR))
    voice = np.zeros((L, 2)); amb = np.zeros((L, 2)); fx = np.zeros((L, 2)); speech = np.zeros(L, bool)
    t = 0.0; info = {"total": round(T, 3), "seg_starts": [], "impacts": [], "lines": []}
    for i, s in enumerate(segs):
        d = s["frames"] / 30; info["seg_starts"].append(round(t, 3))
        if s["speed"] == 1.0:
            a = load(f"src/norm/{s['clip']}.mp4", s["src_in"], d); F = int(0.012 * SR)
            a[:F] *= np.linspace(0, 1, F)[:, None]; a[-F:] *= np.linspace(1, 0, F)[:, None]
            line = next((l for l in LINES if l[0] == s["clip"] and abs(l[1] - s["src_in"]) < 0.05), None)
            i0 = int(t * SR); n = min(len(a), L - i0)
            if line:
                voice[i0:i0 + n] += a[:n] * db(4); speech[i0:i0 + n] = True; info["lines"].append({"clip": s["clip"], "start": round(t, 3), "end": round(t + d, 3)})
            else:
                amb[i0:i0 + n] += a[:n]
        else:
            place(fx, sfx("curated/zoom-swish.wav"), t + 0.05, -10)
        for clip, ti, word in IMPACTS[part]:
            if clip == s["clip"] and s["src_in"] - 1e-6 <= ti < s["src_out"] - 1e-6:
                to = t + (ti - s["src_in"]) / s["speed"]; info["impacts"].append({"clip": clip, "t": round(to, 3), "word": word, "seg": i})
                place(fx, sfx("sub-impact.wav"), to, -4); place(fx, sfx("curated/hook-impact.wav"), to, -6)
        t += d
    if part == "part1":                                   # "Ready?" laid on the first montage cut (J-cut)
        _, si, clip, a0, a1 = P.READY; tr = info["seg_starts"][si]; r = load(f"src/norm/{clip}.mp4", a0, a1 - a0)
        i0 = int(tr * SR); voice[i0:i0 + len(r)] += r * db(4); speech[i0:i0 + len(r)] = True; info["lines"].append({"clip": clip, "start": round(tr, 3), "end": round(tr + a1 - a0, 3)})
    # music
    if part == "part1":
        brick = next(x for x in info["impacts"] if x["clip"] == "v_215613")["t"]; m_start = info["seg_starts"][3]
        m0 = 58.0 - (brick - m_start); track = "music/mixkit_677_epical_drums_02.mp3"
    else:
        m_start = info["seg_starts"][3]; m0 = 2.0; track = "music/mixkit_676_epical_drums_01.mp3"
    mus = load(track, m0, T - m_start + 0.5); music = np.zeros((L, 2)); i0 = int(m_start * SR); n = min(len(mus), L - i0); music[i0:i0 + n] = mus[:n]
    F = int(0.15 * SR); music[i0:i0 + F] *= np.linspace(0, 1, F)[:, None]
    fo = int(1.2 * SR); music[-fo:] *= np.linspace(1, 0, fo)[:, None]
    # duck music under speech (-11 dB), smoothed
    g = np.where(speech, db(-11), 1.0); k = int(0.12 * SR); g = np.convolve(g, np.ones(k) / k, "same")
    out = voice + amb * db(-15) + music * db(-6) * g[:, None] + fx
    pk = np.abs(out).max(); out *= min(1.0, 0.89 / pk) if pk > 0 else 1
    sf.write(f"src/{part}_premix.wav", out, SR, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"src/{part}_premix.wav", "-af", "alimiter=limit=0.5:attack=3:release=80:level=false",
                    "-ar", str(SR), "-c:a", "pcm_s16le", f"edit/assets/{part}_mix.wav"], check=True)
    info.update(music={"track": track, "start_out": round(m_start, 3), "track_in": round(m0, 3)})
    json.dump(info, open(f"edit/{part}_audio.json", "w"), indent=1)
    print(part, "T", round(T, 2), "impacts", info["impacts"], "lines", info["lines"], "music", info["music"])


for p in ("part1", "part2"):
    mix(p)
