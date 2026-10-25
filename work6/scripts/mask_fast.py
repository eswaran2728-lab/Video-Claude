# BiRefNet-lite via onnxruntime directly on keyframes (every 2nd frame + segment ends);
# in-between frames are filled by optical-flow warping the neighbouring keyframe masks.
import cv2,os,time,numpy as np,onnxruntime as ort
so=ort.SessionOptions();so.enable_cpu_mem_arena=False;so.intra_op_num_threads=4
S=ort.InferenceSession('/root/.rembg/models/birefnet-general-lite/birefnet-general-lite.onnx',so,providers=['CPUExecutionProvider'])
R=[(305,346),(9,90),(150,249),(369,403),(403,457)]
need=sorted({f for a,b in R for f in range(a,b+1)})
cap=cv2.VideoCapture("edit/src_1080.mp4");F={};i=0
while True:
    ok,f=cap.read()
    if not ok or i>max(need): break
    if i in need: F[i]=f
    i+=1
M,S_=np.array([0.485,0.456,0.406]),np.array([0.229,0.224,0.225])
def infer(f):
    im=cv2.cvtColor(cv2.resize(f,(1024,1024),interpolation=cv2.INTER_LANCZOS4),cv2.COLOR_BGR2RGB).astype(np.float32)
    im=im/max(im.max(),1e-6);x=((im-M)/S_).transpose(2,0,1)[None].astype(np.float32)
    p=1/(1+np.exp(-S.run(None,{'input_image':x})[0][0,0]))
    p=(p-p.min())/(p.max()-p.min()+1e-6)
    return cv2.resize((p*255).astype(np.uint8),(f.shape[1],f.shape[0]),interpolation=cv2.INTER_LINEAR)
key=set()
for a,b in R:
    key|=set(range(a,b+1,2))|{b}
t0=time.time();n=0
for k in sorted(key):
    p=f"bgx/masks/{k:05d}.png"
    if not os.path.exists(p): cv2.imwrite(p,infer(F[k]));n+=1
    if n and n%20==0: print("key",n,len(key),round(time.time()-t0),flush=True)
def warp(m,src,dst):
    g0=cv2.cvtColor(cv2.resize(src,(540,960)),cv2.COLOR_BGR2GRAY);g1=cv2.cvtColor(cv2.resize(dst,(540,960)),cv2.COLOR_BGR2GRAY)
    fl=cv2.calcOpticalFlowFarneback(g1,g0,None,0.5,4,21,3,5,1.1,0)  # dst->src
    fl=cv2.resize(fl,(1080,1920))*2
    yy,xx=np.mgrid[0:1920,0:1080].astype(np.float32)
    return cv2.remap(m,xx+fl[...,0],yy+fl[...,1],cv2.INTER_LINEAR)
for fi in need:
    p=f"bgx/masks/{fi:05d}.png"
    if os.path.exists(p): continue
    a,b=fi-1,fi+1
    ma=cv2.imread(f"bgx/masks/{a:05d}.png",0);mb=cv2.imread(f"bgx/masks/{b:05d}.png",0)
    if ma is None or mb is None:
        cv2.imwrite(p,infer(F[fi]));continue
    w=(warp(ma,F[a],F[fi]).astype(np.float32)+warp(mb,F[b],F[fi]).astype(np.float32))/2
    cv2.imwrite(p,w.astype(np.uint8))
print("done",n,round(time.time()-t0),flush=True)
