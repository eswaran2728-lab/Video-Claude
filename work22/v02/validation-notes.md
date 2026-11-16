# v02 validation notes
Status: DRAFT PREVIEW, not approved; no final export. v01 kept unchanged.

Owner's message for this clip: "Showing my new statue" (speech itself is not intelligible to transcription).
Assets: analysis/segment.py (statue cut-out: colour seeds + manual seeds + OpenCV GrabCut) -> analysis/statue_alpha.png;
analysis/make_v02_assets.py -> statue_colour.png, statue_grey.png (generated layer-line 'printed' look, a visual effect),
toolpath.png (slicer-style hologram), wire.png (edge wireframe), bg_clean.jpg (statue inpainted out, defocused), statue_rows.json (nozzle path).
Grade: same LUT as v01 (grade.cube) baked into hero_graded.jpg / statue_colour.png / bg_clean.jpg / turn.mp4.

Checks: lint 0 errors; snapshots of every beat; draft render 17.1 s, 1080x1920, decodes clean, -15.9 LUFS, peak -1.0 dBFS; crossfade into end card checked by frame brightness.
Not verified: audio never listened to; motion judged from stills; cut-out has small leftovers (a few px of shirt/hand near the sword hilt and right arm).
