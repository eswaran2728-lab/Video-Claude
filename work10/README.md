# Cyber Roadshow 2026 — event recap (AirAsia AVSEC), HyperFrames, 1080x1920, 30 fps, 25.4 s

Preview v01: `PREVIEW_cyber_roadshow_recap_v01.mp4` (720x1280). Final export waits for approval. Nothing is published.

## Rebuild
```
./make_proxies.sh        # stream the two ProRes 4K HLG MOVs from Drive -> proxy/*.mov (SDR, full res); originals untouched
python3 transcribe.py    # speech check on every video (none found: no talking-head footage in the folder)
python3 track.py         # follow the red stage screen in IMG_6421 -> edit/track.json
python3 make_assets.py   # tracked 9:16 crops, photo plates (from the DNGs), audio bed -> edit/assets/
python3 build.py         # content.json + index.tpl.html -> edit/index.html, edit/timing_map.json
cd edit && npx hyperframes@0.8.193 check && npx hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v01.mp4
cd .. && ./master_preview.sh renders/draft_v01.mp4 PREVIEW_cyber_roadshow_recap_v01.mp4
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
