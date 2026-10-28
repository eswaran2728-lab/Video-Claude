# Earbuds (noise cancelling) affiliate reel — HyperFrames, 1080x1920, 30 fps, 32.57 s

**Current: preview v05 (waiting for approval):** `PREVIEW_earbuds_noise_cancel_v05.mp4` (720x1280, -14 LUFS). No final
export has been rendered and nothing is published.

| version | file | what changed |
|---|---|---|
| v05 | `PREVIEW_earbuds_noise_cancel_v05.mp4` | creator on v04: "Its good but the colour grading look like artificial": natural light-falloff background, milder grade, b-roll matched |
| v04 | `PREVIEW_earbuds_noise_cancel_v04.mp4` | creator's note "add broll from web that relavent to wht i talk": four licensed Mixkit inserts on the problem lines, graded to v03 |
| v03 | `PREVIEW_earbuds_noise_cancel_v03.mp4` | creator's note on v02 "too bright, make it simple, make the background dark, make it cinematic": matte-darkened background, simpler cinematic grade, no face-light; v02's isolated voice kept |
| v02 | `PREVIEW_earbuds_noise_cancel_v02.mp4` | creator's note "do colour grading, if possible isolate my voice": stronger grade + tracked face-light, DeepFilterNet3 voice isolation |
| v01 | `PREVIEW_earbuds_noise_cancel_v01.mp4` | first cut (unchanged; rebuild with VERSION unset) |

## v05 — creator's note on v04: "Its good but the colour grading look like artificial"
Same edit, captions, graphics, audio and b-roll choices as v04; only the look changes.
- **Why v04 looked artificial:** the room was cut down to 30% with a hard matte edge, so he looked pasted onto a dark
  backdrop. A strong grade (contrast, teal/warm split, heavy vignette) sat on top. A wide-feather version was also tried
  and rejected: it left a glow around the hair (`sheets/natural_bg_options.jpg`).
- **Now: light falloff.** The background is 80% bright right beside him and eases (smoothstep over 220 px) to 42% far
  from him, with saturation easing to 75%. The matte edge stays tight (3×3 erode, 2.5 px feather), so there is no halo and
  no step at his outline (`sheets/natural_bg_falloff.jpg`, right column; `VERSION=v05 python3 make_plate.py`).
- **Milder grade** (`grade_v05.json`):
  - contrast +0.08, highlights −0.18, blacks −0.04, saturation −0.05;
  - faint teal shadows / warm highlights (0.035 / 0.025);
  - vignette 0.22, grain 0.015.
- **B-roll** recut with a natural pre-grade (no pre-darkening): `VERSION=v05 python3 make_broll.py` →
  `broll_<id>_v05.mp4` and `broll_v05.json`. v04's files are kept.
- v05 preview checked:
  - full decode, 0 errors; 977 frames / 32.57 s; −13.9 LUFS, −1.5 dBFS;
  - no black frames; audio aligned within 3 ms;
  - 1 fps sheet (`sheets/preview_v05_1fps.jpg`): consistent look, no halo.
  - Not done: a human listening pass.
- Rebuild: `VERSION=v05 python3 make_plate.py && VERSION=v05 python3 make_broll.py && VERSION=v05 python3 build.py`,
  then apply `grade_v05.json` to `#plate #br232 #br918 #br239 #br8742` with `media-treatment`, then render and master.

## v04 — creator's note on v03: "Add broll from web that relavent to wht i talk"
v03 (dark cinematic plate, isolated voice, same cut/captions/graphics) plus four web b-roll inserts. They are used only where he
describes the problem; everything about the product, its features and the payoff stays his real footage, so no other
brand's earbuds or product appear. Pexels and Pixabay returned 403 from this environment; Mixkit was used.
Each item's own page was checked for **"Mixkit Stock Video Free License"** (commercial and social use, no attribution
required) on 2026-10-28. Restricted-licence items (personal use only) were rejected, as were clips showing earbuds/earphones.
| out (s) | his line | clip (Mixkit page) | treatment |
|---|---|---|---|
| 1.46–3.32 | noise romba irukkumna | Woman walks through the city speaking on the phone — https://mixkit.co/free-stock-video/woman-walks-through-the-city-speaking-on-the-phone-232/ | src 2.0 s, 9:16 crop of the 4K file; NOISE word + bars stay on top |
| 4.50–6.43 | okay, namma office-la irunthaalum sari | Busy office space — https://mixkit.co/free-stock-video/busy-office-space-918/ | src 0.5 s; *office* chip on top |
| 6.43–7.43 | car-la porappa | Woman talking on the phone in a car — https://mixkit.co/free-stock-video/woman-talking-on-the-phone-in-a-car-239/ | src 0.2 s; lifted (low-key original) |
| 9.45–11.70 | romba call pesurappa, romba noise kidaikkum | Young man upset while talking on the phone — https://mixkit.co/free-stock-video/young-man-upset-while-talking-on-the-phone-8742/ | src 2.4 s; lifted; *call* pill + noise bars on top |

He stays on camera for the hook's first words, "disturbance-aa irukka?", "intha maathiri time-la namma vanthu" and from
"so, athukkuthaan" to the end.
- `make_broll.py` streams each 4K file, trims it to the line, crops 9:16 around the person and pre-grades it toward v03.
  It writes `edit/assets/v/broll_<id>.mp4` and `broll.json` (source, licence, in-points, crops, output windows, also
  copied into `edit/timing_map_v04.json`).
- In the composition each insert is its own `<video>` (track 5) above the plate. v03's `grade_v03.json` is applied to the
  plate and to every insert with `media-treatment`, so they match.
- Also fixed: a tiny leftover orange dot from the collapsed noise bars (present since v01) now hides fully.
- v04 preview checked:
  - full decode, 0 errors; 977 frames / 32.57 s; −13.9 LUFS, −1.5 dBFS;
  - no black frames; audio aligned within 3 ms;
  - 1 fps sheet and frames around every insert cut (`sheets/preview_v04_1fps.jpg`, `sheets/preview_v04_cuts.jpg`);
  - not done: a human listening pass.
- Rebuild: `python3 make_broll.py && VERSION=v04 python3 build.py`, then apply `grade_v03.json` to `#plate #br232 #br918
  #br239 #br8742` with `media-treatment`, then render and `master_preview.sh` as for v03.

## v03 — creator's note on v02: "Its too bright make it simple and nee make the background dark make it cinematic"
Same cut, captions, graphics, music and SFX; audio is v02's isolated-voice mix (`mix_v02.wav`).
- **Dark background:** a foreground matte separates him and the earbuds case from the room. Everything outside it
  is darkened to 30% and desaturated by 40% (`VERSION=v03 python3 make_plate.py` → `plate_v03.mp4`).
  - Matte: `make_matte.py` with rembg's ONNX models (no pickled code). BiRefNet-lite runs at 10 fps and keeps the
    held case in the foreground. Between its keyframes the union of the neighbouring two is used, so moving hands are
    never darkened. The edge is pulled in about 2 px with a 1.4 px feather.
  - u2net_human_seg was also run (`src/matte_u2.mp4`) but is not used. It drops the case, and its loose outline left a
    light halo around the hair once the wall was dark (`sheets/matte_cmp.jpg`, `sheets/halo_check.jpg` after the fix).
  - RVM (video matting) was not used: running its code from the old download folder was blocked.
- **Simpler, less bright:**
  - the v02 face-light is removed;
  - the base correction is colour balance + light sharpening only, without v01's midtone lift (`grade_ffmpeg_v03.txt`);
  - v02's HSL secondaries are dropped.
- **Cinematic grade** (`grade_v03.json`, applied on `#plate` with `hyperframes media-treatment`):
  - exposure −0.06, contrast +0.16, highlights −0.22, blacks −0.08, saturation −0.12;
  - teal in the shadows, warm highlights;
  - vignette 0.30, film grain 0.035.
- Rebuild v03 (after v01/v02 steps):
  ```
  python3 make_matte.py bir            # ~30 min on this CPU (u2 pass optional)
  export VERSION=v03 && python3 make_plate.py && python3 build.py
  cd edit && npx --yes hyperframes@0.8.193 media-treatment --project . --file index.html --selector '#plate' \
    --grading "$(tr -d '\n' < ../grade_v03.json)" --apply
  npx --yes hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v03.mp4
  cd .. && ./master_preview.sh renders/draft_v03.mp4 PREVIEW_earbuds_noise_cancel_v03.mp4
  ```

## v02 — creator's note on v01: "Do colour grading if possible isolate my voice"
Same cut, captions, graphics, music and SFX as v01.
- **Voice isolation:** DeepFilterNet3 (github.com/Rikorose/DeepFilterNet; model zip from its repo) runs on the joined
  dialogue before the compressor chain (`tools/voice_isolate.py` → `src/voice_df_full.wav`, full strength). The FFT
  denoise is dropped from the chain.
  - The scripts never let DF's own checkpoint loader run: weights are loaded with `torch.load(weights_only=True)`, so
    no pickled code executes.
  - It runs in a throwaway venv (deepfilternet + deepfilterlib only) on the system PyTorch; torchaudio is stubbed and
    used only by DF's file I/O.
  - Measured on the finished voice track: background in the pauses −26.3 → −38.1 dB, speech −20.2 → −21.0 dB, so
    speech-to-background goes from 6.1 to 17.1 dB. (In v01 the compressor lifted the room noise between words.)
  - Intelligibility check (Whisper large-v3 on the raw vs isolated voice, `compare_voice.py`): mean word confidence
    0.582 → 0.607 (English pass) and 0.475 → 0.624 (Tamil pass). No words were lost.
- **Colour grade:**
  - Tracked face-light, baked into `plate_v02.mp4` (`VERSION=v02 python3 make_plate.py`): your face is tracked with
    OpenCV CSRT (`track_face.py` → `track_face.json`, checked on `sheets/face_track_check.jpg`). A soft ellipse lifts
    it about 20% so it reads against the brighter tan shirt; no visible edge.
  - Creative grade, persisted on `#plate` with `hyperframes media-treatment` (`grade_v02.json`):
    - contrast +0.22, highlights −0.20 (ceiling), blacks −0.08;
    - temperature −0.06 (the analysis found a slight warm cast), vibrance +0.16;
    - violet in the shadows (ties to the case), warm highlights;
    - HSL secondaries: case purple +18% saturation, bright tan shirt −14% saturation so your face leads;
    - vignette 0.32, light grain.
  - Before/after of the final grade: `sheets/grade_v02_steps.jpg` (v01 | face-light only | v02). `sheets/grade_v01_vs_v02.jpg` shows a first, weaker try that was replaced. The grade was confirmed in the render:
    the wall region differs by about 24 levels from the ungraded plate.
- Rebuild v02 (after the v01 steps that make `src/dialogue_raw.wav`, `track.json`):
  ```
  python3 track_face.py
  <venv>/bin/python -I tools/voice_isolate.py <dir>/DeepFilterNet3 src/dialogue_raw.wav src/voice_df_full.wav
  export VERSION=v02 && python3 make_plate.py && python3 make_dialogue.py && python3 mix_audio.py && python3 build.py
  cd edit && npx --yes hyperframes@0.8.193 media-treatment --project . --file index.html --selector '#plate' \
    --grading "$(tr -d '\n' < ../grade_v02.json)" --apply
  npx --yes hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v02.mp4
  cd .. && ./master_preview.sh renders/draft_v02.mp4 PREVIEW_earbuds_noise_cancel_v02.mp4
  ```
- v02 preview checked:
  - full decode, 0 errors; 977 frames / 32.57 s; −13.9 LUFS, −1.5 dBFS peak;
  - no black frames; audio aligned with the dialogue within 3 ms;
  - 1 fps sheet at phone size (`sheets/preview_v02_1fps.jpg`): the grade is consistent shot to shot.
  - Still not done: a human listening pass.

## v01

## Source
- Drive folder `1_GhbNTw56Y0ljytsH3Z7dQ7Hiv_QFTqP` holds two files named `3b5b7d85628e467eaa9b80b3eb762869.mp4`
  (ids `1MU4eVzq…` and `1LUcJ517…`, 30,559,028 bytes each). Both were downloaded to `src/orig/` and hashed:
  SHA-256 `629fb550f299ec798c4e2fd98ed45260d56c4203d5715baa2a844a5afc9a4b5a` for both (MD5 `68b132b1…` for both), so
  they are the same file. One copy is used (`src/source.mp4` → `1MU4eVzq…`); both originals stay untouched on Drive.
- 32.79 s, 720x1280 HEVC (recorded 2026-10-27 11:25 UTC), mono AAC 44.1 kHz. One continuous take: him at his desk in a
  tan shirt, holding a purple earbuds case (the case has a small screen on its face; he does not mention it).
- `proxy/src30.mov` = 30 fps CFR copy (x264 crf 14, PCM audio) used for analysis and the plate.

## What he says (Malaysian Tamil with English product words) and what is claimed
Product: **earbuds he bought on TikTok**. No brand or model is named in the audio, so none is shown.
Claims he makes: **noise cancelling**, **two microphones**, the other person hears you clearly and you hear them
clearly. No price, battery, discount or result is mentioned, and none is added.

## Edit
- Hook (his first line is the strongest): *"call pesumbothu background-la noise romba irukkumna, ungalukku
  disturbance-aa irukka?"* — kept first, no reordering.
- Cuts: head 0–0.40 s (camera settling, no speech); the 0.62 s dead pause at src 16.30–16.92 between "…purchase
  pannen" and "intha earbuds-la" (hidden by a reframe). The take has no false starts or repeats; everything else kept.
- Src 0.40–0.66 are blurred, then a blink, so output frames 0–7 hold src frame 20 (sharp, eyes open). Lips are still
  for the first 0.27 s under "call…".
- The last frame is held 0.8 s under the link pill as the music tails out.

## Timing map (source → output). Full machine-readable map: `edit/timing_map.json`
| out (s) | spoken line (src s) | meaning | visual treatment | source asset |
|---|---|---|---|---|
| 0.00–4.50 | call pesumbothu background-la noise romba irukkumna, ungalukku disturbance-aa irukka? (0.40–4.90) | Background noise on calls bothering you? | Push-in 1.00→1.15 on his face; orange noise bars at chest from frame 0; kinetic **NOISE** lands on "noise" (1.46) and turns orange/widens on "disturbance" (3.64) | camera |
| 4.50–11.70 | okay, namma office-la irunthaalum sari, car-la porappa, intha maathiri time-la namma vanthu romba call pesurappa, romba noise kidaikkum (4.90–12.10) | At the office or in the car, calls get a lot of noise | Wide + slow drift. *office* chip (5.27), *car* chip (6.43) merge into a *call* pill (9.75); noise bars return around it on "romba noise" (10.93) | camera; drawn icons |
| 11.70–15.90 | so, athukkuthaan naan intha earbuds-a TikTok-la vanthu purchase pannen (12.10–16.30) | That's why I bought these earbuds on TikTok | Pill + noise collapse to a dot on "so" (11.96); punch-in to face + case as he lifts it (12.65–13.05); the dot flies onto the real case and opens into a tracked ring + EARBUDS label (13.50–15.62) | camera; case tracked with OpenCV CSRT (`track.json`) |
| 15.90 | — cut — (16.30–16.92 removed) | | reframe 1.27 → 1.00 hides the jump | |
| 15.90–20.30 | intha earbuds-la noise cancelling and then two microphones irukkurathaala (16.92–21.30) | The two features | Punch-in 1.16 on face + case at chest; label 1 NOISE CANCELLING on "noise cancelling" (17.17), its mini noise bars go flat on "cancelling" (17.76); label 2 TWO MICROPHONES on "two" (18.51) | camera |
| 20.30–24.70 | ungaloda call vanthu noise cancel aayi, neenga pesurappa (21.30–25.70) | Your call gets noise-cancelled when you talk | *call* pill + noise (21.16); noise flattens into a clean line on "cancel" (22.48); pill splits into NEENGA ↔ AVANGA on "neenga" (23.46) | camera |
| 24.70–29.06 | [unclear] thelivaa vilangum, ungalukkum avanga pesurathu clear-aa vilangum (25.70–30.08) | They hear you clearly, you hear them clearly | Punch-in 1.13 on face + case; pulse NEENGA→AVANGA (25.64), AVANGA→NEENGA (26.72); CLEAR on "clear-aa" (28.38) | camera |
| 29.06–32.57 | so ungalukku venumna, keezha link-ku click panni purchase pannikonga (30.08–32.79) | Buy it from the link below | Wide; *link* pill with a down arrow on "keezha" (29.82), pressed on "click" (30.54); last frame held 31.77–32.57 | camera |

Graphics are drawn explanations (shapes and labels), not product evidence; every product shot is his real footage.
No cut-out, 3D model or tracking of hidden surfaces; the "reveal" is a tracked ring on the real case.

## Captions
Romanized Malaysian Tamil, as spoken, with his English words kept in English. This follows the rule in his own
`malaysian-affiliate-script-video-director` skill (Tamil audio → Romanized Tamil captions, not translation). Tamil script
is not used, so Tamil font rendering does not arise; Montserrat (local `edit/assets/fonts`) was confirmed in the render.
Text and times: `captions.py`. The reading comes from 7 Whisper large-v3 passes:
- auto / Tamil / English / translate;
- phrase chunks and finer windows;
- a re-transcription of the edited track.

Whisper's one-pass Tamil was garbled, and its one-pass translation flipped "thelivaa vilangum" (clear) into "will not
be able to hear", so no single pass was trusted. **Unresolved (please confirm):**
| src s | caption shown | issue |
|---|---|---|
| 4.95–6.83 | office-la irunthaalum sari | two passes hear "office vanthaalum sari" |
| 11.31–12.10 | romba noise kidaikkum | last word heard as kidaichu / kidaikkum / kekkum |
| 14.12–16.18 | TikTok-la vanthu purchase pannen | verb ending unclear; "vanthu" in 2 of 4 passes |
| 25.70–26.60 | (not captioned) | lead-in before "thelivaa vilangum" heard as "appasil oru" — left out, not guessed |
| 30.84–31.56 | keezha link-ku | heard as "keezhe-la vilakku-kku" (= link-kku) |

## Look and sound
- Grade (`grade_ffmpeg.txt`, baked into the plate):
  - gentle midtone lift, with highlight roll-off on the bright ceiling;
  - slightly less magenta in the skin;
  - +4% saturation and a light unsharp.
  - Skin stays natural. AI upscaling (Real-ESRGAN) was tested for close-ups and rejected: it invents a waffle texture
    on the shirt (`sheets/test_cmp.jpg`). Punch-ins stay ≤1.27x with one Lanczos resample from the source.
- Palette: violet glass and lavender (#c9a8ff) taken from the case; warm orange only for "noise"; white text.
- Dialogue (`make_dialogue.py`): 80 Hz HPF, light FFT denoise, 2-stage compression, -3 dBFS limiter.
- Music: "Digital Clouds", Alejandro Magaña (A. M.), Mixkit #175, **Mixkit Stock Music Free License** (the page's
  licence field, checked 2026-10-27). It sits about 17 dB under the voice, lifts slightly in pauses and the end hold,
  and fades out.
- SFX: edit-video's synthesized pack (Apache-2.0), one per visible event, transient on the event frame
  (`edit/cues.json`): hook impact, thock (NOISE), pops (chips/labels/ring), swish (punch-in), light shutter (cut), latch
  (noise goes flat ×2), ticks (pulses), ding (CLEAR), click (link press).
- Master: 2-pass loudnorm -14 LUFS (preview -1.5 dBTP, final -2 dBTP).

## Motion references (Prompt Motion) and what was adapted
1. **Speech built as architecture** — https://prompt-motion.com/gdgtify-287ddf
   - Words get roles; the cue sheet follows phrases, not a beat grid, with moments of stillness.
   - Used for the hook: NOISE lands on the spoken "noise" and changes on "disturbance".
2. **Shape morphing through UI states** — https://prompt-motion.com/twoclipping-5cba86
   - One element carried through states.
   - Used for: chips → call pill → dot → ring on the real case; noise bars → flat line → NEENGA↔AVANGA link → link pill.
3. **Talking-head clip edit** — https://prompt-motion.com/sab8a-364a5a
   - The speaker stays on camera, with phrase captions with keyword colour and graphics that react to the line.
   - Used for the overall treatment.

Construction guidance came from https://prompt-motion.com/templates/showreel: one type system, a restrained palette and
deterministic timeline time. Its 120 BPM "something on every beat", half-second holds and looping were not adopted; they
would fight the dialogue.

## Skills used
- `edit-video` (base: cut, captions, safe area, sound on the frame, review).
- `adaptive-glass` (palette from footage, glass chips, sound map).
- `hyperframes` CLI 0.8.193 (renderer smoke-tested first: `smoke/`).
- His `malaysian-affiliate-script-video-director` (caption language rule).

Inspected and not used:
- The repo's `windows-install/clean-cut-windows.zip`, opened in a scratch folder. Its `clean-cut` skill does
  cut + plain captions only and forbids graphics/music; `video-style-picker` asks a style question first.
- `intelligent-video-editor` (Remotion; branding only on request).

## Rebuild
```
python3 transcribe.py; python3 transcribe_chunks.py; python3 transcribe_fine.py; python3 transcribe_prompted.py
python3 track_case.py                  # CSRT track of the case -> track.json (+ sheets/track_check.jpg)
python3 make_plate.py                  # EDL + head hold + framing + grade -> edit/assets/v/plate.mp4
python3 make_dialogue.py               # -> edit/assets/dialogue.wav ; python3 verify_cut.py re-transcribes it
python3 build.py                       # -> edit/index.html, edit/cues.json, edit/timing_map.json
python3 mix_audio.py                   # dialogue + music + SFX -> edit/assets/mix.wav (+ stems)
cd edit && npx --yes hyperframes@0.8.193 check && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v01.mp4
cd .. && ./master_preview.sh renders/draft_v01.mp4 PREVIEW_earbuds_noise_cancel_v01.mp4
# after approval only:
# cd edit && npx --yes hyperframes@0.8.193 render --quality high --fps 30 -o ../renders/final_v01.mp4
# cd .. && ./master_final.sh renders/final_v01.mp4 FINAL_Earbuds_Noise_Cancel_1080x1920.mp4
```
Large media (originals, proxy, plate, renders) are git-ignored and rebuilt by the scripts.

## Review of the encoded preview
**Performed:**
- Full decode (0 errors). 977 frames / 32.57 s; audio 32.60 s; -14.0 LUFS, -1.7 dBFS peak.
- No black frames; no freezes other than the intended holds.
- Audio aligned with the dialogue track within 3 ms (cross-correlation).
- Frame 1 and the first 3 s at 5 fps; a 1 fps sheet of the whole video at phone size; snapshots of every layout.
- Caption box inside the 269 px top line and 720 px centre width; captions above the eyes (never over the mouth).
- Graphics between chin and hands, nudged right where he holds the case at the left. Product visible in every
  product beat.
- Re-transcription of the cut (no lost words).

**Not performed:** a human listening pass. I cannot hear the audio, so music taste, SFX loudness against the voice and
the Tamil wording are checked only by measurement and ASR.
