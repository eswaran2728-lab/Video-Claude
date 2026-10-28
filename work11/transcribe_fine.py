# Finer passes on the lines the chunk pass left uncertain: Tamil (with/without prompt, beam 8) and Tamil->English translation.
import json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "proxy/src30.mov", "-af", "highpass=f=90,lowpass=f=7500",
                                  "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
CH = [(0.0, 2.9), (2.7, 4.95), (4.95, 7.5), (7.4, 12.1), (12.1, 15.85), (13.4, 15.9), (21.1, 25.25), (24.3, 27.5), (27.4, 29.8), (25.25, 29.7), (29.7, 32.75), (30.0, 32.75)]
P = "Tanglish: Tamil with English words like call, noise, background, disturbance, office, car, earbuds, TikTok, noise cancelling, microphones, clear, link, click, purchase."
out = []
for s, e in CH:
    seg = a[int(s * 16000):int(e * 16000)]; r = {"start": s, "end": e}
    for name, kw in [("ta_b8", dict(language="ta", beam_size=8)), ("ta_p", dict(language="ta", beam_size=8, initial_prompt=P)),
                     ("tr", dict(language="ta", task="translate", beam_size=8))]:
        segs, _ = m.transcribe(seg, condition_on_previous_text=False, temperature=0, **kw)
        r[name] = " ".join(x.text.strip() for x in segs); print(f"{s:5.2f}-{e:5.2f} {name:6s} {r[name]}", flush=True)
    out.append(r)
json.dump(out, open("transcript_fine.json", "w"), ensure_ascii=False, indent=1)
