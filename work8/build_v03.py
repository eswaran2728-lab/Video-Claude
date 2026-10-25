# v03 of the QUALITY / CHEAP / FAST explainer (writes edit/index.html) = v02 (no notebook photo, no earlier-shoot
# footage) + licensed stock b-roll on the two beats that v01 had b-roll on, after the creator allowed public-web b-roll:
# "you're going to buy a product" (phone shopping) and "if you're spending money with me" (a parcel being sealed).
# Stock: Mixkit Stock Video Free License (commercial use, no attribution required), checked on each item page.
# Every reveal is keyed to a word in the FINAL edited dialogue (word times from verify_cuts.json, re-based onto the
# output timeline with edl.out_of). Diagram: three labels + three PAIR loops (the idea of his notebook sketch: each loop
# encloses two labels). Selecting a pair = draw its loop, fill its two chips; the label left outside drops.
import json, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.join(HERE, "edit"); os.chdir(HERE)
exec(open("edl.py").read())
G = json.load(open("edit/geometry.json"))
GRADE = open("grade_attr.txt").read().strip()
LAB = G["labels"]
W = lambda seg, t: out_of(seg, OUT[seg][3] + t)        # word time inside an EDL piece (piece-relative) -> output time

# ---- speech-synced cue times (piece-relative times from verify_cuts.json) ----
T = dict(
    three=W(0, 0.60), two=W(0, 1.04),
    diagram=W(1, 1.68),
    Q=W(2, 0.48), C=W(2, 1.22), F=W(2, 2.48), psych=W(2, 3.98),
    things=W(3, 3.92),
    qc_q=W(4, 2.04), qc_c=W(4, 3.12), qc_f=W(4, 4.98),
    every=W(5, 0.24), withme=W(5, 1.92), three2=W(5, 4.82), two2=W(5, 5.44), drop=W(5, 6.72),
    qf_q=W(6, 1.18), qf_f=W(6, 2.04), qf_c=W(6, 5.60), sim=W(6, 6.84), cf_f=W(6, 8.28), cf_c=W(6, 8.88), cf_q=W(6, 9.84),
    ideol=W(7, 0.40), comment=W(7, 4.74),
)
SPLIT_END = OUT[1][0]                      # hook board+pane until "okay guys"
SK1 = (OUT[3][0], 12.2); SK2 = (23.1, 25.4)  # stock inserts
FULL1 = (OUT[5][0], SK2[0]); FULL2 = (43.3, SPEECH_END)
END_T = SPEECH_END; END_D = round(TOTAL - END_T, 3)

# ---- video layers ----
def g(): return f' data-color-grading="{GRADE}"'
tm = json.load(open("edit/timing_map_v03.json"))
vids = []
for s in tm["spans"]:
    o0, o1 = s["out_start"], s["out_end"]; d = round(o1 - o0, 3); sid, kind = s["id"], s["kind"]
    if kind == "pane":
        vids.append(f'      <video id="{sid}" class="clip pane" src="assets/v/{sid}.mp4" muted playsinline data-start="{o0}" data-duration="{d}" data-track-index="1" style="z-index:1"{g()}></video>')
    elif kind == "bubble":
        vids.append(f'      <video id="{sid}" class="clip cam" src="assets/v/{sid}.mp4" muted playsinline data-start="{o0}" data-duration="{d}" data-track-index="5" style="z-index:5"{g()}></video>')
    else:
        vids.append(f'      <video id="{sid}" class="clip vid" src="assets/v/{sid}.mp4" muted playsinline data-start="{o0}" data-duration="{d}" data-track-index="1" style="z-index:1"{g()}></video>')
for bl in tm["broll"]:
    o0, o1 = bl["out_start"], bl["out_end"]
    vids.append(f'      <!-- {bl["id"]}: {bl["note"]} -->')
    vids.append(f'      <video id="{bl["id"]}" class="clip vid" src="assets/v/{bl["id"]}.mp4" muted playsinline data-start="{o0}" data-duration="{round(o1 - o0, 3)}" data-track-index="2" style="z-index:1"{g()}></video>')

# ---- SVG: the three pair loops, their highlight strokes, and the dot ----
svg = []
for k, v in G["loops"].items():
    svg.append(f'            <path id="L{k}" class="loop" pathLength="1" d="{v["d_clean"]}" style="stroke:#b9b1a4;stroke-width:4" />')
for k, v in G["loops"].items():
    svg.append(f'            <path id="S{k}" class="sel" pathLength="1" d="{v["d_clean"]}" />')
CEN = (540, round((LAB["Q"][1] + 2 * LAB["C"][1]) / 3))
svg.append(f'            <circle id="dot" cx="{CEN[0]}" cy="{CEN[1]}" r="18" fill="#1c1b1a" stroke="#f1ece3" stroke-width="5" />')

NAMES = {"Q": "QUALITY", "C": "CHEAP", "F": "FAST"}; COL = {"Q": "#e4572e", "C": "#12936a", "F": "#2c5ddb"}
chips = []
for k in "QCF":
    chips.append(f'          <div id="c{k}" class="chip">{NAMES[k]}<div class="x"></div></div>')
for k in "QCF":
    chips.append(f'          <div id="t{k}" class="tag">× NOT {NAMES[k]}</div>')

# ---- timeline ----
js = []; A = js.append
def at(t): return round(t, 3)
INK, MUTE, DROPBG, DROPTX = "#1c1b1a", "#b9b1a4", "#d9d2c6", "#8e877b"
TAGPOS = {"Q": (540, LAB["Q"][1] - 90), "C": (LAB["C"][0], LAB["C"][1] + 96), "F": (LAB["F"][0], LAB["F"][1] + 96)}

# frame 0 state: split layout (board on top, speaker pane below), empty paper
init = []; I = init.append
I('gsap.set("#bw",{clipPath:"inset(0px 0px 910px 0px)"});')
I('gsap.set("#bc",{transformOrigin:"540px 655px",scale:0.78,y:-259});')
I('gsap.set("#dg path",{strokeDasharray:1,strokeDashoffset:1});')
I('gsap.set("#dot",{opacity:0});')
for k in "QCF":
    x, y = LAB[k]
    I(f'gsap.set("#c{k}",{{xPercent:-50,yPercent:-50,x:{x},y:{y},scale:0.6,opacity:0,backgroundColor:"{COL[k]}",color:"#ffffff"}});')
    I(f'gsap.set("#c{k} .x",{{scaleX:0}});')
    tx, ty = TAGPOS[k]
    I(f'gsap.set("#t{k}",{{xPercent:-50,yPercent:-50,x:{tx},y:{ty},opacity:0}});')
I('gsap.set(".cam",{transformOrigin:"50% 50%"});')
I('gsap.set("#full1",{transformOrigin:"45% 28%"});')
I('gsap.set("#sk1",{transformOrigin:"60% 70%"});')
I('gsap.set("#full2",{transformOrigin:"47% 26%"});')

# hook: slow push; the three labels pop in from the first words "இந்த மூனில" (of these three), the three pair loops
# (each holds two) draw on "two"
A(f'tl.to("#bc",{{scale:0.80,duration:{at(SPLIT_END)},ease:"none"}},0);')
for i, k in enumerate("QCF"):
    A(f'tl.to("#c{k}",{{scale:1,opacity:1,duration:0.32,ease:"back.out(1.8)"}},{at(0.05 + 0.15 * i)});')
for i, k in enumerate(["QC", "QF", "CF"]):
    A(f'tl.to("#L{k}",{{strokeDashoffset:0,duration:0.55,ease:"power1.inOut"}},{at(T["two"] + 0.15 * i)});')
for k in "QCF":
    A(f'tl.to("#c{k}",{{backgroundColor:"{INK}",duration:0.4}},{at(T["two"] + 0.9)});')

# "okay guys, a diagram": board opens to full screen, pane slides away, the face cam pops in under it, the dot arrives
A(f'tl.to("#bw",{{clipPath:"inset(0px 0px 0px 0px)",duration:0.5,ease:"power3.inOut"}},{at(SPLIT_END)});')
A(f'tl.to("#bc",{{scale:1,y:0,duration:0.5,ease:"power3.inOut"}},{at(SPLIT_END)});')
A(f'tl.to("#pane1",{{y:920,duration:0.45,ease:"power2.in"}},{at(SPLIT_END + 0.05)});')
A(f'tl.fromTo("#cam1",{{scale:0.5,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(1.7)"}},{at(SPLIT_END + 0.5)});')
A(f'tl.fromTo("#dot",{{opacity:0,attr:{{r:40}}}},{{opacity:1,attr:{{r:18}},duration:0.35,ease:"back.out(2)"}},{at(T["diagram"] - 0.1)});')
for k in G["loops"]:
    A(f'tl.to("#L{k}",{{stroke:"{INK}",strokeWidth:5,duration:0.4}},{at(T["diagram"] - 0.1)});')

# "this is quality, cheap and then fast": each label lights in its colour on its word; the previous one steps back
for k in "QCF":
    A(f'tl.to("#c{k}",{{backgroundColor:"{COL[k]}",scale:1.1,duration:0.2,ease:"power2.out"}},{at(T[k])});')
    A(f'tl.to("#c{k}",{{scale:1,duration:0.3}},{at(T[k] + 0.2)});')
for a, b_ in (("Q", "C"), ("C", "F")):
    A(f'tl.to("#c{a}",{{backgroundColor:"{INK}",opacity:0.55,duration:0.3}},{at(T[b_])});')
tidy = T["F"] + 0.6
for k in "QCF":
    A(f'tl.to("#c{k}",{{backgroundColor:"{INK}",opacity:1,duration:0.4}},{at(tidy)});')
for k in G["loops"]:
    A(f'tl.to("#L{k}",{{stroke:"{MUTE}",strokeWidth:4,duration:0.4}},{at(tidy)});')

def hop(k, t, d=0.3):
    x, y = LAB[k]; A(f'tl.to("#dot",{{attr:{{cx:{x},cy:{y - 74}}},duration:{d},ease:"back.out(1.6)"}},{at(t - 0.08)});')
def home(t): A(f'tl.to("#dot",{{attr:{{cx:{CEN[0]},cy:{CEN[1]}}},duration:0.4,ease:"power3.inOut"}},{at(t)});')
def fill(k, t): A(f'tl.to("#c{k}",{{backgroundColor:"{COL[k]}",opacity:1,scale:1.06,duration:0.22,ease:"power2.out"}},{at(t)});'); A(f'tl.to("#c{k}",{{scale:1,duration:0.3}},{at(t + 0.22)});')
def neutral(k, t, op=1): A(f'tl.to("#c{k}",{{backgroundColor:"{INK}",color:"#f1ece3",opacity:{op},y:{LAB[k][1]},rotation:0,scale:1,duration:0.3}},{at(t)});')
def select(p, t, dur=1.2):
    A(f'tl.to("#S{p}",{{strokeDashoffset:0,duration:{dur},ease:"power1.inOut"}},{at(t)});')
    A(f'tl.to("#L{p}",{{fill:"rgba(28,27,26,0.06)",duration:0.4}},{at(t)});')
    for q in G["loops"]:
        if q != p: A(f'tl.to("#L{q}",{{opacity:0.28,duration:0.3}},{at(t)});')
def unselect(p, t):
    A(f'tl.to("#S{p}",{{opacity:0,duration:0.25}},{at(t)});'); A(f'tl.set("#S{p}",{{strokeDashoffset:1,opacity:1}},{at(t + 0.3)});')
    A(f'tl.to("#L{p}",{{fill:"rgba(28,27,26,0)",duration:0.25}},{at(t)});')
    for q in G["loops"]: A(f'tl.to("#L{q}",{{opacity:1,duration:0.3}},{at(t)});')
def drop(k, t):
    A(f'tl.to("#c{k}",{{y:{LAB[k][1] + 18},rotation:-4,backgroundColor:"{DROPBG}",color:"{DROPTX}",opacity:1,duration:0.35,ease:"back.out(2)"}},{at(t)});')
    A(f'tl.to("#c{k} .x",{{scaleX:1,duration:0.25,ease:"power2.out"}},{at(t + 0.12)});')
    A(f'tl.fromTo("#t{k}",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.8)"}},{at(t + 0.3)});')
def undrop(k, t):
    neutral(k, t); A(f'tl.to("#c{k} .x",{{scaleX:0,duration:0.2}},{at(t)});'); A(f'tl.to("#t{k}",{{opacity:0,duration:0.25}},{at(t)});')

# stock: someone shopping on a phone for "you're going to buy a product"; back to the board on "remember these three things"
A(f'tl.set("#bw",{{autoAlpha:0}},{at(SK1[0])});'); A(f'tl.set("#bw",{{autoAlpha:1}},{at(SK1[1])});')
A(f'tl.fromTo("#sk1",{{scale:1.0}},{{scale:1.07,duration:{at(SK1[1] - SK1[0])},ease:"none"}},{at(SK1[0])});')
for i, k in enumerate("QCF"):                             # dot taps each of the three things
    tt = T["things"] + 0.27 * i
    hop(k, tt, 0.22); A(f'tl.to("#c{k}",{{backgroundColor:"{COL[k]}",opacity:1,duration:0.15}},{at(tt)});'); neutral(k, tt + 0.45, 0.55)
home(T["things"] + 1.2)

# QUALITY + CHEAP -> won't come FAST
for k in "QCF": neutral(k, OUT[4][0] + 0.2)
hop("Q", T["qc_q"]); fill("Q", T["qc_q"]); hop("C", T["qc_c"]); fill("C", T["qc_c"]); select("QC", T["qc_q"])
drop("F", T["qc_f"])

# him full frame for "every product" (punch in), then stock: a parcel being sealed for "if you're spending money with me"
A(f'tl.set("#bw",{{autoAlpha:0}},{at(FULL1[0])});')
A(f'tl.fromTo("#full1",{{scale:1.0}},{{scale:1.08,duration:0.4,ease:"power2.out"}},{at(T["every"])});')
A(f'tl.fromTo("#sk2",{{scale:1.08}},{{scale:1.0,duration:{at(SK2[1] - SK2[0])},ease:"power1.out"}},{at(SK2[0])});')
# reset the diagram while hidden, back for "choose two of three, drop one": each pair in turn, the third label steps out
rs = FULL1[0] + 0.1
unselect("QC", rs); undrop("F", rs); home(rs)
for k in "QC": neutral(k, rs)
A(f'tl.set("#bw",{{autoAlpha:1}},{at(SK2[1])});')
A(f'tl.to("#cQ,#cC,#cF",{{scale:1.08,duration:0.18,yoyo:true,repeat:1,ease:"power1.inOut"}},{at(T["three2"])});')
cyc = [("QC", "F"), ("QF", "C"), ("CF", "Q")]
for i, (p, out_k) in enumerate(cyc):
    tt = T["two2"] + 0.62 * i
    A(f'tl.to("#S{p}",{{strokeDashoffset:0,duration:0.32,ease:"power2.out"}},{at(tt)});')
    A(f'tl.to("#c{out_k}",{{opacity:0.25,duration:0.2}},{at(tt)});')
    A(f'tl.to("#S{p}",{{opacity:0,duration:0.2}},{at(tt + 0.5)});'); A(f'tl.set("#S{p}",{{strokeDashoffset:1,opacity:1}},{at(tt + 0.72)});')
    A(f'tl.to("#c{out_k}",{{opacity:1,duration:0.2}},{at(tt + 0.5)});')

# QUALITY + FAST -> not CHEAP
hop("Q", T["qf_q"]); fill("Q", T["qf_q"]); hop("F", T["qf_f"]); fill("F", T["qf_f"]); select("QF", T["qf_q"])
drop("C", T["qf_c"])
# similarly: FAST + CHEAP -> not QUALITY
sm = T["sim"] - 0.2
unselect("QF", sm); undrop("C", sm); neutral("Q", sm); neutral("F", sm); home(sm)
hop("F", T["cf_f"]); fill("F", T["cf_f"]); hop("C", T["cf_c"]); fill("C", T["cf_c"]); select("CF", T["cf_f"], 0.9)
drop("Q", T["cf_q"])

# resolution: all three pair loops and the three labels, stable, then back to him
rv = OUT[7][0] + 0.05
unselect("CF", rv); undrop("Q", rv)
for k in "QCF": A(f'tl.to("#c{k}",{{backgroundColor:"{COL[k]}",color:"#ffffff",opacity:1,duration:0.35}},{at(rv + 0.35)});')
for k in G["loops"]: A(f'tl.to("#L{k}",{{stroke:"{INK}",strokeWidth:5,duration:0.4}},{at(rv + 0.1)});')
home(rv)
A(f'tl.set("#bw",{{autoAlpha:0}},{at(FULL2[0])});')
A(f'tl.fromTo("#full2",{{scale:1.0}},{{scale:1.07,duration:0.4,ease:"power2.out"}},{at(T["comment"] - 0.1)});')
# end card
A(f'tl.fromTo("#end",{{opacity:0}},{{opacity:1,duration:0.35}},{at(END_T)});')
A(f'tl.fromTo("#end img",{{scale:0.9,opacity:0}},{{scale:1,opacity:1,duration:0.5,ease:"back.out(1.6)"}},{at(END_T + 0.1)});')
A(f'tl.fromTo("#end .l1,#end .l2,#end .l3",{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.4,stagger:0.12,ease:"power3.out"}},{at(END_T + 0.35)});')

# ---- captions: English translation of the Tamil, his English words kept; bottom-anchored ----
q, c, f, k_ = (lambda s: f'<b class="kq">{s}</b>'), (lambda s: f'<b class="kc">{s}</b>'), (lambda s: f'<b class="kf">{s}</b>'), (lambda s: f'<b class="kg">{s}</b>')
CAPS = [
    (0.0, SPLIT_END, f"Of these 3, you can only {k_('choose 2')}", "split"),
    (SPLIT_END, OUT[2][0], "Okay guys, here's a diagram", "full"),
    (OUT[2][0], T["psych"] - 0.75, f"This is {q('QUALITY')}, {c('CHEAP')} and {f('FAST')}", "full"),
    (T["psych"] - 0.75, OUT[3][0], "It's a psychology", "full"),
    (OUT[3][0], W(3, 1.54), "You're going to buy a product", "full"),
    (W(3, 1.54), W(3, 3.62), "If you want to buy it,", "full"),
    (W(3, 3.62), OUT[4][0], f"remember these {k_('3 things')}", "full"),
    (OUT[4][0], T["qc_f"] - 0.35, f"How? {q('QUALITY')} and {c('CHEAP')}", "full"),
    (T["qc_f"] - 0.35, OUT[5][0], f"won't come {f('FAST')}", "full"),
    (OUT[5][0], T["withme"], "You can use this for every product", "full"),
    (T["withme"], T["three2"] - 0.05, "If you're spending money with me,", "full"),
    (T["three2"] - 0.05, T["drop"], f"you have to {k_('choose 2 of 3')}", "full"),
    (T["drop"], OUT[6][0], f"and {k_('drop 1')}", "full"),
    (OUT[6][0], W(6, 3.4), f"If you want {q('QUALITY')} and {f('FAST')},", "full"),
    (W(6, 3.4), T["sim"] - 0.2, f"don't expect the price to be {c('CHEAP')}", "full"),
    (T["sim"] - 0.2, W(6, 9.5), f"Same way, if you want {f('FAST')} and {c('CHEAP')},", "full"),
    (W(6, 9.5), OUT[7][0], f"don't expect {q('QUALITY')}", "full"),
    (OUT[7][0], W(7, 3.3), "This is my ideology", "full"),
    (W(7, 3.3), SPEECH_END, "If you like it, comment below", "full"),
]
caps = []
for i, (a, b, html, mode) in enumerate(CAPS):
    bottom = 1920 - 985 if mode == "split" else 1920 - 1240
    caps.append(f'      <div id="cap{i}" class="clip cap" data-start="{at(a)}" data-duration="{at(b - a)}" data-track-index="8"><div class="box" style="bottom:{bottom}px"><span class="t">{html}</span></div></div>')
    if i == 1:   # "okay guys": starts at the hook position and rides down with the opening board, never over his face
        A(f'tl.fromTo("#cap{i} .box",{{y:-255,opacity:0}},{{opacity:1,duration:0.16}},{at(a)});')
        A(f'tl.to("#cap{i} .box",{{y:0,duration:0.5,ease:"power3.inOut"}},{at(a + 0.02)});')
    else:
        A(f'tl.fromTo("#cap{i} .box",{{y:14,opacity:0}},{{y:0,opacity:1,duration:0.16,ease:"power2.out"}},{at(a)});')

# ---- sound: one cue per visible event, on its first frame ----
SFX = [(T["three"], "ui-pop.wav", 0.45), (T["two"], "tick.wav", 0.7), (SPLIT_END + 0.02, "zoom-swish.wav", 0.4), (SPLIT_END + 0.5, "ui-pop.wav", 0.35)]
SFX += [(T[k], "ui-pop.wav", 0.5) for k in "QCF"]
SFX += [(T["things"] + 0.27 * i, "tick.wav", 0.55) for i in range(3)]
SFX += [(T["qc_q"], "tick.wav", 0.6), (T["qc_c"], "tick.wav", 0.6), (T["qc_q"] + 1.2, "latch.wav", 0.55), (T["qc_f"], "thock.wav", 0.8)]
SFX += [(T["two2"] + 0.62 * i, "tick.wav", 0.45) for i in range(3)]
SFX += [(T["qf_q"], "tick.wav", 0.6), (T["qf_f"], "tick.wav", 0.6), (T["qf_q"] + 1.2, "latch.wav", 0.55), (T["qf_c"], "thock.wav", 0.8)]
SFX += [(T["cf_f"], "tick.wav", 0.6), (T["cf_c"], "tick.wav", 0.6), (T["cf_f"] + 0.9, "latch.wav", 0.55), (T["cf_q"], "thock.wav", 0.8)]
SFX += [(END_T + 0.1, "clean-ding.wav", 0.45)]
DUR = {}
import soundfile as sf
sfx = []
for i, (t, fn, v) in enumerate(SFX):
    DUR.setdefault(fn, round(sf.info(f"edit/assets/sfx/{fn}").duration, 3))
    sfx.append(f'      <audio id="sfx{i}" class="clip" src="assets/sfx/{fn}" data-start="{at(t)}" data-duration="{DUR[fn]}" data-volume="{v}"></audio>')

html = open("index_v02.tpl.html").read()
for k, v in {"%%VIDEOS%%": "\n".join(vids), "%%SVG%%": "\n".join(svg), "%%CHIPS%%": "\n".join(chips), "%%CAPTIONS%%": "\n".join(caps),
             "%%SFX%%": "\n".join(sfx), "%%JS%%": "\n".join("      " + j for j in js), "%%INIT%%": "\n".join("      " + j for j in init), "%%TOTAL%%": str(TOTAL), "%%SPEECH_END%%": str(SPEECH_END),
             "%%END_T%%": str(END_T), "%%END_D%%": str(END_D), "%%BOARD_D%%": str(FULL2[0]),
             "%%SKX%%": "0", "%%SKY%%": "0", "%%SKH%%": "0"}.items():
    html = html.replace(k, v)
open("edit/index.html", "w").write(html)          # render entry (each version's builder writes it)
json.dump({"cues": {k: v for k, v in T.items()}, "captions": [dict(start=at(a), end=at(b), text=h) for a, b, h, m in CAPS],
           "sfx": [dict(t=at(t), file=fn, gain=v) for t, fn, v in SFX]}, open("edit/cues_v03.json", "w"), indent=1)
print("built", TOTAL, len(js), "tweens", len(CAPS), "captions", len(SFX), "sfx")
# guard: a JS syntax error freezes every animated layer in the render, so refuse to leave a broken composition
import subprocess
chk = subprocess.run(["node", "-e", "const s=require('fs').readFileSync('edit/index.html','utf8');new Function(s.split('<script>')[1].split('</script>')[0])"], capture_output=True, text=True)
if chk.returncode: raise SystemExit("timeline JS does not parse:\n" + chk.stderr[-600:])
