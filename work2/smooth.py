import cv2,json,numpy as np
from scipy.signal import medfilt
R={int(k):v for k,v in json.load(open("detect_raw.json")).items()}
out={}
for a,b in [(0,119),(1387,2509)]:
    idx=np.arange(a,b+1);v=np.array([R[i] for i in idx])
    cx=v[:,1]+v[:,3]/2;cy=v[:,2]+v[:,4]/2;sz=np.maximum(v[:,3],v[:,4])
    good=v[:,0]>=0.55
    mx=medfilt(np.where(good,cx,np.nan).copy()*0+cx,15);my=medfilt(cy,15)
    good&=(np.abs(cx-mx)<60)&(np.abs(cy-my)<60)
    for arr in (cx,cy,sz):
        arr[~good]=np.interp(idx[~good],idx[good],arr[good])
    cx,cy,sz=[medfilt(x,5) for x in (cx,cy,sz)]
    k=np.ones(5)/5;cx,cy,sz=[np.convolve(np.pad(x,2,mode='edge'),k,'valid') for x in (cx,cy,sz)]
    for j,i in enumerate(idx): out[i]=[float(cx[j]),float(cy[j]),float(sz[j]*1.25)]
json.dump({str(k):v for k,v in out.items()},open("facetrack.json","w"))
cap=cv2.VideoCapture("cut.mp4");i=0;th=[]
sel=set(list(range(0,120,10))+list(range(1390,2510,24)))
while True:
    ok,f=cap.read()
    if not ok: break
    if i in sel:
        cx,cy,s=out[i];cv2.circle(f,(int(cx),int(cy)),int(s/2),(0,0,255),4);cv2.putText(f,str(i),(10,60),0,2,(0,255,255),4)
        th.append(cv2.resize(f,(144,256)))
    i+=1
rows=[np.hstack(th[k:k+12]+[np.zeros((256,144,3),np.uint8)]*(12-len(th[k:k+12]))) for k in range(0,len(th),12)]
cv2.imwrite("tracksheet2.jpg",np.vstack(rows))
