# FOCA Checklist (AA/SEC/F/070): staff training video (AI voiceover + motion graphics)

16:9, 1920x1080, 30 fps, 8 min 28 s, HyperFrames 0.8.193. **Current: v01 preview** (`PREVIEW_FOCA_Checklist_training_v01.mp4`,
1280x720). No final export has been made and nothing is published.

## Sources
- **Deck:** the creator's `src/FOCA_Checklist_Staff_Guide.pptx` (30 slides; render `sheets/deck.jpg`).
- **Extraction (`extract19.py` → `slides.json`):** for each slide, the deck's own material:
  - phone screenshot and close-up image (copied unchanged to `edit/assets/deck/`);
  - the red highlight boxes, converted to screenshot pixels;
  - the role badge (Security staff / Airline Representative / Security Representative);
  - the text.
- **Narration:** the creator's slide script, verbatim (`script19_raw.md`), parsed by `script19.py` into 30 scenes and 134 sentences.
  - **Trainer directions are not spoken** ("Point to…", "Show…", "Ask trainees…"); the motion graphics do the pointing.
  - **Pronunciation help for the AI voice:**
    - AA/SEC/F/070 → "A. A. S. E. C. F. zero seven zero"; airasia.com → "Air Asia dot com";
    - STA/ATA/STD/ATD spelled out; "(PDF to Drive + Sheet)" → "PDF to Drive plus Sheet";
    - "Keep it on, Restricted": without the comma it was heard as "unrestricted".

## Voice
- **Engine:** Kokoro af_heart on the device (same voice as the F/077 and F/042 videos).
- **Check:** every line transcribed back (`vo_check.json`). The remaining differences are spelling only.

## Scenes (`build19.py`)
- **Step slides:**
  - The deck screenshot in a phone frame, plus the step label and role badge (blue for Security, orange for Airline Rep).
  - The title and the deck's instruction.
  - On the line that says tap / look for / enter / choose / sign, the deck's highlight appears as a pulsing ring with a
    tap ripple, the screenshot punches in on that field, and the deck's **CLOSE-UP** card pops in beside it.
- **Own layouts:**
  - 1 title (who does what, in order; same phone);
  - 2 three role cards;
  - 3 rules;
  - 4 QR code with a scan line;
  - 5 Chrome steps plus the "Add to Home screen" tip;
  - 7 the whole form;
  - 17 the phone passes from the Airline Rep to the Security Rep;
  - 22 "Not saved" steps;
  - 27 Drive folder path (My Drive → AA-SEC Signed Forms (RESTRICTED) → FOCA) with the PDF name pattern;
  - 28 FOCA Records row (TEST data) with the PDF link highlighted;
  - 30 five questions ticked green, then the practice prompt.
- **Chrome:** form code, "NN / 30 · title", red progress bar. **Captions:** every line.

## Sound (`mix19.py`)
- **Voice:** cleaned and lightly compressed.
- **Music:** "Motivating Mornings" (Mixkit #33, Mixkit Stock Music Free License), under the title and the closing practice
  section only.
- **SFX:** soft clicks and pops (edit-video pack, Apache-2.0).
- **Limiter:** a gentle limiter keeps the true peak under −1.5 dBTP at −14 LUFS.

## Notes for the creator
- The Drive screenshots show the account avatar ("E") and the sharing dialog with the people list already blurred, as in
  the deck. The PDF and record shown are the deck's TEST record.

## Rebuild
```
python3 extract19.py && python3 tts19.py && python3 build19.py && python3 mix19.py
cd edit && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 --sdr --workers 3 -o ../renders/draft_v01.mp4
cd .. && ./master_preview.sh renders/draft_v01.mp4 PREVIEW_FOCA_Checklist_training_v01.mp4
```
- **Checks:**
  - Output: 1280x720, 15,234 frames, 507.9 s; −14.0 LUFS, −1.3 dBFS peak.
  - Full decode with 0 errors; audio lag 0 ms; `hyperframes check` 0 errors.
- **Final (only after approval):** `render --quality high --sdr --workers 3` → `./master_final.sh`.
