# Silambam @ Festival Kesenian & Kebudayaan Malaysia 2026 — Part 1 + Part 2 highlight reels

9:16, 30 fps, HyperFrames 0.8.193. **Current: v02 previews (see the v02 section). v01 previews:**
- `PREVIEW_silambam_part1_v01.mp4` (≈45.7 s)
- `PREVIEW_silambam_part2_v01.mp4` (≈41.7 s)

Both are 720x1280, −14 LUFS. No final export has been made and nothing is published.

**Finals (approved v02, creator: "Proceed final"):**
- `FINAL_Silambam_Part1_v02_1080x1920.mp4`: 67.4 s, −14.7 LUFS / −1.8 dBFS.
- `FINAL_Silambam_Part2_v02_1080x1920.mp4`: 62.6 s, −14.3 LUFS / −1.6 dBFS.
- Both are 1080x1920, 30 fps, H.264 ≈22 Mb/s, AAC 256k, rendered with `--quality high` and mastered with `master_final.sh`.
- Checked:
  - full decode, 0 errors, no black frames;
  - audio aligned within 3 ms;
  - frames match the approved previews (mean difference 1.6–2.5 levels at 5 sample times).
- Not in git (size). Made as previewed: the gold header wording without the logo; no logo file was received (it came
  only as an inline image). Nothing is published.

**Finals with logo (approved v03, creator: "Proceed final"):**
- `FINAL_Silambam_Part1_v03_logo_1080x1920.mp4`: 67.4 s, −14.7 LUFS / −1.8 dBFS.
- `FINAL_Silambam_Part2_v03_logo_1080x1920.mp4`: 62.6 s, −14.3 LUFS / −1.6 dBFS.
- Both are 1080x1920, 30 fps, rendered with `--quality high` and mastered with `master_final.sh`.
- Checked:
  - full decode, 0 errors, no black frames;
  - frames match the approved v03 previews (mean difference 1.6–2.5 levels);
  - logo crisp in the header (`sheets/final_logo_check.png`).
- The v02 finals without the logo are kept. To free disk space for this render, the regenerable proxy folders of
  work7 and work8 were emptied (rebuild with their `make_proxies.sh`). Not in git (size). Nothing is published.

## v03 — logo added (creator: "Add the logo i attach" / "Remove background")
- The creator's Mahaguru Dr. Sri S. Arumugam PJK medal logo (`src/logo/logo_original.png`, 447x447 on white) has its
  white background removed by `make_logo.py`. A flood fill from the border keeps the whites inside the medal; the edge
  is soft and de-fringed. Output: `edit/assets/logo_arumugam.png` (407x400) + `LOGO_Mahaguru_Arumugam_transparent.png`
  for the creator.
- Placed 150 px high beside the gold "MAHAGURU SRI S ARUMUGAM · STUDENTS" header on both parts. Everything else is v02.
- Previews: `PREVIEW_silambam_part{1,2}_v03_logo.mp4`. Rebuild: `python3 make_logo.py`, then the v02 steps
  (`VERSION=v02 python3 build13.py …` picks the logo up automatically).

## v02 — creator's note on v01: "make those video cinematic look, make the videos run a bit longer time so can see the shows,
## at top header add mahaguru sri s arumugam logo that gold on and add mahaguru sri s arumugam students"
Previews: `PREVIEW_silambam_part1_v02.mp4` (≈67.4 s), `PREVIEW_silambam_part2_v02.mp4` (≈62.6 s). v01 files are kept.
- **Longer shots** (`plan13_v02.py`):
  - performance shots held ~3 s (4 beats) instead of 0.7–1.5 s;
  - self-defence shots get 1.5–2.3 s of lead-in before the slow motion;
  - the human pyramid plays 10 s of source at 1.4x;
  - all 29 clips still used.
- **Team introduction now in Part 1:** v_215647 30.85–33.95, "Mahaguru Sri S Arumugam avargalin maanavargal"
  (students of Mahaguru Sri S Arumugam). The name was confirmed by the creator; the club name before it stays out
  (unclear).
- **Cinematic grade** (`VERSION=v02 python3 render_segments.py`):
  - gentle filmic S-curve (lifted blacks, softened highlights) and −8 % saturation to tame the stage LEDs;
  - teal shadows / warm highlights;
  - then a soft vignette and fine moving grain on the finished frame.
  - A first, darker try was eased after comparison (`sheets/grade_v01_v02.jpg`).
- **Gold header** for the whole video: "MAHAGURU SRI S ARUMUGAM" over "— STUDENTS —" in gold, on a soft dark top shade
  (y≈222–330). Captions moved down to y=420, Part chips to y=430.
  - **Logo:** the creator sent the Mahaguru medal logo inline, but no image file reached this workspace. `build13.py`
    places `edit/assets/logo_arumugam.png` beside the wording automatically once it exists. Needs: re-attach the logo
    as a file.
- Rebuild:
  ```
  ./normalize.sh
  VERSION=v02 python3 render_segments.py part1 part2
  VERSION=v02 python3 mix13.py
  VERSION=v02 python3 build13.py part1
  VERSION=v02 python3 build13.py part2
  ```
  then render `edit/` and `edit_p2/` and master them as in v01.

## Source
- Google Drive folder "Claude video editing" (eswaran3561): 25 videos + 12 photos. Google Drive refused downloads to
  this workspace ("quota exceeded", also for a fresh zip and with Google's own virus-scan confirmation). A chunked
  workaround was stopped as circumvention.
- Used instead: the creator's WeTransfer zip "WhatsApp Unknown 2026-11-02 at 10.24.52 AM.zip" (167 MB): 29 videos + 9
  photos, **WhatsApp-compressed** (576x1024 portrait, 1024x576 / 832x464 / 640x368 landscape).
  - It holds every Drive video, matched by duration (the 4K ProRes IMG_6684/6685/6688 arrive as 640x368), plus 4
    extra clips.
  - Unzipped to `src/wa/` with renamed files `v_HHMMSS.mp4` / `p_HHMMSS.jpeg` (WhatsApp timestamps). `normalize.sh` →
    `src/norm/` (30 fps CFR working copies, regenerable; deleted after the plates were rendered, for disk space).

## What is in the footage (all 29 clips reviewed: `sheets/r8/`, frame strips per clip)
- **Stunts:**
  - watermelon smashed with a blade on a man lying on a bed of spikes: portrait v_215609 (impact 33.95 s) + landscape
    v_225618 (impact 19.45 s);
  - concrete block on a man's head broken with a hammer: portrait v_215613 (impact 24.0 s) + landscape v_225624
    (≈28.6 s);
  - self-defence takedowns and throws: v_225545 (≈8.5 s), v_225554 (≈20.5 s);
  - a human-pyramid pose: v_215617.
- **Stage:** stick sparring (most landscape clips), team line-up, the MCs, the crowd, the final group pose.
- **Backstage:** huddle, hands-in cheers, line-up with sticks.
- **Speech** (Whisper large-v3, `transcripts.json`, word timings `lines.json`); only these are used:
  - v_215628 (MC, English): "Thank you. Right after this we have the next performance."
  - v_213143 (Tamil): "Vanakkam guru, vanakkam"
  - v_215603: "Ready?"
  - v_215631 (MC): "Let's go."
  - v_213120 (MC, Tamil): "…ungaludaiya aadharavu romba romba mukkiyam … romba nandri" — translation pass: "Your support is
    very important. Thank you very much."
- Not used: v_215647 (a team member introduces the team — club and guru names differ between passes, see Unresolved).
  Everything else is stage music and crowd (Whisper's "Thank you for watching" etc. are hallucinations).

## Edit (plan13.py; full table `timing_table.md`, machine-readable `timing_map.json`)
All 29 videos are used at least once (`plan13.check_coverage()` → none missing).

**Part 1 (45.7 s):**
- **Hook:** the watermelon smash, real speed into 0.25x interpolated slow motion through the impact; SMASH. on the hit.
- **Title card:** festival-poster style; date bar 31.10 & 1.11.2026, SILAMBAM, festival name.
- **Backstage** (huddle, hands-in, line-up) under the MC's "Right after this we have the next performance."
- **"Vanakkam guru, vanakkam" salute.**
- **"Ready?"** → SILAMBAM marquee wipe.
- **Fast stick demo:** 15 cuts of 1–2 beats on the music's 0.743 s beat.
- **Brick stunt:** set-up, hammer raise during the music's drop, impact in 0.25x slow motion on the next drum hit with
  UNBREAKABLE., then a REPLAY from the second angle (0.33x).
- **Throw teaser and "COMING NEXT · PART 2" card.**

**Part 2 (41.7 s):**
- **Hook:** the watermelon from the second angle (2ND ANGLE, 0.25x slow motion, AGAIN.).
- **MC speech** ("…your support is very important… thank you") and "Let's go!"
- **SELF-DEFENCE marquee and takedowns/throws:** two in 0.4x slow motion, TAKEDOWN.
- **TEAMWORK:** the human pyramid at 1.6x.
- **The crowd and FINALE:** final poses.
- **End card** over the backstage huddle (SILAMBAM, festival, dates, TERIMA KASIH · THANK YOU).

**Layout:**
- Portrait clips fill the frame.
- Landscape clips sit in a zoomed band (2.0–2.7x, cropped around the action's motion centroid) over a blurred, darker
  copy of themselves, keeping more of the WhatsApp resolution than a full 9:16 crop. The landscape clips are softer at
  phone size.
- Slow motion: ffmpeg `minterpolate` (mci/aobmc) frame interpolation.

## Motion graphics — Prompt Motion references, adapted
1. **Festival lineup promo reel** — https://prompt-motion.com/gonzalomacagno-2de1a9
   - Vertical festival poster: colour bars over a date strip, one huge headline, stacked lines rising out of a mask.
   - Used for the title card, the Part 2 teaser and the end card.
2. **Bold kinetic type showreel** — https://prompt-motion.com/shneural-2abdfa
   - One giant word punching in on the hit, and repeating marquee rows.
   - Used for SMASH. / UNBREAKABLE. / AGAIN. / TAKEDOWN. on the impact frames (with a white flash), and the SILAMBAM /
     SELF-DEFENCE marquee wipes.

Section chips (BACKSTAGE, STICK DEMO, STUNT, REPLAY, SELF-DEFENCE, TEAMWORK, THE CROWD, FINALE) and captions sit
inside the safe area. Type: Inter Display Black/Bold + Inter SemiBold; palette red #e1124b, gold #f2b705 (the yellow
belts), white on a dark ink.

## Sound (mix13.py)
- **Clip sound:** spoken lines at full level, the stage sound low underneath. Slow motion is silent apart from a swish
  into it and sub-impact + hook-impact on the impact frame (edit-video SFX pack, Apache-2.0).
- **Music** — both Mixkit Stock Music Free License, checked on the tag page:
  - Part 1: "Epical Drums 02" (Grigoriy Nuzhny, Mixkit #677); its drop (56.5–57.8 s) sits on the hammer raise, and the
    next hit (58.0 s) on the brick impact.
  - Part 2: "Epical Drums 01" (Mixkit #676).
- Music ducked 11 dB under speech; master −14 LUFS.

## Unresolved
- **Team name, guru name, club.** v_215647 says roughly "we are the students of Maha Guru … (Arumugam / S.R. Mohan?)". The
  passes disagree, so nothing is shown. Please give the exact names if you want them on the title or end card.
- **Quality.** The edit uses the WhatsApp copies. For a sharper final, send the original Drive files another way (e.g.
  Dropbox/WeTransfer of the originals); the same plan re-renders from them.
- **Music.** Not auditioned by ear; stage music in the clips is kept low and may belong to its performers.
- Photos (9 in the zip, 12 on Drive) are not used in v01. Videos were asked for; photos can be added as quick stills.

## Rebuild
```
./normalize.sh                                  # src/wa -> src/norm (30 fps working copies) + sheets
python3 transcribe.py; python3 transcribe_lines.py; python3 score.py
python3 render_segments.py part1 part2          # -> edit/assets/v/part{1,2}_plate.mp4, segments.json
python3 mix13.py                                # -> edit/assets/part{1,2}_mix.wav, edit/part{1,2}_audio.json
python3 build13.py part1 && python3 build13.py part2      # -> edit/index.html, edit_p2/index.html
(cd edit && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_part1.mp4)
(cd edit_p2 && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_part2.mp4)
./master_preview.sh renders/draft_part1.mp4 PREVIEW_silambam_part1_v01.mp4 45.667
./master_preview.sh renders/draft_part2.mp4 PREVIEW_silambam_part2_v01.mp4 41.733
```
