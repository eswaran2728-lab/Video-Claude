# Re-transcribe the edited dialogue (output timeline) to check the cut lost no words. -> verify_cut.json
import json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "edit/assets/dialogue.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32)
res = {}
for name, kw in [("ta", dict(language="ta")), ("en", dict(language="en")), ("cut_ta", dict(language="ta", clip=(14.4, 18.6)))]:
    seg = a if "clip" not in kw else a[int(kw["clip"][0] * 16000):int(kw.pop("clip")[1] * 16000)]
    ss, _ = m.transcribe(seg, beam_size=5, vad_filter=name != "cut_ta", word_timestamps=True, condition_on_previous_text=False, **kw)
    res[name] = [{"s": s.start, "e": s.end, "t": s.text, "w": [[w.word, round(w.start, 2), round(w.end, 2)] for w in s.words]} for s in ss]
    print("==", name); [print(f"{s['s']:6.2f}-{s['e']:6.2f} {s['t']}") for s in res[name]]
json.dump(res, open("verify_cut.json", "w"), ensure_ascii=False, indent=1)
