# v04 assets from the upscaled plates (upscale_photos.py -> edit/assets/p3/): GTR-free booth card crops (cards3/, as v03) and the
# finale photo wall (tiles4/: all 20 photos - v03's 16 + the creator's four added photos; no video frames).
# Left out as unclear (motion blur at display size): IMG_6419, IMG_6420, IMG_6436.
import os, subprocess
from PIL import Image
from gtr_boxes import hits
A = "edit/assets"; os.makedirs(f"{A}/cards3", exist_ok=True); os.makedirs(f"{A}/tiles4", exist_ok=True)

def cut(k, x0, x1, y0, aspect, out, size, write=True):
    """crop plate k from x0..x1 (fractions) at the given w/h aspect starting at y0; refuse if it touches GTR"""
    im = Image.open(f"{A}/p3/{k}.jpg"); W, H = im.size
    w = (x1 - x0) * W; h = w / aspect
    if h > H + 1: raise SystemExit(f"{k}: crop too tall")
    h = min(h, H)
    box = (x0, y0, x1, y0 + h / H)
    if box[3] > 1.0001: raise SystemExit(f"{k}: crop runs off the bottom")
    if hits(k, box): raise SystemExit(f"{k}: crop {box} touches GTR {hits(k, box)}")
    im.crop((round(x0 * W), round(y0 * H), round(x1 * W), round(y0 * H + h))).resize(size, Image.LANCZOS).save(out, quality=90)
    return [round(v, 3) for v in box]

# booth cards: inner 744x939 (shown at 2x)
CA = 744 / 939; log = {}
for k, x0, y0 in [("912ed0e8", 0.62, 0.29), ("38af901c", 0.12, 0.0), ("ACAE9274", 0.19, 0.0), ("IMG_6433", 0.18, 0.0)]:
    im = Image.open(f"{A}/p3/{k}.jpg"); W, H = im.size
    wf = min(1 - x0, CA * H / W) if W > H else 1 - x0
    log[f"card {k}"] = cut(k, x0, x0 + wf, y0, CA, f"{A}/cards3/{k}.jpg", (1488, 1878))

# finale tiles 270x384 (saved 540x768): landscape plates cut full-height (or from y0 down) around a GTR-safe centre
TA = 270 / 384
TILE = {"IMG_6426": (.36, 0), "IMG_6427": (.50, 0), "IMG_6461": (.35, 0), "2ee1beb9": (.40, 0), "38af901c": (.36, 0), "ACAE9274": (.35, 0),
        "IMG_6433": (.33, 0), "IMG_6423": (.44, 0), "IMG_6429": (.30, 0), "IMG_6430": (.50, 0), "IMG_6437": (.38, 0), "IMG_6438": (.37, 0),
        "IMG_6439": (.36, 0), "IMG_6440": (.42, 0), "IMG_6435": (.42, 0),
        "hall_handout": (.40, 0), "booth_visitors": (.52, 0.06), "hall_keychain": (.36, 0), "booth_handover": (.55, 0)}
for k, (cx, y0) in TILE.items():
    W, H = Image.open(f"{A}/p3/{k}.jpg").size; wf = TA * H * (1 - y0) / W
    log[f"tile {k}"] = cut(k, cx - wf / 2, cx + wf / 2, y0, TA, f"{A}/tiles4/{k}.jpg", (540, 768))
log["tile 912ed0e8"] = cut("912ed0e8", 0.62, 1.0, 0.28, TA, f"{A}/tiles4/912ed0e8.jpg", (540, 768))
for k, v in log.items(): print(k, v)
