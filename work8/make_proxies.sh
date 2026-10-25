#!/bin/bash
# Stream each Drive original (720x1280 HEVC, SDR) into a 1080x1920 30fps CFR H.264 proxy; originals stay on Drive.
cd "$(dirname "$0")"
while read n id; do
  [ -f proxy/$n.mp4 ] && continue
  U="https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
  ffmpeg -nostdin -v error -y -i "$U" -map 0:v:0 -map 0:a:0 -vf "fps=30,scale=1080:1920:flags=lanczos,format=yuv420p" -c:v libx264 -crf 16 -preset medium -g 15 -c:a aac -b:a 192k -ac 2 -ar 48000 proxy/$n.tmp.mp4 && mv proxy/$n.tmp.mp4 proxy/$n.mp4
  echo "$n done $(date +%T)"
done <<LIST
a336 1scEBmWGo8Yj5X8SKWjVfz6TXq4Wt2HR3
d67f 1XrTNxduluzuq7og1NnwHJG4NzB-6NssW
e5dd 1OfRYiitkubC3QnEaw-ZNj2Coha-2_6xj
b5ae 1BkKJi95muqw1Er2ko7KqlegFcZ2lSUOI
LIST
echo ALL_DONE
