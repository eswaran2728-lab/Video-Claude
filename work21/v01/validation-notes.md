# v01 validation notes

Status: DRAFT PREVIEW — not approved, no final export made.

## Source facts (read from the footage)
- Stage banner: "Sambutan Hari Deepavali / தீபாவளி கொண்டாட்டம் / Peringkat Negeri Selangor 2026 / 14 November 2026 (Sabtu) / 6.00 PTG – 11.30 MLM / Dataran Klang @ Padang Chetty, Klang".
- Performers' shirts read "SILAMBAM" on the back (c06 ~21.6 s). Team / school name is not readable and is not used.
- No speech: whisper found no usable words in three test clips, so there are no captions, only titles.
- Sources are 848x478. c05, c10, c13 are 30 fps and ~6 dB quieter (a second, wider recording); the rest are 24 fps.
- Several clips carry overlapping stretches of the same soundtrack (c02→c06→c09, c11→c04) while showing different action, so the audio is not locked to the picture. The reel uses one clip's audio (c12, 0–45.5 s) unbroken.

## Proxies
`ffmpeg -i source/cNN.mp4 -an -vf "scale=1696:956:flags=lanczos,unsharp=5:5:0.6,fps=30" -c:v libx264 -crf 14 -g 15`

## Checks run
- `hyperframes lint`: 0 errors; warnings are the "move into a sub-composition" structure advice (titles live in the root file).
- Snapshots of every shot and the end card inspected for framing, text fit and Tamil glyph rendering.
- Draft render probed for duration, size and loudness (see delivery message).

## Not verified
- Audio was not listened to (no playback here). Levels and structure only. Whether the soundtrack is a commercial song is unknown.
- The three synthesized accents (boom on the leap and takedown, whoosh on part changes, chime on the end card) are unheard.
- Motion was judged from still frames, not watched at speed.
