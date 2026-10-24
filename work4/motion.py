import cv2,numpy as np,json
res={}
for v in ["v176","v185","v186","v201","v203"]:
    cap=cv2.VideoCapture(f"src/{v}.mp4");fps=cap.get(5);prev=None;t=0;scores=[];tt=[]
    step=max(1,round(fps/10));k=0
    while True:
        ok,f=cap.read()
        if not ok: break
        if k%step==0:
            g=cv2.cvtColor(cv2.resize(f,(320,180)),cv2.COLOR_BGR2GRAY)[30:130]   # middle band: performers
            if prev is not None:
                fl=cv2.calcOpticalFlowFarneback(prev,g,None,0.5,2,9,2,5,1.1,0)
                mag=np.linalg.norm(fl,axis=2);scores.append(float(np.percentile(mag,97)));tt.append(k/fps)
            prev=g
        k+=1
    s=np.array(scores);sm=np.convolve(s,np.ones(5)/5,'same')
    res[v]={"t":[round(x,2) for x in tt],"m":[round(float(x),3) for x in sm]}
    # 1 s summary
    sec=[round(float(sm[(np.array(tt)>=i)&(np.array(tt)<i+1)].mean()),2) for i in range(int(tt[-1]))]
    print(v,"dur",round(k/fps,1),"mean",round(float(sm.mean()),2),"\n ",sec)
json.dump(res,open("motion.json","w"))
