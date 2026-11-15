#!/bin/bash
# AI-upscale every shot of a version's edit plan into per-shot proxies. Resumable: finished shots are skipped.
V=${1:-v03}; cd "$(dirname "$0")/../.."
python3 -c "
import json
for s in json.load(open('$V/edit-plan.json'))['shots']: print(s['id'], s['clip'], s['in'], round(s['dur']+0.2,2))" | while read id clip in dur; do
  out=$V/assets/video/$id.mp4
  [ -f "$out" ] && continue
  python3 analysis/sr/upscale.py source/$clip.mp4 $in $dur $V/assets/video/.tmp_$id.mp4 && mv $V/assets/video/.tmp_$id.mp4 $out
done; ls $V/assets/video | wc -l
