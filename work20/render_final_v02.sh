#!/bin/bash
# FINAL high-quality 1920x1080 30 fps renders of the approved v02 projects -> FINAL/<export name>.mp4 (+ matching .srt)
cd "$(dirname "$0")"; mkdir -p FINAL
for v in ${@:-v1_foca v2_notoc v3_aor v4_search}; do
  name=$(python3 -c "import scripts20;print(scripts20.VIDEOS['$v']['export'].replace('.mp4',''))")
  rm -rf /tmp/hyperframes-extract-cache-0/hfcache-v8-* $v/v02/renders/work-* 2>/dev/null
  (cd $v/v02/edit && npx --yes hyperframes@0.8.193 render --quality high --fps 30 --sdr --workers 3 -o ../renders/high_v02.mp4 > ../render_final.log 2>&1) || { echo "FAIL $v"; continue; }
  ./master_final.sh $v/v02/renders/high_v02.mp4 FINAL/$name.mp4 >/dev/null && rm -f $v/v02/renders/high_v02.mp4
  cp $v/v02/$name.srt FINAL/$name.srt
  F=FINAL/$name.mp4
  echo "$v $(ffprobe -v error -count_frames -show_entries stream=width,height,r_frame_rate,nb_read_frames:format=duration -of csv=p=0 $F | tr '\n' ' ') $(ffmpeg -nostdin -hide_banner -i $F -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I:|Peak:)' | tr -s ' ' | tr '\n' ' ') errors:$(ffmpeg -nostdin -v error -i $F -f null - 2>&1 | wc -l) size:$(du -h $F | cut -f1)"
done
echo DONE
