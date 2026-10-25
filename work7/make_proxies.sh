#!/bin/bash
# Stream each Drive original (ProRes 4K HLG / HEVC) straight into a 1080x1920 SDR H.264 proxy; originals stay on Drive.
cd "$(dirname "$0")"
TM="zscale=w=1080:h=1920:filter=lanczos,zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
SDR="scale=1080:1920:flags=lanczos,format=yuv420p"
while read n id kind; do
  [ -f proxy/$n.mp4 ] && continue
  U="https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
  VF=$TM; [ "$kind" = sdr ] && VF=$SDR
  ffmpeg -nostdin -v error -y -i "$U" -map 0:v:0 -map 0:a:0 -vf "$VF" -c:v libx264 -crf 16 -preset medium -g 15 -c:a aac -b:a 192k -ac 2 proxy/$n.tmp.mp4 && mv proxy/$n.tmp.mp4 proxy/$n.mp4
  echo "$n done $(date +%T)"
done <<LIST
IMG_6357 1WzgwP8FhQNoqhEHmNhGUZfCampzZxxes sdr
3437BABC 1KGN5uAmSuFXBx9MDx2XWpW9M414Adoco sdr
IMG_6351 1zqaIYt8CRPyaW9pe7KJA1EMTO_CPmREr hlg
IMG_6359 1XDfd7T7xoiuwUOVmiAK2BZN19rKVqM4u hlg
IMG_6354 1mPK817byaXn2D5rETExqOaQ83FP3hU7q hlg
IMG_6356 1uPe4LjkbLPuJkALtSAo1LS5hD_lXyrFI hlg
IMG_6353 18pxtUD7pX5xySwuGbTU68FELB5iMicEn hlg
IMG_6352 1A3RPxn4jQj4VBk78S_0GLDumwiLf_2_b hlg
IMG_6358 1k8H2nZ8wK8x9z4AMxpqlzMkPmU3seEfL hlg
LIST
echo ALL_DONE
