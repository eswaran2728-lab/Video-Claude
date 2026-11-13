# மகாகுரு / Mahaguru – short film edit

Edit of the *Mahaguru Higgsfield Production Bible* (v1.0) using the 39 shots + title/dedication plates generated in Higgsfield (Seedance 2.0).

Rebuild:
1. `python3 dl.sh`-style download of each latest take listed in `shots.json` into `raw/`, then upscale to `film/assets/video/` (1920×1080, lanczos).
2. `SSL_CERT_FILE=/root/.ccr/ca-bundle.crt python3 tools/make_voice.py` – Tamil narration/dialogue from `lines.json` (Microsoft Tamil neural voices via edge-tts).
3. `python3 tools/musicgen.py` – temporary score cues (MusicGen-small).
4. `python3 build_film.py && python3 mix_audio.py && python3 build_film.py`
5. `cd film && npx hyperframes check && npx hyperframes render --quality delivery -o renders/Mahaguru_master.mp4`

`Mahaguru_Tamil.srt` – Tamil subtitles. Voices and score are temporary (demo) – replace with recorded Tamil narrator/cast and the real song before release.
