# HyperFrames project for work21 v01 -> edit/index.html (+ edit/cues.json for the mix).
# Layers: graded video plate (track 1) < photos + motion graphics (one GSAP timeline, track 3) ; pre-mixed audio (track 2).
# Colours follow the event banner (yellow / red / blue on dark); type: Inter Display Black Italic (banner-like sporty italic).
import json, math, random
import plan21 as P
b, T, B = P.b, P.TOTAL, P.B
Y, R, BL, INK = "#ffc72c", "#e4002b", "#2f5bea", "#0b0b10"
els, init, js, cues = [], [], [], []
fmt = lambda d: ",".join(f"{k}:{json.dumps(v)}" for k, v in d.items())
def J(sel, t, d, props, ease="power3.out"): js.append(f'tl.to("{sel}",{{{fmt(props)},duration:{round(d, 3)},ease:"{ease}"}},{round(t, 3)});')
def FROM(sel, t, d, frm, to, ease="power3.out"): js.append(f'tl.fromTo("{sel}",{{{fmt(frm)}}},{{{fmt(to)},duration:{round(d, 3)},ease:"{ease}"}},{round(t, 3)});')
def SET(sel, t, props): js.append(f'tl.set("{sel}",{{{fmt(props)}}},{round(t, 3)});')
def INIT(sel, props): init.append(f'gsap.set("{sel}",{{{fmt(props)}}});')
def CUE(t, f, g): cues.append((round(t, 3), f, g))
def show(sel, t0, t1, fade_in=0.0, fade_out=0.0):
    INIT(sel, {"opacity": 0})
    (J(sel, t0, fade_in, {"opacity": 1}, "power1.out") if fade_in else SET(sel, t0, {"opacity": 1}))
    if t1 < T: (J(sel, t1 - fade_out, fade_out, {"opacity": 0}, "power1.in") if fade_out else SET(sel, t1, {"opacity": 0}))

# ---------------- photos (beat cuts, alternating push-ins) ----------------
origins = ["50% 45%", "35% 50%", "65% 50%", "50% 60%"]
for j, p in enumerate(P.PHOTOS):
    t0, t1, pid = b(p["k0"]), b(p["k1"]), p["id"]
    if p["mode"] == "cover":
        els.append(f'<img id="ph{pid}" class="full" src="assets/p/{pid}.jpg" alt="" style="transform-origin:{origins[j % 4]}">')
        show(f"#ph{pid}", t0, t1); FROM(f"#ph{pid}", t0, t1 - t0, {"scale": 1.0}, {"scale": 1.07 if p["k1"] - p["k0"] < 4 else 1.12}, "sine.inOut")
    else:
        els.append(f'<div id="ph{pid}" class="full"><img class="full" src="assets/p/{pid}_bg.jpg" alt=""><img id="phc{pid}" class="card" src="assets/p/{pid}.jpg" alt=""></div>')
        show(f"#ph{pid}", t0, t1); FROM(f"#phc{pid}", t0, t1 - t0, {"scale": 1.0}, {"scale": 1.045}, "sine.inOut")
    if p["k0"] >= 40 and j % 2 == 1: CUE(t0, "curated/camera-shutter-light.wav", -20)

# plate push-ins: only where the action needs emphasis (the shout, the slow-motion spin, the salute)
for k0, k1, z in ((4, 8, 1.08), (28, 32, 1.10), (36, 40, 1.06)):
    SET("#plate", b(k0), {"scale": 1.0}); J("#plate", b(k0), b(k1) - b(k0), {"scale": z}, "sine.inOut"); SET("#plate", b(k1), {"scale": 1.0})

# ---------------- HOOK: SILAMBAM slam (beat 4) ----------------
els.append(f'''<div id="hk" class="layer">
  <div id="hkS1" class="stripe" data-layout-allow-overflow style="top:1235px;background:{R}"></div><div id="hkS2" class="stripe" data-layout-allow-overflow style="top:1355px;background:{BL}"></div>
  <div id="hkW" class="word">SILAMBAM</div>
  <div id="hkSub" class="sub">HARI SUKAN NEGARA · SEPANG 2026</div></div>''')
show("#hk", b(4) - 0.05, b(8) - 0.1, 0, 0.25)
FROM("#hkS1", b(4) - 0.05, 0.3, {"scaleX": 0, "transformOrigin": "0% 50%"}, {"scaleX": 1}); FROM("#hkS2", b(4), 0.3, {"scaleX": 0, "transformOrigin": "100% 50%"}, {"scaleX": 1})
FROM("#hkW", b(4), 0.32, {"scale": 1.9, "opacity": 0}, {"scale": 1, "opacity": 1}, "expo.out")
for i, dx in enumerate((10, -8, 5, -3, 0)): J("#hkW", b(4) + 0.32 + i * 0.04, 0.04, {"x": dx}, "none")
FROM("#hkSub", b(5), 0.35, {"y": 24, "opacity": 0}, {"y": 0, "opacity": 1})
CUE(b(4), "curated/hook-impact.wav", -8); CUE(b(4) - 0.05, "curated/zoom-swish.wav", -16)

# ---------------- CONTEXT: event title card over the boy on stage (beats 8-16) ----------------
ICON_CAL = f'<svg width="38" height="38" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2" fill="none" stroke="{Y}" stroke-width="2.2"/><path d="M3 10h18M8 3v4M16 3v4" stroke="{Y}" stroke-width="2.2"/></svg>'
ICON_PIN = f'<svg width="38" height="38" viewBox="0 0 24 24"><path d="M12 22s7-7.2 7-12.5A7 7 0 005 9.5C5 14.8 12 22 12 22z" fill="none" stroke="{Y}" stroke-width="2.2"/><circle cx="12" cy="9.5" r="2.6" fill="{Y}"/></svg>'
els.append(f'''<div id="ev" class="layer">
  <div id="evBars"><div class="bar" style="background:{R}"></div><div class="bar" style="background:{Y}"></div><div class="bar" style="background:{BL}"></div></div>
  <div id="evPanel" class="panel">
    <div id="evSmall" class="evs">{P.EVENT_SMALL}</div>
    <div class="evbig"><span id="evW0" style="color:{Y}">HARI</span> <span id="evW1" style="color:#ff5468">SUKAN</span> <span id="evW2" style="color:#7fa6ff">NEGARA</span></div>
    <div id="evSub" class="evsub">{P.EVENT_SUB}</div>
    <div id="evD" class="pill">{ICON_CAL}<span>{P.EVENT_DATE}</span></div>
    <div id="evV" class="pill">{ICON_PIN}<span>{P.EVENT_VENUE}</span></div>
  </div></div>''')
show("#ev", b(8), b(16) - 0.15, 0, 0.3)
FROM("#evBars", b(8), 0.45, {"x": -1100}, {"x": 0}, "expo.out"); CUE(b(8), "curated/zoom-swish.wav", -14)
FROM("#evPanel", b(8) + 0.15, 0.45, {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1})
FROM("#evSmall", b(8) + 0.3, 0.35, {"opacity": 0, "y": 14}, {"opacity": 1, "y": 0})
for i in range(3):
    FROM(f"#evW{i}", b(9) + i * B, 0.32, {"scale": 1.6, "opacity": 0}, {"scale": 1, "opacity": 1}, "back.out(1.7)"); CUE(b(9) + i * B, "curated/ui-pop.wav", -15)
FROM("#evSub", b(11), 0.35, {"opacity": 0, "y": 16}, {"opacity": 1, "y": 0})
FROM("#evD", b(12), 0.35, {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0}); CUE(b(12), "tick.wav", -14)
FROM("#evV", b(12.5), 0.35, {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0}); CUE(b(12.5), "tick.wav", -14)
CUE(b(16) - 1.6, "curated/metallic-riser.wav", -13)          # builds into the drop

# ---------------- PERFORMANCES (beats 16-40): flash on the drop, section tag, slow-motion tag ----------------
els.append('<div id="flash" class="full" style="background:#fff"></div>'); INIT("#flash", {"opacity": 0})
for t in (b(16), b(40)):
    SET("#flash", t, {"opacity": 0.55}); J("#flash", t + 0.02, 0.22, {"opacity": 0}, "power2.out")
CUE(b(16), "sub-impact.wav", -10)
def tag(id_, text, t0, t1, color=Y):
    els.append(f'<div id="{id_}" class="tag"><i style="background:{color}"></i>{text}</div>')
    show(f"#{id_}", t0, t1, 0, 0.25); FROM(f"#{id_}", t0, 0.4, {"x": -60, "opacity": 0}, {"x": 0, "opacity": 1})
tag("tgPerf", "IN ACTION", b(16) + 0.1, b(20)); tag("tgSlow", "SLOW MOTION", b(28) + 0.1, b(32) - 0.1)
CUE(b(28), "curated/zoom-swish.wav", -15)

# small event tag, top, while the story runs (performances -> payoff)
for n_, (a_, z_) in enumerate(((b(16) + 0.3, b(40) - 0.1), (b(44), b(76) - 0.1))):
    els.append(f'<div id="evtag{n_}" class="evtag"><i></i>{P.TAG}</div>'); show(f"#evtag{n_}", a_, z_, 0.4, 0.3)

# ---------------- MEDALS & BELTS (beat 40) over the first presentation photo ----------------
els.append(f'<div id="mb" class="layer"><div id="mbBar" class="mbbar"></div><div id="mb1" class="mbt">MEDALS</div><div id="mb2" class="mbt" style="top:430px;color:#fff">&amp; BELTS</div></div>')
show("#mb", b(40), b(44) - 0.05, 0, 0.3)
FROM("#mbBar", b(40), 0.35, {"scaleX": 0, "transformOrigin": "0% 50%"}, {"scaleX": 1}, "expo.out")
FROM("#mb1", b(40) + 0.08, 0.4, {"x": -120, "opacity": 0}, {"x": 0, "opacity": 1}, "expo.out")
FROM("#mb2", b(41), 0.4, {"x": 120, "opacity": 0}, {"x": 0, "opacity": 1}, "expo.out")
CUE(b(40), "curated/zoom-swish.wav", -12); CUE(b(41), "thock.wav", -14)

# ---------------- PAYOFF: TAHNIAH! (beat 76) with gold particles, held over the medal-group clip ----------------
random.seed(21); parts = []
for i in range(46):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(220, 560); s = random.uniform(8, 18)
    parts.append(f'<i id="pt{i}" class="pt" style="width:{s:.0f}px;height:{s:.0f}px"></i>')
    INIT(f"#pt{i}", {"x": 0, "y": 0, "opacity": 0, "scale": 0.4})
    t = b(76) + random.uniform(0, 0.25)
    SET(f"#pt{i}", t, {"opacity": 1}); J(f"#pt{i}", t, random.uniform(1.0, 1.6), {"x": round(r * math.cos(a)), "y": round(r * math.sin(a) * 0.55 + random.uniform(40, 160)), "scale": 1, "opacity": 0}, "power2.out")
els.append(f'''<div id="th" class="layer">
  <div id="thBg" class="thbg"></div>
  <div id="thParts" class="parts">{"".join(parts)}</div>
  <div id="thW" class="thw">TAHNIAH!</div>
  <div id="thC" class="thc">CONGRATULATIONS</div>
  <div id="thL" class="thl">to all the young Silambam athletes</div></div>''')
show("#th", b(76) - 0.05, b(P.K_END) - 0.05, 0, 0.3)
FROM("#thBg", b(76) - 0.05, 0.4, {"opacity": 0}, {"opacity": 1})
FROM("#thW", b(76), 0.45, {"scale": 2.0, "opacity": 0}, {"scale": 1, "opacity": 1}, "expo.out")
FROM("#thC", b(77), 0.4, {"y": 24, "opacity": 0}, {"y": 0, "opacity": 1})
FROM("#thL", b(78), 0.4, {"y": 20, "opacity": 0}, {"y": 0, "opacity": 1})
CUE(b(76), "sub-impact.wav", -11); CUE(b(76) + 0.05, "sparkle.wav", -12); CUE(b(77), "shimmer.wav", -17)

# ---------------- END CARD (beat 88 -> fade out) ----------------
els.append(f'''<div id="end" class="layer">
  <img id="enBg" class="full" src="assets/p/{P.END_BG}_bg.jpg" alt="">
  <div id="enS1" class="stripe" data-layout-allow-overflow style="top:745px;background:{R}"></div><div id="enS2" class="stripe" data-layout-allow-overflow style="top:865px;background:{BL}"></div>
  <div id="enW" class="word" style="top:735px">SILAMBAM</div>
  <div id="enE" class="ene">HARI SUKAN NEGARA</div>
  <div id="enP" class="enp">{P.EVENT_SUB}</div>
  <div id="enD" class="end">15.11.2026 · {P.EVENT_VENUE}</div></div>''')
show("#end", b(P.K_END), T, 0.35); FROM("#enBg", b(P.K_END), T - b(P.K_END), {"scale": 1.0}, {"scale": 1.1}, "sine.inOut")
FROM("#enS1", b(P.K_END) + 0.1, 0.35, {"scaleX": 0, "transformOrigin": "0% 50%"}, {"scaleX": 1}); FROM("#enS2", b(P.K_END) + 0.15, 0.35, {"scaleX": 0, "transformOrigin": "100% 50%"}, {"scaleX": 1})
FROM("#enW", b(P.K_END) + 0.15, 0.45, {"scale": 1.4, "opacity": 0}, {"scale": 1, "opacity": 1}, "expo.out")
for i, s in enumerate(("#enE", "#enP", "#enD")): FROM(s, b(P.K_END + 2) + i * 0.35, 0.4, {"y": 20, "opacity": 0}, {"y": 0, "opacity": 1})
CUE(b(P.K_END) + 0.15, "thock.wav", -12)
els.append('<div id="fade" class="full" style="background:#000"></div>'); INIT("#fade", {"opacity": 0}); J("#fade", T - 1.1, 1.0, {"opacity": 1}, "power1.in")

CSS = f'''
@font-face {{ font-family: "IDBI"; src: url("assets/fonts/InterDisplay-BlackItalic.otf"); }}
@font-face {{ font-family: "IDB"; src: url("assets/fonts/InterDisplay-Black.otf"); }}
@font-face {{ font-family: "IEBI"; src: url("assets/fonts/InterDisplay-ExtraBoldItalic.otf"); }}
@font-face {{ font-family: "ISB"; src: url("assets/fonts/Inter-SemiBold.otf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
#root {{ position: absolute; inset: 0; overflow: hidden; }}
.vid {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; transform-origin: 50% 40%; }}
#gfx {{ position: absolute; inset: 0; }}
.full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
.card {{ position: absolute; left: 0; top: 240px; width: 1080px; height: 1440px; object-fit: cover; box-shadow: 0 30px 80px rgba(0,0,0,.6); }}
.layer {{ position: absolute; inset: 0; }}
.stripe {{ position: absolute; left: -40px; width: 1160px; height: 26px; transform: skewY(-4deg); }}
.word {{ position: absolute; left: 0; top: 1225px; width: 1080px; text-align: center; font-family: "IDBI"; font-size: 168px; line-height: 1; color: {Y};
        letter-spacing: 2px; -webkit-text-stroke: 3px {INK}; text-shadow: 0 10px 0 {INK}, 0 18px 40px rgba(0,0,0,.55); }}
.sub {{ position: absolute; left: 140px; top: 1430px; width: 800px; text-align: center; font-family: "ISB"; font-size: 34px; letter-spacing: 4px; color: #fff;
       background: rgba(11,11,16,.78); padding: 14px 0; border-radius: 10px; }}
#evBars {{ position: absolute; left: 0; top: 1188px; width: 1080px; }}
.bar {{ height: 12px; margin-bottom: 6px; transform: skewX(-20deg); width: 1100px; }}
.panel {{ position: absolute; left: 72px; top: 1240px; width: 936px; height: 470px; background: rgba(11,11,16,.84); border-radius: 22px; padding: 34px 40px; }}
.evs {{ font-family: "ISB"; font-size: 34px; letter-spacing: 8px; color: #fff; }}
.evbig {{ font-family: "IDBI"; font-size: 78px; line-height: 1.15; margin-top: 6px; white-space: nowrap; }}
.evbig span {{ display: inline-block; }}
.evsub {{ font-family: "IEBI"; font-size: 40px; color: #fff; letter-spacing: 1px; margin-top: 4px; }}
.pill {{ display: flex; align-items: center; gap: 16px; font-family: "ISB"; font-size: 36px; color: #fff; margin-top: 22px; }}
.tag {{ position: absolute; left: 72px; top: 1500px; display: flex; align-items: center; gap: 16px; padding: 14px 26px 14px 18px; background: rgba(11,11,16,.8);
       border-radius: 12px; font-family: "IDBI"; font-size: 52px; color: #fff; letter-spacing: 2px; }}
.tag i {{ width: 14px; height: 52px; display: block; transform: skewX(-15deg); }}
.evtag {{ position: absolute; left: 72px; top: 290px; display: flex; align-items: center; gap: 12px; padding: 10px 20px; background: rgba(11,11,16,.72);
         border-radius: 40px; font-family: "ISB"; font-size: 28px; letter-spacing: 2px; color: #fff; }}
.evtag i {{ width: 12px; height: 12px; border-radius: 50%; background: {Y}; display: block; }}
.mbbar {{ position: absolute; left: 0; top: 300px; width: 1080px; height: 270px; background: linear-gradient(90deg, rgba(11,11,16,.9), rgba(11,11,16,.55)); }}
.mbt {{ position: absolute; left: 72px; top: 300px; font-family: "IDBI"; font-size: 120px; line-height: 1.1; color: {Y}; }}
.thbg {{ position: absolute; left: 0; top: 230px; width: 1080px; height: 420px; background: linear-gradient(180deg, rgba(11,11,16,.0), rgba(11,11,16,.82) 25%, rgba(11,11,16,.82) 75%, rgba(11,11,16,0)); }}
.parts {{ position: absolute; left: 540px; top: 360px; }}
.pt {{ position: absolute; display: block; border-radius: 50%; background: {Y}; box-shadow: inset -3px -3px 0 #c88a00; }}
.thw {{ position: absolute; left: 0; top: 290px; width: 1080px; text-align: center; font-family: "IDBI"; font-size: 150px; line-height: 1;
       background: linear-gradient(180deg, #fff6c8, {Y} 45%, #c88a00); -webkit-background-clip: text; background-clip: text; color: transparent;
       filter: drop-shadow(0 8px 0 {INK}); }}
.thc {{ position: absolute; left: 0; top: 465px; width: 1080px; text-align: center; font-family: "IDB"; font-size: 54px; color: #fff; letter-spacing: 10px; }}
.thl {{ position: absolute; left: 0; top: 545px; width: 1080px; text-align: center; font-family: "ISB"; font-size: 38px; color: #ffe9a8; }}
.ene {{ position: absolute; left: 0; top: 960px; width: 1080px; text-align: center; font-family: "IDBI"; font-size: 76px; color: #fff; }}
.enp {{ position: absolute; left: 0; top: 1060px; width: 1080px; text-align: center; font-family: "IEBI"; font-size: 40px; color: #fff; letter-spacing: 1px; }}
.end {{ position: absolute; left: 0; top: 1130px; width: 1080px; text-align: center; font-family: "ISB"; font-size: 36px; color: {Y}; letter-spacing: 2px; }}
'''
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
open("edit/index.html", "w").write(doc)
json.dump({"cues": [{"t": a, "sfx": f, "gain_db": g} for a, f, g in sorted(cues)]}, open("edit/cues.json", "w"), indent=1)
print("built", T, "s;", len(js), "tweens;", len(cues), "cues")
