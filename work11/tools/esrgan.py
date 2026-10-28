# Real-ESRGAN "realesr-general-x4v3" (SRVGGNetCompact, BSD-3, github.com/xinntao/Real-ESRGAN release v0.2.5.0) on CPU, tiled.
# Weights are loaded with weights_only=True (tensors only, no pickled code runs).
import torch, torch.nn as nn, torch.nn.functional as F, numpy as np

class SRVGG(nn.Module):
    def __init__(s, nf=64, nc=32, up=4):
        super().__init__(); s.up = up
        b = [nn.Conv2d(3, nf, 3, 1, 1), nn.PReLU(nf)]
        for _ in range(nc): b += [nn.Conv2d(nf, nf, 3, 1, 1), nn.PReLU(nf)]
        b += [nn.Conv2d(nf, 3 * up * up, 3, 1, 1)]; s.body = nn.ModuleList(b); s.ps = nn.PixelShuffle(up)
    def forward(s, x):
        o = x
        for m in s.body: o = m(o)
        return s.ps(o) + F.interpolate(x, scale_factor=s.up, mode="nearest")

def _sd(p):
    sd = torch.load(p, map_location="cpu", weights_only=True)
    return sd.get("params", sd)

def load(w, wdn=None, dn=0.5):
    sd = _sd(w)
    if wdn:   # Real-ESRGAN's denoise-strength blend: dn=1 base model; lower = gentler, less invented texture
        s2 = _sd(wdn); sd = {k: dn * sd[k] + (1 - dn) * s2[k] for k in sd}
    m = SRVGG(); m.load_state_dict(sd); m.eval(); return m

@torch.no_grad()
def upscale(m, img, tile=384, pad=12):
    x = torch.from_numpy(np.asarray(img, np.float32) / 255).permute(2, 0, 1)[None]
    _, _, H, W = x.shape; out = torch.zeros(1, 3, H * 4, W * 4)
    for y0 in range(0, H, tile):
        for x0 in range(0, W, tile):
            ya, yb, xa, xb = max(0, y0 - pad), min(H, y0 + tile + pad), max(0, x0 - pad), min(W, x0 + tile + pad)
            o = m(x[:, :, ya:yb, xa:xb]); ty, tx = min(tile, H - y0), min(tile, W - x0)
            out[:, :, y0 * 4:(y0 + ty) * 4, x0 * 4:(x0 + tx) * 4] = o[:, :, (y0 - ya) * 4:(y0 - ya + ty) * 4, (x0 - xa) * 4:(x0 - xa + tx) * 4]
    return (out[0].clamp(0, 1).permute(1, 2, 0).numpy() * 255 + 0.5).astype(np.uint8)
