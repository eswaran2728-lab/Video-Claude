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
