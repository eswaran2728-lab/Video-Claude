# v01 of the earbuds reel -> edit/index.html (HyperFrames 0.8.193), edit/cues.json (SFX cue sheet), edit/timing_map.json.
# Layer stack: graded/framed camera plate (make_plate.py) -> one carried graphic system -> Romanized Tanglish captions.
# Every graphic is keyed to a word he says (source word times -> output with plan.s2o):
#   hook   "background-la noise ... disturbance-aa irukka?"  orange noise bars + kinetic NOISE that turns on "disturbance"
#   context "office-la ... car-la ... call pesurappa ... romba noise"  office/car chips merge into a call pill, noise returns
#   turn   "so, athukkuthaan ... earbuds"  the noise collapses to a dot that flies onto the real case and opens as a ring
#   features "noise cancelling" / "two microphones"  two labels, one at a time; the bars inside the first one go flat
#   payoff "call ... noise cancel aayi"  noise around the call pill flattens into a clean line;
#          "thelivaa vilangum" / "ungalukkum avanga pesurathu"  the line links NEENGA and AVANGA, pulse each way; "clear-aa"
#   CTA    "keezha link-ku click panni"  the link strip folds into a link pill with a down arrow; pressed on "click"
# Graphics are explanations (drawn shapes), not product evidence; the product shown is only his real footage.
import os, json, random, html
# v02 (VERSION=v02): same cut/graphics/captions; face-lit plate (plate_v02.mp4) and the voice-isolated mix (mix_v02.wav).
# Its creative grade is then persisted on #plate with `hyperframes media-treatment` (grade_v02.json, see README).
VERSION = os.environ.get("VERSION", "v01"); SUF = "" if VERSION == "v01" else "_" + VERSION
import plan
from captions import CAPS
S = plan.s2o
TOTAL = plan.TOTAL
R = lambda v: round(v, 3)

T = dict(noise=S(1.86), dist=S(4.04), reset=4.42, office=S(5.67), car=S(6.83), call=S(10.15), noise2=S(11.33), so=S(12.36),
         lift=S(13.10), earbuds=S(13.90), ring_end=15.62, nc=S(18.19), flat=S(18.78), two=S(19.53), feat_end=S(21.25),
         call2=S(22.18), cancel=S(23.50), neenga=S(24.48), thel=S(26.66), avanga=S(27.74), clear=S(29.40),
         keezha=S(30.84), click=S(31.56))
# Measured on v01 snapshots: eyes ~610, mouth ~860, chin ~945 (wide). Captions go above the eyes (top 290, mostly hair/
# wall behind them); graphics sit between the chin and the hands/product, which is held left (x<400, y>1100) or at chest.
GY = 1020                                    # features, payoff link, CTA
GH = 1150                                    # hook: NOISE word + bars over the chest (no product yet)
GC = 1110                                    # context chips / call pill
LAV, ORG, INK, WHITE = "#c9a8ff", "#ff8a4c", "#1c1029", "#f7f3ff"

T["link_out"] = T["keezha"] - 0.45
# ---------------- noise bars: one SVG path, 30 vertical strokes; heights keyed every 0.12 s (seeded, deterministic) ----
NB, BW, PITCH = 30, 600, 20
def bars_d(h, cy=80):
    return " ".join(f"M{10 + i * PITCH} {R(cy - h[i] / 2)} L{10 + i * PITCH} {R(cy + h[i] / 2)}" for i in range(NB))
rnd = random.Random(11)
def noisy(amp, mask=None):
    h = [max(4, amp * (0.25 + 0.75 * rnd.random()) * 140) for _ in range(NB)]
    if mask: h = [v if mask(i) else 4 for i, v in enumerate(h)]
    return h
FLAT = [4] * NB

# ---------------- captions ----------------
caps_html, caps_js = [], []
for i, (a, b, txt, kw) in enumerate(CAPS):
    o0 = 0.0 if i == 0 else S(a); o1 = TOTAL if b > 90 else S(min(b, CAPS[i + 1][0] if i + 1 < len(CAPS) else b))
    if o1 is None: o1 = 15.90
    t = html.escape(txt)
    if kw: t = t.replace(html.escape(kw), f'<em>{html.escape(kw)}</em>', 1)
    caps_html.append(f'      <div id="c{i}" class="cap"><span class="t">{t}</span></div>')
    caps_js.append((i, R(o0), R(o1)))

# ---------------- ring track (reveal window) ----------------
ring = []
for n in range(round((T["earbuds"] - 0.40) * 30), round(T["ring_end"] * 30) + 1, 2):   # every 2nd output frame
    t = n / 30; c = plan.case_src(plan.o2s(t))
    if c:
        x, y, s = plan.to_out(t, c[0], c[1]); r = 0.42 * c[2] * plan.BASE * s
        ring.append((R(t), R(x), R(y), R(2 * r)))

# ---------------- cue sheet (SFX), out seconds = the frame the event becomes visible ----------------
CUES = [
    (0.0, "hook-impact", -16), (T["noise"], "thock", -9), (T["dist"], "tick", -12),
    (T["office"], "ui-pop", -14), (T["car"], "ui-pop", -14), (T["call"], "ui-click", -15),
    (12.65, "zoom-swish", -15), (T["earbuds"], "ui-pop", -12),
    (15.90 - 2 / 30, "camera-shutter-light", -17),
    (T["nc"], "ui-pop", -13), (T["flat"] + 0.30, "latch", -13), (T["two"], "ui-pop", -13),
    (T["call2"], "ui-pop", -14), (T["cancel"] + 0.32, "latch", -12),
    (T["thel"], "tick", -14), (T["avanga"], "tick", -14), (T["clear"], "clean-ding", -15),
    (T["keezha"], "ui-pop", -13), (T["click"], "ui-click", -11),
]
json.dump({"cues": [{"t": R(a), "sfx": b, "gain_db": g} for a, b, g in CUES]}, open("edit/cues.json", "w"), indent=1)

# ---------------- timeline JS ----------------
js, init = [], []
A, I = js.append, init.append
def tw(sel, t, d, props, ease="power3.out"):
    p = ",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())
    A(f'tl.to("{sel}",{{{p},duration:{R(d)},ease:"{ease}"}},{R(t)});')
def st(sel, t, props):
    p = ",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())
    A(f'tl.set("{sel}",{{{p}}},{R(t)});')

# captions: quick fade/rise in, instant out at the next caption
I('gsap.set(".cap",{opacity:0});')
for i, o0, o1 in caps_js:
    if i == 0: I('gsap.set("#c0",{opacity:1});')
    else:
        st(f"#c{i}", o0, {"opacity": 0, "y": 10}); tw(f"#c{i}", o0, 0.14, {"opacity": 1, "y": 0}, "power2.out")
    if o1 < TOTAL - 0.01: st(f"#c{i}", o1, {"opacity": 0})

# --- hook: bars (frame 0 already live), NOISE word, disturbance
I(f'gsap.set("#nz",{{x:0,y:0,scale:1,opacity:1}}); gsap.set("#nzp",{{attr:{{d:"{bars_d(noisy(0.35))}"}},stroke:"{ORG}"}});')
I('gsap.set("#nword",{opacity:0,scale:1.35,filter:"blur(14px)"});')
k = 0.12; t = 0.12
while t < T["reset"]:
    amp = 0.35 if t < T["noise"] else (0.72 if t < T["dist"] else 1.0)
    tw("#nzp", t - k, k, {"attr": {"d": bars_d(noisy(amp))}}, "sine.inOut"); t += k
tw("#nword", T["noise"], 0.34, {"opacity": 1, "scale": 1, "filter": "blur(0px)"}, "expo.out")
tw("#nword", T["dist"], 0.25, {"color": ORG}, "power2.out")
tw("#nword", T["dist"], 0.25, {"scaleX": 1.07}, "power2.out")
# reset on "okay": the word and the bars collapse into the centre dot, which then hides
tw("#nword", T["reset"], 0.28, {"scale": 0.2, "opacity": 0}, "power3.in")
tw("#nzp", T["reset"], 0.28, {"attr": {"d": bars_d(FLAT)}}, "power3.in")
tw("#nz", T["reset"], 0.30, {"scaleX": 0.02}, "power3.in")
I('gsap.set("#dot",{opacity:0,scale:0,x:0,y:0});')
st("#dot", T["reset"] + 0.22, {"opacity": 1, "scale": 1}); tw("#dot", T["reset"] + 0.30, 0.22, {"scale": 0, "opacity": 0}, "power2.in")

# --- context: office chip, car chip, they merge into the call pill
I('gsap.set("#office",{x:0,opacity:0,y:18}); gsap.set("#car",{x:0,opacity:0,y:18}); gsap.set("#call",{xPercent:-50,yPercent:-50,opacity:0,scale:0.6});')
tw("#office", T["office"], 0.42, {"opacity": 1, "y": 0}, "power3.out")
tw("#car", T["car"], 0.42, {"opacity": 1, "y": 0}, "power3.out")
tw("#office", T["call"] - 0.05, 0.40, {"x": 198, "scale": 0.7, "opacity": 0}, "power3.inOut")
tw("#car", T["call"] - 0.05, 0.40, {"x": -177, "scale": 0.7, "opacity": 0}, "power3.inOut")
tw("#call", T["call"] + 0.12, 0.40, {"opacity": 1, "scale": 1}, "back.out(1.4)")
# "romba noise": bars come back around the pill (centre strokes hidden behind the pill)
st("#nz", T["noise2"] - 0.01, {"scaleX": 1, "opacity": 1, "y": GC - GH})
mid = lambda i: i < 9 or i > 20
t = T["noise2"]
while t + 0.12 <= T["so"] + 1e-6:
    tw("#nzp", t, 0.12, {"attr": {"d": bars_d(noisy(0.8, mid))}}, "sine.inOut"); t += 0.12
# "so, athukkuthaan": pill + bars collapse to the dot; the dot flies onto the real case and opens into the ring
tw("#nzp", T["so"], 0.30, {"attr": {"d": bars_d(FLAT)}}, "power3.in"); tw("#nz", T["so"], 0.32, {"scaleX": 0.02, "opacity": 0}, "power3.in")
tw("#call", T["so"], 0.32, {"scale": 0.12, "opacity": 0}, "power3.in")
st("#dot", T["so"] + 0.26, {"x": 0, "y": GC - GH, "opacity": 1, "scale": 1})
r0 = ring[0]
lab_x = lambda x: R(max(x, 230))           # label sits under the ring, kept inside the left safe edge
tw("#dot", T["lift"], T["earbuds"] - T["lift"], {"x": R(r0[1] - 540), "y": R(r0[2] - GH)}, "power3.inOut")
I(f'gsap.set("#ring",{{xPercent:-50,yPercent:-50,opacity:0,x:{r0[1]},y:{r0[2]},width:20,height:20}}); gsap.set("#rlab",{{xPercent:-50,opacity:0,x:{lab_x(r0[1])},y:{R(r0[2] + r0[3] / 2 + 22)}}});')
st("#dot", T["earbuds"], {"opacity": 0})
st("#ring", T["earbuds"], {"opacity": 1})
first = True
for (tt, x, y, d) in ring:
    if tt < T["earbuds"]: continue
    if first:
        tw("#ring", tt, 0.30, {"width": d, "height": d, "x": x, "y": y}, "back.out(1.6)"); first = False; t_ring0 = tt + 0.30
    elif tt >= t_ring0:
        tw("#ring", tt, 0.066, {"width": d, "height": d, "x": x, "y": y}, "none")
    if tt >= T["earbuds"] + 0.16:
        tw("#rlab", tt, 0.066, {"x": lab_x(x), "y": R(y + d / 2 + 22)}, "none")
tw("#rlab", T["earbuds"] + 0.16, 0.30, {"opacity": 1}, "power2.out")
tw("#ring", T["ring_end"], 0.22, {"opacity": 0, "scale": 1.15}, "power2.in"); tw("#rlab", T["ring_end"], 0.22, {"opacity": 0}, "power2.in")

# --- features: two labels, one at a time; the bars inside label 1 flatten on "cancelling"
I('gsap.set("#fA,#fB",{xPercent:-50,opacity:0,y:24}); gsap.set("#clear,#cta",{xPercent:-50});')
mini = lambda h: " ".join(f"M{4 + i * 9} {R(26 - h[i] / 2)} L{4 + i * 9} {R(26 + h[i] / 2)}" for i in range(8))
mr = random.Random(5)
I(f'gsap.set("#mzp",{{attr:{{d:"{mini([10 + 30 * mr.random() for _ in range(8)])}"}},stroke:"{ORG}"}});')
tw("#fA", T["nc"], 0.42, {"opacity": 1, "y": 0}, "power3.out")
t = T["nc"]
while t + 0.1 <= T["flat"] + 1e-6:
    tw("#mzp", t, 0.1, {"attr": {"d": mini([10 + 30 * mr.random() for _ in range(8)])}}, "sine.inOut"); t += 0.1
tw("#mzp", T["flat"], 0.42, {"attr": {"d": mini([3] * 8)}, "stroke": LAV}, "power3.inOut")
tw("#fB", T["two"], 0.42, {"opacity": 1, "y": 0}, "power3.out")
tw("#mic1", T["two"] + 0.18, 0.30, {"scale": 1, "opacity": 1}, "back.out(2)"); tw("#mic2", T["two"] + 0.32, 0.30, {"scale": 1, "opacity": 1}, "back.out(2)")
I('gsap.set("#mic1,#mic2",{scale:0,opacity:0,transformOrigin:"50% 50%"});')
tw("#fA", T["feat_end"], 0.30, {"opacity": 0, "y": -16}, "power2.in"); tw("#fB", T["feat_end"] + 0.06, 0.30, {"opacity": 0, "y": -16}, "power2.in")

PAY_DX = 60                                  # payoff sits a little right: he holds the case at the left
# --- payoff: call pill + noise; "noise cancel aayi" flattens the noise into a clean line
st("#call", T["call2"] - 0.01, {"scale": 0.6, "opacity": 0}); st("#callw", T["call2"] - 0.01, {"y": GY - GC, "x": PAY_DX})
tw("#call", T["call2"], 0.40, {"opacity": 1, "scale": 1}, "back.out(1.4)")
st("#nz", T["call2"] - 0.01, {"scaleX": 1, "opacity": 1, "y": GY - GH, "x": PAY_DX, "clipPath": "inset(0px 0px 0px 170px)"}); st("#nzp", T["call2"] - 0.01, {"stroke": ORG, "attr": {"d": bars_d(FLAT)}})
t = T["call2"] + 0.1
mid2 = lambda i: 5 <= i < 9 or i > 20        # left-most strokes off: the case is held there, at the left
while t + 0.12 <= T["cancel"] + 1e-6:
    tw("#nzp", t, 0.12, {"attr": {"d": bars_d(noisy(0.8, mid2))}}, "sine.inOut"); t += 0.12
tw("#nzp", T["cancel"], 0.50, {"attr": {"d": bars_d(FLAT)}, "stroke": LAV}, "power3.inOut")
I('gsap.set("#line",{opacity:0,scaleX:0.0}); gsap.set("#nA,#nB",{opacity:0,scale:0.5}); gsap.set("#pulse",{opacity:0,x:0});')
st("#line", T["cancel"] + 0.30, {"opacity": 1, "scaleX": 0.86})
st("#nz", T["cancel"] + 0.52, {"opacity": 0})
# "neenga pesurappa": the pill splits into the two ends; the line stretches into the link
tw("#call", T["neenga"], 0.36, {"scale": 0.2, "opacity": 0}, "power3.in")
tw("#line", T["neenga"], 0.50, {"scaleX": 1}, "power3.inOut")
tw("#nA", T["neenga"] + 0.18, 0.40, {"opacity": 1, "scale": 1}, "back.out(1.6)")
tw("#nB", T["neenga"] + 0.30, 0.40, {"opacity": 1, "scale": 1}, "back.out(1.6)")
PX0, PX1 = 0, 220
st("#pulse", T["thel"], {"opacity": 1, "x": PX0}); tw("#pulse", T["thel"], 0.75, {"x": PX1}, "power2.inOut"); tw("#pulse", T["thel"] + 0.75, 0.15, {"opacity": 0}, "none")
st("#pulse", T["avanga"], {"opacity": 1, "x": PX1}); tw("#pulse", T["avanga"], 0.75, {"x": PX0}, "power2.inOut"); tw("#pulse", T["avanga"] + 0.75, 0.15, {"opacity": 0}, "none")
I('gsap.set("#clear",{opacity:0,scale:0.6,y:10});')
tw("#clear", T["clear"], 0.38, {"opacity": 1, "scale": 1, "y": 0}, "back.out(1.8)")
tw("#line", T["clear"], 0.38, {"backgroundColor": WHITE}, "power2.out")
# --- CTA: the link strip folds into the link pill
for sel in ("#nA", "#nB", "#clear"):
    tw(sel, T["link_out"], 0.32, {"opacity": 0, "scale": 0.6}, "power3.in")
tw("#line", T["link_out"], 0.40, {"scaleX": 0.05, "opacity": 0}, "power3.in")
I('gsap.set("#cta",{opacity:0,scale:0.6}); gsap.set("#arrow",{y:-6});')
tw("#cta", T["keezha"], 0.40, {"opacity": 1, "scale": 1}, "back.out(1.5)")
for j in range(4):
    tw("#arrow", T["keezha"] + 0.35 + j * 0.6, 0.30, {"y": 8}, "sine.inOut"); tw("#arrow", T["keezha"] + 0.65 + j * 0.6, 0.30, {"y": -6}, "sine.inOut")
tw("#cta", T["click"], 0.08, {"scale": 0.92}, "power2.in"); tw("#cta", T["click"] + 0.08, 0.30, {"scale": 1}, "back.out(2.2)")

# ---------------- HTML ----------------
ICON_OFFICE = '<svg viewBox="0 0 40 40" class="ic"><path d="M8 35V7h16v28M24 15h9v20M4 35h32M13 13h5M13 19h5M13 25h5M28 21h1M28 27h1" /></svg>'
ICON_CAR = '<svg viewBox="0 0 40 40" class="ic"><path d="M5 26v-6l4-8h22l4 8v6zM5 26v4h5v-4M30 26v4h5v-4M9 20h22" /><circle cx="11" cy="22.5" r="1.6"/><circle cx="29" cy="22.5" r="1.6"/></svg>'
ICON_CALL = '<svg viewBox="0 0 40 40" class="ic"><path d="M13 6l-5 2c-2 6 2 16 8 21s14 7 18 4l1-5-7-4-3 3c-4-1-8-6-9-10l3-3z" /></svg>'
ICON_MIC = lambda i: f'<svg id="mic{i}" viewBox="0 0 24 40" class="mic"><rect x="6" y="3" width="12" height="20" rx="6"/><path d="M2 18c0 6 4 10 10 10s10-4 10-10M12 28v8M7 37h10"/></svg>'
ARROW = '<svg id="arrow" viewBox="0 0 40 40" class="ic"><path d="M20 6v26M9 22l11 11 11-11" /></svg>'

body = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "MontBlack"; src: url("assets/fonts/Montserrat-Black.ttf") format("truetype"); font-weight: 900; }}
      @font-face {{ font-family: "MontXB"; src: url("assets/fonts/Montserrat-ExtraBold.ttf") format("truetype"); font-weight: 800; }}
      @font-face {{ font-family: "MontB"; src: url("assets/fonts/Montserrat-Bold.ttf") format("truetype"); font-weight: 700; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #140c1d; }}
      .clip {{ position: absolute; inset: 0; }}
      .vid {{ width: 1080px; height: 1920px; object-fit: cover; }}
      /* glass: deep violet from the case, one quiet rim */
      .glass {{ background: rgba(28,14,44,0.66); -webkit-backdrop-filter: blur(16px) saturate(1.25); backdrop-filter: blur(16px) saturate(1.25);
        border: 1.5px solid rgba(232,214,255,0.42); box-shadow: 0 14px 34px rgba(10,4,18,0.38); color: {WHITE}; }}
      #gfx {{ z-index: 10; pointer-events: none; }}
      .abs {{ position: absolute; left: 0; top: 0; }}
      #nz {{ position: absolute; left: {540 - BW // 2}px; top: {GH - 80}px; width: {BW + 20}px; height: 160px; transform-origin: 50% 50%; }}
      #nz path {{ fill: none; stroke-width: 10; stroke-linecap: round; }}
      #nword {{ position: absolute; left: 0; width: 1080px; top: {GH - 92}px; text-align: center; font-family: "MontBlack"; font-size: 168px;
        line-height: 184px; letter-spacing: 6px; color: {WHITE}; text-shadow: 0 8px 30px rgba(20,8,32,0.55), 0 0 2px rgba(20,8,32,0.6); }}
      .chip {{ position: absolute; height: 92px; border-radius: 46px; display: flex; align-items: center; gap: 16px; padding: 0 34px 0 26px;
        font-family: "MontXB"; font-size: 44px; letter-spacing: 1px; white-space: nowrap; }}
      .ic {{ width: 48px; height: 48px; fill: none; stroke: {LAV}; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }}
      .ic circle {{ fill: {LAV}; stroke: none; }}
      #office {{ left: 190px; top: {GC - 46}px; }} #car {{ left: 610px; top: {GC - 46}px; }}
      #call {{ left: 0; top: 0; }}
      #dot {{ position: absolute; left: {540 - 16}px; top: {GH - 16}px; width: 32px; height: 32px; border-radius: 50%; background: {LAV};
        box-shadow: 0 0 0 6px rgba(201,168,255,0.25); }}
      #ring {{ position: absolute; left: 0; top: 0; border-radius: 50%; border: 6px solid {LAV};
        box-shadow: 0 0 0 2px rgba(20,8,32,0.35), 0 0 26px rgba(201,168,255,0.45), inset 0 0 0 2px rgba(20,8,32,0.25); }}
      #rlab {{ position: absolute; left: 0; top: 0; height: 70px; line-height: 70px; padding: 0 26px; border-radius: 37px;
        font-family: "MontBlack"; font-size: 40px; letter-spacing: 3px; }}
      .feat {{ position: absolute; left: 540px; height: 70px; border-radius: 35px; display: flex; align-items: center; gap: 16px; padding: 0 30px 0 22px;
        font-family: "MontBlack"; font-size: 36px; letter-spacing: 2px; white-space: nowrap; }}
      #fA {{ top: 985px; }} #fB {{ top: 1067px; }}
      #fA svg {{ width: 70px; height: 48px; }} #fA path {{ fill: none; stroke-width: 5; stroke-linecap: round; }}
      .mic {{ width: 26px; height: 44px; fill: none; stroke: {LAV}; stroke-width: 3; stroke-linecap: round; }} .mic rect {{ fill: rgba(201,168,255,0.35); }}
      #link {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
      #line {{ position: absolute; left: 480px; width: 220px; top: {GY - 4}px; height: 8px; border-radius: 4px; background: {LAV};
        box-shadow: 0 0 18px rgba(201,168,255,0.6); transform-origin: 50% 50%; }}
      .node {{ position: absolute; top: {GY - 46}px; height: 92px; border-radius: 46px; padding: 0 30px; line-height: 92px; font-family: "MontBlack";
        font-size: 32px; letter-spacing: 2px; }}
      #nA {{ right: 600px; }} #nB {{ left: 700px; }}   /* node edges meet the line ends (480 / 700): clear of the case */
      #pulse {{ position: absolute; left: {480 - 14}px; top: {GY - 14}px; width: 28px; height: 28px; border-radius: 50%; background: #fff;
        box-shadow: 0 0 0 8px rgba(255,255,255,0.22), 0 0 26px rgba(255,255,255,0.8); }}
      #clear {{ position: absolute; left: 590px; top: {GY + 62}px; height: 76px; line-height: 76px; padding: 0 34px; border-radius: 38px;
        background: {LAV}; color: {INK}; font-family: "MontBlack"; font-size: 44px; letter-spacing: 6px;
        box-shadow: 0 12px 30px rgba(10,4,18,0.35); }}
      #cta {{ position: absolute; left: 540px; top: {GY - 50}px; height: 100px; border-radius: 50px; display: flex; align-items: center; gap: 14px;
        padding: 0 40px 0 30px; font-family: "MontBlack"; font-size: 48px; letter-spacing: 2px; }}
      #cta .ic {{ stroke: {INK}; width: 52px; height: 52px; }} #cta .disc {{ width: 66px; height: 66px; border-radius: 50%; background: {LAV};
        display: flex; align-items: center; justify-content: center; }}
      /* captions: centred, above the eyes (top 290, inside the 269 px safe line), 1-2 lines, one keyword in the case's lavender */
      #caps {{ z-index: 20; pointer-events: none; }}
      .cap {{ position: absolute; left: 180px; width: 720px; top: 290px; text-align: center; }}
      .cap .t {{ display: inline; font-family: "MontXB"; font-size: 54px; line-height: 1.32; color: #fff; padding: 6px 20px; border-radius: 16px;
        background: rgba(24,12,38,0.80); -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
      .cap em {{ font-style: normal; font-family: "MontBlack"; color: {LAV}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{TOTAL}">
      <video id="plate" class="clip vid" src="assets/v/plate{SUF}.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="1" style="z-index:1"></video>
      <audio id="mix" src="assets/mix{SUF}.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
      <div id="gfx" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="3">
        <div id="nz"><svg viewBox="0 0 {BW + 20} 160" width="{BW + 20}" height="160"><path id="nzp" d="{bars_d(FLAT)}" /></svg></div>
        <div id="nword">NOISE</div>
        <div id="office" class="chip glass">{ICON_OFFICE}office</div>
        <div id="car" class="chip glass">{ICON_CAR}car</div>
        <div id="callw" class="abs" style="left:540px;top:{GC}px"><div id="call" class="chip glass">{ICON_CALL}call</div></div>
        <div id="dot"></div>
        <div id="ring"></div>
        <div id="rlab" class="glass">EARBUDS</div>
        <div id="fA" class="feat glass"><svg viewBox="0 0 76 52"><path id="mzp" d="" /></svg>NOISE CANCELLING</div>
        <div id="fB" class="feat glass">{ICON_MIC(1)}{ICON_MIC(2)}TWO MICROPHONES</div>
        <div id="link"><div id="line"></div><div id="pulse"></div>
          <div id="nA" class="node glass">NEENGA</div><div id="nB" class="node glass">AVANGA</div><div id="clear">CLEAR</div></div>
        <div id="cta" class="glass"><div class="disc">{ARROW}</div>link</div>
      </div>
      <div id="caps" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="4">
{chr(10).join(caps_html)}
      </div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      {chr(10).join("      " + l for l in init).strip()}
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join("      " + l for l in js)}
      tl.set({{}}, {{}}, {TOTAL});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("edit/index.html", "w").write(body)

# ---------------- timing map ----------------
tm = {"version": VERSION, "total": TOTAL, "fps": 30, "source": "src/source.mp4 (Drive 3b5b7d85628e467eaa9b80b3eb762869.mp4, both copies identical)",
      "edl": [{"out_start": a, "out_end": b, "src_in": c, "src_out": d} for a, b, c, d in plan.SEG_OUT],
      "head": "src 0.40-0.50 shown as a hold of src 0.50 (first sharp frame); end hold: last frame frozen %.3f s" % plan.END_HOLD,
      "framing": [{"out": R(a), "scale": b, "focus": [c, d]} for a, b, c, d in plan.FRAMING],
      "captions": [{"out_start": o0, "out_end": o1, "src_start": CAPS[i][0], "text": CAPS[i][2], "keyword": CAPS[i][3]} for i, o0, o1 in caps_js],
      "graphics": {k: R(v) for k, v in T.items()},
      "ring_track_window_out": [ring[0][0], ring[-1][0]],
      "sfx": json.load(open("edit/cues.json"))["cues"],
      "music": "Digital Clouds - Alejandro Magana (A. M.), Mixkit #175, Mixkit Stock Music Free License; from 0.0 s, bed under speech"}
json.dump(tm, open(f"edit/timing_map{SUF}.json", "w"), indent=1, ensure_ascii=False)
print("built", VERSION, TOTAL, len(js), "timeline entries;", len(ring), "ring keys")
