#!/bin/bash
# v04 = v03 master + the supplied "Silambam Masters" clip appended at the end (clip lowered 2 dB to match -16 LUFS).
cd "$(dirname "$0")/.."
ffmpeg -y -v error -i v03/renders/deepavali_silambam_v03_master.mp4 -i source/masters_outro.mp4 -filter_complex \
 "[0:v]fps=30,format=yuv420p,setsar=1[v0];[1:v]fps=30,scale=1080:1920,format=yuv420p,setsar=1,fade=t=in:d=0.3[v1];[0:a]aresample=48000[a0];[1:a]aresample=48000,volume=-2dB,afade=t=in:d=0.15[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 17 -maxrate 14M -bufsize 28M -profile:v high -c:a aac -b:a 256k -movflags +faststart v04/renders/Silambam_Deepavali_Selangor_2026_FINAL_with_masters.mp4
