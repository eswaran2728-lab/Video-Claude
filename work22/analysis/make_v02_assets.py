"""v02 assets from the graded hero frame + statue alpha: colour cut-out, grey 'printed' cut-out with layer ridges,
slicer-style toolpath hologram, CAD-style edge wireframe, background with the statue removed (blurred, for parallax),
row extents of the statue for the nozzle path."""
import numpy as np, cv2, json
from PIL import Image
X0, Y0, X1, Y1 = 150, 1100, 1950, 3700                      # crop of the 2160x3840 frame
hero = cv2.imread('v01/assets/img/hero_graded.jpg')         # graded colour frame
raw = cv2.imread('analysis/frames/a_005.png')
a = cv2.imread('analysis/statue_alpha.png', 0).astype(np.float32) / 255
c = lambda im: im[Y0:Y1, X0:X1]
A = c(a); col = c(hero)
def rgba(bgr, al): out = np.dstack([bgr[..., ::-1], (al * 255).astype(np.uint8)]); return Image.fromarray(out.astype(np.uint8), 'RGBA')
rgba(col, A).save('v02/assets/img/statue_colour.png', optimize=True)
# grey PLA: luminance, flattened, slight sheen + horizontal layer ridges (every 7 px)
L = cv2.cvtColor(c(raw), cv2.COLOR_BGR2GRAY).astype(np.float32)
L = 135 + (L - 120) * 0.62
yy = np.arange(L.shape[0])[:, None]
ridge = 1 - 0.10 * (0.5 + 0.5 * np.cos(2 * np.pi * yy / 7.0))
L = L * ridge
g = np.dstack([L * 0.97, L * 0.99, L * 1.03]).clip(0, 255).astype(np.uint8)
g = cv2.cvtColor(np.ascontiguousarray(g), cv2.COLOR_RGB2BGR)
rgba(g, A).save('v02/assets/img/statue_grey.png', optimize=True)
# toolpath hologram: lines every 9 px coloured by height, plus outer-wall outline
H, W = A.shape
m = A > 0.5
t = np.zeros((H, W, 4), np.float32)
ys = np.arange(H)
hcol = np.stack([np.interp(ys, [0, H], [0.62, 0.15]), np.interp(ys, [0, H], [0.45, 0.88]), np.ones(H)], 1)  # violet top -> cyan bottom (RGB)
lines = (ys % 9) < 3
for ch in range(3): t[..., ch] = hcol[:, ch][:, None]
t[..., 3] = (m & lines[:, None]) * 0.55
edge = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((7, 7), np.uint8)) > 0
t[edge, :3] = (0.55, 0.95, 1.0); t[edge, 3] = 1.0
Image.fromarray((t * 255).astype(np.uint8), 'RGBA').save('v02/assets/img/toolpath.png', optimize=True)
# CAD wireframe: Canny edges inside the statue
ed = cv2.Canny(cv2.GaussianBlur(c(raw), (5, 5), 0), 40, 110) > 0
ed &= cv2.erode(m.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
ed = cv2.dilate(ed.astype(np.uint8), np.ones((2, 2), np.uint8)) > 0
w = np.zeros((H, W, 4), np.uint8); w[ed] = (150, 235, 255, 230)
Image.fromarray(w, 'RGBA').save('v02/assets/img/wire.png', optimize=True)
# background without the statue (inpainted at half res, then soft blur = depth of field)
hm = cv2.dilate((a > 0.2).astype(np.uint8) * 255, np.ones((41, 41), np.uint8))
sm = cv2.resize(hero, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA); smm = cv2.resize(hm, (sm.shape[1], sm.shape[0]))
bg = cv2.inpaint(sm, smm, 18, cv2.INPAINT_TELEA)
bg = cv2.GaussianBlur(bg, (0, 0), 9)
bg = cv2.resize(bg, (2160, 3840), interpolation=cv2.INTER_CUBIC)
cv2.imwrite('v02/assets/img/bg_clean.jpg', bg, [cv2.IMWRITE_JPEG_QUALITY, 90])
# row extents (crop coordinates) every 10 px, for the nozzle path
rows = []
for y in range(0, H, 10):
    xs = np.where(m[y])[0]
    if len(xs) > 20: rows.append([y, int(xs.min()), int(xs.max())])
json.dump({'crop': [X0, Y0, X1, Y1], 'rows': rows}, open('v02/statue_rows.json', 'w'))
print('assets ok', W, H, len(rows))
