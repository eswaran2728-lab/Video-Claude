#!/bin/bash
# Stream each Drive original into a small analysis proxy (360p, 30 fps CFR, H.264 crf 24, mono AAC); originals stay on Drive.
# HLG (iPhone HDR) clips are tone-mapped to BT.709 (Hable). Rotation metadata is honoured by ffmpeg autorotate.
# Retries: Drive throttles bursts of requests (returns an error page), so each file gets up to 5 tries.
cd "$(dirname "$0")"
TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv"
while IFS=$'\t' read id name; do
  case "$name" in *.mov|*.MOV) ;; *) continue;; esac
  out="proxy/${name%.*}.mp4"; [ -f "$out" ] && continue
  u="https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
  for try in 1 2 3 4 5; do
    hlg=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$u" 2>/dev/null)
    if [ -n "$hlg" ]; then
      VF="fps=30,scale='if(gt(iw,ih),640,-2)':'if(gt(iw,ih),-2,640)':flags=bicubic"
      [ "$hlg" = "arib-std-b67" ] && VF="$VF,$TM"
      if ffmpeg -nostdin -v error -y -i "$u" -map 0:v:0 -map 0:a:0? -vf "$VF,format=yuv420p" -c:v libx264 -crf 24 -preset veryfast -g 30 \
           -c:a aac -b:a 96k -ac 1 -ar 48000 "proxy/tmp_$name.mp4"; then mv "proxy/tmp_$name.mp4" "$out"; echo "$name ok try$try $(date +%T)"; break; fi
    fi
    rm -f "proxy/tmp_$name.mp4"; echo "$name retry $try"; sleep $((15*try))
  done
done < drive_files_v2.tsv
echo ALL_DONE
