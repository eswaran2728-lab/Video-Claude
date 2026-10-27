# Review — AVSEC Cyber Roadshow recap

## Status

**Final.** Both client logos are in: the AVSEC badge and the Allstars "Dare to Dream" logo. Each is shown whole at the top of the opening and in the end-card footer. For each, only the plain background outside the artwork was made transparent; the artwork is untouched.

## Rankings (changed on request)

The client asked for the real leaderboards instead of one-by-one name reveals:

- **Spot the Risk challenge (13–19 s):** the client's three booth-screen screenshots, joined by `scripts/stitch_board.py` into one board of rows 01–20. The header comes from screenshot 1. Rows that appear in two screenshots are kept once, using the complete copy, so the browser scrollbar in screenshot 1 doesn't show. Row 12, cut off at the bottom of screenshot 2, is completed from the identical row box above it; only empty row background is borrowed, never text.
- **Human Firewall video quiz (19–25 s):** the four quiz screenshots arrived only as chat images, not files. The 19 rows (#1–#19) are typeset in the quiz's own navy and yellow style from those screenshots. Names, percentages and order were checked against the quiz's own data.
- Each board opens on its top 3 (white brackets, `TOP 3` tag, red flood, confetti *behind* the panel), then scrolls so every row is shown.

## Measured on the final MP4

| Check | Result |
| --- | --- |
| Format | 1080 × 1920, 30 fps, video and audio both exactly 35.000 s, H.264 + AAC |
| Loudness (after AAC encode) | −14.0 LUFS integrated, −1.2 dB peak |
| QR destination | Read from the encoded video at 30.4, 30.6, 31.5, 32.5, 33.5, 34.5 and 34.9 s → `https://airasia-avsec-spot-the-risk.vercel.app/play` every time, also at half resolution |
| QR hold | Readable and static from 30.4 s to the end (4.5 s) |
| Host/organizer URLs | Not present anywhere in the video or the QR |
| Leaderboards | Spot the Risk rows 01–20 and quiz #1–#19 all appear, in order, in the encoded frames |
| `hyperframes check` | Passes: 0 errors, 0 warnings |

## Looked at (contact sheets and full-size frames)

- The opening, both leaderboards (top-3 lock and scrolled ends), the collective thank-you and the QR end card. Checked at 1080 × 1920 and at phone width.
- Every word of copy sits between y 170 and 1330 px. The exception is the end-card logo lockup and footer (y 1384–1630): fully in frame, but low enough that a social app's caption bar could cover part of it.
- The board text from the screenshots is about 30 px tall on a 1080-wide frame: readable full-screen on a phone, small in a feed thumbnail. Pausing shows every name.

## Creative calls

- **Light/dark rhythm:** dark scan → light recap → dark podium → red flood on each top-3 lock → light thank-you → dark invitation. Each switch lands on a bar line.
- **Inclusivity:** both boards scroll to their last row, so every listed player gets screen time. "To every Allstar who took part: thank you." follows straight after.
- **Challenge recap:** abstract risk icons, not screenshots of the game's photos.
- **Copy:** exactly as briefed. Interface labels were added (`SCAN 100%`, `● ALLSTARS DETECTED`, `RISK`, `TOP 3`, board titles, `SCAN TO PLAY`, `AVSEC BOOTH · CYBER ROADSHOW`). "Spot the Risk" is used as in the brief; the game's own header reads "Spot the Security Risk".

## Not checked

- **The sound was measured, not heard.** The music is composed in code. Its band balance and sections were checked by analysis. Have someone listen once on a phone speaker. To swap in a licensed track, replace `assets/audio/music.wav`.
- The render used local Chrome, not Docker. Fonts are the HyperFrames-bundled Inter and JetBrains Mono.

## Weakest shot / with more time

- **Shot 3 (podium, 10–13 s)** still teases "1 · 2 · 3" before boards that are lists. With more time, the podium could turn into the first board.
- With the quiz screenshots as files, the quiz board could use the real images like the Spot the Risk board does.
