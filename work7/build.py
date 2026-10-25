# Builds edit/index.html for the AVSEC keychain reel from edl.py (speech-led cut + b-roll).
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.join(HERE, "edit")
exec(open(os.path.join(HERE, "edl.py")).read())
VERSION = os.environ.get("VERSION", "v03")      # v01 light grade; v02 relit + cinematic grade + leaks; v03 = v02 with denoised dialogue + gentler face light
AD = {"v01": "v/", "v02": "vc/"}.get(VERSION, "vc3/")
DLG = "dialogue_v03.wav" if VERSION not in ("v01", "v02") else "dialogue.wav"
GP = os.path.join(HERE, "grade_attr.txt" if VERSION == "v01" else "grade_cine_attr.txt")  # v03 keeps the v02 grade
GRADE = open(GP).read().strip() if os.path.exists(GP) else ""
g = (lambda: f' data-color-grading="{GRADE}"') if GRADE else (lambda: "")
FPS = 30

def w(seg, src): return out_of(seg, src)          # output time of a spoken word
T50, TDES, TMULTI = w(0, 5.18), w(1, 9.40), w(1, 12.14)
T3, TRED, TBLK, TWHT = w(2, 16.72), w(2, 18.36), w(2, 18.70), w(2, 19.20)
TDSG, TPKG, TDLV = w(3, 6.80), w(3, 7.56), w(3, 11.88)
TBULK, TDM = w(4, 35.86), w(4, 39.48)
END_T = V[-1][4]

json.dump({"speech": [dict(zip(["out_start", "out_end", "clip", "src_in", "src_out"], s)) for s in OUT],
           "visual": [dict(zip(["id", "layout", "clip", "src_in", "out_start", "out_end", "note"], v)) for v in V]},
          open(os.path.join(E, "timing_map.json"), "w"), indent=1)

vis, js = [], []
for vid, layout, clip, a, o0, o1, note in V:
    d = round(o1 - o0, 3)
    vis.append(f"      <!-- {vid} ({layout}): {note} -->")
    if layout == "split":
        vis.append(f'      <video id="m{vid}" class="clip src" src="assets/{AD}{vid}_top.mp4" muted playsinline data-start="{o0}" data-duration="{d}" data-track-index="1" style="inset:auto;left:0;top:0;width:1080px;height:1000px"{g()}></video>')
        vis.append(f'      <video id="m{vid}f" class="clip src" src="assets/{AD}{vid}_faceC.mp4" muted playsinline data-start="{o0}" data-duration="{d}" data-track-index="2" style="inset:auto;left:0;top:960px;width:1080px;height:960px"{g()}></video>')
        vis.append(f'      <div id="seam{vid}" class="clip" data-start="{o0}" data-duration="{d}" data-track-index="3" style="inset:auto;left:0;top:900px;width:1080px;height:140px;background:linear-gradient(180deg, rgba(11,11,13,0) 0%, rgba(11,11,13,0.85) 50%, rgba(11,11,13,0) 100%)"></div>')
    else:
        vis.append(f'      <video id="m{vid}" class="clip vid src" src="assets/{AD}{vid}.mp4" muted playsinline data-start="{o0}" data-duration="{d}" data-track-index="1"{g()}></video>')

# camera moves, each tied to a beat
js += [
    'tl.fromTo("#mV1",{scale:1},{scale:1.07,duration:2.3,ease:"none"},0);',
    f'tl.set("#mV2",{{transformOrigin:"50% 28%"}},0);',
    f'tl.fromTo("#mV2",{{scale:1}},{{scale:1.08,duration:0.35,ease:"power2.out"}},{T50 - 0.05});',          # punch-in on "50"
    'tl.fromTo("#mV4",{y:-20},{y:0,duration:0.45,ease:"power3.out"},%s);' % V[3][4],
    'tl.fromTo("#mV6",{scale:1},{scale:1.08,duration:%s,ease:"none"},%s);' % (round(V[5][5] - V[5][4], 3), V[5][4]),
    'tl.set("#mV10",{transformOrigin:"50% 28%"},0);',
    f'tl.fromTo("#mV10",{{scale:1}},{{scale:1.07,duration:0.35,ease:"power2.out"}},{TDM - 0.05});',          # punch-in on "DM"
    'tl.fromTo("#mV12",{scale:1.12},{scale:1.0,duration:%s,ease:"power2.out"},%s);' % (round(TOTAL - END_T, 3), END_T),
]

# motion graphics
COUNT_T = round(T50 - 0.2, 3)
js += [
    'tl.fromTo("#hook .k1",{scale:1.08},{scale:1,duration:0.5,ease:"power3.out"},0);',
    'tl.fromTo("#hook .k2",{opacity:0,y:18},{opacity:1,y:0,duration:0.3,ease:"power3.out"},0.35);',
    'tl.to("#hook",{opacity:0,duration:0.15},2.15);',
    f'tl.fromTo("#count .card",{{y:18}},{{y:0,duration:0.42,ease:"power3.out"}},{COUNT_T});',
    f'tl.to("#count",{{opacity:0,duration:0.2}},{round(V[1][5] - 0.25, 3)});',
]
for k in range(11):  # 0 -> 50 counter, frame-stepped (seek-safe)
    js.append(f'tl.set("#countN",{{textContent:"{k * 5}"}},{round(COUNT_T + 0.1 + k / FPS, 4)});')
COLS_T = round(T3 - 0.05, 3)
js += [
    f'tl.fromTo("#colsH",{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2)"}},{COLS_T});',
    f'tl.fromTo("#c1",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.25,ease:"power3.out"}},{TRED - 0.05});',
    f'tl.fromTo("#c2",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.25,ease:"power3.out"}},{TBLK - 0.05});',
    f'tl.fromTo("#c3",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.25,ease:"power3.out"}},{TWHT - 0.05});',
    f'tl.to("#cols",{{opacity:0,duration:0.18}},{round(V[5][5] - 0.2, 3)});',
    f'tl.fromTo("#checks .card",{{y:18}},{{y:0,duration:0.42,ease:"power3.out"}},{V[6][4]});',
    f'tl.fromTo("#p1",{{strokeDashoffset:60}},{{strokeDashoffset:0,duration:0.25,ease:"power2.out"}},{TDSG});',
    f'tl.fromTo("#p2",{{strokeDashoffset:60}},{{strokeDashoffset:0,duration:0.25,ease:"power2.out"}},{TPKG});',
    f'tl.to("#checks",{{opacity:0,duration:0.18}},{round(V[6][5] - 0.2, 3)});',
    f'tl.fromTo("#stamp .s",{{scale:2.2,opacity:0,rotation:-16}},{{scale:1,opacity:1,rotation:-7,duration:0.28,ease:"back.out(2)"}},{TDLV});',
    f'tl.fromTo("#bulk .h",{{y:30,opacity:0}},{{y:0,opacity:1,duration:0.32,ease:"power3.out"}},{TBULK - 0.05});',
    f'tl.to("#bulk",{{opacity:0,duration:0.18}},{round(V[8][5] - 0.2, 3)});',
    f'tl.fromTo("#dm .card",{{y:18,scale:0.85}},{{y:0,scale:1,duration:0.35,ease:"back.out(1.8)"}},{TDM});',
    f'tl.fromTo("#endDim",{{opacity:0}},{{opacity:1,duration:0.35}},{END_T});',
    f'tl.fromTo("#end img",{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(1.6)"}},{END_T + 0.05});',
    f'tl.fromTo("#end .l1",{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"power3.out"}},{END_T + 0.15});',
    f'tl.fromTo("#end .l2",{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"power3.out"}},{END_T + 0.3});',
]

# captions: English translation of the Tamil speech, phrase by phrase on the spoken words
R = '<span class="sw r">red</span>'; K = '<span class="sw k">black</span>'; WH = '<span class="sw w">white</span>'
CAP = [
    (w(0, 0.24), w(0, 4.48), "In the company I work at,"),
    (w(0, 4.52), w(0, 7.66), "I needed <b>50 keychains</b> as a giveaway."),
    (w(1, 8.58), w(1, 11.56), "So I designed all of these:"),
    (w(1, 11.56), w(1, 14.75), "<b>multi-colour</b> keychains for them."),
    (w(2, 14.88), w(2, 17.90), "As you can see, every keychain here comes in <b>3 colours</b>:"),
    (w(2, 17.98), w(2, 19.90), f"{R}, {K} and {WH}."),
    (w(3, 6.22), w(3, 9.30), "I've done the <b>design</b> and <b>packaging</b>."),
    (w(3, 9.80), w(3, 12.84), "As soon as possible, I'll deliver them." if VERSION not in ("v01", "v02") else "As soon as possible, I'll deliver them to you."),  # v03: "to you"/"tomorrow" unverified
    (w(4, 35.12), w(4, 37.40), "If you want <b>bulk orders</b> like this,"),
    (w(4, 37.54), w(4, 41.30), "contact me or <b>DM</b> me."),
]
caps = []
for i, (a, b, txt) in enumerate(CAP):
    lay = next(v[1] for v in V if v[4] <= a < v[5])
    top = 840 if lay == "split" else 1090
    caps.append(f'      <div id="cap{i}" class="clip cap" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="8"><div class="box" style="top:{top}px"><span class="t">{txt}</span></div></div>')
    js.append(f'tl.fromTo("#cap{i} .box",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.12,ease:"power2.out"}},{a});')

# sound on the frame of each visible event (hit offset into the file subtracted)
SFX = [("hook-impact", 0.0, 0.5), ("camera-shutter-light", V[1][4] - 0.07, 0.4), ("ui-pop", COUNT_T, 0.35),
       ("camera-shutter", V[2][4] - 0.13, 0.35), ("camera-shutter-light", V[3][4] - 0.07, 0.35),
       ("ui-pop", COLS_T, 0.35), ("tick", TRED - 0.05, 0.5), ("tick", TBLK - 0.05, 0.5), ("tick", TWHT - 0.05, 0.5),
       ("camera-shutter", V[6][4] - 0.13, 0.35), ("ui-click", TDSG, 0.45), ("ui-click", TPKG, 0.45),
       ("thock", TDLV, 0.7), ("ui-pop", TBULK - 0.05, 0.35), ("ui-pop", TDM, 0.35),
       ("zoom-swish", V[10][4] + 0.25, 0.45), ("clean-ding", END_T + 0.05, 0.35)]
PEAK = {"zoom-swish": 0.139, "ui-pop": 0.02}
DUR = {"hook-impact": 1.9, "camera-shutter-light": 0.16, "camera-shutter": 0.3, "ui-pop": 0.2, "tick": 0.09, "ui-click": 0.12,
       "thock": 0.12, "zoom-swish": 0.76, "clean-ding": 0.55}
json.dump([{"sound": s, "t": round(t, 3), "gain": gn} for s, t, gn in SFX], open(os.path.join(E, "cues.json"), "w"), indent=1)
sfx = [f'      <audio id="sx{n}" class="clip" src="assets/sfx/{s}.wav" data-start="{max(0.0, round(t - PEAK.get(s, 0.0), 3))}" data-duration="{DUR[s]}" data-volume="{gn}"></audio>'
       for n, (s, t, gn) in enumerate(SFX)]

# warm light leaks on the two big transitions (v02)
leaks = []
if VERSION != "v01":
    for n, (t0, d) in enumerate(((V[1][4] - 0.25, 0.75), (V[10][4] - 0.1, 1.1))):
        leaks.append(f'      <div id="leak{n}" class="clip leak" data-start="{round(t0, 3)}" data-duration="{d}" data-track-index="4"><i class="a"></i><i class="g"></i></div>')
        js.append(f'tl.fromTo("#leak{n}",{{opacity:0,x:-140}},{{opacity:0.85,x:0,duration:{d / 2},ease:"sine.out"}},{round(t0, 3)});')
        js.append(f'tl.to("#leak{n}",{{opacity:0,x:120,duration:{d / 2},ease:"sine.in"}},{round(t0 + d / 2, 3)});')
rep = {"%%DLG%%": DLG, "%%LEAKS%%": "\n".join(leaks), "%%TOTAL%%": TOTAL, "%%SPEECH_END%%": SPEECH_END, "%%VISUALS%%": "\n".join(vis), "%%CAPTIONS%%": "\n".join(caps),
       "%%SFX%%": "\n".join(sfx), "%%JS%%": "\n".join("      " + l for l in js),
       "%%COUNT_T%%": COUNT_T, "%%COUNT_D%%": round(V[1][5] - COUNT_T, 3),
       "%%COLS_T%%": COLS_T, "%%COLS_D%%": round(V[5][5] - COLS_T, 3),
       "%%CHK_T%%": V[6][4], "%%CHK_D%%": round(V[6][5] - V[6][4], 3),
       "%%STAMP_T%%": round(TDLV, 3), "%%STAMP_D%%": round(V[7][5] - TDLV, 3),
       "%%BULK_T%%": round(TBULK - 0.05, 3), "%%BULK_D%%": round(V[8][5] - TBULK + 0.05, 3),
       "%%DM_T%%": TDM, "%%DM_D%%": round(V[9][5] - TDM, 3),
       "%%END_T%%": END_T, "%%END_D%%": round(TOTAL - END_T, 3)}
html = open(os.path.join(HERE, "index.tpl.html")).read()
for k, v in rep.items():
    html = html.replace(k, str(v))
open(os.path.join(E, "index.html"), "w").write(html)
print("wrote", len(js), "tweens;", len(CAP), "captions;", len(SFX), "sfx; total", TOTAL)
