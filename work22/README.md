# work22 — painted statue showcase reel (new media set, 16 Nov 2026)

Source: one clip in the Drive folder, `A001_11152346_C016.mov` (Blackmagic Camera on iPhone, 2160x3840 portrait, 24 fps, Rec.709, 57 s). Not in git.
Usable picture: 0.00–1.80 s (statue presented, then turned). After ~2 s the camera is moved around the room; not used. No intelligible speech (Whisper only produced hallucinated text in Tamil/English/Malay), so no captions.

- `build.py` — builds `vNN/index.html` from `vNN/edit-plan.json` (stills zoomed about anchor points, print/paint reveal, callouts, titles, end card).
- `grade.py` — the colour grade as a 3D LUT (`vNN/grade.cube`), baked into stills and the video proxy with ffmpeg `lut3d`.
- `audio.py` — original synthesized music (drone, percussion, bells) and effects; no third-party audio.
- `v01/` — first preview. Rebuild: `python3 grade.py v01/grade.cube`, re-bake assets (commands in v01/validation-notes.md), `python3 build.py v01 && python3 audio.py v01`, then `npx hyperframes render --quality draft` in v01.
