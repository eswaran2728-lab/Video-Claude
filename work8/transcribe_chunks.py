# Retake/repeat check: split each clip at pauses (silencedetect) and transcribe every chunk on its own
# (Tamil auto, English, Tamil->English) so Whisper cannot copy one sentence over the next. -> chunks.json
import sys, json, subprocess, re, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
SR = 16000; out = {}
for n in sys.argv[1:] or ["d67f", "e5dd", "b5ae", "a336"]:
    log = subprocess.run(["ffmpeg", "-nostdin", "-i", f"proxy/{n}.mp4", "-af", "highpass=f=90,silencedetect=n=-34dB:d=0.32", "-f", "null", "-"], capture_output=True, text=True).stderr
    a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f"proxy/{n}.mp4", "-af", "highpass=f=90,lowpass=f=7500", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    dur = len(a) / SR
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]; se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    # speech chunks = gaps between silences
    edges = [0.0] + [v for p in zip(ss, se) for v in p] + [dur]
    chunks = [(edges[i], edges[i + 1]) for i in range(0, len(edges) - 1, 2) if edges[i + 1] - edges[i] > 0.25]
    out[n] = []
    print("==", n, flush=True)
    for s, e in chunks:
        x = a[int(max(0, s - 0.15) * SR):int(min(dur, e + 0.15) * SR)]
        r = {"s": round(s, 2), "e": round(e, 2)}
        for key, mode in (("ta", dict(language="ta")), ("en", dict(language="en")), ("tr", dict(language="ta", task="translate"))):
            segs, _ = m.transcribe(x, beam_size=5, condition_on_previous_text=False, **mode)
            r[key] = " ".join(t.text.strip() for t in segs)
        out[n].append(r)
        print(f"{s:6.2f}-{e:6.2f} | {r['ta']} | {r['en']} | {r['tr']}", flush=True)
json.dump(out, open("chunks.json", "w"), ensure_ascii=False, indent=1)
