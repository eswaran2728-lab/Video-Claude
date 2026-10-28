# One more whole-clip Tamil pass with a Tanglish style prompt (no content words beyond those every pass agreed on), VAD on,
# plus overlapping 8 s windows. Used only to cross-check the reading in transcript_final.json.
import json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "proxy/src30.mov", "-af", "highpass=f=90,lowpass=f=7500",
                                  "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
P = "வணக்கம். Call பேசும்போது backgroundல noise இருக்கும். இந்த earbudsல noise cancelling இருக்கு. கீழே link click பண்ணுங்க."
res = {}
segs, _ = m.transcribe(a, language="ta", beam_size=5, vad_filter=True, initial_prompt=P, word_timestamps=True)
res["full_prompt"] = [{"s": s.start, "e": s.end, "t": s.text} for s in segs]
for s in res["full_prompt"]: print(f"{s['s']:6.2f}-{s['e']:6.2f} {s['t']}", flush=True)
res["win"] = []
for st in np.arange(0, 26, 3.0):
    seg = a[int(st * 16000):int(min(st + 8, 32.75) * 16000)]
    ss, _ = m.transcribe(seg, language="ta", beam_size=5, initial_prompt=P, condition_on_previous_text=False, temperature=0)
    t = " ".join(x.text.strip() for x in ss); res["win"].append({"s": float(st), "t": t}); print(f"win {st:4.1f}: {t}", flush=True)
json.dump(res, open("transcript_prompted.json", "w"), ensure_ascii=False, indent=1)
