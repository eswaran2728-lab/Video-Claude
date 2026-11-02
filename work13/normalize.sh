#!/bin/bash
# WhatsApp exports -> 30 fps CFR working copies (rotation applied, yuv420p, H.264 crf 23, mono 48 kHz AAC) + 1 frame / 2 s sheets.
cd "$(dirname "$0")"
for f in src/wa/v_*.mp4; do
  n=$(basename "$f" .mp4); o="src/norm/$n.mp4"
  [ -f "$o" ] || ffmpeg -nostdin -v error -y -i "$f" -vf "fps=30,format=yuv420p" -c:v libx264 -crf 23 -preset fast -g 15 -c:a aac -b:a 128k -ac 1 -ar 48000 "$o"
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$o")
  ffmpeg -nostdin -v error -y -i "$o" -vf "fps=1/2,scale=-2:200,drawtext=text='$n %{pts\:flt}':x=3:y=3:fontsize=12:fontcolor=yellow:box=1:boxcolor=black,tile=12x3" -frames:v 1 "sheets/wa/$n.jpg"
  echo "$n $d"
done
