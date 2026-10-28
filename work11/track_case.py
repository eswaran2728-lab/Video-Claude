# Track the purple case with OpenCV CSRT over the three product windows (init boxes read off gridded frames
# sheets/grid_product.jpg, source coords 720x1280). -> track.json {window: [[t, cx, cy, w, h], ...]} + a check sheet.
import cv2, json
WIN = {"reveal": (14.3, 13.9, 16.0, (135, 535, 170, 170)),  # (init t, from, to, box): left hand beside his face
       "chest": (20.1, 18.6, 21.9, (295, 775, 170, 170)),   # both hands at chest, screen side to camera
       "side": (25.9, 25.9, 29.2, (110, 660, 160, 160))}    # left hand beside his face again
cap = cv2.VideoCapture("proxy/src30.mov"); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
res = {}
for k, (ti, a, b, box) in WIN.items():
    i0, ia, ib = round(ti * 30), round(a * 30), round(b * 30); rows = {}
    for rng in (range(i0, ib + 1), range(i0, ia - 1, -1)):     # forward and backward from the init frame
        tr = cv2.TrackerCSRT_create(); tr.init(frames[i0], box)
        for i in rng:
            ok, bb = tr.update(frames[i]) if i != i0 else (True, box)
            x, y, w, h = [float(v) for v in bb]; rows[i] = [round(i / 30, 3), round(x + w / 2, 1), round(y + h / 2, 1), round(w), round(h), int(ok)]
    res[k] = [rows[i] for i in sorted(rows)]
json.dump(res, open("track.json", "w"))
# check sheet: every 0.4 s, box drawn
tiles = []
for k, rows in res.items():
    for r in rows[::12]:
        f = frames[round(r[0] * 30)].copy(); cx, cy, w, h = r[1:5]
        cv2.rectangle(f, (int(cx - w / 2), int(cy - h / 2)), (int(cx + w / 2), int(cy + h / 2)), (0, 255, 255), 4)
        cv2.putText(f, f"{k} {r[0]}", (10, 50), 0, 1.4, (0, 255, 255), 3); tiles.append(cv2.resize(f, (180, 320)))
while len(tiles) % 10: tiles.append(tiles[-1] * 0)
rows_img = [cv2.hconcat(tiles[i:i + 10]) for i in range(0, len(tiles), 10)]
cv2.imwrite("sheets/track_check.jpg", cv2.vconcat(rows_img))
