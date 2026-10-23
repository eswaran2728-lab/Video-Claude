import json,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",compute_type="int8",cpu_threads=4)
a=np.frombuffer(open("main16k.wav","rb").read()[44:],np.int16).astype(np.float32)/32768
segs,info=m.transcribe(a,language="ta",word_timestamps=True,vad_filter=True,condition_on_previous_text=False,beam_size=5,
    initial_prompt="Okay guys, Mayana Kaali Amman statue, Eshan Creations. Malaysian Tamil, konjam English.")
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"w":w.word,"s":w.start,"e":w.end} for w in s.words]})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}",flush=True)
json.dump(out,open("transcript.json","w"),ensure_ascii=False)
