# Intelligibility check for voice isolation: Whisper large-v3 (English pass, word probabilities) on the raw dialogue
# and on the DeepFilterNet versions. A drop in mean word probability would mean the isolation damaged the words.
import json, subprocess, numpy as np, sys
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8'); res = {}
for f in sys.argv[1:]:
    a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    for lang in ("en", "ta"):
        ss, _ = m.transcribe(a, language=lang, beam_size=5, word_timestamps=True, condition_on_previous_text=False)
        ss = list(ss); p = [w.probability for s in ss for w in s.words]
        res[f"{f}|{lang}"] = {"mean_p": round(float(np.mean(p)), 3), "words": len(p), "text": " ".join(s.text.strip() for s in ss)}
        print(f, lang, res[f"{f}|{lang}"]["mean_p"], len(p), "|", res[f"{f}|{lang}"]["text"][:160], flush=True)
json.dump(res, open("compare_voice.json", "w"), ensure_ascii=False, indent=1)
