import cv2,numpy as np,json,os
N=2510;os.makedirs("masks3",exist_ok=True)
nf=[120,53,207,185,13,61,100,339,60,146,62,41,78,139,390,210,26,93,170,17]
seg=np.zeros(N,int);c=0
for k,n in enumerate(nf): seg[c:c+n]=k;c+=n
FT={int(k):v for k,v in json.load(open("facetrack.json")).items()}
held=lambda i:(i<=119) or (i>=1387)
EX=np.ones((1280,720),np.float32);EX[370:900,0:140]=0
_cap=cv2.VideoCapture("cut.mp4");_F={};_pos=[0]
# static background reference for the shelf-statue zone (camera is on a tripod), from talking frames with nothing in that zone
_rc=cv2.VideoCapture("cut.mp4");_refs=[];_k=0
while _k<=1385:
    _ok,_f=_rc.read()
    if _k>=1300 and _k%5==0: _refs.append(_f[340:900,110:235].astype(np.int16))
    _k+=1
REFZ=np.median(np.stack(_refs),0).astype(np.int16);_rc.release()
_h=cv2.cvtColor(REFZ.astype(np.uint8),cv2.COLOR_BGR2HSV)
_gold=(_h[...,0]>=10)&(_h[...,0]<=35)&(_h[...,1]>=70)&(_h[...,2]>=90)
_silver=(_h[...,1]<60)&(_h[...,2]>=120)
TZ=cv2.dilate((_gold|_silver).astype(np.uint8),np.ones((7,7),np.uint8))
def FR(i):
    if i in _F: return _F[i]
    if i<_pos[0]:
        _cap.release();_cap.open("cut.mp4");_pos[0]=0;_F.clear()
    while _pos[0]<=i:
        ok,f=_cap.read();_F[_pos[0]]=f;_pos[0]+=1
        if len(_F)>60: del _F[min(_F)]
    return _F[i]
def statue(i):
    if not held(i): return np.zeros((1280,720),np.float32)
    a=cv2.imread(f"bmasks/{i:05d}.png",0).astype(np.float32)/255
    b=(a>0.25).astype(np.uint8);n,lab=cv2.connectedComponents(b)
    cx,cy,_=FT[i];keep=np.zeros_like(b)
    # components touching a disk around the statue face, or large components overlapping the statue column
    disk=np.zeros_like(b);cv2.circle(disk,(int(cx),int(cy)),60,1,-1)
    for l in set(np.unique(lab[disk>0]).tolist())-{0}: keep[lab==l]=1
    keep=cv2.dilate(keep,np.ones((5,5),np.uint8))
    st=np.clip((a*keep*EX-0.1)/0.35,0,1)
    # shelf statue's silver trident (behind, left): drop low-saturation pixels in that zone; the held trident is gold
    sat=cv2.cvtColor(FR(i)[340:900,110:235],cv2.COLOR_BGR2HSV)[...,1]
    z=st[340:900,110:235];z[sat<80]=0
    diff=np.abs(FR(i)[340:900,110:235].astype(np.int16)-REFZ).max(-1)
    z[cv2.erode((diff<22).astype(np.uint8),np.ones((3,3),np.uint8))>0]=0
    z[(TZ>0)&(diff<45)]=0
    return st
from functools import lru_cache
@lru_cache(maxsize=40)
def S_(i): return statue(i)
class _S:
    def __getitem__(self,i): return S_(i)
S=_S()
cov=np.array([float(statue(i)[::4,::4].mean()) for i in range(N)])
print("cov done",flush=True)
out_prev=None
for i in range(N):
    p=cv2.imread(f"rvm/{i:05d}.png",0).astype(np.float32)/255
    s=S[i]
    if held(i):
        nb=[j for j in (i-1,i+1) if 0<=j<N and seg[j]==seg[i] and held(j)]
        if len(nb)==2: s=np.median(np.stack([S[nb[0]],s,S[nb[1]]]),0)
        # long dropout: borrow from nearest strong frame in same segment
        w=[j for j in range(i-6,i+7) if 0<=j<N and seg[j]==seg[i] and held(j)]
        ref=np.median(cov[w]) if w else 0
        if cov[i]<0.85*ref:
            j=max(w,key=lambda j:cov[j]);s=np.maximum(s,S[j]*0.999)
    m=np.maximum(p,s)
    f=None
    cv2.imwrite(f"masks3/{i:05d}.png",(np.clip(m,0,1)*255).astype(np.uint8))
print("done")
