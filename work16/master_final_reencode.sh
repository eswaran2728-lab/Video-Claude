#!/bin/bash
# Final master for grainy (v03) renders: video re-encoded to a delivery size (x264 CRF 17, slow, film tune, capped
# 30 Mb/s), audio 2-pass loudnorm to -14 LUFS / -2 dBTP, AAC 256k. Usage: ./master_final_reencode.sh IN OUT
set -e; IN=$1; OUT=$2
P=$(ffmpeg -nostdin -hide_banner -i "$IN" -af loudnorm=I=-14:TP=-2:LRA=9:print_format=json -f null - 2>&1 | python3 -c "import sys,re,json;j=json.loads(re.findall(r'\{[^{}]*\}',sys.stdin.read())[-1]);print(f\"measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}\")")
ffmpeg -nostdin -v error -y -i "$IN" -map 0:v:0 -map 0:a:0 -c:v libx264 -preset slow -tune film -crf 17 -maxrate 30M -bufsize 60M \
  -pix_fmt yuv420p -profile:v high -g 60 -af "loudnorm=I=-14:TP=-2:LRA=9:$P:linear=true" -ar 48000 -c:a aac -b:a 256k -movflags +faststart "$OUT"
echo "$OUT"
