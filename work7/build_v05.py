# v05: v04 look + motion graphics that illustrate each spoken line, with matching b-roll under a graphics panel.
#  "50 keychains / giveaway"  -> 50-plane grid counting up + GIVEAWAY badge, b-roll: bunch of keychains in hand
#  "I designed ... multi-colour" -> blueprint: the plane outline draws itself, then fills black/red/white
#  "3 colours: red, black, white" -> the same plane turns isometric and explodes into its 3 layers (labels on the words)
#  "design and packaging / deliver" -> checklist, then a box closes and ships
#  "bulk orders ... DM me"     -> BULK ORDERS + DM button with typing dots
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.join(HERE, "edit")
exec(open(os.path.join(HERE, "edl.py")).read())
GRADE = open(os.path.join(HERE, "grade_v04_attr.txt")).read().strip()
g = lambda: f' data-color-grading="{GRADE}"'
FPS = 30
DLG = "dialogue_v03.wav"
def w(seg, src): return out_of(seg, src)
TCO, T50, TGIVE = w(0, 0.24), w(0, 5.18), w(0, 7.16)
TDES, TMULTI = w(1, 9.40), w(1, 12.14)
T3, TRED, TBLK, TWHT = w(2, 16.72), w(2, 18.36), w(2, 18.70), w(2, 19.20)
TDSG, TPKG, TASAP, TDLV = w(3, 6.80), w(3, 7.56), w(3, 9.80), w(3, 11.88)
TBULK, TDM = w(4, 35.86), w(4, 39.48)
S1, S2, S3, S4, S5 = [round(o[0], 3) for o in OUT]
END_T = V[-1][4]
SPLIT_T, SPLIT_END = round(w(0, 4.52), 3), round(S4, 3)            # graphics panel + b-roll pane section
FACE_END = SPLIT_T

# (id, kind, file, out_start, out_end, note)  kind: full | pane (lower half under the graphics panel)
VIS = [
    ("V1", "full", "vc4/V1.mp4", 0.0, 2.3, "hook: build plate slides out"),
    ("V2", "full", "vc4/V2.mp4", 2.3, FACE_END, "speaker: in the company I work at"),
    ("Ph", "pane", "v5/P_hand.mp4", FACE_END, S2, "a bunch of the keychains held to camera"),
    ("Pf", "pane", "v5/P_flex.mp4", S2, S3, "plate flexed, prints pop off"),
    ("Pp", "pane", "v5/P_pour.mp4", S3, round(S3 + 2.98, 3), "box poured: red + black"),
    ("Pm", "pane", "v5/P_macro.mp4", round(S3 + 2.98, 3), S4, "macro: red body, black base, white print"),
    ("V7", "full", "vc4/V7.mp4", S4, V[6][5], "a packed keychain"),
    ("V8", "full", "vc4/V8.mp4", V[7][4], V[7][5], "rows of packed keychains"),
    ("V9", "full", "vc4/V9.mp4", V[8][4], V[8][5], "the whole batch: bulk"),
    ("V10", "full", "vc4/V10.mp4", V[9][4], V[9][5], "speaker CTA"),
    ("V11", "full", "vc4/V11.mp4", V[10][4], V[10][5], "whip"),
    ("V12", "full", "vc4/V12.mp4", V[11][4], TOTAL, "end card"),
]
json.dump({"speech": [dict(zip(["out_start", "out_end", "clip", "src_in", "src_out"], s)) for s in OUT],
           "visual": [dict(zip(["id", "kind", "file", "out_start", "out_end", "note"], v)) for v in VIS]},
          open(os.path.join(E, "timing_map_v05.json"), "w"), indent=1)

vis, js = [], []
for vid, kind, f, o0, o1, note in VIS:
    d = round(o1 - o0, 3)
    vis.append(f"      <!-- {vid} ({kind}): {note} -->")
    if kind == "pane":
        vis.append(f'      <video id="m{vid}" class="clip src" src="assets/{f}" muted playsinline data-start="{o0}" data-duration="{d}" data-track-index="1" style="inset:auto;left:0;top:960px;width:1080px;height:960px"{g()}></video>')
    else:
        vis.append(f'      <video id="m{vid}" class="clip vid src" src="assets/{f}" muted playsinline data-start="{o0}" data-duration="{d}" data-track-index="1"{g()}></video>')

js += [
    'tl.fromTo("#mV1",{scale:1},{scale:1.07,duration:2.3,ease:"none"},0);',
    'tl.fromTo("#mV12",{scale:1.12},{scale:1.0,duration:%s,ease:"power2.out"},%s);' % (round(TOTAL - END_T, 3), END_T),
    'tl.set("#mV10",{transformOrigin:"50% 28%"},0);',
    f'tl.fromTo("#mV10",{{scale:1}},{{scale:1.07,duration:0.35,ease:"power2.out"}},{TDM - 0.05});',
    'tl.fromTo("#hook .k1",{scale:1.08},{scale:1,duration:0.5,ease:"power3.out"},0);',
    'tl.fromTo("#hook .k2",{opacity:0,y:18},{opacity:1,y:0,duration:0.3,ease:"power3.out"},0.35);',
    'tl.to("#hook",{opacity:0,duration:0.15},2.15);',
    # company chip
    'tl.fromTo("#coChip .chipg",{y:18,opacity:0},{y:0,opacity:1,duration:0.35,ease:"power3.out"},2.55);',
    # panel slides down over the speaker as the explanation starts
    f'tl.fromTo("#mgPanel",{{yPercent:-100}},{{yPercent:0,duration:0.45,ease:"power3.out"}},{SPLIT_T});',
    f'tl.fromTo("#mPh",{{yPercent:100}},{{yPercent:0,duration:0.45,ease:"power3.out"}},{SPLIT_T});',
]
# 50 grid
GRID_T = round(SPLIT_T + 0.25, 3)
js.append(f'tl.fromTo("#grid svg",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.16,stagger:0.014,ease:"back.out(2)"}},{GRID_T});')
for k in range(51):
    js.append(f'tl.set("#gN",{{textContent:"{k}"}},{round(GRID_T + k * 0.0145, 4)});')
js += [
    f'tl.fromTo("#gNum",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{GRID_T});',
    f'tl.fromTo("#gGift",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2)"}},{TGIVE});',
    f'tl.to("#mgGrid",{{opacity:0,duration:0.15}},{round(S2 - 0.1, 3)});',
]
# blueprint: outline draws on "designed", fills on "multi-colour"
js += [
    f'tl.fromTo("#bp",{{opacity:0}},{{opacity:1,duration:0.4}},{S2});',
    f'tl.set(["#iB","#redFill","#iW"],{{opacity:0}},0);',
    f'tl.fromTo("#lab1",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{S2 + 0.05});',
    f'tl.fromTo("#draw",{{strokeDashoffset:2600}},{{strokeDashoffset:0,duration:2.2,ease:"power1.inOut"}},{S2 + 0.1});',   # draws through "So I designed"
    f'tl.fromTo(["#dimH","#dimV"],{{scaleX:0,opacity:0}},{{scaleX:1,opacity:1,duration:0.5,ease:"power2.out"}},{TDES + 0.9});',
    f'tl.to("#lab1",{{opacity:0,y:-16,duration:0.2}},{TMULTI - 0.25});',
    f'tl.fromTo("#lab2",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{TMULTI - 0.05});',
    f'tl.to("#iB",{{opacity:1,duration:0.25}},{TMULTI});',
    f'tl.to("#redFill",{{opacity:1,duration:0.3}},{TMULTI + 0.15});',
    f'tl.to("#iW",{{opacity:1,duration:0.25}},{TMULTI + 0.35});',
    f'tl.to(["#draw","#dimH","#dimV"],{{opacity:0,duration:0.3}},{TMULTI + 0.2});',
    # 3 colours: same plane turns isometric, then explodes into its layers
    f'tl.to("#bp",{{opacity:0,duration:0.4}},{S3});',
    f'tl.to("#lab2",{{opacity:0,y:-16,duration:0.2}},{S3});',
    f'tl.to(["#mgPlane .li svg"],{{rotation:-45,duration:0.7,ease:"power2.inOut"}},{S3 + 0.1});',   # spin in plane first...
    f'tl.to([".li"],{{rotationX:55,duration:0.7,ease:"power2.inOut"}},{S3 + 0.1});',               # ...then tilt: true isometric
    f'tl.to([".lw"],{{x:-150,duration:0.7,ease:"power2.inOut"}},{S3 + 0.1});',
    f'tl.fromTo("#lab3",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{T3 - 0.05});',
    f'tl.to("#wW",{{y:-165,duration:0.55,ease:"power3.out"}},{T3});',
    f'tl.to("#wB",{{y:165,duration:0.55,ease:"power3.out"}},{T3});',
    f'tl.fromTo("#tR",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.25,ease:"power3.out"}},{TRED - 0.05});',
    f'tl.fromTo("#tB",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.25,ease:"power3.out"}},{TBLK - 0.05});',
    f'tl.fromTo("#tW",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.25,ease:"power3.out"}},{TWHT - 0.05});',
    f'tl.to(["#mgPlane","#mgLabel"],{{opacity:0,duration:0.2}},{round(S4 - 0.2, 3)});',
    f'tl.to("#mgPanel",{{yPercent:-100,duration:0.3,ease:"power2.in"}},{round(S4 - 0.3, 3)});',
]
# checklist, then the box closes and ships
SHIP_T = V[7][4]
js += [
    f'tl.fromTo("#checks .card",{{y:18}},{{y:0,duration:0.42,ease:"power3.out"}},{S4});',
    f'tl.fromTo("#p1",{{strokeDashoffset:60}},{{strokeDashoffset:0,duration:0.25,ease:"power2.out"}},{TDSG});',
    f'tl.fromTo("#p2",{{strokeDashoffset:60}},{{strokeDashoffset:0,duration:0.25,ease:"power2.out"}},{TPKG});',
    f'tl.to("#checks",{{opacity:0,duration:0.18}},{round(V[6][5] - 0.2, 3)});',
    f'tl.fromTo("#ship .card",{{y:18}},{{y:0,duration:0.42,ease:"power3.out"}},{SHIP_T});',
    f'tl.fromTo("#flapL",{{rotation:-70,svgOrigin:"14 44"}},{{rotation:0,duration:0.35,ease:"power2.in"}},{TASAP});',
    f'tl.fromTo("#flapR",{{rotation:70,svgOrigin:"106 44"}},{{rotation:0,duration:0.35,ease:"power2.in"}},{TASAP + 0.12});',
    f'tl.fromTo("#shipT",{{opacity:0,x:20}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{TASAP + 0.3});',
    f'tl.to("#box",{{x:40,duration:0.35,ease:"power2.in"}},{TDLV - 0.1});',
    f'tl.fromTo("#speed",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.25}},{TDLV - 0.05});',
    f'tl.fromTo("#shipT b",{{scale:1.25}},{{scale:1,duration:0.3,ease:"back.out(2)"}},{TDLV});',
    f'tl.fromTo("#bulk .h",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.32,ease:"power3.out"}},{TBULK - 0.05});',
    f'tl.to("#bulk",{{opacity:0,duration:0.18}},{round(V[8][5] - 0.2, 3)});',
    f'tl.fromTo("#dm .card",{{y:18,scale:0.85}},{{y:0,scale:1,duration:0.35,ease:"back.out(1.8)"}},{TDM});',
]
for n, d in enumerate(("#d1", "#d2", "#d3")):
    js.append(f'tl.fromTo("{d}",{{y:0,opacity:0.5}},{{y:-8,opacity:1,duration:0.25,yoyo:true,repeat:5,ease:"sine.inOut"}},{round(TDM + 0.35 + n * 0.12, 3)});')
js += [
    f'tl.fromTo("#endDim",{{opacity:0}},{{opacity:1,duration:0.35}},{END_T});',
    f'tl.fromTo("#end img",{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(1.6)"}},{END_T + 0.05});',
    f'tl.fromTo("#end .l1",{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"power3.out"}},{END_T + 0.15});',
    f'tl.fromTo("#end .l2",{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"power3.out"}},{END_T + 0.3});',
]
# light leaks on the two big transitions
leaks = []
for n, (t0, d) in enumerate(((2.05, 0.75), (V[10][4] - 0.1, 1.1))):
    leaks.append(f'      <div id="leak{n}" class="clip leak" data-start="{round(t0, 3)}" data-duration="{d}" data-track-index="4"><i class="a"></i><i class="g"></i></div>')
    js.append(f'tl.fromTo("#leak{n}",{{opacity:0,x:-140}},{{opacity:0.85,x:0,duration:{d / 2},ease:"sine.out"}},{round(t0, 3)});')
    js.append(f'tl.to("#leak{n}",{{opacity:0,x:120,duration:{d / 2},ease:"sine.in"}},{round(t0 + d / 2, 3)});')

# captions (English translation of the Tamil speech)
R = '<span class="sw r">red</span>'; K = '<span class="sw k">black</span>'; WH = '<span class="sw w">white</span>'
CAP = [
    (w(0, 0.24), w(0, 4.48), "In the company I work at,"),
    (w(0, 4.52), w(0, 7.66), "I needed <b>50 keychains</b> as a giveaway."),
    (w(1, 8.58), w(1, 11.56), "So I designed all of these:"),
    (w(1, 11.56), w(1, 14.75), "<b>multi-colour</b> keychains for them."),
    (w(2, 14.88), w(2, 17.90), "As you can see, every keychain here comes in <b>3 colours</b>:"),
    (w(2, 17.98), w(2, 19.90), f"{R}, {K} and {WH}."),
    (w(3, 6.22), w(3, 9.30), "I've done the <b>design</b> and <b>packaging</b>."),
    (w(3, 9.80), w(3, 12.84), "As soon as possible, I'll deliver them."),
    (w(4, 35.12), w(4, 37.40), "If you want <b>bulk orders</b> like this,"),
    (w(4, 37.54), w(4, 41.30), "contact me or <b>DM</b> me."),
]
caps = []
for i, (a, b, txt) in enumerate(CAP):
    top = 840 if SPLIT_T <= a < SPLIT_END else 1090
    caps.append(f'      <div id="cap{i}" class="clip cap" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="8"><div class="box" style="top:{top}px"><span class="t">{txt}</span></div></div>')
    js.append(f'tl.fromTo("#cap{i} .box",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.12,ease:"power2.out"}},{a});')

SFX = [("hook-impact", 0.0, 0.5), ("camera-shutter-light", 2.23, 0.4), ("ui-pop", 2.57, 0.3),
       ("zoom-swish", SPLIT_T + 0.2, 0.4), ("tick", GRID_T, 0.45), ("ui-pop", GRID_T + 0.72, 0.4), ("ui-pop", TGIVE, 0.4),
       ("shimmer", TDES + 0.3, 0.3), ("ui-pop", TMULTI, 0.35), ("zoom-swish", S3 + 0.45, 0.35),
       ("thock", T3, 0.55), ("tick", TRED - 0.05, 0.5), ("tick", TBLK - 0.05, 0.5), ("tick", TWHT - 0.05, 0.5),
       ("camera-shutter", S4 - 0.13, 0.35), ("ui-click", TDSG, 0.45), ("ui-click", TPKG, 0.45),
       ("thock", TASAP + 0.3, 0.6), ("zoom-swish", TDLV + 0.05, 0.4), ("ui-pop", TBULK - 0.05, 0.35), ("ui-pop", TDM, 0.35),
       ("zoom-swish", V[10][4] + 0.25, 0.45), ("clean-ding", END_T + 0.05, 0.35)]
PEAK = {"zoom-swish": 0.139, "ui-pop": 0.02, "shimmer": 0.284}
DUR = {"hook-impact": 1.9, "camera-shutter-light": 0.16, "camera-shutter": 0.3, "ui-pop": 0.2, "tick": 0.09, "ui-click": 0.12,
       "thock": 0.12, "zoom-swish": 0.76, "clean-ding": 0.55, "shimmer": 0.9}
json.dump([{"sound": s, "t": round(t, 3), "gain": gn} for s, t, gn in SFX], open(os.path.join(E, "cues_v05.json"), "w"), indent=1)
sfx = [f'      <audio id="sx{n}" class="clip" src="assets/sfx/{s}.wav" data-start="{max(0.0, round(t - PEAK.get(s, 0.0), 3))}" data-duration="{DUR[s]}" data-volume="{gn}"></audio>'
       for n, (s, t, gn) in enumerate(SFX)]

GRID = "".join('<svg viewBox="0 0 400 400"><use href="#plane" /></svg>' for _ in range(50))
rep = {"%%DLG%%": DLG, "%%LEAKS%%": "\n".join(leaks), "%%TOTAL%%": TOTAL, "%%SPEECH_END%%": SPEECH_END,
       "%%VISUALS%%": "\n".join(vis), "%%CAPTIONS%%": "\n".join(caps), "%%SFX%%": "\n".join(sfx),
       "%%JS%%": "\n".join("      " + l for l in js), "%%GRID%%": GRID,
       "%%CO_T%%": 2.5, "%%CO_D%%": round(FACE_END - 2.5, 3),
       "%%SPLIT_T%%": SPLIT_T, "%%SPLIT_D%%": round(SPLIT_END - SPLIT_T, 3),
       "%%GRID_T%%": SPLIT_T, "%%GRID_D%%": round(S2 - SPLIT_T, 3),
       "%%DES_T%%": S2, "%%DES_D%%": round(S4 - S2, 3), "%%PLANE_D%%": round(S4 - S2, 3),
       "%%CHK_T%%": S4, "%%CHK_D%%": round(V[6][5] - S4, 3),
       "%%SHIP_T%%": SHIP_T, "%%SHIP_D%%": round(V[7][5] - SHIP_T, 3),
       "%%BULK_T%%": round(TBULK - 0.05, 3), "%%BULK_D%%": round(V[8][5] - TBULK + 0.05, 3),
       "%%DM_T%%": TDM, "%%DM_D%%": round(V[9][5] - TDM, 3),
       "%%END_T%%": END_T, "%%END_D%%": round(TOTAL - END_T, 3)}
html = open(os.path.join(HERE, "index_v05.tpl.html")).read()
for k, v in rep.items():
    html = html.replace(k, str(v))
open(os.path.join(E, "index.html"), "w").write(html)
print("v05:", len(js), "tweens;", len(CAP), "captions;", len(SFX), "sfx; split", SPLIT_T, "-", SPLIT_END)
