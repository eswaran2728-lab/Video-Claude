// One-command render: stitch leaderboard -> HyperFrames render -> loudness normalise -> named MP4.
//   npm run render
// Output: renders/avsec-cyber-roadshow.mp4
//   (renders/avsec-cyber-roadshow-PREVIEW.mp4 while a logo or the link is still a placeholder)
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, readFileSync, rmSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const run = (cmd, args) => execFileSync(cmd, args, { cwd: root, stdio: "inherit", shell: process.platform === "win32" });
const fail = (msg) => { console.error(msg); process.exit(1); };

// Read the data block the same way the video does.
const ctx = { window: {} };
vm.runInNewContext(readFileSync(join(root, "data/leaderboard.js"), "utf8"), ctx);
const D = ctx.window.AVSEC_DATA;
const ph = (v) => v === undefined || v === "" || (typeof v === "string" && /^\s*\[.*\]\s*$/.test(v));

const shots = D.leaderboardScreenshots || [];
if (!shots.length) fail("No leaderboardScreenshots in data/leaderboard.js");
for (const s of shots) if (!existsSync(join(root, s))) fail(`Screenshot not found: ${s}`);
const logos = D.logos || {};
for (const [k, v] of Object.entries(logos)) if (v && !existsSync(join(root, v))) fail(`Logo file for "${k}" not found: ${v}`);
const logoGaps = Object.entries(logos).filter(([, v]) => v === "").map(([k]) => k);
const urlOk = !ph(D.challengeUrl) && /^https:\/\//.test(D.challengeUrl);
if (/\/host\b|organizer/i.test(D.challengeUrl || "")) fail("challengeUrl points at a host/organizer page. Use the public /play link.");

// Join the Spot the Risk screenshots into one board (needs Python 3 + Pillow).
const py = spawnSync("python3", ["--version"]).status === 0 ? "python3" : "python";
run(py, ["scripts/stitch_board.py"]);

const quiz = D.videoQuiz || [];
console.log(`\nSpot the Risk board: ${shots.length} screenshot(s) -> assets/leaderboard/board.png`);
console.log(`Video quiz board: ${quiz.length} rows${quiz.length ? `, #1 ${quiz[0].name} (${quiz[0].score})` : ""}`);
console.log(`QR / link: ${urlOk ? D.challengeUrl : "[PUBLIC SPOT THE RISK LINK] (no QR)"}`);
console.log(`Logos: ${Object.entries(logos).map(([k, v]) => `${k}=${v === null ? "hidden" : v || "[PLACEHOLDER]"}`).join(", ")}`);
const preview = logoGaps.length > 0 || !urlOk;
if (preview) console.log("Still contains a [PLACEHOLDER] -> rendering a PREVIEW.\n");

mkdirSync(join(root, "renders"), { recursive: true });
const raw = "renders/_raw.mp4";
const out = `renders/avsec-cyber-roadshow${preview ? "-PREVIEW" : ""}.mp4`;

run("npx", ["hyperframes", "render", "-q", "delivery", "-o", raw]);

// Two-pass EBU R128 loudness: -14 LUFS integrated, -1.5 dBTP, video stream copied untouched.
const target = "I=-14:TP=-1.5:LRA=11";
// ffmpeg prints the measurement JSON on stderr.
const probe = spawnSync("ffmpeg", ["-hide_banner", "-nostats", "-i", raw, "-af", `loudnorm=${target}:print_format=json`, "-f", "null", "-"], { cwd: root, encoding: "utf8" }).stderr;
const m = JSON.parse(probe.slice(probe.lastIndexOf("{"), probe.lastIndexOf("}") + 1));
// The AAC re-encode pads audio slightly; cut the file to the video's exact length.
const vdur = spawnSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "csv=p=0", raw], { cwd: root, encoding: "utf8" }).stdout.trim();
run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-i", raw, "-t", vdur, "-c:v", "copy",
  "-af", `loudnorm=${target}:measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset}:linear=true`,
  "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]);
rmSync(join(root, raw), { force: true });
console.log(`\nDone: ${out}`);
