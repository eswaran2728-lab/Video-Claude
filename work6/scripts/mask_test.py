import cv2,time,numpy as np,sys
from rembg import remove,new_session
from PIL import Image
cap=cv2.VideoCapture("edit/src_1080.mp4");tiles=[]
for name in ["birefnet-general-lite"]:
    s=new_session(name)
    for t in [1.0,6.0,11.0,14.5]:
        cap.set(cv2.CAP_PROP_POS_FRAMES,int(t*30));ok,f=cap.read()
        t0=time.time();m=np.array(remove(Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)),session=s,only_mask=True))
        print(name,t,round(time.time()-t0,1),flush=True)
        bg=np.zeros_like(f);bg[:]=(200,60,200)
        a=(m/255.0)[...,None];c=(f*a+bg*(1-a)).astype(np.uint8)
        tiles.append(cv2.resize(c,(270,480)))
cv2.imwrite("bgx/mask_test.jpg",cv2.hconcat(tiles))
