# AI voiceover (Kokoro-82M local, voice af_heart, speed 1.05) for the three motion-graphics parts of the promo.
# Each part: lines laid out with short pauses -> vo/<part>.wav + vo_timing.json (line starts relative to the part).
import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
K = Kokoro("/root/.cache/hyperframes/tts/models/kokoro-v1.0.onnx", "/root/.cache/hyperframes/tts/voices/voices-v1.0.bin"); SR = 24000
PARTS = {
    "intro": [("Check this out!", "Check this out!"), ("This is the original scene from the movie.", "This is the original scene from the movie.")],
    "mid": [("Now… I recreated this exact scene,", "Now. I recreated this exact scene,"), ("just for me!", "just for me!")],
    "cta": [("Want your own version?", "Want your own version?"), ("Just DM me.", "Just D M me."), ("Only RM20 per video!", "Only R M twenty per video!"),
            ("This promotion is for today and tomorrow only: 12 and 13 November.", "This promotion is for today and tomorrow only. The twelfth, and thirteenth of November."),
            ("DM me now, before the offer ends!", "D M me now, before the offer ends!")],
}
GAP = {"intro": [0.25], "mid": [0.05], "cta": [0.35, 0.35, 0.45, 0.4]}
out = {}
for part, lines in PARTS.items():
    seg, t, rows = [np.zeros(int(0.35 * SR))], 0.35, []
    for i, (cap, sp) in enumerate(lines):
        a, sr = K.create(sp, voice="af_heart", speed=1.05, lang="en-us")
        e = np.abs(a) > 0.01; a = a[max(0, np.argmax(e) - 720): len(a) - np.argmax(e[::-1]) + 1440]
        rows.append(dict(text=cap, t0=round(t, 3), t1=round(t + len(a) / SR, 3))); seg.append(a); t += len(a) / SR
        if i < len(lines) - 1: g = GAP[part][i]; seg.append(np.zeros(int(g * SR))); t += g
    seg.append(np.zeros(int(0.5 * SR))); t += 0.5
    sf.write(f"vo/{part}.wav", np.concatenate(seg), SR); out[part] = dict(dur=round(t, 3), lines=rows); print(part, round(t, 2), [r["t0"] for r in rows])
json.dump(out, open("vo_timing.json", "w"), indent=1)
