# Picture plate: every segment of plan16 cut, speed-adjusted, zoomed (sub-pixel, from the 4K tone-mapped copies for M)
# and graded, then joined with an end freeze → edit/assets/v/plate.mp4 (1080x1920, 30 fps, silent).
# Usage: python3 plate16.py [draft]   ("draft" = faster encode)
import subprocess, sys, os, numpy as np, cv2
import plan16 as P
W, H = 1080, 1920
SRC = {"M": [("inter/M_05_25_4k.mp4", 5.4, 24.8), ("inter/M_40_43_4k.mp4", 39.8, 42.8)], "L": [("proxy/frame_lights.mp4", 0.0, 29.36)]}
os.makedirs("edit/assets/v", exist_ok=True); os.makedirs("seg", exist_ok=True)

def ease(u, kind):
    u = min(max(u, 0.0), 1.0)
    return u if kind == "lin" else (u * u * (3 - 2 * u) if kind == "io" else 0.0)

def zoom_at(keys, st):
    if st <= keys[0][0]: return keys[0][1:4]
    for (t0, z0, x0, y0, _), (t1, z1, x1, y1, k) in zip(keys, keys[1:]):
        if t0 <= st <= t1:
            if k == "hold": return (z0, x0, y0) if st < t1 else (z1, x1, y1)
            e = ease((st - t0) / max(t1 - t0, 1e-6), k); return (z0 + (z1 - z0) * e, x0 + (x1 - x0) * e, y0 + (y1 - y0) * e)
    return keys[-1][1:4]

class reader:
    """Streams decoded frames; get(i) returns frame i (i never decreases), holding only the current frame in memory."""
    def __init__(self, path, ss, n_src, w, h):
        cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{ss:.4f}", "-i", path, "-frames:v", str(n_src), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE); self.w, self.h = w, h; self.i = -1; self.cur = None; self.prev = None
    def get(self, i):
        while self.i < i:
            b = self.p.stdout.read(self.w * self.h * 3)
            if len(b) < self.w * self.h * 3: break
            self.prev = self.cur
            self.cur = np.frombuffer(b, np.uint8).reshape(self.h, self.w, 3); self.i += 1
        return self.cur
    def blend(self, pos):
        """Frame at fractional index pos: cross-blend of the two neighbouring frames (smooth slow motion)."""
        i0 = int(np.floor(pos)); w = pos - i0
        if w < 1e-3: return self.get(i0)
        b1 = self.get(i0 + 1); b0 = self.prev if self.prev is not None and self.i == i0 + 1 else b1
        return cv2.addWeighted(b0, 1 - w, b1, w, 0)
    def close(self): self.p.stdout.close(); self.p.wait()

def probe(path):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return tuple(int(x) for x in o.strip().split(","))

CARD = None
def hook_card(img):
    """Lit frame as a rounded card with a soft shadow over a blurred, darkened copy of the same frame."""
    global CARD
    cw, ch = int(round(W * P.HOOK_CARD)), int(round(H * P.HOOK_CARD)); x0, y0 = P.HOOK_XY
    if CARD is None:
        m = np.zeros((ch, cw), np.uint8); r = 34
        cv2.rectangle(m, (r, 0), (cw - r, ch), 255, -1); cv2.rectangle(m, (0, r), (cw, ch - r), 255, -1)
        for cx, cy in ((r, r), (cw - r, r), (r, ch - r), (cw - r, ch - r)): cv2.circle(m, (cx, cy), r, 255, -1, cv2.LINE_AA)
        sh = np.zeros((H, W), np.float32)
        sh[y0 + 18:min(H, y0 + 18 + ch), x0:x0 + cw] = (m[:min(ch, H - y0 - 18)] / 255.0)
        CARD = (m.astype(np.float32)[..., None] / 255.0, cv2.GaussianBlur(sh, (0, 0), 28)[..., None])
    mask, shadow = CARD
    bg = cv2.GaussianBlur(cv2.resize(img, (W // 4, H // 4), interpolation=cv2.INTER_AREA), (0, 0), 9)
    bg = cv2.resize(bg, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) * 0.42
    bg *= (1 - 0.55 * shadow)
    fg = cv2.resize(img, (cw, ch), interpolation=cv2.INTER_AREA).astype(np.float32)
    y1 = min(H, y0 + ch); hh = y1 - y0
    reg = bg[y0:y1, x0:x0 + cw]; bg[y0:y1, x0:x0 + cw] = reg * (1 - mask[:hh]) + fg[:hh] * mask[:hh]
    return np.clip(bg, 0, 255).astype(np.uint8)

def render_seg(s, draft):
    path, base, _ = next(x for x in SRC[s["src"]] if x[1] <= s["a"] and s["b"] <= x[2] + 0.05)
    w, h = probe(path); k = w / W                      # source pixels per output pixel at Z=1
    n_src = int(np.ceil((s["b"] - s["a"]) * P.FPS)) + 2
    rd = reader(path, s["a"] - base, n_src, w, h)
    out = f"seg/{s['name']}.mp4"
    enc = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(P.FPS), "-i", "-",
           "-vf", P.GRADE[s["src"]] + ",format=yuv420p", "-c:v", "libx264", "-crf", "18" if draft else "14", "-preset", "veryfast" if draft else "slow", out]
    e = subprocess.Popen(enc, stdin=subprocess.PIPE)
    for i in range(s["n"]):
        st = s["a"] + i / P.FPS * s["speed"]            # source time of this output frame
        fi = int(round((st - s["a"]) * P.FPS))
        z, cx, cy = zoom_at(P.ZOOM[s["name"]], st)
        hw, hh = W / (2 * z), H / (2 * z)               # half view in 1080-space
        cx = min(max(cx, hw), W - hw); cy = min(max(cy, hh), H - hh)
        sc = z / k                                       # source → output scale
        M = np.array([[sc, 0, W / 2 - cx * k * sc], [0, sc, H / 2 - cy * k * sc]], np.float64)
        src = rd.blend((st - s["a"]) * P.FPS) if (s["speed"] < 1 and P.VERSION >= "v03") else rd.get(fi)
        if sc < 0.75:                                    # pre-shrink with area filter to avoid aliasing on 4K input
            r = sc / 0.9; src = cv2.resize(src, None, fx=r, fy=r, interpolation=cv2.INTER_AREA); M[:, :2] /= r
        img = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if s["name"] == "hook": img = hook_card(img)
        e.stdin.write(img.tobytes())
    e.stdin.close(); e.wait(); rd.close(); return out

if __name__ == "__main__":
    draft = "draft" in sys.argv
    parts = [render_seg(s, draft) for s in P.OUT]
    # end freeze: last frame of the final segment held
    last = parts[-1]
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-sseof", "-0.04", "-i", last, "-frames:v", "1", "seg/last.png"], check=True)
    nfz = P.NF - sum(s["n"] for s in P.OUT)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", "1", "-i", "seg/last.png", "-frames:v", str(nfz), "-r", str(P.FPS),
                    "-vf", ("noise=alls=6:allf=t," if P.VERSION >= "v03" else "") + "format=yuv420p", "-c:v", "libx264", "-crf", "16", "seg/freeze.mp4"], check=True)
    open("seg/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts + ["seg/freeze.mp4"]))
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "seg/list.txt", "-c:v", "libx264",
                    "-crf", "16", "-preset", "medium", "-g", "15", "-pix_fmt", "yuv420p", "-r", str(P.FPS), "-movflags", "+faststart",
                    "edit/assets/v/plate.mp4"], check=True)
    n = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0",
                        "edit/assets/v/plate.mp4"], capture_output=True, text=True).stdout.strip()
    print("plate frames", n, "expected", P.NF)
