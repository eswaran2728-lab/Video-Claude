# Event recap assets: tracked 9:16 crops of the stage footage, photo plates for the animated stills, the audio bed.
# Sources are never modified: proxy/*.mov are SDR masters streamed from the Drive originals, src/dl/* the downloads.
import cv2, json, subprocess, numpy as np, soundfile as sf, os
from PIL import Image
os.makedirs("edit/assets/v", exist_ok=True); os.makedirs("edit/assets/p", exist_ok=True)
TR = json.load(open("edit/track.json")); TT, TX = np.array(TR["t"]), np.array(TR["x"])
W4, H4 = 3840, 2160
GRADE = "eq=contrast=1.06:saturation=1.10:gamma=0.98,unsharp=5:5:0.35"     # lifts the slightly flat HLG->SDR conversion

# (id, src in, src out, crop width, crop top, x bias)  output == source time for IMG_6421 (its song is the soundtrack)
# cut points sit on the song's beat grid (~122 BPM, beats at 0.280 + n*0.491 s)
SEGS = [("v_walk", 2.733, 4.205, 1215, 0, 0), ("v_stage1", 4.205, 9.603, 1215, 0, 40),
        ("v_stage2", 9.603, 12.547, 1080, 300, 60), ("v_stage3", 15.000, 16.472, 1215, 0, 40)]
def render(sid, a, b, cw, top, bias):
    ch = round(cw * 16 / 9); cap = cv2.VideoCapture("proxy/IMG_6421.mov"); cap.set(cv2.CAP_PROP_POS_MSEC, a * 1000)
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30", "-i", "-",
                            "-vf", GRADE, "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-g", "10", f"edit/assets/v/{sid}.mp4"],
                           stdin=subprocess.PIPE)
    n = 0
    while True:
        t = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        if t >= b + 0.1: break
        ok, f = cap.read()
        if not ok: break
        cx = float(np.interp(t, TT, TX)) + bias
        x0 = int(np.clip(cx - cw / 2, 0, W4 - cw)); y0 = int(np.clip(top, 0, H4 - ch))
        enc.stdin.write(cv2.resize(f[y0:y0 + ch, x0:x0 + cw], (1080, 1920), interpolation=cv2.INTER_AREA if cw >= 1080 else cv2.INTER_LANCZOS4).tobytes()); n += 1
    enc.stdin.close(); enc.wait(); print(sid, n, "frames", flush=True)
for s in SEGS: render(*s)

# photo plates: full-res decode (ffmpeg handles the DNGs), scaled to 2400 px tall so a 9:16 window can pan and push in
PHOTOS = {"IMG_6426": "src/dl/IMG_6426.DNG", "IMG_6429": "src/dl/IMG_6429.DNG", "IMG_6437": "src/dl/IMG_6437.DNG",
          "IMG_6439": "src/dl/IMG_6439.DNG", "IMG_6423": "src/dl/IMG_6423.DNG"}
for k, f in PHOTOS.items():
    tmp = f"sheets/full_{k}.png"
    if not os.path.exists(tmp): subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f, "-frames:v", "1", tmp], check=True)
    im = Image.open(tmp).convert("RGB"); w = round(im.width * 2400 / im.height)
    im.resize((w, 2400), Image.LANCZOS).save(f"edit/assets/p/{k}.jpg", quality=90); print(k, im.size, "->", (w, 2400))

# audio: the event's own song (IMG_6421, 0-24.37 s) then the booth's room sound (IMG_6425) under the close
SR = 48000
def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", p, "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                                        capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
TOTAL = 25.4
song, amb = load("proxy/IMG_6421.mov"), load("proxy/IMG_6425.mov")
out = np.zeros((int(TOTAL * SR), 2), np.float32)
n = len(song); env = np.ones(n); f0 = int(23.65 * SR); env[f0:] = np.linspace(1, 0, n - f0) ** 1.5; env[:int(0.02 * SR)] = np.linspace(0, 1, int(0.02 * SR))
out[:n] += song * env[:, None]
a0 = int(23.75 * SR); seg = amb[:len(out) - a0]; e = np.ones(len(seg))
e[:int(0.45 * SR)] = np.linspace(0, 1, int(0.45 * SR)); e[-int(0.9 * SR):] = np.linspace(1, 0, int(0.9 * SR))
gain = 10 ** ((-15 - (-23.5)) / 20) * 0.55                                   # room sound up to just under the song level
out[a0:a0 + len(seg)] += seg * e[:, None] * gain
sf.write("edit/assets/audio.wav", out, SR, subtype="PCM_16")
print("audio", TOTAL, "s, peak", round(float(np.abs(out).max()), 3))
json.dump({"segments": [dict(id=s[0], src="IMG_6421.MOV", src_in=s[1], src_out=s[2], out_start=s[1], out_end=s[2], crop_w=s[3], crop_top=s[4]) for s in SEGS],
           "photos": PHOTOS, "audio": {"song": "IMG_6421.MOV 0-24.37 s -> 0-24.37 s, fade 23.65-24.37", "room": "IMG_6425.MOV 0-1.65 s -> 23.75-25.4 s"}},
          open("edit/assets_map.json", "w"), indent=1)
