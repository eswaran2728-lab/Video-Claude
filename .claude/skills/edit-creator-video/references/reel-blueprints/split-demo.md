# Source-to-result demonstration with presenter below

## Evidence
R2 output observed. See `../reel-observations.md`. The implementation below is an original reconstruction proposal, not recovered seller source.

## Desired result
Use a stable lower presenter while the upper area compares a raw source card with a taller edited output card. A small command label explains the transformation.

## Geometry
Canvas 1080×1920. Upper demo area y=0–960 with warm off-white field. Lower speaker pane y=960–1920. Put source card x=105 y=320 w=390 h=490; result card x=550 y=100 w=425 h=710. Place a slim process label within x=90–960 and y=835–925. Preserve each card aspect ratio with intentional crop or contain.

## Layers and masking
Upper field z=0; upper source and result z=10; lower speaker z=20 clipped to its pane; process label z=40; main captions z=60; logo z=90. The top source card and bottom speaker may be different recordings; do not force lip sync between them. Mute demonstration clips if the lower speaker provides the narrative.

## Frame timing at 30 fps
Show source content immediately, introduce the edited result within 12–18 frames of the relevant cue, and hold both for 45–75 frames. Transition result examples by swapping content inside the same persistent card, with a 6-frame crossfade. Keep the lower pane continuous through those changes unless a real narration edit requires a cut.

## Build in HyperFrames
Use adaptive-glass split-half as a starting scaffold, then replace the upper proof group with two media cards. Generate the miniature edited result from real prepared assets; do not use a still screenshot when motion is the promised comparison. Render the inner result first, then use that local MP4 in the demonstration composition. Use local media and fonts, a paused GSAP timeline registered with HyperFrames, and stable frame-zero states. Drive all movement from composition time. Confirm the chosen schema against the bundled actual builders or installed official HyperFrames documentation.

## Audio and finishing
Retain only one narration source. Map sound accents to visible events and measure the audio transient against its intended frame. Do not infer the reference song or SFX from silent browser observation. Follow the base skill's mixing and subtitle workflow. Export a silent visual layer separately only when it will be deliberately muxed with the final audio.

## Failure checks
The small command label is explanatory text, not a real executable Claude command unless this package implements it. Reduce ancillary UI for mobile readability. Show one selected result clearly rather than several tiny competing demos. Inspect frame 0, every layout change, peak motion, reading holds and the final frame. A successful HTML check is not visual verification. Generate a short preview before extending to the full edit.

## Claude instruction
“Use the split-demo blueprint with my actual media. Give me an edit plan with output-frame timing, layer order and missing dependencies. Build a local HyperFrames preview, explain any fallback, and wait before final export.”
