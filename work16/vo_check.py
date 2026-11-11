# Check the AI voice against the script: transcribe each line clip (faster-whisper small) and score word overlap.
import json, re, glob, numpy as np, soundfile as sf, scipy.signal as ss
from faster_whisper import WhisperModel
from script16 import SCENES
m = WhisperModel("small", device="cpu", compute_type="int8"); T = json.load(open("timing.json")); out = []
norm = lambda s: re.findall(r"[a-z0-9]+", s.lower().replace("check-in", "checkin").replace("check-out", "checkout").replace("check in", "checkin").replace("check out", "checkout"))
for sc in T["scenes"]:
    for r in sc["lines"]:
        if r.get("silent"): continue
        p = f"vo/lines/{sc['id']}_{r['i']:02d}.wav"; a, sr = sf.read(p)
        a = ss.resample_poly(a, 16000, sr).astype(np.float32)
        segs, _ = m.transcribe(a, language="en", beam_size=5); hyp = " ".join(s.text for s in segs).strip()
        spoken = open(p + ".txt").read().split("|", 2)[2]
        ref, h = norm(spoken), norm(hyp); hit = sum(1 for w in ref if w in h) / max(1, len(ref))
        out.append(dict(line=f"{sc['id']}_{r['i']:02d}", spoken=spoken, heard=hyp, match=round(hit, 2)))
json.dump(out, open("vo_check.json", "w"), indent=1, ensure_ascii=False)
bad = [o for o in out if o["match"] < 0.85]
print(len(out), "lines;", len(bad), "below 0.85")
for o in bad: print(o["line"], o["match"], "|", o["spoken"], "| HEARD:", o["heard"])
