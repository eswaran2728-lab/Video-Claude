# v02 privacy edits (creator: "hide that tiktok name" + "blur the women face in the second"):
#  1. original clip: the TikTok logo + "@handle" watermark is blurred where it sits (top-left 0-5.0 s, bottom-right 5.0 s on).
#  2. recreation: the woman's face is tracked (MediaPipe BlazeFace detections, faces_raw.json) through her shot (12.07-24.1 s),
#     smoothed (median, 7 frames), gaps filled, enlarged 1.6x, and blurred inside a feathered ellipse. 15.8-16.7 s (turning,
#     profile, no detection) holds the first detection, enlarged further.
# -> src/original_clean.mp4, src/recreated_faceblur.mp4 (video only; the mix uses the original audio)
import cv2, json, subprocess, numpy as np


def writer(path, W, H):
    return subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                             "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)


def soft_blur(f, mask, k):
    b = cv2.GaussianBlur(f, (0, 0), k); b = cv2.GaussianBlur(cv2.resize(cv2.resize(b, None, fx=0.12, fy=0.12), (f.shape[1], f.shape[0]), interpolation=cv2.INTER_LINEAR), (0, 0), 4)
    a = mask[..., None]; return (f * (1 - a) + b * a).astype(np.uint8)


# 1 watermark
cap = cv2.VideoCapture("src/original_scene_2.44.44PM.mp4"); W, H = int(cap.get(3)), int(cap.get(4)); w = writer("src/original_clean.mp4", W, H); i = 0
TL = [(0, 0, 72, 64), (0, 52, 124, 100)]; BR = [(430, 548, 560, 656)]
def boxmask(boxes):
    m = np.zeros((H, W), np.float32)
    for x0, y0, x1, y1 in boxes: cv2.rectangle(m, (x0, y0), (x1, y1), 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), 4)
MTL, MBR = boxmask(TL), boxmask(BR)
while True:
    ok, f = cap.read()
    if not ok: break
    f = soft_blur(f, MTL if i < 150 else MBR, 9); w.stdin.write(f.tobytes()); i += 1
w.stdin.close(); w.wait(); print("watermark frames", i)

# 2 face track
F = json.load(open("faces_raw.json")); A, B = round(12.07 * 30), round(24.1 * 30)
track = {}
for k in range(A, B):
    c = [b for b in F.get(str(k), []) if b[4] >= 0.45 and b[1] < 380 and b[2] < 300]
    if c: track[k] = max(c, key=lambda b: b[4])[:4]
CUT = round(21.6 * 30)                                          # camera cut inside her shot: smooth each side on its own
full = {}; first = None
for lo, hi in ((A, CUT), (CUT, B)):
    ks = [k for k in sorted(track) if lo <= k < hi]
    if not ks: continue
    arr = np.array([track[k] for k in ks], float)
    med = np.array([np.median(arr[max(0, j - 3): j + 4], axis=0) for j in range(len(ks))])
    for k in range(ks[0], hi): full[k] = [float(np.interp(k, ks, med[:, c])) for c in range(4)]
    if first is None: first, med0 = ks[0], med[0]
hold0 = round(15.8 * 30)
for k in range(hold0, first): full[k] = list(med0) + [1]          # profile hold (marked)
cap = cv2.VideoCapture("src/recreated_3.14.20PM.mp4"); W, H = int(cap.get(3)), int(cap.get(4)); w = writer("src/recreated_faceblur.mp4", W, H); i = 0; dbg = []
while True:
    ok, f = cap.read()
    if not ok: break
    if i in full:
        x, y, bw, bh = full[i][:4]; s = 1.6 if len(full[i]) == 4 else 2.0
        cx, cy = x + bw / 2, y + bh / 2 - 0.05 * bh; ax, ay = bw * s / 2, bh * s * 1.1 / 2
        m = np.zeros((H, W), np.float32); cv2.ellipse(m, (int(cx), int(cy)), (int(ax), int(ay)), 0, 0, 360, 1.0, -1); m = cv2.GaussianBlur(m, (0, 0), max(4, bw * 0.08))
        f = soft_blur(f, m, max(10, bw * 0.12))
        if i % 15 == 0 or 644 <= i <= 652: dbg.append((i, f.copy()))
    w.stdin.write(f.tobytes()); i += 1
w.stdin.close(); w.wait()
tiles = [cv2.putText(cv2.resize(t, (160, 284)), f"{k / 30:.1f}", (6, 24), 0, 0.7, (0, 0, 255), 2) for k, t in dbg]
rows = [np.hstack(tiles[j:j + 10] + [np.zeros_like(tiles[0])] * (10 - len(tiles[j:j + 10]))) for j in range(0, len(tiles), 10)]
cv2.imwrite("sheets/faceblur_check.jpg", np.vstack(rows)); print("face frames", len(full), "from", hold0 / 30, "to", B / 30)
