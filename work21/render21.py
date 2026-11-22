# Prepares the media for the HyperFrames project from plan21:
#  - one graded 1080x1920 30 fps video plate (black under the photo / end-card sections) -> edit/assets/v/plate.mp4
#  - graded photos: 'cover' 9:16 crops, 'card' full photos (1080 wide) + blurred fills -> edit/assets/p/
# Grade: exposure/contrast tidy-up with a gentle S-curve, +6 % contrast, +6 % saturation, slight warmth, light sharpening, soft vignette.
import json, os, subprocess
import plan21 as P
os.makedirs("edit/assets/v", exist_ok=True); os.makedirs("edit/assets/p", exist_ok=True); os.makedirs("renders/seg", exist_ok=True)
GRADE = ("eq=contrast=1.06:saturation=1.06:gamma=0.98,curves=master='0/0.015 0.25/0.235 0.5/0.505 0.78/0.81 1/0.975',"
         "colorbalance=rh=0.02:bh=-0.015,unsharp=5:5:0.4")
VIG = ",vignette=PI/6"
TR = json.load(open("track_1918.json"))
SW, SH = 464, 848


def track_at(t):
    i = min(len(TR["x"]) - 1, max(0, round(t * TR["fps"]))); return TR["x"][i] * SW, TR["y"][i] * SH


def run(cmd): subprocess.run(cmd, check=True)


def frames(o): return int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", o],
                                         capture_output=True, text=True).stdout.strip())


pieces, t_frames = [], 0
for s in sorted(P.SEGS, key=lambda x: x["k0"]):
    f0, f1 = round(P.b(s["k0"]) * 30), round(P.b(s["k1"]) * 30)
    if f0 > t_frames:
        g = f"renders/seg/gap_{len(pieces):02d}.mp4"
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0b0b10:s=1080x1920:r=30:d={(f0 - t_frames) / 30 + 1:.3f}", "-frames:v", str(f0 - t_frames),
             "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", g]); pieces.append(g)
    n = f1 - f0; sp = s.get("speed", 1.0); dur = n / 30
    tm = (f",minterpolate=fps={round(30 / sp, 3)}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts=PTS/{sp},fps=30" if sp < 1 else "")
    z = s.get("zoom")
    if z:                                                  # follow-crop: linear pan between the tracked positions at the segment's ends
        cw, ch = round(SW / z / 2) * 2, round(SW / z * 16 / 9 / 2) * 2
        (xa, ya), (xb, yb) = track_at(s["src"]), track_at(s["src"] + dur * sp)
        X = lambda x: min(max(x - cw / 2, 0), SW - cw); Y = lambda y: min(max(y - ch * 0.55, 0), SH - ch)
        crop = f"crop={cw}:{ch}:x='{X(xa):.1f}+({X(xb) - X(xa):.1f})*t/{dur:.3f}':y='{Y(ya):.1f}+({Y(yb) - Y(ya):.1f})*t/{dur:.3f}',scale=1080:1920:flags=lanczos"
    else:
        crop = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920"
    o = f"renders/seg/{s['id']}.mp4"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(s["src"]), "-t", f"{dur * sp + 0.3:.3f}", "-i", f"src/mov/{s['clip']}.MOV",
         "-vf", f"setpts=PTS-STARTPTS{tm},{crop},{GRADE}{VIG}", "-frames:v", str(n), "-an", "-r", "30", "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", o])
    assert frames(o) == n, (s["id"], frames(o), n)
    pieces.append(o); t_frames = f1
TF = round(P.TOTAL * 30)
if TF > t_frames:
    g = "renders/seg/gap_end.mp4"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0b0b10:s=1080x1920:r=30:d={(TF - t_frames) / 30 + 1:.3f}", "-frames:v", str(TF - t_frames),
         "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", g]); pieces.append(g)
open("renders/seg/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in pieces))
run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "renders/seg/list.txt", "-c", "copy", "edit/assets/v/plate.mp4"])
assert frames("edit/assets/v/plate.mp4") == TF, frames("edit/assets/v/plate.mp4")

# ---- photos ----
def still(src, vf, out): run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vf", vf, "-q:v", "3", "-frames:v", "1", out])
for p in P.PHOTOS + [dict(id=P.END_BG, mode="card", fx=.5)]:
    src = f"src/png/File_{p['id']}.png"
    if p["mode"] == "cover":                               # 9:16 window of the 3:4 photo at focus fx
        still(src, f"crop=720:1280:{(960 - 720) * min(max((p['fx'] - .375) / .25, 0), 1):.0f}:0,scale=1080:1920:flags=lanczos,{GRADE}{VIG}", f"edit/assets/p/{p['id']}.jpg")
    else:
        still(src, f"scale=1080:-2:flags=lanczos,{GRADE}", f"edit/assets/p/{p['id']}.jpg")
        still(src, f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{GRADE},boxblur=30:2,eq=brightness=-0.25:saturation=0.85", f"edit/assets/p/{p['id']}_bg.jpg")
print("plate", TF, "frames;", len(P.PHOTOS), "photos")
