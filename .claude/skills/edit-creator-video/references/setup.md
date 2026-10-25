# Updated HyperFrames route

Use [upstream integration](upstream-integration.md) first: this revision bundles real builders and a pinned runtime setup. The earlier general guidance below still applies where compatible. HyperFrames runtime binaries are installed locally, not shipped in the ZIP.

# Setup and installation

## Claude Code
Place the entire `edit-creator-video` directory under a project's `.claude/skills/` directory for project scope, or under your user `.claude/skills/` directory for personal scope. Preserve `SKILL.md`, `references`, `assets` and `scripts` together. If discovery differs in your installed Claude Code version, consult its current official documentation rather than guessing. You can always ask Claude to read the absolute path to SKILL.md explicitly.

Run `python scripts/doctor.py` from the skill directory (`python3` may be needed on macOS/Linux). Python scripts require Python 3.9 or newer and use only the standard library. Basic rendering needs FFmpeg and FFprobe on PATH. Install these through a trusted package manager appropriate for the operating system; do not run unknown one-line installers. The doctor reports missing tools and does not install anything.

## Windows
Use Python from a trusted distribution. In PowerShell, run `python .\scripts\doctor.py`; use quoted paths when names contain spaces. Place the folder under your Windows user profile's `.claude\skills` or your project `.claude\skills`. Restart the shell after changing PATH. Do not assume Bash commands work in PowerShell.

## macOS and Linux
Use an existing trusted Python and FFmpeg installation. Run from the extracted skill folder. Avoid overwriting system Python. Any additional packages should use a dedicated virtual environment. Check disk space before generating frame sequences.

## Hyperframes discovery
No Hyperframes dependency is included. Ask Claude to inspect the actual project package manifest, installed executable, and current official documentation. Confirm preview and export entry points and supported media/animation primitives. Do not assume a product called Hyperframes uses a particular framework. Complete a 2-second text/video/audio test, then record the exact working commands in the project. If unavailable, use the basic FFmpeg montage helper for a simple preview or build an explicitly identified alternative renderer.

## Troubleshooting
Missing executable: verify PATH in the same shell as Claude. Unsupported codec: make a proxy and preserve originals. Black frame: inspect source alpha, layer ordering and in/out timing. Missing Tamil glyphs: install a licensed Tamil-capable font and use a shaping-aware text renderer. Failed tracking: shorten the shot or use a stationary label. Out of memory: reduce preview resolution and pre-render expensive layers. Never hide a failed render behind a success message.
