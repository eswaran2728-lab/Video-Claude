# Generic rigid tracker for overlay anchors on the plate (Lucas-Kanade features in a box, RANSAC similarity transform,
# forward + backward from a hand-marked reference frame). Jobs below → edit/track_<name>.json + sheets/track_<name>.jpg
# Usage: python3 track16.py [name ...]
import json, sys, subprocess, numpy as np, cv2
import plan16 as P
W, H = 1080, 1920
JOBS = {
    # name: (ref output time, [anchor points on that frame], start, end (output s), feature box x0,y0,x1,y1)
    "callouts": (6.5, [(585, 650), (410, 870)], P.out_t("story", 7.46), P.out_t("story", 11.30), (60, 150, 1020, 1350)),
}
def track(ref_t, refs, t0, t1, box):
    f0, f1, fr = int(t0 * P.FPS), int(t1 * P.FPS) + 1, int(round(ref_t * P.FPS))
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{f0 / P.FPS:.4f}", "-i", "edit/assets/v/plate.mp4", "-frames:v",
                          str(f1 - f0 + 1), "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    G = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
    lk = dict(winSize=(31, 31), maxLevel=3, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 40, 0.01))
    mask = np.zeros((H, W), np.uint8); mask[box[1]:box[3], box[0]:box[2]] = 255
    ref = np.array(refs, np.float32).reshape(-1, 1, 2); pos = {fr: ref}
    for step in (1, -1):
        i = fr; A = np.eye(2, 3, dtype=np.float32)
        while f0 <= i + step <= f0 + len(G) - 1:
            a, b = G[i - f0], G[i + step - f0]
            pts = cv2.goodFeaturesToTrack(a, 400, 0.01, 8, mask=cv2.warpAffine(mask, A, (W, H)))
            q, st, _ = cv2.calcOpticalFlowPyrLK(a, b, pts, None, **lk); ok = st[:, 0] == 1
            M, _ = cv2.estimateAffinePartial2D(pts[ok], q[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0)
            A = (np.vstack([M, [0, 0, 1]]) @ np.vstack([A, [0, 0, 1]]))[:2].astype(np.float32)
            pos[i + step] = cv2.transform(ref, A); i += step
    return G, f0, {int(k): [[round(float(x), 1), round(float(y), 1)] for x, y in v.reshape(-1, 2)] for k, v in sorted(pos.items())}

for name in (sys.argv[1:] or JOBS):
    ref_t, refs, t0, t1, box = JOBS[name]
    G, f0, frames = track(ref_t, refs, t0, t1, box)
    json.dump({"frames": frames, "t0": round(t0, 3), "t1": round(t1, 3)}, open(f"edit/track_{name}.json", "w"))
    sel = np.linspace(f0 + 1, f0 + len(G) - 2, 5).astype(int); tiles = []
    for k in sel:
        im = cv2.cvtColor(G[k - f0], cv2.COLOR_GRAY2BGR)
        for x, y in frames[int(k)]: cv2.circle(im, (int(x), int(y)), 22, (0, 200, 255), 5)
        tiles.append(cv2.resize(im, (270, 480)))
    cv2.imwrite(f"sheets/track_{name}.jpg", np.hstack(tiles)); print(name, "frames", len(frames), round(t0, 2), round(t1, 2))
