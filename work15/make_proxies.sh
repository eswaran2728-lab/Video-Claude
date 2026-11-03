#!/bin/bash
# iPhone HLG HEVC (rotation honoured) -> SDR BT.709 30 fps H.264 proxies, long side 1920, audio AAC 48k. Originals untouched.
cd "$(dirname "$0")"
TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv"
for f in src/drive/*.MOV src/drive/*.MP4; do
  b=$(basename "${f%.*}"); o=proxy/$b.mp4; [ -f "$o" ] && continue
  tr=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$f")
  if [ "$tr" = "arib-std-b67" ]; then VF="$TM,"; else VF=""; fi
  ffmpeg -nostdin -v error -y -i "$f" -vf "${VF}scale='if(gt(iw,ih),1920,-2)':'if(gt(iw,ih),-2,1920)':flags=lanczos,fps=30,format=yuv420p" \
    -c:v libx264 -crf 17 -preset medium -g 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$o" && echo "ok $o"
done
