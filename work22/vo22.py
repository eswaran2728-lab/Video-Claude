# Narration: one HyperFrames TTS clip (Kokoro-82M, af_heart) per line -> vo/lines/<scene>_<n>.wav; word times (faster-whisper) -> timing.json.
# Lines are cached by text; an empty line is a silent beat.
import json, os, re, subprocess, soundfile as sf, numpy as np
import plan22 as P
from faster_whisper import WhisperModel
SAY = [(r"\bRevLog\b", "Rev Log"), (r"\bQR\b", "Q R"), (r"6-digit", "six digit"), (r"\bgeran\b", "guh-rahn")]
def spoken(t):
    for a, b in SAY: t = re.sub(a, b, t)
    return t
os.makedirs("vo/lines", exist_ok=True); WM = WhisperModel("small", device="cpu", compute_type="int8"); out = []
for sc in P.S:
    for n, ln in enumerate(sc["lines"]):
        rec = dict(scene=sc["id"], n=n, text=ln["text"])
        if ln["text"]:
            p = f"vo/lines/{sc['id']}_{n}.wav"; key = f"{P.VOICE}|{P.SPEED}|{spoken(ln['text'])}"
            if not (os.path.exists(p) and os.path.exists(p + ".key") and open(p + ".key").read() == key):
                r = subprocess.run(["npx", "--yes", "hyperframes@0.8.193", "tts", spoken(ln["text"]), "-v", P.VOICE, "-s", str(P.SPEED), "-o", p, "--json"], capture_output=True, text=True)
                assert '"ok":true' in r.stdout, r.stdout + r.stderr
                open(p + ".key", "w").write(key)
            a, sr = sf.read(p); a = a if a.ndim == 1 else a.mean(1)
            e = np.abs(a) > 0.004; i0 = int(np.argmax(e)); i1 = len(a) - int(np.argmax(e[::-1]))      # trim to speech
            rec.update(file=p, sr=sr, i0=i0, i1=i1, dur=round((i1 - i0) / sr, 3))
            import scipy.signal as ss
            seg = ss.resample_poly(a[i0:i1], 16000, sr).astype(np.float32)
            words = [dict(w=re.sub(r"[^\w']", "", w.word).lower(), t=round(w.start, 3), e=round(w.end, 3)) for s_ in WM.transcribe(seg, language="en", word_timestamps=True)[0] for w in s_.words]
            rec["words"] = words; rec["heard"] = " ".join(w["w"] for w in words)
        out.append(rec)
json.dump(out, open("timing.json", "w"), indent=1)
tot = sum(r.get("dur", 0) for r in out); nw = sum(len(r["text"].split()) for r in out)
print(len(out), "lines;", nw, "words;", round(tot, 1), "s of speech;", round(nw / tot * 60), "wpm")
