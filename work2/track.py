import cv2,json
cap=cv2.VideoCapture("cut.mp4");F=[]
while True:
    ok,f=cap.read()
    if not ok: break
    F.append(f)
N=len(F);boxes={}
def run(idx,init):
    t=cv2.TrackerCSRT_create();t.init(F[idx[0]],init);boxes[idx[0]]=init
    for i in idx[1:]:
        ok,b=t.update(F[i])
        if ok: boxes[i]=tuple(int(v) for v in b)
        else: boxes[i]=boxes.get(i-1) or boxes.get(i+1)
A=(180,400,110,150);B=(300,385,115,140)
run(list(range(30,120)),A);run(list(range(30,-1,-1)),A)
run(list(range(1390,N)),B);run(list(range(1390,1381,-1)),B)
json.dump({str(k):v for k,v in boxes.items()},open("facebox.json","w"))
# debug sheet every 12 frames in range B, every 10 in A
sel=list(range(0,120,10))+list(range(1382,N,24))
th=[]
for i in sel:
    g=F[i].copy();x,y,w,h=boxes[i];cv2.rectangle(g,(x,y),(x+w,y+h),(0,0,255),4);cv2.putText(g,str(i),(10,60),0,2,(0,255,255),4)
    th.append(cv2.resize(g,(144,256)))
import numpy as np
rows=[np.hstack(th[k:k+12]+[np.zeros((256,144,3),np.uint8)]*(12-len(th[k:k+12]))) for k in range(0,len(th),12)]
cv2.imwrite("tracksheet.jpg",np.vstack(rows));print(N,len(sel))
