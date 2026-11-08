# Phrase-by-phrase passes (Tamil, Tamil->English, English) on pause-split chunks of both clips.
import json, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8'); out = {}
for k in ["main", "lights"]:
    a, sr = sf.read(f"analysis/src_{k}16k.wav", dtype="float32"); h = 1600
    r = np.array([20*np.log10(np.sqrt(np.mean(a[i:i+h]**2))+1e-9) for i in range(0, len(a)-h, h)])
    quiet = r < -28.5; chunks = []; s = None; q = 0
    for i, v in enumerate(quiet):
        if not v:
            if s is None: s = i
            q = 0
        else:
            q += 1
            if s is not None and q >= 3: chunks.append((s, i-q+1)); s = None
    if s is not None: chunks.append((s, len(r)))
    # merge chunks shorter than 1.2 s into neighbours
    merged = []
    for c in chunks:
        if merged and (c[0]-merged[-1][1] < 4 or c[1]-c[0] < 8): merged[-1] = (merged[-1][0], c[1])
        else: merged.append(c)
    res = []
    for cs, ce in merged:
        s0, e0 = max(0, cs/10-0.15), min(len(a)/sr, ce/10+0.15); seg = a[int(s0*sr):int(e0*sr)]; rr = {"s": round(s0,2), "e": round(e0,2)}
        for name, kw in [("ta", dict(language="ta")), ("tr", dict(language="ta", task="translate")), ("en", dict(language="en"))]:
            ss, _ = m.transcribe(seg, condition_on_previous_text=False, temperature=0, beam_size=8, word_timestamps=True, **kw); ss = list(ss)
            rr[name] = " ".join(x.text.strip() for x in ss)
            rr[name+"_w"] = [[w.word, round(s0+w.start, 2), round(s0+w.end, 2)] for x in ss for w in x.words]
        print(f"{k} {s0:5.2f}-{e0:5.2f} | ta: {rr['ta']} | tr: {rr['tr']} | en: {rr['en']}", flush=True)
        res.append(rr)
    out[k] = res
json.dump(out, open("analysis/transcript_fine.json", "w"), ensure_ascii=False, indent=1)
