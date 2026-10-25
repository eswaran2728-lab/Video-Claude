# Collage grid with foreground cutout

## Evidence
R2 output observed. See `../reel-observations.md`. The implementation below is an original reconstruction proposal, not recovered seller source.

## Desired result
Build a multi-image collage as visual context, with a smaller isolated presenter layered over its centre or lower edge.

## Geometry
For a full output at 1080×1920, reserve grid x=90 y=180 w=900 h=1200. A 2×2 structure gives four 444×594 cells with 12 px gutters. Place the presenter cutout within x=300–780 and y=750–1450; resize to the shot and grid contents. Reserve lower safe space for captions.

## Layers and masking
Base field z=0; four separately clipped image cells z=10; tinted contrast backing only where needed z=15; presenter matte z=25; caption z=60; logo z=90. No segmentation is needed for grid images; only the presenter requires it.

## Frame timing at 30 fps
Reveal the first cell on the hook, then add relevant cells at content beats with 3-frame staggering and 8-frame eased arrivals. Give the cutout a restrained 10-frame entrance. Optionally animate image crops at 1–2% scale over 2 seconds. Do not make all cells move in different directions or distract from the presenter.

## Build in HyperFrames
Use local photographs or licensed stills illustrating the actual argument. Make crop anchors explicit per cell. Create separate image layers rather than baking text into a collage raster. If used as the right card of split-demo, pre-render this output at its native 1080×1920 and downscale only in the outer demo. Use local media and fonts, a paused GSAP timeline registered with HyperFrames, and stable frame-zero states. Drive all movement from composition time. Confirm the chosen schema against the bundled actual builders or installed official HyperFrames documentation.

## Audio and finishing
Retain only one narration source. Map sound accents to visible events and measure the audio transient against its intended frame. Do not infer the reference song or SFX from silent browser observation. Follow the base skill's mixing and subtitle workflow. Export a silent visual layer separately only when it will be deliberately muxed with the final audio.

## Failure checks
Check that the grid does not imply the speaker owns or endorses pictured products. Inspect matte edges against all four backgrounds. A transparent avatar icon is only a placeholder for a smoke test, never a substitute for the real supplied presenter. Inspect frame 0, every layout change, peak motion, reading holds and the final frame. A successful HTML check is not visual verification. Generate a short preview before extending to the full edit.

## Claude instruction
“Use the cutout-grid-reel blueprint with my actual media. Give me an edit plan with output-frame timing, layer order and missing dependencies. Build a local HyperFrames preview, explain any fallback, and wait before final export.”
