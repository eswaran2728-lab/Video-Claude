# Cards above a speaker

## Evidence
R1 output observed. See `../reel-observations.md`. The implementation below is an original reconstruction proposal, not recovered seller source.

## Desired result
Keep the presenter in the lower two-thirds while the upper band carries a small set of relevant visual evidence cards. A bold short title connects the evidence with the spoken idea.

## Geometry
Canvas 1080×1920. Presenter plate fills the frame with eyes near y=850. Reserve x=90–930, y=220–650 for 3 proof tiles. Start with tile size 245×260, 24 px gaps, 24 px corners. Put the title block near y=640–800 only if it clears the face; otherwise move it above the tile row. Use 58–72 px title text and no more than two lines.

## Layers and masking
Background/camera z=0, proof cards z=10, title z=30, captions z=60, supplied logo z=90. A subject matte is optional if tiles never overlap the head. It is required if a card edge should pass behind the hair. Avoid showing two copies of the speaker as a consequence of an accidental fill layer.

## Frame timing at 30 fps
At frame 0 show either the hook proof or the presenter, never a blank board. Cards enter from y+36 with opacity 0 over 10 frames, staggered 3 frames; settle with power3.out. On each spoken point, emphasise the matching tile from scale 1 to 1.035 over 5 frames and hold 20–35 frames. Restore before the next emphasis. Keep a 45–75 frame reading hold for a title. Exit the group with a 6-frame fade or a motivated cut.

## Build in HyperFrames
Use a genuine document/screenshot/actual product frame. For tiny detailed UI, show a crop of the relevant control rather than shrinking a complete page. Build with adaptive-glass media-card scenes or custom local HTML cards. Keep the inner proof frame rectangular and correctly fitted. Use local media and fonts, a paused GSAP timeline registered with HyperFrames, and stable frame-zero states. Drive all movement from composition time. Confirm the chosen schema against the bundled actual builders or installed official HyperFrames documentation.

## Audio and finishing
Retain only one narration source. Map sound accents to visible events and measure the audio transient against its intended frame. Do not infer the reference song or SFX from silent browser observation. Follow the base skill's mixing and subtitle workflow. Export a silent visual layer separately only when it will be deliberately muxed with the final audio.

## Failure checks
The complete card should remain in the safe region at its enlarged state. Check face clearance on moving frames, not just the first frame. Do not invent payment dashboards or figures. A mobile chat wrapper is part of the source demo, not mandatory in the recreation. Inspect frame 0, every layout change, peak motion, reading holds and the final frame. A successful HTML check is not visual verification. Generate a short preview before extending to the full edit.

## Claude instruction
“Use the yap-and-show blueprint with my actual media. Give me an edit plan with output-frame timing, layer order and missing dependencies. Build a local HyperFrames preview, explain any fallback, and wait before final export.”
