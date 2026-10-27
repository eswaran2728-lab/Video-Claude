# v03: AI-upscale every photo (Real-ESRGAN general x4v3, denoise blend 0.5) -> plates 1.5x the v02 size (5760x3240, shown at
# 3840x2160, so zooms stay sharp) in edit/assets/p3/ (cards and tiles: make_assets_v03.py). v02's p/ and tiles/ are kept.
# Each source is first brought to ~4032 px on the long side (the 48 MP DNGs are halved; smaller photos are never pre-enlarged),
# upscaled 4x, then reduced to the plate size with Lanczos.
import os, sys, time, subprocess, numpy as np, torch
from PIL import Image
sys.path.insert(0, "tools"); import esrgan
torch.set_num_threads(4)
A = "edit/assets"; os.makedirs(f"{A}/p3", exist_ok=True)
ALL = ["IMG_6426", "IMG_6427", "IMG_6461", "IMG_6436", "2ee1beb9", "38af901c", "912ed0e8", "ACAE9274", "IMG_6433", "IMG_6423",
       "IMG_6429", "IMG_6430", "IMG_6437", "IMG_6438", "IMG_6439", "IMG_6440", "IMG_6435", "IMG_6419", "IMG_6420"]
def load(k):
    if os.path.exists(f"src/dl/{k}.jpg"): return Image.open(f"src/dl/{k}.jpg").convert("RGB")
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f"src/dl/{k}.DNG", "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True, check=True).stdout
    from io import BytesIO; return Image.open(BytesIO(raw)).convert("RGB")
m = esrgan.load("models/realesr-general-x4v3.pth", "models/realesr-general-wdn-x4v3.pth", 0.5)
only = sys.argv[1:] or ALL
for k in only:
    if os.path.exists(f"{A}/p3/{k}.jpg"): print(k, "done already", flush=True); continue
    t = time.time(); im = load(k); W, H = im.size
    s = min(1.0, 4032 / max(W, H)); inp = im.resize((round(W * s), round(H * s)), Image.LANCZOS) if s < 1 else im
    up = Image.fromarray(esrgan.upscale(m, inp))
    tgt = (5760, 3240) if W >= H else (2025, 3600)
    plate = up.resize((round(tgt[1] * W / H), tgt[1]) if W >= H else tgt, Image.LANCZOS)
    plate.save(f"{A}/p3/{k}.jpg", quality=90)
    print(k, (W, H), "->", inp.size, "x4 ->", plate.size, round(time.time() - t), "s", flush=True)
    del up, plate, inp, im
