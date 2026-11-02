# Tamil voice-over: phrase chunks (split on the quietest 0.2 s points), Tamil with a neutral Tanglish prompt + English
# translation + English transcription, word timestamps. -> transcript.json
import json, subprocess, numpy as np
from faster_whisper import WhisperModel
a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "proxy/src30.mov", "-af", "highpass=f=90,lowpass=7500", "-ac", "1", "-ar", "16000",
                                  "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
CH = [(0.0, 4.5), (4.3, 11.6), (11.4, 18.4), (18.2, 22.4), (22.2, 28.2), (28.0, 34.6)]
P = "Tamil with English words: customer, request, picture, design, statue, inch, colour, contact, bio."
out = []
for s, e in CH:
    seg = a[int(s * 16000):int(e * 16000)]; r = {"s": s, "e": e}
    for name, kw in [("ta", dict(language="ta", initial_prompt=P)), ("tr", dict(language="ta", task="translate")), ("en", dict(language="en"))]:
        ss, _ = m.transcribe(seg, beam_size=5, word_timestamps=True, condition_on_previous_text=False, temperature=0, **kw); ss = list(ss)
        r[name] = " ".join(x.text.strip() for x in ss)
        r[name + "_w"] = [[w.word, round(s + w.start, 2), round(s + w.end, 2)] for x in ss for w in x.words]
        print(f"{s:5.1f}-{e:5.1f} {name}: {r[name]}", flush=True)
    out.append(r)
json.dump(out, open("transcript.json", "w"), ensure_ascii=False, indent=1)
