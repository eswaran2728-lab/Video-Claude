# Tracks the 5 key hooks on the plate (Lucas-Kanade, from a hand-marked reference frame, forward and backward) for the
# numbered tags. → edit/hook_tags.json {frames: {frame: [[x,y]×5]}, pops: [t×5], hide: t}
import json, subprocess, numpy as np, cv2
import plan16 as P
W, H = 1080, 1920
REF_T = 18.1                                              # output time of the reference frame
REF = [(170, 1088), (360, 1088), (552, 1088), (742, 1086), (940, 1084)]   # hook bodies on that frame (marked on a grid)
t0, t1 = P.out_t("story", P.HOOKS_SRC[0]), P.out_t("story", P.HOOKS_SRC[1])
f0, f1, fr = int(t0 * P.FPS) - 2, int(t1 * P.FPS) + 2, int(round(REF_T * P.FPS))
raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{f0 / P.FPS:.4f}", "-i", "edit/assets/v/plate.mp4", "-frames:v", str(f1 - f0 + 1),
                      "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
G = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
lk = dict(winSize=(31, 31), maxLevel=3, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 40, 0.01))
mask = np.zeros((H, W), np.uint8); mask[930:1240, 20:1060] = 255   # the frame's bottom panel + hooks row
ref_pts = np.array(REF, np.float32).reshape(-1, 1, 2)
pos = {fr: ref_pts}
for step in (1, -1):
    i = fr; A = np.eye(2, 3, dtype=np.float32)                    # cumulative similarity transform ref → frame i
    while f0 <= i + step <= f0 + len(G) - 1:
        a, b = G[i - f0], G[i + step - f0]
        pts = cv2.goodFeaturesToTrack(a, 300, 0.01, 8, mask=cv2.warpAffine(mask, A, (W, H)))
        q, st, _ = cv2.calcOpticalFlowPyrLK(a, b, pts, None, **lk)
        ok = st[:, 0] == 1
        M, inl = cv2.estimateAffinePartial2D(pts[ok], q[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0)
        A = (np.vstack([M, [0, 0, 1]]) @ np.vstack([A, [0, 0, 1]]))[:2].astype(np.float32)
        pos[i + step] = cv2.transform(ref_pts, A); i += step
frames = {int(k): [[round(float(x), 1), round(float(y), 1)] for x, y in v.reshape(-1, 2)] for k, v in sorted(pos.items())}
pops = [round(t0 + 0.08 + i * 0.26, 3) for i in range(5)]
json.dump({"frames": frames, "pops": pops, "hide": round(t1 - 0.25, 3)}, open("edit/hook_tags.json", "w"))
# proof strip: tracked marks drawn on 6 frames
sel = np.linspace(f0 + 2, f0 + len(G) - 3, 6).astype(int); tiles = []
for k in sel:
    im = cv2.cvtColor(G[k - f0], cv2.COLOR_GRAY2BGR)
    for x, y in frames[int(k)]: cv2.circle(im, (int(x), int(y)), 18, (0, 200, 255), 3)
    tiles.append(cv2.resize(im[880:1300], (540, 210)))
cv2.imwrite("sheets/hook_track.jpg", np.vstack(tiles))
print("tracked frames", len(frames), "window", round(t0, 2), round(t1, 2), "pops", pops)
