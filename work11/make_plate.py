# v02 (VERSION=v02): + a tracked face-light (track_face.json): a soft ellipse over his face lifts it ~20% so it reads
#   against the brighter tan shirt; -> plate_v02.mp4. v01 output (plate.mp4) is unchanged when VERSION is unset.
# Camera plate for the edit: EDL + head freeze + end hold, punch-in framing (plan.FRAMING, one Lanczos resample straight
# from the 720x1280 source), grade (grade_ffmpeg.txt: gentle midtone lift, highlight roll-off for the bright ceiling, a
# touch less magenta in skin, slight saturation). -> edit/assets/v/plate.mp4 (1080x1920, 30 fps, no audio)
import os, json, subprocess, cv2, numpy as np, plan
VERSION = os.environ.get("VERSION", "v01"); OUT = "edit/assets/v/plate.mp4" if VERSION == "v01" else f"edit/assets/v/plate_{VERSION}.mp4"
FACE = json.load(open("track_face.json")) if VERSION != "v01" else None
YY, XX = np.mgrid[0:plan.SRC_H, 0:plan.SRC_W].astype(np.float32)
def face_light(img, i, gain=0.20):
    rows = FACE[max(0, i - 3):i + 4]; cx, cy, w, h = [sum(r[k] for r in rows) / len(rows) for k in (1, 2, 3, 4)]
    d = ((XX - cx) / (w * 0.75)) ** 2 + ((YY - cy) / (h * 0.70)) ** 2
    m = np.exp(-1.6 * d)[..., None]                       # soft falloff, no visible edge
    return np.clip(img.astype(np.float32) * (1 + gain * m), 0, 255).astype(np.uint8)
cap = cv2.VideoCapture("proxy/src30.mov"); F = []
while True:
    ok, f = cap.read()
    if not ok: break
    F.append(f)
N = round(plan.TOTAL * plan.FPS); G = open("grade_ffmpeg.txt").read().strip()
enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30",
                        "-i", "-", "-vf", G + ",format=yuv420p", "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-g", "15",
                        "-bf", "0", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
log = []
for n in range(N):
    t = n / plan.FPS; s_src = plan.o2s(t); i = min(len(F) - 1, round(s_src * plan.FPS))
    s, fx, fy = plan.framing(t); k = plan.BASE * s
    M = np.float32([[k, 0, fx * (1 - s)], [0, k, fy * (1 - s)]])
    src = face_light(F[i], i) if FACE else F[i]
    enc.stdin.write(cv2.warpAffine(src, M, (1080, 1920), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE).tobytes())
    if n % 30 == 0: log.append((round(t, 2), i, round(s, 3)))
enc.stdin.close(); enc.wait()
print("frames", N, "total", plan.TOTAL, "speech_end", plan.SPEECH_OUT_END); print(log)
