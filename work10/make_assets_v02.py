# v02 assets (v01's make_assets.py and its clips are kept). Creator's notes on v01: no GTR content, use all the images and
# videos, make it a visually stunning recap.
#  - booth video IMG_6425: 9:16 crop on the AVSEC side (the GTR banner at the right edge stays out), slowed to fill 3 bars
#  - phone clips b048 / dc95 (576 / 464 px wide): framed card + pre-blurred full-frame background (honest about the source)
#  - photo plates for all 19 stills, 20 mosaic tiles (19 photos + one stage frame) for the finale
#  - audio: House Fest (Mixkit, Stock Music Free License) -> the event song from IMG_6421 -> House Fest
import json, os, subprocess, numpy as np, soundfile as sf
from PIL import Image
A = "edit/assets"; os.makedirs(f"{A}/v2", exist_ok=True); os.makedirs(f"{A}/p", exist_ok=True); os.makedirs(f"{A}/tiles", exist_ok=True)
def ff(args): subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y"] + args, check=True)
X264 = ["-an", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-g", "10", "-r", "30"]
GRADE = "eq=contrast=1.06:saturation=1.10:gamma=0.98"

# booth video: crop x 0.29-0.61 of the 3840 frame (AVSEC banner + screens), 3.97 s stretched to 5.86 s (slow, steady shot)
ff(["-i", "proxy/IMG_6425.mov", "-vf", f"crop=1215:2160:1110:0,scale=1080:1920:flags=lanczos,setpts=1.4762*PTS,{GRADE}", "-t", "5.95"] + X264 + [f"{A}/v2/v_booth.mp4"])
# phone clips: card 760x1352 + blurred background
for vid, src, a, d in [("b048", "src/dl/b048.mp4", 9.0, 3.95), ("dc95", "src/dl/dc95.mp4", 18.0, 2.0)]:
    ff(["-ss", str(a), "-i", src, "-t", str(d), "-vf", f"fps=30,scale=760:1352:flags=lanczos,{GRADE}"] + X264 + [f"{A}/v2/{vid}_card.mp4"])
    ff(["-ss", str(a), "-i", src, "-t", str(d), "-vf", "fps=30,scale=1080:1920:flags=bicubic,boxblur=40:3,eq=brightness=-0.18:saturation=1.2"] + X264 + [f"{A}/v2/{vid}_bg.mp4"])

# photo plates: landscape -> 4267x2400 (shown at 3840x2160); the one portrait JPG -> 1350x2400
ALL = ["IMG_6426", "IMG_6427", "IMG_6461", "IMG_6436", "2ee1beb9", "38af901c", "912ed0e8", "ACAE9274", "IMG_6433", "IMG_6423",
       "IMG_6429", "IMG_6430", "IMG_6437", "IMG_6438", "IMG_6439", "IMG_6440", "IMG_6435", "IMG_6419", "IMG_6420"]
def load(k):
    if os.path.exists(f"src/dl/{k}.jpg"): return Image.open(f"src/dl/{k}.jpg").convert("RGB")
    f = f"sheets/full_{k}.png"
    if not os.path.exists(f): ff(["-i", f"src/dl/{k}.DNG", "-frames:v", "1", f])
    return Image.open(f).convert("RGB")
FOCUS = {"IMG_6426": .36, "IMG_6427": .5, "IMG_6461": .35, "IMG_6436": .30, "2ee1beb9": .55, "38af901c": .40, "912ed0e8": .5,
         "ACAE9274": .35, "IMG_6433": .33, "IMG_6423": .44, "IMG_6429": .5, "IMG_6430": .5, "IMG_6437": .38, "IMG_6438": .37,
         "IMG_6439": .36, "IMG_6440": .42, "IMG_6435": .55, "IMG_6419": .5, "IMG_6420": .5}
sizes = {}
for k in ALL:
    im = load(k)
    if im.width >= im.height: out = im.resize((round(im.width * 2400 / im.height), 2400), Image.LANCZOS)
    else: out = im.resize((1350, 2400), Image.LANCZOS)
    out.save(f"{A}/p/{k}.jpg", quality=88); sizes[k] = out.size
    # mosaic tile 270x384 (portrait) around the focus, as 2x for sharpness
    tw = round(im.height * 270 / 384); cx = int(FOCUS[k] * im.width); x0 = max(0, min(im.width - tw, cx - tw // 2))
    im.crop((x0, 0, x0 + tw, im.height)).resize((540, 768), Image.LANCZOS).save(f"{A}/tiles/{k}.jpg", quality=85)
    print(k, im.size, "->", out.size, flush=True)
ff(["-ss", "11.0", "-i", "proxy/IMG_6421.mov", "-frames:v", "1", "-vf", "crop=1215:2160:900:0,scale=540:768", f"{A}/tiles/stage_frame.jpg"])

# ---------- audio (48 kHz stereo) ----------
SR = 48000; P = 60 / 123.0
def load_a(p, a=0.0, d=None):
    args = ["ffmpeg", "-nostdin", "-v", "error", "-ss", str(a), "-i", p] + (["-t", str(d)] if d else []) + ["-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(args, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
TOTAL = 45.0; SONG_OFF = 14.826                 # out = song time + 14.826 (song beat n=5 at 2.733 lands on out 17.559)
out = np.zeros((int(TOTAL * SR), 2), np.float32)
def place(x, t0, fin=0.0, fout=0.0, gain=1.0):
    i0 = int(t0 * SR); x = x[:len(out) - i0].copy(); n = len(x); e = np.ones(n)
    if fin: k = int(fin * SR); e[:k] = np.linspace(0, 1, k)
    if fout: k = int(fout * SR); e[-k:] = np.linspace(1, 0, k) ** 1.3
    out[i0:i0 + n] += x * (e * gain)[:, None]
music = "music/mixkit_113_house_fest.mp3"
place(load_a(music, 0.455 + 32 * P, 17.559 + 0.30), 0.0, fin=0.02, fout=0.30, gain=0.62)          # bars from track 16.07 s
place(load_a("proxy/IMG_6421.mov", 2.733 - 0.12, 24.37 - 2.733 + 0.12), 17.559 - 0.12, fin=0.12, fout=0.45, gain=1.0)
place(load_a(music, 0.455 + 125 * P - 0.25, TOTAL - 39.196 + 0.25), 39.196 - 0.25, fin=0.25, fout=1.6, gain=0.62)
sf.write(f"{A}/audio_v02.wav", out, SR, subtype="PCM_16")
print("audio v02", TOTAL, "peak", round(float(np.abs(out).max()), 3))
json.dump({"music": "Mixkit 'House Fest' by Alejandro Magaña (Stock Music Free License) https://mixkit.co/free-stock-music/tag/corporate/ "
                    "track 16.07-33.9 s -> out 0-17.86; track 61.43-67.5 s -> out 38.95-45.0",
           "song": "IMG_6421.MOV 2.61-24.37 s -> out 17.44-39.2 s (event performance track)", "photo_sizes": sizes},
          open("edit/assets_map_v02.json", "w"), indent=1)
