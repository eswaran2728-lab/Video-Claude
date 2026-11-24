# Voice: Kokoro-82M (local, free; the model behind `npx hyperframes tts`), voice af_heart, slowed for children.
# One clip per caption line; per scene: lead-in (longer when a Step card opens the scene), fixed gaps, extra motion time.
# Word timings: faster-whisper word timestamps on each clip, matched to caption words by position. -> vo/sNN.wav, timing.json
import json, os, re, numpy as np, soundfile as sf, scipy.signal as ss
from kokoro_onnx import Kokoro
from faster_whisper import WhisperModel
from script27 import SCENES, EXTRA
K = Kokoro("/root/.cache/hyperframes/tts/models/kokoro-v1.0.onnx", "/root/.cache/hyperframes/tts/voices/voices-v1.0.bin")
VOICE, SPEED, SR = os.environ.get("VOICE", "af_heart"), float(os.environ.get("SPEED", "0.9")), 24000
WM = WhisperModel("small", device="cpu", compute_type="int8")

def say(text, key):
    p = f"vo/lines/{key}.wav"
    if os.path.exists(p) and open(p + ".txt").read() == f"{VOICE}|{SPEED}|{text}":
        a, _ = sf.read(p); return a
    a, sr = K.create(text, voice=VOICE, speed=SPEED, lang="en-us")
    e = np.abs(a) > 0.01; i0 = max(0, np.argmax(e) - int(0.03 * SR)); i1 = min(len(a), len(a) - np.argmax(e[::-1]) + int(0.08 * SR))
    a = a[i0:i1]; sf.write(p, a, SR); open(p + ".txt", "w").write(f"{VOICE}|{SPEED}|{text}"); return a

def words_of(cap, a):
    """caption words with start/end inside the clip (seconds)"""
    cw = cap.split(); d = len(a) / SR
    segs, _ = WM.transcribe(ss.resample_poly(a, 16000, SR).astype(np.float32), language="en", word_timestamps=True, beam_size=5)
    hw = [w for s in segs for w in s.words]
    if len(hw) == len(cw):
        return [dict(w=c, s=round(max(0, h.start), 3), e=round(min(d, h.end), 3)) for c, h in zip(cw, hw)], " ".join(h.word.strip() for h in hw)
    L = [len(re.sub(r"\W", "", c)) + 1 for c in cw]; tot = sum(L); t = 0; out = []
    for c, l in zip(cw, L): out.append(dict(w=c, s=round(t, 3), e=round(t + d * l / tot, 3))); t += d * l / tot
    return out, " ".join(h.word.strip() for h in hw) + "  [proportional]"

timing = {"voice": VOICE, "speed": SPEED, "scenes": []}
for sc in SCENES:
    lead = 1.5 if sc["step"] else (0.6 if sc["id"] != "s01" else 1.4)
    out, t, rows = [np.zeros(int(lead * SR))], lead, []
    for j, ln in enumerate(sc["lines"]):
        cap, cue = ln[0], ln[1]; spoken = ln[2] if len(ln) > 2 else cap
        a = say(spoken, f"{sc['id']}_{j:02d}"); ws, heard = words_of(cap, a)
        rows.append(dict(i=j, text=cap, cue=cue, t0=round(t, 3), t1=round(t + len(a) / SR, 3), words=[dict(w=w["w"], s=round(t + w["s"], 3), e=round(t + w["e"], 3)) for w in ws], heard=heard))
        out.append(a); t += len(a) / SR
        g = 0.25 + 0.42 * EXTRA.get(sc["id"], {}).get(cue, 0)
        out.append(np.zeros(int(g * SR))); t += g
    t_tail = 0.2; out.append(np.zeros(int(t_tail * SR))); t += t_tail
    w = np.concatenate(out); sf.write(f"vo/{sc['id']}.wav", w, SR)
    timing["scenes"].append(dict(id=sc["id"], title=sc["title"], step=sc["step"], dur=round(len(w) / SR, 3), lines=rows))
    print(sc["id"], round(len(w) / SR, 1), "s |", " / ".join(f"{r['text']} => {r['heard']}" for r in rows), flush=True)
t = 0
for s in timing["scenes"]: s["start"] = round(t, 3); t += s["dur"]
timing["total"] = round(t, 3)
json.dump(timing, open("timing.json", "w"), indent=1, ensure_ascii=False); print("total", round(t, 1))
