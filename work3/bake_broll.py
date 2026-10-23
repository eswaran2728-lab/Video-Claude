"""Bake B-roll clips with a liquid-metaball reveal/exit (alpha) and a chrome-gold rim on the liquid edge."""
import cv2,numpy as np,subprocess,sys,json
def smooth(x,a,b): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
def eo(t): return 1-(1-t)**3
def field(W,H,t,seed):
    rng=np.random.RandomState(seed);n=7
    cx=rng.uniform(0.15,0.85,n)*W;cy=rng.uniform(0.15,0.85,n)*H;base=rng.uniform(0.5,1.0,n)
    yy,xx=np.mgrid[0:H:4,0:W:4].astype(np.float32);f=np.zeros_like(xx)
    R=max(W,H)*0.30*t**1.5
    for i in range(n):
        r=R*base[i]*(0.6+0.4*np.sin(t*3+i));d2=(xx-cx[i])**2+(yy-cy[i])**2+1;f+=r*r/d2
    return cv2.resize(f,(W,H),interpolation=cv2.INTER_LINEAR)
def bake(src,start,dur,out,crop=None,size=None,tin=0.5,tout=0.45,seed=1,radius=0,show_at_zero=False):
    cap=cv2.VideoCapture(src);fps=30;cap.set(cv2.CAP_PROP_POS_MSEC,start*1000)
    n=round(dur*fps);frames=[]
    for k in range(n):
        ok,f=cap.read()
        if not ok: f=frames[-1]
        frames.append(f)
    if crop: y0,y1,x0,x1=crop;frames=[f[y0:y1,x0:x1] for f in frames]
    if size: frames=[cv2.resize(f,size,interpolation=cv2.INTER_CUBIC) for f in frames]
    H,W=frames[0].shape[:2]
    rr=np.ones((H,W),np.float32)
    if radius:
        rr=np.zeros((H,W),np.uint8);cv2.rectangle(rr,(radius,0),(W-radius,H),1,-1);cv2.rectangle(rr,(0,radius),(W,H-radius),1,-1)
        for c in [(radius,radius),(W-radius,radius),(radius,H-radius),(W-radius,H-radius)]: cv2.circle(rr,c,radius,1,-1,cv2.LINE_AA)
        rr=cv2.GaussianBlur(rr.astype(np.float32),(0,0),1.2)
    enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgra","-s",f"{W}x{H}","-r","30","-i","-","-c:v","libvpx-vp9","-pix_fmt","yuva420p","-b:v","0","-crf","20","-row-mt","1","-cpu-used","4",out],stdin=subprocess.PIPE)
    gold=np.array([90,200,255],np.float32);white=np.array([255,250,245],np.float32)
    for k,f in enumerate(frames):
        t=k/fps
        if t<tin and not show_at_zero: p=smooth(t/tin,0,1)
        elif t>dur-tout: p=smooth((dur-t)/tout,0,1)
        else: p=None
        if p is None: a=np.ones((H,W),np.float32);rim=0
        else:
            fl=field(W,H,max(p,1e-3),seed)
            a=np.maximum(smooth(fl,0.92,1.08),smooth(p,0.82,1.0))
            band=smooth(fl,0.92,1.0)*(1-smooth(fl,1.05,1.6))*(1-smooth(p,0.85,1.0))
            rim=band[...,None]
        fo=f.astype(np.float32)
        if p is not None: fo=fo*(1-rim*0.8)+rim*0.8*(gold*0.6+white*0.4)
        a=a*rr
        enc.stdin.write(np.dstack([np.clip(fo,0,255).astype(np.uint8),(np.clip(a,0,1)*255).astype(np.uint8)]).tobytes())
    enc.stdin.close();enc.wait();print("wrote",out,W,H,n)
if __name__=="__main__":
    jobs=json.loads(sys.argv[1])
    for j in jobs: bake(**j)
