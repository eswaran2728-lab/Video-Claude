# Configuration contract

`assets/project.example.json` is an example, not a strict renderer schema. `canvas.width/height/fps` set output geometry. `preview` controls the basic helper output; `clips[].path` must resolve to real local images for that helper. `duration` is an output hold in seconds. `music.path` may be null; its gain is in decibels, not a percentage. A full renderer must implement captions, logo and effects itself.

For full edits add `source_in`, `source_out`, `output_start`, `output_end`, `speed`, `focal_anchor`, `fit`, `transition` and `rationale` to timeline clips. Use normalized focal anchors from 0 to 1, measured from the top-left. For overlays define start/end in output seconds, z-order and a safe-area bounding box. Do not pass an example JSON directly to a third-party CLI as if it were that CLI's native schema.

Effects use IDs from `effects.json`, a cue time, duration, intensity 0–1, asset references and fallback notes. Each selected effect must get its own resolved parameters in the generated project. A style is a starting design system; content needs take priority. Preserve a source-to-output timing map when retiming captions and audio.
