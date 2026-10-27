# v03 assets from the upscaled plates (upscale_photos.py -> edit/assets/p3/): GTR-free booth card crops (cards3/), finale tiles
# (tiles3/: the 16 clear photos + 4 frames from the 4K videos). Creator's notes on v02: upscale every image, use clear images only.
# Dropped as unclear (motion blur at display size): IMG_6419, IMG_6420, IMG_6436.
import os, subprocess
from PIL import Image
from gtr_boxes import hits
A = "edit/assets"; os.makedirs(f"{A}/cards3", exist_ok=True); os.makedirs(f"{A}/tiles3", exist_ok=True)

def cut(k, x0, x1, y0, aspect, out, size):
    """crop plate k from x0..x1 (fractions) at the given w/h aspect starting at y0; refuse if it touches GTR"""
    im = Image.open(f"{A}/p3/{k}.jpg"); W, H = im.size
    w = (x1 - x0) * W; h = w / aspect
    if h > H: raise SystemExit(f"{k}: crop too tall")
    box = (x0, y0, x1, y0 + h / H)
    if box[3] > 1.0001: raise SystemExit(f"{k}: crop runs off the bottom")
    if hits(k, box): raise SystemExit(f"{k}: crop {box} touches GTR {hits(k, box)}")
    im.crop((round(x0 * W), round(y0 * H), round(x1 * W), round(y0 * H + h))).resize(size, Image.LANCZOS).save(out, quality=90)
    return [round(v, 3) for v in box]

# booth cards: inner 744x939 (shown at 2x)
CA = 744 / 939; log = {}
for k, x0, y0 in [("912ed0e8", 0.60, 0.29), ("38af901c", 0.12, 0.0), ("ACAE9274", 0.19, 0.0), ("IMG_6433", 0.18, 0.0)]:
    im = Image.open(f"{A}/p3/{k}.jpg"); W, H = im.size
    wf = min(1 - x0, CA * H / W) if W > H else 0.40
    log[f"card {k}"] = cut(k, x0, x0 + wf, y0, CA, f"{A}/cards3/{k}.jpg", (1488, 1878))

# finale tiles 270x384 (saved 540x768); landscape plates are cut full-height around a GTR-safe centre
TA = 270 / 384
TILE_X = {"IMG_6426": .36, "IMG_6427": .50, "IMG_6461": .35, "2ee1beb9": .40, "38af901c": .36, "ACAE9274": .35, "IMG_6433": .33,
          "IMG_6423": .44, "IMG_6429": .30, "IMG_6430": .50, "IMG_6437": .38, "IMG_6438": .37, "IMG_6439": .36, "IMG_6440": .42, "IMG_6435": .42}
for k, cx in TILE_X.items():
    W, H = Image.open(f"{A}/p3/{k}.jpg").size; wf = TA * H / W
    log[f"tile {k}"] = cut(k, cx - wf / 2, cx + wf / 2, 0.0, TA, f"{A}/tiles3/{k}.jpg", (540, 768))
log["tile 912ed0e8"] = cut("912ed0e8", 0.60, 1.0, 0.28, TA, f"{A}/tiles3/912ed0e8.jpg", (540, 768))

# four frames from the 4K videos (stage crop as v02's stage tile; booth crop = v_booth's GTR-free window)
def vframe(src, t, x, name):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(t), "-i", src, "-frames:v", "1",
                    "-vf", f"crop=1215:1728:{x}:216,scale=540:768:flags=lanczos", f"{A}/tiles3/{name}.jpg"], check=True)
vframe("proxy/IMG_6421.mov", 11.0, 900, "stage_a"); vframe("proxy/IMG_6421.mov", 6.2, 900, "stage_b")
vframe("proxy/IMG_6421.mov", 15.6, 900, "stage_c"); vframe("proxy/IMG_6425.mov", 2.0, 1110, "booth_v")
for k, v in log.items(): print(k, v)
