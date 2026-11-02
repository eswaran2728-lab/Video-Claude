#!/bin/bash
# Low-res review copy: 2-pass loudnorm to -14 LUFS / -1.5 dBTP, 720x1280. Usage: ./master_preview.sh renders/draft_v01.mp4 PREVIEW_x.mp4
set -e; IN=$1; OUT=$2
J=$(ffmpeg -nostdin -hide_banner -i "$IN" -af loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json -f null - 2>&1 | python3 -c "import sys,re,json;t=sys.stdin.read();print(json.dumps(json.loads(re.findall(r'\{[^{}]*\}',t)[-1])))")
P=$(echo "$J" | python3 -c "import sys,json;j=json.load(sys.stdin);print(f\"measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}\")")
ffmpeg -nostdin -v error -y -i "$IN" -vf "scale=720:1280:flags=lanczos" -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.5:LRA=9:$P:linear=true" -ar 48000 -c:a aac -b:a 160k -movflags +faststart "$OUT"
echo "$OUT"
