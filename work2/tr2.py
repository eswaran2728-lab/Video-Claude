import json,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",compute_type="int8",cpu_threads=4)
a=np.frombuffer(open("cut.wav","rb").read()[44:],np.int16).astype(np.float32)/32768
edl=json.load(open("edl.json"));res=[]
for i,(s,e,t) in enumerate(edl):
    d=e-s;chunk=a[int(t*16000):int((t+d)*16000)]
    lang,prob,allp=m.detect_language(chunk)
    top=sorted(allp,key=lambda x:-x[1])[:3]
    segs,_=m.transcribe(chunk,language="ta",word_timestamps=True,condition_on_previous_text=False,beam_size=5,
        initial_prompt="Mayana Kaali Amman statue, Eshan Creations. Malaysian Tamil, konjam English.")
    segs=list(segs)
    txt=" ".join(x.text for x in segs)
    res.append({"i":i,"t":t,"d":d,"lang":top,"text":txt,"words":[{"w":w.word,"s":w.start+t,"e":w.end+t} for x in segs for w in x.words]})
    print(i,round(t,2),[(l,round(p,2)) for l,p in top],txt,flush=True)
json.dump(res,open("tr2.json","w"),ensure_ascii=False)
