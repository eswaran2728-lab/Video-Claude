# Silambam masters introduction — HyperFrames composition, exactly 15.000 s (450 frames @ 30 fps), 1080x1920.
# Wording: content.json (only place to edit text). Cutouts: cutout.py. Temporary music: make_audio.py.
# Every element is a separate editable layer (SVG frames, text, portraits); all motion lives in one GSAP timeline.
#   0.00-1.00 logo + association   1-3, 3-5, 5-7, 7-9 masters   9-14 credits (static)   14-15 thanks + handle
import json, os, random
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
C = json.load(open("content.json"))
TOTAL, W, H = 15.0, 1080, 1920
RED, BRIGHT, DEEP, GOLD = "#e3121f", "#ff3a3a", "#7e0a12", "#d8b25a"
at = lambda t: round(t, 3)
js, init, html = [], [], []
A, I = js.append, init.append

# ---------------- layout per master (alternating sides) ----------------
SCN = [1.0, 3.0, 5.0, 7.0]
NAME_PX = {"Sri S Arumugam": 132, "Selvaraju": 150, "DATO A.SIVAKUMAR": 98, "Vijayasegaran": 132}
FIG_H = {"photo_d": 1170, "photo_c": 1000, "photo_b": 1180, "photo_a": 1150}     # rendered figure height (px)
FIG_BOTTOM = {"photo_d": 1850, "photo_c": 1720, "photo_b": 1830, "photo_a": 1880}  # figure bottom y (px)
side = ["L", "R", "L", "R"]
def hexagon(cx, cy, r, rot=0):
    import math
    pts = [(cx + r * math.cos(math.radians(rot + 90 + 60 * k)), cy - r * math.sin(math.radians(rot + 90 + 60 * k))) for k in range(6)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"

masters_html = []
for i, m in enumerate(C["masters"]):
    t0 = SCN[i]; L = side[i] == "L"
    im = Image.open(f"edit/assets/cut/{m['photo']}.png"); fh = FIG_H[m["photo"]]; fw = round(im.width * fh / im.height)
    cx = 600 if L else 480                                    # figure / frame centre x (opposite side to the name block)
    fx, fy = cx - fw // 2, FIG_BOTTOM[m["photo"]] - fh       # head starts below the name block; feet may run off the bottom edge
    hx, hy = cx, 1180
    svg = [f'<path class="slab" d="{hexagon(hx, hy, 455, 4 if L else -4)}"/>',
           f'<path class="f f1" pathLength="1" d="{hexagon(hx, hy, 540)}"/>',
           f'<path class="f f2" pathLength="1" d="{hexagon(hx, hy, 470, 8 if L else -8)}"/>',
           f'<path class="f f3" pathLength="1" d="{hexagon(hx, hy, 400, -6 if L else 6)}"/>']
    chev = "".join(f'<path class="chev" d="M{(140 if L else 860) + k * 34},{1640 + (k % 2) * 0} l18,16 l-18,16"/>' for k in range(4))
    sq = f'<rect class="sq" x="{120 if not L else 880}" y="860" width="46" height="46"/><rect class="sq s2" x="{170 if not L else 930}" y="1420" width="26" height="26"/>'
    align = "left" if L else "right"; tx = 90 if L else None
    pos = f"left:90px;" if L else "right:90px;"
    masters_html.append(f'''      <div id="m{i}" class="clip scene" data-start="{at(t0 - 0.02)}" data-duration="{at(2.04 if i < 3 else 2.04)}" data-track-index="2">
        <div class="sin" id="m{i}in">
          <div class="frames" id="fr{i}"><svg viewBox="0 0 1080 1920">{''.join(svg)}{chev}{sq}</svg></div>
          <img class="fig" id="fig{i}" src="assets/cut/{m['photo']}.png" alt="{m['rank']} {m['name']}" style="left:{fx}px;top:{fy}px;width:{fw}px;height:{fh}px" />
          <div class="nb {side[i]}" style="{pos}">
            <div class="idx"><b>0{i + 1}</b> / 04</div>
            <div class="mask"><div class="rank" id="rk{i}"><i></i>{m["rank"]}</div></div>
            <div class="mask"><div class="name" id="nm{i}" style="font-size:{NAME_PX.get(m['name'], 128)}px">{m["name"]}</div></div>
          </div>
        </div>
      </div>''')
    # ---- motion: frames draw, then turn slightly in depth; portrait rises behind a diagonal reveal and pushes in ----
    I(f'gsap.set("#fr{i} .f",{{strokeDasharray:1,strokeDashoffset:1}});')
    I(f'gsap.set("#fr{i}",{{transformPerspective:1400,transformOrigin:"{hx}px {hy}px"}});')
    I(f'gsap.set("#fig{i}",{{transformOrigin:"50% 85%",clipPath:"polygon(0% 0%,100% 0%,100% 0%,0% 0%)"}});')
    I(f'gsap.set("#rk{i}",{{xPercent:{-110 if L else 110},skewX:-9}}); gsap.set("#nm{i}",{{yPercent:115,skewX:-9}});')
    I(f'gsap.set("#fr{i} .slab",{{opacity:0,scale:0.9,transformOrigin:"{hx}px {hy}px"}}); gsap.set("#fr{i} .chev,#fr{i} .sq",{{opacity:0}});')
    for k, cls in enumerate(["f1", "f2", "f3"]):
        A(f'tl.to("#fr{i} .{cls}",{{strokeDashoffset:0,duration:0.42,ease:"power3.out"}},{at(t0 + 0.02 + 0.06 * k)});')
    A(f'tl.to("#fr{i} .slab",{{opacity:1,scale:1,duration:0.4,ease:"power3.out"}},{at(t0 + 0.08)});')
    A(f'tl.to("#fr{i} .chev,#fr{i} .sq",{{opacity:1,duration:0.2,stagger:0.03}},{at(t0 + 0.3)});')
    d = 1 if L else -1
    A(f'tl.fromTo("#fr{i}",{{rotationY:{-14 * d},rotation:{-3 * d},scale:0.94,x:{30 * d}}},{{rotationY:{6 * d},rotation:{3 * d},scale:1.05,x:{-20 * d},duration:1.95,ease:"power1.out"}},{at(t0)});')
    A(f'tl.to("#fr{i} .f2",{{rotation:{4 * d},svgOrigin:"{hx} {hy}",duration:1.9,ease:"none"}},{at(t0)});')
    A(f'tl.to("#fr{i} .f3",{{rotation:{-6 * d},svgOrigin:"{hx} {hy}",duration:1.9,ease:"none"}},{at(t0)});')
    A(f'tl.to("#fig{i}",{{clipPath:"polygon(0% 0%,100% 0%,100% 160%,0% 130%)",duration:0.45,ease:"power3.out"}},{at(t0 + 0.06)});')   # head first, diagonal edge
    A(f'tl.fromTo("#fig{i}",{{y:70,scale:1.0,x:{-12 * d}}},{{y:0,duration:0.5,ease:"power3.out"}},{at(t0 + 0.06)});')
    A(f'tl.to("#fig{i}",{{scale:1.05,x:{14 * d},duration:1.45,ease:"none"}},{at(t0 + 0.5)});')
    A(f'tl.to("#rk{i}",{{xPercent:0,duration:0.32,ease:"power4.out"}},{at(t0 + 0.24)});')
    A(f'tl.to("#nm{i}",{{yPercent:0,duration:0.36,ease:"power4.out"}},{at(t0 + 0.38)});')
    # exit: outgoing layers smear sideways under the wipe (restrained motion blur)
    A(f'tl.to("#m{i}in",{{x:{-90 * d},filter:"blur(6px)",duration:0.16,ease:"power2.in"}},{at(t0 + 1.82)});')

# ---------------- background particles + light sweep ----------------
rnd = random.Random(7); parts = []
for k in range(42):
    x, y, s = rnd.uniform(30, 1050), rnd.uniform(80, 1880), rnd.choice([3, 3, 4, 5, 6])
    col = "#ff4a4a" if rnd.random() < 0.45 else "#ffffff"; op = round(rnd.uniform(0.12, 0.45), 2)
    parts.append(f'<i style="left:{x:.0f}px;top:{y:.0f}px;width:{s}px;height:{s}px;background:{col};opacity:{op}"></i>')
    A(f'tl.to("#parts i:nth-child({k + 1})",{{y:{-rnd.uniform(90, 260):.0f},x:{rnd.uniform(-30, 30):.0f},duration:{TOTAL},ease:"none"}},0);')
for k, t in enumerate([0.05] + [s + 0.35 for s in SCN]):
    A(f'tl.set("#sweep",{{x:-1500,opacity:0}},{at(t)}); tl.to("#sweep",{{x:1500,opacity:1,duration:1.1,ease:"power1.inOut"}},{at(t + 0.001)});')
A(f'tl.to("#parts",{{opacity:0.25,duration:0.3}},{at(9.0)}); tl.to("#parts",{{opacity:1,duration:0.3}},{at(14.0)});')

# ---------------- wipes (diagonal red, with trailing ghosts for motion blur) ----------------
WIPES = [1.0, 3.0, 5.0, 7.0, 9.0, 14.0]
I('gsap.set("#wipeIn",{x:-2300});')
for T in WIPES:
    A(f'tl.set("#wipeIn",{{x:-2300}},{at(T - 0.20)}); tl.to("#wipeIn",{{x:2300,duration:0.40,ease:"power2.inOut"}},{at(T - 0.199)});')

# ---------------- opening ----------------
I('gsap.set("#ologo",{scale:0.78,opacity:0}); gsap.set("#glint",{xPercent:-160}); gsap.set("#oname",{yPercent:110}); gsap.set("#obar",{scaleX:0});')
I('gsap.set("#hdr",{opacity:0,y:-16});')
A('tl.to("#ologo",{scale:1,opacity:1,duration:0.34,ease:"back.out(1.7)"},0.04);')
A('tl.to("#glint",{xPercent:160,duration:0.42,ease:"power2.inOut"},0.30);')
A('tl.to("#oname",{yPercent:0,duration:0.28,ease:"power4.out"},0.34);')
A('tl.to("#obar",{scaleX:1,duration:0.3,ease:"power3.out"},0.42);')
A('tl.to("#ologo",{scale:1.04,duration:0.5,ease:"none"},0.38);')
A('tl.to("#hdr",{opacity:1,y:0,duration:0.3,ease:"power2.out"},0.62);')
A(f'tl.to("#hdr",{{opacity:0,duration:0.15}},{at(13.85)});')

# ---------------- credits (one stable layout, whole list visible 9.2-13.8) ----------------
cr = C["credits"]; byh = {c["heading"]: c for c in cr}
def block(c, cls=""):
    names = "".join(f"<div>{n}</div>" for n in c["names"])
    return f'<div class="cb {cls}"><h3>{c["heading"]}</h3>{names}</div>'
cols = f'<div class="cols">{block(cr[2])}{block(cr[3])}</div>'
def wrap(n, limit=32):                                               # long credit lines break before the middle "and"
    if len(n) <= limit or " and " not in n: return [n]
    cuts = [k for k in range(len(n)) if n.startswith(" and ", k)]
    k = min(cuts, key=lambda k: abs(k - len(n) / 2)); return [n[:k], n[k + 1:]]
sp = {"heading": cr[4]["heading"], "names": [l for n in cr[4]["names"] for l in wrap(n)]}
credits_inner = f'<div class="ct">{C["association"]}</div><div class="cbar"></div>{block(cr[0])}{block(cr[1])}{cols}{block(sp, "thanks")}'
I('gsap.set("#crin",{opacity:0,y:30});')
A('tl.to("#crin",{opacity:1,y:0,duration:0.28,ease:"power3.out"},9.02);')

# ---------------- ending ----------------
I('gsap.set("#elogo",{scale:0.8,opacity:0}); gsap.set("#e1",{yPercent:110,skewX:-9}); gsap.set("#e2",{yPercent:110,skewX:-9}); gsap.set("#ebar",{scaleX:0}); gsap.set("#ehandle",{opacity:0,y:20}); gsap.set("#eglint",{xPercent:-160});')
A('tl.to("#elogo",{scale:1,opacity:1,duration:0.32,ease:"back.out(1.6)"},14.02);')
A('tl.to("#e1",{yPercent:0,duration:0.3,ease:"power4.out"},14.10);')
A('tl.to("#e2",{yPercent:0,duration:0.3,ease:"power4.out"},14.18);')
A('tl.to("#ebar",{scaleX:1,duration:0.3,ease:"power3.out"},14.26);')
A('tl.to("#ehandle",{opacity:1,y:0,duration:0.28,ease:"power2.out"},14.32);')
A('tl.to("#eglint",{xPercent:160,duration:0.45,ease:"power2.inOut"},14.35);')
A('tl.to("#ein",{scale:1.03,duration:0.85,ease:"none"},14.15);')

# ---------------- sound: music dominant; a whoosh per wipe, a soft impact per name ----------------
sfx = []
for k, T in enumerate(WIPES):
    sfx.append((T - 0.2, "zoom-swish.wav", 0.28))
for t0 in SCN: sfx.append((t0 + 0.40, "thock.wav", 0.32))
sfx += [(0.30, "shimmer.wav", 0.22), (14.30, "shimmer.wav", 0.2)]
sfx_html = "\n".join(f'      <audio id="sx{k}" class="clip" src="assets/sfx/{f}" data-start="{at(t)}" data-duration="0.9" data-volume="{v}"></audio>' for k, (t, f, v) in enumerate(sfx))

tpl = open("index.tpl.html").read()
out = (tpl.replace("%%TOTAL%%", str(TOTAL)).replace("%%HEADER%%", C["header"]).replace("%%ASSOC%%", (lambda w: " ".join(w[:2]) + "<br><b>" + " ".join(w[2:]) + "</b>")(C["association"].split()))
          .replace("%%MASTERS%%", "\n".join(masters_html)).replace("%%PARTS%%", "".join(parts)).replace("%%CREDITS%%", credits_inner)
          .replace("%%END1%%", C["ending"].rsplit(" ", 1)[0]).replace("%%END2%%", C["ending"].rsplit(" ", 1)[1]).replace("%%HANDLE%%", C["handle"])
          .replace("%%SFX%%", sfx_html).replace("%%INIT%%", "\n".join("      " + x for x in init)).replace("%%JS%%", "\n".join("      " + x for x in js)))
open("edit/index.html", "w").write(out)
json.dump({"scenes": {"open": [0, 1], **{f"master{i + 1}": [SCN[i], SCN[i] + 2] for i in range(4)}, "credits": [9, 14], "end": [14, 15]},
           "wipes_center": WIPES, "sfx": [dict(t=at(t), file=f, gain=v) for t, f, v in sfx]}, open("edit/timing.json", "w"), indent=1)
import subprocess
chk = subprocess.run(["node", "-e", "const s=require('fs').readFileSync('edit/index.html','utf8');new Function(s.split('<script>')[1].split('</script>')[0])"], capture_output=True, text=True)
if chk.returncode: raise SystemExit("timeline JS does not parse:\n" + chk.stderr[-600:])
print("built", len(js), "tweens")
