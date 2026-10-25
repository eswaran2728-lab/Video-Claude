# 32. Vertigo

Original construction recipe; numerical values below are starting points, not seller settings.

## Inputs and prerequisites
Use the approved timeline, source clip, selected font and palette. Additional requirement: depth separation or appropriate source camera motion. Confirm source media and the renderer support this requirement before promising the effect.

## Construction
Combine foreground scale compensation with increasing background scale or simulated depth; preserve the face dimensions.

## Timeline and animation
Build slowly over 1.5–2.5 seconds. Use output seconds and convert to frames with `round(seconds * fps)`. Clamp keyframes to the effect interval. Use cubic ease-out for entry and ease-in for exit; preserve linear motion for scans and rolling values. Keep audio continuous unless the edit decision list explicitly changes it.

## Layer and parameter contract
Create layers in this order where relevant: background media, wall or scene graphic, subject matte, explanatory overlay, captions, brand mark. Keep the logo and subtitles outside the effect group. Start with intensity 0.6, offset 0 seconds from the approved cue, and a maximum of one dominant effect at a time. At 1080 × 1920, reserve x=90–930 and y=180–1540 for essential information; validate against the destination UI.

## Implementation decision
Use HTML/CSS/SVG for flat type, cards and paths; use a verified canvas/WebGL/3D implementation for depth, particles and refraction. Precompute masks and tracking data where needed. Cache intermediate assets at the project frame rate. Render a 2-second smoke test including entry and exit before inserting the effect in the full video. Do not use an invented Hyperframes component or flag.

## Reduced-complexity fallback
Use a small conventional push-in. Record this substitution in the preview notes; do not describe a flat approximation as a fully tracked or physically simulated effect.

## Acceptance checks
Inspect the first frame, peak motion, readable hold, exit and the next frame. Check that names are exact, labels point to the correct object, and text is not clipped. Inspect at phone size. For masks, inspect hair, hands and moving edges; for tracked assets, inspect drift and occlusion. Disable the effect if it obscures the message or creates an uncorrectable artifact.

## Example instruction
“Apply Vertigo at the approved emphasis cue. Use my palette and actual assets, keep subtitles readable, show a preview, and report any fallback.”
