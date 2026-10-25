# AVSEC keychain reel — Eshan Creations (work7)

Source: 9 clips in the Drive folder (ProRes 4K HLG + HEVC, iPhone). `make_proxies.sh` streams each original from Drive
into a 1080x1920 SDR proxy (HLG -> BT.709 Hable tone-map); originals stay on Drive. Preview: `PREVIEW_avsec_keychains_v01.mp4`.

## Story (35.5 s, 1080x1920, 30 fps)
Hook (plate of red AVSEC planes slides out of the printer, "50 CUSTOM KEYCHAINS") -> why (company giveaway, 50 pcs)
-> design (multi-colour) -> 3 colours red/black/white -> design + packaging done, ready to deliver -> bulk orders, DM
-> Eshan Creations end card.

Speech is Tamil; captions are an English translation (Whisper large-v3 `translate` + `en`, both agreeing).
Cut: 6358 20.0–34.8 (where he works — transcription uncertain, repeats the giveaway point), 6358 42–44.8
("Claude, later cut this one"), 3437 0–6.1 (repeats "50 pieces"), 3437 12.9–21.5 (second CTA; the 4K one is used).

Files: `edl.py` (speech + visual EDL), `make_assets.py` (clips + denoised/normalised dialogue), `mix_music.py`
(ducked bed), `build.py` -> `edit/index.html` (timing map `edit/timing_map.json`, SFX cues `edit/cues.json`),
`gen_bgm.py` (local MusicGen-small bed, AI-generated placeholder), `grade_attr.txt`.
Render: `cd edit && npx hyperframes@0.8.193 render . --quality draft`, then 2-pass loudnorm to -14 LUFS.

## v02 — cinematic colour + lighting
- `relight.py` (edit/assets/v -> edit/assets/vc): face shots get a CSRT-tracked warm key light on the face, torso and
  keychain table kept lit, background shelves fall into shadow; product b-roll gets a warm pool of light with darker
  edges; soft highlight roll-off. Face paths in `edit/assets/vc/face_track.json`.
- Grade `grade_cine_attr.txt`: contrast +0.14, highlights −0.12, blacks −0.06, teal shadows / amber highlights
  (wheels), vignette 0.22, grain 0.05. Warm light leaks on the hook→speaker cut and into the end card.
- Split panes are pre-cropped (`V4_top`, `V4_faceC`): the grading wrapper ignores `object-position`, which had
  dropped the face out of the lower pane in v01.
- Build: `python3 build.py` (v02, default) or `VERSION=v01 python3 build.py`.

## v03 — background noise removed, gentler face light
- `denoise.py`: spectral noise reduction per speech clip (noise profile from the quietest 15% of frames, Wiener-style
  gain with floor + smoothing, pauses lowered further) -> `edit/assets/clean_*.wav`. Dialogue noise floor
  -33 dB -> -56 dB with speech level unchanged; re-transcription of the cleaned audio is as complete as the original.
- `relight.py` v03 (`edit/assets/vc3`): face key light 0.36 -> 0.10, warmth 0.06 -> 0.025, background falloff softer.
- Caption "I'll deliver them to you" -> "I'll deliver them" (models disagree: "to you" vs "tomorrow").
- Build: `VERSION=v03 python3 make_assets.py && VERSION=v03 python3 relight.py && python3 build.py` (v03 default;
  `VERSION=v02` / `VERSION=v01` rebuild earlier versions).
