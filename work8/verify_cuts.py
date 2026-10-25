# Transcribe each EDL piece (cleaned audio) with word timestamps: no clipped first/last words, right sentence.
import json, subprocess, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
exec(open("edl.py").read())
m = WhisperModel('large-v3', device='cpu', compute_type='int8'); res = []
for i, (o0, o1, clip, a, b) in enumerate(OUT):
    x, sr = sf.read(f"edit/assets/clean_{clip}.wav"); x = x[int(a * sr):int(b * sr)]
    x = np.interp(np.arange(0, len(x), 3), np.arange(len(x)), x).astype(np.float32)   # 48k -> 16k
    r = {"i": i, "clip": clip, "a": a, "b": b}
    for k, mode in (("en", dict(language="en")), ("ta", dict(language="ta"))):
        segs, _ = m.transcribe(x, beam_size=5, word_timestamps=True, condition_on_previous_text=False, **mode)
        r[k] = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
    res.append(r)
    print(i, clip, a, b, "\n EN", " ".join(f"{w}[{s}]" for w, s, e in r["en"]), "\n TA", " ".join(f"{w}[{s}-{e}]" for w, s, e in r["ta"]), flush=True)
json.dump(res, open("verify_cuts.json", "w"), ensure_ascii=False, indent=1)
