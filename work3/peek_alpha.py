import cv2,numpy as np,subprocess,sys
src,frames,out=sys.argv[1],[int(x) for x in sys.argv[2].split(",")],sys.argv[3]
tiles=[]
for n in frames:
    subprocess.run(["ffmpeg","-v","error","-y","-c:v","libvpx-vp9","-i",src,"-vf",f"select=eq(n\\,{n})","-frames:v","1","-pix_fmt","rgba","/tmp/_pk.png"],check=True)
    im=cv2.imread("/tmp/_pk.png",cv2.IMREAD_UNCHANGED).astype(np.float32);a=im[...,3:]/255
    bg=np.zeros_like(im[...,:3]);bg[:]=(40,10,30)
    o=np.clip(im[...,:3]*a+bg*(1-a),0,255).astype(np.uint8);cv2.putText(o,str(n),(10,60),0,2,(0,255,255),4)
    tiles.append(cv2.resize(o.astype(np.uint8),(150,int(150*im.shape[0]/im.shape[1]))))
cv2.imwrite(out,np.hstack(tiles))
