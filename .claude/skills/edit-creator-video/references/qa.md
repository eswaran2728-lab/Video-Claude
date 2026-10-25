# Quality gate

Before preview: confirm every asset exists; inspect media orientation and duration; verify names and claims; confirm source and output ranges; remove example paths. Check that selected capabilities exist, and log any fallback.

Before asking for approval: play the opening, ending, every join and each effect at normal speed. Inspect captions at phone size. Check faces, cropping, glyphs, line wraps, contrast, logo visibility and platform-safe positioning. Listen for clipped words, doubled audio, abrupt loops and over-loud effects. Ensure a quiet ending and no unintended black frame. If no playback tool exists, inspect representative frames and audio metadata, and state that listening/playback still needs human review.

Before final delivery: verify the approved version, dimensions, frame rate, codec, duration, orientation, colour and audio stream. Check A/V sync near the beginning and end. Render a contact sheet for human review if useful. Label an untested advanced effect as unverified. Do not claim end-to-end video quality from JSON checks or a successful process alone.

Maintain `validation-notes.md` in the working edit: environment, checks run, preview path, limitations and approval status. Keep this record separate from the skill itself.
