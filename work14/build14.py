# HyperFrames composition -> edit/index.html. Plate (compose14.py) + HTML motion graphics + mix (mix14.py).
# Prompt Motion techniques adapted (not copied):
#  - "Photo print app launch film" (prompt-motion.com/twoclipping-221cab): a photo that becomes a physical print; elements
#    carried from one scene into the next -> the customer's picture card flies into a pinned "REF" thumbnail while the real
#    statue prints, then becomes the comparison card; text rises out of a mask line.
#  - "Engraving-style Claude ad" (prompt-motion.com/lexnlin-038035): graphic marks painted on top of real imagery -> the
#    slicer outline / nozzle line / ruler drawn over the real statue.
# Facts on screen are the creator's: 3D printed, PETG filament, 6 inch, made from the customer's picture. No invented specs.
import json, html
import plan14 as P
W, S, T = P.W, {s["name"]: s for s in P.SCENES}, P.TOTAL; R = lambda v: round(v, 3)
SW = json.load(open("edit/swatches.json"))
CYAN, SILVER, INK = "#36d6ff", "#d9dde3", "#07090d"
els, js, init = [], [], []
E, J, I = els.append, js.append, init.append
def tw(sel, t, d, props, ease="power3.out"):
    J(f'tl.to("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())},duration:{R(d)},ease:"{ease}"}},{R(t)});')
def st(sel, t, props):
    J(f'tl.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())}}},{R(t)});')
def show(sel, t0, t1, y=14, d=0.3):
    I(f'gsap.set("{sel}",{{opacity:0,y:{y}}});'); tw(sel, t0, d, {"opacity": 1, "y": 0})
    if t1 < T - 0.01: tw(sel, t1 - 0.22, 0.22, {"opacity": 0}, "power2.in")

# ---- captions: Romanized Tamil as spoken + English meaning (CTA line given as English only: wording not fully clear) ----
CAPS = [(0.0, 1.95, "Oru customer enakku request panni", "A customer asked me"),
        (1.95, W["sangili"] - 0.05, "intha picture-la irunthu", "from this picture"),
        (W["sangili"] - 0.05, W["inches"] + 1.0, "intha Sangili Karuppar, oru 6 inches-la", "this Sangili Karuppar, 6 inches"),
        (W["inches"] + 1.0, W["athukkaaga"] - 0.1, "venum nu kettu irunthaanga", "is what they asked for"),
        (W["athukkaaga"] - 0.1, W["design"] - 0.3, "So athukkaaga, avanga ketta photo-la ulla maathiri", "so, just like the photo they sent"),
        (W["design"] - 0.3, S["compare"]["t1"], "naan design panni eduthathu", "I designed and made it"),
        (S["colour"]["t0"], S["colour"]["t1"], "So neenga paakkalaam, avanga kudutha athe colour tone-la", "you can see: the same colour tone they gave"),
        (S["want"]["t0"], W["karuppar2"] - 0.2, "Ungalukkum intha picture venum appadinna", "if you want this too"),
        (W["karuppar2"] - 0.2, S["end"]["t0"], "intha Sangili Karuppar venum appadinna, neenga thaaraalamaa…", "if you want this Sangili Karuppar, feel free…"),
        (S["end"]["t0"], W["vanakkam"] - 0.3, None, "contact me (details in my bio)"),
        (W["vanakkam"] - 0.3, T, "Vanakkam!", None)]
for i, (a, b, ta, en) in enumerate(CAPS):
    body = (f'<span class="t">{html.escape(ta)}</span>' if ta else "") + (f'<br><span class="en">{html.escape(en)}</span>' if en else "")
    E(f'<div id="c{i}" class="cap">{body}</div>')
    I(f'gsap.set("#c{i}",{{opacity:{1 if i == 0 else 0}}});')
    if i: st(f"#c{i}", a, {"opacity": 1})
    if b < T - 0.01: st(f"#c{i}", b, {"opacity": 0})

# ---- customer's picture: hook card -> pinned REF thumbnail (print) -> comparison card -> REF (colour) ----
E('<div id="ref" class="ref"><img src="assets/reference.jpg" alt=""><div class="reftag" id="reftag">CUSTOMER\'S PICTURE</div></div>')
I('gsap.set("#ref",{xPercent:-50,yPercent:-50,x:540,y:1000,rotation:-2.5,scale:1});')
tw("#ref", 0.0, 3.0, {"scale": 1.04}, "none")                       # slow push while he says "from this picture"
p0 = S["print"]["t0"]
tw("#ref", p0 - 0.15, 0.55, {"x": 168, "y": 900, "scale": 0.3, "rotation": -4}, "power3.inOut")
st("#reftag", p0 + 0.2, {"innerText": "REF"})
c0 = S["compare"]["t0"]
tw("#ref", c0, 0.6, {"x": 540, "y": 645, "scale": 0.45, "rotation": 0}, "power3.inOut"); st("#reftag", c0 + 0.3, {"innerText": "CUSTOMER'S PICTURE"})
k0 = S["colour"]["t0"]
tw("#ref", k0 - 0.1, 0.35, {"opacity": 0, "scale": 0.3}, "power2.in")

# ---- 3D PRINT scene: HUD chip + progress, ruler 6 INCH, PETG / 3D PRINTED chips ----
rv = S["print"]["reveal"]
E('<div id="hud" class="hud"><i class="dot"></i><span id="hudt">3D PRINTING</span><b id="pct">0%</b></div>')
show("#hud", rv[0] - 0.1, S["print"]["t1"])
I('gsap.set("#pct",{innerText:0});')
J(f'tl.to("#pct",{{innerText:100,duration:{R(rv[1] - rv[0])},ease:"power3.out",snap:{{innerText:1}},modifiers:{{innerText:v=>Math.round(v)+"%"}}}},{R(rv[0])});')
st("#hudt", rv[1] + 0.05, {"innerText": "PRINTED"}); st("#pct", rv[1] + 0.05, {"innerText": "✓"})
for k in range(4): tw(".hud .dot", rv[0] + k * 0.8, 0.4, {"opacity": 0.25}, "sine.inOut"); tw(".hud .dot", rv[0] + k * 0.8 + 0.4, 0.4, {"opacity": 1}, "sine.inOut")
# ruler beside the statue: base y=1560, top y=500 (layout default), ticks 0..6
ticks = "".join(f'<div class="tk" style="top:{round(1060 - k * 1060 / 6)}px"><span>{k}</span></div>' for k in range(7))
E(f'<div id="ruler" class="ruler"><div class="rl" id="rl"></div>{ticks}<div class="rlab" id="rlab">6 INCH</div></div>')
I('gsap.set("#rl",{scaleY:0}); gsap.set("#ruler .tk",{opacity:0}); gsap.set("#rlab",{opacity:0,y:10});'); st("#ruler", 0, {"opacity": 1})
ri = W["inches"] - 0.15
tw("#rl", ri, 0.7, {"scaleY": 1}, "power3.out")
for k in range(7): tw(f"#ruler .tk:nth-of-type({k + 2})", ri + 0.1 * k, 0.15, {"opacity": 1})
tw("#rlab", ri + 0.7, 0.3, {"opacity": 1, "y": 0}); tw("#ruler", S["print"]["t1"] - 0.25, 0.25, {"opacity": 0}, "power2.in")
SPOOL = '<svg viewBox="0 0 40 40" class="ic"><circle cx="20" cy="20" r="15"/><circle cx="20" cy="20" r="5"/><path d="M20 5v10M20 25v10M5 20h10M25 20h10"/></svg>'
NOZ = '<svg viewBox="0 0 40 40" class="ic"><path d="M10 6h20v10H10zM14 16h12l-4 10h-4zM20 26v8"/><path d="M8 36h24"/></svg>'
E(f'<div id="k1" class="chip" style="top:1215px">{SPOOL}PETG FILAMENT</div>'); show("#k1", W["inches"] + 1.1, S["print"]["t1"])
E(f'<div id="k2" class="chip" style="top:1300px">{NOZ}3D PRINTED</div>'); show("#k2", W["inches"] + 1.6, S["print"]["t1"])

# ---- DESIGN -> REAL labels ----
E('<div id="arrow" class="arrow">▼</div>'); show("#arrow", c0 + 0.5, S["compare"]["t1"])
E('<div id="realtag" class="chip mid" style="top:1690px">REAL · 3D PRINTED IN PETG</div>'); show("#realtag", W["design"], S["compare"]["t1"])

# ---- SAME COLOUR TONE: swatches from the picture vs the print ----
def sw(id_, col, side, y, lab):
    return f'<div id="{id_}" class="sw {side}" style="top:{y}px"><i style="background:{col}"></i><span>{lab}</span></div>'
E(sw("s1", SW["ref"][0], "l", 760, "PICTURE") + sw("s2", SW["ref"][1], "l", 930, "PICTURE") + sw("s3", SW["print"][0], "r", 760, "PRINT") + sw("s4", SW["print"][1], "r", 930, "PRINT"))
for k, sel in enumerate(["#s1", "#s3", "#s2", "#s4"]):
    I(f'gsap.set("{sel}",{{opacity:0,x:{-40 if sel in ("#s1", "#s2") else 40}}});')
    tw(sel, W["colour"] - 0.4 + 0.15 * k, 0.35, {"opacity": 1, "x": 0}); tw(sel, S["colour"]["t1"] - 0.25, 0.25, {"opacity": 0}, "power2.in")
E('<div id="tone" class="chip mid big" style="top:1110px">✓ SAME COLOUR TONE</div>'); show("#tone", W["colour"] + 0.9, S["colour"]["t1"])

# ---- WANT ONE? ----
E('<div id="want" class="want"><div class="wi" id="wi">WANT ONE?</div></div>')
I('gsap.set("#wi",{yPercent:110,opacity:0});'); st("#wi", S["want"]["t0"] + 0.1, {"opacity": 1}); tw("#wi", S["want"]["t0"] + 0.15, 0.5, {"yPercent": 0}, "power4.out"); tw("#wi", S["want"]["t1"] - 0.3, 0.3, {"yPercent": -110}, "power3.in")
for k, txt in enumerate(["6 INCH", "PETG", "3D PRINTED"]):
    E(f'<div id="w{k}" class="pill" style="left:{[150, 445, 680][k]}px">{txt}</div>'); show(f"#w{k}", S["want"]["t0"] + 1.2 + 0.3 * k, S["want"]["t1"])

# ---- END card ----
e0 = S["end"]["t0"]
E('<div id="end" class="endc"><div class="e1"><span id="e1">SANGILI KARUPPAR</span></div><div class="e2" id="e2">3D PRINTED STATUE · PETG · 6 INCH</div>'
  '<div class="cta" id="cta">CONTACT · LINK IN BIO</div></div>')
I('gsap.set("#e1",{yPercent:110}); gsap.set("#e2",{opacity:0,y:12}); gsap.set("#cta",{opacity:0,scale:0.85});')
tw("#e1", e0 + 0.2, 0.5, {"yPercent": 0}, "power4.out"); tw("#e2", e0 + 0.5, 0.35, {"opacity": 1, "y": 0}); tw("#cta", e0 + 0.85, 0.35, {"opacity": 1, "scale": 1}, "back.out(1.8)")

doc = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "IDB"; src: url("assets/fonts/InterDisplay-Black.otf"); font-weight: 900; }}
      @font-face {{ font-family: "IDBo"; src: url("assets/fonts/InterDisplay-Bold.otf"); font-weight: 700; }}
      @font-face {{ font-family: "ISB"; src: url("assets/fonts/Inter-SemiBold.otf"); font-weight: 600; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
      .clip {{ position: absolute; inset: 0; }}
      .vid {{ width: 1080px; height: 1920px; object-fit: cover; }}
      #gfx {{ z-index: 10; pointer-events: none; }}
      .cap {{ position: absolute; left: 60px; width: 960px; top: 272px; text-align: center; }}
      .cap .t {{ display: inline; font-family: "IDBo"; font-size: 46px; line-height: 1.3; color: #fff; padding: 6px 18px; border-radius: 12px;
        background: rgba(7,9,13,.78); -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
      .cap .en {{ display: inline-block; margin-top: 10px; font-family: "ISB"; font-size: 31px; color: {CYAN}; padding: 4px 14px; border-radius: 8px; background: rgba(7,9,13,.7); }}
      .ref {{ position: absolute; left: 0; top: 0; width: 560px; padding: 16px 16px 64px; background: #f4f4f2; border-radius: 6px; box-shadow: 0 30px 70px rgba(0,0,0,.6); }}
      .ref img {{ display: block; width: 528px; height: auto; border-radius: 2px; }}
      .reftag {{ position: absolute; left: 0; right: 0; bottom: 12px; text-align: center; font-family: "IDB"; font-size: 30px; letter-spacing: 4px; color: #111; }}
      .hud {{ position: absolute; left: 80px; top: 500px; height: 64px; padding: 0 22px; border-radius: 12px; display: flex; align-items: center; gap: 14px;
        background: rgba(7,9,13,.75); border: 1.5px solid rgba(54,214,255,.55); font-family: "IDB"; font-size: 30px; letter-spacing: 3px; color: #fff; }}
      .hud .dot {{ width: 14px; height: 14px; border-radius: 50%; background: {CYAN}; box-shadow: 0 0 12px {CYAN}; display: block; }}
      .hud b {{ color: {CYAN}; min-width: 74px; text-align: right; }}
      .ruler {{ position: absolute; left: 905px; top: 500px; width: 120px; height: 1060px; }}
      .rl {{ position: absolute; left: 0; top: 0; width: 4px; height: 1060px; background: {CYAN}; box-shadow: 0 0 10px {CYAN}; transform-origin: 50% 100%; }}
      .tk {{ position: absolute; left: 0; width: 26px; height: 3px; background: {CYAN}; }}
      .tk span {{ position: absolute; left: 34px; top: -18px; font-family: "IDBo"; font-size: 28px; color: {SILVER}; }}
      .rlab {{ position: absolute; left: -150px; top: -86px; width: 260px; text-align: right; font-family: "IDB"; font-size: 46px; color: {CYAN}; letter-spacing: 1px; }}
      .chip {{ position: absolute; left: 80px; height: 66px; padding: 0 22px 0 14px; border-radius: 12px; display: flex; align-items: center; gap: 12px;
        background: rgba(7,9,13,.8); border: 1.5px solid rgba(217,221,227,.45); font-family: "IDB"; font-size: 30px; letter-spacing: 3px; color: #fff; white-space: nowrap; }}
      .chip.mid {{ left: 540px; transform: translateX(-50%); padding: 0 26px; }}
      .chip.big {{ height: 80px; font-size: 38px; border-color: {CYAN}; color: {CYAN}; }}
      .ic {{ width: 40px; height: 40px; fill: none; stroke: {CYAN}; stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round; }}
      .arrow {{ position: absolute; left: 0; width: 1080px; top: 846px; text-align: center; font-family: "IDB"; font-size: 40px; color: {CYAN}; text-shadow: 0 0 14px {CYAN}; }}
      .sw {{ position: absolute; width: 160px; display: flex; flex-direction: column; align-items: center; gap: 10px; }}
      .sw.l {{ left: 60px; }} .sw.r {{ left: 860px; }}
      .sw i {{ display: block; width: 110px; height: 110px; border-radius: 50%; border: 4px solid rgba(255,255,255,.85); box-shadow: 0 10px 26px rgba(0,0,0,.5); }}
      .sw span {{ font-family: "IDB"; font-size: 24px; letter-spacing: 3px; color: {SILVER}; background: rgba(7,9,13,.7); padding: 2px 10px; border-radius: 6px; }}
      .want {{ position: absolute; left: 0; width: 1080px; top: 470px; overflow: hidden; text-align: center; }}
      .wi {{ font-family: "IDB"; font-size: 112px; letter-spacing: -2px; color: #fff; text-shadow: 0 10px 30px rgba(0,0,0,.6); }}
      .pill {{ position: absolute; top: 1610px; height: 64px; line-height: 64px; padding: 0 24px; border-radius: 32px; background: {CYAN}; color: {INK};
        font-family: "IDB"; font-size: 30px; letter-spacing: 2px; box-shadow: 0 10px 24px rgba(0,0,0,.45); }}
      .endc {{ position: absolute; left: 0; width: 1080px; top: 1130px; text-align: center; }}
      .e1 {{ overflow: hidden; }} .e1 span {{ display: inline-block; font-family: "IDB"; font-size: 84px; color: #fff; letter-spacing: -1px; }}
      .e2 {{ margin-top: 8px; font-family: "IDBo"; font-size: 34px; color: {SILVER}; letter-spacing: 2px; }}
      .cta {{ display: inline-block; margin-top: 26px; background: {CYAN}; color: {INK}; font-family: "IDB"; font-size: 40px; letter-spacing: 3px; padding: 18px 36px; border-radius: 14px;
        box-shadow: 0 0 30px rgba(54,214,255,.45); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{T}">
      <video id="plate" class="clip vid" src="assets/v/plate.mp4" muted playsinline data-start="0" data-duration="{T}" data-track-index="1" style="z-index:1"></video>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{T}" data-track-index="2" data-volume="1"></audio>
      <div id="gfx" class="clip" data-start="0" data-duration="{T}" data-track-index="3">
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
open("edit/index.html", "w").write(doc); print("built", T, len(js), "timeline entries")
