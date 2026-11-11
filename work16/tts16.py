# AI voiceover: Kokoro-82M (local ONNX, the model `npx hyperframes tts` uses), voice af_heart, speed 1.0.
# One clip per script line (trimmed of leading/trailing silence), laid out per scene with fixed pauses, so every caption and
# visual cue gets an exact start time. -> vo/<scene>.wav (24 kHz mono) + timing.json
import json, os, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from script16 import SCENES, QA
K = Kokoro("/root/.cache/hyperframes/tts/models/kokoro-v1.0.onnx", "/root/.cache/hyperframes/tts/voices/voices-v1.0.bin")
VOICE, SPEED, SR = os.environ.get("VOICE", "af_heart"), float(os.environ.get("SPEED", "1.0")), 24000
LEAD, TAIL = 1.0, 1.2                         # silence before the first and after the last line of a scene
os.makedirs("vo/lines", exist_ok=True)
NUM = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def say(text, key):
    p = f"vo/lines/{key}.wav"
    if os.path.exists(p) and open(p + ".txt").read() == f"{VOICE}|{SPEED}|{text}":
        a, _ = sf.read(p); return a
    a, sr = K.create(text, voice=VOICE, speed=SPEED, lang="en-us"); assert sr == SR
    e = np.abs(a) > 0.01; i0 = max(0, np.argmax(e) - int(0.03 * SR)); i1 = min(len(a), len(a) - np.argmax(e[::-1]) + int(0.06 * SR))
    a = a[i0:i1]; sf.write(p, a, SR); open(p + ".txt", "w").write(f"{VOICE}|{SPEED}|{text}"); return a


def gap_after(cap, nxt):
    if nxt is None: return 0
    if re.match(r"^(Mistake \d|Rule \d|First:|Second:|Third:|Fourth:|Fifth:|At the (beginning|end) of your shift|Now,|However,|So,|Therefore|For example|Before|Alright|And one)", nxt[0]): return 0.75
    if cap.endswith(":"): return 0.3
    return 0.42


timing = {"voice": VOICE, "speed": SPEED, "scenes": []}
for sc in SCENES + [dict(id="s13", title="Staff understanding check", lines=None)]:
    if sc["lines"] is None:                   # Q&A: question, think pause (3.5 s on screen countdown), answer
        lines = [("Staff understanding check.", "intro", "Staff understanding check. Let's see how much you remember."), ]
        for i, (q, a, qs, as_) in enumerate(QA):
            lines.append((q, f"q{i + 1}", f"Question {NUM[i]}. {qs or q}"))
            lines.append((a, f"a{i + 1}", as_ or a))
        lines.append(("End of training. AA/SEC/F/077 – Attendance Record Staff Guidance", "end", None))
    else: lines = sc["lines"]
    out, t, rows = [np.zeros(int(LEAD * SR))], LEAD, []
    for j, ln in enumerate(lines):
        cap, cue = ln[0], ln[1]; spoken = ln[2] if len(ln) > 2 else cap
        if spoken is None:                    # silent end card line
            rows.append(dict(i=j, text=cap, cue=cue, t0=round(t, 3), t1=round(t + 4.0, 3), silent=True)); t += 4.0
            out.append(np.zeros(int(4.0 * SR))); continue
        a = say(spoken, f"{sc['id']}_{j:02d}")
        rows.append(dict(i=j, text=cap, cue=cue, t0=round(t, 3), t1=round(t + len(a) / SR, 3)))
        out.append(a); t += len(a) / SR
        nxt = lines[j + 1] if j + 1 < len(lines) else None
        g = gap_after(cap, nxt)
        if cue and cue.startswith("q") and cue[1:].isdigit(): g = 3.5      # think time before the answer
        elif cue and cue.startswith("a") and cue[1:].isdigit(): g = 1.4
        out.append(np.zeros(int(g * SR))); t += g
    out.append(np.zeros(int(TAIL * SR))); t += TAIL
    w = np.concatenate(out); sf.write(f"vo/{sc['id']}.wav", w, SR)
    timing["scenes"].append(dict(id=sc["id"], title=sc["title"], dur=round(len(w) / SR, 3), lines=rows))
    print(sc["id"], round(len(w) / SR, 1), "s", len(rows), "lines", flush=True)
t = 0
for s in timing["scenes"]: s["start"] = round(t, 3); t += s["dur"]
timing["total"] = round(t, 3)
json.dump(timing, open("timing.json", "w"), indent=1, ensure_ascii=False); print("total", round(t, 1))
