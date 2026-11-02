# Finer passes on the isolated voice (src/vo_iso.wav): Tamil (no prompt, beam 8), Tamil->English, per phrase window.
import json, subprocess, numpy as np
from faster_whisper import WhisperModel
a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "src/vo_iso.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32)
m = WhisperModel('large-v3', device='cpu', compute_type='int8'); out = []
W = [(0.0, 4.0), (4.2, 11.2), (11.3, 15.2), (14.8, 18.4), (18.0, 21.6), (21.8, 25.0), (24.8, 28.4), (28.0, 31.0), (30.5, 34.6)]
for s, e in W:
    seg = a[int(s * 16000):int(e * 16000)]; r = {"s": s, "e": e}
    for name, kw in [("ta", dict(language="ta", beam_size=8)), ("tr", dict(language="ta", task="translate", beam_size=8))]:
        ss, _ = m.transcribe(seg, condition_on_previous_text=False, temperature=0, word_timestamps=True, **kw); ss = list(ss)
        r[name] = " ".join(x.text.strip() for x in ss); r[name + "_w"] = [[w.word, round(s + w.start, 2), round(s + w.end, 2)] for x in ss for w in x.words]
        print(f"{s:5.1f}-{e:5.1f} {name}: {r[name]}", flush=True)
    out.append(r)
json.dump(out, open("transcript_fine.json", "w"), ensure_ascii=False, indent=1)
