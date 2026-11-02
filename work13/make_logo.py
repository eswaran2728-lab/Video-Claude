# Creator's Mahaguru Dr. Sri S. Arumugam logo (src/logo/logo_original.png, white background) -> transparent PNG for the header.
# White is removed by flood fill from the image border on near-white pixels (so whites INSIDE the medal - the portrait
# background, the shirt - are kept because the gold ring closes them), then a 1-px soft edge, trimmed, scaled to 400 px high.
import numpy as np, cv2
from PIL import Image
im = np.array(Image.open("src/logo/logo_original.png").convert("RGB")); H, W = im.shape[:2]
f = im.astype(int); near = ((f.min(axis=2) > 225) & (f.max(axis=2) - f.min(axis=2) < 30)).astype(np.uint8)
mask = np.zeros((H + 2, W + 2), np.uint8); out = near.copy()
for x in range(0, W, 4):
    for y in (0, H - 1):
        if out[y, x] == 1: cv2.floodFill(out, mask, (x, y), 2)
for y in range(0, H, 4):
    for x in (0, W - 1):
        if out[y, x] == 1: cv2.floodFill(out, mask, (x, y), 2)
alpha = np.where(out == 2, 0, 255).astype(np.uint8)
# soften the cut edge and pull out the white fringe from anti-aliased pixels
alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
fr = (alpha > 0) & (alpha < 255); a = alpha[..., None].astype(float) / 255
rgb = f.astype(float); rgb[fr] = np.clip((rgb[fr] - 255 * (1 - a[fr])) / np.maximum(a[fr], 0.2), 0, 255)
ys, xs = np.where(alpha > 8); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
rgba = np.dstack([rgb.astype(np.uint8), alpha])[y0:y1, x0:x1]
o = Image.fromarray(rgba, "RGBA"); o = o.resize((round(o.width * 400 / o.height), 400), Image.LANCZOS)
o.save("edit/assets/logo_arumugam.png"); o.save("LOGO_Mahaguru_Arumugam_transparent.png")
# check sheet on dark and on a stage frame colour
for name, bg in (("dark", (14, 11, 16)), ("red", (150, 20, 50))):
    c = Image.new("RGBA", o.size, bg + (255,)); c.alpha_composite(o); c.convert("RGB").save(f"sheets/logo_on_{name}.png")
print("logo", o.size, "trim box", (x0, y0, x1, y1), "of", (W, H))
