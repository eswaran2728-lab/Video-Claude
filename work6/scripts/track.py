# CSRT-track callout anchors over a source range of the upscaled footage; writes per-frame centres (source frame index -> x,y).
import cv2,json,sys
cap=cv2.VideoCapture("edit/src_1080.mp4")
T={"necklace":(400,750,110),"waist":(430,1000,120),"rock":(400,1500,130)}
f0,f1=int(5.0*30),int(9.2*30)
cap.set(cv2.CAP_PROP_POS_FRAMES,f0);ok,fr=cap.read()
trk={}
for k,(x,y,r) in T.items():
    t=cv2.TrackerCSRT_create();t.init(fr,(x-r//2,y-r//2,r,r));trk[k]=t
out={k:{f0:[x,y]} for k,(x,y,r) in T.items()}
for fi in range(f0+1,f1+1):
    ok,fr=cap.read()
    if not ok:break
    for k,t in trk.items():
        ok2,b=t.update(fr)
        if ok2: out[k][fi]=[b[0]+b[2]/2,b[1]+b[3]/2]
        else: out[k][fi]=out[k][fi-1]
# light smoothing
import numpy as np
res={}
for k,d in out.items():
    fs=sorted(d);a=np.array([d[i] for i in fs],float)
    ker=np.ones(5)/5
    sm=np.stack([np.convolve(np.pad(a[:,j],2,mode='edge'),ker,'valid') for j in range(2)],1)
    res[k]={str(f):[round(v[0],1),round(v[1],1)] for f,v in zip(fs,sm)}
json.dump(res,open("edit/track.json","w"))
for k in res: 
    ks=list(res[k]);print(k,res[k][ks[0]],res[k][ks[len(ks)//2]],res[k][ks[-1]])
