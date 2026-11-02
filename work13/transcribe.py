# Whisper large-v3 over every clip (auto language, VAD on, word timestamps) to find any usable speech (MC, team calls)
# and where the crowd/music is. -> transcripts.json  {clip: {lang, p, segments:[{s,e,t,nsp,lp}]}}
import json, glob, os, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8'); out = {}
if os.path.exists('transcripts.json'): out = json.load(open('transcripts.json'))
for f in sorted(glob.glob('src/norm/v_*.mp4')):
    n = os.path.basename(f)[:-4]
    if n in out: continue
    a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    if len(a) < 16000: out[n] = {"lang": None, "segments": []}; continue
    ss, info = m.transcribe(a, beam_size=5, vad_filter=True, condition_on_previous_text=False)
    out[n] = {"lang": info.language, "p": round(info.language_probability, 2),
              "segments": [{"s": round(s.start, 2), "e": round(s.end, 2), "t": s.text.strip(), "nsp": round(s.no_speech_prob, 2),
                            "lp": round(s.avg_logprob, 2)} for s in ss]}
    print(n, info.language, round(info.language_probability, 2), len(out[n]["segments"]), flush=True)
    json.dump(out, open('transcripts.json', 'w'), ensure_ascii=False, indent=1)
print("ALL_DONE", flush=True)
