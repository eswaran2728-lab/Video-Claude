# 3D wall frame art → key holder with lamps — Eshan Creations reel (work16)

**Current: preview v02** (`PREVIEW_eshan_3d_wall_frame_keyholder_v02.mp4`, 720x1280, 36.9 s, −14 LUFS) — v01 plus motion
graphics. v01 is kept (`versions/index_v01.html`, `versions/cues_v01.json`; rebuild with `VERSION=v01 python3 build16.py`).
Composition 1080x1920, 30 fps, HyperFrames 0.8.193.
**FINAL v03 — clean voice + cinematic (approved):** `FINAL_Eshan_3D_Wall_Frame_KeyHolder_v03_cinematic_1080x1920.mp4`
(not in git, size). The earlier v02 final is unchanged. Nothing is published.
**FINAL (approved v02):** `FINAL_Eshan_3D_Wall_Frame_KeyHolder_v02_1080x1920.mp4` — not in git (size). Nothing is published.

## Sources (Drive folder `1r1MNaLtPCPtHEZbUQF0geENsWPKxnyts`, 2 files, uploaded 8.11.2026; `drive_files.tsv`)
- **M** `IMG_6792.MOV` — iPhone 16 Pro Max, 4K ProRes 422 HLG (HDR), 46.0 s, vertical. The unlit frame held up to the
  camera; the creator explains it in Tamil–English. Tone-mapped to SDR (`make_proxies.sh`); the plate uses 4K
  tone-mapped copies, so punch-ins stay sharp.
- **L** `fa799ce5e58a49c29107dcd042ded275.mp4` — 720x1280 HEVC, 29.4 s, already edited (cuts at 10.6 and 15.4 s). The
  lamps being switched on, then the fully lit frame; voice explains how and closes with the call to action.
- No logo, music, reference or brief was supplied. Branding is text only: **ESHAN CREATIONS · @e_shan9** (from the
  creator's profile). No logo was made up.
- What the footage shows: Shiva and Parvati in relief, painted, in front of a gold mountain/crescent cut-out; "N ❤ A"
  letters on top; two lamps in the top corners that switch on by turning them; **5 key hooks** along the bottom
  (counted on the footage, matches "anju key hold").

## Story (`plan16.py`; full map in `analysis/timing_map.md`; speech in `analysis/transcript.md`)
| output s | beat | what's on screen |
|---|---|---|
| 0–3.07 | **Hook**: the payoff first | The lit frame as a card on its own blurred glow; "QUICK REVIEW · 3D WALL FRAME ART" + KEY HOLDER / LAMPS chips; his "Okay guys, quick review". |
| 3.07–9.0 | What it is | Hard cut to the unlit frame (the lights are "off" until the payoff). Slow push-in on "we call it **3D wall frame art**". |
| 9.0–12.1 | "This was just a frame" | Punch out to wide and hold still. |
| 12.1–16.1 | A customer messaged | Punch in close on the faces. |
| 16.1–20.8 | Key holder, 5 keys | Push in to the bottom, panning with the hand-held frame; **numbered tags 1–5 tracked onto the hooks** (`track_hooks16.py`). |
| 20.8–23.1 | "How to use it? See this lamp" | Top of the frame, both lamps in view. |
| 23.1–27.3 | **Payoff**: "hold the lamp, turn it — it turns on" | Music drops back while he turns it; at 26.77 s the lit frame appears: warm bloom on the lamp, sparks, shimmer, and a beat in the music. |
| 27.3–28.6 | Breathing room | Fully lit frame, no voice, music up. |
| 28.6–34.4 | CTA + goodbye | "Want one for your home? You can follow me", "Okay, bye — thank you!" |
| 33.8–36.8 | End card | ESHAN CREATIONS · Custom 3D Wall Frame Art · @e_shan9 over the darkened lit frame. |

Cut: the unclear passage about "home" (M 24.8–34.6), a mid-video "give a like", repeated "quick review", the two
repeats of the lamp instruction while hands cover lamps 2–3 (L 7.4–19), and the empty wall at the start.

## v02: motion graphics ("Add motion graphics that related to this content")
Picture, cut, captions, music and voice are unchanged from v01; only graphics and their sounds were added
(`gfx_v02.py`, imported by `build16.py` when `VERSION>=v02`). Each one illustrates what he is saying and is pinned to
the real object in the shot:
| output s | he says | graphic |
|---|---|---|
| 5.0–8.4 | "we call it 3D wall frame art" | Callouts drawn onto the real layers, **tracked** with the hand-held frame (`track16.py callouts`): GOLD CUT-OUT (on the mountain peak) and SHIVA &amp; PARVATI (on the crescent on Shiva's hair). |
| 12.4–17.4 | "a customer messaged me… they wanted a key holder" | Message card (NEW MESSAGE · CUSTOMER) with typing dots; "Request: **KEY HOLDER**" appears on the word; its key becomes a gold badge that flies down and lands on the hooks, then the 1–5 hook tags pop. The card is a summary of the request, not a quote. |
| 21.8–23.0 | "see this lamp" | Pulsing gold rings **tracked** on both lamps (`track_lamps16.py`). |
| 23.2–28.3 | "hold the lamp, turn it here… it turns on" | HOLD + TURN card: the arrow turns in quarter-turns while he turns the lamp; on the reveal frame (26.77 s) its bulb lights and the line changes to LAMP ON. |
| 34.0–34.4 | end card | Recap chips 3D WALL ART · 5 KEY HOOKS · LAMPS, then the name. |
New sounds (edit-video pack): ticks on callouts and lamp rings, pops on the cards and chips, a click on "KEY HOLDER", a
latch when the key lands, ratchets on the turning arrow — each on the first frame its element appears
(`reports/sync-v02/`). 25 cues in total.

v02 checks: `hyperframes check` passes (0 errors); 1105 frames, 0 decode errors, no black frames; audio vs mix 0 ms at
5/20/30 s; −14.0 LUFS, −1.4 dBFS peak; every graphic checked at phone size (`sheets/v2_*.jpg`, `sheets/preview_v02_sheet.jpg`).

## Look and sound
- **Grade:** M +6 % contrast, +10 % saturation, gentle S-curve, light sharpening (tone-mapped HLG looks flat). L: small
  cool-cast reduction, +5 % contrast. In the lit shots the white letters still look slightly blue: daylight mixing with
  the warm LEDs; I left that rather than force it.
- **Captions:** English meaning of his Tamil–English speech, his own English words kept (3D wall frame art, key holder,
  lamp, follow). Inter Display, cream on a dark pill, gold for the key words, centred, bottom edge at y=1240, max 720 px.
  One caption ("How to use it?") sits at the top because the frame is held low there and would cover the faces.
- **Music:** "Love is Eternal", Ahjay Stelino, Mixkit #37, **Mixkit Stock Music Free License** (allows social-media use;
  checked on mixkit.co). Starts 1.5 s in, so a low-end beat lands on the lamp reveal. About 12 dB under the voice,
  dipped while he turns the lamp, lifted on the reveal, the glow hold and the end card.
- **Voice:** both clips cleaned (85 Hz high-pass, light denoise, presence +2 dB), matched in level, compressed. 
- **SFX:** edit-video pack (Apache-2.0), 15 cues in `edit/cues.json`, each on its event frame (strips in `reports/sync-v01/`).

## Checks on the v01 preview
- `hyperframes check`: passes, 0 errors (warnings: file size/structure, and a contrast warning on the end title while
  it is still masked out of view).
- 1105 frames / 36.83 s render; preview 720x1280, full decode with 0 errors, no black frames.
- Audio vs `edit/assets/mix.wav`: 0 ms lag at 5, 20 and 30 s. Preview −14.0 LUFS, −1.5 dBFS peak.
- Section balance: voice −19 to −21 dB RMS in every spoken section; music+SFX ≈12 dB below under speech.
- Phone-size stills: every caption checked against faces; hook tags checked against the hooks (`sheets/`).
- **Not done:** a human listening pass. I could not play the audio; Tamil wording, mix balance and SFX levels were
  checked by transcription and measurement only.

## Open questions for the creator
1. "You can **follow me**" — the model heard "pulanam/puranam"; please confirm it was "follow".
2. The cut passage (M 24.8–34.6) about "home" — if it explains the N ❤ A letters (e.g. normally "HOME", the customer
   asked for initials), tell me and I'll put it back with a caption.
3. Captions are in English. Want Tamil script or Tanglish captions instead? Send the exact wording and I'll set it.

## Rebuild
```
./download.sh && ./make_proxies.sh
python3 transcribe_fine.py                  # optional; transcripts are committed
python3 plate16.py draft && python3 track_hooks16.py && python3 track_lamps16.py && python3 track16.py
VERSION=v03 python3 build16.py && VERSION=v03 python3 mix16.py   # build writes edit/gfx_cues.json, which the mix reads
# v03 voice: <venv>/bin/python -I tools/voice_isolate.py <DeepFilterNet3 dir> analysis/voice/M_raw.wav analysis/voice/M_df.wav (same for L)
cd edit && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v02.mp4
cd .. && ./master_preview.sh renders/draft_v02.mp4 PREVIEW_eshan_3d_wall_frame_keyholder_v02.mp4
```
Final (only after approval): `python3 plate16.py` (slow, high-quality encode) → `render --quality high --fps 30` →
`./master_final.sh renders/final_v01.mp4 FINAL_….mp4`.

## Final v02 (creator: "Proceed final")
- Same composition as the approved v02 preview. `python3 plate16.py` (high-quality plate: CRF 14, preset slow, from the
  4K tone-mapped copies) → tracking re-run on that plate (hooks within 18 px, lamps 3 px, callouts 2 px of the preview;
  tags checked on the final frames) → `VERSION=v02 python3 build16.py && python3 mix16.py` →
  `render --quality high --fps 30` → `./master_final.sh renders/final_v02.mp4 FINAL_….mp4` (video copied, AAC 256k,
  2-pass loudnorm).
- Checks: 1080x1920 H.264 High, yuv420p, 30 fps, 1105 frames, 36.9 s, 31.4 Mb/s; AAC 48 kHz stereo; −14.0 LUFS,
  −2.0 dBFS peak; full decode 0 errors; no black frames; audio vs `edit/assets/mix.wav` 0 ms at 5/20/30 s; contact
  sheet `sheets/final_v02_sheet.jpg` matches the preview; first frame = hook title, last frame = end card.
- Still open (not changed for the final): "follow me" wording, the cut "home" passage, caption language. No human
  listening pass was possible in this session.

## v03: clean voice + cinematic ("Remove the background noise make it my voice clear and then make the video cinematic")
Built with `VERSION=v03` (now the default; `VERSION=v02` / `v01` rebuild the earlier versions; their compositions and
cues are in `versions/`). Story, captions and v02 graphics are kept.
- **Voice:** both clips run through **DeepFilterNet3** (`tools/voice_isolate.py`, model from the DeepFilterNet repo,
  MIT/Apache-2.0; venv with deepfilternet + torch) → `analysis/voice/{M,L}_df.wav` (not in git). Then 80 Hz high-pass,
  −2.5 dB at 250 Hz (mud), +2.5 dB at 3.5 kHz (presence), +1.5 dB air shelf, de-esser, two-stage compression.
  - Measured on the full clips: background in pauses −30.5 → −72 dB (M) and −31.4 → −70 dB (L); speech-to-noise
    13.7 → 51 dB and 16.3 → 54 dB. In the final mix, pauses sit ~31 dB under speech.
  - A Tamil→English re-transcription of four phrases gives the same meaning before and after (no words lost).
- **Picture (film look, in the plate):** on top of the v02 correction — warm highlights / slightly cool shadows, lifted
  blacks with a soft highlight roll-off, warm halation on bright areas (lamps, gold), vignette, fine moving grain
  (`plan16.FILM`; the glow blend runs in RGB).
- **Camera:** the hard punch cuts in the story are now smooth eased moves (pull back on "just a frame", ease in to the
  faces on "a customer messaged me", ease out as the frame is lowered). The lit hold after the reveal is **slow motion
  0.7x** with frame blending (+0.57 s).
- **Transitions / finishing (`gfx_v03.py`):** lights-off dip from the lit opening into the unlit frame; warm light-leak
  sweep into "how to use it?"; anamorphic flare streak across the lamp on the reveal frame; letterbox bars close in for
  the end card; hook title focus-pull and wider tracking.
- **Score:** "A New Life", Eugenio Mininni, Mixkit #543, **Mixkit Stock Music Free License** (film score, orchestral
  hybrid). It builds from near-silence under the whole story; its swell (24.62 s in the track) is placed on the lamp
  reveal (output 26.77 s), so the music starts at 2.15 s. Level set against the voice: ~13–15 dB under speech, it
  swells only after his last word "…on", forward on the slow-motion glow and the end card.
- **Sound design:** riser peaking on the reveal (kept under the voice), sub-impact + shimmer on the reveal, soft
  whooshes on each eased camera move and the light leak, lights-off thock, impact as the letterbox closes.
- **Checks (v03 preview):** `hyperframes check` passes; 1122 frames / 37.4 s; 0 decode errors; no black segments
  (the dip stops just short of black); audio vs mix 0 samples; −14.0 LUFS, −1.4 dBFS peak; voice −19 to −21 dB RMS in
  every spoken section, music+SFX 13–15 dB under it; SFX strips `reports/sync-v03/`; contact sheet
  `sheets/draft_v03_sheet.jpg`. **No listening pass** — judged by measurement and transcription only.

## Final v03 (creator: "Proceed final")
- `VERSION=v03 python3 plate16.py` (high-quality plate, 12 min) → tracking re-run on it (hooks ≤14 px, lamps ≤6 px,
  callouts ≤3 px from the reviewed preview) → `build16.py` + `mix16.py` → `render --quality high --fps 30`
  (`renders/final_v03.mp4`, 389 MB / ~83 Mb/s because of the film grain; kept as the archive master, not in git) →
  `./master_final_reencode.sh renders/final_v03.mp4 FINAL_….mp4` (x264 CRF 17 slow, film tune, capped 30 Mb/s;
  2-pass loudnorm; AAC 256k).
- Checks: 1080x1920 H.264 High, yuv420p, 30 fps, 1122 frames, 37.5 s, 29.1 Mb/s, 137 MB; AAC 48 kHz stereo;
  −14.0 LUFS, −2.0 dBFS peak; full decode 0 errors; no black segments; audio vs `edit/assets/mix.wav` 0 ms at 5/20/30 s;
  delivery encode vs the high-quality render PSNR 37–47 dB; contact sheet `sheets/final_v03_sheet.jpg` matches the
  preview. No human listening pass in this session.
