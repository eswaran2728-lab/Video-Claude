#!/bin/bash
set -e
cd "$(dirname "$0")"
K=motion-kinetic-type
i=0
while IFS='|' read -r txt dur; do
  python3 $K/render.py $K/template.html out/kt_$i.webm --alpha --w 1080 --h 420 --dur $dur --text "$txt" --set c1=f7c948 --set c2=ffffff --set c3=ffd25a
  i=$((i+1))
done <<'L'
THE ART OF SILAMBAM|1.85
PURE SPEED|1.7
RAW POWER|1.7
SHARP FOCUS|1.7
TOTAL DISCIPLINE|1.7
LIVING TRADITION|1.7
ONE TEAM|1.7
L
P=motion-particles
python3 $P/render.py $P/template.html out/particles.webm --alpha --w 1080 --h 810 --dur 4.8 --text "SILAMBAM" --set c1=f7c948 --set c2=fff1b8 --set c3=ff9a3c
echo RENDER_OK
