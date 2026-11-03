# Video segments of plan15.SEGS -> one 80 s plate (black where the HTML photo / graphic sections are) -> edit/assets/v/plate.mp4
#  'p'  : scale to cover 1080x1920 (centre crop)         'bg': same, blurred + darkened (cards sit on it)
#  speed<1: motion-interpolated slow motion (minterpolate mci/aobmc), else setpts.
# Grade: gentle S-curve, contrast +7 %, saturation +5 %, a touch of warmth in the highlights, light sharpening; soft vignette.
import json, os, subprocess
import os, importlib
VERSION = os.environ.get("VERSION", "v01"); SUF = "" if VERSION == "v01" else "_" + VERSION
P = importlib.import_module("plan15" if VERSION == "v01" else f"plan15_{VERSION}")
os.makedirs("edit/assets/v", exist_ok=True); os.makedirs("renders/seg", exist_ok=True)
GRADE = ("eq=contrast=1.07:saturation=1.05:gamma=0.98,curves=master='0/0.02 0.25/0.235 0.5/0.505 0.78/0.81 1/0.97',"
         "colorbalance=rh=0.025:bh=-0.02,unsharp=5:5:0.35")
FIN = ",vignette=PI/6"


def filt(s):
    sp = s["speed"]
    tm = (f",minterpolate=fps={round(30 / sp, 3)}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts=PTS/{sp},fps=30" if sp <= 0.6
          else (f",setpts=PTS/{sp},fps=30" if sp != 1 else ""))
    cover = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920"
    if s["kind"] == "raw": return f"setpts=PTS-STARTPTS,{cover}"            # creator's finished graphic clip: no grade
    if s["kind"] == "bg":
        return f"setpts=PTS-STARTPTS{tm},{cover},{GRADE},boxblur=26:2,eq=brightness=-0.22:saturation=0.8{FIN}"
    return f"setpts=PTS-STARTPTS{tm},{cover},{GRADE}{FIN}"


pieces, meta, t = [], [], 0.0
def black(d, i):
    o = f"renders/seg/{VERSION}_gap_{i:02d}.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0e0b10:s=1080x1920:r=30:d={d + 1:.4f}", "-frames:v", str(round(d * 30)),
                    "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", o], check=True); return o
for i, s in enumerate(sorted(P.SEGS, key=lambda x: x["t0"])):
    f0, f1 = round(s["t0"] * 30), round(s["t1"] * 30)
    if f0 > round(t * 30): pieces.append(black((f0 - round(t * 30)) / 30, i))
    n = f1 - f0; o = f"renders/seg/{VERSION}_{s['id']}.mp4"; need = n / 30 * s["speed"] + 0.2
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(s["src_in"]), "-t", f"{need:.3f}", "-i", f"proxy/{s['clip']}.mp4",
                    "-vf", filt(s), "-frames:v", str(n), "-an", "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", o], check=True)
    got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                              "-of", "csv=p=0", o], capture_output=True, text=True).stdout.strip())
    assert got == n, (s["id"], got, n)
    pieces.append(o); meta.append({**s, "frames": n, "src_out": round(s["src_in"] + n / 30 * s["speed"], 3)}); t = f1 / 30
    print(s["id"], n, flush=True)
if round(t * 30) < round(P.TOTAL * 30): pieces.append(black((round(P.TOTAL * 30) - round(t * 30)) / 30, 99))
open(f"renders/seg/list{SUF}.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in pieces))
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"renders/seg/list{SUF}.txt", "-c", "copy",
                f"edit/assets/v/plate{SUF}.mp4"], check=True)
json.dump(meta, open(f"segments{SUF}.json", "w"), indent=1); print("plate", P.TOTAL)
