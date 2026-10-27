// One-command render: HyperFrames render -> loudness normalise -> named MP4.
//   npm run render
// Output: renders/avsec-cyber-roadshow.mp4
//   (renders/avsec-cyber-roadshow-PREVIEW.mp4 while any result is still a [PLACEHOLDER])
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, readFileSync, rmSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const run = (cmd, args) => execFileSync(cmd, args, { cwd: root, stdio: "inherit", shell: process.platform === "win32" });

// Read the data block the same way the video does.
const ctx = { window: {} };
vm.runInNewContext(readFileSync(join(root, "data/leaderboard.js"), "utf8"), ctx);
const D = ctx.window.AVSEC_DATA;
const ph = (v) => v === undefined || v === "" || (typeof v === "string" && /^\s*\[.*\]\s*$/.test(v));
const pending = D.leaderboard.some((e) => ph(e.name) || ph(e.points) || ph(e.time));
const logos = D.logos || {};
const logoGaps = Object.entries(logos).filter(([, v]) => v === "").map(([k]) => k);
for (const [k, v] of Object.entries(logos)) {
  if (v && !existsSync(join(root, v))) {
    console.error(`Logo file for "${k}" not found: ${v}`);
    process.exit(1);
  }
}
const urlOk = !ph(D.challengeUrl) && /^https:\/\//.test(D.challengeUrl);
if (/\/host\b|organizer/i.test(D.challengeUrl || "")) {
  console.error("challengeUrl points at a host/organizer page. Use the public /play link.");
  process.exit(1);
}

console.log("\nRanking in the video:");
[...D.leaderboard].sort((a, b) => a.rank - b.rank).forEach((e) =>
  console.log(`  #${e.rank}  ${e.name}  |  ${e.points} pts  |  ${e.time === null ? "(time hidden)" : e.time}`));
console.log(`QR / link: ${urlOk ? D.challengeUrl : "[PUBLIC SPOT THE RISK LINK] (no QR)"}`);
console.log(`Logos: ${Object.entries(logos).map(([k, v]) => `${k}=${v === null ? "hidden" : v || "[PLACEHOLDER]"}`).join(", ")}`);
if (pending || logoGaps.length) console.log("Still contains [PLACEHOLDERS] -> rendering a PREVIEW.\n");

mkdirSync(join(root, "renders"), { recursive: true });
const raw = "renders/_raw.mp4";
const out = `renders/avsec-cyber-roadshow${pending || logoGaps.length ? "-PREVIEW" : ""}.mp4`;

run("npx", ["hyperframes", "render", "-q", "delivery", "-o", raw]);

// Two-pass EBU R128 loudness: -14 LUFS integrated, -1.5 dBTP, video stream copied untouched.
const target = "I=-14:TP=-1.5:LRA=11";
// ffmpeg prints the measurement JSON on stderr.
const probe = spawnSync("ffmpeg", ["-hide_banner", "-nostats", "-i", raw, "-af", `loudnorm=${target}:print_format=json`, "-f", "null", "-"], { cwd: root, encoding: "utf8" }).stderr;
const m = JSON.parse(probe.slice(probe.lastIndexOf("{"), probe.lastIndexOf("}") + 1));
run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-i", raw, "-c:v", "copy",
  "-af", `loudnorm=${target}:measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset}:linear=true`,
  "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]);
rmSync(join(root, raw), { force: true });
console.log(`\nDone: ${out}`);
