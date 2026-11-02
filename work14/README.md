# Sangili Karuppar — 3D-printed statue reel (customer design → real print)

**Preview v01 (waiting for approval):** `PREVIEW_sangili_karuppar_3dprint_v01.mp4`
- 720x1280, 31.97 s, −13.9 LUFS.
- HyperFrames 0.8.193, 1080x1920, 30 fps.
- No final export yet; nothing is published.

## Sources
- `src/source.mov`: the creator's clip, 34.6 s, 720x1280 HEVC HLG (tone-mapped to SDR in `proxy/src30.mov`).
  - 0–20.4 s: handheld footage of the printed statue.
  - 20.5–23 s: CapCut logo; then black to 34.6 s.
  - Audio: the creator's Tamil voice-over mixed with a music bed (likely added in CapCut).
- `src/customer_reference.jpg`: the customer's picture (the design the print was made from).
- Facts from the creator: 3D printed in **PETG filament**, **6 inch**, made from the customer's picture. No other
  specs (layer height, print time, price) are shown; the on-screen print percentage is a progress animation only.

## What he says (Whisper large-v3, 4 passes on the isolated voice: `transcript.json`, `transcript_fine.json`)
| src (s) | Romanized Tamil (captioned) | meaning |
|---|---|---|
| 0.5–3.9 | Oru customer enakku request panni, intha picture-la irunthu | A customer asked me, from this picture |
| 4.3–10.9 | intha Sangili Karuppar, oru 6 inches-la … venum nu kettu irunthaanga | this Sangili Karuppar, 6 inches, is what they asked for |
| 11.4–17.7 | So athukkaaga, avanga ketta photo-la ulla maathiri naan design panni eduthathu | so I designed and made it just like their photo |
| 18.2–20.6 | So neenga paakkalaam, avanga kudutha athe colour tone-la (kuduthirukkom) | you can see: the same colour tone they gave |
| 22.2–27.9 | Ungalukkum intha picture venum appadinna, … intha Sangili Karuppar venum appadinna, neenga thaaraalamaa … | if you want this too, feel free … |
| 28.0–33.8 | (contact … bio … Vanakkam) | captioned in English only: "contact me (details in my bio)", then "Vanakkam!" |

Unresolved words:
- ~9.1 s: a word after "6 inches-la", heard as "kaattais / cottage"; left out of the caption.
- 28–33 s: the exact Tamil wording around "bio / number" is unclear.

## Edit (`plan14.py`, `compose14.py`, `mix14.py`, `build14.py`)
- **Voice:**
  - isolated from the CapCut music with DeepFilterNet3 (`tools/voice_isolate.py`; music bass −23 dB, speech band kept);
  - pauses at 5.1, 11.1, 17.7, 24.9 and 29.6 s tightened to ~0.3 s;
  - CapCut tail removed;
  - 34.6 s → 31.1 s of speech + 0.9 s end hold.
- **Statue cut-out:**
  - BiRefNet-lite ONNX masks (`make_masks.py`, keyframes every 3rd frame + optical-flow fill);
  - the holding hand removed by an edge-connected skin-colour filter (`cutout_lib.py`; the PETG print itself has no
    skin colours);
  - shots with a hanging cable (5.5–7.6 s), blurry close-ups (12.5–14 s) and cropped-head frames are not used.
- **Scenes:**
  1. Customer's picture as a photo card.
  2. **3D print:** the real statue prints layer by layer on a glowing print bed (nozzle line + slicer-style outline above
     it, printer ticks). "SANGILI KARUPPAR" sits behind the statue. A 6 INCH ruler draws on "6 inches"; PETG FILAMENT /
     3D PRINTED chips; the picture is pinned as a REF thumbnail.
  3. **Design → real:** picture card above the real statue, "REAL · 3D PRINTED IN PETG".
  4. **Same colour tone:** black + silver swatches sampled from the picture and from the print.
  5. **WANT ONE?** with 6 INCH / PETG / 3D PRINTED.
  6. **End:** SANGILI KARUPPAR · 3D PRINTED STATUE · PETG · 6 INCH · CONTACT · LINK IN BIO.
- **Music:** "Epical Drums 05" (Grigoriy Nuzhny, Mixkit #680), **Mixkit Stock Music Free License**, ducked 17 dB under
  the voice. The original CapCut music is not used (its licence is unknown).
- **SFX:** edit-video pack (Apache-2.0), each on its visible event (`edit/cues.json`).
- **Prompt Motion techniques adapted:**
  - "Photo print app launch film" https://prompt-motion.com/twoclipping-221cab: a photo becoming a physical print; the
    card carried through scenes.
  - "Engraving-style Claude ad" https://prompt-motion.com/lexnlin-038035: marks painted over real imagery — the slicer
    outline, nozzle line and ruler.

## Checks on the preview
- Full decode, 0 errors; 959 frames / 31.97 s; −13.9 LUFS, −2.0 dBFS.
- No black frames; voice aligned (cross-correlation).
- Lint passes; snapshots of every scene and a 1 fps sheet at phone size (`sheets/`).
- Not done: a human listening pass.

## Rebuild
```
python3 make_masks.py                     # ~35 min CPU
<venv>/bin/python -I tools/voice_isolate.py <DeepFilterNet3 dir> src/vo_raw.wav src/vo_iso.wav
python3 compose14.py
python3 mix14.py
python3 build14.py
cd edit && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 -o ../renders/draft_v01.mp4
cd .. && ./master_preview.sh renders/draft_v01.mp4 PREVIEW_sangili_karuppar_3dprint_v01.mp4
```

## Final v01 (approved preview -> final)
- `FINAL_Sangili_Karuppar_3DPrint_v01_1080x1920.mp4` (not in git; *.mp4 ignored): HyperFrames `render --quality high --fps 30` of the
  same composition as PREVIEW v01 -> `renders/final_v01.mp4`, then `./master_final.sh` (video copied, AAC 256k, 2-pass loudnorm).
- Checks: 1080x1920 H.264, 30 fps, 959 frames, 32.0 s; -14.0 LUFS integrated, -2.2 dBFS peak; 0 decode errors; no black frames;
  audio vs edit/assets/mix.wav lag 0.0 ms; contact sheet `sheets/final_v01_sheet.jpg` matches the preview.
