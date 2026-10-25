# Cut video-only clips and assemble the cleaned dialogue track from the EDL.
import subprocess, os
CLEAN = os.environ.get("VERSION", "v03") not in ("v01", "v02")
DLG = "dialogue.wav" if not CLEAN else "dialogue_v03.wav"
exec(open("edl.py").read())
A = "edit/assets/v"
def cut(name, clip, a, d):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", f"proxy/{clip}.mp4", "-t", f"{d + 0.1:.3f}", "-an",
                    "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-g", "10", f"{A}/{name}.mp4"], check=True)
for vid, layout, clip, a, o0, o1, note in V:
    cut(vid, clip, a, o1 - o0)
    if layout == "split":  # the speaker for the lower pane, in sync with the dialogue
        seg = next(i for i, s in enumerate(OUT) if s[0] <= o0 < s[1])
        cut(vid + "_face", OUT[seg][2], OUT[seg][3] + (o0 - OUT[seg][0]), o1 - o0)
# dialogue: each sentence denoised (workshop hum/fans), 20 ms fades, joined on the output timeline
parts = []
for i, (o0, o1, clip, a, b) in enumerate(OUT):
    p = f"edit/assets/dlg_{i}.wav"
    src = f"edit/assets/clean_{clip}.wav" if CLEAN else f"proxy/{clip}.mp4"   # clean_*.wav from denoise.py
    nr = "" if CLEAN else "afftdn=nf=-28:nr=10,"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", src, "-vn",
                    "-af", f"highpass=f=85,{nr}afade=t=in:d=0.02,afade=t=out:st={b - a - 0.03:.3f}:d=0.03",
                    "-ar", "48000", "-ac", "2", p], check=True)
    parts.append(p)
with open("edit/assets/dlg_list.txt", "w") as f:
    for p in parts: f.write(f"file '{os.path.basename(p)}'\n")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "edit/assets/dlg_list.txt", "-af", "loudnorm=I=-16:TP=-2:LRA=7", "-ar", "48000", "-c:a", "pcm_s16le", f"edit/assets/{DLG}"], check=True)
for p in parts: os.remove(p)
os.remove("edit/assets/dlg_list.txt")
# split panes are pre-cropped (the colour-grading wrapper does not honour object-position)
for vid, layout, *_ in V:
    if layout == "split":
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{A}/{vid}.mp4", "-vf", "crop=1080:1000:0:460", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", f"{A}/{vid}_top.mp4"], check=True)
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{A}/{vid}_face.mp4", "-vf", "crop=1080:960:0:67", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", f"{A}/{vid}_faceC.mp4"], check=True)
print("ok", SPEECH_END)
