# Persistent catalogue with changing effect demonstrations

## Evidence
R3 output observed. See `../reel-observations.md`. The implementation below is an original reconstruction proposal, not recovered seller source.

## Desired result
A stable speaker shot carries a short heading and two small effect lists. Highlight one list item while a selected effect demonstrates its result in the camera scene.

## Geometry
Canvas 1080×1920. Heading x=150 y=230 w=780 h=150; two list blocks x=75 and x=700, y=410, w≈300. Reserve a central head exclusion region. These dense lists are for a showcase, not the default design for normal reels. Use 70 px heading and 30–36 px list text initially, then reduce the number of items if readability fails.

## Layers and masking
Camera/background z=0; behind-subject effect z=10; subject matte z=20 when needed; foreground effect z=35; list/title HUD z=50; captions z=60; logo z=90. Effects that intentionally replace the full scene may hide or relocate the HUD; document the decision.

## Frame timing at 30 fps
Keep the active list item in the accent colour for the full effect interval; dim inactive items without reducing legibility. Trigger the effect at its exact output frame and return to the base state before the next demonstration. Suggested per-effect interval: 36–75 frames depending on complexity. Use a clean shot at the end for the closing line. Do not use a new SFX on every list highlight.

## Build in HyperFrames
Build one selected effect at a time, pre-render expensive masks or 3D, and assemble the catalogue from those verified sections. For the observed miniature editor layout, use 3–4 small panels: prompt, progress, timeline with real source thumbnails, and a preview video. Treat progress as a conceptual animation unless it reflects a real run. Use local media and fonts, a paused GSAP timeline registered with HyperFrames, and stable frame-zero states. Drive all movement from composition time. Confirm the chosen schema against the bundled actual builders or installed official HyperFrames documentation.

## Audio and finishing
Retain only one narration source. Map sound accents to visible events and measure the audio transient against its intended frame. Do not infer the reference song or SFX from silent browser observation. Follow the base skill's mixing and subtitle workflow. Export a silent visual layer separately only when it will be deliberately muxed with the final audio.

## Failure checks
Do not recreate all 16 source demonstrations from a handful of sampled frames. Use existing effect recipes for construction and mark their numerical settings as suggested. Keep captions separate from the HUD and do not capture outer Instagram comments or controls as part of the final composition. Inspect frame 0, every layout change, peak motion, reading holds and the final frame. A successful HTML check is not visual verification. Generate a short preview before extending to the full edit.

## Claude instruction
“Use the effect-showcase blueprint with my actual media. Give me an edit plan with output-frame timing, layer order and missing dependencies. Build a local HyperFrames preview, explain any fallback, and wait before final export.”
