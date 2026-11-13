# AI voiceover for one partner video: Kokoro-82M local (voice af_heart, speed 0.85), one clip per sentence, laid out with short
# pauses (longer before the next action); word timestamps from faster-whisper on each clip so rings land on "tap" / "check".
# Usage: python3 vo20.py v1_foca  -> v1_foca/vo/full.wav, v1_foca/timing.json
import sys, os, re, json, numpy as np, soundfile as sf, scipy.signal as ss
from kokoro_onnx import Kokoro
from faster_whisper import WhisperModel
import scripts20 as S
v = sys.argv[1]; VER = os.environ.get("VER", "v01"); D = (S.VIDEOS2 if VER == "v02" else S.VIDEOS)[v]; O = v if VER == "v01" else f"{v}/{VER}"; SR = 24000; SPEED = 0.85
K = Kokoro("/root/.cache/hyperframes/tts/models/kokoro-v1.0.onnx", "/root/.cache/hyperframes/tts/voices/voices-v1.0.bin")
WM = WhisperModel("small", device="cpu", compute_type="int8")
os.makedirs(f"{O}/vo/lines", exist_ok=True)
ACTION = re.compile(r"^(Tap|Sign|Check|Then|If|Read|Scroll|Pass|Enter|Type|Review|When|Next|First|Security emails|Keep|The witness|After|Before|Now|Don|Remember|In the app|Situation)")
LEAD, SCENE_GAP, TAIL = 0.5, 1.0, 1.4
GAP_ACT, GAP, BEAT = (0.95, 0.6, 0.35) if VER == "v01" else (0.8, 0.45, 0.3)
if VER != "v01": SCENE_GAP = 0.8
out, t, lines, scenes = [np.zeros(int(LEAD * SR))], LEAD, [], []
for si, sc in enumerate(D["scenes"]):
    title, slides, vo = (sc if len(sc) == 3 else (sc[0], sc[1], sc[1]))
    if si: out.append(np.zeros(int(SCENE_GAP * SR))); t += SCENE_GAP
    s0 = t; slv = vo if isinstance(vo, list) else [(None, vo)]
    tagged = [(n, x) for n, txt in slv for x in S.sentences(txt)]; sents = [x for _, x in tagged]
    for j, (sl_n, cap) in enumerate(tagged):
        if j and tagged[j - 1][0] != sl_n: out.append(np.zeros(int(BEAT * SR))); t += BEAT        # a beat between slides
        sp = S.spoken(cap); p = f"{O}/vo/lines/{si}_{j:02d}.wav"
        if os.path.exists(p) and open(p + ".txt").read() == f"{SPEED}|{sp}":
            a, _ = sf.read(p)
        else:
            a, sr = K.create(sp, voice="af_heart", speed=SPEED, lang="en-us")
            e = np.abs(a) > 0.01; a = a[max(0, np.argmax(e) - 720): len(a) - np.argmax(e[::-1]) + 1440]
            sf.write(p, a, SR); open(p + ".txt", "w").write(f"{SPEED}|{sp}")
        a16 = ss.resample_poly(a, 16000, SR).astype(np.float32)
        segs, _ = WM.transcribe(a16, language="en", beam_size=5, word_timestamps=True)
        words = [dict(w=re.sub(r"[^\w']", "", w.word).lower(), t=round(t + w.start, 3), e=round(t + w.end, 3)) for sg in segs for w in sg.words]
        lines.append(dict(scene=si, slide=sl_n, i=len(lines), text=cap, t0=round(t, 3), t1=round(t + len(a) / SR, 3), words=words))
        out.append(a); t += len(a) / SR
        if j < len(sents) - 1:
            g = GAP_ACT if ACTION.match(sents[j + 1]) else GAP
            out.append(np.zeros(int(g * SR))); t += g
    scenes.append(dict(title=title, slides=slides if isinstance(slides, str) else [n for n, _ in slides], t0=round(s0, 3), t1=round(t, 3)))
out.append(np.zeros(int(TAIL * SR))); t += TAIL
w = np.concatenate(out); sf.write(f"{O}/vo/full.wav", w, SR)
nw = sum(len(S.sentences(vo)[0:0]) for _ in []) or sum(len(l["text"].split()) for l in lines)
json.dump(dict(total=round(len(w) / SR, 3), words=nw, wpm=round(nw / (len(w) / SR) * 60, 1), scenes=scenes, lines=lines), open(f"{O}/timing.json", "w"), indent=1, ensure_ascii=False)
print(v, "total", round(len(w) / SR, 1), "s,", nw, "words,", round(nw / (len(w) / SR) * 60), "wpm overall")
