# Sepang team recap + congratulations — Kejohanan Silambam Antara Sekolah Tamil Peringkat Negeri Selangor 2026

9:16, 1080x1920, 30 fps, 80 s, HyperFrames 0.8.193. **Current: v02 preview** (`PREVIEW_sepang_silambam_recap_v02_song.mp4`, 95.6 s). The v01 preview is kept
(`PREVIEW_sepang_silambam_recap_v01.mp4`, 80 s, composition in `versions/index_v01.html`). No final export has been made and
nothing is published.

## Sources
- **Drive folder** `1r1MNaLtPCPtHEZbUQF0geENsWPKxnyts`: 97 unique files, uploaded 3.11.2026 (listing: `drive_files.tsv`,
  de-duplicated: `dl_list.tsv`).
  - 11 videos (iPhone HLG HEVC, 60 fps, about 2 min in all).
  - 86 photos (HEIC/JPG).
  - Downloaded by `download.sh` (one plain request per file).
  - Videos → SDR proxies by `make_proxies.sh` (`proxy/`); photos → upright sRGB JPEGs by `convert_photos.py` (`src/photos/`).
  - Contact sheets: `sheets/photos_*.jpg`, `sheets/v_*.jpg`.
- **Poster** (chat): `src/poster/poster_kejohanan_2026.jpg`.
- **Logos** (chat), cleaned by `make_logos.py`:
  - Mahaguru Dr. Sri S. Arumugam medal: the same file as in work13; its transparent version is reused.
  - Persatuan Silambam Malaysia: kept on its original white background, shown inside a white card or disc. Removing the
    white automatically also erased the figures' white uniforms.
  - The figure-with-stick logo ("MY SILAMBAM SELANGOR" on its ring; the creator calls it the Selangor logo): cut from its
    black background with BiRefNet-lite.
- **Results:** the creator's message (see `plan15.ZONES` / `OVERALL`; sums are asserted). The team name "Persatuan Silambam
  Malaysia Daerah Sepang" is also from that message.
- **Speech:** none usable. `transcripts.json` (faster-whisper large-v3) finds only crowd noise, "give a clap", and an
  unclear name announcement in IMG_5221. The story is therefore visual, with no captions of speech.

## Story (output seconds; `plan15.py`, `timing_table.md`)
| | time | content |
|---|---|---|
| Hook | 0–5.7 | A bout (IMG_5215) → three students with medals and certificates, while a counter rolls 0→13. "13 MEDALS · SEPANG TEAM" locks with gold particles. |
| Poster → motion graphics | 5.7–15.3 | The poster tilts in as a card. Its own title pieces tear out (KEJOHANAN, SILAMBAM breaking past the edges, PERINGKAT NEGERI SELANGOR, 2026), then regroup with the date / time / venue boxes, the Tamil slogan and the organisers. |
| The day | 15.3–25.0 | THE ARENA (crowd), THE ATHLETES (seated), the march-in, THE BOUTS, then a 0.5x slow-motion exchange. |
| Results | 25.0–49.2 | Five zone cards on the music's drop: school rows with silver/bronze badges that spin in. Schools without a medal read "PARTICIPATED". Each card ends on a zone-total counter. |
| Tally | 49.2–58.8 | GOLD 0 (dimmed) / SILVER 4 / BRONZE 9, then medals per zone as stacked bars. GRAND TOTAL 13 MEDALS lands on a downbeat with rays and gold particles. |
| Congratulations | 58.8–73.3 | Eight photos, one every 3 beats: the students with medals, the podium, the masters. "TAHNIAH! CONGRATULATIONS to all our students, masters & participating schools … for their hard work, dedication & achievements". |
| End card | 73.3–80 | The three logos, PERSATUAN SILAMBAM MALAYSIA DAERAH SEPANG, MAHAGURU SRI S ARUMUGAM · STUDENTS, the poster's கலையை காப்போம், KEJOHANAN SILAMBAM 2026 · 31.10.2026. |

**Header:** the three logos plus a gold "MAHAGURU SRI S ARUMUGAM / STUDENTS" stay up for the whole video until the end
card, where the logos are shown large.

## Prompt Motion references (adapted, not copied)
- "Poster breaking its frame" https://prompt-motion.com/pankajkumar-dev-0bee87. The prompt: "a poster breaking out of its
  own frame". The pieces are the poster's own pixels, cut along a torn edge (`make_poster_pieces.py`), with no retyping.
- "Badge unlock screen animation" https://prompt-motion.com/bthreeagency-b9b8d9. Solid metallic badges that spin in on Y,
  settle without bounce, then release a particle burst; gold particles on the grand total.
- "Festival lineup promo reel" https://prompt-motion.com/gonzalomacagno-2de1a9. The zone name is the headline, school
  rows rise out of a mask line, and a counter footer closes each card.

## Look and sound
- **Grade** (`render15.py`): gentle S-curve, +7 % contrast, +5 % saturation, slight warmth in the highlights, light
  sharpening and a soft vignette. Results and hook backgrounds are blurred and darkened copies of the podium clip.
- **Music:** "Driving Ambition", Ahjay Stelino, Mixkit #32, Mixkit Stock Music Free License (checked on the tag page).
  - It starts at 13.46 s into the track, so the drop lands on the results and the outro on the end card.
  - Fades out to 80 s.
- **Clip sound** is kept low underneath (crowd, the stick clacks in the bouts). Slow motion is silent apart from SFX.
- **SFX:** edit-video pack (Apache-2.0), 86 cues in `edit/cues.json`. They cover the tears, badge shimmers, counters,
  impacts and camera shutters.
- **Loudness:** −14 LUFS.

## Not claimed
- No photo or clip is tied to a particular school or result. The podium shots and bouts are general tournament footage.
- No gold medal is implied; the gold column shows 0.

## Rebuild
```
./download.sh && ./make_proxies.sh && python3 convert_photos.py && python3 make_logos.py && python3 make_poster_pieces.py
python3 render15.py && python3 build15.py && python3 mix15.py
cd edit && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 --sdr -o ../renders/draft_v01.mp4   # --sdr: some photos carry HDR metadata
cd .. && ./master_preview.sh renders/draft_v01.mp4 PREVIEW_sepang_silambam_recap_v01.mp4
```
Final (only after approval): `render --quality high --sdr` → `./master_final.sh renders/final_v01.mp4 FINAL_….mp4`.

## Checks (v01 preview)
- 720x1280, 2400 frames, 80.0 s; −14.0 LUFS, −1.6 dBFS peak.
- Full decode with 0 errors; no black frames; audio vs `edit/assets/mix.wav` lag 0 ms at three points.
- `hyperframes check`: 0 errors. Remaining warnings are the rolling counter digits (they are meant to pass quickly) and
  the file size. Heavy overlays were reduced (pre-blurred photos, linear gradients) after a black-capture risk warning.
- Snapshots at phone size: `sheets/snap1`–`snap3`, `sheets/preview_v01_sheet.jpg`.
- I could not listen to the audio; music placement and SFX levels were checked by measurement only.

## v02: the creator's song and credits clip ("add this song, add that video at last, remove the song of the video, make sure the song beat and sound sync")
Built with `VERSION=v02` (`plan15_v02.py`); outputs carry `_v02`.
- **Music:** the creator-supplied "Nimirndhu Nil" (Shankar Mahadevan, film *Saroja*, 2008),
  `music/nimirndhu_nil_creator_supplied.m4a`. It is not in git (copyright).
  - Rights for posting are the creator's call. Platforms may mute or claim a commercial film song; the in-app music
    library is the safe route.
- **Beat sync:** beat grid fitted on the song itself (spectral-flux onsets): 0.48005 s per beat (125 bpm), anchored at its
  drop after the break (song 45.645 s = output 0.0).
  - Checked in 8 s windows over the whole 96 s: the grid sits within 5 ms of the song's beats in every window.
  - Every cut, poster tear, zone card, badge reveal, photo change and the grand total (beat 124 = 59.53 s) are placed
    on that grid (to the nearest frame).
- **Length:** the day montage gains two shots (guests honoured at the banner, IMG_5213; a second bout exchange) so the
  results start on beat 64. Congratulations photos now change every 3 beats.
- **Credits clip:** the creator's `VID-20261102-WA01232.mp4` (15 s: Mahaguru, Mahaguru Selvaraju, Mahaguru Dato
  Sivakumar, Grand Master Vijayasegaran, the masters list, "Thanks for watching") plays last, from 80.65 s.
  - Its picture is untouched (576x1024 scaled to 1080x1920, so it is softer than the rest).
  - Its own song is removed; the supplied song plays under it and fades out over the last 2.5 s.
  - The gold header is hidden there because the clip has its own.
