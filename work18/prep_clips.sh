#!/bin/bash
# Clips for the promo (originals untouched): sharp foreground (card) + blurred, darkened cover background, 30 fps, no audio
# (sound is in the mix). Original scene: 0-17.4 s (the TikTok logo end card after 17.4 s is cut). Recreation: full 32.2 s.
cd "$(dirname "$0")"
V="-c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -an -r 30"
ffmpeg -nostdin -v error -y -t 17.4 -i src/original_scene_2.44.44PM.mp4 -vf "scale=980:-2:flags=lanczos,unsharp=5:5:0.5" $V edit/assets/v/orig_fg.mp4
ffmpeg -nostdin -v error -y -t 17.4 -i src/original_scene_2.44.44PM.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.18:saturation=0.8" $V edit/assets/v/orig_bg.mp4
ffmpeg -nostdin -v error -y -i src/recreated_3.14.20PM.mp4 -vf "scale=900:-2:flags=lanczos,unsharp=5:5:0.5" $V edit/assets/v/rec_fg.mp4
ffmpeg -nostdin -v error -y -i src/recreated_3.14.20PM.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.18:saturation=0.8" $V edit/assets/v/rec_bg.mp4
for f in edit/assets/v/*.mp4; do echo "$f $(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=width,height,nb_read_frames -of csv=p=0 $f)"; done
