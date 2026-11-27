# OCR every listed screenshot (word boxes, native 585x1266 pixel coords) -> ocr.json. Used only to place rings/zooms on real UI text.
import json, subprocess, sys, os, csv, io
S = "src/unz/revlog screenshot"; m = json.load(open(f"{S}/manifest.json")); out = {}
for e in m:
    f = e.get("file")
    if not f: continue
    r = subprocess.run(["tesseract", f"{S}/{f}", "-", "--psm", "11", "tsv"], capture_output=True, text=True).stdout
    words = []
    for row in csv.DictReader(io.StringIO(r), delimiter="\t"):
        if row.get("text", "").strip() and float(row["conf"]) > 40:
            words.append(dict(t=row["text"], x=int(row["left"]), y=int(row["top"]), w=int(row["width"]), h=int(row["height"])))
    out[f] = words
json.dump(out, open("ocr.json", "w"))
print(len(out), sum(len(v) for v in out.values()))
