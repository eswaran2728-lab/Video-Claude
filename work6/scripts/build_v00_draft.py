# Builds edit/index.html for the Sangili Karuppar product reel (v01).
# Output timeline (s, 30 fps) -> source (s) map is written to edit/timing_map.json.
import json, os
FPS = 30
TOTAL = 18.8
HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.join(HERE, "edit")
GRADE = open(os.path.join(HERE, "grade_attr.txt")).read().strip() if os.path.exists(os.path.join(HERE, "grade_attr.txt")) else ""

# id, kind, asset, out_start, out_end, source_in, source_out, note
SEG = [
    ("A",  "video", "segA.mp4", 0.0,  1.1,  10.4, 11.5, "hook: push-in to the face"),
    ("A2", "img",   "frzA.jpg", 1.1,  2.2,  11.5, 11.5, "hook freeze on the face, READY STOCK stamp"),
    ("B",  "video", "segB.mp4", 2.2,  5.6,  0.0,  3.4,  "zoom-out reveal: full statue on its base"),
    ("C",  "video", "segC.mp4", 5.6,  9.6,  5.0,  9.0,  "orbit with tracked detail callouts"),
    ("D",  "video", "segD.mp4", 9.6,  11.0, 12.0, 13.4, "pull back toward the hand"),
    ("E",  "img",   "frzE.jpg", 11.0, 13.6, 13.4, 13.4, "freeze + punch-in on the hand: WITH EETI IN HAND"),
    ("F",  "video", "segF.mp4", 13.6, 15.6, 13.4, 15.4, "pull back to the full statue, price reveal"),
    ("G",  "img",   "frzG.jpg", 15.6, TOTAL, 15.36, 15.36, "end card on the last frame"),
]
json.dump([dict(zip(["id", "kind", "asset", "out_start", "out_end", "source_in", "source_out", "note"], s)) for s in SEG],
          open(os.path.join(E, "timing_map.json"), "w"), indent=1)

TRACK = json.load(open(os.path.join(E, "track.json")))
SRC_C, OUT_C = 5.0, 5.6  # segment C mapping
# callouts: key, out_in, out_out, label, label box (x, y) on canvas
CALL = [
    ("necklace", 5.7, 7.1, "GOLD-PAINTED<br>ORNAMENTS", 610, 600),
    ("waist",    7.05, 8.45, "RED &amp; GOLD<br>WAIST CLOTH", 620, 930),
    ("rock",     8.4,  9.55, "ROCK<br>BASE", 640, 1160),
]

def g(attr=True):
    return f' data-color-grading="{GRADE}"' if (GRADE and attr) else ""

slides, js, sfx = [], [], []
for i, (sid, kind, asset, a, b, si, so, note) in enumerate(SEG):
    d = round(b - a, 4)
    if kind == "video":
        slides.append(f'      <!-- {sid}: {note} -->\n      <video id="m{sid}" class="clip vid src" src="assets/{asset}" muted playsinline data-start="{a}" data-duration="{d}" data-track-index="1"{g()}></video>')
    else:
        extra = ""
        if sid == "E":
            extra = ""
        slides.append(f'      <!-- {sid}: {note} -->\n      <div id="s{sid}" class="clip still" data-start="{a}" data-duration="{d}" data-track-index="1">{extra}<div class="pz" id="pz{sid}" data-layout-allow-overflow><img class="src" src="assets/{asset}" alt=""{g()} /></div></div>')

# --- camera moves -----------------------------------------------------------
js.append('tl.fromTo("#pzA2",{scale:1},{scale:1.05,duration:1.1,ease:"none"},1.1);')
js.append('tl.fromTo("#mB",{scale:1.32},{scale:1,duration:0.45,ease:"expo.out"},2.2);')
# eeti punch-in: fist at (100,880) on the still -> lands near (300,900) at 1.7x
js.append('tl.fromTo("#pzE",{scale:1,x:0,y:0},{scale:1.7,x:0,y:-596,duration:0.45,ease:"power3.inOut"},11.05);')
js.append('tl.to("#pzE",{scale:1,x:0,y:0,duration:0.45,ease:"power3.inOut"},13.15);')
js.append('tl.fromTo("#pzG",{scale:1},{scale:1.06,duration:%s,ease:"none"},15.6);' % round(TOTAL - 15.6, 3))

# --- tracked callouts -------------------------------------------------------
calls = []
for k, t0, t1, label, lx, ly in CALL:
    pts = TRACK[k]
    calls.append(f'''      <div id="co_{k}" class="clip callout" data-start="{t0}" data-duration="{round(t1 - t0, 4)}" data-track-index="5" style="inset:0">
        <svg class="lead" width="1080" height="1920" viewBox="0 0 1080 1920"><line id="ln_{k}" x1="{lx}" y1="{ly + 40}" x2="{lx}" y2="{ly + 40}" /></svg>
        <div class="dot" id="dt_{k}"></div>
        <div class="lab" id="lb_{k}" style="left:{lx}px;top:{ly}px">{label}</div>
      </div>''')
    # per-frame follow (source frame = 150 + (t - 5.6) * 30)
    f_first = int(round(t0 * FPS)); f_last = int(round(t1 * FPS))
    for fo in range(f_first, f_last + 1):
        t = fo / FPS
        sf = str(int(round(SRC_C * FPS + (t - OUT_C) * FPS)))
        if sf not in pts: continue
        x, y = pts[sf]
        js.append(f'tl.set("#dt_{k}",{{x:{x - 14:.1f},y:{y - 14:.1f}}},{t:.4f});tl.set("#ln_{k}",{{attr:{{x2:{x:.1f},y2:{y:.1f}}}}},{t:.4f});')
    js.append(f'tl.fromTo("#dt_{k}",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(3)"}},{t0});')
    js.append(f'tl.fromTo("#ln_{k}",{{strokeDashoffset:600}},{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{t0 + 0.05});')
    js.append(f'tl.fromTo("#lb_{k}",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{t0 + 0.12});')
    js.append(f'tl.to("#co_{k}",{{opacity:0,duration:0.18}},{t1 - 0.18});')
    sfx.append(("tick", t0, 0.55))

# --- text animation ---------------------------------------------------------
js += [
    # hook title is already settled at frame 0 (readable without sound), small settle drift
    'tl.fromTo("#hookTitle",{scale:1.06},{scale:1,duration:0.6,ease:"power3.out"},0);',
    'tl.fromTo("#stamp",{scale:2.2,opacity:0,rotation:-14},{scale:1,opacity:1,rotation:-6,duration:0.28,ease:"back.out(2.2)"},1.1);',
    'tl.to("#hook",{opacity:0,y:-30,duration:0.2,ease:"power2.in"},2.0);',
    'tl.fromTo("#chipB",{opacity:0,y:40},{opacity:1,y:0,duration:0.35,ease:"power3.out"},2.55);',
    'tl.to("#chipB",{opacity:0,y:-20,duration:0.2},5.35);',
    'tl.fromTo("#ring",{scale:0.3,opacity:0},{scale:1,opacity:1,duration:0.3,ease:"back.out(2)"},11.45);',
    'tl.fromTo("#eetiL1",{opacity:0,y:50},{opacity:1,y:0,duration:0.35,ease:"power3.out"},11.6);',
    'tl.fromTo("#eetiL2",{opacity:0,y:30},{opacity:1,y:0,duration:0.35,ease:"power3.out"},12.0);',
    'tl.to("#ring",{opacity:0,duration:0.15},13.05);',
    'tl.to("#eeti",{opacity:0,y:20,duration:0.25,ease:"power2.in"},13.3);',
    'tl.fromTo("#price",{scale:0.55,opacity:0,y:-40},{scale:1,opacity:1,y:0,duration:0.42,ease:"back.out(1.8)"},14.2);',
    'tl.fromTo("#sheen",{xPercent:-160},{xPercent:260,duration:0.8,ease:"power2.inOut"},14.75);',
    'tl.set("#sheen",{xPercent:-160},16.85);',
    'tl.to("#sheen",{xPercent:260,duration:0.8,ease:"power2.inOut"},16.9);',
    'tl.fromTo("#endDim",{opacity:0},{opacity:1,duration:0.5,ease:"power1.out"},15.6);',
    'tl.to("#price",{y:-134,duration:0.45,ease:"power3.inOut"},15.6);',
    'tl.fromTo("#endT2",{opacity:0,y:30},{opacity:1,y:0,duration:0.4,ease:"power3.out"},16.0);',
    'tl.fromTo("#cta",{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"},16.35);',
    'tl.to("#cta",{scale:1.05,duration:0.45,ease:"sine.inOut",yoyo:true,repeat:3},16.8);',
]

# --- sound cues (time = first frame that shows the event) --------------------
sfx += [
    ("hook-impact", 0.0, 0.8), ("thock", 1.1, 0.7), ("zoom-swish", 2.2, 0.55), ("ui-pop", 2.6, 0.45),
    ("camera-shutter-light", 11.0, 0.5), ("zoom-swish", 11.27, 0.5), ("ui-pop", 11.65, 0.45),
    ("metallic-riser", 14.2, 0.45), ("sub-impact", 14.2, 0.85), ("shimmer", 15.15, 0.4),
    ("ui-pop", 16.37, 0.45), ("clean-ding", 16.4, 0.4),
]
# file offset of each sound's hit, so the hit (not the file start) lands on the event frame
PEAK = {"zoom-swish": 0.139, "metallic-riser": 1.522, "shimmer": 0.284, "hook-impact": 0.0, "ui-pop": 0.02}
json.dump([{"sound": s, "t": t, "gain": gn} for s, t, gn in sfx], open(os.path.join(E, "cues.json"), "w"), indent=1)
DUR = {"hook-impact": 1.9, "metallic-riser": 1.64, "shimmer": 0.9, "zoom-swish": 0.76, "sub-impact": 0.64, "clean-ding": 0.55, "ui-pop": 0.2, "tick": 0.09, "thock": 0.12, "camera-shutter-light": 0.16}
audio = []
for n, (s_, t, gn) in enumerate(sfx):
    st = max(0.0, round(t - PEAK.get(s_, 0.0), 3))
    audio.append(f'      <audio id="sx{n}" class="clip" src="assets/sfx/{s_}.wav" data-start="{st}" data-duration="{DUR.get(s_, 0.3)}" data-volume="{gn}"></audio>')

tpl = open(os.path.join(HERE, "index.tpl.html")).read()
html = (tpl.replace("%%TOTAL%%", str(TOTAL)).replace("%%ENDD%%", str(round(TOTAL-15.6,3))).replace("%%PRICED%%", str(round(TOTAL-14.2,3))).replace("%%CTAD%%", str(round(TOTAL-16.35,3)))
        .replace("%%SLIDES%%", "\n".join(slides))
        .replace("%%CALLOUTS%%", "\n".join(calls))
        .replace("%%SFX%%", "\n".join(audio))
        .replace("%%JS%%", "\n".join("      " + l for l in js)))
open(os.path.join(E, "index.html"), "w").write(html)
print("wrote", len(js), "tweens/sets;", len(sfx), "sfx cues")
