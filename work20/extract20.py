# Each Partner Briefing deck -> shapes.json: every shape on every slide in 1920x1080 slide pixels (EMU * 1920/12192000):
# pictures (with media name), red-outlined highlight boxes, coloured role badges/panels, arrows and text. Pictures copied to
# edit/assets/media/ (the real app screenshots / form scans embedded in the slides).
import re, json, zipfile, shutil, sys, os
v = sys.argv[1]; z = zipfile.ZipFile(f"{v}/src/deck.pptx"); K = 1920 / 12192000; out = []
os.makedirs(f"{v}/edit/assets/media", exist_ok=True)
names = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)], key=lambda n: int(re.findall(r"\d+", n)[0]))
for nm in names:
    n = int(re.findall(r"\d+", nm)[0]); s = z.read(nm).decode()
    rels = dict(re.findall(r'Id="(\w+)"[^>]*Target="\.\./media/([^"]+)"', z.read(f"ppt/slides/_rels/slide{n}.xml.rels").decode()))
    shapes = []
    for m in re.finditer(r'<p:(pic|sp|cxnSp)>.*?</p:\1>', s, re.S):
        blk, kind = m.group(0), m.group(1)
        g = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"/>', blk)
        if not g: continue
        x, y, w, h = [round(int(q) * K, 1) for q in g.groups()]
        d = dict(kind=kind, x=x, y=y, w=w, h=h)
        if kind == "pic":
            e = re.search(r'r:embed="(\w+)"', blk)
            if e and e.group(1) in rels:
                d["src"] = rels[e.group(1)]
                with z.open(f"ppt/media/{d['src']}") as f, open(f"{v}/edit/assets/media/{d['src']}", "wb") as o: shutil.copyfileobj(f, o)
        else:
            d["geom"] = (re.search(r'prstGeom prst="(\w+)"', blk) or [None, ""])[1]
            ln = re.search(r'<a:ln[^>]*>(.*?)</a:ln>', blk, re.S); d["ln"] = (re.findall(r'srgbClr val="(\w+)"', ln.group(1)) or [""])[0] if ln else ""
            f = re.search(r'<p:spPr>(.*?)</p:spPr>', blk, re.S); d["fill"] = (re.findall(r'<a:solidFill><a:srgbClr val="(\w+)"', f.group(1)) or [""])[0] if f else ""
            d["t"] = " ".join(t for t in re.findall(r'<a:t>([^<]*)</a:t>', blk) if t.strip()).strip()
        shapes.append(d)
    out.append(dict(n=n, shapes=shapes))
json.dump(out, open(f"{v}/shapes.json", "w"), indent=1, ensure_ascii=False)
print(v, len(out), "slides")
