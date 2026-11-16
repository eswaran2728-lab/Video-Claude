"""work23 builder: talking-head story reel. Reads vNN/edit-plan.json + vNN/timing-map.json, writes vNN/index.html.
Every segment is its own graded proxy (assets/video/<id>.mp4) in an untimed wrapper that carries punch-ins.
Graphics are plan-driven ('gfx'), all times on the output clock. usage: python3 build3.py v01"""
import json, os, sys, html
ROOT = os.path.dirname(os.path.abspath(__file__)); V = sys.argv[1]
P = json.load(open(os.path.join(ROOT, V, 'edit-plan.json')))
M = json.load(open(os.path.join(ROOT, V, 'timing-map.json')))
W, H, FPS = 1080, 1920, 30
segs = M['segments']; CUT = M['cut_end']; TOTAL = round(CUT + P['tail_card'], 3)
e = html.escape
body, js = [], []

# ---------- footage with punch-ins ----------
zoom = P.get('zoom', {})
for i, s in enumerate(segs):
    sid, at, du = s['id'], s['at'], s['dur']
    body.append(f'      <div id="w-{sid}" class="vw" style="z-index:{i+1}"><video id="v-{sid}" class="clip full" src="assets/video/{sid}.mp4" muted playsinline data-start="{at:.3f}" data-duration="{du:.3f}" data-media-start="0" data-track-index="1"></video></div>')
    z = zoom.get(sid, {})
    ox, oy = z.get('origin', [50, 34])
    s0 = z.get('scale', 1.0 if i % 2 == 0 else 1.14)
    js.append(f'      gsap.set("#w-{sid}", {{ scale: {s0}, transformOrigin: "{ox}% {oy}%" }});')
    js.append(f'      tl.to("#w-{sid}", {{ scale: {round(s0 * z.get("push", 1.035), 4)}, duration: {du:.3f}, ease: "none" }}, {at:.3f});')
    for k in z.get('steps', []):                        # in-segment zoom cuts: [t_out, scale]
        js.append(f'      tl.set("#w-{sid}", {{ scale: {k[1]} }}, {k[0]});')
        js.append(f'      tl.to("#w-{sid}", {{ scale: {round(k[1]*1.02,4)}, duration: {round(at+du-k[0],3)}, ease: "none" }}, {k[0]});')

# ---------- graphics ----------
for i, g in enumerate(P['gfx']):
    gid = f'g{i+1}'; st, en = g['t'][0], g['t'][1]; d = round(en - st, 3); k = g['kind']
    if k == 'hook':
        body.append(f'''      <div id="{gid}" class="clip hook" data-start="{st}" data-duration="{d}" data-track-index="3" data-track-kind="graphics">
        <div class="hk-k">{e(g['kicker'])}</div><div class="hk-h"><span class="hk-a">{e(g['a'])}</span><span id="{gid}b" class="hk-b">{e(g['b'])}</span></div></div>''')
        js.append(f'      tl.fromTo("#{gid} .hk-k", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, {st});')
        js.append(f'      tl.fromTo("#{gid} .hk-a", {{ opacity: 0, yPercent: 60 }}, {{ opacity: 1, yPercent: 0, duration: 0.4, ease: "power4.out" }}, {st+0.05});')
        js.append(f'      tl.fromTo("#{gid}b", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)" }}, {g["b_at"]});')
        js.append(f'      tl.to("#{gid} .hk-a", {{ opacity: 0, yPercent: -60, duration: 0.2, ease: "power2.in" }}, {g["b_at"]-0.05});')
    elif k == 'tag':          # top-left HUD tag (print attempt etc.)
        body.append(f'''      <div id="{gid}" class="clip tag {g.get('tone','')}" data-start="{st}" data-duration="{d}" data-track-index="4" data-track-kind="graphics"><span class="dot"></span><span class="tk">{e(g['kicker'])}</span><span class="tt">{e(g['text'])}</span></div>''')
        js.append(f'      tl.fromTo("#{gid}", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {st});')
        js.append(f'      tl.to("#{gid}", {{ opacity: 0, x: -30, duration: 0.2 }}, {en-0.22:.3f});')
    elif k == 'card':         # lower-third glass card
        body.append(f'''      <div id="{gid}" class="clip card" data-start="{st}" data-duration="{d}" data-track-index="5" data-track-kind="graphics"><div class="cbar"></div><div class="ck">{e(g['kicker'])}</div><div class="ct">{e(g['text'])}</div></div>''')
        js.append(f'      tl.fromTo("#{gid}", {{ opacity: 0, y: 40, rotationX: -30 }}, {{ opacity: 1, y: 0, rotationX: 0, duration: 0.45, ease: "power3.out" }}, {st});')
        js.append(f'      tl.fromTo("#{gid} .cbar", {{ scaleY: 0 }}, {{ scaleY: 1, transformOrigin: "50% 100%", duration: 0.35, ease: "power2.out" }}, {st+0.1});')
        js.append(f'      tl.to("#{gid}", {{ opacity: 0, y: 20, duration: 0.22 }}, {en-0.24:.3f});')
    elif k == 'chips':
        chips = ''.join(f'<span class="chip" style="--c:{c[1]}"><i></i>{e(c[0])}</span>' for c in g['items'])
        body.append(f'''      <div id="{gid}" class="clip chips" data-start="{st}" data-duration="{d}" data-track-index="6" data-track-kind="graphics">{chips}</div>''')
        js.append(f'      tl.fromTo("#{gid} .chip", {{ opacity: 0, y: 30, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, stagger: {g.get("stagger", 0.35)}, ease: "back.out(2)" }}, {st});')
        js.append(f'      tl.to("#{gid}", {{ opacity: 0, duration: 0.22 }}, {en-0.24:.3f});')
    elif k == 'big':          # center punch word
        body.append(f'''      <div id="{gid}" class="clip big" data-start="{st}" data-duration="{d}" data-track-index="7" data-track-kind="graphics"><div class="bw">{e(g['text'])}</div>{('<div class="bs">%s</div>' % e(g['sub'])) if g.get('sub') else ''}</div>''')
        js.append(f'      tl.fromTo("#{gid} .bw", {{ opacity: 0, scale: 2.2, rotation: -6 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(1.8)" }}, {st});')
        if g.get('sub'): js.append(f'      tl.fromTo("#{gid} .bs", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {st+0.25});')
        js.append(f'      tl.to("#{gid}", {{ opacity: 0, scale: 1.1, duration: 0.2 }}, {en-0.22:.3f});')
    elif k == 'callout':      # dot + leader + label on a fixed screen point
        ax, ay = g['at']; lx, ly = g['label']
        body.append(f'''      <div id="{gid}" class="clip call" data-start="{st}" data-duration="{d}" data-track-index="8" data-track-kind="graphics">
        <svg class="csvg" viewBox="0 0 1080 1920"><circle id="{gid}r" cx="{ax}" cy="{ay}" r="30"/><circle id="{gid}d" cx="{ax}" cy="{ay}" r="11"/><path id="{gid}l" pathLength="1" d="M {ax} {ay} L {lx} {ly}"/></svg>
        <div id="{gid}t" class="clab" style="left:{lx}px; top:{ly}px">{e(g['text'])}</div></div>''')
        js.append(f'      tl.fromTo("#{gid}d", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, {st});')
        js.append(f'      tl.fromTo("#{gid}r", {{ scale: 0.3, opacity: 1, transformOrigin: "50% 50%" }}, {{ scale: 1.8, opacity: 0, duration: 0.9, ease: "power2.out" }}, {st});')
        js.append(f'      tl.fromTo("#{gid}l", {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }}, {st+0.1});')
        js.append(f'      tl.fromTo("#{gid}t", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {st+0.35});')
        js.append(f'      tl.to("#{gid}", {{ opacity: 0, duration: 0.2 }}, {en-0.22:.3f});')
    elif k == 'slicer':       # settings panel with animated sliders (no invented values)
        rows = ''.join(f'<div class="srow"><span>{e(r)}</span><div class="strk"><div id="{gid}s{j}" class="sfil"></div><div id="{gid}k{j}" class="sknob"></div></div></div>' for j, r in enumerate(g['rows']))
        body.append(f'''      <div id="{gid}" class="clip slicer" data-start="{st}" data-duration="{d}" data-track-index="9" data-track-kind="graphics"><div class="sh"><span class="sdot"></span>{e(g['title'])}</div>{rows}<div id="{gid}ok" class="sok">{e(g['ok'])}</div></div>''')
        js.append(f'      tl.fromTo("#{gid}", {{ opacity: 0, y: 60, rotationY: -25 }}, {{ opacity: 1, y: 0, rotationY: 0, duration: 0.5, ease: "power3.out" }}, {st});')
        for j, (a, b) in enumerate(g['moves']):
            js.append(f'      tl.fromTo("#{gid}s{j}", {{ scaleX: {a} }}, {{ scaleX: {b}, transformOrigin: "0 50%", duration: 0.9, ease: "power2.inOut" }}, {st+0.5+j*0.25});')
            js.append(f'      tl.fromTo("#{gid}k{j}", {{ x: {a*420:.0f} }}, {{ x: {b*420:.0f}, duration: 0.9, ease: "power2.inOut" }}, {st+0.5+j*0.25});')
        js.append(f'      tl.fromTo("#{gid}ok", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }}, {st+0.5+len(g["moves"])*0.25+0.8:.2f});')
        js.append(f'      tl.to("#{gid}", {{ opacity: 0, y: 30, duration: 0.25 }}, {en-0.27:.3f});')
    if g.get('flash'):
        js.append(f'      tl.fromTo("#flash", {{ opacity: {g["flash"]} }}, {{ opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false }}, {st});')
    if g.get('shine'):
        js.append(f'      tl.fromTo("#shine", {{ x: -1300, opacity: 1 }}, {{ x: 1400, opacity: 1, duration: 0.6, ease: "power2.inOut", immediateRender: false }}, {st});')

for t in P.get('flashes', []):
    js.append(f'      tl.fromTo("#flash", {{ opacity: 0.5 }}, {{ opacity: 0, duration: 0.28, ease: "power2.out", immediateRender: false }}, {t});')

# ---------- end card ----------
EC = P['endcard']; es = CUT - 0.3
body.append(f'''      <div id="end" class="clip" data-start="{es:.3f}" data-duration="{TOTAL-es:.3f}" data-track-index="10" data-track-kind="graphics">
        <div id="endph"><img src="assets/img/photo.jpg" alt=""></div><div id="endsh"></div>
        <div id="sparks">{''.join(f'<i style="left:{(i*137.5)%1000+40:.0f}px; top:{(i*211.3)%1500+200:.0f}px; width:{3+i%3*2}px; height:{3+i%3*2}px"></i>' for i in range(24))}</div>
        <div id="endi"><div class="ek">{e(EC['kicker'])}</div><div class="en">{e(EC['name'])}</div><div class="er"></div><div class="es">{e(EC['line'])}</div><div><span class="eh">{e(EC['handle'])}</span></div></div>
      </div>''')
js.append(f'''      tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.45, ease: "power1.inOut" }}, {es});
      tl.fromTo("#endph", {{ scale: 1.12 }}, {{ scale: 1.0, duration: {TOTAL-es:.2f}, ease: "power2.out" }}, {es});
      tl.fromTo("#endi > *", {{ y: 36, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.55, stagger: 0.12, ease: "power3.out" }}, {es+0.35});
      tl.fromTo("#endi .er", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.inOut" }}, {es+0.55});
      tl.fromTo("#sparks i", {{ opacity: 0, y: 30 }}, {{ opacity: 0.85, y: -60, duration: {TOTAL-es-0.3:.2f}, stagger: {{ each: 0.05 }}, ease: "none" }}, {es+0.2});''')

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
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0b0907; }}
      #root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; font-family:"HSans",sans-serif; background:#0b0907; }}
      .vw {{ position:absolute; inset:0; pointer-events:none; }}
      .full {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
      #vig {{ position:absolute; inset:0; z-index:40; pointer-events:none; background:radial-gradient(90% 70% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.38) 100%); }}
      #grad {{ position:absolute; left:0; bottom:0; width:{W}px; height:760px; z-index:41; pointer-events:none; background:linear-gradient(rgba(8,6,4,0), rgba(8,6,4,.62)); }}
      #flash {{ position:absolute; inset:0; z-index:90; background:#fff3dc; opacity:0; pointer-events:none; }}
      #shine {{ position:absolute; left:0; top:-300px; width:520px; height:2600px; z-index:89; transform:rotate(16deg); opacity:0; pointer-events:none; mix-blend-mode:screen;
        background:linear-gradient(90deg, rgba(255,226,160,0), rgba(255,226,160,.45), rgba(255,226,160,0)); }}
      .hook {{ position:absolute; left:0; width:{W}px; top:0; padding:150px 70px 120px; z-index:60; text-align:center; background:linear-gradient(rgba(8,6,4,.85), rgba(8,6,4,.55) 60%, rgba(8,6,4,0)); }}
      .hk-k {{ font-weight:700; font-size:30px; letter-spacing:.3em; color:#f0c35b; text-transform:uppercase; text-shadow:0 2px 12px rgba(0,0,0,.8); }}
      .hk-h {{ position:relative; display:grid; place-items:center; margin-top:16px; font-family:"HSerif",serif; font-weight:700; line-height:1.04; }}
      .hk-a, .hk-b {{ grid-area:1/1; }}
      .hk-a {{ font-size:84px; color:#ffffff; text-shadow:0 6px 30px rgba(0,0,0,.75); }}
      .hk-b {{ font-size:110px; background:linear-gradient(180deg,#fff6dc,#f3cf7c 55%,#c98d2c); -webkit-background-clip:text; background-clip:text; color:transparent; filter:drop-shadow(0 6px 24px rgba(0,0,0,.7)); }}
      .tag {{ position:absolute; left:70px; top:250px; z-index:61; display:flex; align-items:center; gap:16px; padding:16px 28px; border-radius:16px;
        background:rgba(12,14,18,.72); border:1.5px solid rgba(140,230,255,.55); box-shadow:0 10px 36px rgba(0,0,0,.5); }}
      .tag .dot {{ width:16px; height:16px; border-radius:50%; background:#5fe0ff; box-shadow:0 0 12px #5fe0ff; }}
      .tag.gold {{ border-color:rgba(240,195,91,.7); }} .tag.gold .dot {{ background:#f0c35b; box-shadow:0 0 12px #f0c35b; }}
      .tag .tk {{ font-weight:700; font-size:28px; letter-spacing:.2em; color:#8fe9ff; text-transform:uppercase; }}
      .tag.gold .tk {{ color:#f0c35b; }}
      .tag .tt {{ font-family:"HSerif",serif; font-weight:700; font-size:44px; color:#fbf3e3; }}
      .card {{ position:absolute; left:70px; top:1430px; z-index:62; padding:24px 36px 26px 44px; border-radius:22px; max-width:900px; transform-origin:50% 100%;
        background:linear-gradient(135deg, rgba(36,27,18,.86), rgba(14,11,8,.9)); border:1.5px solid rgba(255,214,150,.5); box-shadow:0 20px 60px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.15); }}
      .cbar {{ position:absolute; left:0; top:18px; bottom:18px; width:8px; border-radius:4px; background:linear-gradient(#ffe0a0,#d99a3a); }}
      .ck {{ font-weight:700; font-size:28px; letter-spacing:.22em; color:#f0c35b; text-transform:uppercase; }}
      .ct {{ font-family:"HSerif",serif; font-weight:700; font-size:64px; color:#fbf3e3; line-height:1.08; margin-top:8px; }}
      .chips {{ position:absolute; left:70px; right:70px; top:1680px; z-index:63; display:flex; flex-wrap:wrap; gap:18px; }}
      .chip {{ display:inline-flex; align-items:center; gap:14px; padding:14px 28px; border-radius:999px; font-weight:700; font-size:44px; color:#fbf3e3;
        background:rgba(14,11,8,.8); border:1.5px solid rgba(255,255,255,.25); box-shadow:0 10px 30px rgba(0,0,0,.5); }}
      .chip i {{ width:34px; height:34px; border-radius:50%; background:var(--c); box-shadow:inset 0 -6px 10px rgba(0,0,0,.35), inset 0 6px 10px rgba(255,255,255,.4), 0 0 14px var(--c); }}
      .big {{ position:absolute; left:0; width:{W}px; top:1180px; z-index:70; text-align:center; }}
      .bw {{ display:inline-block; font-family:"HSerif",serif; font-weight:700; font-size:150px; line-height:1; color:#fff; padding:10px 40px 24px; border-radius:30px;
        background:linear-gradient(180deg, rgba(240,195,91,.95), rgba(196,128,36,.95)); color:#1a1006; box-shadow:0 24px 70px rgba(0,0,0,.6); }}
      .bs {{ font-weight:700; font-size:40px; color:#fbf3e3; margin-top:18px; text-shadow:0 3px 14px rgba(0,0,0,.85); }}
      .call {{ position:absolute; inset:0; z-index:64; }}
      .csvg {{ position:absolute; inset:0; width:{W}px; height:{H}px; overflow:visible; }}
      .csvg circle:first-child {{ fill:none; stroke:#ffe1a0; stroke-width:4; }}
      .csvg circle:nth-child(2) {{ fill:#ffd37a; stroke:#1a120a; stroke-width:4; }}
      .csvg path {{ fill:none; stroke:#ffe1a0; stroke-width:5; stroke-dasharray:1; filter:drop-shadow(0 2px 6px rgba(0,0,0,.7)); }}
      .clab {{ position:absolute; transform:translate(-50%,-110%); white-space:nowrap; padding:16px 30px; border-radius:18px; font-family:"HSerif",serif; font-weight:700; font-size:48px; color:#1a1006;
        background:linear-gradient(180deg,#ffe6ad,#f0c35b); box-shadow:0 14px 40px rgba(0,0,0,.55); }}
      .slicer {{ position:absolute; left:110px; width:860px; top:1180px; z-index:65; padding:28px 34px; border-radius:24px; transform-origin:0 50%;
        background:linear-gradient(160deg, rgba(20,24,30,.9), rgba(10,12,16,.92)); border:1.5px solid rgba(140,230,255,.45); box-shadow:0 24px 70px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.12); }}
      .sh {{ display:flex; align-items:center; gap:14px; font-weight:700; font-size:30px; letter-spacing:.2em; text-transform:uppercase; color:#8fe9ff; margin-bottom:18px; }}
      .sdot {{ width:14px; height:14px; border-radius:50%; background:#5fe0ff; box-shadow:0 0 10px #5fe0ff; }}
      .srow {{ display:flex; align-items:center; justify-content:space-between; gap:24px; padding:12px 0; font-size:34px; color:#e9eef5; }}
      .strk {{ position:relative; width:440px; height:12px; border-radius:6px; background:rgba(255,255,255,.12); }}
      .sfil {{ position:absolute; left:0; top:0; width:420px; height:12px; border-radius:6px; background:linear-gradient(90deg,#5fe0ff,#f0c35b); }}
      .sknob {{ position:absolute; left:-12px; top:-10px; width:32px; height:32px; border-radius:50%; background:#fff; box-shadow:0 0 0 4px rgba(95,224,255,.5), 0 4px 12px rgba(0,0,0,.5); }}
      .sok {{ margin-top:18px; display:inline-block; font-weight:700; font-size:34px; color:#0b1a10; background:#7ff0a8; padding:10px 26px; border-radius:999px; }}
      #end {{ position:absolute; inset:0; z-index:95; overflow:hidden; background:#0b0907; }}
      #endph {{ position:absolute; inset:0; }} #endph img {{ width:{W}px; height:{H}px; object-fit:cover; }}
      #endsh {{ position:absolute; inset:0; background:linear-gradient(rgba(10,8,6,.86) 0%, rgba(10,8,6,.35) 38%, rgba(10,8,6,.15) 60%, rgba(10,8,6,.55) 100%); }}
      #sparks i {{ position:absolute; border-radius:50%; background:#ffd37a; box-shadow:0 0 10px 3px rgba(255,200,100,.6); opacity:0; }}
      #endi {{ position:absolute; left:80px; width:{W-160}px; top:170px; text-align:center; }}
      #endi .ek {{ font-weight:700; font-size:30px; letter-spacing:.3em; color:#f0c35b; text-transform:uppercase; }}
      #endi .en {{ font-family:"HSerif",serif; font-weight:700; font-size:104px; line-height:1.04; margin-top:20px; color:#fcebc6; text-shadow:0 0 30px rgba(240,190,90,.45), 0 4px 18px rgba(0,0,0,.7); }}
      #endi .er {{ width:240px; height:4px; margin:28px auto 0; background:linear-gradient(90deg,rgba(240,195,91,0),#f0c35b,rgba(240,195,91,0)); }}
      #endi .es {{ font-size:38px; color:#f1dfc0; margin-top:24px; }}
      #endi .eh {{ display:inline-block; margin-top:26px; font-weight:700; font-size:40px; color:#1a120a; padding:12px 40px; border-radius:999px; background:linear-gradient(180deg,#ffe0a0,#e6ad45); box-shadow:0 8px 30px rgba(240,180,70,.45); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
{chr(10).join(body[:len(segs)])}
      <div id="vig"></div><div id="grad"></div>
{chr(10).join(body[len(segs):])}
      <div id="shine"></div><div id="flash"></div>
      <audio id="voice" class="clip" src="assets/audio/voice.wav" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="12" data-volume="1"></audio>
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
print('built', V, 'total', TOTAL)
