#!/bin/bash
# Full-file downloads of the creator's Drive media (one plain request per file). Usage: ./download.sh  (reads dl_list.tsv)
cd "$(dirname "$0")/src/drive"
while IFS=$'\t' read -r id name mime size rest; do
  [ -f "$name" ] && [ "$(stat -c %s "$name")" = "$size" ] && continue
  for try in 1 2 3; do
    curl -sS -L --max-time 900 -o "$name.part" "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t" && \
      [ "$(stat -c %s "$name.part")" = "$size" ] && mv "$name.part" "$name" && echo "ok $name" && break
    echo "retry $try $name ($(stat -c %s "$name.part" 2>/dev/null))"; sleep $((try*5))
  done
done < ../../dl_list.tsv
echo DONE
