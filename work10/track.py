# Track the red CYBER ROADSHOW screen in IMG_6421 (SDR 4K master) so 9:16 crops stay on the stage while the phone pans.
# Red mask (R high, G/B low) centroid x per frame, 2.4..16.6 s, median + moving-average smoothed -> edit/track.json
import cv2, numpy as np, json
cap = cv2.VideoCapture("proxy/IMG_6421.mov"); fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_MSEC, 2400); xs, ts = [], []
while True:
    t = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    ok, f = cap.read()
    if not ok or t > 16.6: break
    s = cv2.resize(f, (480, 270)).astype(np.int16); b, g, r = s[..., 0], s[..., 1], s[..., 2]
    m = (r > 150) & (g < 90) & (b < 100) & (r - g > 90)
    m[200:] = False                                            # ignore red clothing in the crowd (lower part of frame)
    ys, xx = np.nonzero(m)
    xs.append(float(np.median(xx)) * 8 if len(xx) > 200 else np.nan); ts.append(round(t, 3))
x = np.array(xs); idx = np.arange(len(x)); ok = ~np.isnan(x); x = np.interp(idx, idx[ok], x[ok])
from scipy.ndimage import median_filter, uniform_filter1d
x = uniform_filter1d(median_filter(x, 9), 15)
json.dump({"t": ts, "x": [round(v, 1) for v in x]}, open("edit/track.json", "w"))
print(len(ts), "frames", "x range", round(x.min()), round(x.max()), [round(x[i]) for i in range(0, len(x), 30)])
