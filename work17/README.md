# AA/SEC/F/042 High-Lift Escort eForm: staff training video (AI voiceover + motion graphics)

16:9, 1920x1080, 30 fps, ≈18 min 18 s, HyperFrames 0.8.193. **Current: v01 preview** (`PREVIEW_AA-SEC-F-042_HiLift_Escort_training_v01.mp4`,
1280x720). No final export has been made and nothing is published.

## Sources
- **Deck:** the creator's `src/High-Lift_Escort_eForm_Staff_Guide_AA_SEC_F_042.pptx` (39 slides; render: `sheets/deck.jpg`).
- **Extraction (`extract17.py`, output `slides.json`):** for every slide, the phone screenshot it shows (copied unchanged to
  `edit/assets/deck/`), the deck's own **red highlight boxes and circles**, and its text.
  - The boxes are read from the slide XML and converted to screenshot pixels, so each highlight in the video sits exactly
    where the deck put it (checked in `sheets/box_check.jpg`).
- **Narration:** the creator's slide-by-slide script, verbatim, in `script17_raw.md`; parsed in `script17.py` (39 scenes,
  203 lines).
  - Captions show the script text.
  - The AI voice gets pronunciation help only:
    - AA/SEC/F/042 → "A. A. S. E. C. F. zero four two";
    - sample data is read out (TEST-AK01 → "test, A K zero one"; KUL-TEST, TEST-HL01, TEST-0001, TEST001, TEST002);
    - times → "ten a.m.", "eleven thirty a.m.";
    - AM/PM → "a.m./p.m.", because "A M" was swallowed in a first take;
    - ETD, QR and ID are spelled; AVSEC → "Av-Sec"; Staff No. → "Staff Number".

## Voice
- **Engine:** Kokoro-82M on the device, voice af_heart, the same voice as the AA/SEC/F/077 video.
- **Generation:** `tts17.py`, the same pipeline as work16 (one clip per line, fixed pauses).
- **Check (`vo_check.py`, output `vo_check.json`):** every line transcribed back and compared with the script.
  - Two lines said "M or PM"; they were fixed and re-checked.
  - The remaining differences are spelling only (QR / Q R, 11.30 / eleven thirty, "High Lift" for Hi-lift).

## Scenes (`build17.py`)
- **Step slides (4–35, phone screenshots), from one template:**
  - the deck screenshot in a device frame (long pages scroll through it);
  - the deck kicker ("PAGE 6 OF 9"), step number and title;
  - the deck's short instruction;
  - "Sample: …" chip, "TEST / SAMPLE DATA" badge, and "Then tap Next" chip.
  - **On the line that says tap / locate / select / enter:** the deck's highlight appears as a pulsing red ring with a tap
    ripple, and the screenshot punches in on that field (zoom of up to 1.55x), zooming back out before the scene ends.
  - **On lines naming the Duty Security Executive:** a red banner, "Report any abnormality immediately to the Duty
    Security Executive".
- **Own layouts:**
  - 1 title and what the training covers;
  - 2 what the form is for (with the form's own instruction quoted);
  - 3 open the form (the deck's QR code, with a scan line);
  - 36 cannot change after Submit;
  - 37 the Google Sheet with the TEST row highlighted;
  - 38 who does what;
  - 39 troubleshooting → escalation (supervisor → System Unit) → manual form only with Head of Department approval →
    at all times → "Thank you / Stay alert…" closing card.
- **Chrome:** form code (top left), "NN / 39 · slide title" (top right), red progress bar.
- **Captions:** every line, on a dark bar.

## Sound (`mix17.py`)
- **Voice:** cleaned and compressed; the master is −14 LUFS.
- **Music:** "Motivating Mornings" (Mixkit #33, Mixkit Stock Music Free License), only under the opening and closing
  cards, and ducked.
- **SFX:** soft pops, clicks and swishes (edit-video pack, Apache-2.0).

## Notes for the creator
- The deck's screenshots show the signed-in work email at the top of several form pages; they are used as supplied.
- Slide 3 shows the deck's real QR code for the form.

## Rebuild
```
python3 extract17.py && python3 tts17.py && python3 build17.py && python3 mix17.py
cd edit && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 --sdr --workers 3 -o ../renders/draft_v01.mp4
cd .. && ./master_preview.sh renders/draft_v01.mp4 PREVIEW_AA-SEC-F-042_HiLift_Escort_training_v01.mp4
```
Final (only after approval): `render --quality high --sdr --workers 3` → `./master_final.sh renders/final_v01.mp4 FINAL_….mp4`.
