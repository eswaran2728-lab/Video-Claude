# v03 logo bar art from the creator's files (AirAsia AVSEC badge, Allstars "Dare to Dream"), shown for the whole video.
#  - AVSEC badge: the black square around the shield is made transparent (flood fill from the corners; the shield's own black
#    inside stays because the yellow border closes it), trimmed to the shield.
#  - Allstars: 223x125 on white -> Real-ESRGAN x4 (same model as the photos); it sits on the bar's white, so no cut-out needed.
import os, sys, numpy as np, torch, cv2
from PIL import Image
sys.path.insert(0, "tools"); import esrgan
torch.set_num_threads(2)
UP = "/root/.claude/uploads/0f5de6a0-cb79-5121-a40c-201a11ec7d73"
O = "edit/assets/logos"; os.makedirs(O, exist_ok=True); os.makedirs("src/logos", exist_ok=True)
Image.open(f"{UP}/b8d35af4-image.webp").convert("RGB").save("src/logos/avsec_badge_original.png")
Image.open(f"{UP}/bbf097d5-image.png").convert("RGB").save("src/logos/allstars_original.png")

im = np.array(Image.open("src/logos/avsec_badge_original.png")); H, W = im.shape[:2]
dark = (im.max(axis=2) < 60).astype(np.uint8)
mask = np.zeros((H + 2, W + 2), np.uint8); out = dark.copy()
for p in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)]:
    if dark[p[1], p[0]]: cv2.floodFill(out, mask, p, 2)
alpha = np.where(out == 2, 0, 255).astype(np.uint8)
alpha = cv2.GaussianBlur(alpha, (3, 3), 0)                    # soft 1-px edge instead of a jagged cut
ys, xs = np.where(alpha > 0); im = np.dstack([im, alpha])[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
badge = Image.fromarray(im, "RGBA"); badge = badge.resize((round(badge.width * 400 / badge.height), 400), Image.LANCZOS)
badge.save(f"{O}/avsec_badge.png"); print("avsec", badge.size)

m = esrgan.load("models/realesr-general-x4v3.pth", "models/realesr-general-wdn-x4v3.pth", 0.5)
al = Image.fromarray(esrgan.upscale(m, Image.open("src/logos/allstars_original.png"))); al.save(f"{O}/allstars.png"); print("allstars", al.size)
