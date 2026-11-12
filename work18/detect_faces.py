# Face detection on every frame of the recreation (MediaPipe BlazeFace short-range, CPU), at 1x and, if nothing is found,
# 2x upscale for small, far faces. -> faces_raw.json {frame: [[x, y, w, h, score], ...]} in source pixels (478x850)
import cv2, json, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(base_options=mpt.BaseOptions(model_asset_path="tools/blaze_face_short_range.tflite",
                                              delegate=mpt.BaseOptions.Delegate.CPU), min_detection_confidence=0.35))
cap = cv2.VideoCapture("src/recreated_3.14.20PM.mp4"); out = {}; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    res = []
    for sc in (1.0, 2.0):
        g = cv2.resize(f, None, fx=sc, fy=sc, interpolation=cv2.INTER_CUBIC) if sc != 1 else f
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(g, cv2.COLOR_BGR2RGB)))
        for d in r.detections:
            b = d.bounding_box; res.append([round(b.origin_x / sc), round(b.origin_y / sc), round(b.width / sc), round(b.height / sc), round(d.categories[0].score, 2)])
        if res: break
    if res: out[i] = res
    i += 1
json.dump(out, open("faces_raw.json", "w")); print("frames", i, "with faces", len(out))
for k in range(0, i, 15): print(round(k / 30, 1), out.get(k))
