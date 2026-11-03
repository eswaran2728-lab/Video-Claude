# The creator's tournament poster (src/poster/poster_kejohanan_2026.jpg, 853x1280) -> torn-paper pieces for the
# "poster breaking its frame" motion graphic (Prompt Motion: pankajkumar-dev-0bee87). Each piece is the poster's own pixels
# (no retyping), cut along a jagged torn edge with a thin white paper fibre rim, upscaled 2x (Lanczos).
# -> edit/assets/poster/<name>.png + pieces.json (box in poster px, for placing each piece exactly over the full poster)
import json, numpy as np, cv2
from PIL import Image
P = Image.open("src/poster/poster_kejohanan_2026.jpg").convert("RGB"); SC = 2
P.resize((P.width * SC, P.height * SC), Image.LANCZOS).save("edit/assets/poster/full.jpg", quality=95)
BOX = {"logos": (140, 40, 650, 200), "kejohanan": (172, 248, 738, 386), "silambam": (22, 384, 838, 549),
       "peringkat": (104, 552, 750, 684), "y2026": (248, 646, 602, 760), "anjuran": (228, 760, 632, 962),
       "date": (24, 1034, 306, 1173), "time": (304, 1034, 562, 1173), "venue": (560, 1034, 834, 1173), "tamil": (172, 1176, 702, 1270)}
rng = np.random.default_rng(7); meta = {}


def torn(w, h, amp=7, step=9):
    """jagged polygon inside a w x h box: random walk along each edge"""
    pts = []
    def edge(a, b, n):
        for i in range(n + 1):
            u = i / n; x = a[0] + (b[0] - a[0]) * u; y = a[1] + (b[1] - a[1]) * u; yield x, y
    def jit(): return rng.uniform(0, amp)
    nx, ny = max(2, w // step), max(2, h // step)
    for x, y in edge((0, 0), (w, 0), nx): pts.append((x, y + jit()))
    for x, y in edge((w, 0), (w, h), ny): pts.append((x - jit(), y))
    for x, y in edge((w, h), (0, h), nx): pts.append((x, y - jit()))
    for x, y in edge((0, h), (0, 0), ny): pts.append((x + jit(), y))
    return np.array(pts, np.float32)


for k, (x0, y0, x1, y1) in BOX.items():
    crop = P.crop((x0, y0, x1, y1)); w, h = crop.width * SC, crop.height * SC
    img = np.array(crop.resize((w, h), Image.LANCZOS)); pad = 10
    poly = torn(w, h, amp=9, step=14)
    outer = np.zeros((h + 2 * pad, w + 2 * pad), np.uint8); cv2.fillPoly(outer, [(poly + pad).astype(np.int32)], 255, cv2.LINE_AA)
    inner = cv2.erode(outer, np.ones((7, 7), np.uint8))                      # paper fibre rim = outer - inner
    canvas = np.full((h + 2 * pad, w + 2 * pad, 3), 248, np.uint8); canvas[pad:pad + h, pad:pad + w] = img
    rim = (outer > 0) & (inner == 0); canvas[rim] = (canvas[rim] * 0.25 + np.array([250, 247, 240]) * 0.75).astype(np.uint8)
    Image.fromarray(np.dstack([canvas, outer]), "RGBA").save(f"edit/assets/poster/{k}.png")
    meta[k] = dict(box=[x0, y0, x1, y1], pad=pad / SC, png=[w + 2 * pad, h + 2 * pad])
json.dump({"poster": [P.width, P.height], "scale": SC, "pieces": meta}, open("edit/assets/poster/pieces.json", "w"), indent=1)
print("pieces", list(meta))
