# v04 web b-roll (creator: "add broll from web that relevant to what i talk"). Only beats where he describes the problem;
# every product/feature/payoff shot stays his real footage (no other earbuds shown). Source: Mixkit, each item checked on
# its own page for "Mixkit Stock Video Free License" (commercial + social use, no attribution required), 2026-10-28.
# Streamed from the 4K file, trimmed to the line, cropped 9:16 around the person, pre-darkened toward the v03 look
# (the plate's media-treatment grade is applied to these elements too). -> edit/assets/v/broll_<id>.mp4 (1080x1920, 30 fps)
import subprocess, json, plan
S = plan.s2o
BROLL = [  # id, page slug, what he says at that moment, src_in (s), crop x in the 3840-wide frame, out window
    (232, "woman-walks-through-the-city-speaking-on-the-phone-232", "noise romba irukkumna (background noise on a call)", 2.0, 1560, S(1.86), S(3.72)),
    (918, "busy-office-space-918", "office-la irunthaalum sari", 0.5, 1500, S(4.90), S(6.83)),
    (239, "woman-talking-on-the-phone-in-a-car-239", "car-la porappa", 0.2, 880, S(6.83), S(7.83)),
    (8742, "young-man-upset-while-talking-on-the-phone-8742", "romba call pesurappa, romba noise kidaikkum", 2.4, 1820, S(9.85), S(12.10)),
]
LIFT = {239: 0.17, 8742: 0.16}              # low-key originals: lift so faces read after the shared v03 grade
LOOK = "eq=brightness={b}:contrast=1.08:saturation=0.75,colorbalance=rs=-0.04:bs=0.05:rh=0.03:bh=-0.02,vignette=PI/4.5"
meta = []
for vid, slug, line, s_in, cx, o0, o1 in BROLL:
    d = round(o1 - o0, 3); out = f"edit/assets/v/broll_{vid}.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(s_in), "-i", f"https://assets.mixkit.co/videos/{vid}/{vid}-2160.mp4",
                    "-t", str(d + 0.1), "-an", "-vf", f"fps=30,crop=1215:2160:{cx}:0,scale=1080:1920:flags=lanczos,{LOOK.format(b=round(-0.05 + LIFT.get(vid, 0), 3))},format=yuv420p",
                    "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-g", "15", "-bf", "0", out], check=True)
    meta.append({"id": vid, "page": f"https://mixkit.co/free-stock-video/{slug}/", "licence": "Mixkit Stock Video Free License",
                 "line": line, "src_in": s_in, "crop": f"1215x2160 at x={cx} of 3840x2160", "out_start": o0, "out_end": o1})
    print(vid, o0, o1, d)
json.dump(meta, open("broll.json", "w"), indent=1)
