# Extra b-roll panes for v05 (lower half under the motion-graphics panel), relit like the v04 b-roll.
import subprocess, os, cv2, numpy as np, sys
os.environ["VERSION"] = "v04"
src = open("relight.py").read(); exec(src[:src.index("def run(")])      # grade(), BG/BW from the v04 relight
OUT = "edit/assets/v5"; os.makedirs(OUT, exist_ok=True)
PANES = [  # name, clip, src_in, duration, crop top (1080x960 window of the 1080x1920 frame)
    ("P_hand",   "3437BABC", 0.30, 3.40, 300),   # bunch of keychains held to camera
    ("P_flex",   "IMG_6352", 0.40, 6.45, 480),   # plate flexed, prints pop off
    ("P_pour",   "IMG_6353", 0.30, 3.00, 440),   # box poured: red + black
    ("P_macro",  "IMG_6351", 3.40, 2.20, 480),   # macro: red body, black outline, white print
]
for name, clip, a, d, top in PANES:
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{a}", "-i", f"proxy/{clip}.mp4", "-t", f"{d}", "-an", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080, 3)
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x960", "-r", "30", "-i", "-",
                            "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-g", "10", f"{OUT}/{name}.mp4"], stdin=subprocess.PIPE)
    for f in fr:
        enc.stdin.write(np.ascontiguousarray(grade(f, BG, BW)[top:top + 960]).tobytes())
    enc.stdin.close(); enc.wait(); print(name, len(fr))
