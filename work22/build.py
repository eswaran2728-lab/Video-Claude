"""Statue reel: builds vNN/index.html from vNN/edit-plan.json, then applies the grade.
usage: python3 build.py v01 [--no-grade]
Still shots show assets/img/hero.jpg (2160x3840 frame at source 0.167 s) zoomed about an anchor point;
anchor = source px, screen = output px where that anchor sits. Times are output seconds."""
import json, os, sys, html, subprocess, math

ROOT = os.path.dirname(os.path.abspath(__file__))
V = sys.argv[1] if len(sys.argv) > 1 else 'v01'
P = json.load(open(os.path.join(ROOT, V, 'edit-plan.json')))
W, H, FPS = 1080, 1920, 30
SW, SH = 2160, 3840
e = html.escape

t = 0.0
for s in P['shots']:
    s['at'] = round(t, 3); t = round(t + s['dur'], 3)
TOTAL = round(t, 3)
json.dump({'total': TOTAL, 'shots': [{k: s.get(k) for k in ('id', 'kind', 'src_time', 'at', 'dur', 'why')} for s in P['shots']]},
          open(os.path.join(ROOT, V, 'timing-map.json'), 'w'), indent=1)

def xy(anchor, screen, k):
    return round(screen[0] - anchor[0] * k, 2), round(screen[1] - anchor[1] * k, 2)

layers, js, grade_sel = [], [], []
for i, s in enumerate(P['shots']):
    sid, at, dur = s['id'], s['at'], s['dur']
    z = i + 1
    if s['kind'] == 'blank':
        layers.append(f'''      <div id="{sid}" class="clip shot" data-start="{at:.3f}" data-duration="{dur:.3f}" data-track-index="1" style="z-index:{z}"></div>''')
        continue
    if s['kind'] == 'video':
        layers.append(f'''      <div id="{sid}" class="vshot" style="z-index:{z}"><video id="v-{sid}" class="clip full" src="assets/video/{s['src']}" muted playsinline data-start="{at:.3f}" data-duration="{dur:.3f}" data-media-start="0" data-track-index="2"></video></div>''')
        grade_sel.append(f'#v-{sid}')
        continue
    k0, k1 = SW / s['cw0'] * 0.5 if False else W / s['cw0'], W / s['cw1']
    a, sc = s['anchor'], s.get('screen', [540, 960])
    x0, y0 = xy(a, sc, k0); x1, y1 = xy(a, sc, k1)
    colour = f'<div id="m-{sid}" class="mv"><img id="i-{sid}" class="still" src="assets/img/hero_graded.jpg" alt=""></div>'
    inner = colour
    grade_sel.append(f'#i-{sid}')
    if s.get('print'):
        inner = f'<div id="g-{sid}" class="greyw"><div id="gm-{sid}" class="mv"><img id="ig-{sid}" class="still" src="assets/img/hero_grey.jpg" alt=""><div class="layers"></div></div></div><div id="cw-{sid}" class="greyw" style="clip-path:polygon(0% 0%,0% 0%,0% 0%)">{colour}</div><div id="scan-{sid}" class="scan"><div id="noz-{sid}" class="noz"></div></div>'
        grade_sel.append(f'#ig-{sid}')
        js.append(f'      gsap.set("#gm-{sid}", {{ x: {x0}, y: {y0}, scale: {k0}, transformOrigin: "0 0" }});')
        js.append(f'      tl.to("#gm-{sid}", {{ x: {x1}, y: {y1}, scale: {k1}, duration: {dur}, ease: "none" }}, {at});')
        pr = s['print']; ps, pe = at + pr['scan'][0], at + pr['scan'][1]
        js.append(f'      tl.fromTo("#g-{sid}", {{ clipPath: "inset({pr["from"]}% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: {pe-ps:.3f}, ease: "none", immediateRender: true }}, {ps:.3f});')
        js.append(f'      tl.fromTo("#scan-{sid}", {{ y: {round(H*pr["from"]/100)} }}, {{ y: 0, duration: {pe-ps:.3f}, ease: "none", immediateRender: true }}, {ps:.3f});')
        js.append(f'      tl.fromTo("#noz-{sid}", {{ x: 60 }}, {{ x: {W-120}, duration: 0.32, ease: "sine.inOut", yoyo: true, repeat: {max(1, int((pe-ps)/0.32))} }}, {ps:.3f});')
        js.append(f'      tl.to("#scan-{sid}", {{ opacity: 0, duration: 0.25 }}, {pe:.3f});')
        # brush reveal of the painted (colour) frame over the grey one
        br = pr['paint']; bs, be = at + br[0], at + br[1]
        js.append(f'''      (function(){{ const el = document.querySelector("#cw-{sid}"); const st = {{ p: 0 }};
        const pts = n => {{ const o = []; for (let j = 0; j <= 24; j++) {{ const yy = j / 24 * 100; o.push([n - yy * 0.55 + Math.sin(j * 2.3) * 2.2 + Math.sin(j * 5.1) * 1.1, yy]); }} return o; }};
        tl.to(st, {{ p: 1, duration: {be-bs:.3f}, ease: "power1.inOut", onUpdate: () => {{ const n = -10 + st.p * 175; const e = pts(n);
          el.style.clipPath = st.p <= 0 ? "polygon(0% 0%,0% 0%,0% 0%)" : "polygon(" + e.map(q => q[0].toFixed(2) + "% " + q[1] + "%").join(",") + ",-5% 100%,-5% 0%)"; }} }}, {bs:.3f});
      }})();''')
        js.append(f'      tl.fromTo("#brush-{sid}", {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: {be-bs:.3f}, ease: "power1.inOut" }}, {bs:.3f});')
        js.append(f'      tl.to("#brushw-{sid}", {{ opacity: 0, duration: 0.3 }}, {be+0.05:.3f});')
        inner += f'<svg id="brushw-{sid}" class="brushw" viewBox="0 0 1080 1920"><path id="brush-{sid}" pathLength="1" d="M -60 -40 C 260 300, 420 700, 640 1000 S 980 1600, 1180 2000" /></svg>'
    layers.append(f'''      <div id="{sid}" class="clip shot" data-start="{at:.3f}" data-duration="{dur:.3f}" data-track-index="1" style="z-index:{z}">{inner}</div>''')
    js.append(f'      gsap.set("#m-{sid}", {{ x: {x0}, y: {y0}, scale: {k0}, transformOrigin: "0 0" }});')
    js.append(f'      tl.to("#m-{sid}", {{ x: {x1}, y: {y1}, scale: {k1}, duration: {dur}, ease: "{s.get("ease", "none")}" }}, {at});')
    if s.get('flash_in'):
        js.append(f'      tl.fromTo("#flash", {{ opacity: 0.5 }}, {{ opacity: 0, duration: 0.28, ease: "power2.out", immediateRender: false }}, {at});')

# callouts (anchor sits still on screen because each detail zooms about it)
cl = []
for i, c in enumerate(P['callouts']):
    cid = f'c{i+1}'; s = next(x for x in P['shots'] if x['id'] == c['shot'])
    ax, ay = s.get('screen', [540, 960]); lx, ly = c['label_at']
    st, du = s['at'] + 0.15, s['dur'] - 0.15
    cl.append(f'''      <div id="{cid}" class="clip call" data-start="{st:.3f}" data-duration="{du:.3f}" data-track-index="4" data-track-kind="graphics">
        <svg class="callsvg" viewBox="0 0 1080 1920"><circle id="{cid}r" cx="{ax}" cy="{ay}" r="26" /><circle id="{cid}d" cx="{ax}" cy="{ay}" r="9" /><path id="{cid}l" pathLength="1" d="M {ax} {ay} L {lx} {ly}" /></svg>
        <div id="{cid}t" class="lab" style="left:{lx + (16 if c['side']=='r' else -16)}px; top:{ly}px; transform:translate({'0' if c['side']=='r' else '-100%'},-50%)"><span class="lk">{e(c['kicker'])}</span><span class="lt">{e(c['text'])}</span></div>
      </div>''')
    js.append(f'      tl.fromTo("#{cid}d", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.25, ease: "back.out(3)" }}, {st:.3f});')
    js.append(f'      tl.fromTo("#{cid}r", {{ scale: 0.4, opacity: 0.9, transformOrigin: "50% 50%" }}, {{ scale: 1.6, opacity: 0, duration: 0.7, ease: "power2.out" }}, {st:.3f});')
    js.append(f'      tl.fromTo("#{cid}l", {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }}, {st+0.1:.3f});')
    js.append(f'      tl.fromTo("#{cid}t", {{ opacity: 0, x: {-24 if c["side"]=="r" else 24} }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {st+0.3:.3f});')
    js.append(f'      tl.to("#{cid}", {{ opacity: 0, duration: 0.18 }}, {st+du-0.2:.3f});')

tx = []
for i, c in enumerate(P['titles']):
    tid = f't{i+1}'
    lines = ''.join(f'<div class="{a}">{e(b)}</div>' for a, b in c['lines'])
    tx.append(f'      <div id="{tid}" class="clip ttl" data-start="{c["start"]:.3f}" data-duration="{c["end"]-c["start"]:.3f}" data-track-index="3" data-track-kind="graphics"><div id="{tid}i" class="ttli">{lines}</div></div>')
    js.append(f'      tl.fromTo("#{tid}i > div", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, stagger: 0.08, ease: "power3.out", immediateRender: {"true" if c["start"] == 0 else "false"} }}, {max(0, c["start"]-(0 if c["start"]==0 else 0)):.3f});' if c['start'] > 0 else f'      gsap.set("#{tid}i > div", {{ opacity: 1 }});')
    if c.get('hl'):
        js.append(f'      tl.fromTo("#{tid}i .hl", {{ backgroundSize: "0% 100%" }}, {{ backgroundSize: "100% 100%", duration: 0.45, ease: "power2.out" }}, {c["start"]+0.35:.3f});')
    js.append(f'      tl.to("#{tid}i", {{ opacity: 0, y: -12, duration: 0.2, ease: "power2.in" }}, {c["end"]-0.22:.3f});')

EC = P['endcard']; es = next(x['at'] for x in P['shots'] if x['id'] == EC['shot'])
spark = ''.join(f'<i style="left:{(i*137.5)%1000+40:.0f}px; top:{(i*263.1)%1500+200:.0f}px; width:{4+i%3*3}px; height:{4+i%3*3}px"></i>' for i in range(22))
js.append(f'      tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, {es});')
js.append(f'      tl.fromTo("#endbg", {{ scale: 1.18 }}, {{ scale: 1.04, duration: {TOTAL-es:.2f}, ease: "power2.out" }}, {es});')
js.append(f'      tl.fromTo("#endi > *", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.55, stagger: 0.14, ease: "power3.out" }}, {es+0.25});')
js.append(f'      tl.fromTo("#endrule", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.inOut" }}, {es+0.45});')
js.append(f'      tl.fromTo("#sparks i", {{ opacity: 0, scale: 0 }}, {{ opacity: 0.9, scale: 1, duration: 0.5, stagger: {{ each: 0.06, from: "random" }}, ease: "power2.out" }}, {es+0.3});')
js.append(f'      tl.to("#sparks i", {{ y: -60, duration: {TOTAL-es-0.3:.2f}, ease: "none", stagger: {{ each: 0.02 }} }}, {es+0.3});')

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
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#16120f; }}
      #root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; font-family:"HSans",sans-serif; background:#16120f; }}
      .shot {{ position:absolute; inset:0; overflow:hidden; background:#16120f; }}
      .vshot {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; }}
      .mv {{ position:absolute; left:0; top:0; width:{SW}px; height:{SH}px; }}
      .still {{ position:absolute; left:0; top:0; width:{SW}px; height:{SH}px; }}
      .full {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
      .greyw {{ position:absolute; inset:0; overflow:hidden; }}
      .layers {{ position:absolute; inset:0; background:repeating-linear-gradient(0deg, rgba(255,255,255,.10) 0 2px, rgba(0,0,0,.10) 2px 5px); }}
      .scan {{ position:absolute; left:0; top:0; width:{W}px; height:6px; background:#ffe9b0; box-shadow:0 0 18px 6px rgba(255,200,90,.75), 0 0 60px 18px rgba(255,170,60,.35); z-index:5; }}
      .noz {{ position:absolute; top:-46px; left:0; width:60px; height:46px; background:linear-gradient(#3a3a3a,#1d1d1d); clip-path:polygon(0 0,100% 0,100% 60%,62% 60%,50% 100%,38% 60%,0 60%); }}
      .brushw {{ position:absolute; inset:0; width:{W}px; height:{H}px; z-index:6; }}
      .brushw path {{ fill:none; stroke:#e9b54a; stroke-width:16; stroke-linecap:round; stroke-dasharray:1; opacity:.9; filter:drop-shadow(0 0 10px rgba(255,190,80,.7)); }}
      #vig {{ position:absolute; inset:0; z-index:39; pointer-events:none; background:radial-gradient(85% 70% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,.32) 100%); }}
      #scrim {{ position:absolute; left:0; top:0; width:{W}px; height:640px; z-index:40; background:linear-gradient(rgba(10,8,6,.78), rgba(10,8,6,.45) 55%, rgba(10,8,6,0)); pointer-events:none; }}
      #scrimb {{ position:absolute; left:0; bottom:0; width:{W}px; height:420px; z-index:40; background:linear-gradient(rgba(10,8,6,0), rgba(10,8,6,.55)); pointer-events:none; }}
      .ttl {{ position:absolute; left:90px; width:{W-180}px; top:200px; z-index:50; text-align:center; }}
      .k {{ font-weight:700; font-size:30px; letter-spacing:.24em; color:#e9b54a; text-transform:uppercase; margin-bottom:16px; }}
      .h {{ font-family:"HSerif",serif; font-weight:700; font-size:84px; line-height:1.05; color:#f8efe0; text-shadow:0 4px 24px rgba(0,0,0,.55); }}
      .hl {{ display:inline-block; line-height:1.3; margin-top:6px; background-image:linear-gradient(#e9b54a,#e9b54a); background-repeat:no-repeat; background-position:0 88%; background-size:0% 100%; padding:0 8px; color:#1a120a; text-shadow:none; }}
      .call {{ position:absolute; inset:0; z-index:45; }}
      .callsvg {{ position:absolute; inset:0; width:{W}px; height:{H}px; overflow:visible; }}
      .callsvg circle:first-child {{ fill:none; stroke:#ffe1a0; stroke-width:4; }}
      .callsvg circle:nth-child(2) {{ fill:#ffd37a; stroke:#1a120a; stroke-width:3; }}
      .callsvg path {{ fill:none; stroke:#ffe1a0; stroke-width:4; stroke-dasharray:1; filter:drop-shadow(0 2px 6px rgba(0,0,0,.6)); }}
      .lab {{ position:absolute; display:flex; flex-direction:column; gap:4px; padding:16px 26px; border-radius:18px; background:rgba(22,16,11,.82); border:2px solid rgba(233,181,74,.85); white-space:nowrap; }}
      .lk {{ font-weight:700; font-size:28px; letter-spacing:.22em; color:#e9b54a; text-transform:uppercase; }}
      .lt {{ font-family:"HSerif",serif; font-weight:700; font-size:44px; color:#f8efe0; }}
      #flash {{ position:absolute; inset:0; background:#fff3dc; opacity:0; z-index:60; pointer-events:none; }}
      #end {{ position:absolute; inset:0; z-index:70; overflow:hidden; background:#120d09; }}
      #endbg {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; }}
      #endbg img {{ width:{W}px; height:{H}px; }}
      #endshade {{ position:absolute; inset:0; background:radial-gradient(80% 55% at 50% 45%, rgba(18,13,9,.35), rgba(18,13,9,.9)); }}
      #sparks i {{ position:absolute; border-radius:50%; background:#ffd37a; box-shadow:0 0 12px 3px rgba(255,200,100,.7); }}
      #endi {{ position:absolute; left:90px; width:{W-180}px; top:640px; text-align:center; }}
      #endi .ek {{ font-weight:700; font-size:30px; letter-spacing:.3em; color:#e9b54a; text-transform:uppercase; }}
      #endi .en {{ font-family:"HSerif",serif; font-weight:700; font-size:112px; line-height:1.02; color:#f8efe0; margin-top:26px; }}
      #endrule {{ width:260px; height:4px; background:#e9b54a; margin:40px auto 0; }}
      #endi .es {{ font-size:42px; line-height:1.3; color:#f1dfc0; margin-top:38px; }}
      #endi .eh {{ display:inline-block; margin-top:46px; font-weight:700; font-size:44px; color:#1a120a; background:#e9b54a; border-radius:999px; padding:16px 44px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
{chr(10).join(layers)}
      <div id="vig"></div><div id="scrim"></div><div id="scrimb"></div>
{chr(10).join(tx)}
{chr(10).join(cl)}
      <div id="flash"></div>
      <div id="end" class="clip" data-start="{es:.3f}" data-duration="{TOTAL-es:.3f}" data-track-index="5" data-track-kind="graphics">
        <div id="endbg"><img src="assets/img/hero_blur.jpg" alt=""></div><div id="endshade"></div>
        <div id="sparks">{spark}</div>
        <div id="endi">
          <div class="ek">{e(EC['kicker'])}</div>
          <div class="en">{e(EC['name'])}</div>
          <div id="endrule"></div>
          <div class="es">{'<br>'.join(e(x) for x in EC['lines'])}</div>
          <div><span class="eh">{e(EC['handle'])}</span></div>
        </div>
      </div>
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
P['_total'] = TOTAL
print('built', V, 'total', TOTAL, 'shots', [(s['id'], s['at']) for s in P['shots']])

g = P.get('grading')
if g and '--no-grade' not in sys.argv:
    r = subprocess.run(['npx', 'hyperframes', 'media-treatment', '--selector', ', '.join(grade_sel), '--grading', json.dumps(g), '--apply', '--json'],
                       cwd=os.path.join(ROOT, V), capture_output=True, text=True)
    print('grade ok' if '"changed": true' in r.stdout else ('grade:' + r.stdout[-300:] + r.stderr[-300:]))
