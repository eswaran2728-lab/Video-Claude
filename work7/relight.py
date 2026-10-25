# Cinematic relight of the cut clips (edit/assets/v -> edit/assets/vc).
# Face shots: CSRT-tracked warm key light on the face, torso and the keychain table kept lit, background shelves
# fall off into shadow. Product b-roll: a warm pool of light on the product, darker frame edges.
# A soft highlight roll-off keeps faces and white packaging from clipping.
import cv2, numpy as np, subprocess, os, json
SRC, DST = "edit/assets/v", "edit/assets/vc"
os.makedirs(DST, exist_ok=True)
W, H = 1080, 1920
FACE = {"V2": (380, 330, 240, 300), "V4_face": (320, 330, 250, 310), "V10": (400, 290, 250, 310), "V12": (660, 40, 240, 260)}
BROLL = ["V1", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V11"]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

def softclip(x, knee=0.82):
    over = np.maximum(x - knee, 0)
    return np.where(x > knee, knee + (1 - knee) * np.tanh(over / (1 - knee)), x)

def grade(frame, gain, warm):
    f = frame.astype(np.float32) / 255.0
    f = f * gain[..., None]
    f[..., 2] *= 1 + 0.06 * warm; f[..., 1] *= 1 + 0.015 * warm; f[..., 0] *= 1 - 0.06 * warm
    return (softclip(np.clip(f, 0, 1.5)) * 255).clip(0, 255).astype(np.uint8)

def face_gain(cx, cy, fw, fh):
    key = np.exp(-(((xx - cx) / (1.25 * fw)) ** 2 + ((yy - cy) / (1.15 * fh)) ** 2))
    torso = np.exp(-(((xx - cx) / (2.6 * fw)) ** 2 + ((yy - (cy + 1.9 * fh)) / (1.6 * fh)) ** 2))
    table = np.clip((yy - 0.6 * H) / (0.12 * H), 0, 1)
    g = 0.74 + 0.36 * key + 0.16 * torso + 0.2 * table
    return np.minimum(g, 1.12), key

def broll_gain():
    pool = np.exp(-(((xx - W / 2) / (0.48 * W)) ** 2 + ((yy - 0.56 * H) / (0.38 * H)) ** 2))
    return 0.8 + 0.28 * pool, pool
BG, BW = broll_gain()

def run(name, per_frame):
    cap = cv2.VideoCapture(f"{SRC}/{name}.mp4")
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-g", "10", f"{DST}/{name}.mp4"], stdin=subprocess.PIPE)
    i = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        enc.stdin.write(per_frame(i, f).tobytes()); i += 1
    enc.stdin.close(); enc.wait()
    return i

track = {}
for name, box in FACE.items():
    cap = cv2.VideoCapture(f"{SRC}/{name}.mp4"); ok, f = cap.read()
    t = cv2.TrackerCSRT_create(); t.init(f, box); pts = [(box[0] + box[2] / 2, box[1] + box[3] / 2)]
    while True:
        ok, f = cap.read()
        if not ok: break
        ok2, b = t.update(f)
        pts.append((b[0] + b[2] / 2, b[1] + b[3] / 2) if ok2 else pts[-1])
    p = np.array(pts); k = 9
    sm = np.stack([np.convolve(np.pad(p[:, j], k // 2, mode="edge"), np.ones(k) / k, "valid") for j in range(2)], 1)
    track[name] = sm.round(1).tolist()
    fw, fh = box[2], box[3]
    n = run(name, lambda i, f, sm=sm, fw=fw, fh=fh: grade(f, *face_gain(sm[min(i, len(sm) - 1)][0], sm[min(i, len(sm) - 1)][1], fw, fh)))
    print(name, n, "frames, face path", sm[0].round(), "->", sm[-1].round(), flush=True)
json.dump(track, open(f"{DST}/face_track.json", "w"))
for name in BROLL:
    n = run(name, lambda i, f: grade(f, BG, BW))
    print(name, n, flush=True)
# split panes pre-cropped, as in make_assets.py
for src, dst, crop in (("V4", "V4_top", "1080:1000:0:460"), ("V4_face", "V4_faceC", "1080:960:0:67")):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{DST}/{src}.mp4", "-vf", f"crop={crop}", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", f"{DST}/{dst}.mp4"], check=True)
