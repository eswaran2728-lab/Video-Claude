#!/bin/bash
# v03 = approved v02 + the creator's Masters Intro v02 (15 s, its own sound) at the end. Usage: ./append_v03.sh IN_V02.mp4 OUT.mp4
# Both are 1080x1920 30 fps; one re-encode (x264 CRF 16) through the concat filter, short audio fades at the join, then -14 LUFS master.
set -e; cd "$(dirname "$0")"; IN=$1; OUT=$2; A=src/append/masters_intro_v02.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
ffmpeg -nostdin -v error -y -i "$IN" -i "$A" -filter_complex \
 "[0:v]fps=30,format=yuv420p,setsar=1[v0];[1:v]fps=30,format=yuv420p,setsar=1[v1];[0:a]aresample=48000,afade=t=out:st=$(python3 -c "print(round($D-0.03,3))"):d=0.03[a0];[1:a]aresample=48000,afade=t=in:d=0.02[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][ac];[ac]alimiter=limit=0.7:attack=3:release=60:level=false[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -c:a pcm_s24le renders/v03_joined.mkv
./master_final.sh renders/v03_joined.mkv "$OUT" >/dev/null && rm renders/v03_joined.mkv && echo "$OUT"
