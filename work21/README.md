# Silambam at Hari Sukan Negara, Sepang 2026: event reel

9:16, 1080x1920, 30 fps, HyperFrames 0.8.193.
- **Current:** v02 preview, `PREVIEW_silambam_hari_sukan_negara_sepang_v02.mp4` (2:11, draft render quality; project `edit_v02/`).
- v01 is kept unchanged: `PREVIEW_..._v01.mp4`, 61 s, project `edit/`.
- No final export has been made and nothing is published.

## v02: "use all the videos and pics, about 2 minutes, fast pace, motion graphics, Mahaguru logo at top, Mahaguru Sri S Arumugam students, a good Tamil song"
Built from `plan21_v02.py`, `build21_v02.py` (+ `build21_v02.css`), `render21.py` / `mix21.py` with `VERSION=v02`.
- **All media:**
  - All 107 photos appear in the cut (`plan21_v02` asserts this).
  - Both performance clips are cut through (22 moments), plus the medal-group clip.
  - A photo wall at 1:55 assembles all 107 photos again.
- **Pace:** about 92 hard cuts on a 110 BPM grid.
  - Distinct photos get one beat (0.55 s); near-identical burst frames get half a beat; group photos get 1.5 beats.
  - The song's quieter break (1:10–1:27) slows to longer push-ins on the eight best close-ups ("PROUD MOMENTS").
  - The song's stop is a freeze-flash; the music then returns to fast cuts ("ON THE STAGE").
- **Brand:**
  - The Mahaguru logo (the transparent file supplied for work15) pops in large at 0:09 over the stage lineups, with "MAHAGURU SRI S ARUMUGAM / STUDENTS".
  - It then flies into a header on a dark backing at the top, held until the end card.
  - The end card shows the large logo, the name, the event and the date.
- **Motion graphics:**
  - SILAMBAM slam; the event card from the banner text; IN ACTION and SLOW MOTION tags.
  - MEDALS & BELTS, PROUD MOMENTS and ON THE STAGE titles.
  - TAHNIAH! with particles; the photo wall "PROUD OF EVERY STUDENT".
  - Push-ins on photos, and flashes on section changes.
- **Music:** a commercial Tamil film song was not downloaded (no licence; platforms may mute or claim it). The placeholder is
  "Mumbai Chase", Steve Oxen, Fesliyan Studios: fast, Indian (tabla, sitar, tumbi, shehnai), Indian, not Tamil.
  - Licence: free for non-commercial use with a link to fesliyanstudios.com in the post's description. Commercial or
    monetised use needs a donation licence.
  - Fesliyan notes that TikTok/Instagram/Facebook may limit one track to 60 s.
  - It plays from its first big hit (song 3.85 s) to its natural end.
  - The edit can be re-cut to a song file the creator supplies, as in work15 v02.
- **Checks:**
  - 1080x1920, 3942 frames, 131.4 s; −14.0 LUFS, −1.9 dBFS peak; full decode with 0 errors.
  - Audio lag 0 ms at 10, 60 and 110 s.
  - Cuts sit a median 29 ms from the beat grid.
  - The only dark frames are the closing fade. Cuts are snapped to the frame grid, which fixed one-frame black gaps at clip→photo cuts.
  - `hyperframes check`: 0 errors, 3 structural warnings.


## Sources
**Drive folder** `1r1MNaLtPCPtHEZbUQF0geENsWPKxnyts`, new set uploaded 22.11.2026 (the folder's earlier set is work15).
- Contents: 107 photos (File_000–106, PNG), plus 3 iPhone clips (IMG_1921 63.7 s, IMG_1918 26.3 s, IMG_2025 5.8 s; 464x848, 30 fps).
- Downloaded one request per file; sizes verified against Drive (`src/all.tsv`).

**Event, read from the banner:**
- MAJLIS PERASMIAN HARI SUKAN NEGARA · PERINGKAT DAERAH SEPANG 2026
- 15 NOVEMBER 2026 (AHAD) | UNIKL MIAT, DENGKIL

**What the media shows:**
- Two Silambam stick performances:
  - IMG_1921: a girl, in an indoor hall.
  - IMG_1918: a boy, on the stage in front of the banner.
- A medal and belt presentation to many young athletes (photos).
- A medal group on stage (IMG_2025).
- A judges' table (File_106).

**Speech:** none. faster-whisper large-v3 returns only stock hallucinations ("Terima kasih kerana menonton", "Selamat malam") over
steady venue sound (`transcripts.json`). The story is visual, with no speech captions.

## Story (`plan21.py`; full map in `timing_table.md`)
The edit is locked to the music's beat (99.38 BPM; drop on 9.66 s).

| Time (s) | Section | Content |
|---|---|---|
| 0–4.8 | Hook | Jump kick into a floor move → jumping spin → the close-up shout with the stick overhead. "SILAMBAM" slams in at 2.4 s. |
| 4.8–9.7 | Context | The boy on stage in front of the real banner. The title card builds: MAJLIS PERASMIAN / HARI SUKAN NEGARA / PERINGKAT DAERAH SEPANG 2026 / date / venue. A riser leads into the drop. |
| 9.7–24.1 | Performances | Six cuts alternating the two performers ("IN ACTION"): a 0.5x slow-motion spin ("SLOW MOTION"), follow-crops on the boy, ending on the kneeling stick salute. |
| 24.1–43.5 | Medals & belts | "MEDALS & BELTS" over the first photo, then 14 photos cut on the beat. Medal-going-on moments alternate with proud results, across different ages, with alternating push-ins. |
| 43.5–53.1 | Payoff | Two group photos, then the medal-group clip. "TAHNIAH! CONGRATULATIONS to all the young Silambam athletes", with gold particles. |
| 53.1–61 | End card | SILAMBAM · HARI SUKAN NEGARA · PERINGKAT DAERAH SEPANG 2026 · 15.11.2026 · UNIKL MIAT, DENGKIL, then a fade. |

## Look and sound
- **Grade:** gentle S-curve, +6 % contrast, +6 % saturation, slight warmth, light sharpening and a soft vignette (`render21.py`).
- **Type:** Inter Display Black Italic, echoing the banner's lettering. Colours are taken from the banner (yellow, red, blue on dark).
- **Music:** "Driving Ambition", Ahjay Stelino, Mixkit #32 (Mixkit Stock Music Free License), from 29.08 s into the track, so its drop
  lands on the performances and its outro on the end card.
- **Venue sound:** kept low under each clip; none under the slow motion.
- **SFX:** 25 cues from the edit-video pack (Apache-2.0), on their visual events (`edit/cues.json`).
- **Loudness:** −14 LUFS.

## Not claimed / limits
- No logos were supplied, so none were added. The black-and-gold club is not named, because nothing in the media names it.
- The presenter is not named. The banner names who officiates the opening, but the woman presenting the medals is a different person.
- The text says only "medals & belts"; the media doesn't show what they were awarded for.
- The clips are low resolution (464x848), so the boy's follow-crop (1.45x) is soft at full size.
- I could not listen to the audio; levels and sync were checked by measurement only.

## Rebuild
```
python3 render21.py && python3 build21.py && python3 mix21.py
cd edit && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 --sdr --workers 3 -o ../renders/draft_v01.mp4
cd .. && ./master_final.sh renders/draft_v01.mp4 PREVIEW_silambam_hari_sukan_negara_sepang_v01.mp4
```
Final, only after approval: `render --quality high`, then `master_final.sh`.

## Checks (v01 preview)
- 1080x1920, 1830 frames, 61.0 s; −14.0 LUFS, −3.8 dBFS peak; full decode with 0 errors.
- Audio/mix lag: 0 ms at 5, 25 and 50 s. The only dark frame is the closing fade.
- `hyperframes check`: 0 errors. The 2 warnings are structural (one large composition), the same pattern work15 rendered with.
- Snapshots and sheets: `sheets/snap1`, `sheets/preview_v01_sheet.jpg`.
