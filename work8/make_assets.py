# Cut every visible video span from the EDL and assemble the cleaned dialogue track.
#  pane  : speaker under the hook board (1080x910, source y 170..1080), pre-cropped (the grading wrapper ignores object-position)
#  bubble: round face cam under the full-screen diagram (640x640 face crop -> 320x320)
#  full  : speaker full frame
#  broll : the creator's own footage from the AVSEC keychain shoot (work7, already relit/denoised there)
import subprocess, os, json, shutil
exec(open("edl.py").read())
A = "edit/assets/v"; os.makedirs(A, exist_ok=True)
FACE_X = {"b5ae": 450, "e5dd": 490, "d67f": 540, "a336": 510}       # face centre x in the 1080x1920 proxy (y ~ 500)
def src_at(t):                                                      # output time -> (clip, source time)
    for o0, o1, clip, a, b in OUT:
        if o0 <= t < o1 + 1e-6: return clip, a + (t - o0)
    o0, o1, clip, a, b = OUT[-1]; return clip, a + (t - o0)
def ff(args): subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y"] + args, check=True)
X264 = ["-an", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-g", "10", "-r", "30"]

# (id, kind, out_start, out_end, note) ; spans never cross an EDL segment boundary except where noted
SPANS = [
    ("pane0", "pane", 0.0, 2.9, "hook: speaker under the notebook sketch"),
    ("pane1", "pane", 2.9, 3.6, "pane slides away as the board expands"),
    ("cam1", "bubble", 3.4, 5.28, "okay guys, a diagram"),
    ("cam2", "bubble", 5.28, 9.66, "quality, cheap, fast"),
    ("cam3", "bubble", 12.2, 15.19, "remember these three things"),
    ("cam4", "bubble", 15.19, 21.19, "quality + cheap -> not fast"),
    ("full1", "full", 21.19, 23.1, "use it for every product"),
    ("cam5", "bubble", 25.4, 29.62, "choose two, drop one"),
    ("cam6", "bubble", 29.62, 40.95, "the two other pairs"),
    ("cam7", "bubble", 40.95, 43.3, "my ideology"),
    ("full2", "full", 43.3, 46.42, "comment below"),
]
BROLL = [("br1", "../work7/edit/assets/vc4/V7.mp4", 0.15, 9.66, 12.2, "a packed AVSEC keychain: a product being bought"),
         ("br2", "../work7/edit/assets/vc4/V1.mp4", 0.0, 23.1, 25.4, "his printer: build plate of keychains slides out (spending money with me)")]

for sid, kind, o0, o1, note in SPANS:
    clip, s = src_at(o0 + 1e-4); d = o1 - o0 + 0.1
    if kind == "pane": vf = "crop=1080:910:0:170"
    elif kind == "bubble": vf = f"crop=640:640:{FACE_X[clip] - 320}:180,scale=320:320:flags=lanczos"
    else: vf = "null"
    ff(["-ss", f"{s:.3f}", "-i", f"proxy/{clip}.mp4", "-t", f"{d:.3f}", "-vf", vf] + X264 + [f"{A}/{sid}.mp4"])
for bid, f, s, o0, o1, note in BROLL:
    ff(["-ss", f"{s:.3f}", "-i", f, "-t", f"{o1 - o0 + 0.1:.3f}"] + X264 + [f"{A}/{bid}.mp4"])

# dialogue: denoised speech (denoise.py), 20/30 ms fades per piece, joined, levelled
parts = []
for i, (o0, o1, clip, a, b) in enumerate(OUT):
    p = f"edit/assets/dlg_{i}.wav"
    ff(["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", f"edit/assets/clean_{clip}.wav", "-af",
        f"highpass=f=85,afade=t=in:d=0.02,afade=t=out:st={b - a - 0.03:.3f}:d=0.03", "-ar", "48000", "-ac", "2", p])
    parts.append(p)
with open("edit/assets/dlg_list.txt", "w") as f:
    for p in parts: f.write(f"file '{os.path.basename(p)}'\n")
ff(["-f", "concat", "-safe", "0", "-i", "edit/assets/dlg_list.txt", "-af", "loudnorm=I=-16:TP=-2:LRA=7", "-ar", "48000", "-c:a", "pcm_s16le", "edit/assets/dialogue.wav"])
for p in parts: os.remove(p)
os.remove("edit/assets/dlg_list.txt")
json.dump({"speech": [dict(zip(["out_start", "out_end", "clip", "src_in", "src_out"], o)) for o in OUT],
           "spans": [dict(id=s[0], kind=s[1], out_start=s[2], out_end=s[3], src=dict(zip(["clip", "src_in"], src_at(s[2] + 1e-4))), note=s[4]) for s in SPANS],
           "broll": [dict(id=b[0], file=b[1], src_in=b[2], out_start=b[3], out_end=b[4], note=b[5]) for b in BROLL]},
          open("edit/timing_map.json", "w"), indent=1)
print("ok", SPEECH_END, TOTAL)
