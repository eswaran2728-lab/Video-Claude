import cv2,json,numpy as np,sys,subprocess
W,H=720,1280
FT={int(k):v for k,v in json.load(open("facetrack.json")).items()}
bg0=cv2.imread("bg.jpg");bh=int(bg0.shape[0]*W/bg0.shape[1])
bg0=cv2.resize(bg0,(W,bh))[(bh-H)//2:(bh-H)//2+H]
bg0=cv2.GaussianBlur(bg0,(0,0),5)
bg0=(bg0.astype(np.float32)*0.85)
# grade LUT: gentle S-curve + warmth
x=np.arange(256)/255.0
s=np.clip(x+0.10*np.sin(2*np.pi*(x-0.5))*-1*0+0.12*(x-0.5)*(1-np.abs(2*x-1)),0,1)
lutR=np.clip((s**0.97)*255*1.03,0,255).astype(np.uint8);lutG=np.clip(s*255,0,255).astype(np.uint8);lutB=np.clip((s**1.04)*255*0.96,0,255).astype(np.uint8)
def grade(f):
    f=cv2.merge([cv2.LUT(f[:,:,0],lutB),cv2.LUT(f[:,:,1],lutG),cv2.LUT(f[:,:,2],lutR)])
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV).astype(np.float32);hsv[:,:,1]*=1.08
    return cv2.cvtColor(np.clip(hsv,0,255).astype(np.uint8),cv2.COLOR_HSV2BGR)
def hide_face(f,i):
    if i not in FT: return f
    cx,cy,s=FT[i];r=int(s*0.55);x0,y0=max(int(cx-r),0),max(int(cy-r),0);x1,y1=min(int(cx+r),W),min(int(cy+r),H)
    roi=f[y0:y1,x0:x1]
    if roi.size==0: return f
    sm=cv2.resize(roi,(max(1,(x1-x0)//16),max(1,(y1-y0)//16)),interpolation=cv2.INTER_LINEAR)
    pix=cv2.GaussianBlur(cv2.resize(sm,(x1-x0,y1-y0),interpolation=cv2.INTER_NEAREST),(0,0),4)
    m=np.zeros((y1-y0,x1-x0),np.float32);cv2.circle(m,(int(cx-x0),int(cy-y0)),int(s*0.5),1,-1);m=cv2.GaussianBlur(m,(0,0),4)[...,None]
    f[y0:y1,x0:x1]=(pix*m+roi*(1-m)).astype(np.uint8);return f
start=int(sys.argv[1]) if len(sys.argv)>1 else 0;end=int(sys.argv[2]) if len(sys.argv)>2 else 10**9;outp=sys.argv[3] if len(sys.argv)>3 else "comp_noaudio.mp4"
cap=cv2.VideoCapture("cut.mp4")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p",outp],stdin=subprocess.PIPE)
prev=None;i=0;N=2510
while True:
    ok,f=cap.read()
    if not ok or i>end: break
    if i>=start:
        m=cv2.imread(f"masks/{i:05d}.png",0).astype(np.float32)/255
        m=np.clip((m-0.15)/0.7,0,1)
        m=cv2.GaussianBlur(m,(0,0),1.2)
        if prev is not None: m=0.65*m+0.35*prev
        prev=m
        f=hide_face(f,i);f=grade(f)
        z=1.0+0.04*i/N
        M=cv2.getRotationMatrix2D((W/2,H/2),0,z);bg=cv2.warpAffine(bg0,M,(W,H),borderMode=cv2.BORDER_REFLECT)
        mm=m[...,None]
        # light wrap
        edge=np.clip(cv2.GaussianBlur(mm[...,0],(0,0),6)-mm[...,0],0,1)[...,None]*0
        o=f.astype(np.float32)*mm+bg*(1-mm)
        enc.stdin.write(np.clip(o,0,255).astype(np.uint8).tobytes())
    i+=1
enc.stdin.close();enc.wait();print("done",i)
