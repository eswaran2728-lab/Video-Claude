#!/bin/bash
# Final master: video stream copied as rendered; audio 2-pass loudnorm to -14 LUFS, true-peak ceiling -2 dBTP
# (leaves room for AAC overshoot so the encoded peak stays at or under about -1.5). Usage: ./master_final.sh IN OUT
set -e; IN=$1; OUT=$2
P=$(ffmpeg -nostdin -hide_banner -i "$IN" -af loudnorm=I=-14:TP=-2:LRA=9:print_format=json -f null - 2>&1 | python3 -c "import sys,re,json;j=json.loads(re.findall(r'\{[^{}]*\}',sys.stdin.read())[-1]);print(f\"measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}\")")
ffmpeg -nostdin -v error -y -i "$IN" -map 0:v:0 -map 0:a:0 -c:v copy -af "loudnorm=I=-14:TP=-2:LRA=9:$P:linear=true" -ar 48000 -c:a aac -b:a 256k -movflags +faststart "$OUT"
echo "$OUT"
