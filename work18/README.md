# Movie-scene recreation promo (9:16)

1080x1920, 30 fps, 73.2 s, HyperFrames 0.8.193. **Current: v01 preview** (`PREVIEW_movie_scene_promo_v01.mp4`, 720x1280).
No final export has been made and nothing is published.

## Sources (creator)
- `src/original_scene_2.44.44PM.mp4`: the original movie-scene clip, a TikTok repost with its watermark and creator handle.
  - Used from 0 to 17.4 s. After 17.4 s it shows the TikTok logo end card, which is cut.
- `src/recreated_3.14.20PM.mp4`: the creator's recreation, used in full (32.17 s).

## Edit (`build18.py`; clips prepared by `prep_clips.sh`; sound by `mix18.py`; voice by `vo18.py`)
| time | part |
|---|---|
| 0–4.4 | Intro MG + AI voice: "Check this out! This is the original scene from the movie." ("THE ORIGINAL / MOVIE SCENE", "▼ Watch this first") |
| 4.4–21.8 | The original scene with its own song, in a gold-edged card over a blurred copy; "ORIGINAL SCENE · FROM THE MOVIE"; "NEXT: MY VERSION ▶" in the last 3 s |
| 21.8–26.0 | MG + voice: "Now… I recreated this exact scene, just for me!" (gold punch-in, sparkles) |
| 26.0–58.2 | The recreation, in full, with its own song; "MY RECREATION"; "WANT YOURS? RM20 per video" sticker in the last 8 s |
| 58.2–73.2 | CTA MG + voice: "WANT YOUR OWN VERSION?" → "DM ME" → "ONLY RM20 PER VIDEO" badge → "PROMO · TODAY & TOMORROW ONLY" with Thu 12 / Fri 13 Nov 2026 date cards → "DM ME NOW · OFFER ENDS 13 NOV" |

- **Voice:** Kokoro af_heart, speed 1.05 (on the device). Checked by transcription: "RM20" is read as "R M twenty".
- **Sound:**
  - Each clip's own song is at full length, normalised to −14 LUFS so both play at the same level.
  - Music "What About Action?" (Diego Nava, Mixkit #474, Mixkit Stock Music Free License) only under the MG parts,
    ducked under the voice.
  - SFX (edit-video pack, Apache-2.0) on wipes and reveals.
- **Checks:**
  - Loudness by part: −14.0 / −13.7 / −13.9 / −14.1 / −14.3 LUFS.
  - Full decode with 0 errors; audio lag 0 ms; `hyperframes check` 0 errors.
- **Notes:**
  - The original clip shows another TikTok creator's watermark and handle; it is shown as supplied.
  - No contact handle was given, so the CTA says "DM me".

## v02: creator's notes ("hide that tiktok name" + "blur the women face in the second") → final
- **`privacy18.py`, TikTok watermark:** the TikTok logo and "@handle" in the original clip are blurred where they sit
  (top-left 0–5.0 s, bottom-right 5.0–17.4 s) → `src/original_clean.mp4`.
- **`privacy18.py`, the woman's face in the recreation:**
  - Tracked with MediaPipe BlazeFace on every frame (`detect_faces.py`, `faces_raw.json`) through her shot (12.07–24.1 s).
  - The track is smoothed separately on each side of the camera cut at 21.6 s, and gaps are filled.
  - From 15.8 s, while she turns (no detection), the first detection is held.
  - Blur: feathered ellipse, 1.6x the face box → `src/recreated_faceblur.mp4`.
  - Checked frame by frame around the cut: `sheets/faceblur_check.jpg`.
- **Rebuild:** `prep_clips.sh` now builds the clips from those files; the composition and sound are unchanged.
  - Preview `PREVIEW_movie_scene_promo_v02.mp4`; v01 is kept.
