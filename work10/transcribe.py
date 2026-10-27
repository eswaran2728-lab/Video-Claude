# Whisper large-v3 over every video's audio: language auto-detect + English + Tamil->English. -> transcript.json
import json, subprocess, sys, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8'); res = {}
for name, path in [("IMG_6421", "proxy/IMG_6421.mov"), ("IMG_6425", "proxy/IMG_6425.mov"), ("dc95", "src/dl/dc95.mp4"), ("b048", "src/dl/b048.mp4")]:
    a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    rms = 20 * np.log10(np.sqrt((a ** 2).mean()) + 1e-9)
    for mode in [dict(), dict(language="en"), dict(language="ta", task="translate")]:
        segs, info = m.transcribe(a, beam_size=5, vad_filter=True, word_timestamps=True, condition_on_previous_text=False, **mode)
        segs = list(segs); k = f"{name}|{mode.get('language', 'auto')}|{mode.get('task', 'transcribe')}"
        res[k] = {"lang": info.language, "p": round(info.language_probability, 2), "rms_db": round(float(rms), 1),
                  "segments": [{"s": round(s.start, 2), "e": round(s.end, 2), "t": s.text, "nsp": round(s.no_speech_prob, 2)} for s in segs]}
        print("==", k, info.language, round(info.language_probability, 2), "rms", round(float(rms), 1), flush=True)
        for s in segs: print(f"  {s.start:6.2f}-{s.end:6.2f} nsp={s.no_speech_prob:.2f} {s.text}", flush=True)
json.dump(res, open("transcript.json", "w"), ensure_ascii=False, indent=1)
