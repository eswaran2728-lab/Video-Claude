# Replace the park background with a temple plate.
# - alpha: BiRefNet-lite masks (bgx/masks), 3-frame temporal median, 1px erode + feather
# - camera feel: similarity motion of the ORIGINAL background (LK features outside the statue) is
#   accumulated per segment and applied, damped, to the new plate, so orbit/push-ins still read
# - grounding: soft contact shadow under the lowest statue pixels; warm light-wrap on the edges
# usage: python3 scripts/composite_bg.py <plate.jpg> <outdir>
import cv2, numpy as np, os, sys, subprocess
PLATE, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
DAMP_T, DAMP_S, OVER = 0.45, 0.6, 1.3
SEGS = {"segA": (306, 345), "segB": (9, 88), "segC": (150, 247), "segD": (369, 401), "segF": (402, 455)}
STILLS = {"frzA": 345, "frzE": 402, "frzG": 455}

cap = cv2.VideoCapture("edit/src_1080.mp4")
frames = {}
need = sorted({f for a, b in SEGS.values() for f in range(a, b + 1)} | set(STILLS.values()))
i = 0
while True:
    ok, f = cap.read()
    if not ok or i > max(need): break
    if i in need: frames[i] = f
    i += 1

plate = cv2.imread(PLATE)
ph, pw = plate.shape[:2]
s0 = max(W * OVER / pw, H * OVER / ph)
plate = cv2.resize(plate, (int(pw * s0), int(ph * s0)), interpolation=cv2.INTER_LANCZOS4)
PH, PW = plate.shape[:2]

def mask(fi):
    m = cv2.imread(f"bgx/masks/{fi:05d}.png", 0)
    return m

def alpha_for(fi, lo, hi):
    ms = [mask(j) for j in (fi - 1, fi, fi + 1) if lo <= j <= hi and os.path.exists(f"bgx/masks/{j:05d}.png")]
    m = np.median(np.stack(ms), 0).astype(np.uint8) if len(ms) == 3 else mask(fi)
    m = cv2.erode(m, np.ones((3, 3), np.uint8))
    m = cv2.GaussianBlur(m, (0, 0), 1.2)
    return m.astype(np.float32) / 255.0

def bg_motion(prev, cur, mprev):
    g0, g1 = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY), cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY)
    keep = (cv2.dilate(mprev, np.ones((41, 41), np.uint8)) < 0.1).astype(np.uint8) * 255
    p0 = cv2.goodFeaturesToTrack(g0, 400, 0.01, 12, mask=keep)
    if p0 is None or len(p0) < 12: return np.eye(2, 3)
    p1, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, p0, None)
    good = st.ravel() == 1
    if good.sum() < 12: return np.eye(2, 3)
    M, _ = cv2.estimateAffinePartial2D(p0[good], p1[good], method=cv2.RANSAC, ransacReprojThreshold=2.0)
    return M if M is not None else np.eye(2, 3)

def place_plate(sc, tx, ty):
    # plate centred, scaled by sc about the frame centre, shifted by (tx, ty)
    M = np.array([[sc, 0, W / 2 - sc * PW / 2 + tx], [0, sc, H / 2 - sc * PH / 2 + ty]], np.float32)
    return cv2.warpAffine(plate, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def comp(fg, a, bg):
    a3 = a[..., None]
    out = bg.astype(np.float32)
    f = fg.astype(np.float32)
    # warm the overcast-daylight statue toward the lamp-lit plate
    f[..., 2] *= 1.07; f[..., 1] *= 1.0; f[..., 0] *= 0.88
    ys, xs = np.where(a > 0.5)
    if len(ys) and ys.max() < H - 12:
        yb = int(ys.max()); sel = ys > yb - 60; cx = xs[sel].mean(); w = max(80, (xs[sel].max() - xs[sel].min()) * 0.8)
        # soft reflection on the polished floor
        n = min(260, H - yb - 1)
        if n > 20:
            rf = f[yb - n:yb][::-1]; ra = a[yb - n:yb][::-1] * np.linspace(0.22, 0, n)[:, None]
            rf = cv2.GaussianBlur(rf, (0, 0), 3); ra = cv2.GaussianBlur(ra, (0, 0), 3)
            seg = out[yb:yb + n]; seg[:] = seg * (1 - ra[..., None]) + rf * ra[..., None]
        # contact shadow
        sh = np.zeros((H, W), np.float32)
        cv2.ellipse(sh, (int(cx), int(yb - 4)), (int(w), int(w * 0.14)), 0, 0, 360, 1.0, -1)
        sh = cv2.GaussianBlur(sh, (0, 0), w * 0.15)
        out *= (1 - 0.7 * sh)[..., None]
    # warm rim/light-wrap from the glowing doorway on the statue's edge
    edge = np.clip(a - cv2.erode(a, np.ones((9, 9), np.uint8)), 0, 1)[..., None]
    blur_bg = cv2.GaussianBlur(bg, (0, 0), 10).astype(np.float32)
    rim = blur_bg * 0.6 + np.array([60, 140, 230], np.float32) * 0.4
    f = f * (1 - 0.45 * edge) + rim * 0.45 * edge
    res = f * a3 + out * (1 - a3)
    return np.clip(res, 0, 255).astype(np.uint8)

def enc(path):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                             "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", "-g", "10", path], stdin=subprocess.PIPE)

# pass 1: original-background motion per frame
mot = {}
for name, (a, b) in SEGS.items():
    for fi in range(a + 1, b + 1):
        M = bg_motion(frames[fi - 1], frames[fi], alpha_for(fi - 1, a, b))
        mot[fi] = (np.sqrt(abs(np.linalg.det(M[:, :2]))), M[0, 2], M[1, 2])
# pass 2: accumulate (continuing across source-contiguous segments), fit inside the plate margin
state = {}
for name, (a, b) in [(k, SEGS[k]) for k in ("segA", "segB", "segC", "segD", "segF")]:
    sc, tx, ty = state.get(a - 1, (1.0, 0.0, 0.0))
    path = []
    for fi in range(a, b + 1):
        if fi in mot and fi - 1 >= a:
            ds, dx, dy = mot[fi]; sc *= ds ** DAMP_S; tx += dx * DAMP_T; ty += dy * DAMP_T
        path.append((fi, sc, tx, ty))
    mx = max(abs(p[2]) for p in path) / (W * (OVER - 1) / 2 * 0.85 + 1e-6)
    my = max(abs(p[3]) for p in path) / (H * (OVER - 1) / 2 * 0.85 + 1e-6)
    k = 1 / max(1, mx, my)
    for fi, sc_, tx_, ty_ in path:
        state[fi] = (max(sc_, 1 / OVER * 1.02), tx_ * k, ty_ * k)
    e = enc(f"{OUT}/{name}.mp4")
    for fi in range(a, b + 1):
        sc_, tx_, ty_ = state[fi]
        e.stdin.write(comp(frames[fi], alpha_for(fi, a, b), place_plate(sc_, tx_, ty_)).tobytes())
    e.stdin.close(); e.wait(); print(name, "done k=%.2f" % k, flush=True)

for name, fi in STILLS.items():
    sc, tx, ty = state.get(fi, state.get(fi - 1, (1.0, 0.0, 0.0)))
    lo, hi = (fi - 1, fi + 1)
    img = comp(frames[fi], alpha_for(fi, lo, hi), place_plate(sc, tx, ty))
    cv2.imwrite(f"{OUT}/{name}.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 96])
print("stills done")
