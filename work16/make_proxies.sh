#!/bin/bash
# HLG ProRes (rotation honoured) → SDR BT.709 30 fps proxies; 4K tone-mapped copies of the M ranges the plate uses. Originals untouched.
cd "$(dirname "$0")"; mkdir -p proxy inter
TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv"
ffmpeg -nostdin -v error -y -i src/drive/IMG_6792.MOV -map 0:v:0 -map 0:a:0 -vf "$TM,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" \
  -c:v libx264 -crf 16 -preset medium -g 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart proxy/IMG_6792.mp4
ffmpeg -nostdin -v error -y -i src/drive/fa799ce5e58a49c29107dcd042ded275.mp4 -vf "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" \
  -c:v libx264 -crf 16 -preset medium -g 30 -c:a aac -b:a 192k -ar 48000 -ac 1 -movflags +faststart proxy/frame_lights.mp4
ffmpeg -nostdin -v error -y -ss 5.4 -t 19.4 -i src/drive/IMG_6792.MOV -map 0:v:0 -vf "$TM,fps=30,format=yuv420p" -c:v libx264 -crf 12 -preset fast -g 15 -an inter/M_05_25_4k.mp4
ffmpeg -nostdin -v error -y -ss 39.8 -t 3.0 -i src/drive/IMG_6792.MOV -map 0:v:0 -vf "$TM,fps=30,format=yuv420p" -c:v libx264 -crf 12 -preset fast -g 15 -an inter/M_40_43_4k.mp4
mkdir -p analysis; for k in IMG_6792:main frame_lights:lights; do ffmpeg -nostdin -v error -y -i proxy/${k%%:*}.mp4 -vn -ac 1 -ar 16000 analysis/src_${k##*:}16k.wav; done
