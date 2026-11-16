"""Deepavali stage reel: builds the HyperFrames project from edit-plan.json.
Usage: python3 build.py v01    (then: python3 audio.py v01 ; grade is applied by build)
All times in seconds. `in` = source time in the clip, `at` = output time (computed)."""
import json, os, sys, html, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
V = sys.argv[1] if len(sys.argv) > 1 else 'v01'
P = json.load(open(os.path.join(ROOT, V, 'edit-plan.json')))
W, H, FPS = 1080, 1920, 30
PY, PS = P['panel']['top'], P['panel']['size']          # square footage panel
SRC_W, SRC_H = 848, 478
K = PS / SRC_H                                           # source px -> panel px
VW = SRC_W * K

t = 0.0
for s in P['shots']:
    s['at'] = round(t, 3); t = round(t + s['dur'], 3)
TOTAL = P['total']
json.dump({'shots': [{k: s[k] for k in ('id', 'clip', 'in', 'dur', 'at', 'why')} for s in P['shots']], 'total': TOTAL},
          open(os.path.join(ROOT, V, 'timing-map.json'), 'w'), indent=1)

def tx(cx, z=1.0):
    """wrapper x so that source column cx sits at panel centre (clamped to the picture)."""
    x = PS / 2 - cx * K
    return round(max(PS - VW, min(0, x)), 1)

e = html.escape
vids, tw = [], []
for i, s in enumerate(P['shots']):
    sid = s['id']
    vids.append(f'''        <div id="w-{sid}" class="sw" style="z-index:{i+1}"><video id="v-{sid}" class="clip" src="assets/video/{s['id'] if P.get('per_shot_proxies') else s['clip']}.mp4" muted playsinline data-start="{s['at']:.3f}" data-duration="{s['dur']:.3f}" data-media-start="{0 if P.get('per_shot_proxies') else s['in']:.3f}" data-track-index="1"></video></div>''')
    kf = s['move']                      # [[t_rel, cx, zoom, ease?], ...]
    bz = 1.0 if s.get('wide') else P.get('base_zoom', 1.0)
    kf = [[k[0], k[1], round(k[2]*bz, 3)] + k[3:] for k in kf]
    cx0, z0 = kf[0][1], kf[0][2]
    tw.append(f'''      gsap.set("#w-{sid}", {{ x: {tx(cx0)}, scale: {z0}, transformOrigin: "{round(cx0*K,1)}px 36%" }});''')
    for a, b in zip(kf, kf[1:]):
        ease = b[3] if len(b) > 3 else 'sine.inOut'
        tw.append(f'''      tl.to("#w-{sid}", {{ x: {tx(b[1])}, scale: {b[2]}, duration: {round(b[0]-a[0],3)}, ease: "{ease}" }}, {round(s['at']+a[0],3)});''')

txt, ttw = [], []
for i, c in enumerate(P['text']):
    cid = f"t{i+1}"
    dur = round(c['end'] - c['start'], 3)
    lines = ''.join(f'<div class="{l[0]}">{e(l[1])}</div>' for l in c['lines'])
    txt.append(f'''      <div id="{cid}" class="clip tx {c['zone']}" data-start="{c['start']:.3f}" data-duration="{dur:.3f}" data-track-index="{3 if c['zone']=='top' else 4}" data-track-kind="graphics"><div id="{cid}i" class="txi">{lines}</div></div>''')
    ttw.append(f'''      tl.fromTo("#{cid}i > div", {{ y: 34, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.42, stagger: 0.09, ease: "power3.out" }}, {c['start']:.3f});''')
    if c.get('out', True):
        ttw.append(f'''      tl.to("#{cid}i", {{ opacity: 0, y: -14, duration: 0.22, ease: "power2.in" }}, {c['end']-0.24:.3f});''')

fl = ''.join(f'''      tl.fromTo("#flash", {{ opacity: 0.55 }}, {{ opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false }}, {x});\n''' for x in P['flashes'])
EC = P['endcard']
HD = P.get('header')
chips = ''.join(f'<span id="chip{i+1}" class="chip">{e(c["label"])}</span>' for i, c in enumerate(P['chips']))
chtw = ''
for i, c in enumerate(P['chips']):
    chtw += f'''      tl.to("#chip{i+1}", {{ color: "#1a0d08", backgroundColor: "#f0c35b", duration: 0.25 }}, {c['start']});\n'''
    chtw += f'''      tl.to("#chip{i+1}", {{ color: "#f0c35b", backgroundColor: "rgba(240,195,91,0)", duration: 0.25 }}, {c['end']});\n'''

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
      @font-face {{ font-family:"HTamil"; font-weight:700; src:url("assets/fonts/serif-tamil-700.woff2") format("woff2"); }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#120706; }}
      #root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; font-family:"HSans",sans-serif;
        background: radial-gradient(120% 60% at 50% 0%, #5a1210 0%, #2a0b0a 45%, #120706 100%); }}
      #glow {{ position:absolute; left:0; top:{PY+PS-40}px; width:{W}px; height:520px; background: radial-gradient(70% 60% at 50% 0%, rgba(240,160,60,.22), rgba(240,160,60,0) 70%); }}
      #panel {{ position:absolute; left:0; top:{PY}px; width:{W}px; height:{PS}px; overflow:hidden; background:#000; z-index:5; }}
      .sw {{ position:absolute; left:0; top:0; width:{VW:.1f}px; height:{PS}px; }}
      .sw video {{ position:absolute; left:0; top:0; width:{VW:.1f}px; height:{PS}px; object-fit:cover; }}
      #flash {{ position:absolute; inset:0; background:#fff3d6; opacity:0; z-index:60; pointer-events:none; }}
      .rule {{ position:absolute; left:0; width:{W}px; height:4px; background:linear-gradient(90deg, rgba(240,195,91,0), #f0c35b 18%, #f7e3a6 50%, #f0c35b 82%, rgba(240,195,91,0)); z-index:6; }}
      .tx {{ position:absolute; left:84px; width:{W-168}px; z-index:20; text-align:center; }}
      .tx.top {{ top:150px; height:{PY-150-24}px; display:flex; align-items:flex-end; justify-content:center; }}
      .tx.bot {{ top:{PY+PS+44}px; height:150px; display:flex; align-items:flex-start; justify-content:center; }}
      .kick {{ font-weight:700; font-size:30px; letter-spacing:.2em; color:#f0c35b; text-transform:uppercase; margin-bottom:14px; }}
      .big {{ font-family:"HSerif",serif; font-weight:700; font-size:78px; line-height:1.04; color:#fff6e6; }}
      .mid {{ font-family:"HSerif",serif; font-weight:700; font-size:66px; line-height:1.06; color:#fff6e6; }}
      .cap {{ font-weight:700; font-size:46px; line-height:1.18; color:#fff6e6; }}
      .sub {{ font-weight:400; font-size:36px; line-height:1.25; color:#f3d9a4; margin-top:10px; }}
      #chips {{ position:absolute; left:0; width:{W}px; top:{PY+PS+P.get('chips_gap',214)}px; z-index:20; display:flex; justify-content:center; gap:18px; }}
      .chip {{ font-weight:700; font-size:28px; letter-spacing:.12em; text-transform:uppercase; color:#f0c35b; border:2px solid #f0c35b; border-radius:999px; padding:10px 26px; background-color:rgba(240,195,91,0); }}
      #hdr {{ position:absolute; left:0; top:0; width:{W}px; height:{PY}px; z-index:90; pointer-events:none; }}
      #hdri {{ position:absolute; left:0; width:{W}px; top:{HD.get('top',56)}px; height:{HD.get('logo',150)}px; display:flex; align-items:center; justify-content:center; gap:22px; }}
      #hdri img {{ height:{HD.get('logo',150)}px; width:auto; }}
      #hdri .l1 {{ font-weight:700; font-size:38px; line-height:1.1; letter-spacing:.07em; color:#fff6e6; text-transform:uppercase; }}
      #hdri .l2 {{ font-weight:700; font-size:30px; line-height:1.2; letter-spacing:.32em; color:#f0c35b; text-transform:uppercase; margin-top:6px; }}
      #end {{ position:absolute; inset:0; z-index:80; background: radial-gradient(110% 70% at 50% 38%, #6a1512 0%, #2a0b0a 55%, #120706 100%); }}
      #endi {{ position:absolute; left:108px; width:{W-216}px; top:560px; text-align:center; }}
      #end .ta {{ font-family:"HTamil",serif; font-weight:700; font-size:92px; line-height:1.3; color:#f7d77a; }}
      #end .en {{ font-family:"HSerif",serif; font-weight:700; font-size:64px; line-height:1.12; color:#fff6e6; margin-top:44px; }}
      #end .dt {{ font-weight:700; font-size:34px; letter-spacing:.14em; text-transform:uppercase; color:#f0c35b; margin-top:44px; }}
      #end .ln {{ width:220px; height:4px; background:#f0c35b; margin:40px auto 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
      <div id="glow"></div>
      <div class="rule" style="top:{PY-4}px"></div>
      <div class="rule" style="top:{PY+PS}px"></div>
      <div id="panel">
{chr(10).join(vids)}
        <div id="flash"></div>
      </div>
{chr(10).join(txt)}
      <div id="chipw" class="clip" data-start="{P['chips'][0]['start']-0.4:.3f}" data-duration="{EC['start']-P['chips'][0]['start']+0.4:.3f}" data-track-index="5" data-track-kind="graphics"><div id="chips">{chips}</div></div>
      <div id="end" class="clip" data-start="{EC['start']:.3f}" data-duration="{TOTAL-EC['start']:.3f}" data-track-index="6" data-track-kind="graphics">
        <div id="endi">
          <div class="ta">{e(EC['tamil'])}</div>
          <div class="ln"></div>
          <div class="en">{e(EC['title'])}</div>
          <div class="dt">{e(EC['date'])}</div>
        </div>
      </div>
{('<div id="hdr" class="clip" data-start="0" data-duration="%.3f" data-track-index="7" data-track-kind="graphics"><div id="hdri"><img src="%s" alt=""><div><div class="l1">%s</div><div class="l2">%s</div></div></div></div>' % (TOTAL, HD['logo_src'], e(HD['line1']), e(HD['line2']))) if HD else ''}
      <audio id="bed" class="clip" src="assets/audio/bed.wav" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="10" data-volume="1"></audio>
      <audio id="sfx" class="clip" src="assets/audio/sfx.wav" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="11" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tw)}
{chr(10).join(ttw)}
{fl}{chtw}      tl.fromTo("#chips", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {P['chips'][0]['start']-0.4});
      tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.7, ease: "power2.inOut" }}, {EC['start']});
      tl.fromTo("#endi > div", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, stagger: 0.16, ease: "power3.out" }}, {EC['start']+0.45});
      tl.to("#endi", {{ scale: 1.03, duration: {TOTAL-EC['start']-0.5:.2f}, ease: "none" }}, {EC['start']+0.5});
      tl.set({{}}, {{}}, {TOTAL});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, V, 'index.html'), 'w').write(doc)
print('built', V, 'shots', len(P['shots']), 'total', TOTAL)

g = P.get('grading')
if g and '--no-grade' not in sys.argv:
    sel = ', '.join(f"#v-{s['id']}" for s in P['shots'])
    r = subprocess.run(['npx', 'hyperframes', 'media-treatment', '--selector', sel, '--grading', json.dumps(g), '--apply', '--json'],
                       cwd=os.path.join(ROOT, V), capture_output=True, text=True)
    print('grade:', r.stdout[-200:].strip() or r.stderr[-300:])
