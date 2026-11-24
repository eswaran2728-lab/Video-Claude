"""AI upscale (Real-ESRGAN compact realesr-general-x4v3, same model as work21) of still screenshots: 4x then area-down to 2x."""
import sys, numpy as np, torch, torch.nn as nn, torch.nn.functional as F
from PIL import Image
class SRVGG(nn.Module):
    def __init__(s, nf=64, nc=32, up=4):
        super().__init__(); s.up=up; b=[nn.Conv2d(3,nf,3,1,1), nn.PReLU(nf)]
        for _ in range(nc): b += [nn.Conv2d(nf,nf,3,1,1), nn.PReLU(nf)]
        b.append(nn.Conv2d(nf,3*up*up,3,1,1)); s.body=nn.ModuleList(b); s.ps=nn.PixelShuffle(up)
    def forward(s,x):
        o=x
        for m in s.body: o=m(o)
        return s.ps(o)+F.interpolate(x,scale_factor=s.up,mode='nearest')
m=SRVGG(); sd=torch.load('/home/user/Video-Claude/work21/analysis/sr/realesr-general-x4v3.pth',map_location='cpu'); m.load_state_dict(sd.get('params',sd)); m.eval()
for src,dst in zip(sys.argv[1::2], sys.argv[2::2]):
    im=np.asarray(Image.open(src).convert('RGB')).astype(np.float32)/255
    x=torch.from_numpy(im).permute(2,0,1)[None]
    with torch.no_grad(): y=m(x).clamp(0,1)
    h,w=im.shape[:2]; y=F.interpolate(y,size=(h*2,w*2),mode='area')
    Image.fromarray((y[0].permute(1,2,0).numpy()*255).round().astype(np.uint8)).save(dst, quality=95); print(dst)
