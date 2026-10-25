# Product detail above a speaker

## Evidence
R2 output observed; broader sequencing is a proposed method. See `../reel-observations.md`. The implementation below is an original reconstruction proposal, not recovered seller source.

## Desired result
Combine everyday product or activity b-roll with a presenter below. Add a compact factual tag only when the information is verified.

## Geometry
Canvas 1080×1920. Top b-roll y=180–900, bottom presenter y=900–1920; adjust the dividing line to preserve face framing. Place an approved short tag near the product at x=680 y=450, with w≤260 and h≤100. Avoid showing a price if the user has not confirmed it.

## Layers and masking
Background z=0, upper b-roll z=10 clipped, lower camera z=10 separately clipped, tag z=35, captions z=60, logo z=90. Use neutral colour matching between lifestyle footage and camera. Do not mirror a product with directional text.

## Frame timing at 30 fps
Cut the top pane on meaningful nouns and actions while keeping the lower presenter stable. Use 1.2–2.5 second b-roll holds initially; slower for intricate craft work. Tags enter over 6 frames on the associated noun and remain for 30–60 frames. Hide tags before the next unrelated image.

## Build in HyperFrames
Use media-bleed split scenes in adaptive-glass, or custom nested video panes in HyperFrames. Preserve real sound only when it supports the scene; otherwise mute top-pane audio and mix separately. Use Eshan Creation product clips here with approved material, dimensions and price. Use local media and fonts, a paused GSAP timeline registered with HyperFrames, and stable frame-zero states. Drive all movement from composition time. Confirm the chosen schema against the bundled actual builders or installed official HyperFrames documentation.

## Audio and finishing
Retain only one narration source. Map sound accents to visible events and measure the audio transient against its intended frame. Do not infer the reference song or SFX from silent browser observation. Follow the base skill's mixing and subtitle workflow. Export a silent visual layer separately only when it will be deliberately muxed with the final audio.

## Failure checks
Check upper crops for the actual feature under discussion. Avoid mismatched product variants or using demonstrative footage as proof of an unsupported claim. This recipe does not establish a complete vendor personal-reel preset. Inspect frame 0, every layout change, peak motion, reading holds and the final frame. A successful HTML check is not visual verification. Generate a short preview before extending to the full edit.

## Claude instruction
“Use the personal-short-form-reels blueprint with my actual media. Give me an edit plan with output-frame timing, layer order and missing dependencies. Build a local HyperFrames preview, explain any fallback, and wait before final export.”
