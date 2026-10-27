# booth_handover.jpg (creator's added photo): remove the two GTR fragments on the plain banner behind the man - the GTR logo
# just above his head and the partial "TH"/"V" letters beside his jaw. Each small box is refilled row by row with the banner's
# own colour sampled just left of it (plus matching grain), so nothing from his head, face or collar is pulled in.
# Output: src/added/booth_handover_retouched.jpg
import cv2, numpy as np
rng = np.random.default_rng(7)
im = cv2.imread("src/added/booth_handover.jpg").astype(np.float32); H, W = im.shape[:2]; out = im.copy()
BOXES = [(0.640, 0.224, 0.668, 0.251, True),     # GTR logo above his head (banner on both sides -> blend left to right)
         (0.6262, 0.355, 0.6368, 0.415, False),  # "TH" left of his jaw (sample left only: a thin strip of banner)
         (0.6228, 0.415, 0.6368, 0.464, False)]  # "V" left of his collar
mask = np.zeros((H, W), np.float32)
for x0, y0, x1, y1, both in BOXES:
    xa, xb, ya, yb = int(x0 * W), int(x1 * W), int(y0 * H), int(y1 * H); s = 8 if not both else 14
    for y in range(ya, yb):
        L = np.median(im[y, xa - s - 2:xa - 2], axis=0)
        R = np.median(im[y, xb + 2:xb + s + 2], axis=0) if both else L
        t = np.linspace(0, 1, xb - xa)[:, None]; out[y, xa:xb] = L * (1 - t) + R * t
    grain = im[ya:yb, xa - s - 2:xa - 2].std(axis=(0, 1)); out[ya:yb, xa:xb] += rng.normal(0, 1, (yb - ya, xb - xa, 1)) * min(grain.mean(), 6) * 0.5
    mask[ya:yb, xa:xb] = 1
out = cv2.GaussianBlur(out, (5, 5), 0)
a = cv2.GaussianBlur(cv2.dilate(mask, np.ones((3, 3), np.uint8)), (9, 9), 0)[..., None]   # feathered edges
out = im * (1 - a) + out * a
cv2.imwrite("src/added/booth_handover_retouched.jpg", np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])
c = lambda a: a[int(0.15 * H):int(0.55 * H), int(0.55 * W):int(0.72 * W)]
s = cv2.resize(np.hstack([c(im), c(out)]).astype(np.uint8), None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC); cv2.imwrite("sheets/handover_retouch_check.jpg", s)
