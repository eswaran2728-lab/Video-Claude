"""Colour grade for the statue reel, written once as a 3D LUT (grade.cube) and applied identically to
the stills and the video proxy with ffmpeg lut3d. Look: warm workshop, product colours kept true.
1 exposure +4.5%  2 gentle S-curve  3 black point  4 highlight roll-off (sword/specular)
5 split tone: cool-teal shadows (brown wall recedes), warm highlights  6 vibrance +6% (low-sat colours more)"""
import numpy as np, sys, os
def grade(rgb):
    x = np.clip(rgb * 1.045, 0, 1)
    s = x * x * (3 - 2 * x); x = x + (s - x) * 0.20
    x = np.clip((x - 0.012) / 0.988, 0, 1)
    hi = x > 0.82; x = np.where(hi, 0.82 + (x - 0.82) * 0.72, x)
    L = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
    x = x + np.array([-0.012, 0.010, 0.030]) * (1 - L) ** 2.2 + np.array([0.025, 0.010, -0.015]) * L ** 2
    m = x.max(-1, keepdims=True); n = x.min(-1, keepdims=True); sat = (m - n) / (m + 1e-6)
    L = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
    x = L + (x - L) * (1 + 0.06 * (1 - sat))
    return np.clip(x, 0, 1)
N = 33
g = np.linspace(0, 1, N)
b, gg, r = np.meshgrid(g, g, g, indexing='ij')          # .cube order: red fastest
lut = grade(np.stack([r, gg, b], -1).reshape(-1, 3))
out = sys.argv[1] if len(sys.argv) > 1 else 'grade.cube'
with open(out, 'w') as f:
    f.write('TITLE "statue-reel workshop grade"\nLUT_3D_SIZE %d\n' % N)
    for v in lut: f.write('%.6f %.6f %.6f\n' % tuple(v))
print('wrote', out)
