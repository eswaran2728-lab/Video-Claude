# AirAsia Security: four Partner Briefing guide videos (HyperFrames)

Four separate videos for signers who are handed Security's phone. Each is 1920x1080, 30 fps, and has its own editable
HyperFrames project and SRT. **Status: v01 previews for review** (draft render quality, 1920x1080). No final MP4 has
been made and nothing is published.

| # | Video | Project | Runtime | Target | Preview | SRT |
|---|---|---|---|---|---|---|
| 1 | FOCA Checklist · AA/SEC/F/070 (Airline Representative) | `v1_foca/edit` | 1:26.5 | 80–90 s | `v1_foca/PREVIEW_01_FOCA_Checklist_Partner_Guide_v01.mp4` | `v1_foca/01_FOCA_Checklist_Partner_Guide.srt` |
| 2 | NOTOC (Firearm) · AA-SEC-F-063 (Captain) | `v2_notoc/edit` | 1:17.5 | 75–85 s | `v2_notoc/PREVIEW_02_NOTOC_Partner_Guide_v01.mp4` | `v2_notoc/02_NOTOC_Partner_Guide.srt` |
| 3 | Acknowledgement of Receipt · AA/SEC/F/007 | `v3_aor/edit` | 2:06.8 | ≈ 2:00 | `v3_aor/PREVIEW_03_Acknowledgement_of_Receipt_Partner_Guide_v01.mp4` | `v3_aor/03_Acknowledgement_of_Receipt_Partner_Guide.srt` |
| 4 | Search List · AA/SEC/F/008 | `v4_search/edit` | 1:28.9 | 80–90 s | `v4_search/PREVIEW_04_Search_List_Partner_Guide_v01.mp4` | `v4_search/04_Search_List_Partner_Guide.srt` |

## How the videos are built
- **Original slides on screen.** Each deck is exported at 3840x2160 (`vN/slides/`); `extract20.py` reads each slide.
  - Read: the position of every picture, the deck's red highlight boxes and the role panels (`shapes.json`).
  - Embedded screenshots go to `vN/edit/assets/media/`.
  - Every shot starts on the full slide in its original proportions, then the camera zooms into one panel at a time.
- **Rings and highlights** sit in slide coordinates inside the camera, so they stay on the real buttons while it zooms.
  - "tap" → a pulsing amber ring, timed to the spoken word "tap" (faster-whisper word timestamps).
  - "check" → a held highlight box; extra read time follows the "check" lines.
- **Colour + text for roles.** A pill under the stage always names who has the phone:
  - blue: SECURITY;
  - orange: the person taking the next action (Airline Representative, Captain, staff handing over, CBTO staff,
    witness, person searched).
- **Motion graphics** (on the stage, never over screen fields):
  - phone handovers between labelled people;
  - Situation A/B box flow;
  - "Where your signed copy goes": signed PDF with Record ID → restricted AirAsia folder → record log → email copy;
  - witness outcomes;
  - the closing "Your part: Check → Sign → Confirm → Hand back" card.
- **Captions:** at most 2 lines, in a band under the stage, synced per sentence; the same text is written to the `.srt`.
- **Voice:** Kokoro-82M on the device (af_heart, speed 0.85), reading the script verbatim.
  - Rate: 126–138 words per minute overall, with longer pauses before each action.
  - Read holds per plan file.
  - Checked by transcription: every line matches; "CBTO" is read as the letters C-B-T-O.
  - Pronunciation help: NOTOC = "No-tock", ID = "I D", PDF = "P D F".
- **Sound:**
  - Music: "Motivating Mornings" (Mixkit, free licence), low and ducked under the voice.
  - SFX: soft taps and pops (edit-video pack).
  - Level: −14 LUFS, peak ≤ −1.5 dBTP.
- **Files:** `scripts20.py` (voiceover text), `vo20.py` (voice + word times), `plan_vN_*.py` (what shows when),
  `build20.py` (HyperFrames project + SRT + mix), `render_previews.sh`.

## Asset notes: missing or substituted
**1. FOCA**
- The **"Something is wrong" button is not in the deck's app screenshots** (slides 7–8).
  - Shown instead: a plain-text callout ("Tap ‘Something is wrong’, not shown in the deck screenshot") plus the
    phone-back-to-Security animation.
- The signed PDF on slide 12 is the deck's real TEST PDF; the zoom shows the filename (form name + Record ID) and
  "FOCA Checklist" in the PDF header.

**2. NOTOC**
- Slide 12 has a **Saved screen and a filename example, not a PDF view**. They are labelled "SAVED SCREEN · TEST
  RECORD" and "PDF FILENAME EXAMPLE"; the ring sits on the Record ID.
- "Something is wrong" uses the real button on slide 10.

**3. Acknowledgement of Receipt**
- The app screenshots **do not show the role or the items list** (the signer has to scroll up).
  - For "check your role / the items" (Situation A) and "scroll up and check each item" (Situation B), the video shows
    the paper form's items area from slides 7 and 13.
  - Labelled "PAPER FORM", with the callout "On the phone, scroll up…".
- "Tell Security before signing" is shown on the deck's DO/DON'T slide 20 with a callout.
- Slide 19 is a Saved screen and filename example, labelled as such.

**4. Search List**
- The app screenshot **shows only the name box**; the search details and items list are not on any app screenshot.
  These come from the paper form on slide 6, labelled "PAPER FORM", with the callouts "On the phone, scroll up…" and
  "‘Nil’ means nothing was found".
- **Slide 12 (listed in the brief for the items check) is the DO/DON'T slide**, not an items list. It is used for "tell
  Security before you sign" ("Read the details before signing").
- Slide 11 is a Saved screen and filename example, labelled as such.

**All decks**
- Only TEST data appears (TEST names, IDs, signatures and records).
- No live names, emails, links or QR codes were found in the slides, so nothing needed masking.

## Checks (v01 previews)
- `npx hyperframes check`: 0 errors on all four.
  - AOR has 2 warnings, both because slides 7 and 13 are shown twice in the same scene (intended).
- Snapshots of every scene were reviewed at phone size: `vN/sheets/snap1`, `snap2`.
  - Checked: framing, rings on buttons, captions clear of screen fields.
- Rebuild: `python3 vo20.py vN && python3 build20.py vN`, then `./render_previews.sh`.
  - Final (after approval): `render --quality high`, then `master_final.sh`, with the export names from the brief.
