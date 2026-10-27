#!/bin/bash
# Stream each Drive ProRes 4K HLG original into a full-res SDR master (3840x2160, H.264 CRF 14, hable tonemap) plus
# the original PCM stereo audio; originals stay on Drive (IMG_6421 is 2.2 GB, disk is tight).
cd "$(dirname "$0")"
TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
while read n id; do
  [ -f proxy/$n.mp4 ] && continue
  U="https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
  ffmpeg -nostdin -v error -y -i "$U" -map 0:v:0 -map 0:a:0 -vf "$TM" -c:v libx264 -crf 14 -preset medium -g 15 -c:a pcm_s16le -ar 48000 proxy/$n.tmp.mov \
    && mv proxy/$n.tmp.mov proxy/$n.mov
  echo "$n done $(date +%T)"
done <<LIST
IMG_6425 1GlqzGUo5zmXoTnWw9-NbSJ_wRWtcaucJ
IMG_6421 1L4FiBpeUpBeo8TIZ8S8pAdjjCZMLZzOH
LIST
echo ALL_DONE
