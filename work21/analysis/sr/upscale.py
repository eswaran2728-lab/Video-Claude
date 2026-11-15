"""AI upscale (Real-ESRGAN compact 'realesr-general-x4v3', BSD-3) of one source segment to a 2x proxy.
usage: upscale.py SRC IN DUR OUT.mp4   -> 1696x956, source frame rate, blended 70/30 with lanczos to keep it natural."""
import sys, subprocess, numpy as np, torch, torch.nn as nn, torch.nn.functional as F, os, time
class SRVGG(nn.Module):
    def __init__(s, nf=64, nc=32, up=4):
        super().__init__(); s.up=up; b=[nn.Conv2d(3,nf,3,1,1), nn.PReLU(nf)]
        for _ in range(nc): b += [nn.Conv2d(nf,nf,3,1,1), nn.PReLU(nf)]
        b.append(nn.Conv2d(nf,3*up*up,3,1,1)); s.body=nn.ModuleList(b); s.ps=nn.PixelShuffle(up)
    def forward(s,x):
        o=x
        for m in s.body: o=m(o)
        return s.ps(o)+F.interpolate(x,scale_factor=s.up,mode='nearest')
src,ss,dur,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
W,H,OW,OH=848,478,1696,956
fps=subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=r_frame_rate','-of','csv=p=0',src],capture_output=True,text=True).stdout.strip()
m=SRVGG(); sd=torch.load(os.path.join(os.path.dirname(__file__),'realesr-general-x4v3.pth'),map_location='cpu'); m.load_state_dict(sd.get('params',sd)); m.eval()
raw=subprocess.run(['ffmpeg','-v','error','-ss',str(ss),'-t',str(dur),'-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
fr=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3)
enc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{OW}x{OH}','-r',fps,'-i','-','-c:v','libx264','-crf','12','-preset','fast','-g','12','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
t0=time.time()
with torch.no_grad():
    for f in fr:
        x=torch.from_numpy(f.copy()).permute(2,0,1)[None].float()/255
        y=m(x).clamp(0,1)
        y=F.interpolate(y,size=(OH,OW),mode='area')
        b=F.interpolate(x,size=(OH,OW),mode='bicubic',align_corners=False).clamp(0,1)
        o=(0.7*y+0.3*b)
        enc.stdin.write((o[0].permute(1,2,0)*255).round().byte().numpy().tobytes())
enc.stdin.close(); enc.wait(); print(out,len(fr),'frames',round((time.time()-t0)/max(1,len(fr)),2),'s/frame')
