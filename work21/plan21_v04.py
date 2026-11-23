# work21 v04 = approved v03 (v02 reel + Masters Intro) with the 4 photos added to Drive on 23.11.2026:
#   N1 designed "Hari Sukan Negara" poster with the whole medal group -> the payoff, held under TAHNIAH (beats 207-211)
#   N3, N4 the presenter handing a gift hamper on stage; N2 two coaches -> just before the coaches' group photo (beats 197-201)
#   all four also join the photo wall. Music, timing grid and every other section are unchanged from v02.
import os
from PIL import Image, ImageOps
from plan21_v02 import BPM, B, MUSIC_IN, b, TOTAL, MUSIC, FADE, SLOWMO, WALL, K_END, GROUP, BURST, EVENT_SMALL, EVENT_SUB, EVENT_DATE, EVENT_VENUE, BRAND1, BRAND2
import plan21_v02 as V2
OUT = "edit_v04"
SRC = {f"N{i}": f"src/new/N{i}.jpg" for i in range(1, 5)}
SIZE = dict(V2.SIZE); SIZE.update({k: ImageOps.exif_transpose(Image.open(v)).size for k, v in SRC.items()})
SEGS = [dict(s) for s in V2.SEGS]
for s in SEGS:
    if s["id"] == "g1": s["k1"] = 207                               # medal-group clip 8 -> 4 beats
PHOTOS = [dict(p) for p in V2.PHOTOS if not (161 <= p["k0"] < 201)]
def section(ids, k0, k1, group_weight=1.5):
    w = [0.5 if p in BURST else (group_weight if p in GROUP else 1.0) for p in ids]; acc = k0
    for p, x in zip(ids, w):
        d = x * (k1 - k0) / sum(w); PHOTOS.append(dict(id=p, k0=round(acc, 4), k1=round(acc + d, 4), mode=V2.mode(p))); acc += d
    PHOTOS[-1]["k1"] = k1
section([f"{i:03d}" for i in range(53, 93)], 161, 197)             # ON THE STAGE, 4 beats tighter
PHOTOS += [dict(id="N3", k0=197, k1=198, mode="cover", fx=.43), dict(id="N4", k0=198, k1=199, mode="cover", fx=.43),
           dict(id="N2", k0=199, k1=201, mode="full"), dict(id="N1", k0=207, k1=211, mode="card", low=True)]
PHOTOS.sort(key=lambda p: p["k0"])
assert {p["id"] for p in PHOTOS} == set(SIZE), sorted(set(SIZE) - {p["id"] for p in PHOTOS})
