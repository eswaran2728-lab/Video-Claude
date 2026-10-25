# Builds edit/index.html for the Sangili Karuppar product reel.
# Cut points are snapped to strong onsets of the supplied song (sangili_karupar_song.m4a, ~166 bpm).
# The output -> source timing map is written to edit/timing_map.json; sound cues to edit/cues.json.
import json, os
FPS = 30
TOTAL = 16.6
HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.join(HERE, "edit")
GP = os.path.join(HERE, "grade_attr.txt")
GRADE = open(GP).read().strip() if os.path.exists(GP) else ""
# v01 = original park footage, v02 = temple background composite (assets/v2/)
AD = os.environ.get("ASSET_DIR", "v2/")

# id, kind, asset, out_start, out_end, source_in, source_out, note
SEG = [
    ("A",  "video", "segA.mp4", 0.0,   1.31,  10.19, 11.5,  "hook: push-in to the face"),
    ("A2", "img",   "frzA.jpg", 1.31,  2.25,  11.5,  11.5,  "hook freeze on the face, READY STOCK stamp on the beat"),
    ("B",  "video", "segB.mp4", 2.25,  4.91,  0.3,   2.96,  "zoom-out reveal: full statue on its base"),
    ("C",  "video", "segC.mp4", 4.91,  8.15,  5.0,   8.24,  "orbit with tracked detail callouts"),
    ("D",  "video", "segD.mp4", 8.15,  9.21,  12.30, 13.36, "pull back toward the hand"),
    ("E",  "img",   "frzE.jpg", 9.21,  11.34, 13.4,  13.4,  "freeze + punch-in on the hand: WITH EETI IN HAND"),
    ("F",  "video", "segF.mp4", 11.34, 13.11, 13.4,  15.17, "pull back to the full statue, price reveal"),
    ("G",  "img",   "frzG.jpg", 13.11, TOTAL, 15.17, 15.17, "end card on the last frame, song outro"),
]
json.dump([dict(zip(["id", "kind", "asset", "out_start", "out_end", "source_in", "source_out", "note"], s)) for s in SEG],
          open(os.path.join(E, "timing_map.json"), "w"), indent=1)

TRACK = json.load(open(os.path.join(E, "track.json")))
SRC_C, OUT_C = 5.0, 4.91
# callouts: key, out_in, out_out, label, label box (x, y)
CALL = [
    ("necklace", 5.05, 6.6,  "GOLD-PAINTED<br>ORNAMENTS", 610, 600),
    ("waist",    6.6,  8.12, "RED &amp; GOLD<br>WAIST CLOTH", 620, 930),
]

def g():
    return f' data-color-grading="{GRADE}"' if GRADE else ""

slides, js, sfx = [], [], []
for sid, kind, asset, a, b, si, so, note in SEG:
    d = round(b - a, 4)
    if kind == "video":
        slides.append(f'      <!-- {sid}: {note} -->\n      <video id="m{sid}" class="clip vid src" src="assets/{AD}{asset}" muted playsinline data-start="{a}" data-duration="{d}" data-track-index="1"{g()}></video>')
    else:
        slides.append(f'      <!-- {sid}: {note} -->\n      <div id="s{sid}" class="clip still" data-start="{a}" data-duration="{d}" data-track-index="1"><div class="pz" id="pz{sid}" data-layout-allow-overflow><img class="src" src="assets/{AD}{asset}" alt=""{g()} /></div></div>')

# --- camera moves -----------------------------------------------------------
js += [
    'tl.fromTo("#pzA2",{scale:1},{scale:1.05,duration:0.94,ease:"none"},1.31);',
    'tl.fromTo("#mB",{scale:1.32},{scale:1,duration:0.45,ease:"expo.out"},2.25);',
    # eeti punch-in: fist at (100,880) on the still -> (170,900) at 1.7x, no exposed edge
    'tl.fromTo("#pzE",{scale:1,x:0,y:0},{scale:1.7,x:0,y:-596,duration:0.4,ease:"power3.inOut"},9.24);',
    'tl.to("#pzE",{scale:1,x:0,y:0,duration:0.4,ease:"power3.inOut"},10.94);',
    'tl.fromTo("#pzG",{scale:1},{scale:1.06,duration:%s,ease:"none"},13.11);' % round(TOTAL - 13.11, 3),
]

# --- tracked callouts -------------------------------------------------------
calls = []
for k, t0, t1, label, lx, ly in CALL:
    pts = TRACK[k]
    calls.append(f'''      <div id="co_{k}" class="clip callout" data-start="{t0}" data-duration="{round(t1 - t0, 4)}" data-track-index="5" style="inset:0">
        <svg class="lead" width="1080" height="1920" viewBox="0 0 1080 1920"><line id="ln_{k}" x1="{lx}" y1="{ly + 40}" x2="{lx}" y2="{ly + 40}" /></svg>
        <div class="dot" id="dt_{k}"></div>
        <div class="lab" id="lb_{k}" style="left:{lx}px;top:{ly}px">{label}</div>
      </div>''')
    for fo in range(int(round(t0 * FPS)), int(round(t1 * FPS)) + 1):
        t = fo / FPS
        sf = str(int(round(SRC_C * FPS + (t - OUT_C) * FPS)))
        if sf not in pts:
            continue
        x, y = pts[sf]
        js.append(f'tl.set("#dt_{k}",{{x:{x - 14:.1f},y:{y - 14:.1f}}},{t:.4f});tl.set("#ln_{k}",{{attr:{{x2:{x:.1f},y2:{y:.1f}}}}},{t:.4f});')
    js.append(f'tl.fromTo("#dt_{k}",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(3)"}},{t0});')
    js.append(f'tl.fromTo("#ln_{k}",{{strokeDashoffset:600}},{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{t0 + 0.05});')
    js.append(f'tl.fromTo("#lb_{k}",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{t0 + 0.12});')
    js.append(f'tl.to("#co_{k}",{{opacity:0,duration:0.18}},{round(t1 - 0.18, 3)});')
    sfx.append(("tick", t0, 0.6))

# --- text -------------------------------------------------------------------
js += [
    'tl.fromTo("#hookTitle",{scale:1.06},{scale:1,duration:0.6,ease:"power3.out"},0);',
    'tl.fromTo("#stamp",{scale:2.2,opacity:0,rotation:-14},{scale:1,opacity:1,rotation:-6,duration:0.26,ease:"back.out(2.2)"},1.31);',
    'tl.to("#hook",{opacity:0,y:-30,duration:0.18,ease:"power2.in"},2.07);',
    'tl.fromTo("#chipB",{opacity:0,y:40},{opacity:1,y:0,duration:0.35,ease:"power3.out"},2.52);',
    'tl.to("#chipB",{opacity:0,y:-20,duration:0.2},4.7);',
    'tl.fromTo("#ring",{scale:0.3,opacity:0},{scale:1,opacity:1,duration:0.28,ease:"back.out(2)"},9.6);',
    'tl.fromTo("#eetiL1",{opacity:0,y:50},{opacity:1,y:0,duration:0.32,ease:"power3.out"},9.7);',
    'tl.fromTo("#eetiL2",{opacity:0,y:30},{opacity:1,y:0,duration:0.32,ease:"power3.out"},9.98);',
    'tl.to("#ring",{opacity:0,duration:0.15},10.86);',
    'tl.to("#eeti",{opacity:0,y:20,duration:0.22,ease:"power2.in"},11.1);',
    'tl.fromTo("#price",{scale:0.55,opacity:0,y:-40},{scale:1,opacity:1,y:0,duration:0.4,ease:"back.out(1.8)"},12.05);',
    'tl.fromTo("#sheen",{xPercent:-160},{xPercent:260,duration:0.8,ease:"power2.inOut"},12.5);',
    'tl.to("#price",{y:-134,duration:0.45,ease:"power3.inOut"},13.11);',
    'tl.fromTo("#endDim",{opacity:0},{opacity:1,duration:0.5,ease:"power1.out"},13.11);',
    'tl.fromTo("#endT2",{opacity:0,y:30},{opacity:1,y:0,duration:0.4,ease:"power3.out"},14.16);',
    'tl.fromTo("#cta",{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"},13.69);',
    'tl.to("#cta",{scale:1.05,duration:0.36,ease:"sine.inOut",yoyo:true,repeat:3},14.16);',
    'tl.set("#sheen",{xPercent:-160},14.8);',
    'tl.to("#sheen",{xPercent:260,duration:0.8,ease:"power2.inOut"},14.86);',
]

# --- sound cues (t = first frame that shows the event) ----------------------
sfx += [
    ("hook-impact", 0.0, 0.55), ("thock", 1.31, 0.7), ("zoom-swish", 2.3, 0.4), ("ui-pop", 2.55, 0.35),
    ("camera-shutter-light", 9.21, 0.45), ("zoom-swish", 9.44, 0.4), ("ui-pop", 9.73, 0.35),
    ("metallic-riser", 12.05, 0.32), ("sub-impact", 12.05, 0.7), ("shimmer", 12.9, 0.3),
    ("ui-pop", 13.72, 0.35), ("clean-ding", 13.72, 0.3),
]
PEAK = {"zoom-swish": 0.139, "metallic-riser": 1.522, "shimmer": 0.284, "ui-pop": 0.02}
DUR = {"hook-impact": 1.9, "metallic-riser": 1.64, "shimmer": 0.9, "zoom-swish": 0.76, "sub-impact": 0.64,
       "clean-ding": 0.55, "ui-pop": 0.2, "tick": 0.09, "thock": 0.12, "camera-shutter-light": 0.16}
json.dump([{"sound": s, "t": t, "gain": gn} for s, t, gn in sfx], open(os.path.join(E, "cues.json"), "w"), indent=1)
audio = []
for n, (s_, t, gn) in enumerate(sfx):
    st = max(0.0, round(t - PEAK.get(s_, 0.0), 3))
    audio.append(f'      <audio id="sx{n}" class="clip" src="assets/sfx/{s_}.wav" data-start="{st}" data-duration="{DUR[s_]}" data-volume="{gn}"></audio>')

tpl = open(os.path.join(HERE, "index.tpl.html")).read()
rep = {"%%TOTAL%%": TOTAL, "%%ENDD%%": round(TOTAL - 13.11, 3), "%%PRICED%%": round(TOTAL - 12.05, 3),
       "%%CTAD%%": round(TOTAL - 13.69, 3), "%%SLIDES%%": "\n".join(slides), "%%CALLOUTS%%": "\n".join(calls),
       "%%SFX%%": "\n".join(audio), "%%JS%%": "\n".join("      " + l for l in js)}
for k, v in rep.items():
    tpl = tpl.replace(k, str(v))
open(os.path.join(E, "index.html"), "w").write(tpl)
print("wrote", len(js), "tweens/sets;", len(sfx), "sfx cues")
