# Re-transcribe the source in phrase chunks (split at the pauses found in transcript.json): the one-pass Tamil output was garbled
# and the one-pass translation flipped a line's meaning. Each chunk: Tamil without a prompt, Tamil with a neutral Tanglish prompt
# (only words already heard in the English pass), English transcription. -> transcript_chunks.json
import json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('large-v3', device='cpu', compute_type='int8')
CH = [(0.0, 4.95), (4.95, 12.1), (12.1, 15.85), (15.85, 21.1), (21.1, 25.25), (25.25, 29.7), (29.7, 32.75)]
a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "proxy/src30.mov", "-af", "highpass=f=90,lowpass=f=7500",
                                  "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
P = "Call பேசும்போது noise இருக்கும். Office, car. Earbuds, TikTok, noise cancelling, two microphones, link, purchase."
out = []
for s, e in CH:
    seg = a[int(s * 16000):int(e * 16000)]; r = {"start": s, "end": e}
    for name, kw in [("ta", dict(language="ta")), ("ta_prompt", dict(language="ta", initial_prompt=P)), ("en", dict(language="en"))]:
        segs, _ = m.transcribe(seg, beam_size=5, word_timestamps=True, condition_on_previous_text=False, temperature=0, **kw)
        segs = list(segs); r[name] = " ".join(x.text.strip() for x in segs)
        r[name + "_words"] = [{"w": w.word, "s": round(s + w.start, 2), "e": round(s + w.end, 2), "p": round(w.probability, 2)} for x in segs for w in x.words]
        print(f"{s:5.2f}-{e:5.2f} {name:10s} {r[name]}", flush=True)
    out.append(r)
json.dump(out, open("transcript_chunks.json", "w"), ensure_ascii=False, indent=1)
