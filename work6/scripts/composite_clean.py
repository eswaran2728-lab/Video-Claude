# v04 "clean" composite: fixes the glitchy look of v03.
# - source: flow-aligned temporal denoise (prev/next frames averaged onto the current one) + light sharpening
# - matte: neighbour masks warped onto the current frame and averaged (no edge boiling), guided filter
#   against the cleaned frame, 1px choke, edge colour decontamination (no sky/park halo)
# - gentler relight: mild contrast, gold pop in float, soft inner backlight from a blurred matte (it no longer
#   traces jagged edges); smoothed plate motion; no dust, no grain
# usage: python3 scripts/composite_clean.py bgx/plate_final.jpg edit/assets/v4
import cv2, numpy as np, os, sys, subprocess, json
PLATE, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
W, H, FPS, TOTAL = 1080, 1920, 30, 16.6
DAMP_T, DAMP_S, OVER = 0.45, 0.6, 1.3
# segment: (source first, source last, output start)
SEGS = {"segA": (306, 345, 0.0), "segB": (9, 88, 2.25), "segC": (150, 247, 4.91), "segD": (369, 401, 8.15), "segF": (402, 418, 11.34)}  # v04: F ends on 13.93 s, the last frame with a clean face
# still: (source frame, output start, output end)
STILLS = {"frzA": (345, 1.31, 2.25), "frzE": (402, 9.21, 11.34), "frzG": (418, 11.9, TOTAL)}
DOOR = (0.5, 0.40)                       # doorway glow centre on the plate (fractions)
LAMPS = [(0.03, 0.44), (0.975, 0.44)]    # lamp flames on the plate

cap = cv2.VideoCapture("edit/src_1080.mp4")
frames = {}
need = sorted({f for a, b, _ in SEGS.values() for f in range(a - 2, b + 3)} | {s + d for s, _, _ in STILLS.values() for d in (-2, -1, 0, 1, 2)})
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

def raw_alpha(fi):
    m = cv2.imread(f"bgx/masks/{fi:05d}.png", 0)
    if m is None: return None
    f = frames[fi]
    b_, g_, r_ = [f[..., k].astype(np.int16) for k in range(3)]
    rim_zone = (m > 20) & (cv2.erode(m, np.ones((61, 61), np.uint8)) < 128)
    sat_g = (g_ - np.maximum(r_, b_)) / np.maximum(g_, 1)
    green = ((g_ - r_ > 10) & (g_ - b_ > 6) & (g_ > 60) & (g_ < 200) & (sat_g > 0.08) & rim_zone).astype(np.uint8)   # foliage, not the grass-tinted white rock
    green = cv2.dilate(cv2.morphologyEx(green, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)), np.ones((5, 5), np.uint8))
    return m.astype(np.float32) / 255.0 * (1 - green)

_flow = {}
def flow(src, dst):
    """dense flow mapping dst pixels -> src pixels (half-res Farneback, upsampled)"""
    if (src, dst) not in _flow:
        if len(_flow) > 16: _flow.clear()
        g0 = cv2.cvtColor(cv2.resize(frames[src], (540, 960)), cv2.COLOR_BGR2GRAY)
        g1 = cv2.cvtColor(cv2.resize(frames[dst], (540, 960)), cv2.COLOR_BGR2GRAY)
        fl = cv2.calcOpticalFlowFarneback(g1, g0, None, 0.5, 4, 25, 3, 5, 1.1, 0)
        _flow[(src, dst)] = cv2.resize(fl, (W, H)) * 2
    return _flow[(src, dst)]
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
def warp_to(img, src, dst):
    fl = flow(src, dst)
    return cv2.remap(img, XX + fl[..., 0], YY + fl[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

_clean = {}
def clean(fi):
    """temporal denoise: neighbours aligned onto fi, averaged where they agree, then a light unsharp"""
    if fi in _clean: return _clean[fi]
    if len(_clean) > 8: _clean.clear()
    cur = frames[fi].astype(np.float32); acc = cur * 2; wsum = np.full(cur.shape[:2], 2, np.float32)
    for nb in (fi - 1, fi + 1):
        if nb not in frames: continue
        wp = warp_to(frames[nb].astype(np.float32), nb, fi)
        w = np.exp(-(np.abs(wp - cur).mean(2) / 12.0) ** 2)      # ignore where alignment failed
        acc += wp * w[..., None]; wsum += w
    out = acc / wsum[..., None]
    out = cv2.addWeighted(out, 1.35, cv2.GaussianBlur(out, (0, 0), 1.1), -0.35, 0)
    _clean[fi] = np.clip(out, 0, 255)
    return _clean[fi]

def alpha_for(fi, lo, hi):
    acc, ws = None, 0.0
    for nb, w in ((fi - 2, 0.5), (fi - 1, 1.0), (fi, 2.0), (fi + 1, 1.0), (fi + 2, 0.5)):
        if nb < lo - 2 or nb > hi + 2 or nb not in frames: continue
        m = raw_alpha(nb)
        if m is None: continue
        m = m if nb == fi else warp_to(m, nb, fi)
        acc = m * w if acc is None else acc + m * w; ws += w
    a = acc / ws
    guide = clean(fi).astype(np.uint8)
    a = cv2.ximgproc.guidedFilter(guide, (a * 255).astype(np.uint8), 5, 120).astype(np.float32) / 255.0
    a = np.clip((a - 0.18) / 0.77, 0, 1)                               # ~1-2px choke: drops the old-background fringe
    return cv2.GaussianBlur(a, (0, 0), 0.7)

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
    f = fg.astype(np.float32)
    # edge decontamination: edge pixels take the colour of the statue just inside the edge
    core = (a > 0.97).astype(np.float32)
    num = cv2.GaussianBlur(f * core[..., None], (0, 0), 4); den = cv2.GaussianBlur(core, (0, 0), 4)[..., None]
    inner = num / np.maximum(den, 1e-4)
    band = ((a < 0.97) & (den[..., 0] > 0.02)).astype(np.float32)[..., None]
    f = f * (1 - band) + inner * band
    f = f / 255.0
    f = np.clip((f ** 1.06 - 0.5) * 1.08 + 0.5, 0, 1) * 255            # mild contrast, blacks stay detailed
    lum = (f * np.array([0.114, 0.587, 0.299], np.float32)).sum(2, keepdims=True)
    hsv = cv2.cvtColor(f / 255.0, cv2.COLOR_BGR2HSV)                     # float: no banding
    gold = ((hsv[..., 0] > 24) & (hsv[..., 0] < 72) & (hsv[..., 1] > 0.3) & (hsv[..., 2] > 0.3)).astype(np.float32)
    gold = cv2.GaussianBlur(gold, (0, 0), 1.5)[..., None]
    f = lum + (f - lum) * (1 + 0.15 * gold)
    ys, xs = np.where(a > 0.5)
    if len(ys):
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        gx = np.clip((np.arange(W) - x0) / max(1, x1 - x0), 0, 1)
        gy = np.clip((np.arange(H) - y0) / max(1, y1 - y0), 0, 1)
        key = 0.9 + 0.2 * (1 - gx)[None, :] + 0.06 * (1 - gy)[:, None]     # soft warm key from the left lamp
        f *= key[..., None]
        f[..., 2] *= 1.04; f[..., 0] *= 0.93
    # soft backlight: an inner glow from a heavily blurred matte, strongest on top-facing edges
    ab = cv2.GaussianBlur(a, (0, 0), 9)
    inner_glow = np.clip(a - ab, 0, 1) * 2.2 * a
    gyy = cv2.Sobel(cv2.GaussianBlur(a, (0, 0), 12), cv2.CV_32F, 0, 1, ksize=5)
    top = np.clip(gyy / (np.abs(gyy).max() + 1e-6) * 3, 0, 1)
    f += np.array([60, 140, 230], np.float32) * (inner_glow * (0.3 + 0.7 * top))[..., None] * 0.5
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
        M = bg_motion(frames[fi - 1], frames[fi], raw_alpha(fi - 1))
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
    arr = np.array([[p[1], p[2] * k, p[3] * k] for p in path])
    if len(arr) > 9:                                   # smooth out tracking jitter, keep the start (continuity) fixed
        pad = np.pad(arr, ((4, 4), (0, 0)), mode="edge")
        sm = np.stack([np.convolve(pad[:, j], np.ones(9) / 9, "valid") for j in range(3)], 1)
        sm += arr[0] - sm[0]
        arr = sm
    for (fi, _, _, _), (sc_, tx_, ty_) in zip(path, arr):
        state[fi] = (max(sc_, 1 / OVER * 1.02), tx_, ty_)

ONLY = set(os.environ.get("ONLY", "").split(",")) - {""}
for name, (a, b, t0) in SEGS.items():
    if ONLY and name not in ONLY: continue
    e, ea = enc(f"{OUT}/{name}_bg.mp4"), enc_alpha(f"{OUT}/{name}_fg.webm")
    for fi in range(a, b + 1):
        sc_, tx_, ty_ = state[fi]
        t = t0 + (fi - a) / FPS
        e.stdin.write(light_plate(place_plate(sc_, tx_, ty_), t, sc_, tx_, ty_).tobytes())
        ea.stdin.write(statue_layer(clean(fi), alpha_for(fi, a, b)).tobytes())
    for p_ in (e, ea): p_.stdin.close(); p_.wait()
    print(name, "done", flush=True)

for name, (fi, t0, t1) in STILLS.items():
    if ONLY and name not in ONLY: continue
    sc_, tx_, ty_ = state[fi]
    base = place_plate(sc_, tx_, ty_)
    e = enc(f"{OUT}/{name}_bg.mp4")
    for n in range(int(np.ceil((t1 - t0) * FPS)) + 2):
        e.stdin.write(light_plate(base, t0 + n / FPS, sc_, tx_, ty_).tobytes())
    e.stdin.close(); e.wait()
    cv2.imwrite(f"{OUT}/{name}_fg.png", statue_layer(clean(fi), alpha_for(fi, fi - 1, fi + 1)))
    print(name, "done", flush=True)

print("all done")
