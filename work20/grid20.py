# slide renders (3840x2160) -> grid crops in 1920-slide pixel coordinates, for authoring zoom / ring targets
import sys
from PIL import Image, ImageDraw
v, out = sys.argv[1], sys.argv[2]; specs = [tuple(map(int, a.split(","))) for a in sys.argv[3:]]   # n,x0,y0,x1,y1 (1920 coords)
tiles = []
for n, x0, y0, x1, y1 in specs:
    im = Image.open(f"{v}/slides/s-{n:02d}.jpg").convert("RGB").crop((x0 * 2, y0 * 2, x1 * 2, y1 * 2)); d = ImageDraw.Draw(im)
    for x in range((x0 // 25 + 1) * 25, x1, 25):
        c = (255, 0, 0) if x % 100 == 0 else (255, 170, 170); d.line([((x - x0) * 2, 0), ((x - x0) * 2, im.height)], fill=c, width=1)
        if x % 100 == 0: d.text(((x - x0) * 2 + 3, 3), str(x), fill=(255, 0, 0))
    for y in range((y0 // 25 + 1) * 25, y1, 25):
        c = (0, 0, 255) if y % 100 == 0 else (170, 170, 255); d.line([(0, (y - y0) * 2), (im.width, (y - y0) * 2)], fill=c, width=1)
        if y % 100 == 0: d.text((3, (y - y0) * 2 + 3), str(y), fill=(0, 0, 255))
    d.text((8, im.height - 20), f"slide {n}", fill=(255, 0, 255)); tiles.append(im)
H = max(t.height for t in tiles); W = sum(t.width for t in tiles) + 10 * len(tiles)
sheet = Image.new("RGB", (W, H), (60, 60, 60)); x = 0
for t in tiles: sheet.paste(t, (x, 0)); x += t.width + 10
sheet.save(out)
