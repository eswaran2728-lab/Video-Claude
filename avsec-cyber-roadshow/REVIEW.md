# Review — AVSEC Cyber Roadshow recap

## Status

**PREVIEW.** The film is finished. These items are still pending:

1. **Top-three results.** The brief's placeholders are kept on purpose. The live Spot the Security Risk board was still open when checked and lists every attempt, so "Ruby Ruslan" (#2) and "Ruby" (#3) may be the same person. That means the ranking is not yet reliable. Raw entries: `data/live-snapshot-2026-10-27.json`.
2. **Allstars logo file.** It was sent as an image in chat, which doesn't reach the build machine as a file. A marked `[ALLSTARS LOGO]` slot holds its place at the opening and on the end card.

## Measured on the final MP4

| Check | Result |
| --- | --- |
| Format | 1080 × 1920, 30 fps, 1,050 frames = 35.00 s, H.264 + AAC |
| Loudness (after AAC encode) | −14.0 LUFS integrated, −1.2 dB peak |
| QR destination | Decoded from the encoded video at 30.4, 30.6, 31.5, 32.5, 33.5, 34.5 and 34.9 s → `https://airasia-avsec-spot-the-risk.vercel.app/play` every time, also at half resolution |
| QR hold | Readable and static from 30.4 s to the end (4.5 s) |
| Host/organizer URLs | Not present anywhere in the video or the QR |
| `hyperframes check` | Passes: 0 errors, 0 warnings (lint, runtime, layout, contrast, craft) |
| Copy | Matches the brief word for word (checked against STORYBOARD.md) |

## Looked at (contact sheets and full-size frames)

- Opening scan reveal, each rank card (including stress tests with a 22-character name, a hidden time and an empty URL), the collective thank-you, and the QR end card. Checked at 1080 × 1920 and at 360 px phone width.
- Every word of copy sits between y 170 and 1330 px, clear of phone/app UI. Exception: the end-card logo lockup (y 1384–1574) and the footer line (y 1600) are lower. They are fully in frame but could be partly covered by a social app's caption bar. They are brand marks, not information.

## Creative calls

- **Light/dark rhythm:** dark scan → light recap → dark podium → red flood for 1st → light thank-you → dark invitation. Each switch lands on a bar line with a hit.
- **First place:** the whole ground floods red, the card turns white with red numerals, and confetti launches from *behind* the card, so it can never cover a name.
- **Inclusivity beat:** the three names make room for "To every Allstar who took part: thank you." A row of abstract dots stands for everyone else. It is not a count and implies no number.
- **Challenge recap:** abstract line icons (USB stick, password sticky note, unattended badge, etc.), not screenshots. The game's real photos are behind the play flow, so none were adapted.
- **Copy:** exactly as briefed. Interface micro-labels were added (`SCAN 100%`, `● ALLSTARS DETECTED`, `RISK`, `SCAN TO PLAY`, place labels, `AVSEC BOOTH · CYBER ROADSHOW`). The brief's "Spot the Risk" is kept, although the game's own header says "Spot the Security Risk".

## Not checked

- **The sound was measured, not heard.** The music is composed in code (`scripts/make_music.py`). Its band balance and sections were checked by analysis (low-end share ~65%, breakdown within 2 dB of the groove, no stray tones). Have someone listen once on a phone speaker. To swap in a licensed track, replace `assets/audio/music.wav`.
- The render used local Chrome, not Docker. Fonts are the HyperFrames-bundled Inter and JetBrains Mono, so they should match elsewhere.

## Weakest shot / with more time

- **Shot 3 (podium, 10–13 s)** is the plainest frame. With more time: real depth on the podium (a lit top face) and a slower, longer spotlight cross.
- The recap icons are generic by design. If you're cleared to use the game's real photos, the recap could zoom into one of them instead.
