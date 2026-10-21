import json, numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",compute_type="int8",cpu_threads=8)
a=np.frombuffer(open("audio.wav","rb").read()[44:],np.int16).astype(np.float32)/32768
segs,info=m.transcribe(a,word_timestamps=True,vad_filter=True,condition_on_previous_text=False,beam_size=5)
out=[{"start":s.start,"end":s.end,"text":s.text,"words":[{"w":w.word,"s":w.start,"e":w.end} for w in s.words]} for s in segs]
json.dump(out,open("transcript.json","w"),ensure_ascii=False)
print(info.language)
for s in out: print(f"[{s['start']:6.1f}-{s['end']:6.1f}] {s['text']}")
