#!/bin/bash
# Low-res review copy: 720x1280, audio 2-pass loudnorm -14 LUFS / -2 dBTP, duration kept exactly as rendered.
set -e; IN=$1; OUT=$2; DUR=${3:-25.4}
P=$(ffmpeg -nostdin -hide_banner -i "$IN" -af loudnorm=I=-14:TP=-2:LRA=9:print_format=json -f null - 2>&1 | python3 -c "import sys,re,json;j=json.loads(re.findall(r'\{[^{}]*\}',sys.stdin.read())[-1]);print(f\"measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}\")")
ffmpeg -nostdin -v error -y -i "$IN" -vf "scale=720:1280:flags=lanczos" -c:v libx264 -crf 22 -preset medium -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-2:LRA=9:$P:linear=true" -ar 48000 -c:a aac -b:a 192k -t "$DUR" -movflags +faststart "$OUT"
echo "$OUT"
