# work21 v06 = v05 with the performance section cut down ("cut down the loop video, it comes multiple times"):
# instead of 13 alternating cuts between the girl's and the boy's clips, each performer gets ONE continuous take:
#   girl  (IMG_1921 11.00 s -> 18.64 s real time, then 18.64 -> 20.28 s at half speed into her jumping spin)   beats 24-44
#   the four performance photos 106, 102, 103, 105 (one beat each)                                               beats 44-48
#   boy   (IMG_1918 5.40 s ->, continuing from his event-card shot, follow-crop)                                 beats 48-64
# Hook, event card, photos, music, beat grid, titles, header, payoff, wall and the appended Masters Intro are as v05.
import plan21_v05 as V5
from plan21_v05 import *            # noqa
OUT = "edit_v06"
SEGS = [s for s in V5.SEGS if not (24 <= s["k0"] < 64)]
SEGS += [dict(id="girl_rt", clip="IMG_1921", src=11.00, k0=24, k1=38),
         dict(id="girl_sm", clip="IMG_1921", src=round(11.00 + b(38) - b(24), 3), k0=38, k1=44, speed=.5),
         dict(id="boy", clip="IMG_1918", src=5.40, k0=48, k1=64, zoom=1.25)]
SEGS.sort(key=lambda s: s["k0"])
SLOWMO = (38, 44)
PHOTOS = [p for p in V5.PHOTOS if not (24 <= p["k0"] < 64)]
PHOTOS += [dict(id=i, k0=44 + n, k1=45 + n, mode=mode(i)) for n, i in enumerate(("106", "102", "103", "105"))]
PHOTOS.sort(key=lambda p: p["k0"])
for c in ("IMG_1921", "IMG_1918", "IMG_2025"):
    rs = sorted((s["src"], s["src"] + (b(s["k1"]) - b(s["k0"])) * s.get("speed", 1)) for s in SEGS if s["clip"] == c)
    assert all(a[1] <= z[0] + 1e-3 for a, z in zip(rs, rs[1:])), (c, rs)
    assert rs[-1][1] <= {"IMG_1921": 63.6, "IMG_1918": 26.2, "IMG_2025": 5.7}[c], (c, rs[-1])
