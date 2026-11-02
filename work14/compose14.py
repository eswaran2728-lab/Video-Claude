# Statue plate for the reel: the real statue (BiRefNet cut-out, hand removed - cutout_lib.clean_mask) composited on a
# designed dark "3D-printer bed" background (radial glow, perspective grid floor), cyan rim light so the black PETG reads on
# dark, the title SANGILI KARUPPAR set BEHIND the statue in the print scene, and the layer-by-layer print reveal
# (statue appears from the base up under a glowing nozzle line; above the line only a faint slicer-style outline).
# Overlays (captions, labels, ruler, reference picture) are HTML in build14.py. -> edit/assets/v/plate.mp4 (no audio)
import json, subprocess, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
import plan14 as P
from cutout_lib import clean_mask
W, H, FPS = 1080, 1920, 30; N = int(round(P.TOTAL * FPS))
CYAN = np.array([255, 214, 54], np.float32)            # BGR of #36d6ff
cap = cv2.VideoCapture("proxy/src30.mov")
_cache = {}


def src(i):
    if i not in _cache:
        cap.set(1, i); ok, f = cap.read(); m = cv2.imread(f"masks/{i:05d}.png", 0)
        _cache[i] = (f, clean_mask(f, m))
        if len(_cache) > 80: _cache.pop(next(iter(_cache)))
    return _cache[i]


# ---- background ----
def make_bg():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - 540) / 900) ** 2 + ((yy - 900) / 1100) ** 2)
    base = np.clip(1 - r, 0, 1)[..., None]
    bg = np.array([18, 13, 11], np.float32) * (1 - base) + np.array([52, 40, 30], np.float32) * base   # deep blue-charcoal
    img = bg.copy(); HZ = 1290                                                                    # horizon of the bed
    grid = np.zeros((H, W), np.float32)
    for k in range(-14, 15):                                                                     # converging lines
        x_far = 540 + k * 38; x_near = 540 + k * 170
        cv2.line(grid, (int(x_far), HZ), (int(x_near), H), 1.0, 2, cv2.LINE_AA)
    y = HZ; step = 14.0
    while y < H:                                                                                 # receding cross lines
        cv2.line(grid, (0, int(y)), (W, int(y)), 1.0, 2, cv2.LINE_AA); y += step; step *= 1.22
    fade = np.clip((yy - HZ) / 420, 0, 1) * np.clip(1 - np.abs(xx - 540) / 700, 0, 1)
    img += (grid * fade * 0.22)[..., None] * CYAN
    glow = np.exp(-(((xx - 540) / 420) ** 2 + ((yy - 1470) / 70) ** 2))[..., None]               # light pool on the bed
    img += glow * np.array([90, 75, 40], np.float32)
    return np.clip(img, 0, 255)


BG = make_bg()
FONT = ImageFont.truetype("../work13/edit/assets/fonts/InterDisplay-Black.otf", 170)
def title_layer():
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
    for txt, y in (("SANGILI", 560), ("KARUPPAR", 740)):
        w = d.textlength(txt, font=FONT); d.text(((W - w) / 2, y), txt, font=FONT, fill=255)
    return np.array(im, np.float32) / 255
TITLE = title_layer()

# ---- statue playback per scene ----
LAYOUT = {None: dict(h=1060, bottom=1560), "low": dict(h=760, bottom=1640), "small": dict(h=640, bottom=1110), "mid": dict(h=860, bottom=1560)}


def items_for(scene):
    out = []
    for it in scene["statue"] or []:
        if it[0] == "still": out.append(("still", round(it[1] * FPS), it[2]))
        else: a, b, sp = it; out.append(("clip", (round(a * FPS), round(b * FPS)), (b - a) / sp))
    return out


def geometry(frames):
    """median bbox of the cleaned mask over the item's frames -> scale + anchor (keeps the statue steady, no jitter)"""
    bb = []
    for i in frames[::3] or frames:
        m = src(i)[1]; ys, xs = np.where(m > 128)
        if len(ys): bb.append((xs.min(), xs.max(), ys.min(), ys.max()))
    b = np.median(np.array(bb), axis=0); return dict(cx=(b[0] + b[1]) / 2, top=b[2], bot=b[3])


def statue_at(scene, t):
    """(frame index, geometry) for output time t inside the scene; the last item holds if the scene runs longer"""
    rel = t - scene["t0"]
    for kind, rng, dur in scene["_items"]:
        if rel < dur or (kind, rng, dur) == scene["_items"][-1]:
            if kind == "still": return rng, scene["_geo"][str(rng)], min(rel, dur) / max(dur, 1e-6)
            a, b = rng; i = min(b, a + int(round(min(rel, dur) / dur * (b - a)))); return i, scene["_geo"][str(rng)], 0
        rel -= dur
    return None


for sc in P.SCENES:
    sc["_items"] = items_for(sc); sc["_geo"] = {}
    for kind, rng, dur in sc["_items"]:
        fr = [rng] if kind == "still" else list(range(rng[0], rng[1] + 1)); sc["_geo"][str(rng)] = geometry(fr)

meta = {"scenes": []}
enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-g", "15", "edit/assets/v/plate.mp4"], stdin=subprocess.PIPE)
ease = lambda u: 1 - (1 - u) ** 3
for n in range(N):
    t = n / FPS; sc = next(s for s in P.SCENES if s["t0"] <= t < s["t1"] + 1e-6) if t < P.TOTAL else P.SCENES[-1]
    img = BG.copy()
    if sc["name"] == "print":                                     # title behind the statue, fades in on "Karuppar"
        a = np.clip((t - P.W["karuppar"]) / 0.5, 0, 1) * 0.16
        if a > 0: img = img * (1 - TITLE[..., None] * a) + TITLE[..., None] * a * 235
    st = statue_at(sc, t) if sc["statue"] else None
    if st:
        i, geo, still_u = st; f, m = src(i); L = LAYOUT[sc.get("layout")]
        push = 1 + 0.035 * still_u                                # slow push on held frames
        s = L["h"] / (geo["bot"] - geo["top"]) * push
        M = np.float32([[s, 0, 540 - geo["cx"] * s], [0, s, L["bottom"] - geo["bot"] * s]])
        fw = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4); mw = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR).astype(np.float32) / 255
        fw = np.clip((fw.astype(np.float32) - 6) * 1.12, 0, 255)  # slight contrast lift on the black PETG
        rim = np.clip(cv2.GaussianBlur(mw, (0, 0), 9) - mw * 0.9, 0, 1)[..., None]
        reveal = sc.get("reveal")
        if reveal and t < reveal[1] + 0.4:
            u = ease(np.clip((t - reveal[0]) / (reveal[1] - reveal[0]), 0, 1))
            ys = np.where(mw.max(axis=1) > 0.3)[0]; top, bot = (ys.min(), ys.max()) if len(ys) else (0, H)
            yl = bot - u * (bot - top) if u < 1 else -100
            yy = np.arange(H, dtype=np.float32)[:, None]
            below = np.clip((yy - yl) / 3, 0, 1)                  # printed part
            edge = cv2.morphologyEx((mw > 0.5).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32)
            ghost = (edge * 0.45 + mw * 0.05) * (1 - below)
            a = (mw * below)[..., None]
            img = img * (1 - a) + fw * a
            img += (rim * below[..., None]) * CYAN * 0.55
            img += ghost[..., None] * CYAN
            if u < 1:                                             # nozzle line + glow across the statue width at yl
                xs = np.where(mw[int(np.clip(yl, 0, H - 1))] > 0.2)[0]
                x0, x1 = (xs.min(), xs.max()) if len(xs) else (440, 640)
                band = np.exp(-((yy - yl) / 5) ** 2) * 0.9 + np.exp(-((yy - yl) / 26) ** 2) * 0.35
                xm = np.zeros((1, W), np.float32); xm[0, max(0, x0 - 30):min(W, x1 + 30)] = 1; xm = cv2.GaussianBlur(xm, (0, 0), 12)
                img += (band * xm)[..., None] * CYAN
                nx = x0 + (x1 - x0) * (0.5 + 0.5 * np.sin(t * 9.0)); ny = int(yl) - 6           # the nozzle head
                pts = np.array([[nx - 26, ny - 44], [nx + 26, ny - 44], [nx + 9, ny], [nx - 9, ny]], np.int32)
                cv2.fillConvexPoly(img, pts, (205, 205, 210), cv2.LINE_AA); cv2.circle(img, (int(nx), ny + 2), 5, (255, 240, 170), -1, cv2.LINE_AA)
        else:
            a = mw[..., None]; img = img * (1 - a) + fw * a; img += rim * CYAN * 0.55
    enc.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
    if n % 150 == 0: print("frame", n, N, sc["name"], flush=True)
enc.stdin.close(); enc.wait()
json.dump({"total": P.TOTAL, "frames": N, "scenes": [{k: v for k, v in s.items() if not k.startswith("_")} for s in P.SCENES]}, open("edit/plate_meta.json", "w"), indent=1)
print("plate done", N)
