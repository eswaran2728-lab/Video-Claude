#!/bin/bash
# Remove the repeated line (segment 3: 12.6667s-18.8333s, frames 380-564) from the full composite
set -e
cd "$(dirname "$0")"
ffmpeg -v error -y -i kali-edit/comp_full.mp4 -filter_complex \
 "[0:v]select='not(between(n\,380\,564))',setpts=N/30/TB[v];[0:a]aselect='not(between(t\,12.6667\,18.8333))',asetpts=N/SR/TB[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 15 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k kali-edit/comp.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 kali-edit/comp.mp4
