# v03: foreground matte for the dark-background grade (rembg 2.x, ONNX models already in ~/.rembg/models):
#  pass "u2" : u2net_human_seg on every frame (fast, crisp person edges, but it can drop the held earbuds case)
#  pass "bir": birefnet-general-lite every 3rd frame (keeps the case; ~5.5 s/frame on this CPU)
# make_plate.py (VERSION=v03) takes max(u2, birefnet interpolated to 30 fps), smoothed in time and feathered.
# -> src/matte_u2.mp4 (30 fps) / src/matte_bir.mp4 (10 fps), gray 720x1280.  Usage: python3 make_matte.py u2|bir
import sys, subprocess, time, cv2, numpy as np
from PIL import Image
from rembg import new_session, remove
which = sys.argv[1]; name, step, out = {"u2": ("u2net_human_seg", 1, "src/matte_u2.mp4"),
                                         "bir": ("birefnet-general-lite", 3, "src/matte_bir.mp4")}[which]
s = new_session(name); cap = cv2.VideoCapture("proxy/src30.mov"); i = n = 0; t0 = time.time()
enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", "720x1280",
                        "-r", str(30 // step), "-i", "-", "-c:v", "libx264", "-pix_fmt", "gray", "-crf", "8", out], stdin=subprocess.PIPE)
while True:
    ok, f = cap.read()
    if not ok: break
    if i % step == 0:
        a = remove(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)), session=s, only_mask=True)
        enc.stdin.write(np.asarray(a, np.uint8).tobytes()); n += 1
        if n % 50 == 0: print(which, i, round(time.time() - t0), "s", flush=True)
    i += 1
enc.stdin.close(); enc.wait(); print(which, "done", n, "frames", round(time.time() - t0), "s", flush=True)
