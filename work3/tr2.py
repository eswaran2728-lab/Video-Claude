import json,numpy as np,re
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",compute_type="int8",cpu_threads=4)
a=np.frombuffer(open("main16k.wav","rb").read()[44:],np.int16).astype(np.float32)/32768
sil=[tuple(map(float,re.match(r"([\d.]+)-([\d.]+)",l).groups())) for l in open("sil.txt")]
# speech chunks between silences, merged to <=8s
pts=[0.0]+[x for s in sil for x in s]+[len(a)/16000];chunks=[]
for k in range(0,len(pts)-1,2):
    s,e=pts[k],pts[k+1]
    if e-s>0.25: chunks.append([s,e])
merged=[]
for c in chunks:
    if merged and c[1]-merged[-1][0]<8 and c[0]-merged[-1][1]<0.8: merged[-1][1]=c[1]
    else: merged.append(c)
res=[]
for s,e in merged:
    x=a[int(max(s-0.1,0)*16000):int((e+0.1)*16000)]
    _,_,lp=m.detect_language(x);top=sorted(lp,key=lambda z:-z[1])[:2]
    seg,_=m.transcribe(x,language="ta",word_timestamps=True,condition_on_previous_text=False,beam_size=5,temperature=0)
    seg=list(seg);txt=" ".join(z.text for z in seg)
    res.append({"s":s,"e":e,"text":txt,"lang":top,"words":[{"w":w.word,"s":w.start+s-0.1,"e":w.end+s-0.1} for z in seg for w in z.words]})
    print(f"[{s:6.2f}-{e:6.2f}] {[(l,round(p,2)) for l,p in top]} {txt}",flush=True)
json.dump(res,open("transcript2.json","w"),ensure_ascii=False)
