import numpy as np,sys
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",compute_type="int8",cpu_threads=4)
a=np.frombuffer(open("main16k.wav","rb").read()[44:],np.int16).astype(np.float32)/32768
for s,e in [(26.5,38.0),(37.5,48.5),(48.0,60.5)]:
    x=a[int(s*16000):int(e*16000)]
    seg,_=m.transcribe(x,language="ta",word_timestamps=True,condition_on_previous_text=False,beam_size=5,temperature=0,vad_filter=False)
    print(f"== {s}-{e}")
    for z in seg: print(" | ".join(f"{w.word.strip()}@{w.start+s:.2f}" for w in z.words),flush=True)
