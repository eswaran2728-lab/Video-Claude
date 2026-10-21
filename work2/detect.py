import cv2,json,numpy as np
S=0.5
sel=np.load("frames_sel.npy")
B=[(180,400,110,150),(305,390,100,115),(335,375,115,130),(420,370,105,120)]
T=[]
for f,(x,y,w,h) in zip(sel,B):
    t=cv2.resize(f[y:y+h,x:x+w],None,fx=S,fy=S)
    for sc in (0.75,0.85,1.0,1.15,1.3):
        T.append((cv2.resize(t,None,fx=sc,fy=sc),w*sc,h*sc))
cap=cv2.VideoCapture("cut.mp4");i=0;R={}
RANGES=[(0,119),(1382,2509)]
while True:
    ok,f=cap.read()
    if not ok: break
    if any(a<=i<=b for a,b in RANGES):
        g=cv2.resize(f,None,fx=S,fy=S);best=(-1,)
        for t,w,h in T:
            r=cv2.matchTemplate(g,t,cv2.TM_CCOEFF_NORMED)
            r[:, :int(140*S)]=-1
            _,mv,_,ml=cv2.minMaxLoc(r)
            if mv>best[0]: best=(mv,ml[0]/S,ml[1]/S,w,h)
        R[i]=best
    i+=1
json.dump({k:list(v) for k,v in R.items()},open("detect_raw.json","w"))
sc=[v[0] for v in R.values()];print("score pct",np.percentile(sc,[5,25,50,75]))
