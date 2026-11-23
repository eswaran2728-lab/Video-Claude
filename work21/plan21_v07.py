# work21 v07 = v06 with the girl's spin sped up to 1.5x ("speed up the spinning into 1.5") instead of 0.5x slow motion.
# The spin segment keeps its place (beats 38-44); at 1.5x it now covers IMG_1921 18.64 -> 23.55 s. No SLOW MOTION tag.
import plan21_v06 as V6
from plan21_v06 import *            # noqa
OUT = "edit_v07"
SEGS = [dict(s) for s in V6.SEGS]
for s in SEGS:
    if s["id"] == "girl_sm": s.update(id="girl_fast", speed=1.5)
SLOW_TAG = None
PERF2 = True
for c in ("IMG_1921",):
    rs = sorted((s["src"], s["src"] + (b(s["k1"]) - b(s["k0"])) * s.get("speed", 1)) for s in SEGS if s["clip"] == c)
    assert all(a[1] <= z[0] + 1e-3 for a, z in zip(rs, rs[1:])), rs
