import cv2,json,numpy as np,subprocess
from sr import upscale
edl=json.load(open("edl.json"))
keep=set();order=[]
for fa,fb,_ in edl:
    for f in range(fa,fb): order.append(f)
W,H=1080,1920
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgra","-s",f"{W}x{H}","-r","30","-i","-",
    "-c:v","libvpx-vp9","-pix_fmt","yuva420p","-b:v","0","-crf","14","-row-mt","1","-deadline","good","-cpu-used","4","edit/assets/talent.webm"],stdin=subprocess.PIPE)
want=set(order);cap=cv2.VideoCapture("main30.mkv");i=0;cache={}
X=np.linspace(0,1,W)[None,:,None];warmL=np.array([60,185,255],np.float32);coolR=np.array([255,120,150],np.float32)  # BGR gold / violet-blue
prev=None;starts={fa for fa,_,_ in edl}
while True:
    ok,f=cap.read()
    if not ok: break
    if i in want:
        f=upscale(f,W,H)
        a=cv2.resize(cv2.imread(f"rvm/{i:05d}.png",0),(W,H),interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
        g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32)/255
        a=np.clip(cv2.ximgproc.guidedFilter(g,a,6,1e-3),0,1)
        if i in starts: prev=None
        if prev is not None: a=0.85*a+0.15*prev
        prev=a
        # rim light: inner edge band of the matte, gold from the left, violet-blue from the right
        inner=np.clip(a-cv2.GaussianBlur(a,(0,0),13),0,1)*2.2
        rim=np.clip(inner,0,1)[...,None]*a[...,None]
        tint=warmL*(1-X)+coolR*X
        fo=f.astype(np.float32)
        fo=fo+rim*0.55*(tint-fo*0.4)
        out=np.dstack([np.clip(fo,0,255).astype(np.uint8),(a*255).astype(np.uint8)])
        cache[i]=out
    i+=1
    # flush in EDL order as frames become available (EDL is monotonic in source time)
    while order and order[0] in cache:
        enc.stdin.write(cache.pop(order[0]).tobytes()) if order.count(order[0])==1 else enc.stdin.write(cache[order[0]].tobytes())
        order.pop(0)
enc.stdin.close();enc.wait();print("talent done")
