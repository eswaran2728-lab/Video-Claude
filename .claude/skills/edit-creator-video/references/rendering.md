# Updated HyperFrames route

Use [upstream integration](upstream-integration.md) first: this revision bundles real builders and a pinned runtime setup. The earlier general guidance below still applies where compatible. HyperFrames runtime binaries are installed locally, not shipped in the ZIP.

# Rendering adapters and capability limits

## Choose deliberately
FFmpeg supports cuts, scale, pad, crop, basic mixing, fades and subtitle burn-in when the build includes required filters. HTML/CSS/SVG or canvas can express cards, text and charts but needs a verified frame capture/export workflow. Real 3D, subject segmentation, reliable tracking, depth maps and speech recognition need separate tooling. None is automatically supplied by a prose skill.

## Hyperframes adapter procedure
Inspect the project and installed version; use current official docs for its exact commands. Identify composition size, frame rate, duration, asset serving, font loading and audio capabilities. Build a minimal source video plus one title and an audio track. Preview and export 2 seconds; verify duration and sync with FFprobe and playback. Only then port the timeline. If the tool cannot perform an effect, implement a pre-rendered overlay or record a simpler fallback. Use the actual bundled builders described in upstream-integration.md. Their automated tests were run; the HyperFrames runtime installation in this hosted environment failed during an ONNX dependency download, so an end-to-end HyperFrames render remains unverified here.

## Coordinate and timing rules
Author at 1080 × 1920, 30 fps by default; confirm platform and footage requirements. Use output-timeline seconds. Render at deterministic times, not wall-clock time; seed random particles. Use even dimensions for H.264. Preserve aspect ratio and avoid stretching. Normalize phone rotation metadata through a proxy if necessary. Use an SDR Rec.709 workflow unless HDR is explicitly supported end to end; inspect HDR sources for washed-out conversion.

## Basic montage helper
`python scripts/render_montage.py assets/project.example.json /absolute/output/preview.mp4`
Replace the example paths first. This helper renders a photo-only, hard-cut sequence with fit-and-pad, silent audio by default, and optional supplied music trimmed to the montage. It does not render captions, logos, speech, effects, crossfades, camera moves or carousels. Use it only for a basic sequence check. Claude must implement richer compositions with a verified renderer. The helper refuses an existing output path and does not mutate originals.

## Export starting points
Preview: 540 × 960, 30 fps, H.264 and AAC if audio exists. Approved final: 1080 × 1920, source-appropriate frame rate, H.264 yuv420p, AAC 48 kHz and fast-start metadata. Treat these as interoperable starting values rather than current platform guarantees. Use a higher-quality intermediate when compositing multiple passes. Inspect final playback and media metadata; an exit code alone is insufficient.
