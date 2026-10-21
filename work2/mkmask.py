import cv2,os
from rembg import remove,new_session
from PIL import Image
s=new_session("isnet-general-use")
cap=cv2.VideoCapture("cut.mp4");i=0
while True:
    ok,f=cap.read()
    if not ok: break
    p=f"masks/{i:05d}.png"
    if not os.path.exists(p):
        m=remove(Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)),session=s,only_mask=True)
        m.save(p)
    i+=1
    if i%100==0: print(i,flush=True)
print("done",i)
