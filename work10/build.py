# Cyber Roadshow 2026 event recap — HyperFrames composition (edit/index.html), 1080x1920, 30 fps, 25.4 s.
# Soundtrack = the event's own song from IMG_6421 (output time == song time, so stage clips stay in sync with it),
# cuts on its beat grid (~122 BPM: 0.280 + n*0.491 s), photos animated as slow pans/push-ins, three tip cards on the
# exact lyric lines, a beat-timed close built from the booth banner. Wording: content.json.
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
C = json.load(open("content.json"))
TOTAL = 25.4
B = lambda n: round(0.280 + n * 0.491, 3)                     # beat n
at = lambda t: round(t, 3)
PW, PH = 3840, 2160                                          # photo plate as displayed (scaled from 4267x2400)
js, init, layers = [], [], []
A, I = js.append, init.append

# ---------- footage (tracked 9:16 crops, see make_assets.py) ----------
VIDS = [("v_walk", 2.733, 4.205), ("v_stage1", 4.205, 9.603), ("v_stage2", 9.603, 12.547), ("v_stage3", 15.000, 16.472)]
for vid, a, b in VIDS:
    layers.append(f'      <video id="{vid}" class="clip vid" src="assets/v/{vid}.mp4" muted playsinline data-start="{a}" data-duration="{at(b - a)}" data-track-index="1"></video>')

# ---------- photos: 9:16 window over the landscape plate; pan (cx0 -> cx1, fraction of width) + gentle push ----------
PHOTOS = [  # id, file, start, end, cx0, cx1, push, note
    ("p1", "IMG_6426", 0.0, 2.733, 0.30, 0.40, 1.05, "launch on stage: pan along the guests to the button press"),
    ("p3", "IMG_6437", 16.472, 18.925, 0.37, 0.405, 1.06, "a visitor plays the booth game on the tablet"),
    ("p4", "IMG_6439", 18.925, 20.888, 0.36, 0.55, 1.04, "feedback on her phone + plane keychain, then the AVSEC staff member's thumbs-up"),
    ("p5", "IMG_6423", 20.888, TOTAL, 0.55, 0.86, 1.03, "booth wide, then the STOP. THINK. VERIFY. banner"),
]
for pid, f, a, b, c0, c1, push, note in PHOTOS:
    extra = ""
    if pid == "p4":   # highlight: phone ("Thank you for your feedback!") + keychain, in plate coordinates
        x0, y0, x1, y1 = 0.425 * PW, 0.43 * PH, 0.485 * PW, 0.68 * PH
        extra = f'<div class="ring" id="ring4" style="left:{x0:.0f}px;top:{y0:.0f}px;width:{x1 - x0:.0f}px;height:{y1 - y0:.0f}px"></div>'
    if pid == "p5":   # bracket around the banner wording
        x0, y0, x1, y1 = 0.878 * PW, 0.165 * PH, 0.995 * PW, 0.475 * PH
        extra = (f'<svg class="brk" id="brk5" style="left:{x0:.0f}px;top:{y0:.0f}px;width:{x1 - x0:.0f}px;height:{y1 - y0:.0f}px" viewBox="0 0 100 100" preserveAspectRatio="none">'
                 f'<path pathLength="1" d="M18,2 H2 V98 H18 M82,2 H98 V98 H82" /></svg>')
    layers.append(f'''      <!-- {pid}: {f} — {note} -->
      <div id="{pid}" class="clip ph" data-start="{a}" data-duration="{at(b - a)}" data-track-index="2"><div class="push" id="{pid}push"><div class="pan" id="{pid}pan">
        <img src="assets/p/{f}.jpg" alt="{note}" />{extra}</div></div></div>''')
    I(f'gsap.set("#{pid}pan",{{x:{540 - c0 * PW:.0f}}}); gsap.set("#{pid}push",{{transformOrigin:"540px 960px"}});')
    d = at(b - a)
    if pid == "p5":
        A(f'tl.to("#{pid}pan",{{x:{540 - c1 * PW:.0f},duration:1.25,ease:"power2.inOut"}},{a});')
        A(f'tl.fromTo("#{pid}push",{{scale:1.0}},{{scale:{push},duration:{d},ease:"none"}},{a});')
    else:
        A(f'tl.to("#{pid}pan",{{x:{540 - c1 * PW:.0f},duration:{d},ease:"{"power1.inOut" if pid == "p4" else "none"}"}},{a});')
        A(f'tl.fromTo("#{pid}push",{{scale:1.0}},{{scale:{push},duration:{d},ease:"none"}},{a});')

# deepfake talk: landscape slide shown whole as a card over its own blurred plate (a 9:16 crop would cut the slide)
layers.append('''      <!-- p2: IMG_6429 — "Anatomy of a deepfake attack" talk on stage, shown whole -->
      <div id="p2" class="clip ph" data-start="12.547" data-duration="2.453" data-track-index="2">
        <img class="bgblur" src="assets/p/IMG_6429.jpg" alt="" />
        <div class="card" id="p2card"><img id="p2img" src="assets/p/IMG_6429.jpg" alt="Anatomy of a deepfake attack talk" /></div>
      </div>''')
I('gsap.set("#p2card",{scale:0.92,opacity:0}); gsap.set("#p2img",{transformOrigin:"35% 45%"});')
A('tl.to("#p2card",{scale:1,opacity:1,duration:0.35,ease:"power3.out"},12.547);')
A('tl.fromTo("#p2img",{scale:1.0},{scale:1.12,duration:2.45,ease:"none"},12.547);')
I('gsap.set("#ring4",{opacity:0,scale:1.25,transformOrigin:"50% 50%"}); gsap.set("#brk5 path",{strokeDasharray:1,strokeDashoffset:1});')
A(f'tl.to("#ring4",{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.8)"}},{B(39) + 0.05});')
A('tl.to("#ring4",{opacity:0,duration:0.3},20.35);')
A(f'tl.to("#brk5 path",{{strokeDashoffset:0,duration:0.35,ease:"power2.out"}},{B(44) - 0.35});')

# ---------- opening title (lower third, clear of the guests' faces) ----------
t = C["title"]
title = "".join(f'<div class="tm"><div class="tl" id="tl{k}">{w}</div></div>' for k, w in enumerate(t["lines"]))
layers.append(f'''      <div id="title" class="clip" data-start="0" data-duration="2.733" data-track-index="5">
        <div class="scrim"></div>
        <div class="tbox"><div class="chip" id="tchip">{t["chip"]}</div>{title}<div class="tsub" id="tsub">{t["sub"]}</div></div>
      </div>''')
I('gsap.set("#title .tl",{yPercent:110}); gsap.set("#tchip,#tsub",{opacity:0,y:16});')
A('tl.to("#tchip",{opacity:1,y:0,duration:0.25,ease:"power2.out"},0.05);')
for k in range(len(t["lines"])):
    A(f'tl.to("#tl{k}",{{yPercent:0,duration:0.35,ease:"power4.out"}},{B(k)});')
A(f'tl.to("#tsub",{{opacity:1,y:0,duration:0.25,ease:"power2.out"}},{B(3)});')
A('tl.to("#title .tbox",{y:-40,opacity:0,duration:0.22,ease:"power2.in"},2.5);')

# ---------- three tip cards, on the lyric lines ----------
TIPS = [(B(7), 6.62), (B(20), 12.42), (15.000, 18.40)]
for k, (tip, (a, b)) in enumerate(zip(C["tips"], TIPS)):
    words = "".join(f'<span class="w">{w}</span> ' for w in tip["text"].split())
    layers.append(f'''      <div id="tip{k}" class="clip tip" data-start="{at(a)}" data-duration="{at(b - a + 0.05)}" data-track-index="6">
        <div class="tcard" id="tc{k}"><div class="tlab"><i>{k + 1:02d}</i>{tip["label"]}</div><div class="ttxt">{words}</div></div></div>''')
    I(f'gsap.set("#tc{k}",{{opacity:0,y:40,scale:0.94}}); gsap.set("#tc{k} .w",{{opacity:0,y:18}});')
    A(f'tl.to("#tc{k}",{{opacity:1,y:0,scale:1,duration:0.38,ease:"back.out(1.6)"}},{at(a)});')
    A(f'tl.to("#tc{k} .w",{{opacity:1,y:0,duration:0.25,stagger:0.07,ease:"power2.out"}},{at(a + 0.12)});')
    A(f'tl.to("#tc{k}",{{opacity:0,y:-24,duration:0.22,ease:"power2.in"}},{at(b - 0.2)});')

# ---------- close: banner words on the beat, then the AVSEC line ----------
c = C["close"]
cw = "".join(f'<div class="cm"><div class="cw c{k}" id="cw{k}">{w}</div></div>' for k, w in enumerate(c["words"]))
layers.append(f'''      <div id="close" class="clip" data-start="21.8" data-duration="{at(TOTAL - 21.8)}" data-track-index="7">
        <div class="dim" id="dim"></div>
        <div class="cbox">{cw}</div>
        <div class="lock" id="lock"><div class="org">{c["org"]}</div><div class="rule" id="rule"></div><div class="tag">{c["tagline"]}</div><div class="ev">{c["event"]}</div></div>
        <div class="black" id="black"></div>
      </div>''')
I('gsap.set("#dim",{opacity:0}); gsap.set("#close .cw",{yPercent:110}); gsap.set("#lock",{opacity:0,y:24}); gsap.set("#rule",{scaleX:0}); gsap.set("#black",{opacity:0});')
A(f'tl.to("#dim",{{opacity:1,duration:0.35,ease:"power1.out"}},{B(45) - 0.1});')
for k in range(3):
    A(f'tl.to("#cw{k}",{{yPercent:0,duration:0.32,ease:"power4.out"}},{B(45 + k)});')
A(f'tl.to("#lock",{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{B(48)});')
A(f'tl.to("#rule",{{scaleX:1,duration:0.35,ease:"power3.out"}},{B(48) + 0.1});')
A(f'tl.to("#black",{{opacity:1,duration:0.35,ease:"power1.in"}},{at(TOTAL - 0.35)});')

# ---------- sound: the event song + room tone (make_assets.py); a few soft cues on graphic events ----------
SFX = [(B(7), "ui-pop.wav", 0.22), (B(20), "ui-pop.wav", 0.22), (15.0, "ui-pop.wav", 0.22), (20.888, "zoom-swish.wav", 0.22), (B(47), "thock.wav", 0.35)]
sfx = "\n".join(f'      <audio id="sx{k}" class="clip" src="assets/sfx/{f}" data-start="{at(t)}" data-duration="0.8" data-volume="{v}"></audio>' for k, (t, f, v) in enumerate(SFX))

html = open("index.tpl.html").read()
for k, v in {"%%TOTAL%%": str(TOTAL), "%%LAYERS%%": "\n".join(layers), "%%SFX%%": sfx,
             "%%INIT%%": "\n".join("      " + x for x in init), "%%JS%%": "\n".join("      " + x for x in js)}.items():
    html = html.replace(k, v)
open("edit/index.html", "w").write(html)
tm = json.load(open("edit/assets_map.json"))
json.dump({"duration": TOTAL, "beat_grid": "0.280 + n*0.491 s",
           "timeline": [dict(out_start=a, out_end=b, source="IMG_6421.MOV", src_in=a, src_out=b, kind="video (tracked 9:16 crop)") for _, a, b in VIDS] +
                       [dict(out_start=a, out_end=b, source=f + ".DNG", kind="photo pan/push", note=n) for _, f, a, b, *_r, n in PHOTOS] +
                       [dict(out_start=12.547, out_end=15.0, source="IMG_6429.DNG", kind="photo card", note="deepfake talk slide shown whole")],
           "graphics": {"title": [0, 2.733], "tips": [[at(a), at(b)] for a, b in TIPS], "ring_IMG_6439": [B(39), 20.65], "bracket_banner": [B(44) - 0.35, TOTAL],
                        "close_words": [B(45), B(46), B(47)], "close_lockup": B(48)},
           "audio": tm["audio"], "sfx": [dict(t=at(t), file=f, gain=v) for t, f, v in SFX]}, open("edit/timing_map.json", "w"), indent=1)
chk = subprocess.run(["node", "-e", "const s=require('fs').readFileSync('edit/index.html','utf8');new Function(s.split('<script>')[1].split('</script>')[0])"], capture_output=True, text=True)
if chk.returncode: raise SystemExit("timeline JS does not parse:\n" + chk.stderr[-600:])
print("built", TOTAL, len(js), "tweens")
