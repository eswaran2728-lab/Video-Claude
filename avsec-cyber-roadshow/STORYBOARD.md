# AVSEC Cyber Roadshow — Thank-You Recap · Storyboard

35 s · 1080 × 1920 (9:16) · 30 fps · MP4 · no voiceover · reads with sound off

## Verified facts this film relies on

| Fact | Source | How verified |
| --- | --- | --- |
| Game title: **Spot the Security Risk** (user copy says "Spot the Risk") | Host + play page header | Page HTML |
| AirAsia AVSEC Cybersecurity Awareness Challenge · 10 photos · 3 levels · 100 points each (max 1,000) | Play page | Page HTML |
| Ranking: highest points, then fastest completion time | Leaderboard API order (`score` desc, `durationMs` asc) | API response |
| Completion time is a real recorded value (`durationMs`) | Leaderboard API | API response |
| Public link: `https://airasia-avsec-spot-the-risk.vercel.app/play` | Host page script (`origin + '/play'`) and official booth QR | QR decoded with zxing |
| Human Firewall quiz: separate board, score /10, no recorded time, 11 people tied on 10/10 | Organizer API | API response |

Not used: the host and organizer URLs (never shown or encoded), and any participant count or statistic.

Logos (supplied by the client during the build): the AVSEC badge is in the video. The AirAsia Allstars "Dare to Dream" logo has a marked slot that fills in once its file is added.

**Ranking status: not final.** The game was still open when checked, and the board lists every attempt, so the same person may appear twice (e.g. "Ruby Ruslan" and "Ruby" in places 2 and 3). The delivery render uses the placeholders from the brief; `data/live-snapshot-2026-10-27.json` holds the raw top entries for you to confirm.

## Look

- Palette: AirAsia-inspired red `#E8112D` / signal red `#FF2D3F` on dark, white `#FFFFFF`, charcoal `#141417`, deep `#0A0A0C`, paper `#F4F2EF`. No yellow, no gradients-as-decoration.
- Type: Inter 900 for kinetic display (tight −0.045em), Inter 700 for supporting lines, JetBrains Mono for interface micro-labels and all numbers (tabular).
- Cyber cues: scan line, corner brackets, target reticles, detection tags, faint 60 px grid. Aviation cues: runway centre-line dashes, boarding-pass perforation on the rank cards.
- Light/dark switches land on the bar line with a hit: dark → **light** (5 s) → dark (10 s) → red flood for 1st (20.2 s) → **light** (25 s) → dark (29 s).
- Text band: every word between y 170 and 1330 px so phone/app UI never covers it.

## Shots

Times in seconds. Music is 120 BPM: one beat = 0.5 s, one bar = 2 s.

### 1 · Thank you — 0.0–5.0 (dark)

| t | Picture | Sound |
| --- | --- | --- |
| 0.0 | Frame 0 (thumbnail): deep charcoal, grid, corner brackets, a red scan line at the top edge, and the headline as a dim outline waiting to be scanned. | Pad swells, soft digital scan texture |
| 0.15–0.3 | The scan passes the top of the frame and reveals the logo lockup: AVSEC badge │ Allstars logo, each shown whole. | |
| 0.1–1.2 | Red pulse travels down the frame (`power2.inOut`). As it passes, it uncovers **THANK YOU,** (white) then **ALLSTARS!** (red), 190 px Inter 900. Scan counter runs to 100%. | Kick enters on beat 2 |
| 1.25 | Reticle brackets snap onto ALLSTARS! (`back.out`), tag `● DETECTED: ALLSTARS` | pop |
| 1.8–2.3 | "For joining us at the AVSEC booth" words blur in 0.07 s apart (58 px). | |
| 2.6 | "Cyber Roadshow" lands as a red-outlined event tag with a runway dash rule drawn under it. | soft click |
| 2.8–4.6 | Hold. Background grid drifts; scan line idles at the bottom. | Groove |
| 4.6–5.0 | Scan line sweeps back up fast, everything blurs out behind it. | whoosh |

### 2 · Challenge recap — 5.0–10.0 (light)

| t | Picture | Sound |
| --- | --- | --- |
| 5.0 | Hard switch to paper white. A 3 × 3 field of abstract line icons (laptop, badge, USB stick, sticky note, door, phone, suitcase, cup, monitor) draws in. | Drop: full groove |
| 5.3 / 5.8 / 6.3 | A crosshair cursor flicks between three icons, locking each with a red box + `RISK` tag (USB, sticky note, unattended badge). | pop × 3 (rotating takes) |
| 5.6 | **You spotted the risks.** lands above the grid, "risks." in red, 104 px. | |
| 7.3–7.8 | Icons collapse into the centre; a shield outline draws on (stroke) and fills red. | whoosh |
| 7.8 | **You strengthened the human firewall.** "human firewall." in red; shield sits above it with a white check. | |
| 9.6–10.0 | Shield turns charcoal and scales past the frame — its fill becomes the next scene. | whoosh-cinematic tail |

### 3 · Ranking build-up — 10.0–13.0 (dark)

| t | Picture | Sound |
| --- | --- | --- |
| 10.0 | Charcoal. Three podium blocks rise from the bottom with a physical overshoot (2 · 1 · 3), outline numerals. | Drums thin to kick + filter sweep |
| 10.3 | **OUR TOP RANKERS** slams in word by word (124 px). | |
| 10.8 | **AVSEC BOOTH CHALLENGE** tracks open in red mono (44 px). | |
| 11.2–12.6 | Two soft spotlight cones sweep across the podium and cross on #1. | riser (peak 12.9) |
| 12.6–13.0 | Lights dim to near black — the held breath before the payoff. | Drop-out |

### 4 · Top three — 13.0–25.0

One reusable card (boarding-pass style): rank numeral, place label, name, POINTS, TIME. Numbers are static from the moment they land until the card leaves.

| t | Picture | Sound |
| --- | --- | --- |
| 13.0–13.4 | **3rd** card rises in from below with motion blur, lands. "03" slams. | impact |
| 13.5–14.0 | Red scan line passes over the card revealing name, then points and time. | scan tick |
| 14.0–16.4 | Hold — dead still (2.4 s). | Groove |
| 16.4–16.7 | Card whips up and out; **2nd** card arrives the same way. | whoosh + impact |
| 17.4–19.9 | Hold (2.5 s). | Swell begins under it |
| 20.2 | Colour flood: the whole ground turns red. **1st** card arrives white with charcoal type and red numerals — the strongest reveal. | Big impact + sparkle, full groove |
| 20.6–21.3 | Name and numbers reveal; red/white confetti bursts from *behind* the card (never over the name). | |
| 21.3–24.7 | Hold (3.4 s). | |
| 24.7–25.0 | Card shrinks toward the centre as the ground goes white. | whoosh |

### 5 · Collective thank you — 25.0–29.0 (light)

| t | Picture | Sound |
| --- | --- | --- |
| 25.0 | The three names arrive together as compact rows (01 · 02 · 03) at the top. | Breakdown: warm chords |
| 26.0 | **To every Allstar who took part: thank you.** — per-word, 84 px; "thank you." in red. A row of small abstract dots (not countable as a statistic) spreads out under the names to say "everyone". | |
| 27.1 | **Stay alert. Stay cyber safe.** in red, below. | soft click |
| 27.1–29.0 | Hold. | |

### 6 · Open invitation — 29.0–35.0 (dark)

| t | Picture | Sound |
| --- | --- | --- |
| 29.0 | Hard switch to charcoal. **Missed the booth?** slams in. | Final chorus |
| 29.5 | **Try the Spot the Risk challenge.** | |
| 29.9–30.5 | White QR card scales up and settles; corner brackets lock on. Label `SCAN TO PLAY`. URL below in mono. | pop |
| 30.6 | **Think you can spot them all?** in red. | |
| 30.95 | Logo lockup rises into the footer (AVSEC badge │ Allstars logo), then `AVSEC BOOTH · CYBER ROADSHOW`. | |
| 30.6–35.0 | Everything static (QR held 4.5 s+). | Uplifting resolve on the tonic, ring-out to 35.0 |

## Sound plan

Original instrumental composed in code for this film (120 BPM, D major, I–V–vi–IV) — owned outright, no licence needed. Effects are from the HyperFrames bundled library (Pixabay Content License: commercial use, no attribution required; see `assets/sfx/CREDITS.md`). Mix target −14 LUFS, true peak ≤ −1 dBTP, measured on the encoded MP4.
