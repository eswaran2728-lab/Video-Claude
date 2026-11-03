# Check the clips' sound for speech worth keeping (faster-whisper large-v3, int8 CPU). -> transcripts.json
import json, glob, os, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8"); out = {}
for f in sorted(glob.glob("proxy/*.mp4")):
    a = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
    segs, info = m.transcribe(a, vad_filter=True, beam_size=5)
    out[os.path.basename(f)] = dict(lang=info.language, p=round(info.language_probability, 2),
                                    segs=[dict(a=round(s.start, 2), b=round(s.end, 2), t=s.text.strip(), nsp=round(s.no_speech_prob, 2)) for s in segs])
    print(f, info.language, [(s["a"], s["t"]) for s in out[os.path.basename(f)]["segs"]], flush=True)
json.dump(out, open("transcripts.json", "w"), indent=1, ensure_ascii=False)
