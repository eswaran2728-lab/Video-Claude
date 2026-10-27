# AVSEC Cyber Roadshow — "Thank You, Allstars" recap

35-second, 9:16 (1080 × 1920) motion-graphics video for the AirAsia AVSEC booth, built with [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP rendered to MP4).

- **Video:** `renders/avsec-cyber-roadshow-PREVIEW.mp4` — results are still placeholders, so the file and the rank cards say PREVIEW.
- **Storyboard:** `STORYBOARD.md` · **Review notes:** `REVIEW.md` · **Preview stills:** `stills/`

## Replace the leaderboard data (2 steps)

1. Open **`data/leaderboard.js`** and replace each `[BRACKETED]` value:

   ```js
   { rank: 1, name: "Sofian A.",   points: 1000, time: "16.2s" },
   { rank: 2, name: "Ruby Ruslan", points: 1000, time: "16.3s" },
   { rank: 3, name: "Fae",         points: 1000, time: "18.8s" },
   ```

   *(Example of the format only. Confirm the real results first; see "Ranking" below.)*

   - `rank` sets the order (1 = first place). Reveals always run 3 → 2 → 1.
   - `name`: long names wrap onto two lines automatically.
   - `points`: a number, so `1000` is shown as `1,000`.
   - `time`: only a real recorded completion time. Use `null` to hide the TIME box for that person.
   - `challengeUrl`: the public link that is printed and encoded in the QR. Set it to `""` to show the `[PUBLIC SPOT THE RISK LINK]` placeholder and hide the QR.
   - `logos`: see "Logos" below.

2. Rerender:

   ```bash
   npm install        # first time only
   npm run render
   ```

   The script prints the ranking, link and logos it is about to render, renders, normalises the sound to −14 LUFS, and writes `renders/avsec-cyber-roadshow.mp4`. While any result or logo is still a placeholder, the file is called `…-PREVIEW.mp4`, and placeholder results also put a red "PREVIEW · RESULTS PENDING" tag on the rank cards. If the URL points at a host or organizer page, the script stops.

   Optional check: `python3 scripts/verify_render.py renders/avsec-cyber-roadshow.mp4` confirms the size, frame rate and length, and decodes the QR from the finished video to make sure it matches `challengeUrl` for at least 4 seconds (needs `pip install zxing-cpp pillow`).

Requirements: Node 22+, FFmpeg, and Chrome Headless Shell (`npx hyperframes browser ensure`). To look at frames or edit timing visually, run `npm run preview`.

## Ranking (Spot the Security Risk)

The booth's live board ranks by **points (high to low), then fastest completion time**. Times are recorded per attempt (`durationMs`), and the video shows them with one decimal (for example, `16.2s`) so close finishes stay distinct.

Before you fill in the names, check two things:

- **The board lists every attempt** (players can tap "Play again"), so one person can appear more than once under different spellings.
- **The game was still open** when it was checked (27 Oct 2026, ~08:25 UTC).

`data/live-snapshot-2026-10-27.json` holds the raw top entries from that moment, with the open questions listed. The video does not read that file.

## Verified sources

| Item | Value | How it was verified |
| --- | --- | --- |
| Public participant link | `https://airasia-avsec-spot-the-risk.vercel.app/play` | The host page builds it as `origin + '/play'`, and the official booth QR decodes to the same URL |
| Game title | Spot the Security Risk (shown in the video as "Spot the Risk", per the brief) | Host and play page headers |
| Scoring | 10 questions × 100 points = 1,000 max | Play page |

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
data/leaderboard.js          ← the only file to edit for results and link
index.html                   root: scene order, music and sound-effect timing
compositions/s1-thanks.html  0–5 s   Thank you (scan reveal)
compositions/s2-recap.html   5–10 s  Challenge recap (risk markers, shield)
compositions/s3-buildup.html 10–13 s Ranking build-up (podium)
compositions/s4-reveal.html  13–25 s Top three (reusable rank card)
compositions/s5-together.html 25–29 s Collective thank you
compositions/s6-invite.html  29–35 s Invitation (URL + QR, from the data file)
assets/js/helpers.js         formatting, auto-fit and placeholder detection
scripts/render.mjs           one-command render + loudness normalisation
scripts/make_music.py        original music bed
```
