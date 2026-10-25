# FavStash integration for Claude Code + HyperFrames

## Snapshot and scope
Bundle source: https://github.com/alisadiq-ai/favstash-ai-video-editing-skills
Pinned commit: `b6901b21e1ef690f3443556718700d60b38f5c19`. Upstream package version: 0.7.0. Preserve `vendor/favstash/LICENSE` and `THIRD_PARTY_NOTICES.md`; bundled fonts retain their OFL. This copy includes all ten upstream skills, their scripts, SFX, fonts, tests and references. It omits Git history, CI and upstream workspace agent settings. The original plugin manifest is retained for attribution and upstream validation; do not load that subtree with --plugin-dir for the local-only workflow because its manifest declares an optional FavStash connector. No code or skill files were changed inside the vendored snapshot. Upstream preview pictures are examples, not reusable stock. Read its notices before reusing media.

This integration defaults to LOCAL editing in the user's existing HyperFrames environment. Do not connect FavStash, alter MCP configuration, upload footage or install global skills just because upstream setup discusses them. Those are optional separate actions. Our preview approval requirement and exact user brief govern this workflow. Preserve existing working runtime versions and user edits.

## Paths from this skill root
- Base edit: `vendor/favstash/skills/3-editing/edit-video/SKILL.md`.
- HyperFrames + GSAP builder: `vendor/favstash/skills/3-editing-styles/adaptive-glass/SKILL.md`.
- White UI canvas: `vendor/favstash/skills/3-editing-styles/paper-grid/SKILL.md`.
- Head-over-card composition: `vendor/favstash/skills/3-editing-styles/breakout-card/SKILL.md`.
- Product animation: `vendor/favstash/skills/3-editing-styles/product-motion-ads/SKILL.md`.
- Extra 33 effect recipes: `vendor/favstash/skills/3-editing-styles/motion-effects/references/effects.md`.
- Simple footage captions: `vendor/favstash/skills/3-editing-styles/text-over-footage/SKILL.md`.
- Research, scripting and optional publishing: other three stage folders in `vendor/favstash/skills/`.

## Default local workflow
Read the base edit skill plus ONE relevant style. Read motion-effects only for selected accents. Use our reel-blueprint index for the reference-specific layouts. Do not combine all looks in a single shot. A base preset, a layout blueprint and an accent effect are different choices.

Run from an existing creator workspace using actual absolute paths:
```text
node <skill>/vendor/favstash/skills/3-editing/edit-video/scripts/doctor.mjs --workspace <workspace> --json
node <skill>/vendor/favstash/skills/3-editing/edit-video/scripts/new-edit.mjs --workspace <workspace> --slug silambam-lunch
```
Use the returned run path; do not guess its date or random ID. Keep media in that run and generate a new version directory for every revision. If HyperFrames and GSAP already work, reuse them. For a fresh runtime, run:
```text
node <skill>/vendor/favstash/skills/3-editing/edit-video/scripts/init-workspace.mjs --workspace <workspace> --install
```
The snapshot pins HyperFrames 0.8.32 and GSAP 3.14.2 when no existing versions are configured. Node 22+ is required. This prepares a local runtime, not a FavStash account. Verify the installed CLI help and run a smoke composition before reporting render readiness. Python and macOS-specific capabilities are separate.

## Real scaffold, not pseudocode
Copy upstream `adaptive-glass/assets/composition.example.json` into the run, replace media paths, set durationFrames and contiguous scenes, then run:
```text
node <skill>/vendor/favstash/skills/3-editing-styles/adaptive-glass/scripts/scaffold-glass.mjs <run>/work/scenes.json --output <run>/work/glass-v01 --workspace <workspace>
<workspace>/.favstash-studio/runtime/node_modules/.bin/hyperframes check <run>/work/glass-v01
<workspace>/.favstash-studio/runtime/node_modules/.bin/hyperframes render <run>/work/glass-v01 --fps 30 --quality high --output <run>/previews/glass-v01.mp4
```
On Windows use the executable's `.cmd` wrapper. Validate these arguments against installed help if using a different release. The scaffold output is SILENT: dialogue, captions and SFX need a deliberate finishing/mixing pass. Do not deliver it as a complete edited video.

## Installation choices
The single `edit-creator-video` folder can be copied into `.claude/skills/` with its vendor subtree intact. Claude can read all nested material explicitly through this router. To expose all upstream skills as separate discoverable Claude skills, run our `scripts/install_claude_skills.py` from the extracted folder, first in dry-run mode; it copies all ten rather than relying on the upstream install example which currently omits motion-effects from its explicit list. Existing destinations are never overwritten.

## Selection map
Talking head + UI proof → adaptive-glass; white educational interface → paper-grid; portrait escaping a card → breakout-card; no camera/product-only story → product-motion-ads; simple quote/joke montage → text-over-footage. Use the original 9 style recipes as optional palette/pacing directions, not alternative engine schemas. Our original project.example.json is not the upstream scaffold's composition schema.
