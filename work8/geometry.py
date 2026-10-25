# Diagram geometry for the sketch -> explainer transition.
# The notebook sketch (IMG_6372, top drawing cropped to edit/assets/sketch_top.jpg, 1110x900) has three pen loops, and
# each loop encloses TWO labels: QUALITY+CHEAP (tall loop, pointed at the bottom left), QUALITY+FAST (loop running to
# the bottom right) and CHEAP+FAST (flat ellipse along the bottom). They are traced here as closed Catmull-Rom curves,
# resampled to N points and paired point-for-point with clean capsules through the same two labels, so one path can
# morph from the hand-drawn line into the clean diagram. Output: edit/geometry.json (canvas px, 1080x1920).
import json, math, numpy as np
N = 120
SK = dict(x=40, y=250, s=1000 / 1110)          # where the sketch photo sits on the canvas
def sk(p): return (SK["x"] + p[0] * SK["s"], SK["y"] + p[1] * SK["s"])

# hand traces in sketch-photo pixels (clockwise, starting at the top)
TRACE = {
    "QC": [(480, 80), (560, 140), (572, 230), (540, 340), (470, 480), (380, 610), (260, 735), (140, 800), (78, 790), (55, 690),
           (85, 520), (140, 330), (215, 180), (330, 98)],
    "QF": [(330, 88), (440, 95), (540, 160), (640, 280), (725, 420), (765, 560), (745, 660), (610, 712), (500, 650), (360, 500),
           (240, 360), (185, 250), (215, 140)],
    "CF": [(440, 478), (640, 482), (790, 512), (835, 570), (790, 640), (640, 700), (440, 722), (240, 728), (90, 712), (45, 660),
           (70, 575), (180, 520), (300, 490)],
}
LABEL_SK = {"Q": (335, 255), "C": (175, 612), "F": (640, 597)}

# clean layout (canvas px): an upright triangle of labels inside the off-white board
LAB = {"Q": (540, 455), "C": (345, 865), "F": (735, 865)}
PAIRS = {"QC": ("Q", "C"), "QF": ("Q", "F"), "CF": ("C", "F")}
RB, OVER = 168, 200                             # ellipse semi-minor axis, overshoot of the semi-major axis past each label

def catmull(pts, n):
    P = np.array(pts, float); m = len(P); out = []
    for i in range(m):
        p0, p1, p2, p3 = P[(i - 1) % m], P[i], P[(i + 1) % m], P[(i + 2) % m]
        for t in np.linspace(0, 1, 40, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    return resample(np.array(out), n)

def resample(P, n):
    Q = np.vstack([P, P[:1]]); seg = np.linalg.norm(np.diff(Q, axis=0), axis=1); cum = np.concatenate([[0], np.cumsum(seg)])
    ts = np.linspace(0, cum[-1], n, endpoint=False)
    return np.stack([np.interp(ts, cum, Q[:, 0]), np.interp(ts, cum, Q[:, 1])], 1)

def capsule(a, b, n):
    # clean loop for a pair: an ellipse whose long axis runs through both labels (rounder, like the pen loops)
    a, b = np.array(a, float), np.array(b, float); L = np.linalg.norm(b - a); d = (b - a) / L; nrm = np.array([-d[1], d[0]])
    c, A = (a + b) / 2, L / 2 + OVER
    t = np.linspace(0, 2 * math.pi, 720, endpoint=False)
    return resample(c + np.outer(A * np.cos(t), d) + np.outer(RB * np.sin(t), nrm), n)

def align(src, dst):
    # same winding, then rotate dst's start index so corresponding points are nearest (smooth morph, no twisting)
    def area(P): return 0.5 * np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1])
    if np.sign(area(src)) != np.sign(area(dst)): dst = dst[::-1]
    best = min(range(len(dst)), key=lambda k: np.sum(np.linalg.norm(src - np.roll(dst, -k, 0), axis=1)))
    return np.roll(dst, -best, 0)

def d_of(P): return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in P) + " Z"

out = {"N": N, "sketch": SK, "labels_sketch": {k: sk(v) for k, v in LABEL_SK.items()}, "labels": LAB, "loops": {}}
for k, tr in TRACE.items():
    hand = np.array([sk(p) for p in catmull(tr, N)])
    clean = align(hand, capsule(LAB[PAIRS[k][0]], LAB[PAIRS[k][1]], N))
    out["loops"][k] = {"hand": hand.round(1).tolist(), "clean": clean.round(1).tolist(), "d_hand": d_of(hand), "d_clean": d_of(clean)}
json.dump(out, open("edit/geometry.json", "w"))
print({k: (np.array(v["clean"]).min(0).round(), np.array(v["clean"]).max(0).round()) for k, v in out["loops"].items()})
