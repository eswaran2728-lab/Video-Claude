# Creator's logos -> transparent PNGs for the edit (originals kept in src/logos/).
# - Mahaguru Dr. Sri S. Arumugam medal: the transparent version already made in work13 (same source file, byte-identical).
# - Persatuan Silambam Malaysia (white background): flood fill of near-white from the border (inner whites kept).
# - Silambam Selangor logo (black background; the figure's black trousers touch the black): BiRefNet-lite matte (local ONNX).
import shutil, numpy as np, cv2, onnxruntime as ort
from PIL import Image
OUT = "edit/assets/logos/"
shutil.copy("../work13/LOGO_Mahaguru_Arumugam_transparent.png", OUT + "mahaguru.png")


def trim_save(rgb, alpha, name, h=400):
    ys, xs = np.where(alpha > 8); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    o = Image.fromarray(np.dstack([rgb.astype(np.uint8), alpha])[y0:y1, x0:x1], "RGBA")
    if o.height < h: o = o.resize((round(o.width * h / o.height), h), Image.LANCZOS)
    o.save(OUT + name); return o


# Silambam Malaysia
im = np.array(Image.open("src/logos/silambam_malaysia_original.jpg").convert("RGB")); H, W = im.shape[:2]; f = im.astype(int)
near = ((f.min(axis=2) > 215) & (f.max(axis=2) - f.min(axis=2) < 35)).astype(np.uint8); out = near.copy(); m = np.zeros((H + 2, W + 2), np.uint8)
for x in range(0, W, 3):
    for y in (0, H - 1):
        if out[y, x] == 1: cv2.floodFill(out, m, (x, y), 2)
for y in range(0, H, 3):
    for x in (0, W - 1):
        if out[y, x] == 1: cv2.floodFill(out, m, (x, y), 2)
alpha = cv2.GaussianBlur(np.where(out == 2, 0, 255).astype(np.uint8), (3, 3), 0)
fr = (alpha > 0) & (alpha < 255); a = alpha[..., None].astype(float) / 255; rgb = f.astype(float)
rgb[fr] = np.clip((rgb[fr] - 255 * (1 - a[fr])) / np.maximum(a[fr], 0.2), 0, 255)
s = trim_save(rgb, alpha, "silambam_malaysia.png")  # NOT used: the flood fill also removes the figures' white uniforms -> the edit shows the original on a white logo card (silambam_malaysia_onwhite.jpg)
shutil.copy("src/logos/silambam_malaysia_original.jpg", OUT + "silambam_malaysia_onwhite.jpg")

# Silambam Selangor (BiRefNet)
so = ort.SessionOptions(); so.enable_cpu_mem_arena = False; so.enable_mem_pattern = False
S = ort.InferenceSession('/root/.rembg/models/birefnet-general-lite/birefnet-general-lite.onnx', so, providers=['CPUExecutionProvider'])
bgr = cv2.imread("src/logos/selangor_original.jpg"); MEAN, STD = np.array([0.485, 0.456, 0.406]), np.array([0.229, 0.224, 0.225])
x = cv2.cvtColor(cv2.resize(bgr, (1024, 1024), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2RGB).astype(np.float32) / 255
x = ((x - MEAN) / STD).transpose(2, 0, 1)[None].astype(np.float32)
p = 1 / (1 + np.exp(-S.run(None, {'input_image': x})[0][0, 0])); p = (p - p.min()) / (p.max() - p.min() + 1e-6)
alpha = cv2.resize((p * 255).astype(np.uint8), (bgr.shape[1], bgr.shape[0]), interpolation=cv2.INTER_LINEAR)
alpha = np.where(alpha > 200, 255, np.where(alpha < 40, 0, alpha)).astype(np.uint8)
g = trim_save(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(float), alpha, "silambam_selangor.png")
for nm in ("mahaguru", "silambam_malaysia", "silambam_selangor"):
    o = Image.open(OUT + nm + ".png")
    for bgn, bg in (("dark", (14, 11, 16)), ("red", (150, 20, 40)), ("white", (245, 245, 245))):
        c = Image.new("RGBA", o.size, bg + (255,)); c.alpha_composite(o); c.convert("RGB").save(f"sheets/logo_{nm}_on_{bgn}.png")
print("ok", s.size, g.size)
