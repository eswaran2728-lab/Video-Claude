import sys,json,subprocess,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel('large-v3',device='cpu',compute_type='int8')
out={}
for f in sys.argv[1:]:
    a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
    segs,info=m.transcribe(a,word_timestamps=True,vad_filter=True)
    segs=list(segs)
    out[f]={"language":info.language,"prob":info.language_probability,"segments":[{"start":s.start,"end":s.end,"text":s.text,"words":[{"w":w.word,"s":w.start,"e":w.end,"p":w.probability} for w in s.words]} for s in segs]}
    print("==",f,info.language,round(info.language_probability,2),flush=True)
    for s in segs: print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}",flush=True)
json.dump(out,open("transcript.json","w"),ensure_ascii=False,indent=1)
