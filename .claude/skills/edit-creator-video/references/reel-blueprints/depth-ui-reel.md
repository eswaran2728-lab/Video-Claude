# UI behind a foreground presenter

## Evidence
R1 output observed. See `../reel-observations.md`. The implementation below is an original reconstruction proposal, not recovered seller source.

## Desired result
Build real visual depth using a full camera background, a UI evidence plane behind the presenter, and a foreground identity or action card.

## Geometry
At 1080×1920, place a channel/page panel around x=95 y=180 w=890 h=730; use 28 px corners. Keep the head close to the horizontal centre, with most of the panel visible above and beside it. Put one foreground information strip near x=150 y=1240 w=780 h=140, adjusted to avoid hands and platform controls.

## Layers and masking
Camera room plate z=0; background UI z=10; temporally stable subject matte z=20; foreground strip z=35; captions z=60; logo z=90. Derive the matte from the same constant-frame-rate source as the visible face. Do not simply place an unmasked full-frame camera on top, because it hides the background UI.

## Frame timing at 30 fps
UI panel starts at scale .94, y+26 and settles to scale 1 over 14 frames. Subject remains at native temporal speed; avoid an unnecessary scale bounce. Foreground strip enters 6 frames later over 9 frames. A small number can count up over 18–24 frames only when a verified target exists. Hold the completed composition for at least 45 frames.

## Build in HyperFrames
Prepare camera-clean.mp4 and a synchronized alpha subject layer, or a luma matte with a matching frame count. Composite source×mask + underlying×(1−mask). Use feathering only at the edge, approximately 1–2 px at full resolution, and suppress colour spill without blurring face detail. Build a channel-like interface from supplied real captures or label a conceptual mockup. Use local media and fonts, a paused GSAP timeline registered with HyperFrames, and stable frame-zero states. Drive all movement from composition time. Confirm the chosen schema against the bundled actual builders or installed official HyperFrames documentation.

## Audio and finishing
Retain only one narration source. Map sound accents to visible events and measure the audio transient against its intended frame. Do not infer the reference song or SFX from silent browser observation. Follow the base skill's mixing and subtitle workflow. Export a silent visual layer separately only when it will be deliberately muxed with the final audio.

## Failure checks
Inspect hair at frames before, during and after each hand movement. Check the exact start frame of every plate and remove duplicated audio from matte layers. Verify any channel name, count and button label. If segmentation is unavailable, use a visibly framed presenter inset and report that fallback. Inspect frame 0, every layout change, peak motion, reading holds and the final frame. A successful HTML check is not visual verification. Generate a short preview before extending to the full edit.

## Claude instruction
“Use the depth-ui-reel blueprint with my actual media. Give me an edit plan with output-frame timing, layer order and missing dependencies. Build a local HyperFrames preview, explain any fallback, and wait before final export.”
