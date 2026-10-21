import cv2,os,sys,time
from rembg import remove,new_session
from PIL import Image
s=new_session("birefnet-general-lite")
cap=cv2.VideoCapture("cut.mp4");i=0;t0=time.time();n=0
while True:
    ok,f=cap.read()
    if not ok: break
    if (i<=119 or i>=1387) and not os.path.exists(f"bmasks/{i:05d}.png"):
        remove(Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)),session=s,only_mask=True).save(f"bmasks/{i:05d}.png");n+=1
        if n%50==0: print(i,n,round(time.time()-t0),flush=True)
    i+=1
print("done",n,round(time.time()-t0))
