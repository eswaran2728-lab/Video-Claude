# Persatuan Silambam Daerah Sepang × Karate R. Tiagarajan — photo montage (HyperFrames)

- Source photos: `.DNG` files are actually JPEG (iPhone 16 Pro Max, 8064×4536); originals untouched in `orig/`, browser copies in `work/` (not committed).
- Build: `python3 build.py` → `edit/index.html` (sequence, beat-snapped boundaries, titles, leaks).
- Preview: `cd edit && npx hyperframes preview` (Studio) or `npx hyperframes render -q draft`.

## Replacing the TEMP music
1. Put the licensed song (e.g. "Mustafa Mustafa") at `edit/assets/music_TEMP.wav` **or** change `src` of `<audio id="music">` in `index.tpl.html`.
2. Trim it to the chosen section (≈42 s) first, e.g. `ffmpeg -ss <start> -t 42 -i song.mp3 -af afade=t=out:st=39.3:d=2.7 edit/assets/music_TEMP.wav`.
3. `cd edit && npx hyperframes beats .` then `cd .. && python3 build.py` — photo changes re-snap to the new beats.
