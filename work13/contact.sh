#!/bin/bash
# One 6-frame strip per Drive video (seeks over HTTP, nothing downloaded). HLG clips tone-mapped to SDR for viewing.
cd "$(dirname "$0")"
TMV="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
while IFS=$'\t' read id name; do
  case "$name" in *.mov|*.MOV) ;; *) continue;; esac
  [ -f "sheets/clips/${name%.*}.jpg" ] && continue
  u="https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$u"); [ -z "$d" ] && continue
  hlg=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$u")
  F="scale=-2:320"; [ "$hlg" = "arib-std-b67" ] && F="scale=-2:320,$TMV"
  rm -f sheets/clips/_f*.jpg
  for k in 0 1 2 3 4 5; do t=$(python3 -c "print(round($d*($k+0.5)/6,2))")
    ffmpeg -nostdin -v error -y -ss $t -i "$u" -frames:v 1 -vf "$F,drawtext=text='$name $t':x=4:y=4:fontsize=12:fontcolor=yellow:box=1:boxcolor=black" sheets/clips/_f$k.jpg
  done
  ffmpeg -nostdin -v error -y -i sheets/clips/_f%d.jpg -vf tile=6x1 -frames:v 1 "sheets/clips/${name%.*}.jpg" 2>/dev/null || ffmpeg -nostdin -v error -y -pattern_type glob -i 'sheets/clips/_f*.jpg' -vf tile=6x1 "sheets/clips/${name%.*}.jpg"
  echo "$name $d $hlg"
done < drive_files_v2.tsv
rm -f sheets/clips/_f*.jpg
