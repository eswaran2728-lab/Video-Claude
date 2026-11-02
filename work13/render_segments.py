# Render every planned segment to a 1080x1920 30 fps piece, then join each part into one plate.
#  'p'  portrait: scaled to cover 1080x1920.
#  'l'  landscape: a zoomed band (height by source size) cropped around the action (motion centroid of the segment),
#       over a blurred, darker cover copy of the same clip.
#  'lt' landscape title background: blurred, darker cover copy only (the title card sits on it).
#  speed < 1: motion-interpolated slow motion (minterpolate mci/aobmc to 30/speed fps, then timestamps stretched).
# Light festival grade on everything (contrast +6 %, saturation +8 %, gentle unsharp). Audio is built in mix13.py.
# -> edit/assets/v/part{1,2}_plate.mp4 (+ segments.json with each piece's crop/center for the timing map)
import json, os, subprocess, sys, numpy as np, cv2
import plan13 as P
os.makedirs("edit/assets/v", exist_ok=True); os.makedirs("renders/seg", exist_ok=True)
GRADE = "eq=contrast=1.06:saturation=1.08,unsharp=5:5:0.4"
BAND = {576: 1180, 464: 1080, 368: 980}             # band height by source height (2.0x / 2.3x / 2.7x zoom)
CENTER = {("v_215631", 0.0): 0.60}                    # manual crop centre where motion picks the wrong subject (MCs at right)


def dims(clip):
    w, h = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0",
                           f"src/norm/{clip}.mp4"], capture_output=True, text=True).stdout.strip().split(",")
    return int(w), int(h)


def action_center(clip, a, b):
    """horizontal centre (0..1) of motion inside [a,b]; ignores the outer 6 % (lights flicker at the edges)"""
    cap = cv2.VideoCapture(f"src/norm/{clip}.mp4"); prev = None; acc = None
    for i in range(round(a * 30), round(b * 30) + 1, 2):
        cap.set(1, i); ok, f = cap.read()
        if not ok: break
        g = cv2.cvtColor(cv2.resize(f, (160, int(160 * f.shape[0] / f.shape[1]))), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            d = np.abs(g - prev).sum(axis=0); acc = d if acc is None else acc + d
        prev = g
    if acc is None or acc.sum() == 0: return 0.5
    acc[:10] = 0; acc[-10:] = 0; x = np.arange(len(acc))
    return float(np.clip((acc * x).sum() / acc.sum() / len(acc), 0.3, 0.7))


def seg_filter(seg, w, h):
    sp = seg["speed"]; slow = f",minterpolate=fps={round(30 / sp, 3)}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts=PTS/{sp},fps=30" if sp < 1 else ""
    fast = f",setpts=PTS/{sp},fps=30" if sp > 1 else ""
    pre = f"[0:v]setpts=PTS-STARTPTS{slow}{fast},{GRADE},split=2[s1][s2];"
    cover = f"[s1]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    if seg["kind"] == "p":
        return pre + cover + "[o];[s2]nullsink", None
    bg = cover + ",boxblur=28:2,eq=brightness=-0.16:saturation=0.75[bg];"
    if seg["kind"] == "lt":
        return pre + cover + ",boxblur=22:2,eq=brightness=-0.28:saturation=0.8[o];[s2]nullsink", None
    bh = BAND.get(h, 1100); sw = round(w * bh / h)
    cx = CENTER.get((seg["clip"], seg["src_in"])) or action_center(seg["clip"], seg["src_in"], seg["src_out"])
    x0 = int(min(max(cx * sw - 540, 0), sw - 1080))
    fg = f"[s2]scale={sw}:{bh}:flags=lanczos,crop=1080:{bh}:{x0}:0[fg];"
    return pre + bg + fg + f"[bg][fg]overlay=0:{960 - bh // 2}[o]", dict(center=round(cx, 3), band=bh, crop_x=x0, zoom=round(bh / h, 2))


def render_part(name, segs):
    tl, total = P.timeline(segs); pieces = []; meta = []
    for i, s in enumerate(tl):
        w, h = dims(s["clip"]); fc, info = seg_filter(s, w, h); out = f"renders/seg/{name}_{i:02d}.mp4"
        d = s["out_end"] - s["out_start"]
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(s["src_in"]), "-t", str(s["src_out"] - s["src_in"] + 0.1),
                        "-i", f"src/norm/{s['clip']}.mp4", "-filter_complex", fc, "-map", "[o]", "-t", str(d), "-an",
                        "-r", "30", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], check=True)
        n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                                "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip())
        pieces.append(out); meta.append({**s, **(info or {}), "frames": n}); print(name, i, s["clip"], s["speed"], d, n, info, flush=True)
    lst = f"renders/seg/{name}.txt"; open(lst, "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in pieces))
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    f"edit/assets/v/{name}_plate.mp4"], check=True)
    return meta, total


if __name__ == "__main__":
    which = sys.argv[1:] or ["part1", "part2"]
    out = json.load(open("segments.json")) if os.path.exists("segments.json") else {}
    for nm in which:
        meta, total = render_part(nm, P.PART1 if nm == "part1" else P.PART2); out[nm] = {"total": total, "segments": meta}
    json.dump(out, open("segments.json", "w"), indent=1)
