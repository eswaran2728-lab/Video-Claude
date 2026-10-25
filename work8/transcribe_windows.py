# Sentence-window check for the pair statements in b5ae (Whisper repeated one sentence across 13-25 s on the full take).
# Each window is transcribed alone; Tamil with a code-mixed prompt, plus English and Tamil->English. -> windows.json
import json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8'); SR = 16000
P = "Quality, cheap, fast. இந்த மூன்றில இரண்டு தான் choose பண்ண முடியும். Quality-ஆ cheap-ஆ கிடைக்கிற பொருள் fast-ஆ கிடைக்காது."
W = {"b5ae": [(0.4, 3.8), (4.0, 7.75), (7.6, 13.0), (13.5, 18.3), (18.4, 24.6), (24.4, 27.6), (27.5, 34.3), (34.3, 45.6), (46.3, 50.9), (51.0, 53.6), (53.6, 60.0)],
     "e5dd": [(0, 3.1), (3.0, 4.3), (4.1, 6.7), (6.6, 8.8), (8.7, 10.8), (10.7, 14.2), (14.0, 14.85)],
     "d67f": [(0, 2.5), (2.4, 7.7), (7.6, 11.8), (11.7, 16.9)],
     "a336": [(0.9, 2.8), (2.7, 7.7), (7.6, 11.1), (11.9, 16.3), (16.2, 18.4)]}
res = {}
for n, wins in W.items():
    a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f"proxy/{n}.mp4", "-af", "highpass=f=90,lowpass=f=7500", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    res[n] = []
    for s, e in wins:
        x = a[int(s * SR):int(e * SR)]; r = {"s": s, "e": e}
        for key, mode in (("ta", dict(language="ta", initial_prompt=P)), ("en", dict(language="en")), ("tr", dict(language="ta", task="translate"))):
            segs, _ = m.transcribe(x, beam_size=5, condition_on_previous_text=False, vad_filter=False, **mode)
            r[key] = " ".join(t.text.strip() for t in segs)
        res[n].append(r); print(f"{n} {s:5.1f}-{e:5.1f}\n  TA {r['ta']}\n  EN {r['en']}\n  TR {r['tr']}", flush=True)
json.dump(res, open("windows.json", "w"), ensure_ascii=False, indent=1)
