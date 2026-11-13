#!/bin/bash
# snapshot the middle of EVERY sentence (+ the last frame) of a v02 build: ./snapall20.sh v1_foca/v02
d=$1; cd "$(dirname "$0")"
AT=$(python3 - "$d" <<'PY'
import json, sys
x = json.load(open(f"{sys.argv[1]}/layout.json")); L = x["lines"]
print(",".join(str(round((l["t0"] + l["t1"]) / 2 + 0.5, 2)) for l in L) + "," + str(round(x["total"] - 1.2, 2)))
PY
)
rm -rf "$d/sheets/all"; mkdir -p "$d/sheets"; (cd "$d/edit" && npx --yes hyperframes@0.8.193 snapshot -o ../sheets/all --no-end --at "$AT" >/dev/null 2>&1)
python3 - "$d" <<'PY'
import sys, os
from PIL import Image
d = sys.argv[1]; fs = sorted(f for f in os.listdir(f"{d}/sheets/all") if f.endswith(".png"))
W, H, C = 640, 360, 4
for k in range(0, len(fs), 16):
    g = fs[k:k + 16]; sheet = Image.new("RGB", (W * C, H * ((len(g) + C - 1) // C)), "black")
    for j, f in enumerate(g): sheet.paste(Image.open(f"{d}/sheets/all/{f}").convert("RGB").resize((W, H)), ((j % C) * W, (j // C) * H))
    sheet.save(f"{d}/sheets/sheet_{k // 16 + 1}.jpg", quality=85)
print(d, len(fs), "frames")
PY
