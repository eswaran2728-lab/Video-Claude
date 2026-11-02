# Word-level re-transcription of the spoken lines used in the edit (forced language per line). -> lines.json
import json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
L = [("v_213120", 0.0, 9.6, "ta"), ("v_213143", 0.0, 3.2, "ta"), ("v_215628", 0.0, 4.6, "en"), ("v_215631", 0.0, 1.5, "en"),
     ("v_215603", 0.0, 1.2, "en"), ("v_215647", 26.5, 42.3, "ta")]
out = {}
for c, a, b, lang in L:
    au = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", f"src/norm/{c}.mp4",
                                       "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    for task in (["transcribe", "translate"] if lang == "ta" else ["transcribe"]):
        ss, _ = m.transcribe(au, language=lang, task=task, beam_size=5, word_timestamps=True, condition_on_previous_text=False)
        ss = list(ss)
        out[f"{c}|{task}"] = [{"s": round(a + w.start, 2), "e": round(a + w.end, 2), "w": w.word, "p": round(w.probability, 2)} for s in ss for w in s.words]
        print(c, task, " ".join(f"{w['w'].strip()}[{w['s']}]" for w in out[f"{c}|{task}"]), flush=True)
json.dump(out, open("lines.json", "w"), ensure_ascii=False, indent=1)
