# Portrait cutouts: FSRCNN x2 upscale (OpenCV dnn_superres, local model) -> BiRefNet-general matte (onnxruntime, local)
# -> RGBA PNG in edit/assets/cut/. Originals in src/ stay untouched. Masks also saved for inspection.
import cv2, numpy as np, onnxruntime as ort, os, sys
so = ort.SessionOptions(); so.intra_op_num_threads = 4
S = ort.InferenceSession('/root/.rembg/models/birefnet-general/birefnet-general.onnx', so, providers=['CPUExecutionProvider'])
inp = S.get_inputs()[0].name
sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel('../work6/scripts/FSRCNN_x2.pb'); sr.setModel('fsrcnn', 2)
M, SD = np.array([0.485, 0.456, 0.406]), np.array([0.229, 0.224, 0.225])
os.makedirs('edit/assets/cut', exist_ok=True); os.makedirs('sheets/masks', exist_ok=True)
for name in sys.argv[1:] or ['photo_a', 'photo_b', 'photo_c', 'photo_d']:
    f = cv2.imread(f'src/{name}.jpg')
    up = sr.upsample(f)
    im = cv2.cvtColor(cv2.resize(up, (1024, 1024), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    x = ((im - M) / SD).transpose(2, 0, 1)[None].astype(np.float32)
    p = 1 / (1 + np.exp(-S.run(None, {inp: x})[0][0, 0]))
    m = cv2.resize(p, (up.shape[1], up.shape[0]), interpolation=cv2.INTER_CUBIC).clip(0, 1)
    rgba = np.dstack([up, (m * 255).astype(np.uint8)])
    cv2.imwrite(f'edit/assets/cut/{name}.png', rgba); cv2.imwrite(f'sheets/masks/{name}_mask.png', (m * 255).astype(np.uint8))
    print(name, f.shape[:2], '->', up.shape[:2], 'alpha>0.5 frac', round(float((m > 0.5).mean()), 3), flush=True)
