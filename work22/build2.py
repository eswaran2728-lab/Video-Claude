"""v02+ builder for the statue reel: premium 3D-printing graphics.
usage: python3 build2.py v02
Scene A (create): slicer hologram + CAD wireframe on a perspective build plate, the grey print rising layer by layer
under a modelled hotend (sparks, hot bead), then a brush-stroke paint reveal and a gold glint.
Scene B (details): the 4K still zoomed about anchors, with 3D orbit rings, CAD leader lines and glass labels.
Scene C (reveal): parallax pull-back (cut-out statue over a clean, defocused background) into the real footage.
Scene D (end): podium/turntable with rings, light rays, reflection and brand card. All time is output seconds."""
import json, os, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))
V = sys.argv[1] if len(sys.argv) > 1 else 'v02'
P = json.load(open(os.path.join(ROOT, V, 'edit-plan.json')))
R = json.load(open(os.path.join(ROOT, V, 'statue_rows.json')))
W, H, FPS = 1080, 1920, 30
SW, SH = 2160, 3840
X0, Y0, X1, Y1 = R['crop']; CW, CH = X1 - X0, Y1 - Y0
e = html.escape

at, t = {}, 0.0
for s in P['shots']:
    s['at'] = round(t, 3); at[s['id']] = s['at']; t = round(t + s['dur'], 3)
TOTAL = round(t, 3)
json.dump({'total': TOTAL, 'shots': [{k: s.get(k) for k in ('id', 'kind', 'src_time', 'at', 'dur', 'why')} for s in P['shots']]},
          open(os.path.join(ROOT, V, 'timing-map.json'), 'w'), indent=1)
S = {s['id']: s for s in P['shots']}
js, body = [], []

def words(txt, cls):
    return ''.join(f'<span class="wm"><span class="w {cls}">{e(w)}</span></span> ' for w in txt.split())

# ---------------- Scene A: create (print + paint) ----------------
A = S['p1']; a0, ad = A['at'], A['dur']; pr = A['print']
K = A['scale']; SX, SY = A['pos']            # statue crop placed at (SX,SY) with scale K
ps, pe = a0 + pr['scan'][0], a0 + pr['scan'][1]
bs, be = a0 + pr['paint'][0], a0 + pr['paint'][1]
rows = [[round(SY + y * K, 1), round(SX + x0 * K, 1), round(SX + x1 * K, 1)] for y, x0, x1 in R['rows']]
top_y, bot_y = rows[0][0], rows[-1][0]
body.append(f'''      <div id="sA" class="clip scene" data-start="{a0:.3f}" data-duration="{ad:.3f}" data-track-index="1" data-track-kind="graphics">
        <div class="studio"></div><div id="beamA" class="beam"></div>
        <div class="platew" style="top:{bot_y-230:.0f}px"><div id="plate" class="plate"><div class="pgrid"></div><div class="pedge"></div></div></div>
        <div id="statA" class="statw" style="left:{SX}px; top:{SY}px; width:{CW*K:.1f}px; height:{CH*K:.1f}px">
          <img id="tp" class="lay" src="assets/img/toolpath.png" alt=""><img id="wf" class="lay" src="assets/img/wire.png" alt="">
          <div id="greyw" class="lay"><img class="lay" src="assets/img/statue_grey.png" alt=""></div>
          <div id="colw" class="lay"><img class="lay" src="assets/img/statue_colour.png" alt=""></div>
          <div id="glint" class="lay glint"></div>
        </div>
        <div id="bead" class="bead"></div>
        <div id="noz" class="noz"><div class="fan"></div><div class="sink"></div><div class="block"></div><div class="tip"></div><div class="hot"></div></div>
        <div id="sparks">{''.join(f'<i id="sp{i}"></i>' for i in range(28))}</div>
        <svg id="brushA" class="brush" viewBox="0 0 1080 1920"><path id="bstroke" pathLength="1" d="M 120 120 C 380 520, 300 900, 640 1150 S 1000 1500, 960 1840" /></svg>
        <div id="hud" class="hud"><svg viewBox="0 0 120 120"><circle class="trk" cx="60" cy="60" r="50"/><circle id="ring" class="prg" cx="60" cy="60" r="50" pathLength="1"/></svg>
          <div class="hudt"><div id="hudk" class="hk">Printing</div><div class="hn"><span id="pct">0</span>%</div></div></div>
      </div>''')
js.append(f'''      const ROWS = {json.dumps(rows)};
      const rowAt = y => {{ let lo = ROWS[0]; for (const r of ROWS) {{ if (r[0] <= y) lo = r; else break; }} return lo; }};
      const nozX = (t, y) => {{ const r = rowAt(y); return r[1] + (r[2] - r[1]) * (0.5 + 0.5 * Math.sin(t * 13.0)); }};
      const scanY = t => {bot_y} - ({bot_y} - {top_y}) * Math.min(1, Math.max(0, (t - {ps}) / {pe-ps}));
      gsap.set("#greyw", {{ clipPath: "inset(100% 0% 0% 0%)" }});
      gsap.set("#colw", {{ clipPath: "polygon(0% 0%,0% 0%,0% 0%)" }});
      const pst = {{ t: {ps} }};
      tl.to(pst, {{ t: {pe}, duration: {pe-ps:.3f}, ease: "none", onUpdate: () => {{
        const y = scanY(pst.t), f = ({bot_y} - y) / ({bot_y} - {top_y});
        document.querySelector("#greyw").style.clipPath = "inset(" + ((y - {SY}) / {CH*K:.2f} * 100).toFixed(2) + "% 0% 0% 0%)";
        const x = nozX(pst.t, y);
        gsap.set("#noz", {{ x: x - 60, y: y - 186 }}); gsap.set("#bead", {{ x: x - 70, y: y - 3, opacity: 1 }});
        document.querySelector("#pct").textContent = Math.round(f * 100);
        document.querySelector("#ring").style.strokeDashoffset = (1 - f).toFixed(4);
      }} }}, {ps});
      gsap.set("#noz", {{ x: nozX({ps}, {bot_y}) - 60, y: {bot_y} - 186 }});
      tl.to("#noz", {{ y: -260, opacity: 0, duration: 0.45, ease: "power2.in" }}, {pe});
      tl.to("#bead", {{ opacity: 0, duration: 0.2 }}, {pe});
      for (let i = 0; i < 28; i++) {{
        const ts = {ps} + ({pe-ps:.3f} - 0.3) * ((i * 0.618) % 1), y = scanY(ts), x = nozX(ts, y);
        const ang = -Math.PI * (0.15 + 0.7 * ((i * 0.37) % 1)), sp = 60 + 90 * ((i * 0.73) % 1);
        tl.fromTo("#sp" + i, {{ x: x, y: y, opacity: 1, scale: 1 }}, {{ x: x + Math.cos(ang) * sp, y: y + Math.sin(ang) * sp + 50, opacity: 0, scale: 0.3, duration: 0.55, ease: "power2.out", immediateRender: false }}, ts);
      }}
      tl.fromTo("#tp", {{ opacity: 0.85 }}, {{ opacity: 0, duration: 0.5 }}, {pe-0.1});
      tl.fromTo("#wf", {{ opacity: 0.9 }}, {{ opacity: 0, duration: 0.5 }}, {pe-0.1});
      tl.to("#hudk", {{ color: "#f0c35b", duration: 0.2 }}, {bs});
      tl.call(() => {{}}, null, {bs});
      tl.to("#hud", {{ opacity: 0, y: 20, duration: 0.3 }}, {pe+0.25});
      (function(){{ const el = document.querySelector("#colw"); const st = {{ p: 0 }};
        const pts = n => {{ const o = []; for (let j = 0; j <= 30; j++) {{ const yy = j / 30 * 100; o.push([n - yy * 0.6 + Math.sin(j * 2.1) * 2.6 + Math.sin(j * 4.7) * 1.3, yy]); }} return o; }};
        tl.to(st, {{ p: 1, duration: {be-bs:.3f}, ease: "power1.inOut", onUpdate: () => {{ const n = -8 + st.p * 175; const q = pts(n);
          el.style.clipPath = st.p <= 0 ? "polygon(0% 0%,0% 0%,0% 0%)" : "polygon(" + q.map(v => v[0].toFixed(2) + "% " + v[1] + "%").join(",") + ",-5% 100%,-5% 0%)"; }} }}, {bs});
      }})();
      tl.fromTo("#bstroke", {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: {be-bs:.3f}, ease: "power1.inOut" }}, {bs});
      tl.to("#brushA", {{ opacity: 0, duration: 0.3 }}, {be});
      tl.fromTo("#glint", {{ backgroundPosition: "-120% 0%" }}, {{ backgroundPosition: "220% 0%", duration: 0.8, ease: "power2.inOut" }}, {be+0.1});
      tl.fromTo("#plate", {{ rotationZ: -10 }}, {{ rotationZ: 10, duration: {ad}, ease: "none" }}, {a0});
      tl.fromTo("#statA", {{ scale: 1.0 }}, {{ scale: 1.06, transformOrigin: "50% 92%", duration: {ad}, ease: "none" }}, {a0});
      tl.fromTo("#beamA", {{ opacity: 0.55, rotation: -6 }}, {{ opacity: 0.9, rotation: 4, duration: {ad}, ease: "sine.inOut" }}, {a0});
      tl.to("#sA", {{ opacity: 0, duration: 0.18 }}, {a0+ad-0.18});''')

# ---------------- Scene B: details ----------------
def xy(anchor, screen, k): return round(screen[0] - anchor[0] * k, 2), round(screen[1] - anchor[1] * k, 2)
for c in P['callouts']:
    s = S[c['shot']]; sid, s0, sd = s['id'], s['at'], s['dur']
    k0, k1 = W / s['cw0'], W / s['cw1']; a = s['anchor']; sc = s['screen']
    x0, y0 = xy(a, sc, k0); x1, y1 = xy(a, sc, k1)
    ax, ay = sc; lx, ly = c['label_at']; ex = lx; ey = ly
    elbow = [ax + (ex - ax) * 0.55, ey]
    body.append(f'''      <div id="{sid}" class="clip scene" data-start="{s0:.3f}" data-duration="{sd:.3f}" data-track-index="1" data-track-kind="graphics">
        <div id="m-{sid}" class="mv"><img class="still" src="assets/img/hero_graded.jpg" alt=""></div>
        <div class="dvig"></div>
        <div class="orb" style="left:{ax-90}px; top:{ay-90}px"><div id="o1-{sid}" class="ring r1"></div><div id="o2-{sid}" class="ring r2"></div></div>
        <svg class="lead" viewBox="0 0 1080 1920"><circle id="d-{sid}" cx="{ax}" cy="{ay}" r="10"/><path id="l-{sid}" pathLength="1" d="M {ax} {ay} L {elbow[0]:.0f} {elbow[1]:.0f} L {ex} {ey}"/>
          <path class="tick" d="M {ex} {ey-14} L {ex} {ey+14}"/></svg>
        <div id="g-{sid}" class="glass" style="left:{ex + 18}px; top:{ey}px"><div class="gk">{e(c['kicker'])}</div><div class="gt">{e(c['text'])}</div><div class="gbar"></div></div>
        <div id="streak-{sid}" class="streak"></div>
      </div>''')
    js.append(f'''      gsap.set("#m-{sid}", {{ x: {x0}, y: {y0}, scale: {k0}, transformOrigin: "0 0" }});
      tl.to("#m-{sid}", {{ x: {x1}, y: {y1}, scale: {k1}, duration: {sd}, ease: "none" }}, {s0});
      tl.fromTo("#streak-{sid}", {{ x: -1400, opacity: 1 }}, {{ x: 1500, opacity: 1, duration: 0.32, ease: "power2.in", immediateRender: false }}, {s0});
      tl.fromTo("#o1-{sid}", {{ scale: 0.2, opacity: 0, rotationX: 68, rotationZ: 0 }}, {{ scale: 1, opacity: 1, rotationX: 68, rotationZ: 200, duration: {sd-0.2:.2f}, ease: "power2.out" }}, {s0+0.12});
      tl.fromTo("#o2-{sid}", {{ scale: 0.2, opacity: 0, rotationY: 64, rotationZ: 0 }}, {{ scale: 1.25, opacity: 0.8, rotationY: 64, rotationZ: -220, duration: {sd-0.2:.2f}, ease: "power2.out" }}, {s0+0.18});
      tl.fromTo("#d-{sid}", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, {s0+0.15});
      tl.fromTo("#l-{sid}", {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: 0.35, ease: "power2.inOut" }}, {s0+0.25});
      tl.fromTo("#g-{sid}", {{ opacity: 0, x: -30, rotationY: -35 }}, {{ opacity: 1, x: 0, rotationY: 0, duration: 0.45, ease: "power3.out" }}, {s0+0.45});
      tl.fromTo("#g-{sid} .gbar", {{ scaleX: 0 }}, {{ scaleX: 1, transformOrigin: "0 50%", duration: 0.5, ease: "power2.out" }}, {s0+0.6});''')

# ---------------- Scene C: parallax reveal ----------------
C = S['rv']; c0, cd = C['at'], C['dur']
anc = C['anchor']; scr = [anc[0] * 0.5, anc[1] * 0.5]
kb0, ks0 = W / C['cw_bg0'], W / C['cw_st0']
bx0, by0 = xy(anc, scr, kb0); sx0, sy0 = xy(anc, scr, ks0)
body.append(f'''      <div id="sC" class="clip scene" data-start="{c0:.3f}" data-duration="{cd:.3f}" data-track-index="1" data-track-kind="graphics">
        <div id="cb" class="mv"><img class="still" src="assets/img/bg_clean.jpg" alt=""><img id="cbs" class="still" src="assets/img/hero_graded.jpg" alt="" style="opacity:0"></div>
        <div id="cs" class="mv"><img class="crop" src="assets/img/statue_colour.png" alt="" style="left:{X0}px; top:{Y0}px; width:{CW}px; height:{CH}px"></div>
      </div>''')
js.append(f'''      gsap.set("#cb", {{ x: {bx0}, y: {by0}, scale: {kb0}, transformOrigin: "0 0" }});
      gsap.set("#cs", {{ x: {sx0}, y: {sy0}, scale: {ks0}, transformOrigin: "0 0" }});
      tl.to("#cb", {{ x: 0, y: 0, scale: 0.5, duration: {cd-0.35:.2f}, ease: "power3.inOut" }}, {c0});
      tl.to("#cs", {{ x: 0, y: 0, scale: 0.5, duration: {cd-0.35:.2f}, ease: "power3.inOut" }}, {c0});
      tl.to("#cbs", {{ opacity: 1, duration: 0.4 }}, {c0+cd-0.55});
      tl.fromTo("#flash", {{ opacity: 0.45 }}, {{ opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false }}, {c0});''')

# ---------------- real footage ----------------
T_ = S['tn']
body.append(f'''      <div class="vshot"><video id="v-tn" class="clip full" src="assets/video/turn.mp4" muted playsinline data-start="{T_['at']:.3f}" data-duration="{T_['dur']:.3f}" data-media-start="0" data-track-index="2"></video></div>''')

# ---------------- Scene D: podium end card ----------------
D = S['ec']; d0, dd = D['at'], D['dur']; EC = P['endcard']
pk = 0.40; pw, ph = CW * pk, CH * pk; px, py = (W - pw) / 2 + 40, 1715 - ph
body.append(f'''      <div id="sD" class="clip scene" data-start="{d0-0.3:.3f}" data-duration="{dd+0.3:.3f}" style="z-index:3" data-track-index="1" data-track-kind="graphics">
        <div class="studio"></div><div id="rays" class="rays"></div>
        <div class="podw"><div class="ptilt"><div id="pod1" class="pring p1"></div><div id="pod2" class="pring p2"></div><div id="pod3" class="pring p3"></div></div><div class="pglow"></div></div>
        <img class="refl" src="assets/img/statue_colour.png" alt="" style="left:{px:.0f}px; top:{1715-ph*0.06:.0f}px; width:{pw:.0f}px; height:{ph:.0f}px">
        <div id="dst" class="dstat" style="left:{px:.0f}px; top:{py:.0f}px; width:{pw:.0f}px; height:{ph:.0f}px"><img class="lay" src="assets/img/statue_colour.png" alt=""><div id="glint2" class="lay glint"></div></div>
        <div id="dust">{''.join(f'<i style="left:{(i*137.5)%1000+40:.0f}px; top:{(i*211.3)%1300+500:.0f}px; width:{3+i%3*2}px; height:{3+i%3*2}px"></i>' for i in range(26))}</div>
        <div id="endi"><div class="ek">{e(EC['kicker'])}</div><div class="en">{e(EC['name'])}</div><div class="er"></div><div class="es">{e(EC['line'])}</div><div><span class="eh">{e(EC['handle'])}</span></div></div>
      </div>''')
js.append(f'''      tl.fromTo("#sD", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {d0-0.3});
      tl.to("#scrim", {{ opacity: 0, duration: 0.35 }}, {d0});
      tl.fromTo("#dst", {{ y: 60, scale: 0.92, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, transformOrigin: "50% 100%", duration: 0.8, ease: "power3.out" }}, {d0+0.1});
      tl.to("#dst", {{ scale: 1.04, transformOrigin: "50% 100%", duration: {dd-0.9:.2f}, ease: "none" }}, {d0+0.9});
      tl.fromTo("#pod1", {{ rotation: 0 }}, {{ rotation: 120, duration: {dd}, ease: "none" }}, {d0});
      tl.fromTo("#pod2", {{ rotation: 0 }}, {{ rotation: -90, duration: {dd}, ease: "none" }}, {d0});
      tl.fromTo("#pod3", {{ rotation: 0, scale: 0.6, opacity: 0 }}, {{ rotation: 60, scale: 1, opacity: 1, duration: 1.0, ease: "power2.out" }}, {d0});
      tl.fromTo("#rays", {{ rotation: -8, opacity: 0 }}, {{ rotation: 8, opacity: 0.75, duration: {dd}, ease: "none" }}, {d0});
      tl.fromTo("#endi > *", {{ y: 34, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, stagger: 0.12, ease: "power3.out" }}, {d0+0.3});
      tl.fromTo("#endi .er", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.inOut" }}, {d0+0.5});
      tl.fromTo("#glint2", {{ backgroundPosition: "-120% 0%" }}, {{ backgroundPosition: "220% 0%", duration: 1.0, ease: "power2.inOut" }}, {d0+1.0});
      tl.fromTo("#dust i", {{ opacity: 0, y: 30 }}, {{ opacity: 0.85, y: -50, duration: {dd-0.3:.2f}, stagger: {{ each: 0.05 }}, ease: "none" }}, {d0+0.2});''')

# ---------------- titles ----------------
for i, c in enumerate(P['titles']):
    tid = f't{i+1}'
    inner = f'<div class="k"><span class="kl"></span>{e(c["kicker"])}<span class="kl"></span></div>'
    if c.get('title'):
        inner += f'<div class="h">{words(c["title"], "")}</div>'
    body.append(f'      <div id="{tid}" class="clip ttl" data-start="{c["start"]:.3f}" data-duration="{c["end"]-c["start"]:.3f}" data-track-index="3" data-track-kind="graphics">{inner}</div>')
    st = c['start']
    if st > 0:
        js.append(f'      tl.fromTo("#{tid} .k", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out", immediateRender: false }}, {st});')
        js.append(f'      tl.fromTo("#{tid} .w", {{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.55, stagger: 0.07, ease: "power4.out", immediateRender: false }}, {st+0.08});')
    js.append(f'      tl.to("#{tid}", {{ opacity: 0, y: -14, duration: 0.2, ease: "power2.in" }}, {c["end"]-0.22:.3f});')

doc = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width={W}, height={H}">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family:"HSerif"; font-weight:700; src:url("assets/fonts/serif-latin-700.woff2") format("woff2"); }}
      @font-face {{ font-family:"HSans"; font-weight:400; src:url("assets/fonts/sans-latin-400.woff2") format("woff2"); }}
      @font-face {{ font-family:"HSans"; font-weight:700; src:url("assets/fonts/sans-latin-700.woff2") format("woff2"); }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#07080b; }}
      #root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; font-family:"HSans",sans-serif; background:#07080b; }}
      .scene {{ position:absolute; inset:0; overflow:hidden; }}
      .studio {{ position:absolute; inset:0; background:radial-gradient(70% 45% at 50% 72%, #2a1d12 0%, #120d0a 45%, #06070a 100%); }}
      .beam {{ position:absolute; left:140px; top:-200px; width:800px; height:1900px; transform-origin:50% 0%; background:linear-gradient(180deg, rgba(255,214,150,.20), rgba(255,214,150,0) 85%); clip-path:polygon(42% 0, 58% 0, 100% 100%, 0 100%); mix-blend-mode:screen; }}
      .platew {{ position:absolute; left:-110px; width:1300px; height:900px; perspective:1300px; perspective-origin:50% 0%; }}
      .plate {{ position:absolute; inset:0; transform:rotateX(74deg); transform-origin:50% 30%; border-radius:26px;
        background:radial-gradient(60% 60% at 50% 40%, #2a2f3a, #121419 70%); box-shadow:0 0 0 3px rgba(240,195,91,.5), 0 0 90px 10px rgba(240,170,70,.25); }}
      .pgrid {{ position:absolute; inset:0; border-radius:26px; background-image:linear-gradient(rgba(130,220,255,.22) 2px, transparent 2px), linear-gradient(90deg, rgba(130,220,255,.22) 2px, transparent 2px); background-size:64px 64px; }}
      .pedge {{ position:absolute; inset:-8px; border-radius:32px; border:4px solid rgba(255,205,120,.55); }}
      .statw {{ position:absolute; transform-origin:50% 92%; }}
      .lay {{ position:absolute; left:0; top:0; width:100%; height:100%; }}
      #tp {{ filter:drop-shadow(0 0 10px rgba(80,220,255,.85)); }}
      #wf {{ mix-blend-mode:screen; }}
      .glint {{ -webkit-mask-image:url("assets/img/statue_colour.png"); -webkit-mask-size:100% 100%; mask-image:url("assets/img/statue_colour.png"); mask-size:100% 100%;
        background:linear-gradient(105deg, rgba(255,255,255,0) 40%, rgba(255,246,220,.85) 50%, rgba(255,255,255,0) 60%); background-size:60% 100%; background-repeat:no-repeat; background-position:-120% 0%; mix-blend-mode:screen; }}
      .noz {{ position:absolute; left:0; top:0; width:120px; height:190px; z-index:8; filter:drop-shadow(0 18px 24px rgba(0,0,0,.6)); }}
      .noz .fan {{ position:absolute; left:6px; top:0; width:108px; height:58px; border-radius:10px; background:linear-gradient(180deg,#3b3f47,#1b1d22); box-shadow:inset 0 2px 0 rgba(255,255,255,.18); }}
      .noz .fan::after {{ content:""; position:absolute; left:34px; top:9px; width:40px; height:40px; border-radius:50%; background:repeating-conic-gradient(#555b66 0 18deg,#1a1c20 18deg 36deg); box-shadow:0 0 0 3px #2a2d33; }}
      .noz .sink {{ position:absolute; left:18px; top:58px; width:84px; height:56px; background:repeating-linear-gradient(180deg,#c9ced6 0 5px,#6b717b 5px 9px); border-radius:4px; }}
      .noz .block {{ position:absolute; left:26px; top:114px; width:68px; height:40px; border-radius:5px; background:linear-gradient(90deg,#8a8f99,#e7eaee 45%,#9aa0a9); box-shadow:inset 0 -6px 0 rgba(0,0,0,.25); }}
      .noz .tip {{ position:absolute; left:44px; top:154px; width:32px; height:30px; background:linear-gradient(90deg,#9a6a22,#f2c46c 50%,#a8762a); clip-path:polygon(0 0,100% 0,62% 100%,38% 100%); }}
      .noz .hot {{ position:absolute; left:40px; top:168px; width:40px; height:40px; border-radius:50%; background:radial-gradient(circle,rgba(255,240,200,1) 0%,rgba(255,150,40,.85) 35%,rgba(255,90,0,0) 70%); mix-blend-mode:screen; }}
      .bead {{ position:absolute; left:0; top:0; width:140px; height:6px; border-radius:3px; z-index:7; opacity:0; background:linear-gradient(90deg,rgba(255,140,40,0),#ffd9a0 30%,#fff3dc 50%,#ffd9a0 70%,rgba(255,140,40,0)); box-shadow:0 0 18px 6px rgba(255,170,70,.6); }}
      #sparks i {{ position:absolute; left:0; top:0; width:7px; height:7px; border-radius:50%; background:#ffe2a8; box-shadow:0 0 10px 3px rgba(255,170,60,.9); opacity:0; z-index:9; }}
      .brush {{ position:absolute; inset:0; width:{W}px; height:{H}px; z-index:6; overflow:visible; }}
      .brush path {{ fill:none; stroke:#f0c35b; stroke-width:12; stroke-linecap:round; stroke-dasharray:1; filter:drop-shadow(0 0 14px rgba(255,190,80,.9)); }}
      .hud {{ position:absolute; left:50%; top:1720px; transform:translateX(-50%); display:flex; align-items:center; gap:18px; padding:14px 26px 14px 16px; border-radius:999px; z-index:20;
        background:linear-gradient(135deg,rgba(255,255,255,.12),rgba(255,255,255,.03)); border:1.5px solid rgba(255,255,255,.22); box-shadow:0 10px 40px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.25); }}
      .hud svg {{ width:72px; height:72px; transform:rotate(-90deg); }}
      .hud .trk {{ fill:none; stroke:rgba(255,255,255,.15); stroke-width:10; }}
      .hud .prg {{ fill:none; stroke:#5fe0ff; stroke-width:10; stroke-linecap:round; stroke-dasharray:1; stroke-dashoffset:1; filter:drop-shadow(0 0 6px rgba(95,224,255,.9)); }}
      .hk {{ font-weight:700; font-size:28px; letter-spacing:.22em; text-transform:uppercase; color:#8fe9ff; }}
      .hn {{ font-family:"HSerif",serif; font-weight:700; font-size:48px; color:#f8efe0; line-height:1; }}
      .mv {{ position:absolute; left:0; top:0; width:{SW}px; height:{SH}px; }}
      .still {{ position:absolute; left:0; top:0; width:{SW}px; height:{SH}px; }}
      .crop {{ position:absolute; }}
      .full {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
      .vshot {{ position:absolute; inset:0; z-index:2; pointer-events:none; }}
      .dvig {{ position:absolute; inset:0; background:radial-gradient(75% 55% at 50% 52%, rgba(0,0,0,0) 45%, rgba(0,0,0,.55) 100%); }}
      .orb {{ position:absolute; width:180px; height:180px; perspective:600px; }}
      .ring {{ position:absolute; inset:0; border-radius:50%; }}
      .r1 {{ border:4px solid rgba(255,214,140,.95); border-top-color:transparent; box-shadow:0 0 18px rgba(255,190,90,.7); }}
      .r2 {{ border:3px dashed rgba(140,230,255,.9); border-right-color:transparent; }}
      .lead {{ position:absolute; inset:0; width:{W}px; height:{H}px; overflow:visible; }}
      .lead circle {{ fill:#ffe1a0; stroke:#16110b; stroke-width:4; filter:drop-shadow(0 0 8px rgba(255,200,110,.9)); }}
      .lead path {{ fill:none; stroke:#ffe1a0; stroke-width:4; stroke-dasharray:1; filter:drop-shadow(0 2px 6px rgba(0,0,0,.7)); }}
      .lead .tick {{ stroke-dasharray:none; }}
      .glass {{ position:absolute; transform:translateY(-50%); padding:22px 32px 24px; border-radius:22px; transform-origin:0 50%;
        background:linear-gradient(135deg,rgba(40,30,20,.78),rgba(16,12,9,.86)); border:1.5px solid rgba(255,214,150,.55); box-shadow:0 18px 50px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.18); }}
      .gk {{ font-weight:700; font-size:28px; letter-spacing:.24em; text-transform:uppercase; color:#f0c35b; }}
      .gt {{ font-family:"HSerif",serif; font-weight:700; font-size:50px; color:#fbf2e2; margin-top:6px; white-space:nowrap; }}
      .gbar {{ height:4px; margin-top:14px; border-radius:2px; background:linear-gradient(90deg,#f0c35b,#5fe0ff); }}
      .streak {{ position:absolute; left:0; top:-200px; width:420px; height:2400px; transform:rotate(18deg); opacity:0; background:linear-gradient(90deg,rgba(255,240,210,0),rgba(255,240,210,.55),rgba(255,240,210,0)); mix-blend-mode:screen; }}
      #flash {{ position:absolute; inset:0; background:#fff3dc; opacity:0; z-index:60; pointer-events:none; }}
      .ttl {{ position:absolute; left:80px; width:{W-160}px; top:190px; z-index:40; text-align:center; }}
      .k {{ display:flex; align-items:center; justify-content:center; gap:22px; font-weight:700; font-size:30px; letter-spacing:.28em; color:#f0c35b; text-transform:uppercase; margin-bottom:18px; text-shadow:0 2px 12px rgba(0,0,0,.8); }}
      .kl {{ display:inline-block; width:60px; height:2px; background:linear-gradient(90deg,rgba(240,195,91,0),#f0c35b); }}
      .kl:last-child {{ transform:scaleX(-1); }}
      .h {{ font-family:"HSerif",serif; font-weight:700; font-size:84px; line-height:1.08; text-wrap:balance; }}
      .wm {{ display:inline-block; overflow:hidden; vertical-align:bottom; padding:0 2px 10px; }}
      .w {{ display:inline-block; background:linear-gradient(180deg,#fffaf0 0%,#f6dfb0 55%,#e2b45a 100%); -webkit-background-clip:text; background-clip:text; color:transparent; filter:drop-shadow(0 4px 14px rgba(0,0,0,.65)); }}
      #scrim {{ position:absolute; left:0; top:0; width:{W}px; height:560px; z-index:30; background:linear-gradient(rgba(5,5,7,.72), rgba(5,5,7,0)); pointer-events:none; }}
      .rays {{ position:absolute; left:-460px; top:-700px; width:2000px; height:2600px; transform-origin:50% 40%; opacity:0;
        background:repeating-conic-gradient(from 0deg at 50% 40%, rgba(255,210,140,.10) 0deg 4deg, rgba(255,210,140,0) 4deg 14deg); -webkit-mask-image:radial-gradient(circle at 50% 40%, #000 0%, rgba(0,0,0,0) 60%); mix-blend-mode:screen; }}
      .podw {{ position:absolute; left:140px; top:1500px; width:800px; height:300px; perspective:900px; }}
      .ptilt {{ position:absolute; inset:0; transform:rotateX(76deg); transform-style:preserve-3d; }}
      .pring {{ position:absolute; left:50%; top:50%; border-radius:50%; }}
      .p1 {{ width:760px; height:760px; margin:-380px 0 0 -380px; border:5px solid rgba(240,195,91,.85); border-left-color:transparent; box-shadow:0 0 40px rgba(240,180,80,.5); }}
      .p2 {{ width:600px; height:600px; margin:-300px 0 0 -300px; border:3px dashed rgba(140,230,255,.75); }}
      .p3 {{ width:900px; height:900px; margin:-450px 0 0 -450px; background:radial-gradient(circle, rgba(240,195,91,.35) 0%, rgba(240,195,91,0) 60%); }}
      .pglow {{ position:absolute; left:100px; top:120px; width:600px; height:80px; border-radius:50%; background:radial-gradient(closest-side, rgba(255,210,140,.55), rgba(255,210,140,0)); }}
      .dstat {{ position:absolute; filter:drop-shadow(0 30px 40px rgba(0,0,0,.7)); }}
      .refl {{ position:absolute; transform:scaleY(-1); opacity:.22; -webkit-mask-image:linear-gradient(0deg, rgba(0,0,0,.9) 0%, rgba(0,0,0,0) 40%); }}
      #dust i {{ position:absolute; border-radius:50%; background:#ffd37a; box-shadow:0 0 10px 3px rgba(255,200,100,.6); opacity:0; }}
      #endi {{ position:absolute; left:80px; width:{W-160}px; top:200px; text-align:center; }}
      #endi .ek {{ font-weight:700; font-size:30px; letter-spacing:.3em; color:#f0c35b; text-transform:uppercase; }}
      #endi .en {{ font-family:"HSerif",serif; font-weight:700; font-size:104px; line-height:1.04; margin-top:22px; color:#fcebc6; text-shadow:0 0 30px rgba(240,190,90,.45), 0 4px 18px rgba(0,0,0,.7); }}
      #endi .er {{ width:240px; height:4px; margin:30px auto 0; background:linear-gradient(90deg,rgba(240,195,91,0),#f0c35b,rgba(240,195,91,0)); }}
      #endi .es {{ font-size:38px; color:#f1dfc0; margin-top:26px; }}
      #endi .eh {{ display:inline-block; margin-top:28px; font-weight:700; font-size:40px; color:#1a120a; padding:12px 40px; border-radius:999px; background:linear-gradient(180deg,#ffe0a0,#e6ad45); box-shadow:0 8px 30px rgba(240,180,70,.45); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
{chr(10).join(body)}
      <div id="scrim"></div>
      <div id="flash"></div>
      <audio id="music" class="clip" src="assets/audio/music.wav" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="10" data-volume="1"></audio>
      <audio id="sfx" class="clip" src="assets/audio/sfx.wav" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="11" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
      tl.set({{}}, {{}}, {TOTAL});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, V, 'index.html'), 'w').write(doc)
print('built', V, 'total', TOTAL, [(s['id'], s['at']) for s in P['shots']])
