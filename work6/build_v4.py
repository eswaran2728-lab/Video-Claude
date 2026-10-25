# v04: clean version of v03 - temporally denoised source, stable refined matte (no edge boiling/halo),
# gentler relight, smoothed plate motion, no dust/grain.
# Titles still sit BEHIND the statue and never cover it.
# Same song-synced cut as v01 (build.py). Writes edit/index.html, edit/timing_map.json, edit/cues.json.
import json, os
FPS = 30
TOTAL = 16.6
HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.join(HERE, "edit")
GP = os.path.join(HERE, "grade_clean_attr.txt")
GRADE = open(GP).read().strip() if os.path.exists(GP) else ""
AD = "v4/"

# id, kind, asset stem, out_start, out_end, source_in, source_out, note
SEG = [
    ("A",  "video", "segA", 0.0,   1.31,  10.2,  11.5,  "hook: push-in, face comes in front of the title"),
    ("A2", "img",   "frzA", 1.31,  2.25,  11.5,  11.5,  "hook freeze, READY STOCK stamp on the beat"),
    ("B",  "video", "segB", 2.25,  4.91,  0.3,   2.96,  "zoom-out reveal, PAINTED STATUE behind the head"),
    ("C",  "video", "segC", 4.91,  8.15,  5.0,   8.24,  "orbit with tracked detail callouts"),
    ("D",  "video", "segD", 8.15,  9.21,  12.30, 13.36, "pull back toward the hand"),
    ("E",  "img",   "frzE", 9.21,  11.34, 13.4,  13.4,  "freeze + punch-in on the hand: WITH EETI IN HAND"),
    ("F",  "video", "segF", 11.34, 11.9,  13.4,  13.93, "pull back to the full statue"),
    ("G",  "img",   "frzG", 11.9,  TOTAL, 13.93, 13.93, "freeze; statue steps right for the price, end card, song outro"),
]
json.dump([dict(zip(["id", "kind", "asset", "out_start", "out_end", "source_in", "source_out", "note"], s)) for s in SEG],
          open(os.path.join(E, "timing_map.json"), "w"), indent=1)

TRACK = json.load(open(os.path.join(E, "track.json")))
SRC_C, OUT_C = 5.0, 4.91
# key, out_in, out_out, label, label (x, y) in the free space top-right
CALL = [
    ("necklace", 4.95, 6.3,  "GOLD-PAINTED<br>ORNAMENTS", 660, 300),
    ("waist",    6.3,  7.75, "RED &amp; GOLD<br>WAIST CLOTH", 660, 300),
]
g = (lambda: f' data-color-grading="{GRADE}"') if GRADE else (lambda: "")

layers, js, sfx = [], [], []
for sid, kind, stem, a, b, si, so, note in SEG:
    d = round(b - a, 4)
    layers.append(f"      <!-- {sid}: {note} -->")
    if kind == "video":
        layers.append(f'      <video id="bg{sid}" class="clip bgL" src="assets/{AD}{stem}_bg.mp4" muted playsinline data-start="{a}" data-duration="{d}" data-track-index="1"{g()}></video>')
        layers.append(f'      <video id="fg{sid}" class="clip fgL" src="assets/{AD}{stem}_fg.webm" muted playsinline data-start="{a}" data-duration="{d}" data-track-index="4"{g()}></video>')
    else:
        # freeze frames: the plate keeps its light moving (rays, lamp flicker), the statue is a still cut-out
        layers.append(f'      <video id="bg{sid}" class="clip bgL" src="assets/{AD}{stem}_bg.mp4" muted playsinline data-start="{a}" data-duration="{d}" data-track-index="1"{g()}></video>')
        layers.append(f'      <img id="fg{sid}" class="clip fgL" src="assets/{AD}{stem}_fg.png" alt="" data-start="{a}" data-duration="{d}" data-track-index="4"{g()} />')

# --- camera moves (both layers move together) -------------------------------
js += [
    'tl.fromTo(["#bgA2","#fgA2"],{scale:1},{scale:1.05,duration:0.94,ease:"none"},1.31);',
    'tl.fromTo(["#bgB","#fgB"],{scale:1.32},{scale:1,duration:0.45,ease:"expo.out"},2.25);',
    'tl.fromTo(["#bgE","#fgE"],{scale:1,x:0,y:0},{scale:1.7,x:0,y:-596,duration:0.4,ease:"power3.inOut"},9.24);',
    'tl.to(["#bgE","#fgE"],{scale:1,x:0,y:0,duration:0.4,ease:"power3.inOut"},10.94);',
    'tl.fromTo("#bgG",{scale:1},{scale:1.05,duration:%s,ease:"none"},11.9);' % round(TOTAL - 11.9, 3),
    # price beat: the statue (with its shadow/reflection) steps right to make room for the price
    'tl.set("#fgG",{transformOrigin:"50% 100%"},0);',
    'tl.fromTo("#fgG",{x:0,y:0,scale:1},{x:230,y:110,scale:0.75,duration:0.5,ease:"power3.inOut"},12.0);',
    'tl.to("#fgG",{scale:0.77,duration:%s,ease:"none"},12.5);' % round(TOTAL - 12.5, 3),
]

# --- tracked callouts --------------------------------------------------------
labels, pointers = [], []
for k, t0, t1, label, lx, ly in CALL:
    pts = TRACK[k]
    d = round(t1 - t0, 4)
    labels.append(f'      <div id="lb_{k}" data-layout-allow-overlap class="clip behind lab" data-start="{t0}" data-duration="{d}" data-track-index="3" style="inset:auto;left:{lx}px;top:{ly}px;width:250px">{label}</div>')
    # leader line behind the statue (it disappears where it crosses the body), dot in front on the detail
    labels.append(f'''      <div id="ld_{k}" data-layout-allow-overlap class="clip behind" data-start="{t0}" data-duration="{d}" data-track-index="2">
        <svg class="lead" width="1080" height="1920" viewBox="0 0 1080 1920"><line id="ln_{k}" x1="{lx + 20}" y1="{ly + 92}" x2="{lx + 20}" y2="{ly + 92}" /></svg>
      </div>''')
    pointers.append(f'''      <div id="co_{k}" class="clip front" data-start="{t0}" data-duration="{d}" data-track-index="6"><div class="dot" id="dt_{k}"></div></div>''')
    for fo in range(int(round(t0 * FPS)), int(round(t1 * FPS)) + 1):
        t = fo / FPS
        sf = str(int(round(SRC_C * FPS + (t - OUT_C) * FPS)))
        if sf not in pts:
            continue
        x, y = pts[sf]
        js.append(f'tl.set("#dt_{k}",{{x:{x - 14:.1f},y:{y - 14:.1f}}},{t:.4f});tl.set("#ln_{k}",{{attr:{{x2:{x:.1f},y2:{y:.1f}}}}},{t:.4f});')
    js.append(f'tl.fromTo("#dt_{k}",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(3)"}},{t0});')
    js.append(f'tl.fromTo("#ln_{k}",{{strokeDashoffset:700}},{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{t0 + 0.05});')
    js.append(f'tl.fromTo("#lb_{k}",{{opacity:0,x:24}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{t0 + 0.12});')
    js.append(f'tl.to(["#lb_{k}","#co_{k}","#ld_{k}"],{{opacity:0,duration:0.18}},{round(t1 - 0.18, 3)});')
    sfx.append(("tick", t0, 0.6))

# --- text ---------------------------------------------------------------------
js += [
    'tl.fromTo("#mast",{scale:1.04},{scale:1,duration:0.6,ease:"power3.out"},0);',
    'tl.to("#mast",{opacity:0,duration:0.15},1.16);',
    'tl.fromTo("#stamp",{scale:2.2,opacity:0,rotation:-14},{scale:1,opacity:1,rotation:-6,duration:0.26,ease:"back.out(2.2)"},1.31);',
    'tl.to("#stamp",{opacity:0,duration:0.15},2.1);',
    'tl.fromTo("#headB",{opacity:0,y:30},{opacity:1,y:0,duration:0.35,ease:"power3.out"},2.45);',
    'tl.fromTo("#pieceB",{opacity:0,x:-40},{opacity:1,x:0,duration:0.3,ease:"power3.out"},2.55);',
    'tl.to(["#headB","#pieceB"],{opacity:0,duration:0.2},4.7);',
    'tl.fromTo("#ring",{scale:0.3,opacity:0},{scale:1,opacity:1,duration:0.28,ease:"back.out(2)"},9.6);',
    'tl.fromTo("#eetiTxt",{opacity:0,x:-40},{opacity:1,x:0,duration:0.32,ease:"power3.out"},9.68);',
    'tl.fromTo("#eetiNote",{opacity:0,y:20},{opacity:1,y:0,duration:0.3,ease:"power3.out"},9.85);',
    'tl.to(["#ring","#eetiTxt","#eetiNote"],{opacity:0,duration:0.2},11.05);',
    'tl.fromTo("#endShade",{opacity:0},{opacity:1,duration:0.5},12.05);',
    'tl.fromTo("#priceTxt",{opacity:0,scale:0.6,x:-30},{opacity:1,scale:1,x:0,duration:0.42,ease:"back.out(1.8)"},12.2);',
    'tl.fromTo("#endTitle",{opacity:0,y:-20},{opacity:1,y:0,duration:0.4,ease:"power3.out"},12.4);',
    'tl.fromTo("#cta",{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"},13.69);',
    'tl.to("#cta",{scale:1.05,duration:0.36,ease:"sine.inOut",yoyo:true,repeat:3},14.16);',
    'tl.fromTo("#endNote",{opacity:0,y:20},{opacity:1,y:0,duration:0.35,ease:"power3.out"},13.85);',
]

# --- sound cues (t = first frame that shows the event) --------------------------
sfx += [
    ("hook-impact", 0.0, 0.55), ("thock", 1.31, 0.7), ("zoom-swish", 2.3, 0.4), ("ui-pop", 2.57, 0.35),
    ("camera-shutter-light", 9.21, 0.45), ("zoom-swish", 9.44, 0.4), ("ui-pop", 9.7, 0.35),
    ("zoom-swish", 12.25, 0.35), ("metallic-riser", 12.25, 0.3), ("sub-impact", 12.25, 0.7),
    ("ui-pop", 13.72, 0.35), ("clean-ding", 13.72, 0.3),
]
PEAK = {"zoom-swish": 0.139, "metallic-riser": 1.522, "ui-pop": 0.02}
DUR = {"hook-impact": 1.9, "metallic-riser": 1.64, "zoom-swish": 0.76, "sub-impact": 0.64,
       "clean-ding": 0.55, "ui-pop": 0.2, "tick": 0.09, "thock": 0.12, "camera-shutter-light": 0.16}
json.dump([{"sound": s, "t": t, "gain": gn} for s, t, gn in sfx], open(os.path.join(E, "cues.json"), "w"), indent=1)
audio = [f'      <audio id="sx{n}" class="clip" src="assets/sfx/{s}.wav" data-start="{max(0.0, round(t - PEAK.get(s, 0.0), 3))}" data-duration="{DUR[s]}" data-volume="{gn}"></audio>'
         for n, (s, t, gn) in enumerate(sfx)]

tpl = open(os.path.join(HERE, "index_v2.tpl.html")).read()  # same layout as v02
rep = {"%%TOTAL%%": TOTAL, "%%PRICED%%": round(TOTAL - 12.05, 3), "%%CTAD%%": round(TOTAL - 13.69, 3),
       "%%LAYERS%%": "\n".join(layers), "%%LABELS%%": "\n".join(labels), "%%POINTERS%%": "\n".join(pointers),
       "%%SFX%%": "\n".join(audio), "%%JS%%": "\n".join("      " + l for l in js)}
for k, v in rep.items():
    tpl = tpl.replace(k, str(v))
open(os.path.join(E, "index.html"), "w").write(tpl)
print("wrote", len(js), "tweens/sets;", len(sfx), "sfx cues")
