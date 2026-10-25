# BiRefNet-lite alpha for every source frame used in the edit (statue + rock; the board and park are dropped).
import cv2,os,time,numpy as np
from rembg import remove,new_session
from PIL import Image
R=[(305,346),(9,90),(150,249),(369,403),(402,457)]
need=sorted({f for a,b in R for f in range(a,b+1)})
s=new_session("birefnet-general-lite");cap=cv2.VideoCapture("edit/src_1080.mp4");i=0;t0=time.time();n=0
while True:
    ok,f=cap.read()
    if not ok or i>max(need): break
    if i in need and not os.path.exists(f"bgx/masks/{i:05d}.png"):
        remove(Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)),session=s,only_mask=True).save(f"bgx/masks/{i:05d}.png");n+=1
        if n%20==0: print(i,n,len(need),round(time.time()-t0),flush=True)
    i+=1
print("done",n,round(time.time()-t0),flush=True)
