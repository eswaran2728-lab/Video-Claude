"""Verify a rendered MP4 against the data block.

  python3 scripts/verify_render.py renders/avsec-cyber-roadshow.mp4

Checks: format (1080x1920, 30 fps, ~35 s, audio present), the QR code
decoded from the encoded video at several points of the end-card hold
matches challengeUrl, and the QR stays readable for at least 4 s.
Writes phone-size check frames to stills/.
Needs ffmpeg and `pip install zxing-cpp pillow`.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import zxingcpp
from PIL import Image

root = Path(__file__).resolve().parent.parent
video = Path(sys.argv[1] if len(sys.argv) > 1 else "renders/avsec-cyber-roadshow.mp4")
if not video.is_absolute():
    video = root / video

data_js = (root / "data/leaderboard.js").read_text()
m = re.search(r'challengeUrl:\s*"([^"]*)"', data_js)
url = m.group(1) if m else ""

probe = json.loads(subprocess.run(
    ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)],
    capture_output=True, text=True, check=True).stdout)
v = next(s for s in probe["streams"] if s["codec_type"] == "video")
a = [s for s in probe["streams"] if s["codec_type"] == "audio"]
dur = float(probe["format"]["duration"])
fps = v["r_frame_rate"]
ok = True

def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg)
    ok &= bool(cond)

check(v["width"] == 1080 and v["height"] == 1920, f"size {v['width']}x{v['height']}")
check(fps in ("30/1", "30000/1000"), f"fps {fps}")
check(abs(dur - 35.0) < 0.1, f"duration {dur:.2f}s")
check(len(a) == 1, f"audio streams: {len(a)}")

def frame(t, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", str(video), "-frames:v", "1", str(out)], check=True)
    return Image.open(out)

tmp = root / ".hyperframes" / "verify"
tmp.mkdir(parents=True, exist_ok=True)

# QR must decode to challengeUrl throughout the hold (30.6 s -> 34.9 s).
if url:
    readable = []
    for t in [30.4, 30.6, 31.5, 32.5, 33.5, 34.5, 34.9]:
        img = frame(t, tmp / f"qr-{t}.png")
        res = [r.text for r in zxingcpp.read_barcodes(img)]
        # Also at phone-ish resolution, as a phone camera filming a screen would see it.
        small = img.resize((540, 960), Image.LANCZOS)
        res_small = [r.text for r in zxingcpp.read_barcodes(small)]
        good = url in res and url in res_small
        readable.append((t, good))
        check(good, f"QR at {t:>4}s -> {res or 'nothing'} (half-size: {'ok' if url in res_small else 'no'})")
    held = [t for t, g in readable if g]
    check(held and held[-1] - held[0] >= 4.0, f"QR readable from {held[0] if held else '-'}s to {held[-1] if held else '-'}s")
    bad = [r for r in ("/host", "organizer") if r in url]
    check(not bad, "QR/URL is not a host or organizer link")
else:
    print("INFO no challengeUrl: QR intentionally absent, placeholder shown")

# Check frames for the review (full size and phone width).
stills = root / "stills"
stills.mkdir(exist_ok=True)
for name, t in [("01-opening", 3.2), ("02-recap", 6.9), ("03-firewall", 9.0), ("04-buildup", 12.0),
                ("05-third", 15.5), ("06-second", 19.0), ("07-first", 23.0), ("08-together", 28.5), ("09-endcard-qr", 33.0)]:
    img = frame(t, stills / f"{name}.png")
    img.convert("RGB").save(stills / f"{name}.jpg", quality=88)
    (stills / f"{name}.png").unlink()
    img.resize((360, 640), Image.LANCZOS).convert("RGB").save(tmp / f"{name}-phone.jpg", quality=90)

print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
