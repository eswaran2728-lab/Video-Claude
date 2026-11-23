# work21 v05 = v04 without repeats ("remove the duplicate videos that arrive multiple times, make it one time a bit longer"):
#  - every clip moment is used once (no overlapping source ranges); the hook's spin is no longer repeated by the slow motion,
#    and the performance cuts are fewer and longer (mostly 3 beats instead of 2);
#  - near-identical burst photos are dropped; the kept photo takes the whole burst's time;
#  - 099 is no longer shown twice: the freeze-flash lands on the last close-up of the break;
#  - the photo wall shows the unique photos only. Music, beat grid and all other sections are unchanged.
from PIL import Image, ImageOps
import plan21_v04 as V4
from plan21_v02 import BPM, B, MUSIC_IN, b, TOTAL, MUSIC, FADE, WALL, K_END, GROUP, BURST, EVENT_SMALL, EVENT_SUB, EVENT_DATE, EVENT_VENUE, BRAND1, BRAND2, mode
OUT = "edit_v05"
SRC = V4.SRC

# ---------------- clips: one use per moment ----------------
SEGS = [dict(id="h1", clip="IMG_1921", src=5.20, k0=0, k1=2), dict(id="h2", clip="IMG_1918", src=0.20, k0=2, k1=3, zoom=1.3),
        dict(id="h3", clip="IMG_1921", src=28.00, k0=3, k1=4), dict(id="h4", clip="IMG_1921", src=41.45, k0=4, k1=8),
        dict(id="c1", clip="IMG_1918", src=1.00, k0=8, k1=16)]
PERF = [("v", "IMG_1921", 0.0, 2), ("p", "106", 1), ("v", "IMG_1918", 5.4, 3), ("v", "IMG_1921", 9.0, 3), ("p", "102", 1), ("v", "IMG_1921", 12.4, 3),
        ("v", "IMG_1918", 13.0, 2), ("p", "103", 1), ("v", "IMG_1918", 15.4, 2), ("s", "IMG_1921", 18.8, 4), ("v", "IMG_1921", 25.4, 3), ("p", "105", 1),
        ("v", "IMG_1918", 19.0, 2), ("v", "IMG_1921", 30.0, 2), ("v", "IMG_1921", 33.0, 2), ("v", "IMG_1918", 22.2, 3), ("v", "IMG_1921", 47.0, 2),
        ("v", "IMG_1921", 38.8, 3)]
PHOTOS = []
k = 24.0
for i, it in enumerate(PERF):
    if it[0] == "p": PHOTOS.append(dict(id=it[1], k0=k, k1=k + it[2], mode=mode(it[1]))); k += it[2]
    else:
        SEGS.append(dict(id=f"p{i}", clip=it[1], src=it[2], k0=k, k1=k + it[3], speed=.5 if it[0] == "s" else 1, zoom=1.3 if it[1] == "IMG_1918" else None)); k += it[3]
assert abs(k - 64) < 1e-6, k
SLOWMO = next((s["k0"], s["k1"]) for s in SEGS if s.get("speed", 1) < 1)
SEGS.append(dict(id="g1", clip="IMG_2025", src=0.30, k0=203, k1=207))
# no clip moment twice
for c in ("IMG_1921", "IMG_1918", "IMG_2025"):
    rs = sorted((s["src"], s["src"] + (b(s["k1"]) - b(s["k0"])) * s.get("speed", 1)) for s in SEGS if s["clip"] == c)
    assert all(a[1] <= z[0] for a, z in zip(rs, rs[1:])), (c, rs)

# ---------------- photos: one of each burst, longer ----------------
SIZE = V4.SIZE
def section(ids, k0, k1, group_weight=1.5):
    ids = [p for p in ids if p not in BURST]
    w = [group_weight if p in GROUP else 1.0 for p in ids]; acc = k0
    for p, x in zip(ids, w):
        d = x * (k1 - k0) / sum(w); PHOTOS.append(dict(id=p, k0=round(acc, 4), k1=round(acc + d, 4), mode=mode(p))); acc += d
    PHOTOS[-1]["k1"] = k1
r = lambda a, z: [f"{i:03d}" for i in range(a, z + 1)]
section(["013", "014", "015", "016", "017", "000", "001", "002", "003", "004"], 16, 24)
section(r(5, 12) + r(18, 52), 64, 129)
section(r(93, 100), 129, 161, 1.0); PHOTOS[-1]["freeze_at"] = 159                 # last close-up holds through the stop
section(r(53, 92), 161, 197)
PHOTOS += [dict(id="N3", k0=197, k1=198, mode="cover", fx=.43), dict(id="N4", k0=198, k1=199, mode="cover", fx=.43),
           dict(id="N2", k0=199, k1=201, mode="full"), dict(id="101", k0=201, k1=203, mode="card"), dict(id="N1", k0=207, k1=211, mode="card", low=True)]
PHOTOS.sort(key=lambda p: p["k0"])
ids = [p["id"] for p in PHOTOS]
assert len(ids) == len(set(ids)), "a photo appears twice"
WALL_IDS = sorted(set(ids))
END_BG = "076"
