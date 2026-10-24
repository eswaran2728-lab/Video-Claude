import numpy as np,subprocess
from faster_whisper import WhisperModel
m=WhisperModel("small",compute_type="int8",cpu_threads=4)
for v in ["v176","v185","v186","v201","v203"]:
    raw=subprocess.run(["ffmpeg","-v","error","-i",f"src/{v}.mp4","-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    a=np.frombuffer(raw,np.int16).astype(np.float32)/32768
    segs,info=m.transcribe(a,vad_filter=True,condition_on_previous_text=False)
    segs=list(segs)
    print(f"== {v} lang={info.language} p={info.language_probability:.2f} segs={len(segs)}")
    for s in segs[:8]: print(f"  [{s.start:5.1f}-{s.end:5.1f}] {s.text[:90]}")
