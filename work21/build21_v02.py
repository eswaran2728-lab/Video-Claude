# HyperFrames project for work21 v02 -> edit_v02/index.html (+ edit_v02/cues.json).
# Fast beat-cut edit of every photo and the clips, with a persistent Mahaguru Sri S Arumugam Students header.
import json, math, random
import os, importlib
P = importlib.import_module("plan21_" + os.environ.get("VERSION", "v02"))
b, T, B = P.b, P.TOTAL, P.B
Y, R, BL, INK, GOLD = "#ffc72c", "#e4002b", "#2f5bea", "#0b0b10", "#f2c14e"
els, init, js, cues = [], [], [], []
fmt = lambda d: ",".join(f"{k}:{json.dumps(v)}" for k, v in d.items())
def J(sel, t, d, props, ease="power3.out"): js.append(f'tl.to("{sel}",{{{fmt(props)},duration:{round(d, 3)},ease:"{ease}"}},{round(t, 3)});')
def FROM(sel, t, d, frm, to, ease="power3.out"): js.append(f'tl.fromTo("{sel}",{{{fmt(frm)}}},{{{fmt(to)},duration:{round(d, 3)},ease:"{ease}",immediateRender:false}},{round(t, 3)});')
def SET(sel, t, props): js.append(f'tl.set("{sel}",{{{fmt(props)}}},{round(t, 3)});')
def INIT(sel, props): init.append(f'gsap.set("{sel}",{{{fmt(props)}}});')
def CUE(t, f, g): cues.append((round(t, 3), f, g))
def show(sel, t0, t1, fi=0.0, fo=0.0):
    INIT(sel, {"opacity": 0})
    (J(sel, t0, fi, {"opacity": 1}, "power1.out") if fi else SET(sel, t0, {"opacity": 1}))
    if t1 < T: (J(sel, t1 - fo, fo, {"opacity": 0}, "power1.in") if fo else SET(sel, t1, {"opacity": 0}))
def flash(t, a=0.55): SET("#flash", t, {"opacity": a}); J("#flash", t + 0.02, 0.22, {"opacity": 0}, "power2.out")

# ---------------- photos ----------------
origins = ["50% 45%", "35% 50%", "65% 50%", "50% 60%"]
for j, p in enumerate(P.PHOTOS):
    q = lambda t: round(t * 30) / 30 - 0.004            # snap cuts to the frame the plate cuts on
    t0, t1, pid, e = q(b(p["k0"])), q(b(p["k1"])), p["id"], f"ph{j}"
    slow = 129 <= p["k0"] < 159
    z = 1.12 if slow else (1.05 if t1 - t0 < 0.6 else 1.08)
    if p["mode"] in ("cover", "full"):
        els.append(f'<img id="{e}" class="full" src="assets/p/{pid}.jpg" alt="" style="transform-origin:{origins[j % 4]}">')
        show(f"#{e}", t0, t1 + (0.25 if slow else 0), 0.25 if slow else 0, 0.25 if slow else 0)
        if not p.get("freeze"): FROM(f"#{e}", t0, t1 - t0 + (0.25 if slow else 0), {"scale": 1.0}, {"scale": z}, "sine.inOut")
    else:
        land = P.SIZE[pid][0] > P.SIZE[pid][1]
        css = ("top:820px;height:810px" if p.get("low") else "top:555px;height:810px") if land else "top:240px;height:1440px"
        els.append(f'<div id="{e}" class="full"><img class="full" src="assets/p/{pid}_bg.jpg" alt=""><img id="{e}c" class="card" style="{css}" src="assets/p/{pid}.jpg" alt=""></div>')
        show(f"#{e}", t0, t1); FROM(f"#{e}c", t0, t1 - t0, {"scale": 1.0}, {"scale": 1.05}, "sine.inOut")
    if p.get("freeze"):                                   # the music stops: flash + punch-in, then hold
        FROM(f"#{e}", t0, 0.35, {"scale": 1.0}, {"scale": 1.14}, "expo.out")
    elif 64 <= p["k0"] < 129 or 161 <= p["k0"] < 201:
        if j % 4 == 0: CUE(t0, "curated/camera-shutter-light.wav", -21)

# plate push-ins where the action needs emphasis: the shout, the slow-motion spin, the final bow
for k0, k1, z in ((4, 8, 1.08), (P.SLOWMO[0], P.SLOWMO[1], 1.10), (61, 64, 1.06)):
    SET("#plate", b(k0), {"scale": 1.0}); J("#plate", b(k0), b(k1) - b(k0), {"scale": z}, "sine.inOut"); SET("#plate", b(k1), {"scale": 1.0})

# ---------------- HOOK ----------------
els.append(f'''<div id="hk" class="layer">
  <div id="hkS1" class="stripe" data-layout-allow-overflow style="top:1235px;background:{R}"></div><div id="hkS2" class="stripe" data-layout-allow-overflow style="top:1355px;background:{BL}"></div>
  <div id="hkW" class="word">SILAMBAM</div><div id="hkSub" class="sub">HARI SUKAN NEGARA · SEPANG 2026</div></div>''')
show("#hk", b(4) - 0.05, b(8) - 0.1, 0, 0.2)
FROM("#hkS1", b(4) - 0.05, 0.3, {"scaleX": 0, "transformOrigin": "0% 50%"}, {"scaleX": 1}); FROM("#hkS2", b(4), 0.3, {"scaleX": 0, "transformOrigin": "100% 50%"}, {"scaleX": 1})
FROM("#hkW", b(4), 0.3, {"scale": 1.9, "opacity": 0}, {"scale": 1, "opacity": 1}, "expo.out")
for i, dx in enumerate((10, -8, 5, -3, 0)): J("#hkW", b(4) + 0.3 + i * 0.04, 0.04, {"x": dx}, "none")
FROM("#hkSub", b(5), 0.3, {"y": 24, "opacity": 0}, {"y": 0, "opacity": 1})
CUE(b(4), "curated/hook-impact.wav", -8); CUE(b(4) - 0.05, "curated/zoom-swish.wav", -16); CUE(b(2), "curated/zoom-swish.wav", -19)

# ---------------- EVENT CARD (beats 8-16) ----------------
ICON_CAL = f'<svg width="38" height="38" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2" fill="none" stroke="{Y}" stroke-width="2.2"/><path d="M3 10h18M8 3v4M16 3v4" stroke="{Y}" stroke-width="2.2"/></svg>'
ICON_PIN = f'<svg width="38" height="38" viewBox="0 0 24 24"><path d="M12 22s7-7.2 7-12.5A7 7 0 005 9.5C5 14.8 12 22 12 22z" fill="none" stroke="{Y}" stroke-width="2.2"/><circle cx="12" cy="9.5" r="2.6" fill="{Y}"/></svg>'
els.append(f'''<div id="ev" class="layer">
  <div id="evBars"><div class="bar" style="background:{R}"></div><div class="bar" style="background:{Y}"></div><div class="bar" style="background:{BL}"></div></div>
  <div id="evPanel" class="panel"><div id="evSmall" class="evs">{P.EVENT_SMALL}</div>
    <div class="evbig"><span id="evW0" style="color:{Y}">HARI</span> <span id="evW1" style="color:#ff5468">SUKAN</span> <span id="evW2" style="color:#7fa6ff">NEGARA</span></div>
    <div id="evSub" class="evsub">{P.EVENT_SUB}</div>
    <div id="evD" class="pill">{ICON_CAL}<span>{P.EVENT_DATE}</span></div><div id="evV" class="pill">{ICON_PIN}<span>{P.EVENT_VENUE}</span></div></div></div>''')
show("#ev", b(8), b(16) - 0.1, 0, 0.2)
FROM("#evBars", b(8), 0.4, {"x": -1100}, {"x": 0}, "expo.out"); CUE(b(8), "curated/zoom-swish.wav", -14)
FROM("#evPanel", b(8) + 0.1, 0.4, {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1})
for i in range(3): FROM(f"#evW{i}", b(9) + i * B, 0.3, {"scale": 1.6, "opacity": 0}, {"scale": 1, "opacity": 1}, "back.out(1.7)"); CUE(b(9) + i * B, "curated/ui-pop.wav", -15)
FROM("#evSub", b(11.5), 0.3, {"opacity": 0, "y": 16}, {"opacity": 1, "y": 0})
FROM("#evD", b(12), 0.3, {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0}); FROM("#evV", b(12.5), 0.3, {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0})
CUE(b(12), "tick.wav", -14); CUE(b(12.5), "tick.wav", -14)

# ---------------- BRAND REVEAL (beat 16) -> persistent header (beat 20 to the end card) ----------------
els.append(f'''<div id="hdBand" class="hdband"></div>
<div id="hd" class="hd"><img id="hdLogo" src="assets/logo/mahaguru.png" alt=""><div class="hd1">{P.BRAND1}</div><div class="hd2">{P.BRAND2}</div></div>
<div id="rv" class="layer"><div id="rv1" class="rv1">{P.BRAND1}</div><div id="rv2" class="rv2">{P.BRAND2}</div></div>''')
show("#hdBand", b(16), b(P.K_END), 0.3, 0.3)
INIT("#hd", {"opacity": 0}); SET("#hd", b(16), {"opacity": 1}); J("#hd", b(P.K_END) - 0.3, 0.3, {"opacity": 0})
INIT("#hd .hd1", {"opacity": 0}); INIT("#hd .hd2", {"opacity": 0}); INIT("#hd", {"backgroundColor": "rgba(11,11,16,0)"}); J("#hd", b(20) + 0.3, 0.4, {"backgroundColor": "rgba(11,11,16,0.66)"}, "power1.out")
FROM("#hdLogo", b(16), 0.45, {"y": 190, "scale": 0.2, "opacity": 0}, {"y": 190, "scale": 2.3, "opacity": 1}, "back.out(1.5)")
J("#hdLogo", b(20), 0.6, {"y": 0, "scale": 1}, "power3.inOut")
FROM("#hd .hd1", b(20) + 0.45, 0.35, {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0}); FROM("#hd .hd2", b(20) + 0.6, 0.35, {"opacity": 0, "y": 12}, {"opacity": 1, "y": 0})
show("#rv", b(16.5), b(20.4), 0, 0.3)
FROM("#rv1", b(16.5), 0.4, {"x": -140, "opacity": 0}, {"x": 0, "opacity": 1}, "expo.out"); FROM("#rv2", b(17.5), 0.4, {"scale": 1.8, "opacity": 0}, {"scale": 1, "opacity": 1}, "expo.out")
CUE(b(16), "sub-impact.wav", -10); CUE(b(16) + 0.05, "shimmer.wav", -15); CUE(b(17.5), "curated/hook-impact.wav", -12); CUE(b(20), "curated/zoom-swish.wav", -15)

# ---------------- section titles ----------------
def title(id_, l1, l2, k0, k1, col=Y):
    els.append(f'<div id="{id_}" class="layer"><div id="{id_}b" class="tbar"></div><div id="{id_}1" class="tt">{l1}</div>' + (f'<div id="{id_}2" class="tt" style="top:560px;color:#fff">{l2}</div>' if l2 else "") + '</div>')
    show(f"#{id_}", b(k0), b(k1), 0, 0.25)
    FROM(f"#{id_}b", b(k0), 0.3, {"scaleX": 0, "transformOrigin": "0% 50%"}, {"scaleX": 1}, "expo.out")
    FROM(f"#{id_}1", b(k0) + 0.06, 0.35, {"x": -120, "opacity": 0}, {"x": 0, "opacity": 1}, "expo.out")
    if l2: FROM(f"#{id_}2", b(k0 + 1), 0.35, {"x": 120, "opacity": 0}, {"x": 0, "opacity": 1}, "expo.out"); CUE(b(k0 + 1), "thock.wav", -14)
    CUE(b(k0), "curated/zoom-swish.wav", -12)
def tag(id_, text, k0, k1):
    els.append(f'<div id="{id_}" class="tag"><i style="background:{Y}"></i>{text}</div>')
    show(f"#{id_}", b(k0), b(k1), 0, 0.2); FROM(f"#{id_}", b(k0), 0.35, {"x": -60, "opacity": 0}, {"x": 0, "opacity": 1})
tag("tgPerf", "IN ACTION", 24.1, 28); tag("tgSlow", "SLOW MOTION", P.SLOWMO[0] + 0.1, P.SLOWMO[1] - 0.1)
title("tMB", "MEDALS", "&amp; BELTS", 64, 68)
title("tPM", "PROUD", "MOMENTS", 129, 133)
title("tOS", "ON THE", "STAGE", 161, 164)
els.append('<div id="flash" class="full" style="background:#fff"></div>'); INIT("#flash", {"opacity": 0})
for k in (16, 24, 64, 129, 161, 203): flash(b(k), 0.45)
flash(b(159), 0.85); CUE(b(159), "sub-impact.wav", -9); CUE(b(24), "sub-impact.wav", -12); CUE(b(P.SLOWMO[0]), "curated/zoom-swish.wav", -15)

# ---------------- PAYOFF: TAHNIAH! over the medal-group clip (beat 203) ----------------
random.seed(21); parts = []
for i in range(40):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(220, 560); s = random.uniform(8, 18)
    parts.append(f'<i id="pt{i}" class="pt" style="width:{s:.0f}px;height:{s:.0f}px"></i>'); INIT(f"#pt{i}", {"x": 0, "y": 0, "opacity": 0, "scale": 0.4})
    t = b(203) + random.uniform(0, 0.25); SET(f"#pt{i}", t, {"opacity": 1})
    J(f"#pt{i}", t, random.uniform(1.0, 1.6), {"x": round(r * math.cos(a)), "y": round(r * math.sin(a) * 0.55 + random.uniform(40, 160)), "scale": 1, "opacity": 0}, "power2.out")
els.append(f'''<div id="th" class="layer"><div class="thbg"></div><div class="parts">{"".join(parts)}</div>
  <div id="thW" class="thw">TAHNIAH!</div><div id="thC" class="thc">CONGRATULATIONS</div><div id="thL" class="thl">to all the young Silambam athletes</div></div>''')
show("#th", b(203) - 0.05, b(211), 0, 0.25)
FROM("#thW", b(203), 0.45, {"scale": 2.0, "opacity": 0}, {"scale": 1, "opacity": 1}, "expo.out")
FROM("#thC", b(204), 0.35, {"y": 24, "opacity": 0}, {"y": 0, "opacity": 1}); FROM("#thL", b(205), 0.35, {"y": 20, "opacity": 0}, {"y": 0, "opacity": 1})
CUE(b(203), "sub-impact.wav", -11); CUE(b(203) + 0.05, "sparkle.wav", -12); CUE(b(204), "shimmer.wav", -17)

# ---------------- PHOTO WALL: all 107 photos assemble (beats 211-225) ----------------
ids = sorted(P.SIZE); random.seed(7); COLS = 9 if len(ids) <= 108 else 10; CW = 1080 // COLS; order = list(range(len(ids))); random.shuffle(order)
cells = []
for n, pid in enumerate(ids):
    x, y = (n % COLS) * CW, (n // COLS) * 160
    cells.append(f'<img id="wc{n}" class="wc" src="assets/t/{pid}.jpg" alt="" style="left:{x}px;top:{y}px;width:{CW}px;object-fit:cover">'); INIT(f"#wc{n}", {"opacity": 0, "scale": 0.3})
    t = b(P.WALL[0]) + order[n] / len(ids) * 2.6; FROM(f"#wc{n}", t, 0.3, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, "back.out(1.6)")
els.append(f'''<div id="wall" class="layer" style="background:{INK}"><div id="wallIn" class="layer">{"".join(cells)}</div>
  <div id="wallDim" class="full" style="background:rgba(11,11,16,.62)"></div>
  <div id="wallT" class="wallt"><div class="w1">PROUD OF</div><div class="w2">EVERY STUDENT</div></div></div>''')
show("#wall", round(b(P.WALL[0]) * 30) / 30 - 0.004, b(P.WALL[1]) + 0.35, 0, 0.3)
for i in range(6): CUE(b(P.WALL[0]) + i * 0.45, "tick.wav", -18)
FROM("#wallIn", b(P.WALL[0]), b(P.WALL[1]) - b(P.WALL[0]), {"scale": 1.12}, {"scale": 1.0}, "sine.inOut")
INIT("#wallDim", {"opacity": 0}); J("#wallDim", b(P.WALL[0] + 6), 0.5, {"opacity": 1}, "power1.out")
FROM("#wallT", b(P.WALL[0] + 6.3), 0.45, {"scale": 1.5, "opacity": 0}, {"scale": 1, "opacity": 1}, "expo.out"); CUE(b(P.WALL[0] + 6.3), "curated/hook-impact.wav", -12)

# ---------------- END CARD ----------------
els.append(f'''<div id="end" class="layer"><img id="enBg" class="full" src="assets/p/077_bg.jpg" alt="">
  <img id="enLogo" class="enlogo" src="assets/logo/mahaguru.png" alt="">
  <div id="enB1" class="enb1">{P.BRAND1}</div><div id="enB2" class="enb2">{P.BRAND2}</div>
  <div id="enE" class="ene">HARI SUKAN NEGARA<br>{P.EVENT_SUB}</div><div id="enD" class="end">15.11.2026 · {P.EVENT_VENUE}</div></div>''')
show("#end", b(P.K_END), T, 0.3); FROM("#enBg", b(P.K_END), T - b(P.K_END), {"scale": 1.0}, {"scale": 1.1}, "sine.inOut")
FROM("#enLogo", b(P.K_END) + 0.1, 0.5, {"scale": 0.4, "opacity": 0}, {"scale": 1, "opacity": 1}, "back.out(1.6)")
for i, s in enumerate(("#enB1", "#enB2", "#enE", "#enD")): FROM(s, b(P.K_END + 1.5) + i * 0.3, 0.4, {"y": 20, "opacity": 0}, {"y": 0, "opacity": 1})
CUE(b(P.K_END) + 0.1, "thock.wav", -12); CUE(b(P.K_END) + 0.15, "shimmer.wav", -16)
els.append('<div id="fade" class="full" style="background:#000"></div>'); INIT("#fade", {"opacity": 0}); J("#fade", T - 1.2, 1.1, {"opacity": 1}, "power1.in")

CSS = open("build21_v02.css").read().replace("{Y}", Y).replace("{INK}", INK).replace("{GOLD}", GOLD)
doc = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{T}">
      <video id="plate" class="clip vid" src="assets/v/plate.mp4" muted playsinline data-start="0" data-duration="{T}" data-track-index="1" style="z-index:1"></video>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{T}" data-track-index="2" data-volume="1"></audio>
      <div id="gfx" class="clip" data-start="0" data-duration="{T}" data-track-index="3" style="z-index:2">
        {(chr(10) + "        ").join(els)}
      </div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      {(chr(10) + "      ").join(init)}
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(js)}
      tl.set({{}}, {{}}, {T});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(f"{P.OUT}/index.html", "w").write(doc)
json.dump({"cues": [{"t": a, "sfx": f, "gain_db": g} for a, f, g in sorted(cues)]}, open(f"{P.OUT}/cues.json", "w"), indent=1)
print("built", T, "s;", len(P.PHOTOS), "photos;", len(js), "tweens;", len(cues), "cues")
