# Tracks the two lamps in the "see this lamp" shot (same rigid RANSAC method as track_hooks16.py, on the frame's top panel).
# → edit/lamp_rings.json {frames: {frame: [[x,y],[x,y]]}, show, hide}
import json, subprocess, numpy as np, cv2
import plan16 as P
W, H = 1080, 1920
REF_T = 21.9
REF = [(212, 582), (1000, 522)]                           # left / right lamp on that frame (marked on a grid)
show, hide = round(P.out_t("howto", 41.12), 3), round(P.S["howto"]["o1"] - 0.12, 3)
f0, f1, fr = int(show * P.FPS) - 1, int(hide * P.FPS) + 2, int(round(REF_T * P.FPS))
raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{f0 / P.FPS:.4f}", "-i", "edit/assets/v/plate.mp4", "-frames:v", str(f1 - f0 + 1),
                      "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
G = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
lk = dict(winSize=(31, 31), maxLevel=3, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 40, 0.01))
mask = np.zeros((H, W), np.uint8); mask[380:760, 0:1080] = 255    # letters + top rail of the frame
ref_pts = np.array(REF, np.float32).reshape(-1, 1, 2); pos = {fr: ref_pts}
for step in (1, -1):
    i = fr; A = np.eye(2, 3, dtype=np.float32)
    while f0 <= i + step <= f0 + len(G) - 1:
        a, b = G[i - f0], G[i + step - f0]
        pts = cv2.goodFeaturesToTrack(a, 300, 0.01, 8, mask=cv2.warpAffine(mask, A, (W, H)))
        q, st, _ = cv2.calcOpticalFlowPyrLK(a, b, pts, None, **lk); ok = st[:, 0] == 1
        M, _ = cv2.estimateAffinePartial2D(pts[ok], q[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0)
        A = (np.vstack([M, [0, 0, 1]]) @ np.vstack([A, [0, 0, 1]]))[:2].astype(np.float32)
        pos[i + step] = cv2.transform(ref_pts, A); i += step
frames = {int(k): [[round(float(x), 1), round(float(y), 1)] for x, y in v.reshape(-1, 2)] for k, v in sorted(pos.items())}
json.dump({"frames": frames, "show": show, "hide": hide}, open("edit/lamp_rings.json", "w"))
sel = np.linspace(f0 + 1, f0 + len(G) - 2, 5).astype(int); tiles = []
for k in sel:
    im = cv2.cvtColor(G[k - f0], cv2.COLOR_GRAY2BGR)
    for x, y in frames[int(k)]: cv2.circle(im, (int(x), int(y)), 40, (0, 200, 255), 4)
    tiles.append(cv2.resize(im[300:900], (540, 300)))
cv2.imwrite("sheets/lamp_track.jpg", np.vstack(tiles))
print("lamp frames", len(frames), "show", show, "hide", hide)
