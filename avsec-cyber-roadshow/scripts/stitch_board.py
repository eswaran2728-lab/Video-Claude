"""Join leaderboard screenshots into one tall board image for the video.

  python3 scripts/stitch_board.py

Reads `leaderboardScreenshots` from data/leaderboard.js (top of the board
first), finds the rows in each screenshot, keeps the header from the first
one, drops rows repeated across screenshots, and writes
assets/leaderboard/board.png. A row cut off at the bottom of a screenshot
is completed from the row above it (the rows are identical boxes), so
the board reads as one seamless list. Needs Pillow.
"""

import re
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

root = Path(__file__).resolve().parent.parent
data = (root / "data/leaderboard.js").read_text()
block = re.search(r"leaderboardScreenshots:\s*\[(.*?)\]", data, re.S)
files = re.findall(r'"([^"]+)"', block.group(1)) if block else []
if not files:
    sys.exit("No leaderboardScreenshots listed in data/leaderboard.js")

MARGIN = 30  # panel colour kept either side of the rows


def is_row(c):
    return sum(c[:3]) > 80  # rows are lighter than the panel background


def runs(vals, minlen):
    out, s = [], None
    for i, v in enumerate(vals):
        if v and s is None:
            s = i
        if not v and s is not None:
            if i - s >= minlen:
                out.append((s, i))
            s = None
    if s is not None and len(vals) - s >= minlen:
        out.append((s, len(vals)))
    return out


def find_rows(im):
    w, h = im.size
    px = im.load()
    probe_x = 120
    ys = runs([is_row(px[probe_x, y]) for y in range(h)], 20)
    full = [r for r in ys if r[0] > 0 and r[1] < h]
    ref = max(full, key=lambda r: r[1] - r[0])
    ym = (ref[0] + ref[1]) // 2
    xs = runs([is_row(px[x, ym]) for x in range(w)], 50)
    x0, x1 = xs[0][0], xs[-1][1]
    return ys, x0, x1, ref[1] - ref[0]


def signature(img):
    return img.convert("L")


def same(a, b):
    # Same row seen in two screenshots: almost no pixel differs strongly.
    # (Different rows differ in thousands of text pixels.)
    if a.size != b.size:
        w, h = min(a.width, b.width), min(a.height, b.height)
        a, b = a.crop((0, 0, w, h)), b.crop((0, 0, w, h))
    diff = ImageChops.difference(a, b).point(lambda v: 255 if v > 60 else 0)
    return ImageStat.Stat(diff).mean[0] / 255 < 0.004


pieces = []          # (image, row_left_x)
seen = []            # (signature, piece index, repaired?) of rows already placed
panel = None
row_h = gap = None
for n, f in enumerate(files):
    first_new = len(seen)  # rows before this index came from earlier screenshots
    im = Image.open(root / f).convert("RGB")
    w, h = im.size
    ys, x0, x1, rh = find_rows(im)
    panel = panel or im.getpixel((max(0, x0 - 3), ys[0][0] + rh // 2))
    row_h = row_h or rh
    full_rows = [r for r in ys if r[1] - r[0] >= rh - 2 and r[0] > 0]
    if gap is None and len(full_rows) > 1:
        gap = full_rows[1][0] - full_rows[0][1]
    left = max(0, x0 - MARGIN)
    right = min(w, x1 + MARGIN)
    if n == 0:
        row_w = x1 - x0
        # Header: everything above the first row.
        pieces.append((im.crop((left, 0, right, ys[0][0])), x0 - left))
    for i, (a, b) in enumerate(ys):
        if a == 0:
            continue  # cut off at the top: the previous screenshot has it
        repaired = False
        if b - a >= rh - 2:
            row = im.crop((left, a, right, b))
        elif b == h and b - a >= 0.6 * rh and i > 0:
            # Cut off at the bottom: complete it with the bottom of the row above.
            pa, pb = ys[i - 1]
            missing = rh - (b - a)
            row = Image.new("RGB", (right - left, rh))
            row.paste(im.crop((left, a, right, b)), (0, 0))
            row.paste(im.crop((left, pb - missing, right, pb)), (0, b - a))
            repaired = True
        else:
            continue
        # Compare only the row box itself (aligned on its left edge), top 60%.
        sig = signature(row.crop((x0 - left, 0, x0 - left + (x1 - x0), int(rh * 0.6))))
        match = next((k for k, (s, _, _) in enumerate(seen) if k >= len(seen) - 6 and k < first_new and same(sig, s)), None)
        if match is not None:
            s, idx, was_repaired = seen[match]
            if was_repaired and not repaired:
                # Prefer the complete copy over the patched one (no edge artefacts).
                pieces[idx] = (row, x0 - left)
                seen[match] = (s, idx, False)
            continue
        seen.append((sig, len(pieces), repaired))
        pieces.append((row, x0 - left))

gap = gap or 12
W = max(p.width - off for p, off in pieces) + MARGIN
H = pieces[0][0].height + sum(p.height + gap for p, _ in pieces[1:]) + MARGIN
board = Image.new("RGB", (W, H), panel)
y = 0
row_tops = []
for i, (p, off) in enumerate(pieces):
    board.paste(p, (MARGIN - off, y))
    if i > 0:
        row_tops.append(y)
    y += p.height + (gap if i > 0 else 0)
out = root / "assets/leaderboard/board.png"
board.save(out)
# Geometry for the video, so it can frame and scroll to exact rows.
(root / "assets/leaderboard/board.js").write_text(
    "// Generated by scripts/stitch_board.py. Do not edit.\n"
    f"window.AVSEC_BOARD = {{ width: {W}, height: {H}, rowHeight: {row_h}, rowLeft: {MARGIN}, "
    f"rowRight: {MARGIN + row_w}, rowTops: {row_tops} }};\n")
print(f"wrote {out.relative_to(root)}  {W}x{H}  rows={len(row_tops)}  rowH={row_h} gap={gap}")
