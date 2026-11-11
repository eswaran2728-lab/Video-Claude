# Read the creator's deck (src/*.pptx): per slide, the screenshot it shows (copied to edit/assets/deck/), the red highlight boxes
# drawn over it (converted to screenshot pixel coordinates), and its text blocks in reading order. -> slides.json
import re, json, zipfile, shutil, sys
from PIL import Image
PPTX = "src/High-Lift_Escort_eForm_Staff_Guide_AA_SEC_F_042.pptx"; z = zipfile.ZipFile(PPTX); out = []
RED = "E4002B"
for n in range(1, 41):
    try: s = z.read(f"ppt/slides/slide{n}.xml").decode()
    except KeyError: continue
    rels = dict(re.findall(r'Id="(\w+)"[^>]*Target="\.\./media/([^"]+)"', z.read(f"ppt/slides/_rels/slide{n}.xml.rels").decode()))
    pics, boxes, texts = [], [], []
    for m in re.finditer(r'<p:(pic|sp|cxnSp)>.*?</p:\1>', s, re.S):
        blk, kind = m.group(0), m.group(1)
        g = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"/>', blk)
        if not g: continue
        x, y, w, h = map(int, g.groups())
        if kind == "pic":
            e = re.search(r'r:embed="(\w+)"', blk); src = rels.get(e.group(1)) if e else None
            if src: pics.append(dict(src=src, x=x, y=y, w=w, h=h))
            continue
        geom = (re.search(r'prstGeom prst="(\w+)"', blk) or [None, ""])[1]
        ln = re.search(r'<a:ln[^>]*>(.*?)</a:ln>', blk, re.S)
        txt = " ".join(t for t in re.findall(r'<a:t>([^<]*)</a:t>', blk) if t.strip()).strip()
        if ln and RED in ln.group(1) and not txt and geom in ("roundRect", "rect", "ellipse"): boxes.append(dict(x=x, y=y, w=w, h=h, round=geom == "ellipse"))
        elif txt:
            sz = re.findall(r'sz="(\d+)"', blk); texts.append(dict(t=txt, x=x, y=y, size=int(sz[0]) / 100 if sz else 0))
    shot = None
    if pics:
        p = max(pics, key=lambda q: q["w"] * q["h"]); im = Image.open(z.open(f"ppt/media/{p['src']}")); W, H = im.size
        with z.open(f"ppt/media/{p['src']}") as f, open(f"edit/assets/deck/{p['src']}", "wb") as o: shutil.copyfileobj(f, o)
        hb = [dict(x=round((b["x"] - p["x"]) / p["w"] * W), y=round((b["y"] - p["y"]) / p["h"] * H), w=round(b["w"] / p["w"] * W), h=round(b["h"] / p["h"] * H), round=b["round"]) for b in boxes]
        shot = dict(src=p["src"], size=[W, H], boxes=hb)
    texts.sort(key=lambda q: (q["y"], q["x"]))
    out.append(dict(n=n, shot=shot, texts=[dict(t=q["t"], size=q["size"]) for q in texts]))
    print(n, shot and shot["src"], shot and shot["boxes"], [q["t"][:30] for q in texts][:6])
json.dump(out, open("slides.json", "w"), indent=1, ensure_ascii=False)
