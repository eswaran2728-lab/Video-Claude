#!/bin/bash
# Transcribe every speech chunk separately (Tamil, whisper large-v3) to avoid repetition loops.
cd "$(dirname "$0")/.."
python3 -c "
import json
d=json.load(open('analysis/speech_segments.json'))
for c,v in d.items():
    for i,(a,b) in enumerate(v['chunks']): print(c,i,a,b)" | while read c i a b; do
  d=analysis/asr/${c}_$i; mkdir -p $d; [ -f $d/transcript.json ] && continue
  ffmpeg -y -v error -ss $a -to $b -i analysis/${c}_c.wav $d/a.wav
  (cd $d && npx hyperframes transcribe a.wav --engine whisper --model large-v3 --language ta --json </dev/null >/dev/null 2>&1)
  echo "$c $i $a $b done"
done
