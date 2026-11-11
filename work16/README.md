# AA/SEC/F/077 Attendance Record: staff training video (AI voiceover + motion graphics)

16:9, 1920x1080, 30 fps, ≈16 min 36 s, HyperFrames 0.8.193. **Current: v01 preview** (`PREVIEW_AA-SEC-F-077_training_v01.mp4`,
1280x720). No final export has been made and nothing is published.

## Sources
- **Deck:** the creator's `src/AA-SEC-F-077_Attendance_Staff_Training.pptx` (12 slides).
  - Its own media is reused, unchanged, in `edit/assets/deck/`: the green and red **SAMPLE** QR images, and the Google
    Form, confirmation and Google Sheet screenshots (staff details already hidden in the deck).
  - Slide renders: `sheets/deck.jpg`.
- **Script:** the creator's trainer's speaking script, split into 13 scenes in `script16.py`.
  - Captions show the script wording verbatim.
  - The voice uses a spoken form only where the AI needs help pronouncing something:
    - AA/SEC/F/077 is spelled "A. A. S. E. C. F. zero seven seven";
    - QR, DSE, SO, ASO and ID are read letter by letter;
    - times are spoken out ("eight oh five A M"); 11/12 November becomes "the eleventh/twelfth of November";
    - the arrows in the reporting flow become "to".
  - Additions to the spoken text: "Staff understanding check. Let's see how much you remember." and "Question one…ten"
    in the Q&A.

## Voice
- **Engine:** Kokoro-82M, run locally (the model behind `npx hyperframes tts`), voice **af_heart** (US English, female),
  speed 1.0. Free, no account, and nothing leaves the machine.
- **Generation (`tts16.py`):** one clip per line, trimmed. Pauses are 0.42 s between sentences, 0.75 s before a new
  point and 0.3 s after a colon. Each Q&A question gets a 3.5 s think pause, with a countdown ring on screen.
- **Check (`vo_check.py`):** every line was transcribed back with faster-whisper and compared with the script (`vo_check.json`).
  - The form code originally slurred ("Aasek"), so it is now spelled letter by letter; the re-check hears "AASECF 077".
  - The remaining differences are spelling only (QR vs Q R, DSE vs D S E, "Authorized" vs "Authorised").

## Scenes (`build16.py`; every reveal starts on the voice line that names it)
| # | Scene | Motion graphics |
|---|---|---|
| 01 | Introduction | Navy title card with the two QR cards; a shift timeline from Check-in to Check-out; what you need (phone, AirAsia Google account, correct QR); the three agenda points; the goal |
| 02 | Two QR codes | Green and red QR cards that pulse on "Green means… / Red means…"; "Never swap them"; the four steps (Scan → Fill in → Submit → Recorded) |
| 03 | Scan the Check-in QR | Phone scanning the green QR, then the form; a/b/c checklist; "Personal Gmail ✗"; the title is verified, then shown as the wrong (Check-out) title and back again |
| 04 | Fill in the Check-in form | The deck's form screenshot with highlight boxes (Record email tick, DSE/SO/ASO), designation tiles (ASO picked), date, Name and Staff ID fields, a "What the form asks" list |
| 05 | Select your team | Team radio screenshot; ALPHA/BRAVO/CHARLIE/DELTA tiles; Sheet tabs; the Bravo→Alpha example landing in the wrong tab; reporting flow Staff → DSE → Operations Security Manager → Correction |
| 06 | Review, submit, confirm | Six-item checklist ticking; Submit press; "Once per shift"; the real confirmation screenshot ("YOU SHOULD SEE THIS"); troubleshooting, plus "inform your supervisor" and duplicates |
| 07 | Scan the Check-out QR | As 03 in red; "not the green QR again"; the shorter Check-out form |
| 08 | Complete the Check-out form | Check-out form screenshot with highlights; overnight example (11 Nov 8 PM → 12 Nov 8 AM: select 11 Nov); same team (Bravo = Bravo); no Name/Designation; confirmation screenshot |
| 09 | Times are automatic | Check-in/Check-out time cards stamped 8:05 AM and 8:10 PM on the voice; "no time field"; Sheet timestamp columns highlighted |
| 10 | Where the record goes | Four-step flow into the Sheet; Alpha/Bravo/Charlie/Delta tabs highlighted on the screenshot; supervisors review; staff responsibilities |
| 11 | Common mistakes | Six ✗ → ✓ rows, revealed on each mistake and its fix; "inform your respective DSE" |
| 12 | Final recap | Check-in and Check-out columns (4 steps each); three rules; escalation flow; purpose; "Thank you" card; "Any questions?" |
| 13 | Staff understanding check | 10 questions with a think countdown, then the expected answer; "END OF TRAINING" card |

- **Chrome:** form code (top left), chapter "NN / 13 · title" (top right), and a progress bar along the bottom.
- **Captions:** every spoken line, at most 2 lines on screen at once, on a navy bar.
- **Look:** the deck's palette (navy, Check-in green, Check-out red, amber highlights) in Inter.

## Sound (`mix16.py`)
- **Voice:** high-pass, light presence boost, gentle compression; the master is set to −14 LUFS.
- **Music:** "Motivating Mornings" (Ahjay Stelino, Mixkit #33, Mixkit Stock Music Free License). It plays only under the
  opening title, the thank-you card and the end card, and is ducked under the voice.
- **SFX:** soft clicks, pops and dings on reveals, and a swish between scenes. These come from the edit-video pack
  (Apache-2.0), mixed low.

## Note for the creator
- Slide 6 of the deck says "No confirmation screen? … press Submit again". The speaking script says to check the fields
  and connection and to inform your supervisor instead of submitting repeatedly. **The video follows the script.**

## Rebuild
```
python3 tts16.py && python3 build16.py && python3 mix16.py
cd edit && npx --yes hyperframes@0.8.193 render --quality draft --fps 30 --sdr -o ../renders/draft_v01.mp4
cd .. && ./master_preview.sh renders/draft_v01.mp4 PREVIEW_AA-SEC-F-077_training_v01.mp4
```
Final (only after approval): `render --quality high --sdr` → `./master_final.sh renders/final_v01.mp4 FINAL_….mp4`.

## Checks (v01 preview)
- **Render:** 3 workers, about 10 min.
- **Output:** 1280x720, 29,883 frames, 996.2 s; −14.0 LUFS, −1.3 dBFS peak.
- **Playback:** full decode with 0 errors; no black stretches (the navy title/end cards are intended); audio vs `edit/assets/mix.wav` lag 0 ms at three points.
- **`hyperframes check`:** 0 errors. Warnings left: small text inside the mock form UI, and two duplicate-image notices.
- **Snapshots:** `sheets/snap1`, `snap2` and `sheets/preview_v01_sheet.jpg` (one frame every 25 s).
- **Not verified:** I cannot listen. The voice was checked by speech recognition (`vo_check.json`), and levels by measurement only.
