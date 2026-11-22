# work21 v02 plan: every photo (107) and both performance clips + the medal clip, ~2:11, fast cuts on the beat.
# Music: "Mumbai Chase", Steve Oxen (Fesliyan Studios), 109.998 BPM, started on its first big hit (song beat 7 = 3.853 s).
# Song sections in output beats: full energy 0-129, break 129-159 (quieter), hit on 159 + stop, back on 161, outro to the end.
import os
from PIL import Image
BPM = 109.998
B = 60 / BPM                      # 0.5455 s
MUSIC_IN = 0.035 + 7 * B          # 3.853 s
def b(k): return round(k * B, 3)
TOTAL = 131.4                     # song ends at 135.2 s -> output 131.35 s
OUT = "edit_v02"
MUSIC = "music/fesliyan_mumbai_chase_steve_oxen.mp3"
FADE = 1.2

# ---------------- video segments: clip, source in, output beats, speed, zoom ----------------
SEGS = [dict(id="h1", clip="IMG_1921", src=5.20, k0=0, k1=2), dict(id="h2", clip="IMG_1918", src=0.20, k0=2, k1=3, zoom=1.3),
        dict(id="h3", clip="IMG_1921", src=18.50, k0=3, k1=4), dict(id="h4", clip="IMG_1921", src=41.45, k0=4, k1=8),
        dict(id="c1", clip="IMG_1918", src=1.00, k0=8, k1=16)]
# performances (beats 24-64): clips alternate, with the four performance photos and the judges' table as one-beat inserts
PERF = [("v", "IMG_1921", 0.0, 2), ("p", "106", 1), ("v", "IMG_1918", 5.0, 2), ("v", "IMG_1921", 9.0, 2), ("p", "102", 1), ("v", "IMG_1918", 13.0, 2),
        ("v", "IMG_1921", 12.4, 2), ("p", "103", .5), ("p", "104", .5), ("v", "IMG_1918", 15.4, 2), ("v", "IMG_1921", 25.4, 2), ("v", "IMG_1921", 30.0, 2),
        ("p", "105", 1), ("v", "IMG_1918", 7.6, 2), ("v", "IMG_1921", 21.0, 1), ("v", "IMG_1918", 19.0, 2), ("s", "IMG_1921", 18.8, 4), ("v", "IMG_1921", 33.0, 2), ("v", "IMG_1918", 22.2, 2),
        ("v", "IMG_1921", 47.0, 2), ("v", "IMG_1921", 53.0, 2), ("v", "IMG_1921", 38.8, 3)]
PHOTOS = []
k = 24.0
for i, it in enumerate(PERF):
    if it[0] == "p": PHOTOS.append(dict(id=it[1], k0=k, k1=k + it[2])); k += it[2]
    else:
        SEGS.append(dict(id=f"p{i}", clip=it[1], src=it[2], k0=k, k1=k + it[3], speed=.5 if it[0] == "s" else 1, zoom=1.3 if it[1] == "IMG_1918" else None)); k += it[3]
assert abs(k - 64) < 1e-6, k
SEGS.append(dict(id="g1", clip="IMG_2025", src=0.30, k0=203, k1=211))
SLOWMO = (49, 53)                 # where the slow-motion segment sits (beats)

# ---------------- photo sections ----------------
SIZE = {f[5:8]: Image.open(f"src/png/{f}").size for f in os.listdir("src/png")}
GROUP = set("000 001 002 003 004 009 013 014 015 016 017 018 019 023 024 031 032 041 042 043 047 048 049 053 054 055 060 061 062 068 069 070 071 076 077 078 079 084 085 086 090 091 092 101".split())
BURST = set("001 002 003 004 014 032 038 040 042 054 065 067 075 077 079 085 092 104".split())   # near-identical follow-ups: half a beat
def mode(pid):
    w, h = SIZE[pid]
    return "full" if (w, h) == (720, 1280) else ("card" if pid in GROUP or w > h else "cover")
def section(ids, k0, k1, group_weight=1.5):
    w = [0.5 if p in BURST else (group_weight if p in GROUP else 1.0) for p in ids]; s = k1 - k0; acc = k0
    for p, x in zip(ids, w):
        d = x * s / sum(w); PHOTOS.append(dict(id=p, k0=round(acc, 4), k1=round(acc + d, 4))); acc += d
    PHOTOS[-1]["k1"] = k1
r = lambda a, z: [f"{i:03d}" for i in range(a, z + 1)]
section(["013", "014", "015", "016", "017", "000", "001", "002", "003", "004"], 16, 24)                       # the athletes on stage
section(r(5, 12) + r(18, 52), 64, 129)                                                                       # MEDALS & BELTS
section(r(93, 100), 129, 159, 1.0)                                                                           # the break: PROUD MOMENTS, slow pushes
section(r(53, 92), 161, 201)                                                                                 # ON THE STAGE, fast again
PHOTOS.append(dict(id="099", k0=159, k1=161, freeze=True))                                                   # the stop: freeze-flash
section(["101"], 201, 203)                                                                                   # the coaches, before the medal clip
for p in PHOTOS: p.setdefault("mode", mode(p["id"]))
WALL = (211, 225)                 # photo wall: all 107 photos assemble
K_END = 225
used = {p["id"] for p in PHOTOS}
assert used == set(SIZE), sorted(set(SIZE) - used)

EVENT_SMALL, EVENT_SUB = "MAJLIS PERASMIAN", "PERINGKAT DAERAH SEPANG 2026"
EVENT_DATE, EVENT_VENUE = "15 NOVEMBER 2026 (AHAD)", "UNIKL MIAT, DENGKIL"
BRAND1, BRAND2 = "MAHAGURU SRI S ARUMUGAM", "STUDENTS"
