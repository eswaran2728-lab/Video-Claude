# Camera plate for the edit: EDL + head freeze + end hold, punch-in framing (plan.FRAMING, one Lanczos resample straight
# from the 720x1280 source), grade (grade_ffmpeg.txt: gentle midtone lift, highlight roll-off for the bright ceiling, a
# touch less magenta in skin, slight saturation). -> edit/assets/v/plate.mp4 (1080x1920, 30 fps, no audio)
import subprocess, cv2, numpy as np, plan
cap = cv2.VideoCapture("proxy/src30.mov"); F = []
while True:
    ok, f = cap.read()
    if not ok: break
    F.append(f)
N = round(plan.TOTAL * plan.FPS); G = open("grade_ffmpeg.txt").read().strip()
enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30",
                        "-i", "-", "-vf", G + ",format=yuv420p", "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-g", "15",
                        "-bf", "0", "-movflags", "+faststart", "edit/assets/v/plate.mp4"], stdin=subprocess.PIPE)
log = []
for n in range(N):
    t = n / plan.FPS; s_src = plan.o2s(t); i = min(len(F) - 1, round(s_src * plan.FPS))
    s, fx, fy = plan.framing(t); k = plan.BASE * s
    M = np.float32([[k, 0, fx * (1 - s)], [0, k, fy * (1 - s)]])
    enc.stdin.write(cv2.warpAffine(F[i], M, (1080, 1920), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE).tobytes())
    if n % 30 == 0: log.append((round(t, 2), i, round(s, 3)))
enc.stdin.close(); enc.wait()
print("frames", N, "total", plan.TOTAL, "speech_end", plan.SPEECH_OUT_END); print(log)
