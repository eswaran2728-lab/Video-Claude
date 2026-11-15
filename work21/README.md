# work21 — Silambam at Sambutan Hari Deepavali Peringkat Negeri Selangor 2026

Vertical highlight reel (1080x1920, 30 fps, 45.5 s) cut from 12 supplied clips (13 uploaded; one exact duplicate).

- `source/` — original clips from the Drive folder (not in git). c01..c13 in order of file size; c03 was a byte-identical copy of c02.
- `analysis/` — scripts used to study the footage (audio cross-correlation, motion, stitch test).
- `build.py` — builds `vNN/index.html` from `vNN/edit-plan.json` and applies the grade. `audio.py` — makes the audio bed and accents.
- `v01/edit-plan.json` — the edit: every shot's source clip, in-point, duration, camera move, texts, grade.
- `v01/timing-map.json` — source-to-output timing map (generated).
- `v01/validation-notes.md` — what was checked and what was not.

Rebuild: `python3 build.py v01 && python3 audio.py v01`, then in `v01/`: `npx hyperframes lint`, `npx hyperframes render --quality draft`.
Proxies in `v01/assets/video/` are 2x lanczos upscales of the sources (see the ffmpeg line in validation notes).
New revisions: copy `v01/` to `v02/` and edit the plan there; keep v01 as is.
