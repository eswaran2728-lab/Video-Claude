# Whisper large-v3 over every clip: auto language detection, then forced English transcription and Tamil->English
# translation (the speaker mixes Tamil/English). Word timestamps kept for the EDL. -> transcript.json
import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
res = {}
for n in sys.argv[1:] or ["a336", "d67f", "e5dd", "b5ae"]:
    a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f"proxy/{n}.mp4", "-af", "highpass=f=90,lowpass=f=7500",
                                      "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    for mode in [dict(), dict(language="en", task="transcribe"), dict(language="ta", task="translate")]:
        segs, info = m.transcribe(a, word_timestamps=True, vad_filter=True, beam_size=5, condition_on_previous_text=False, **mode)
        segs = list(segs); k = f"{n}|{mode.get('language', 'auto')}|{mode.get('task', 'transcribe')}"
        res[k] = {"lang": info.language, "p": info.language_probability,
                  "segments": [{"start": s.start, "end": s.end, "text": s.text, "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in s.words]} for s in segs]}
        print("==", k, info.language, round(info.language_probability, 2), flush=True)
        for s in segs: print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}", flush=True)
json.dump(res, open("transcript.json", "w"), ensure_ascii=False, indent=1)
