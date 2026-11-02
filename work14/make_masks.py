# Statue cut-out masks (BiRefNet-lite ONNX, local rembg model; no network). Keyframes every 3rd frame inside the used
# source ranges; frames in between are filled by optical-flow warping the nearest keyframe mask. -> masks/NNNNN.png
import cv2, os, time, numpy as np, onnxruntime as ort
so = ort.SessionOptions(); so.intra_op_num_threads = 4; so.enable_cpu_mem_arena = False; so.enable_mem_pattern = False
S = ort.InferenceSession('/root/.rembg/models/birefnet-general-lite/birefnet-general-lite.onnx', so, providers=['CPUExecutionProvider'])
RANGES = [(0.5, 3.6), (5.5, 7.6), (9.4, 10.7), (12.4, 20.35)]
need = sorted({f for a, b in RANGES for f in range(round(a * 30), round(b * 30) + 1)})
key = sorted({f for a, b in RANGES for f in list(range(round(a * 30), round(b * 30) + 1, 3)) + [round(b * 30)]})
cap = cv2.VideoCapture("proxy/src30.mov"); F = {}; i = 0
while True:                                        # keep frames as JPEG bytes (memory: the ONNX model needs the room)
    ok, f = cap.read()
    if not ok or i > max(need): break
    if i in need: F[i] = cv2.imencode(".jpg", f, [cv2.IMWRITE_JPEG_QUALITY, 95])[1]
    i += 1
class _D(dict):
    def __getitem__(self, k): return cv2.imdecode(dict.__getitem__(self, k), cv2.IMREAD_COLOR)
F = _D(F)
MEAN, STD = np.array([0.485, 0.456, 0.406]), np.array([0.229, 0.224, 0.225])
def infer(f):
    im = cv2.cvtColor(cv2.resize(f, (1024, 1024), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB).astype(np.float32) / 255
    x = ((im - MEAN) / STD).transpose(2, 0, 1)[None].astype(np.float32)
    p = 1 / (1 + np.exp(-S.run(None, {'input_image': x})[0][0, 0])); p = (p - p.min()) / (p.max() - p.min() + 1e-6)
    return cv2.resize((p * 255).astype(np.uint8), (f.shape[1], f.shape[0]), interpolation=cv2.INTER_LINEAR)
t0 = time.time()
for n, k in enumerate(key):
    p = f"masks/{k:05d}.png"
    if not os.path.exists(p): cv2.imwrite(p, infer(F[k]))
    if n % 20 == 0: print("key", n, len(key), round(time.time() - t0), flush=True)
def warp(m, src, dst):
    g0 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY); g1 = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    fl = cv2.calcOpticalFlowFarneback(g1, g0, None, 0.5, 4, 21, 3, 5, 1.1, 0)
    h, w = m.shape; yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return cv2.remap(m, xx + fl[..., 0], yy + fl[..., 1], cv2.INTER_LINEAR)
ks = np.array(key)
for fi in need:
    p = f"masks/{fi:05d}.png"
    if os.path.exists(p): continue
    k = int(ks[np.argmin(np.abs(ks - fi))]); cv2.imwrite(p, warp(cv2.imread(f"masks/{k:05d}.png", 0), F[k], F[fi]))
print("done", len(need), "frames", round(time.time() - t0), "s", flush=True)
