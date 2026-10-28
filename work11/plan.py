# Shared edit plan for the earbuds reel (work11): EDL, source<->output time, camera framing, cue times.
# Source: Drive file 3b5b7d85628e467eaa9b80b3eb762869.mp4 (two Drive copies, byte-identical, SHA-256 629fb550…4b5a);
# proxy/src30.mov = 30 fps CFR copy. Output 1080x1920, 30 fps. Speech is Malaysian Tamil with English product words.
import json, math

FPS = 30
SRC_W, SRC_H = 720, 1280
BASE = 1.5                       # source -> output scale before any punch-in (720x1280 -> 1080x1920)

# (src_in, src_out): head trim 0-0.40 (camera settling, no speech; frames 0-14 are blurred), one cut of the 0.86 s pause
# 16.30-16.92 between "...purchase" and "intha earbuds-la". Everything else is kept: the take is a single clean delivery.
EDL = [(0.40, 16.30), (16.92, 32.7867)]
FREEZE_HEAD = 20 / 30            # src 0.40-0.50 are still blurred and 0.50-0.63 is a blink: hold src frame 20 (sharp, eyes
                                 # open) for output frames 0-7, so the cover frame is clean; live from there on
END_HOLD = 0.833                 # freeze of the last frame under the closing card (25 frames)
SEG_OUT = []
_t = 0.0
for a, b in EDL:
    SEG_OUT.append((round(_t, 4), round(_t + b - a, 4), a, b)); _t += b - a
SPEECH_OUT_END = round(_t, 4)
TOTAL = round(math.floor((SPEECH_OUT_END + END_HOLD) * FPS) / FPS, 4)


def o2s(t):
    """output time -> source time (end hold maps to the last source frame)"""
    for o0, o1, a, b in SEG_OUT:
        if t < o1 - 1e-9:
            return max(a + (t - o0), FREEZE_HEAD) if o0 == 0 else a + (t - o0)
    return EDL[-1][1] - 1 / FPS


def s2o(s):
    """source time -> output time (None if cut)"""
    for o0, o1, a, b in SEG_OUT:
        if a - 1e-6 <= s <= b + 1e-6:
            return round(o0 + s - a, 3)
    return None


# ---- camera framing: (out_t, scale, focus_x, focus_y) keyframes in BASE output coords (focus point stays fixed);
# eased between consecutive keys with ease-in-out cubic. A key repeated at the same time = cut (no tween). ----
def _o(s): return s2o(s)
FRAMING = [
    (0.00, 1.00, 540, 600), (0.60, 1.12, 540, 600), (4.40, 1.15, 540, 600),      # hook: visible push on the question
    (4.70, 1.00, 540, 900), (11.90, 1.06, 540, 900),                               # context: wide, slow drift
    (_o(13.05), 1.06, 540, 900), (_o(13.45), 1.24, 400, 760), (15.90, 1.27, 400, 760),  # lifts the case: punch to face + case
    (15.90, 1.00, 540, 960), (_o(18.10), 1.00, 540, 960), (_o(18.45), 1.16, 540, 1010), (_o(21.55), 1.18, 540, 1010),  # features
    (_o(21.75), 1.02, 540, 900), (_o(25.40), 1.06, 540, 900),                     # payoff 1: wide
    (_o(25.62), 1.13, 420, 760), (_o(29.85), 1.15, 420, 760),                     # payoff 2: face + case beside it
    (_o(30.05), 1.00, 540, 900), (TOTAL, 1.05, 540, 900),                         # call to action
]


def _ease(u): return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2


def framing(t):
    K = FRAMING
    if t <= K[0][0]: return K[0][1:]
    for i in range(len(K) - 1):
        a, b = K[i], K[i + 1]
        if a[0] <= t < b[0]:
            if b[0] - a[0] < 1e-6: continue
            u = _ease((t - a[0]) / (b[0] - a[0]))
            return tuple(a[j] + (b[j] - a[j]) * u for j in (1, 2, 3))
    return K[-1][1:]


def to_out(t, x_src, y_src):
    """source pixel (720x1280) -> output pixel at output time t, through BASE and the punch-in"""
    s, fx, fy = framing(t); bx, by = x_src * BASE, y_src * BASE
    return (fx + (bx - fx) * s, fy + (by - fy) * s, s)


# case track (CSRT, track.json) as a function of source time; None outside the tracked windows
_TR = json.load(open(__file__.rsplit("/", 1)[0] + "/track.json"))


def case_src(s):
    for rows in _TR.values():
        if rows[0][0] - 1e-6 <= s <= rows[-1][0] + 1e-6:
            i = min(range(len(rows)), key=lambda k: abs(rows[k][0] - s))
            lo, hi = max(0, i - 3), min(len(rows), i + 4)          # 7-frame moving average
            xs = [r[1] for r in rows[lo:hi]]; ys = [r[2] for r in rows[lo:hi]]; ws = [r[3] for r in rows[lo:hi]]
            return sum(xs) / len(xs), sum(ys) / len(ys), sum(ws) / len(ws)
    return None
