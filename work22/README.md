# RevLog explainer (HyperFrames)

Landscape explainer, 1920×1080, 30 fps, 4:00, narrated by one local AI voice with word-for-word captions.

- Screenshots: `src/unz/revlog screenshot/` (from the supplied ZIP). Not committed.
- Final: `video/RevLog_explainer_1920x1080.mp4`, with `video/narration.md`, `video/captions.srt` and `video/credits.md`.

## Manifest checks (rule 1)
- 86 manifest entries: 82 screenshot files and 4 mock-up entries.
- All 82 listed files exist. No unlisted PNG is in the folder; the leftover `staff-09-bike-opens-without-code.png` is not in the ZIP.
- The video uses 64 of the 82 screenshots.

## Build
```
python3 ocr22.py        # word boxes on every screenshot (tesseract) -> ocr.json, used only to place rings and magnifiers
python3 vo22.py         # HyperFrames tts (Kokoro-82M af_heart, 0.87) per line + word times (faster-whisper) -> timing.json
python3 build22.py      # timeline from the measured voice -> project/index.html, video/captions.srt, layout.json
python3 mix22.py        # voice + ducked music + quiet SFX -> project/assets/mix.wav
cd project && npx hyperframes@0.8.193 render --quality high --fps 30 -o ../video/RevLog_explainer_1920x1080.mp4
```
`plan22.py` holds every narration line and its shot.
- Each line has rings and magnifiers on real UI positions (OCR or measured boxes in the screenshot's own pixels).
- Camera mock-ups are drawn in HTML with made-up data and a "Sample" tag. Their QR codes encode only `REVLOG-SAMPLE`.

## Not available here
The RevLog project (`docs/v2/*.md`, `lib/theme/tokens.dart`, app icon) was not reachable from this session:
- it was not in the ZIP;
- no computer folder was shared;
- attaching the `revlog` repository was not permitted.

So the colours are the tokens given in the brief, plus values measured from the screenshots:
- `#03DAC6` accent;
- `#8D9AE9` stamp blue;
- `#BB86FC` workshop purple.

The flows follow the brief and the screenshots. Corner sizes are chosen to suit the frame. The closing shows the wordmark only, because no app icon was available.
