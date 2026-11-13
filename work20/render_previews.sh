#!/bin/bash
# draft-quality 1920x1080 previews for review (final high-quality MP4s only after approval)
cd "$(dirname "$0")"
for v in v1_foca v2_notoc v3_aor v4_search; do
  name=$(python3 -c "import scripts20;print(scripts20.VIDEOS['$v']['export'].replace('.mp4',''))")
  rm -rf /tmp/hyperframes-extract-cache-0/hfcache-v8-* $v/renders/work-* 2>/dev/null
  (cd $v/edit && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 --sdr --workers 3 -o ../renders/draft_v01.mp4 > ../render_v01.log 2>&1) || { echo "FAIL $v"; continue; }
  ./master_final.sh $v/renders/draft_v01.mp4 $v/PREVIEW_${name}_v01.mp4 >/dev/null
  F=$v/PREVIEW_${name}_v01.mp4
  echo "$v $(ffprobe -v error -count_frames -show_entries stream=width,height,r_frame_rate,nb_read_frames:format=duration -of csv=p=0 $F | tr '\n' ' ') $(ffmpeg -nostdin -hide_banner -i $F -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I:|Peak:)' | tr -s ' ' | tr '\n' ' ') errors:$(ffmpeg -nostdin -v error -i $F -f null - 2>&1 | wc -l)"
done
echo DONE
