# v03 "cinematic lighting" composite. Same mattes and camera-matched plate motion as composite_bg.py, plus:
# - statue relight: deeper blacks, gold pop + specular glow, key light from the left lamp side, strong amber
#   back/rim light from the glowing doorway
# - plate: volumetric rays + haze from the doorway, flickering lamp glow, highlight bloom; animated on the
#   OUTPUT timeline so it keeps moving through the freeze frames (stills become short plate videos)
# - dust motes drifting through the light: a separate full-length alpha overlay (dust.webm)
# usage: python3 scripts/composite_cine.py bgx/plate_final.jpg edit/assets/v3
import cv2, numpy as np, os, sys, subprocess, json
PLATE, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
W, H, FPS, TOTAL = 1080, 1920, 30, 16.6
DAMP_T, DAMP_S, OVER = 0.45, 0.6, 1.3
# segment: (source first, source last, output start)
SEGS = {"segA": (306, 345, 0.0), "segB": (9, 88, 2.25), "segC": (150, 247, 4.91), "segD": (369, 401, 8.15), "segF": (402, 455, 11.34)}
# still: (source frame, output start, output end)
STILLS = {"frzA": (345, 1.31, 2.25), "frzE": (402, 9.21, 11.34), "frzG": (455, 13.11, TOTAL)}
DOOR = (0.5, 0.40)                       # doorway glow centre on the plate (fractions)
LAMPS = [(0.03, 0.44), (0.975, 0.44)]    # lamp flames on the plate

cap = cv2.VideoCapture("edit/src_1080.mp4")
frames = {}
need = sorted({f for a, b, _ in SEGS.values() for f in range(a, b + 1)} | {s for s, _, _ in STILLS.values()})
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

def alpha_for(fi, lo, hi):
    ms = [cv2.imread(f"bgx/masks/{j:05d}.png", 0) for j in (fi - 1, fi, fi + 1) if lo <= j <= hi and os.path.exists(f"bgx/masks/{j:05d}.png")]
    m = np.median(np.stack(ms), 0).astype(np.uint8) if len(ms) == 3 else cv2.imread(f"bgx/masks/{fi:05d}.png", 0)
    f = frames[fi]
    b_, g_, r_ = [f[..., k].astype(np.int16) for k in range(3)]
    rim_zone = (m > 20) & (cv2.erode(m, np.ones((61, 61), np.uint8)) < 128)
    sat_g = (g_ - np.maximum(r_, b_)) / np.maximum(g_, 1)
    green = ((g_ - r_ > 10) & (g_ - b_ > 6) & (g_ > 60) & (g_ < 200) & (sat_g > 0.08) & rim_zone).astype(np.uint8)   # foliage, not the grass-tinted white rock
    green = cv2.dilate(cv2.morphologyEx(green, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)), np.ones((5, 5), np.uint8))
    m = (m.astype(np.float32) * (1 - green)).astype(np.uint8)
    m = cv2.GaussianBlur(cv2.erode(m, np.ones((3, 3), np.uint8)), (0, 0), 1.2)
    return m.astype(np.float32) / 255.0

def bg_motion(prev, cur, aprev):
    g0, g1 = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY), cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY)
    keep = (cv2.dilate(aprev, np.ones((41, 41), np.uint8)) < 0.1).astype(np.uint8) * 255
    p0 = cv2.goodFeaturesToTrack(g0, 400, 0.01, 12, mask=keep)
    if p0 is None or len(p0) < 12: return np.eye(2, 3)
    p1, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, p0, None)
    good = st.ravel() == 1
    if good.sum() < 12: return np.eye(2, 3)
    M, _ = cv2.estimateAffinePartial2D(p0[good], p1[good], method=cv2.RANSAC, ransacReprojThreshold=2.0)
    return M if M is not None else np.eye(2, 3)

def plate_xy(fx, fy, sc, tx, ty):
    return W / 2 - sc * PW / 2 + tx + sc * PW * fx, H / 2 - sc * PH / 2 + ty + sc * PH * fy

def place_plate(sc, tx, ty):
    M = np.array([[sc, 0, W / 2 - sc * PW / 2 + tx], [0, sc, H / 2 - sc * PH / 2 + ty]], np.float32)
    return cv2.warpAffine(plate, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

# ---------------- plate lighting (animated on the output timeline) ----------------
hy, hx = np.mgrid[0:H // 2, 0:W // 2].astype(np.float32) * 2
def screen(base, add):
    return 255 - (255 - base) * (255 - np.clip(add, 0, 255)) / 255

def flicker(t, seed):
    return 0.82 + 0.1 * np.sin(t * 9.1 + seed) + 0.05 * np.sin(t * 23.7 + 2 * seed) + 0.03 * np.sin(t * 51.3 + 3 * seed)

def light_plate(bg, t, sc, tx, ty):
    out = bg.astype(np.float32)
    ox, oy = plate_xy(*DOOR, sc, tx, ty)
    dx, dy = hx - ox, hy - oy
    r = np.sqrt(dx * dx + dy * dy) + 1
    th = np.arctan2(dy, dx)
    rays = np.zeros_like(r)
    for n, ph0, v, w in ((7, 0.3, 0.05, 0.5), (13, 1.7, -0.08, 0.3), (23, 4.1, 0.11, 0.2)):
        rays += w * (0.5 + 0.5 * np.sin(n * th + ph0 + v * t * 6.28)) ** 3
    reach = 900 * sc
    fall = np.exp(-r / reach) * np.clip((r - 60 * sc) / (160 * sc), 0, 1)
    down = 0.55 + 0.45 * np.clip(dy / r, 0, 1)            # light spills forward/down onto the floor more than up
    beam = rays * fall * down * (0.85 + 0.15 * np.sin(t * 1.3))
    haze = np.exp(-(r / (420 * sc)) ** 2)
    glow = cv2.resize((beam * 150 + haze * 70).astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    for k, (fx, fy) in enumerate(LAMPS):                  # lamp flicker pools
        lx, ly = plate_xy(fx, fy, sc, tx, ty)
        lr = np.sqrt((hx - lx) ** 2 + (hy - ly) ** 2)
        glow += cv2.resize((np.exp(-(lr / (230 * sc)) ** 2) * 95 * flicker(t, k + 1)).astype(np.float32), (W, H))
    amber = np.array([0.42, 0.74, 1.0], np.float32)       # BGR
    out = screen(out, glow[..., None] * amber)
    # highlight bloom
    hi = np.clip(out.max(2) - 185, 0, 70)[..., None] / 70.0 * out
    out = screen(out, cv2.GaussianBlur(hi, (0, 0), 14) * 0.45)
    # cinematic falloff: darker floor edges and top so the doorway + statue carry the frame
    out *= (0.72 + 0.28 * np.exp(-((np.mgrid[0:H, 0:W][1] - W / 2) / (W * 0.55)) ** 2))[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)

# ---------------- statue relight ----------------
def relight(fg, a):
    f = fg.astype(np.float32) / 255.0
    f = np.clip((f ** 1.2 - 0.5) * 1.2 + 0.5, 0, 1)                       # deeper glossy blacks
    hsv = cv2.cvtColor((f * 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    gold = ((hsv[..., 0] > 12) & (hsv[..., 0] < 36) & (hsv[..., 1] > 80) & (hsv[..., 2] > 80)).astype(np.float32)
    gold = cv2.GaussianBlur(gold, (0, 0), 1.5)
    hsv[..., 1] = np.clip(hsv[..., 1] * (1 + 0.18 * gold), 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * (1 + 0.10 * gold), 0, 255)
    f = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    ys, xs = np.where(a > 0.5)
    if len(ys):
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        gx = np.clip((np.arange(W) - x0) / max(1, x1 - x0), 0, 1)
        gy = np.clip((np.arange(H) - y0) / max(1, y1 - y0), 0, 1)
        key = 0.80 + 0.32 * (1 - gx)[None, :] + 0.10 * (1 - gy)[:, None]   # warm key from the left lamp, a touch from above
        f *= key[..., None]
        f[..., 2] *= 1.06; f[..., 0] *= 0.9
    # back/rim light from the doorway: edge band, stronger on top-facing edges
    ab = cv2.GaussianBlur(a, (0, 0), 6)
    gyy = cv2.Sobel(ab, cv2.CV_32F, 0, 1, ksize=5)
    edge = np.clip(a - cv2.erode(a, np.ones((17, 17), np.uint8)), 0, 1)
    edge = cv2.GaussianBlur(edge, (0, 0), 3.5) * a
    top = np.clip(gyy / (np.abs(gyy).max() + 1e-6) * 3, 0, 1)            # alpha rising downward = top edge
    rim = edge * (0.25 + 0.95 * top)
    f += np.array([70, 165, 255], np.float32) * rim[..., None] * 1.0
    # specular glow on the gold
    spec = np.clip(f.max(2) - 200, 0, 55)[..., None] / 55.0 * f
    f = screen(f, cv2.GaussianBlur(spec, (0, 0), 5) * 0.35)
    return np.clip(f, 0, 255)

def statue_layer(fg, a):
    f = relight(fg, a)
    C = np.zeros((H, W, 3), np.float32); A = np.zeros((H, W), np.float32)
    def over(cs, as_):
        nonlocal C, A
        An = as_ + A * (1 - as_)
        C = np.where(An[..., None] > 1e-5, (cs * as_[..., None] + C * (A * (1 - as_))[..., None]) / np.maximum(An, 1e-5)[..., None], 0)
        A = An
    ys, xs = np.where(a > 0.5)
    if len(ys) and ys.max() < H - 12:
        yb = int(ys.max()); sel = ys > yb - 60; cx = xs[sel].mean(); w = max(80, (xs[sel].max() - xs[sel].min()) * 0.8)
        sh = np.zeros((H, W), np.float32)
        cv2.ellipse(sh, (int(cx + w * 0.15), int(yb - 4)), (int(w * 1.1), int(w * 0.16)), 0, 0, 360, 1.0, -1)  # key from the left: shadow falls right
        over(np.zeros((H, W, 3), np.float32), cv2.GaussianBlur(sh, (0, 0), w * 0.15) * 0.78)
        n = min(260, H - yb - 1)
        if n > 20:
            rf = np.zeros((H, W, 3), np.float32); ra = np.zeros((H, W), np.float32)
            rf[yb:yb + n] = cv2.GaussianBlur(f[yb - n:yb][::-1], (0, 0), 3)
            ra[yb:yb + n] = cv2.GaussianBlur(a[yb - n:yb][::-1] * np.linspace(0.25, 0, n)[:, None], (0, 0), 3)
            over(rf, ra)
    over(f, a)
    return np.dstack([np.clip(C, 0, 255), np.clip(A * 255, 0, 255)]).astype(np.uint8)

def enc(path):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                             "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", "-g", "10", path], stdin=subprocess.PIPE)
def enc_alpha(path):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                             "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-crf", "18", "-b:v", "0", "-row-mt", "1", "-cpu-used", "4", "-auto-alt-ref", "0", path], stdin=subprocess.PIPE)

# ---------------- plate motion (same as v02) ----------------
mot = {}
for name, (a, b, _) in SEGS.items():
    for fi in range(a + 1, b + 1):
        M = bg_motion(frames[fi - 1], frames[fi], alpha_for(fi - 1, a, b))
        mot[fi] = (np.sqrt(abs(np.linalg.det(M[:, :2]))), M[0, 2], M[1, 2])
state = {}
for name in ("segA", "segB", "segC", "segD", "segF"):
    a, b, _ = SEGS[name]
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

for name, (a, b, t0) in SEGS.items():
    e, ea = enc(f"{OUT}/{name}_bg.mp4"), enc_alpha(f"{OUT}/{name}_fg.webm")
    for fi in range(a, b + 1):
        sc_, tx_, ty_ = state[fi]
        t = t0 + (fi - a) / FPS
        e.stdin.write(light_plate(place_plate(sc_, tx_, ty_), t, sc_, tx_, ty_).tobytes())
        ea.stdin.write(statue_layer(frames[fi], alpha_for(fi, a, b)).tobytes())
    for p_ in (e, ea): p_.stdin.close(); p_.wait()
    print(name, "done", flush=True)

for name, (fi, t0, t1) in STILLS.items():
    sc_, tx_, ty_ = state[fi]
    base = place_plate(sc_, tx_, ty_)
    e = enc(f"{OUT}/{name}_bg.mp4")
    for n in range(int(np.ceil((t1 - t0) * FPS)) + 2):
        e.stdin.write(light_plate(base, t0 + n / FPS, sc_, tx_, ty_).tobytes())
    e.stdin.close(); e.wait()
    cv2.imwrite(f"{OUT}/{name}_fg.png", statue_layer(frames[fi], alpha_for(fi, fi - 1, fi + 1)))
    print(name, "done", flush=True)

# ---------------- dust motes (screen space, whole timeline) ----------------
rng = np.random.default_rng(7)
N = 110
P = dict(x=rng.uniform(0, W, N), y=rng.uniform(0, H, N), z=rng.uniform(0.3, 1.0, N),
         vy=rng.uniform(-14, -4, N), sw=rng.uniform(6, 22, N), sf=rng.uniform(0.2, 0.7, N), ph=rng.uniform(0, 6.28, N))
ea = enc_alpha(f"{OUT}/dust.webm")
for n in range(int(TOTAL * FPS) + 2):
    t = n / FPS
    acc = np.zeros((H, W), np.float32)
    x = (P["x"] + P["sw"] * np.sin(P["ph"] + t * P["sf"] * 6.28)) % W
    y = (P["y"] + P["vy"] * t * P["z"] * 3) % H
    for xi, yi, zi, phi in zip(x, y, P["z"], P["ph"]):
        b = (0.35 + 0.65 * zi) * (0.6 + 0.4 * np.sin(t * 2.3 + phi))
        cv2.circle(acc, (int(xi), int(yi)), max(1, int(1 + 3.2 * zi)), float(b), -1, lineType=cv2.LINE_AA)
    acc = cv2.GaussianBlur(acc, (0, 0), 1.6)
    # motes read where the light is: the doorway column and the lamps
    col = 0.35 + 0.65 * np.exp(-((np.arange(W) - W / 2) / 330.0) ** 2)
    al = np.clip(acc * col[None, :] * 0.9, 0, 1)
    rgba = np.zeros((H, W, 4), np.uint8); rgba[..., 0] = 150; rgba[..., 1] = 215; rgba[..., 2] = 255; rgba[..., 3] = (al * 255).astype(np.uint8)
    ea.stdin.write(rgba.tobytes())
ea.stdin.close(); ea.wait()
print("dust done")
