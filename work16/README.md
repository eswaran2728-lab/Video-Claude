# 3D wall frame art → key holder with lamps — Eshan Creations reel (work16)

**Current: preview v01** (`PREVIEW_eshan_3d_wall_frame_keyholder_v01.mp4`, 720x1280, 36.9 s, −14 LUFS).
Composition 1080x1920, 30 fps, HyperFrames 0.8.193. **No final export yet; nothing is published.**

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
python3 plate16.py draft && python3 track_hooks16.py && python3 mix16.py && python3 build16.py
cd edit && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v01.mp4
cd .. && ./master_preview.sh renders/draft_v01.mp4 PREVIEW_eshan_3d_wall_frame_keyholder_v01.mp4
```
Final (only after approval): `python3 plate16.py` (slow, high-quality encode) → `render --quality high --fps 30` →
`./master_final.sh renders/final_v01.mp4 FINAL_….mp4`.
