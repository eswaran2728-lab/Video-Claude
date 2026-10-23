#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 build_talent.py
python3 bake_broll.py '[
{"src":"src/v118.mp4","start":1.55,"dur":1.75,"out":"edit/assets/b_hook_yest.webm","crop":[290,917,0,720],"size":[960,836],"radius":44,"show_at_zero":true,"tout":0.55,"seed":11},
{"src":"src/v117.mp4","start":4.9,"dur":2.45,"out":"edit/assets/b_hook_real.webm","tin":0.55,"tout":0.5,"seed":5},
{"src":"src/v118.mp4","start":1.6,"dur":2.4,"out":"edit/assets/b1_yest.webm","crop":[290,917,0,720],"size":[960,836],"radius":44,"tin":0.5,"tout":0.45,"seed":21},
{"src":"src/v117.mp4","start":4.0,"dur":6.75,"out":"edit/assets/b2_real.webm","tin":0.6,"tout":0.55,"seed":7},
{"src":"src/v118.mp4","start":1.4,"dur":4.85,"out":"edit/assets/b3_yest.webm","crop":[290,917,0,720],"size":[960,836],"radius":44,"tin":0.5,"tout":0.5,"seed":31}
]'
python3 build_index.py
cd edit && npx hyperframes check 2>&1 | grep -E "✗|Check"
echo HQ_ASSETS_OK
