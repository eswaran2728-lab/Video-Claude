import cv2,numpy as np,os
from scipy.ndimage import median_filter
N=2510;os.makedirs("masks2",exist_ok=True)
def sharp(m,lo,hi): return np.clip((m-lo)/(hi-lo),0,1)
import json
FT={int(k):v for k,v in json.load(open("facetrack.json")).items()}
def EX(i):
    ex=np.ones((1280,720),np.float32);ex[370:900,0:140]=0
    return ex
def EXI(i):
    ex=EX(i)
    return ex
def isnet_keep(a,h,i):
    b=(a>0.3).astype(np.uint8);hb=cv2.dilate((h>0.5).astype(np.uint8),np.ones((9,9),np.uint8))
    n,lab=cv2.connectedComponents(b)
    keep=np.zeros_like(b)
    hit=set(np.unique(lab[hb>0]).tolist())
    if i in FT:
        cx,cy,_=FT[i];hit.add(int(lab[min(int(cy),1279),min(int(cx),719)]))
    hit.discard(0)
    for l in hit: keep[lab==l]=1
    keep=cv2.dilate(keep,np.ones((5,5),np.uint8))
    return a*keep*EXI(i)
M=[];cov=[]
for i in range(N):
    a=cv2.imread(f"masks/{i:05d}.png",0).astype(np.float32)/255
    h=cv2.imread(f"hmasks/{i:05d}.png",0).astype(np.float32)/255
    m=np.maximum(sharp(isnet_keep(a,h,i),0.12,0.45),sharp(h*EX(i),0.15,0.4))
    small=cv2.resize(m,(180,320),interpolation=cv2.INTER_AREA)
    M.append(small);cov.append(float((m>0.5).mean()))
cov=np.array(cov);med=median_filter(cov,31)
bad=set(np.where(cov<med*0.9)[0].tolist())
bad|={b+d for b in list(bad) for d in (-1,1) if 0<=b+d<N}
good=[i for i in range(N) if i not in bad]
print("bad",len(bad))
import bisect
for i in range(N):
    a=cv2.imread(f"masks/{i:05d}.png",0).astype(np.float32)/255
    h=cv2.imread(f"hmasks/{i:05d}.png",0).astype(np.float32)/255
    m=np.maximum(sharp(isnet_keep(a,h,i),0.12,0.45),sharp(h*EX(i),0.15,0.4))
    if i in bad:
        k=bisect.bisect_left(good,i);p=good[max(k-1,0)];n=good[min(k,len(good)-1)]
        for j in (p,n):
            if abs(j-i)<=8:
                aj=cv2.imread(f"masks/{j:05d}.png",0).astype(np.float32)/255
                hj=cv2.imread(f"hmasks/{j:05d}.png",0).astype(np.float32)/255;m=np.maximum(m,sharp(isnet_keep(aj,hj,j),0.12,0.45))
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    cv2.imwrite(f"masks2/{i:05d}.png",(m*255).astype(np.uint8))
print("done")
