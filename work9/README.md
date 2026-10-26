# Silambam masters introduction — HyperFrames, 1080x1920, 30 fps, exactly 15.000 s (450 frames)

**Final (approved v01):** `FINAL_Silambam_Masters_Intro_1080x1920.mp4` — `python3 build.py`, then in `edit/`
`npx hyperframes@0.8.193 render --quality high --fps 30 -o ../renders/final_raw_v01.mp4`, then
`./master_final.sh renders/final_raw_v01.mp4 FINAL_Silambam_Masters_Intro_1080x1920.mp4` (video copied; audio -14 LUFS / -2 dBTP).
Checked: 1080x1920, 30 fps, 450 frames, 15.000 s video and audio, full decode, -13.9 LUFS, peak -2.3 dBFS.
Music is still the TEMPORARY reference-audio bed. Nothing is published.

**v02 (preview, awaiting approval):** credits revised by the creator — Master Sasitharan moved below Master Sivaraj;
Special Thanks now lists Junior Master P.Eswaran, Junior Master Tibaneswaran, Junior Master Tivyapriya and "And Other
Junior Masters and Sepang Silambam Students" (typed with a doubled "AND"; shown without it — to confirm). Credit
spacing tightened so the longer list fits. `PREVIEW_silambam_masters_v02.mp4`; the v01 final is kept
(`FINAL_Silambam_Masters_Intro_1080x1920.mp4`, copy in renders/FINAL_v01_backup.mp4).

## Rebuild
```
python3 cutout.py photo_a   # (one photo per run; BiRefNet-general needs the memory) FSRCNN x2 + matte -> edit/assets/cut/
python3 make_audio.py       # TEMPORARY music bed from the reference audio, exactly 15.000 s -> edit/assets/music.wav
python3 build.py            # content.json + index.tpl.html -> edit/index.html (+ edit/timing.json)
cd edit && npx hyperframes@0.8.193 check && npx hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v01.mp4
cd .. && ./master_preview.sh renders/draft_v01.mp4 PREVIEW_silambam_masters_v01.mp4
```
**All wording is in `content.json`** (header, association, the four introductions, every credit, ending, handle).
Name sizes per master are in `build.py` (`NAME_PX`); figure size/position in `FIG_H` / `FIG_BOTTOM`.

## Assets
| file | what | used for |
|---|---|---|
| src/reference.mov | 476x848, 12.57 s, TikTok-recorded reference (landscape inside vertical) | wording, order, timing study, temporary music |
| src/photo_d.jpg (720x960) | Mahaguru Sri S Arumugam — white hair, Selangor + Malaysia flags; same pose as reference 0–1 s | intro 1 |
| src/photo_c.jpg (960x540) | Mahaguru Selvaraju — outdoor; matches reference 1–2.6 s | intro 2 (smallest figure, ~330 px tall in the original) |
| src/photo_b.jpg (600x600) | Mahaguru DATO A.Sivakumar — blue studio, staff raised; matches reference 2.6–4.3 s | intro 3 |
| src/photo_a.jpg (608x844) | Grand Master Vijayasegaran — plain wall; matches reference 4.6–6.5 s | intro 4 |
| src/logo.png (447x447 RGBA) | gold Mahaguru Dr. Sri S. Arumugam medal logo | opening, header, ending |
Cutouts: FSRCNN x2 (OpenCV dnn_superres, local) then BiRefNet-general (local onnx); staffs, hands and feet kept.
Fonts: Oswald (variable, Google Fonts, OFL) for display type, Inter for the handle. SFX: edit-video skill pack
(synthesized, Apache-2.0): zoom-swish per wipe, thock per name, shimmer on the logo glints.

## Timeline (all transitions inside the slots)
| time | scene |
|---|---|
| 0.00–1.00 | red light sweep, logo springs in, gold glint across the medal, association slides out of its mask, header settles; red wipe 0.80–1.20 |
| 1–3, 3–5, 5–7, 7–9 | per master: 3 nested angular red frames draw on, then turn in depth (rotateY + slight roll, parallax against the figure); portrait rises behind a diagonal reveal then pushes in; rank slides out of its mask, then the name (condensed, skewed italic) with a soft impact; light sweep; layout alternates left/right; outgoing layer smears (6 px blur) under a diagonal red wipe with ghost bands |
| 9–14 | credits, one static layout on plain charcoal: association, MAHAGURU, GRAND MASTER, SENIOR \| BLACK BELT columns, SPECIAL THANKS; whole list visible 9.3–13.8 |
| 14–15 | logo with gold glint, THANKS FOR / WATCHING, red bar, handle; music fades 14.35–15.0 |

Music (TEMPORARY, the reference video's own audio, ~105.5 BPM): out 0–10.10 = ref 1.32–11.42 (the ref downbeat
at 2.32 s lands on intro 1 at 1.00 s; intros 2–4 land on strong 8th-note hits), then a two-bar jump back
(ref 6.87, downbeat to downbeat, 40 ms crossfade) to fill 15 s, faded out at the end.

## Spelling — please confirm
See `_spelling` in content.json. Used in the preview: Kanesan and Thangapaandiyan (as the reference credits read
clearly). Open: Vijayasegaran (intro) vs Vijisegaran (credits) — both kept as in the reference; Selvaraju (intro and
supplied text) vs Selavaraju (reference credits) — Selvaraju used in both places.
