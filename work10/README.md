# Cyber Roadshow 2026 — event recap (AirAsia AVSEC), HyperFrames, 1080x1920, 30 fps

| version | file | length | status |
|---|---|---|---|
| v03 final (current) | `FINAL_Cyber_Roadshow_Recap_v03_1080x1920.mp4` (1080x1920, 30 fps, H.264 ~19 Mb/s, AAC 256k) | 45.0 s, 1350 frames, -14.0 LUFS / -2.0 dBTP | approved, final export |
| v03 preview | `PREVIEW_cyber_roadshow_recap_v03.mp4` (720x1280) | 45.0 s, 1350 frames, -14.0 LUFS / -2.0 dBTP | approved preview (kept) |
| v02 final (superseded: GTR still visible in places) | `FINAL_Cyber_Roadshow_Recap_v02_1080x1920.mp4` (1080x1920, 30 fps, H.264 ~19 Mb/s, AAC 256k) | 45.0 s, 1350 frames, -14.0 LUFS / -2.0 dBTP | approved, final export |
| v02 preview | `PREVIEW_cyber_roadshow_recap_v02.mp4` (720x1280) | 45.0 s, 1350 frames, -14.0 LUFS / -2.0 dBTP | approved preview (kept) |
| v01 | `PREVIEW_cyber_roadshow_recap_v01.mp4` (720x1280) | 25.4 s | superseded (kept) |

Nothing is published, scheduled or uploaded.

## v03 — creator's notes on v02 and what changed
Notes: upscale all the images; use every image, but leave out the blurry ones; show the AirAsia AVSEC and Allstars logos
for the full length of the video.
- Upscaled: all 19 photos with Real-ESRGAN realesr-general-x4v3 (BSD-3; weights blended 50/50 with its denoise variant so
  it cleans rather than invents texture), CPU, `upscale_photos.py` -> `edit/assets/p3/` at 5760x3240 (1.5x the v02 plates,
  so the zooms stay sharp). Weights are not in git: github.com/xinntao/Real-ESRGAN releases v0.2.5.0 -> `models/`.
- Clear photos only: IMG_6419, IMG_6420 and IMG_6436 are left out (motion blur; still smeared after upscaling).
  The other 16 photos and all 4 videos are used.
- Logos: the creator's AirAsia AVSEC badge and Allstars "Dare to Dream" logo (`src/logos/`) on one white bar, top-left,
  0-45 s (`make_logos.py`: badge cut out of its black square, Allstars upscaled x4). Tip cards, chapter labels and the
  phone panel moved down 26-30 px to make room.
- GTR: v02 still showed GTR branding in places (the 912ed0e8 booth card, 2ee1beb9 in the hook, IMG_6435 and some
  photo-wall tiles). v03 marks every GTR banner/logo position per photo in `gtr_boxes.py`; `make_assets_v03.py` and
  `build_v03.py` refuse any card, tile or photo window (at its widest zoom and both ends of its pan) that touches one.
- Re-cut: hook = IMG_6426, IMG_6429, 2ee1beb9, IMG_6427; the talk section uses IMG_6430 alone; the people montage is six
  photos over the same 16 song beats (2,2,3,3,3,3); the photo wall is the 16 photos + 3 stage frames (IMG_6421) + 1 booth
  frame (IMG_6425). Sound, music and timing are otherwise as v02. Exact times: `edit/timing_map_v03.json`.

### Rebuild v03
```
python3 upscale_photos.py    # ~75 s per photo on 4 CPU cores
python3 make_logos.py
python3 make_assets_v03.py   # booth cards + photo-wall tiles, GTR-checked
python3 build_v03.py         # -> edit/index.html (GTR-checks every photo window)
cd edit && npx hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v03.mp4
cd .. && ./master_preview.sh renders/draft_v03.mp4 PREVIEW_cyber_roadshow_recap_v03.mp4 45.0
# final (after approval): render --quality high -o ../renders/final_v03.mp4, then
./master_final.sh renders/final_v03.mp4 FINAL_Cyber_Roadshow_Recap_v03_1080x1920.mp4 45.0
```

## v02 — creator's notes on v01 and what changed
Notes: no GTR content at all; use all the images and videos; cut where needed; make it a visually stunning recap.
- GTR removed: the STOP. THINK. VERIFY. close is gone, and every crop keeps the GTR banners out of frame. One possible
  exception: a small GTR mark may show behind the person on the right in IMG_6435 (on screen for two beats).
- All 4 videos and all 19 photos are used (list below). The low-res phone clips play in a framed card over their own
  blurred frame rather than being stretched to full screen.
- Structure: a beat-cut hook with the title, then numbered chapters (01 SET-UP, 02 THE BOOTH, 03 THE CROWD,
  04 THE STAGE, 05 THE PEOPLE), then a finale wall of every photo that settles into the AIRASIA AVSEC lockup.

### Rebuild v02
```
python3 make_assets_v02.py   # booth crop, phone-clip cards, photo plates + 20 tiles, audio_v02.wav (v01 assets kept)
python3 build_v02.py         # content.json + index_v02.tpl.html -> edit/index.html, edit/timing_map_v02.json
cd edit && npx hyperframes@0.8.193 check && npx hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v02.mp4
cd .. && ./master_preview.sh renders/draft_v02.mp4 PREVIEW_cyber_roadshow_recap_v02.mp4 45.0
# final (after approval): render --quality high -o ../renders/final_v02.mp4, then
./master_final.sh renders/final_v02.mp4 FINAL_Cyber_Roadshow_Recap_v02_1080x1920.mp4 45.0   # video copied as rendered, audio -14 LUFS
```
v01 is rebuilt with `build.py` / `index.tpl.html` (they write the same `edit/index.html`; run the one you need).

### v02 timing map (music at 123 BPM: 1 bar = 1.951 s; stage section on the event song's own beat)
| out (s) | source | treatment | graphic |
|---|---|---|---|
| 0.00–3.90 | IMG_6426, IMG_6436, 2ee1beb9, IMG_6427 | two-beat cuts with a punch-in on each | EVENT RECAP / CYBER / ROADSHOW / 2026 / 27 October |
| 3.90–7.80 | b048 phone clip 9.0–12.95 s | card over its blurred frame | 01 SET-UP |
| 7.80–13.66 | IMG_6425 (crop on the AVSEC side, slowed 1.48x) | dimmed as photo cards land on the beat: 912ed0e8, 38af901c, ACAE9274, IMG_6433 | 02 THE BOOTH |
| 13.66–15.61 | dc95 phone clip 18.0–20.0 s | card over its blurred frame | 03 THE CROWD |
| 15.61–17.56 | IMG_6461 | pan + punch | |
| 17.56–31.30 | IMG_6421 2.73–16.47 s (tracked stage crops) with IMG_6429 + IMG_6430 (deepfake talk) at 27.37–29.83 | slide-up entrance on the song | 04 THE STAGE; tips 01–03 on the lyric lines |
| 31.30–39.20 | IMG_6437, 6438, 6439, 6440, 6435, 6419, 6420, 6423 | two song beats each, pan + push | 05 THE PEOPLE; ring on the phone in IMG_6439 |
| 39.20–45.00 | all 19 photos + one stage frame | wall slides up, tiles pop in, wall settles 1.55x -> 1.0x | AIRASIA AVSEC / Security Is Everyone's Responsibility / CYBER ROADSHOW 2026; fade to black |
Exact times: `edit/timing_map_v02.json`.

### v02 audio
- 0–17.86 s and 38.95–45.0 s: "House Fest" by Alejandro Magaña, Mixkit, Stock Music Free License (covers social posts
  and online marketing; the Restricted licence was not used). Track sections and offsets: `edit/assets_map_v02.json`.
- 17.44–39.20 s: the event's own performance song from IMG_6421, kept in sync with the stage footage. Its rights belong
  to the organiser/performers — confirm before using the recap outside your own channels.
- SFX (synthesized, Apache-2.0): a thock per booth card, a pop per tip, a swish into the stage and into the finale.
- Mastered by 2-pass loudnorm to -14 LUFS / -2 dBTP. The music edit points were placed on the beat grid but not auditioned by ear.

### Known soft shots
The v_walk crop and the dance punch-in (motion blur in the source), and IMG_6420 (a blurry photo, on screen for two beats).

---
# v01 notes (kept for reference)


## Rebuild
```
./make_proxies.sh        # stream the two ProRes 4K HLG MOVs from Drive -> proxy/*.mov (SDR, full res); originals untouched
python3 transcribe.py    # speech check on every video (none found: no talking-head footage in the folder)
python3 track.py         # follow the red stage screen in IMG_6421 -> edit/track.json
python3 make_assets.py   # tracked 9:16 crops, photo plates (from the DNGs), audio bed -> edit/assets/
python3 build.py         # content.json + index.tpl.html -> edit/index.html, edit/timing_map.json
cd edit && npx hyperframes@0.8.193 check && npx hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v01.mp4
cd .. && ./master_preview.sh renders/draft_v01.mp4 PREVIEW_cyber_roadshow_recap_v01.mp4 25.4
```
All on-screen wording: `content.json` (each line notes where it was verified).

## Source inventory (Drive folder 1_GhbNTw56Y0ljytsH3Z7dQ7Hiv_QFTqP)
| file | what it is | used |
|---|---|---|
| IMG_6421.MOV (ProRes 4K HLG, 24.4 s) | walk through the hall, stage dance to a cyber-safety song, booths | yes: soundtrack 0–24.4 s + stage shots |
| IMG_6425.MOV (ProRes 4K HLG, 4.0 s) | static AVSEC booth shot | room sound under the close only |
| dc95…mp4 (464x832, 81 s) / b048…mp4 (576x1024, 12.9 s) | low-res crowd walkthrough / booth setup | no (low resolution) |
| 15 DNG + 4 JPG | booth, stage launch, deepfake talk, visitors, prize moment | IMG_6426, IMG_6429, IMG_6437, IMG_6439, IMG_6423 |
No recording of anyone speaking to camera exists in the folder (Whisper large-v3, with and without voice detection);
the creator confirmed this is an event recap.

## Timing map (output time = IMG_6421 song time)
| out | source | treatment | graphic |
|---|---|---|---|
| 0.000–2.733 | IMG_6426.DNG launch on stage | pan along the guests to the button press | title: EVENT RECAP / CYBER / ROADSHOW / 2026 / 27 October (words on the beats) |
| 2.733–4.205 | IMG_6421 2.733–4.205 | tracked 9:16 crop: walking in | tip 1 from 3.715 |
| 4.205–9.603 | IMG_6421 4.205–9.603 | tracked crop on the stage screen + dancers | "Use strong & unique passwords" to 6.62 |
| 9.603–12.547 | IMG_6421 9.603–12.547 | tighter 1:1 crop on the dancers | "Multi-factor authentication" 10.09–12.42 |
| 12.547–15.000 | IMG_6429.DNG deepfake talk | whole photo as a card over its blurred self, slow push | — |
| 15.000–16.472 | IMG_6421 15.0–16.472 | tracked crop | "Report suspected cyber incidents" 15.0–18.4 |
| 16.472–18.925 | IMG_6437.DNG visitor at the booth game | slow pan/push | (tip 3 continues) |
| 18.925–20.888 | IMG_6439.DNG prize moment | pan from the visitor to the AVSEC staff member | ring on the phone ("Thank you for your feedback!") + keychain |
| 20.888–25.400 | IMG_6423.DNG booth | pan to the GTR banner | bracket on "STOP. THINK. VERIFY.", then the words on three beats and "AIRASIA AVSEC / Security Is Everyone's Responsibility / CYBER ROADSHOW 2026"; fade to black |
Cuts sit on the song's beat grid (~122 BPM, 0.280 + n·0.491 s).

## Verified wording
- Stage screen: "CYBER ROADSHOW 2026", "27 October" (IMG_6421, IMG_6426).
- Song (IMG_6421, Whisper word confidence): "Use strong and unique passwords" (0.87–0.99); "multi-factor authentication"
  (first word, probably "enable", uncertain → not shown); "Report any suspected cyber incidents via the phishing button" (0.87–1.0).
  Not used: the opening line ("Avoid"/"Always sharing sensitive details…" — first word uncertain) and ~13 s / ~20 s (unclear).
- Banners (IMG_6423): "STOP. THINK. VERIFY." (GTR), "AIRASIA AVSEC — Security Is Everyone's Responsibility".

## Prompt Motion references
- Animated business explainer — https://prompt-motion.com/alex-prompter-1ea044 — clean white cards with a small label and
  bold short text, built one at a time; adapted for the three tip cards (on the exact lyric lines) and the calm close.
- The showreel prompt — https://prompt-motion.com/templates/showreel — taken only for its discipline: one typeface (Inter),
  three colours + black/white (taken from the event: red, yellow, white), moves on the beat, no glows/particles/crossfades.
  Its full showreel style was not used.

## Audio
The event's own song (IMG_6421) carries 0–24.4 s, faded 23.65–24.37; the booth's room sound (IMG_6425) takes over for
the close. No music was added. SFX (edit-video skill pack, synthesized, Apache-2.0): soft pop per tip card, one swish
into the closing push, one thock on VERIFY. The song is the performance track recorded at the event; its rights are the
organiser's/performers' — confirm before using the recap outside your own channels.
