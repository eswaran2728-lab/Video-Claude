# v02: track his face (OpenCV CSRT, init on src frame 20, forward to the end) for the face-light in make_plate_v02.py.
# Init box read off sheets/blink.jpg / plate frames: forehead to chin, ear to ear (source 720x1280 coords).
# -> track_face.json [[src_t, cx, cy, w, h], ...] + sheets/face_track_check.jpg
import cv2, json
cap = cv2.VideoCapture("proxy/src30.mov"); F = []
while True:
    ok, f = cap.read()
    if not ok: break
    F.append(f)
box = (255, 290, 210, 330); tr = cv2.TrackerCSRT_create(); tr.init(F[20], box); rows = []
for i in range(len(F)):
    if i < 20: x, y, w, h = box
    elif i == 20: x, y, w, h = box
    else:
        ok, bb = tr.update(F[i]); x, y, w, h = bb
    rows.append([round(i / 30, 3), round(x + w / 2, 1), round(y + h / 2, 1), round(w), round(h)])
json.dump(rows, open("track_face.json", "w"))
tiles = []
for r in rows[20::60]:
    f = F[round(r[0] * 30)].copy(); cx, cy, w, h = r[1:]
    cv2.ellipse(f, (int(cx), int(cy)), (int(w * 0.62), int(h * 0.62)), 0, 0, 360, (0, 255, 255), 3)
    cv2.putText(f, str(r[0]), (10, 50), 0, 1.4, (0, 255, 255), 3); tiles.append(cv2.resize(f, (180, 320)))
while len(tiles) % 9: tiles.append(tiles[-1] * 0)
cv2.imwrite("sheets/face_track_check.jpg", cv2.vconcat([cv2.hconcat(tiles[i:i + 9]) for i in range(0, len(tiles), 9)]))
