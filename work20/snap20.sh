#!/bin/bash
# snapshot the middle of the given sentence numbers (+ the last frame) of one video: ./snap20.sh v2_notoc 0 2 4
v=$1; shift; cd "$(dirname "$0")"
AT=$(python3 - "$v" "$@" <<'PY'
import json, sys
d = json.load(open(f"{sys.argv[1]}/layout.json")); L = d["lines"]
ts = [round((L[int(i)]["t0"] + L[int(i)]["t1"]) / 2 + 0.6, 2) for i in sys.argv[2:]] + [round(d["total"] - 1.5, 2)]
print(",".join(map(str, ts)))
PY
)
rm -rf "$v/sheets/snap2"; (cd "$v/edit" && npx --yes hyperframes@0.8.193 snapshot -o ../sheets/snap2 --no-end --at "$AT" >/dev/null 2>&1); echo "$v $(ls $v/sheets/snap2 | grep -c png) frames"
