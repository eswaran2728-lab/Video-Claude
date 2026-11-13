# Creator's deck (src/FOCA_Checklist_Staff_Guide.pptx) -> slides.json: per slide the phone screenshot (tallest picture), the
# close-up picture (if any), the red highlight boxes (red-outlined roundRects without text) in screenshot pixels, the role badge,
# and the text blocks in reading order. Pictures are copied unchanged to edit/assets/deck/.
import re, json, zipfile, shutil
from PIL import Image
z = zipfile.ZipFile("src/FOCA_Checklist_Staff_Guide.pptx"); RED = "E31837"; out = []
ROLE_COL = {"0B57D0": "blue", "B8550D": "orange"}
for n in range(1, 31):
    s = z.read(f"ppt/slides/slide{n}.xml").decode()
    rels = dict(re.findall(r'Id="(\w+)"[^>]*Target="\.\./media/([^"]+)"', z.read(f"ppt/slides/_rels/slide{n}.xml.rels").decode()))
    pics, boxes, texts, role = [], [], [], None
    for m in re.finditer(r'<p:(pic|sp|cxnSp)>.*?</p:\1>', s, re.S):
        blk, kind = m.group(0), m.group(1)
        g = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"/>', blk)
        if not g: continue
        x, y, w, h = map(int, g.groups())
        if kind == "pic":
            e = re.search(r'r:embed="(\w+)"', blk)
            if e and e.group(1) in rels: pics.append(dict(src=rels[e.group(1)], x=x, y=y, w=w, h=h))
            continue
        geom = (re.search(r'prstGeom prst="(\w+)"', blk) or [None, ""])[1]
        ln = re.search(r'<a:ln[^>]*>(.*?)</a:ln>', blk, re.S); lnc = re.findall(r'srgbClr val="(\w+)"', ln.group(1)) if ln else []
        txt = " ".join(t for t in re.findall(r'<a:t>([^<]*)</a:t>', blk) if t.strip()).strip()
        if geom == "roundRect" and RED in lnc and not txt: boxes.append(dict(x=x, y=y, w=w, h=h))
        elif geom == "roundRect" and lnc and lnc[0] in ROLE_COL and not txt: role = dict(color=ROLE_COL[lnc[0]], y=y)
        elif txt:
            sz = re.findall(r'sz="(\d+)"', blk); texts.append(dict(t=txt, x=x, y=y, w=w, size=int(sz[0]) / 100 if sz else 0))
    texts.sort(key=lambda q: (q["y"], q["x"]))
    if role:
        rt = [q for q in texts if q["y"] == role["y"]]
        if rt: role["text"] = rt[0]["t"]; texts = [q for q in texts if q is not rt[0]]
    shot = close = None
    if pics:
        main = max(pics, key=lambda q: q["h"]); im = Image.open(z.open(f"ppt/media/{main['src']}")); W, H = im.size
        for p in pics:
            with z.open(f"ppt/media/{p['src']}") as f, open(f"edit/assets/deck/{p['src']}", "wb") as o: shutil.copyfileobj(f, o)
        hb = [dict(x=round((b["x"] - main["x"]) / main["w"] * W), y=round((b["y"] - main["y"]) / main["h"] * H), w=round(b["w"] / main["w"] * W),
                   h=round(b["h"] / main["h"] * H)) for b in boxes if main["x"] - 200000 < b["x"] < main["x"] + main["w"]]
        shot = dict(src=main["src"], size=[W, H], boxes=hb, slide_w=main["w"], slide_h=main["h"])
        others = [p for p in pics if p is not main]
        if others:
            c = others[0]; ci = Image.open(z.open(f"ppt/media/{c['src']}")); close = dict(src=c["src"], size=list(ci.size))
    out.append(dict(n=n, shot=shot, close=close, role=role, texts=[dict(t=q["t"], size=q["size"]) for q in texts]))
    print(n, shot and shot["src"], shot and shot["size"], shot and shot["boxes"], close and close["src"], role and role.get("text"), [q["t"][:28] for q in texts][:5])
json.dump(out, open("slides.json", "w"), indent=1, ensure_ascii=False)
