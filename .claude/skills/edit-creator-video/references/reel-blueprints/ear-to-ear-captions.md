# Captions beside the head

## Evidence
R1 output observed. See `../reel-observations.md`. The implementation below is an original reconstruction proposal, not recovered seller source.

## Desired result
A landscape speaker shot is centred inside a quiet dark vertical canvas. Short caption fragments occupy left and right zones around ear height rather than the usual bottom line.

## Geometry
Canvas 1080×1920. Fit a 16:9 shot across width, initially y=650–1258 (1080×608); preserve aspect ratio. Sample the actual ear and face positions. Start caption zones at left x=105–420 and right x=660–960 with y near 900. These are suggested anchors, not measured source coordinates. Use 36–46 px sans text and one line per side when possible.

## Layers and masking
Dark field z=0; landscape footage z=10; side-caption groups z=30; optional tiny source label z=50; logo z=90. Caption groups should not be part of a camera-moving transform. Keep the words outside the face exclusion rectangle. Use a stable face anchor per shot or smoothed tracking when the person moves substantially.

## Frame timing at 30 fps
Use timestamped phrase boundaries. Reveal the first left phrase on its speech cue, then the right phrase on its own cue. Hold the left phrase until the right completes when they form a single meaningful sentence. Use 3–4 frame fades; no per-letter movement or karaoke unless specifically requested. Clear both groups before the next phrase pair. At a cut, recompute the anchors.

## Build in HyperFrames
Create a phrase-pair plan containing startFrame, endFrame, side and approved text. Measure rendered text width using the actual loaded font, then wrap or shorten only editorially permitted text. Keep bilingual translations in a separate lower band rather than adding four side captions. For Tamil, render whole shaped phrases and use a Tamil-capable font. Use local media and fonts, a paused GSAP timeline registered with HyperFrames, and stable frame-zero states. Drive all movement from composition time. Confirm the chosen schema against the bundled actual builders or installed official HyperFrames documentation.

## Audio and finishing
Retain only one narration source. Map sound accents to visible events and measure the audio transient against its intended frame. Do not infer the reference song or SFX from silent browser observation. Follow the base skill's mixing and subtitle workflow. Export a silent visual layer separately only when it will be deliberately muxed with the final audio.

## Failure checks
Test the actual phone-size preview: reference examples can use text too small to copy literally. Enlarge text or shift the face crop when needed. Never cover the mouth or use the blank top/bottom space to add unrelated decorative copy. Inspect frame 0, every layout change, peak motion, reading holds and the final frame. A successful HTML check is not visual verification. Generate a short preview before extending to the full edit.

## Claude instruction
“Use the ear-to-ear-captions blueprint with my actual media. Give me an edit plan with output-frame timing, layer order and missing dependencies. Build a local HyperFrames preview, explain any fallback, and wait before final export.”
