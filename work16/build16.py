# HyperFrames composition for v01 → edit/index.html
# Layers: graded plate (picture) < hook/end gradients < reveal bloom < tracked key-hook tags < captions < titles/end card.
# Audio: edit/assets/mix.wav (mix16.py). Every time comes from plan16 (output timeline, frame-snapped).
import json, re, html, os
import plan16 as P
VERSION = os.environ.get("VERSION", "v02")              # v01 = captions/tags/bloom only; v02 adds gfx_v02 motion graphics
FPS = P.FPS; TOT = round(P.TOTAL, 4)
fr = lambda t: round(round(t * FPS) / FPS, 4)
tags = json.load(open("edit/hook_tags.json"))
R = fr(P.out_t("reveal", P.REVEAL_SRC))
END0 = fr(P.S["end"]["o0"])

def cap_html(i, text, pos=""):
    t = html.escape(text)
    t = re.sub(r"\*(.+?)\*", r'<b>\1</b>', t)
    return f'<div id="c{i}" class="cap {pos}"><span class="t">{t}</span></div>'

caps = [(fr(P.out_t(c[0], c[1])), fr(P.out_t(c[0], c[2])), c[3], c[4] if len(c) > 4 else "") for c in P.CAPS]
CAPS = "\n".join(cap_html(i, txt, pos) for i, (_, _, txt, pos) in enumerate(caps))
if VERSION >= "v02":
    import gfx_v02
    G_CSS, G_HTML, G_JS, G_CUES, END_DELAY = gfx_v02.build(fr, R, END0)
else:
    G_CSS, G_HTML, G_JS, END_DELAY = "", "", [], 0.0
    G_CUES = [(END0 + 0.25, "thock.wav", -12, "end card name lands"), (END0 + 0.75, "curated/ui-pop.wav", -14, "handle pill pops")]
json.dump([list(c) for c in G_CUES], open("edit/gfx_cues.json", "w"), indent=0)
TAGS = "\n".join(f'<div id="k{i}" class="ktag"><span>{i + 1}</span></div>' for i in range(5))

js = []
add = js.append
# --- initial states (set with gsap.set so frame 0 is correct on any seek)
add('gsap.set(".cap",{opacity:0,y:16});')
add('gsap.set(".ktag",{opacity:0,scale:0.4});')
add('gsap.set("#bloom",{opacity:0,scale:0.6});')
add('gsap.set(".spk",{opacity:0});')
add('gsap.set("#endshade",{opacity:0}); gsap.set("#endcard .ln",{yPercent:110}); gsap.set("#rule",{scaleX:0}); gsap.set("#handle",{opacity:0,scale:0.85}); gsap.set("#sub",{opacity:0,y:12});')
add('gsap.set("#hook",{opacity:1}); gsap.set("#hk1",{scale:1.06}); gsap.set("#hk2",{opacity:0.0,y:14}); gsap.set(".chip",{opacity:0,y:16});')
add('const tl = gsap.timeline({ paused: true });')
# --- hook: title is on screen from frame 0, settles, chips pop, everything clears before the cut
add('tl.to("#hk1",{scale:1,duration:0.5,ease:"power3.out"},0);')
add('tl.to("#hk2",{opacity:1,y:0,duration:0.35,ease:"power3.out"},0.15);')
add('tl.to("#ch1",{opacity:1,y:0,duration:0.3,ease:"back.out(1.7)"},0.6);')
add('tl.to("#ch2",{opacity:1,y:0,duration:0.3,ease:"back.out(1.7)"},0.85);')
add(f'tl.to("#hook",{{opacity:0,duration:0.2,ease:"power2.in"}},{fr(P.S["story"]["o0"]) - 0.2});')
# --- captions: stable phrases, quick fade/rise, never overlapping
for i, (a, b, _, _) in enumerate(caps):
    add(f'tl.to("#c{i}",{{opacity:1,y:0,duration:0.14,ease:"power2.out"}},{a});')
    add(f'tl.to("#c{i}",{{opacity:0,duration:0.1,ease:"power1.in"}},{round(b - 0.1, 4)});')
# --- tracked key-hook tags: per-frame positions from track_hooks16.py, numbers pop one by one
fk = sorted(int(k) for k in tags["frames"])
for i in range(5):
    pts = [(k, tags["frames"][str(k)][i]) for k in fk]
    k0, (x0, y0) = pts[0]
    add(f'gsap.set("#k{i}",{{x:{x0 - 34},y:{y0 - 150}}});')
    for (ka, _), (kb, (xb, yb)) in zip(pts, pts[1:]):
        add(f'tl.to("#k{i}",{{x:{xb - 34},y:{yb - 150},duration:{1 / FPS:.5f},ease:"none"}},{ka / FPS:.4f});')
    add(f'tl.to("#k{i}",{{opacity:1,scale:1,duration:0.22,ease:"back.out(2.2)"}},{fr(tags["pops"][i])});')
    add(f'tl.to("#k{i}",{{opacity:0,scale:0.6,duration:0.16,ease:"power2.in"}},{fr(tags["hide"]) + i * 0.03:.4f});')
# --- lamp reveal: warm bloom on the first lamp, a few sparks, then settle
add(f'tl.to("#bloom",{{opacity:0.85,scale:1,duration:0.28,ease:"power2.out"}},{R});')
add(f'tl.to("#bloom",{{opacity:0.28,scale:1.25,duration:1.0,ease:"sine.out"}},{R + 0.28:.4f});')
add(f'tl.to("#bloom",{{opacity:0,duration:0.5,ease:"sine.in"}},{fr(P.S["glow"]["o1"]) - 0.4:.4f});')
for j in range(7):
    d = 0.9 + 0.12 * j
    add(f'tl.fromTo("#s{j}",{{opacity:0,x:0,y:0}},{{opacity:1,duration:0.15,ease:"none"}},{R + 0.05 * j:.4f});')
    add(f'tl.to("#s{j}",{{x:{[-60, 40, 90, -20, 130, 20, -90][j]},y:{[-140, -190, -110, -230, -160, -90, -170][j]},opacity:0,duration:{d:.2f},ease:"power1.out"}},{R + 0.05 * j + 0.15:.4f});')
js.extend(G_JS)
# --- end card
add(f'tl.to("#endshade",{{opacity:1,duration:0.5,ease:"sine.inOut"}},{END0});')
add(f'tl.to("#e1",{{yPercent:0,duration:0.5,ease:"power4.out"}},{END0 + END_DELAY + 0.25:.4f});')
add(f'tl.to("#rule",{{scaleX:1,duration:0.45,ease:"power3.out"}},{END0 + END_DELAY + 0.45:.4f});')
add(f'tl.to("#sub",{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{END0 + END_DELAY + 0.55:.4f});')
add(f'tl.to("#handle",{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"}},{END0 + END_DELAY + 0.75:.4f});')
add(f'tl.set({{}},{{}},{TOT});')
add('window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl;')
JS = "\n      ".join(js)

KEY = '<svg viewBox="0 0 40 40" class="ic"><circle cx="13" cy="20" r="7"/><path d="M20 20h16M30 20v6M35 20v4"/></svg>'
BULB = '<svg viewBox="0 0 40 40" class="ic"><path d="M20 5a11 11 0 0 0-6 20v4h12v-4A11 11 0 0 0 20 5z"/><path d="M15 33h10M16 37h8"/></svg>'
SPARKS = "".join(f'<i id="s{j}" class="spk" style="left:{[230, 250, 270, 215, 290, 240, 205][j]}px;top:{[830, 815, 840, 850, 825, 860, 820][j]}px"></i>' for j in range(7))

doc = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "IDB"; src: url("assets/fonts/InterDisplay-Black.otf"); font-weight: 900; }}
      @font-face {{ font-family: "IDBo"; src: url("assets/fonts/InterDisplay-Bold.otf"); font-weight: 700; }}
      @font-face {{ font-family: "ISB"; src: url("assets/fonts/Inter-SemiBold.otf"); font-weight: 600; }}
      :root {{ --cream: #fff4e2; --gold: #e9c16b; --ink: rgba(18,13,10,.80); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b0908; }}
      .clip {{ position: absolute; inset: 0; }}
      .vid {{ width: 1080px; height: 1920px; object-fit: cover; }}
      #gfx {{ z-index: 10; pointer-events: none; }}
      /* captions: centred on the canvas, bottom edge at y=1240 (inside the 269–1248 safe band), max 720 px */
      .cap {{ position: absolute; left: 180px; width: 720px; bottom: 680px; text-align: center; text-wrap: balance; }}
      .cap .t {{ display: inline; font-family: "IDBo"; font-size: 54px; line-height: 1.32; color: var(--cream); padding: 6px 20px;
        border-radius: 14px; background: var(--ink); -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
      .cap.top {{ bottom: auto; top: 290px; }}
      .cap b {{ color: var(--gold); font-family: "IDB"; font-weight: 900; }}
      /* hook */
      #hook {{ position: absolute; left: 0; width: 1080px; top: 262px; text-align: center; }}
      #hk2 {{ font-family: "ISB"; font-size: 34px; letter-spacing: 7px; color: var(--gold); margin-bottom: 10px; }}
      #hk1 {{ font-family: "IDB"; font-size: 100px; line-height: 0.98; letter-spacing: -1px; color: var(--cream);
        text-shadow: 0 6px 30px rgba(0,0,0,.55); transform-origin: 50% 60%; }}
      #hk1 b {{ color: var(--gold); }}
      .chips {{ margin-top: 22px; display: flex; justify-content: center; gap: 18px; }}
      .chip {{ height: 66px; padding: 0 24px 0 16px; border-radius: 33px; display: flex; align-items: center; gap: 10px;
        background: var(--ink); border: 2px solid rgba(233,193,107,.7); font-family: "IDB"; font-size: 30px; letter-spacing: 3px; color: var(--cream); }}
      .ic {{ width: 38px; height: 38px; fill: none; stroke: var(--gold); stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }}
      /* tracked key-hook tags (68 px badge + stem down to the hook) */
      .ktag {{ position: absolute; left: 0; top: 0; width: 68px; height: 150px; transform-origin: 34px 34px; }}
      .ktag span {{ display: flex; align-items: center; justify-content: center; width: 68px; height: 68px; border-radius: 50%;
        background: var(--gold); color: #1a120b; font-family: "IDB"; font-size: 40px; box-shadow: 0 6px 18px rgba(0,0,0,.5); }}
      .ktag::after {{ content: ""; position: absolute; left: 32px; top: 70px; width: 4px; height: 62px; border-radius: 2px;
        background: linear-gradient(180deg, var(--gold), rgba(233,193,107,0)); }}
      /* lamp reveal */
      #bloom {{ position: absolute; left: -160px; top: 440px; width: 760px; height: 760px; border-radius: 50%; mix-blend-mode: screen;
        background: radial-gradient(circle, rgba(255,214,140,.85) 0%, rgba(255,180,90,.42) 26%, rgba(255,150,60,.12) 52%, rgba(255,150,60,0) 70%); }}
      .spk {{ position: absolute; width: 10px; height: 10px; border-radius: 50%; background: #ffe2a8; box-shadow: 0 0 14px 4px rgba(255,205,120,.8); }}
      /* end card */
      #endshade {{ background: radial-gradient(ellipse at 50% 50%, rgba(10,8,6,.62) 0%, rgba(10,8,6,.78) 60%, rgba(10,8,6,.86) 100%); }}
      #endcard {{ position: absolute; left: 0; width: 1080px; top: 760px; text-align: center; }}
      #endcard .m {{ overflow: hidden; display: block; }}
      #e1 {{ display: inline-block; font-family: "IDB"; font-size: 92px; letter-spacing: 6px; color: var(--cream); }}
      #rule {{ width: 420px; height: 4px; margin: 26px auto 24px; background: var(--gold); border-radius: 2px; }}
      #sub {{ font-family: "IDBo"; font-size: 46px; color: var(--gold); letter-spacing: 1px; }}
      #handle {{ display: inline-block; margin-top: 46px; padding: 14px 36px; border-radius: 40px; border: 2px solid rgba(255,244,226,.6);
        font-family: "IDBo"; font-size: 44px; color: var(--cream); background: rgba(255,255,255,.06); }}
      {G_CSS}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{TOT}">
      <video id="plate" class="clip vid" src="assets/v/plate.mp4" muted playsinline data-start="0" data-duration="{TOT}" data-track-index="1" style="z-index:1"></video>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{TOT}" data-track-index="2" data-volume="1"></audio>
      <div id="gfx" class="clip" data-start="0" data-duration="{TOT}" data-track-index="3">
                <div id="bloom"></div>
        {SPARKS}
        {TAGS}
        {CAPS}
        <div id="hook">
          <div id="hk2">QUICK REVIEW</div>
          <div id="hk1"><b>3D</b> WALL<br>FRAME ART</div>
          <div class="chips"><div id="ch1" class="chip">{KEY}KEY HOLDER</div><div id="ch2" class="chip">{BULB}LAMPS</div></div>
        </div>
        <div id="endshade" class="clip"></div>
        {G_HTML}
        <div id="endcard">
          <span class="m"><span id="e1" class="ln">ESHAN CREATIONS</span></span>
          <div id="rule"></div>
          <div id="sub">Custom 3D Wall Frame Art</div>
          <div id="handle">@e_shan9</div>
        </div>
      </div>
    </div>
    <script>
      {JS}
    </script>
  </body>
</html>
'''
open("edit/index.html", "w").write(doc)
open("edit/meta.json", "w").write(json.dumps({"id": "eshan-3d-wall-frame-keyholder", "name": "eshan-3d-wall-frame-keyholder",
                                               "createdAt": "2026-11-08T07:00:00.000Z"}, indent=2))
open("edit/package.json", "w").write(json.dumps({"name": "edit", "private": True, "type": "module", "scripts": {
    "dev": "npx --yes hyperframes@0.8.193 preview", "check": "npx --yes hyperframes@0.8.193 check",
    "render": "npx --yes hyperframes@0.8.193 render"}}, indent=2))
print("index.html written; total", TOT, "reveal", R, "end", END0, "captions", len(caps))
for a, b, t, _ in caps: print(f"  {a:6.2f}-{b:6.2f} {t}")
