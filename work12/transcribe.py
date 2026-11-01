# Whisper large-v3 over the WhatsApp clip: auto language + forced English / Malay / Tamil, word timestamps, VAD off (short
# clip, crowd audio). Only used to find out whether there is usable speech. -> transcript.json
import json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "proxy/vid30.mov", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32)
res = {}
for name, kw in [("auto", {}), ("en", dict(language="en")), ("ms", dict(language="ms")), ("ta", dict(language="ta"))]:
    ss, info = m.transcribe(a, beam_size=5, word_timestamps=True, condition_on_previous_text=False, vad_filter=False, **kw)
    ss = list(ss)
    res[name] = {"lang": info.language, "p": round(info.language_probability, 2),
                 "segments": [{"s": round(s.start, 2), "e": round(s.end, 2), "t": s.text, "no_speech": round(s.no_speech_prob, 2),
                               "avg_logprob": round(s.avg_logprob, 2)} for s in ss]}
    print("==", name, info.language, round(info.language_probability, 2), flush=True)
    for s in res[name]["segments"]: print(f"  {s['s']:5.2f}-{s['e']:5.2f} nsp={s['no_speech']} lp={s['avg_logprob']} {s['t']}", flush=True)
json.dump(res, open("transcript.json", "w"), ensure_ascii=False, indent=1)
