# Practical compositing and timing for reference-style edits

## Recover a useful specification from a reference
Work from local video when available. Probe dimensions, duration and frame rate. Extract candidate frames at 0.5-second spacing and finer intervals around each transition. Transcribe audio separately. Record the actual shot boundaries, caption changes, visible layers, mask boundaries, anchor points and entry/hold/exit intervals. Label each field observed, measured, inferred or proposed. Reference frames can reveal appearance but not the author's original code or animation curves.

## Work in output frames
For fps=30, frame=round(seconds×30). Use start-inclusive/end-exclusive intervals. A 60-frame scene covers frames 0–59. A source interval at 2–4 seconds is not automatically output 2–4 seconds after earlier footage is removed. Build the dialogue cut first and derive caption/effect timing from the final cut. Require total plate frame counts to match and use CFR intermediates before tracking.

## Subject masking
Do not confuse a black background with alpha. For a luma matte M in [0,1], output RGB = foreground×M + background×(1−M). Verify whether the supplied alpha is straight or premultiplied before compositing; incorrect treatment produces dark fringes. Render a checkerboard inspection. Reuse the exact source frame and crop transform for the matte. Remove colour spill carefully; never use broad blurring to hide all edge problems.

## Screen-space versus scene-space
Captions and brand marks use screen-space anchors and should remain readable when the camera moves. Wall text and sticky labels belong in scene space and need camera/planar/object tracking when the source moves. Corner-pin the four corners of a wall plane and interpolate the transform per frame; a one-frame perspective transform is only valid for a fixed shot. If tracking is weak, shorten the interval or make the overlay explicitly screen-space.

## Depth ordering
For Orbit, split each card into rear/front representations driven by the same position. Let angle=phase+2π×elapsed/period; x=cx+rx×cos(angle), y=cy+ry×sin(angle). Use sin(angle)>0 for the near half (or invert consistently with the drawn ellipse). Hide the duplicate, not the entire card, when crossing between halves. Make near cards modestly larger and keep transitions stable at the dividing line. Place the matte between rear and front groups. Do not fake near/far depth merely by giving all cards a single z-index.

For Frame Break, transform the framed camera and cutout with identical position and scale. Only the base camera is clipped by the card; the cutout is not. Keep the lower cutout edge masked inside the card so an accidental floating torso is not exposed. Show the head and hands crossing the boundary only where the actual matte is good.

For Vertigo, background and subject must be independent. A suggested 2-second synthetic move changes background scale 1→1.25 while subject scale 1→.92; this is a reconstruction, not measured camera physics. A clean room plate needs pixels behind the removed person. If unavailable, retain a limited depth move without exposing unfilled holes.

## Animation
Use paused GSAP timelines and seekable state. Set stable initial values before registering the timeline; hide later overlays in CSS to avoid a first-frame flash. Use fromTo for a complete known start/end state. Avoid Math.random during render without a fixed seed, CSS animation relying on wall-clock time, and video playback started manually outside the renderer's synchronization.

## Typographic measurement
Load local fonts before measuring. Measure the whole shaped phrase with the actual font and bounding box. For Tamil, never split combining characters into independent spans. Use Intl.Segmenter where grapheme-aware animation is required, and inspect the renderer's shaping. Prefer full-phrase opacity changes. A word-card animation can use separate Latin words; its full spoken meaning still needs an accurate subtitle track if readability is reduced.

## Finishing and sound
All silent visual composites must be mixed with the approved narration, music and cue tracks. Use the bundled sfx-sync helper with its actual documented schema. A waveform's first nonzero sample may precede the audible impact; align the perceptual attack or peak, then audition at normal speed. Check sync at both ends after muxing. Avoid deriving beat timestamps from a song title or from a different recording of the same song.
