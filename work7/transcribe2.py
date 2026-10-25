import sys,json,subprocess,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel('large-v3',device='cpu',compute_type='int8')
res={}
for f in ["proxy/IMG_6358.mp4","proxy/3437BABC.mp4"]:
    a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-af","highpass=f=90,lowpass=f=7000,afftdn=nf=-25","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
    for mode in [dict(language="en",task="transcribe"),dict(language="ta",task="translate")]:
        segs,info=m.transcribe(a,word_timestamps=True,vad_filter=True,beam_size=5,condition_on_previous_text=False,**mode)
        segs=list(segs);k=f"{f}|{mode['language']}|{mode['task']}"
        res[k]=[{"start":s.start,"end":s.end,"text":s.text,"words":[{"w":w.word,"s":w.start,"e":w.end,"p":w.probability} for w in s.words]} for s in segs]
        print("==",k,flush=True)
        for s in segs: print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}",flush=True)
json.dump(res,open("transcript2.json","w"),ensure_ascii=False,indent=1)
