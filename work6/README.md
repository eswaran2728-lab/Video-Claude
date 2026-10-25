# Sangili Karuppar statue — product reel (Eshan Creations)

Source: `VID-20261025-WA0002.mp4` (Drive folder, 15.4 s, 368×640 WhatsApp clip, no speech) and the
user-supplied song `sangili_karupar_song.m4a` (16 s of audio). Preview: `PREVIEW_sangili_karuppar_v01.mp4` (720×1280).

## Story (16.6 s, 1080×1920, 30 fps)
| Out (s) | Source (s) | Beat |
|---|---|---|
| 0.00–1.31 | 10.19–11.50 | Hook: push-in to the face, name on screen from frame 0 (EN + Tamil) |
| 1.31–2.25 | freeze 11.50 | READY STOCK stamp lands on the song's first strong hit |
| 2.25–4.91 | 0.30–2.96 | Zoom-out reveal of the full statue, "1 PIECE · READY STOCK" |
| 4.91–8.15 | 5.00–8.24 | Orbit with CSRT-tracked callouts: gold-painted ornaments, red & gold waist cloth |
| 8.15–9.21 | 12.30–13.36 | Pull back toward the hand |
| 9.21–11.34 | freeze 13.40 | Punch-in on the fist: WITH EETI IN HAND / Eeti provided separately |
| 11.34–13.11 | 13.40–15.17 | Pull back to full statue, RM450 card on the beat (12.05) |
| 13.11–16.60 | freeze 15.17 | End card: RM450, DM TO ORDER, song outro |

Cut points snap to strong onsets of the song. Full map: `edit/timing_map.json`; SFX cue sheet: `edit/cues.json`.

## Pipeline
1. `scripts/upscale.py` — denoise + FSRCNN×2 + Lanczos to 1080×1920 (`edit/src_1080.mp4`).
2. `scripts/track.py` — CSRT tracking of callout anchors → `edit/track.json`.
3. Segments/stills cut with ffmpeg into `edit/assets/` (see README table).
4. `python3 build.py` → `edit/index.html` (grade from `grade_attr.txt`, applied with `hyperframes media-treatment`).
5. `cd edit && npx hyperframes@0.8.193 check` then `render . --quality draft` (preview) / `--quality high` (final, after approval).

SFX: FavStash edit-video pack (Apache-2.0, synthesized). Fonts: Montserrat (OFL), Noto Sans Tamil (OFL).
