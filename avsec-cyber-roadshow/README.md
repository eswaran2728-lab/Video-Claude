# AVSEC Cyber Roadshow — "Thank You, Allstars" recap

35-second, 9:16 (1080 × 1920) motion-graphics video for the AirAsia AVSEC booth, built with [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP rendered to MP4).

- **Video:** `renders/avsec-cyber-roadshow-PREVIEW.mp4`. It's called PREVIEW only because the Allstars logo file hasn't been added yet.
- **Storyboard:** `STORYBOARD.md` · **Review notes:** `REVIEW.md` · **Preview stills:** `stills/`

## The two leaderboards (13–25 s)

| Board | Shown as | Source |
| --- | --- | --- |
| **Spot the Risk challenge** (13–19 s) | The real booth screen. Your three screenshots are joined into one board that opens on the top 3, then scrolls | `assets/leaderboard/screens/1.png`, `2.png`, `3.png` |
| **Human Firewall video quiz** (19–25 s) | Typeset in the quiz's own style: the 19 rows from your screenshots, opening on the top 3, then scrolling | `videoQuiz` in `data/leaderboard.js` |

Both boards keep their own ranking rules. Spot the Risk ranks by highest points, then fastest time. The quiz shows each name once with its best score, highest first.

## Update and rerender (2 steps)

1. Edit **`data/leaderboard.js`**:
   - `leaderboardScreenshots`: the Spot the Risk screenshots, top of the board first. To use newer ones, replace the files in `assets/leaderboard/screens/` or list new paths. On every render they're joined automatically: the header comes from the first screenshot, rows that appear twice are shown once, and a row cut off at the edge of a screenshot is completed.
   - `videoQuiz`: one line per quiz row, `{ rank: 1, name: "Sofian Akasah", score: "100%" }`. Add or remove lines freely; the board scrolls to fit.
   - `challengeUrl`: the public link that is printed and encoded in the QR. Set it to `""` to show the `[PUBLIC SPOT THE RISK LINK]` placeholder and hide the QR.
   - `logos`: see "Logos" below.

2. Rerender:

   ```bash
   npm install        # first time only
   npm run render
   ```

   The script joins the screenshots, prints what it is about to render, renders, sets the sound to −14 LUFS, and writes `renders/avsec-cyber-roadshow.mp4`. While a logo or the link is still a placeholder, the file is called `…-PREVIEW.mp4`. If the URL points at a host or organizer page, the script stops.

   Optional check: `python3 scripts/verify_render.py renders/avsec-cyber-roadshow.mp4` confirms the size, frame rate and length. It also reads the QR code from the finished video and checks that it matches `challengeUrl` for at least 4 seconds (needs `pip install zxing-cpp pillow`).

Requirements: Node 22+, FFmpeg, Python 3 with Pillow (`pip install pillow`), and Chrome Headless Shell (`npx hyperframes browser ensure`). To look at frames or edit timing visually, run `npm run preview`.

## Verified sources

| Item | Value | How it was verified |
| --- | --- | --- |
| Public participant link | `https://airasia-avsec-spot-the-risk.vercel.app/play` | The host page builds it as `origin + '/play'`, and the official booth QR decodes to the same URL |
| Game title | Spot the Security Risk (shown as "Spot the Risk", per the brief) | Host and play page headers |
| Spot the Risk results | Your screenshots of the booth leaderboard | Match the game's live leaderboard data (27 Oct 2026) |
| Video quiz results | Your screenshots of the quiz leaderboard (#1–#19) | Names, scores and order match the quiz's live data (27 Oct 2026) |

The host and organizer URLs are not shown or encoded anywhere.

## Logos

The logos appear in full (never cropped) at the top of the opening and in the end-card footer. They are set in the `logos` part of `data/leaderboard.js`:

| Logo | Status | File |
| --- | --- | --- |
| AVSEC badge | **In the video.** Supplied by the client. The only change is that the black area outside the shield was made transparent; the badge artwork is untouched | `assets/logos/avsec.png` |
| AirAsia Allstars "Dare to Dream" | **File needed.** A dashed `[ALLSTARS LOGO]` slot shows until it's added | `assets/logos/allstars.png` |

To add the Allstars logo, save the PNG (a transparent background is best) as `assets/logos/allstars.png`. Then set `allstars: "assets/logos/allstars.png"` and run `npm run render`. Set a logo to `null` to leave it out entirely. The render stops with an error if a logo path points to a missing file.

## Audio and licences

- **Music:** an original instrumental composed in code for this video (`scripts/make_music.py`, 120 BPM). It is owned outright, and `npm run music` regenerates it. To use a licensed track instead, replace `assets/audio/music.wav` and keep the same name.
- **Sound effects:** from the HyperFrames bundled library, under the Pixabay Content License (commercial use, no attribution required). See `assets/sfx/CREDITS.md`.
- **Fonts:** Inter and JetBrains Mono (both SIL OFL), bundled with HyperFrames.
- **Libraries:** GSAP 3.14.2 and qrcode-generator 1.4.4 (MIT), vendored in `assets/vendor/` so renders need no network.

## Files

```
data/leaderboard.js           ← the only file to edit: screenshots, quiz rows, link, logos
index.html                    root: scene order, music and sound-effect timing
compositions/s1-thanks.html   0–5 s   Thank you (scan reveal, logos)
compositions/s2-recap.html    5–10 s  Challenge recap (risk markers, shield)
compositions/s3-buildup.html  10–13 s Ranking build-up (podium)
compositions/s4-reveal.html   13–25 s The two leaderboards
compositions/s5-together.html 25–29 s Collective thank you
compositions/s6-invite.html   29–35 s Invitation (URL + QR, logos)
assets/leaderboard/           screenshots, the joined board.png and its geometry (board.js)
assets/js/helpers.js          logos, link and placeholder handling
scripts/stitch_board.py       joins the leaderboard screenshots
scripts/render.mjs            one-command render + loudness normalisation
scripts/make_music.py         original music bed
scripts/verify_render.py      checks the finished MP4 and its QR
```
