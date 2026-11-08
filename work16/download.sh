#!/bin/bash
# Full-file downloads of the creator's Drive media (folder 1r1MNaLtPCPtHEZbUQF0geENsWPKxnyts). Usage: ./download.sh
mkdir -p "$(dirname "$0")/src/drive"; cd "$(dirname "$0")/src/drive"
tail -n +2 ../../drive_files.tsv | while IFS=$'\t' read -r id name mime size; do
  [ -f "$name" ] && [ "$(stat -c %s "$name")" = "$size" ] && continue
  for try in 1 2 3; do
    curl -sS -L -C - --max-time 3600 -o "$name.part" "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t" && \
      [ "$(stat -c %s "$name.part")" = "$size" ] && mv "$name.part" "$name" && echo "ok $name" && break
    sleep $((try*5))
  done
done
