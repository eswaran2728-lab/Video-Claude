# BeltFlow Lite – parents & students guide (1080x1920, 30 fps). -> video/ (HyperFrames project)
# Layers (index.html): bg (animated plum gradient, amber orbs, drifting stick/belt line-art) · one sub-composition per scene
# (phone mockup with camera push-ins, highlight boxes, finger taps, call-outs) · mascot (stick character) · belt motif ·
# captions (word-by-word highlight) · transitions (belt wipe / swipe / zoom-through / stick-spin at every cut) · audio mix.
# All motion is on GSAP timelines (seekable, deterministic); timings come from timing.json (tts25.py).
import json, html, math, os
T = json.load(open("timing.json")); TOTAL = T["total"]; SC = {s["id"]: s for s in T["scenes"]}
PLUM, PLUM2, AMBER, CARD, GREEN, RED, ORANGE = "#1f1435", "#120a21", "#ff9e1b", "#f7f5fa", "#10b981", "#ef4444", "#f97316"
BELTS = ["#ffffff", "#facc15", "#f97316", "#16a34a", "#2563eb", "#111111"]
R = lambda v: round(v, 3); esc = html.escape
os.makedirs("video/compositions", exist_ok=True)
CUES = []
K = 500 / 780                                   # screenshot px -> screen px
PX, PY, BZ = 274, 190, 16                       # phone frame position, bezel
SX0, SY0 = PX + BZ, PY + BZ                     # screen origin on stage
FX, FY = 540, 700                               # camera focus point
FONT = '"Jakarta", "Inter", sans-serif'

CSS = f'''
@font-face {{ font-family:"Jakarta"; font-weight:400; src:url("assets/fonts/plus-jakarta-sans-latin-400-normal.woff2") format("woff2"); }}
@font-face {{ font-family:"Jakarta"; font-weight:700; src:url("assets/fonts/plus-jakarta-sans-latin-700-normal.woff2") format("woff2"); }}
@font-face {{ font-family:"Jakarta"; font-weight:800; src:url("assets/fonts/plus-jakarta-sans-latin-800-normal.woff2") format("woff2"); }}
#root {{ position:absolute; inset:0; font-family:{FONT}; color:#fff; overflow:hidden; }}
.a {{ position:absolute; }}
.cam {{ position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin:0 0; }}
.phone {{ position:absolute; left:{PX}px; top:{PY}px; width:532px; height:1114px; border-radius:62px; background:linear-gradient(145deg,#3a2d55,#0d0718);
  box-shadow:0 40px 90px rgba(0,0,0,.55), inset 0 0 0 3px rgba(255,255,255,.12); }}
.scr {{ position:absolute; left:{BZ}px; top:{BZ}px; width:500px; height:1082px; border-radius:46px; overflow:hidden; background:{CARD}; }}
.ly {{ position:absolute; left:0; top:0; width:500px; }}
.ly img {{ display:block; width:500px; }}
.notch {{ position:absolute; left:196px; top:26px; width:140px; height:34px; border-radius:20px; background:#0d0718; }}
.hl {{ position:absolute; border:6px solid {AMBER}; border-radius:16px; box-shadow:0 0 0 2400px rgba(18,10,33,.52), 0 0 24px rgba(255,158,27,.8); }}
.pulse {{ position:absolute; border:6px solid {AMBER}; border-radius:50%; }}
.chip {{ position:absolute; padding:18px 30px; border-radius:30px; background:{CARD}; color:{PLUM}; font-weight:800; font-size:44px; box-shadow:0 18px 40px rgba(0,0,0,.4); white-space:nowrap; }}
.chip.am {{ background:{AMBER}; color:{PLUM2}; }} .chip.gr {{ background:{GREEN}; color:#fff; }} .chip.rd {{ background:{RED}; color:#fff; }} .chip.or {{ background:{ORANGE}; color:#fff; }}
.big {{ font-weight:800; font-size:104px; line-height:1.02; letter-spacing:-2px; }}
'''

FINGER = '''<svg width="120" height="150" viewBox="0 0 60 75"><path d="M22 4c3 0 5 2 5 5v20l3-1c3-1 5 1 6 3l1 3 3-1c3 0 5 2 5 4l1 2 3-1c3 0 5 2 5 5v14c0 10-8 18-18 18h-4c-6 0-11-3-14-8L4 47c-2-3-1-6 2-7 2-1 5 0 6 2l5 6V9c0-3 2-5 5-5z"
 fill="#fff7ec" stroke="#1f1435" stroke-width="2.6" stroke-linejoin="round"/></svg>'''


def tick_svg(col="#fff"):
    return f'<svg viewBox="0 0 24 24" width="100%" height="100%"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="{col}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def belt_svg(col, w=170):
    h = w * 0.55; stroke = "#2a1f3d"
    return (f'<svg width="{w}" height="{R(h)}" viewBox="0 0 100 55"><rect x="2" y="12" width="96" height="16" rx="5" fill="{col}" stroke="{stroke}" stroke-width="2.4"/>'
            f'<path d="M44 20 L30 52 L40 52 L50 30 L60 52 L70 52 L56 20 Z" fill="{col}" stroke="{stroke}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<rect x="41" y="9" width="18" height="22" rx="4" fill="{col}" stroke="{stroke}" stroke-width="2.4"/></svg>')


def stick_svg(w=520, h=34):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><linearGradient id="sg{w}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c98a4b"/><stop offset="1" stop-color="#7a4b22"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="{h / 2}" fill="url(#sg{w})"/>'
            f'<rect x="{w * 0.08}" y="0" width="{h * 0.9}" height="{h}" fill="{AMBER}"/><rect x="{w * 0.92 - h * 0.9}" y="0" width="{h * 0.9}" height="{h}" fill="{AMBER}"/></svg>')


class Scene:
    def __init__(s, sid):
        sc = SC[sid]; s.id = sid; s.dur = sc["dur"]; s.start = sc["start"]; s.sc = sc
        s.L = {l["cue"]: l for l in sc["lines"]}; s.els, s.js, s.init, s.layers = [], [], [], {}
        s.phone = False; s.cam_els = []

    def c(s, cue, d=0.0): return R(s.L[cue]["t0"] + d)
    def e(s, cue, d=0.0): return R(s.L[cue]["t1"] + d)
    def w(s, cue, i, d=0.0): return R(s.L[cue]["words"][i]["s"] + d)       # start of word i of a line
    def props(s, p): return ",".join(f"{k}:{json.dumps(v)}" for k, v in p.items())
    def tw(s, sel, t, d, p, ease="power3.out"): s.js.append(f'tl.to("{sel}",{{{s.props(p)},duration:{R(d)},ease:"{ease}"}},{R(max(0, t))});')
    def ft(s, sel, t, d, p0, p1, ease="power3.out"): s.js.append(f'tl.fromTo("{sel}",{{{s.props(p0)}}},{{{s.props(p1)},duration:{R(d)},ease:"{ease}",immediateRender:false}},{R(max(0, t))});')
    def st(s, sel, t, p): s.js.append(f'tl.set("{sel}",{{{s.props(p)}}},{R(max(0, t))});')
    def gs(s, sel, p): s.init.append(f'gsap.set("{sel}",{{{s.props(p)}}});')
    def sfx(s, t, f, g): CUES.append((R(s.start + max(0, t)), f, g))

    def add(s, eid, inner, style="", cls="a", t_in=None, t_out=None, enter="pop", sfx=None, into=None):
        el = f'<div id="{eid}" class="{cls}" style="{style}">{inner}</div>'
        (into if into is not None else s.els).append(el)
        if t_in is not None:
            fr = {"pop": {"opacity": 0, "scale": 0.4}, "up": {"opacity": 0, "y": 60}, "down": {"opacity": 0, "y": -60}, "left": {"opacity": 0, "x": -120},
                  "right": {"opacity": 0, "x": 120}, "fade": {"opacity": 0}}[enter]
            s.gs(f"#{eid}", fr); to = {k: (1 if k in ("opacity", "scale") else 0) for k in fr}
            s.tw(f"#{eid}", t_in, 0.6, to, "back.out(2.2)" if enter == "pop" else "power3.out")
            if sfx: s.sfx(t_in, *sfx)
        if t_out is not None:
            s.tw(f"#{eid}", t_out - 0.35, 0.35, {"opacity": 0, "scale": 0.8} if enter == "pop" else {"opacity": 0}, "power2.in")

    # ---------- phone ----------
    def phone_on(s, screens, t_in=None, style="spring"):
        """screens: [(layer_id, file, height_px_of_screenshot)]"""
        s.phone = True; s.screens = screens
        for lid, f, hpx in screens:
            s.layers[lid] = []; s.lh = getattr(s, "lh", {}); s.lh[lid] = hpx
        s.t_phone = t_in
        if t_in is None:                                   # already on screen after the cut: small settle
            s.gs("#ph", {"scale": 0.96, "transformOrigin": "50% 50%"}); s.tw("#ph", 0.05, 0.8, {"scale": 1}, "back.out(1.6)")
        else:
            s.gs("#ph", {"y": 1300, "rotationX": 35, "rotationY": -28, "rotationZ": -8, "transformPerspective": 1800, "opacity": 0})
            s.tw("#ph", t_in, 1.1, {"y": 0, "rotationX": 0, "rotationY": 0, "rotationZ": 0, "opacity": 1}, "back.out(1.15)")
            s.sfx(t_in, "curated/zoom-swish.wav", -20)
        f0 = (t_in or 0) + 1.2; n = max(1, int((s.dur - f0) / 2.6))
        s.js.append(f'tl.to("#flt",{{y:-12,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{2 * n - 1}}},{R(f0)});')

    def ov(s, lid, html_):
        s.layers[lid].append(html_)

    def push(s, t, sx, sy, Z=1.7, d=0.9, scroll=0):
        px, py = SX0 + sx * K, SY0 + (sy - scroll) * K
        s.tw("#cam", t, d, {"scale": Z, "x": R(FX - Z * px), "y": R(FY - Z * py)}, "power3.inOut"); s.sfx(t, "curated/zoom-swish.wav", -26)

    def pull(s, t, d=0.8): s.tw("#cam", t, d, {"scale": 1, "x": 0, "y": 0}, "power3.inOut")

    def hl(s, lid, rid, box, t_in, t_out, pad=10, r=16):
        x0, y0, x1, y1 = box
        s.ov(lid, f'<div id="{rid}" class="hl" style="left:{R(x0 * K - pad)}px;top:{R(y0 * K - pad)}px;width:{R((x1 - x0) * K + 2 * pad)}px;height:{R((y1 - y0) * K + 2 * pad)}px;border-radius:{r}px"></div>')
        s.gs(f"#{rid}", {"opacity": 0, "scale": 1.35}); s.tw(f"#{rid}", t_in, 0.55, {"opacity": 1, "scale": 1}, "back.out(1.8)")
        s.tw(f"#{rid}", t_out - 0.3, 0.3, {"opacity": 0}, "power2.in"); s.sfx(t_in, "curated/ui-pop.wav", -24)

    def tap(s, lid, rid, x, y, t):
        """finger comes in, presses at t (ripple), leaves"""
        cx, cy = x * K, y * K
        s.ov(lid, f'<div id="{rid}r" class="pulse" style="left:{R(cx - 40)}px;top:{R(cy - 40)}px;width:80px;height:80px"></div>'
                  f'<div id="{rid}" class="a" style="left:{R(cx - 34)}px;top:{R(cy - 8)}px;width:120px;height:150px;filter:drop-shadow(0 8px 10px rgba(0,0,0,.35))">{FINGER}</div>')
        s.gs(f"#{rid}", {"opacity": 0, "x": 130, "y": 170, "transformOrigin": "30% 10%"}); s.gs(f"#{rid}r", {"opacity": 0, "scale": 0.3})
        s.tw(f"#{rid}", t - 0.75, 0.6, {"opacity": 1, "x": 0, "y": 0}, "power3.out")
        s.tw(f"#{rid}", t - 0.12, 0.12, {"scale": 0.86}, "power2.in"); s.tw(f"#{rid}", t, 0.25, {"scale": 1}, "back.out(3)")
        s.ft(f"#{rid}r", t, 0.7, {"opacity": 1, "scale": 0.3}, {"opacity": 0, "scale": 2.6}, "power2.out")
        s.tw(f"#{rid}", t + 0.9, 0.45, {"opacity": 0, "x": 90, "y": 120}, "power2.in"); s.sfx(t, "curated/ui-click.wav", -12)

    def ring(s, lid, rid, x, y, t, n=3, size=90):
        cx, cy = x * K, y * K
        for i in range(n):
            s.ov(lid, f'<div id="{rid}{i}" class="pulse" style="left:{R(cx - size / 2)}px;top:{R(cy - size / 2)}px;width:{size}px;height:{size}px"></div>')
            s.gs(f"#{rid}{i}", {"opacity": 0}); s.ft(f"#{rid}{i}", t + i * 0.45, 1.1, {"opacity": 0.9, "scale": 0.4}, {"opacity": 0, "scale": 2.2}, "power2.out")

    def swap(s, old, new, t, how="slide"):
        if how == "slide":
            s.gs(f"#L{new}", {"x": 500}); s.tw(f"#L{new}", t, 0.7, {"x": 0}, "power3.inOut"); s.tw(f"#L{old}", t, 0.7, {"x": -500}, "power3.inOut")
        else:
            s.gs(f"#L{new}", {"opacity": 0}); s.tw(f"#L{new}", t, 0.6, {"opacity": 1}, "power2.inOut")
        s.sfx(t, "curated/zoom-swish.wav", -24)

    def scroll(s, lid, t, d, y): s.tw(f"#L{lid}", t, d, {"y": R(-y * K)}, "sine.inOut")

    def burst(s, eid, x, y, t, n=26, tick=True, col=GREEN):
        """tick ✓ + small confetti (deterministic)"""
        cols = [AMBER, "#ffd166", GREEN, "#60a5fa", "#f472b6", "#fff"]
        if tick:
            s.add(f"{eid}tk", f'<div style="width:150px;height:150px;border-radius:50%;background:{col};padding:24px;box-shadow:0 0 0 14px rgba(16,185,129,.25)">{tick_svg()}</div>',
                  f"left:{x - 75}px;top:{y - 75}px", "a")
            s.gs(f"#{eid}tk", {"opacity": 0, "scale": 0.2}); s.tw(f"#{eid}tk", t, 0.55, {"opacity": 1, "scale": 1}, "back.out(2.6)")
            s.tw(f"#{eid}tk", t + 1.6, 0.4, {"opacity": 0, "scale": 0.6}, "power2.in")
        for i in range(n):
            a = 2 * math.pi * i / n + 0.3 * math.sin(i * 7.1); dist = 170 + 90 * ((i * 37) % 10) / 10
            w_, h_ = (14, 22) if i % 3 else (16, 16)
            s.add(f"{eid}c{i}", "", f"left:{x}px;top:{y}px;width:{w_}px;height:{h_}px;border-radius:{50 if i % 3 == 0 else 3}%;background:{cols[i % 6]}", "a")
            s.gs(f"#{eid}c{i}", {"opacity": 0})
            s.ft(f"#{eid}c{i}", t + 0.05, 0.7, {"opacity": 1, "x": 0, "y": 0, "rotation": 0}, {"opacity": 1, "x": R(math.cos(a) * dist), "y": R(math.sin(a) * dist - 40), "rotation": 220 + i * 13}, "power3.out")
            s.tw(f"#{eid}c{i}", t + 0.75, 0.9, {"y": R(math.sin(a) * dist + 120), "opacity": 0}, "power1.in")
        s.sfx(t, "clean-ding.wav", -12); s.sfx(t + 0.05, "sparkle.wav", -20)

    def count(s, eid, t, d, to, fmt="{v}", start=0):
        s.js.append(f'(function(){{const o={{v:{start}}};tl.to(o,{{v:{to},duration:{d},ease:"power2.out",onUpdate:()=>{{document.getElementById("{eid}").textContent="{fmt}".replace("{{v}}",Math.round(o.v));}}}},{R(t)});}})();')
        s.sfx(t, "ratchet.wav", -24)

    def step_card(s, n, label):
        s.add("stc", f'''<div class="a" style="left:0;top:560px;width:1080px;text-align:center;font-weight:800;font-size:60px;color:{AMBER};letter-spacing:8px">STEP</div>
          <div class="a" style="left:390px;top:640px;width:300px;height:300px;overflow:hidden"><div id="stn" style="font-weight:800;font-size:300px;line-height:300px;text-align:center">{"<br>".join(str(i) for i in range(n + 1))}</div></div>
          <div class="a" style="left:0;top:980px;width:1080px;text-align:center;font-weight:800;font-size:66px">{esc(label)}</div>
          <div class="a" style="left:415px;top:1100px">{belt_svg(BELTS[n], 250)}</div>''',
              f"left:0;top:0;width:1080px;height:1920px;background:radial-gradient(70% 45% at 50% 42%, #3a2463, {PLUM} 70%)", "a")
        s.gs("#stc", {"opacity": 0, "scale": 1.1}); s.tw("#stc", 0.0, 0.4, {"opacity": 1, "scale": 1}, "power2.out")
        s.gs("#stn", {"y": 0}); s.tw("#stn", 0.15, 0.75, {"y": -300 * n}, "back.out(1.4)"); s.sfx(0.2, "ratchet.wav", -20)
        s.tw("#stc", 1.15, 0.45, {"yPercent": -100, "opacity": 0.3}, "power3.in"); s.sfx(1.15, "curated/zoom-swish.wav", -22)

    def write(s):
        ph = ""
        if s.phone:
            lys = "".join(f'<div id="L{lid}" class="ly" style="height:{R(s.lh[lid] * K)}px;z-index:{i + 1}"><img src="assets/screens/{f}" alt="">{"".join(s.layers[lid])}</div>'
                          for i, (lid, f, h) in enumerate(s.screens))
            ph = f'<div id="cam" class="cam"><div id="flt" class="a" style="left:0;top:0;width:1080px;height:1920px"><div id="ph" class="phone"><div class="scr">{lys}</div><div class="notch"></div></div></div>{"".join(s.cam_els)}</div>'
        open(f"video/compositions/{s.id}.html", "w").write(f'''<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{s.id}" data-width="1080" data-height="1920">
    {ph}
    {(chr(10) + "    ").join(s.els)}
  </div>
  <script>
    {(chr(10) + "    ").join(s.init)}
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(s.js)}
    tl.set({{}}, {{}}, {R(s.dur)});
    window.__timelines["{s.id}"] = tl;
  </script>
</template>
''')


scenes = []; MASCOT = []                     # (abs t, action)
def M(S, t, act): MASCOT.append((R(S.start + t), act))

# ---------------- 01 INTRO ----------------
S = Scene("s01"); scenes.append(S)
S.add("stk", stick_svg(620, 40), "left:230px;top:520px;width:620px;height:40px", "a")
S.gs("#stk", {"rotation": -360}); S.tw("#stk", 0.0, 1.4, {"rotation": 0}, "power3.out")
S.js.append('tl.to("#stk",{rotation:-8,duration:1.4,ease:"sine.inOut",yoyo:true,repeat:3},1.5);'); S.sfx(0.1, "curated/metallic-riser.wav", -22)
for i, wd in enumerate(("How", "to", "use")):
    S.add(f"tw{i}", wd, f"left:{[150, 400, 560][i]}px;top:640px;font-size:96px;font-weight:800", "a", None, None)
    S.ft(f"#tw{i}", 0.0, 0.7, {"y": 30}, {"y": 0}, "power3.out")
S.add("tbf", "BeltFlow", f"left:0;top:760px;width:1080px;text-align:center;font-size:170px;font-weight:800;color:{AMBER};letter-spacing:-4px", "a", None, None)
S.ft("#tbf", 0.0, 0.9, {"scale": 0.92}, {"scale": 1}, "back.out(2)")
S.add("tsub", "For parents &amp; students", "left:0;top:960px;width:1080px;text-align:center;font-size:52px;font-weight:700;opacity:.9", "a", 1.3, None, "up")
for i, col in enumerate(BELTS):
    S.add(f"ib{i}", belt_svg(col, 130), f"left:{75 + i * 160}px;top:1110px", "a", 1.6 + 0.15 * i, None, "pop", ("tick.wav", -26))
S.add("vk", "Vanakkam!", f"left:0;top:300px;width:1080px;text-align:center;font-size:92px;font-weight:800;color:{AMBER}", "a", S.w("hello", 1), None, "pop", ("clean-ding.wav", -18))
M(S, 0.6, "wave"); M(S, S.c("learn"), "cheer")

# ---------------- 02 OPEN THE APP ----------------
S = Scene("s02"); scenes.append(S); S.step_card(1, "Sign in")
S.phone_on([("a", "01-login-parent-student.png", 1688)], t_in=1.1)
S.push(S.c("tap", -0.2), 232, 749, 1.9); S.hl("a", "h1", (40, 720, 740, 780), S.c("tap"), S.dur)
S.tap("a", "t1", 232, 749, S.w("tap", 1, 0.1)); M(S, S.c("open"), "point")

# ---------------- 03 SIGN IN ----------------
S = Scene("s03"); scenes.append(S)
S.phone_on([("a", "02-login-filled.png", 1688)])
S.push(S.c("phone", -0.3), 390, 1010, 1.9); S.hl("a", "h1", (40, 972, 740, 1048), S.c("phone"), S.c("pin"))
S.push(S.c("pin", -0.2), 390, 1130, 1.9, 0.6); S.hl("a", "h2", (40, 1095, 740, 1172), S.c("pin"), S.c("signin"))
S.add("tip", f'<b style="color:{AMBER}">Tip:</b> Get your PIN<br>from your Master', f"left:270px;top:1580px;width:540px;padding:22px 30px;border-radius:30px 30px 30px 6px;background:{CARD};color:{PLUM};font-size:40px;font-weight:700;line-height:1.25;box-shadow:0 18px 40px rgba(0,0,0,.4)", "a", S.c("pin", 0.4), S.dur, "pop", ("curated/ui-pop.wav", -20))
S.push(S.c("signin", -0.3), 390, 1300, 1.6, 0.6); S.tap("a", "t1", 390, 1300, S.w("signin", 1, 0.1))
S.pull(S.w("signin", 1, 0.5)); S.burst("ok", 540, 760, S.w("signin", 1, 0.6))
M(S, S.c("pin", 0.3), "talk"); M(S, S.w("signin", 1, 0.6), "cheer")

# ---------------- 04 LANGUAGE ----------------
S = Scene("s04"); scenes.append(S)
S.phone_on([("a", "02-login-filled.png", 1688), ("b", "03-language-bm.png", 1688), ("c", "04-language-tamil.png", 1688)])
S.push(0.3, 620, 60, 2.2); S.hl("a", "h0", (470, 28, 748, 94), 0.6, 1.4, r=40)
S.tap("b", "t1", 600, 60, S.w("lang", 4, -0.2)); S.swap("a", "b", S.w("lang", 4, -0.15), "fade")
S.hl("b", "h1", (470, 28, 748, 94), S.w("lang", 4), S.w("lang", 6), r=40)
S.swap("b", "c", S.w("lang", 6, -0.1), "fade"); S.hl("c", "h2", (470, 28, 748, 94), S.w("lang", 6), S.dur, r=40)
for i, (lab, wi) in enumerate((("English", 3), ("Malay", 4), ("Tamil", 6))):
    S.add(f"lg{i}", lab, f"left:{[60, 390, 720][i]}px;top:1180px", "chip am" if i == 2 else "chip", S.w("lang", wi), None, "pop", ("curated/ui-pop.wav", -18))
S.pull(S.w("lang", 6, 0.9)); M(S, S.c("lang"), "point")

# ---------------- 05 MY CHILDREN ----------------
S = Scene("s05"); scenes.append(S); S.step_card(2, "See your child")
S.phone_on([("a", "05-parent-my-children.png", 1688)], t_in=1.1)
S.hl("a", "h0", (30, 250, 750, 980), S.c("kids", 0.3), S.c("belt"))
S.push(S.c("belt", -0.2), 432, 288, 2.0); S.hl("a", "h1", (322, 262, 545, 314), S.c("belt"), S.c("count"), r=30)
S.add("bc", f'<div style="display:flex;align-items:center;gap:18px">{belt_svg(BELTS[1], 120)}<span>Yellow belt</span></div>', "left:600px;top:200px", "chip", S.c("belt", 0.4), S.c("count"), "pop")
S.push(S.c("count", -0.2), 310, 461, 2.0); S.hl("a", "h2", (60, 420, 720, 520), S.c("count"), S.dur)
S.add("cnt", f'<span id="cntn">0</span>/20 <span style="font-size:34px;opacity:.75">classes</span>', "left:640px;top:200px;font-size:70px", "chip am", S.c("count", 0.3), S.dur, "pop")
S.count("cntn", S.c("count", 0.5), 1.4, 17); M(S, S.c("kids"), "point")

# ---------------- 06 CHILD DETAILS ----------------
S = Scene("s06"); scenes.append(S)
S.phone_on([("a", "05-parent-my-children.png", 1688), ("b", "06b-child-detail-full.png", 3442)])
S.push(S.c("tapname", -0.2), 171, 293, 1.8); S.tap("a", "t0", 171, 293, S.w("tapname", 1, 0.1))
S.swap("a", "b", S.w("tapname", 1, 0.5)); S.pull(S.w("tapname", 1, 0.5))
S.scroll("b", S.c("green", -0.6), 0.9, 760)
for cue, (lbl, box, cls) in {"green": ("Came", (30, 875, 750, 950), "gr"), "red": ("Absent", (30, 1345, 750, 1420), "rd"), "orange": ("Late", (30, 1110, 750, 1185), "or")}.items():
    S.hl("b", f"h{cue}", box, S.c(cue), S.e(cue, 0.45)); S.push(S.c(cue, -0.25), 390, (box[1] + box[3]) / 2, 1.75, 0.6, scroll=760)
    S.add(f"lb{cue}", lbl, "left:610px;top:1200px;font-size:56px", f"chip {cls}", S.c(cue, 0.1), S.e(cue, 0.45), "pop")
S.pull(S.c("grading", -0.6), 0.6); S.scroll("b", S.c("grading", -0.5), 0.9, 0); S.hl("b", "hg", (22, 395, 760, 712), S.c("grading", 0.3), S.dur)
S.add("gb", f'<div style="display:flex;align-items:center;gap:14px">{belt_svg(BELTS[1], 90)}<span style="font-size:50px">→</span>{belt_svg(BELTS[2], 90)}</div>', "left:560px;top:200px", "chip", S.c("grading", 0.6), S.dur, "pop", ("curated/ui-pop.wav", -20))
M(S, S.c("tapname"), "point"); M(S, S.c("green"), "talk")

# ---------------- 07 PAY THE FEE ----------------
S = Scene("s07"); scenes.append(S); S.step_card(3, "Pay the fee")
S.phone_on([("a", "05-parent-my-children.png", 1688), ("b", "07-pay-fee.png", 1688)], t_in=1.1)
S.hl("a", "h0", (40, 595, 470, 640), S.c("fee"), S.c("pay"), r=24)
S.add("rm", 'RM <span id="rmn">0</span>', "left:640px;top:200px;font-size:72px", "chip rd", S.c("fee", 0.4), S.c("pay", 0.5), "pop")
S.count("rmn", S.c("fee", 0.6), 1.1, 50)
S.push(S.c("pay", -0.3), 391, 802, 1.8); S.tap("a", "t0", 391, 802, S.w("pay", 1, 0.1))
S.swap("a", "b", S.w("pay", 1, 0.5)); S.pull(S.w("pay", 1, 0.5))
S.push(S.c("bank", -0.1), 390, 560, 1.55); S.hl("b", "h1", (40, 420, 742, 690), S.c("bank", 0.2), S.c("copy", 0.6))
S.push(S.c("copy", -0.3), 600, 618, 2.0, 0.6); S.tap("b", "t1", 647, 618, S.w("copy", 1, 0.1))
S.add("cpd", f'<div style="display:flex;align-items:center;gap:14px"><span style="width:52px;height:52px;border-radius:50%;background:{GREEN};padding:9px;display:block">{tick_svg()}</span>Copied!</div>', "left:340px;top:200px", "chip", S.w("copy", 1, 0.3), S.dur, "pop", ("clean-ding.wav", -16))
M(S, S.c("pay"), "point"); M(S, S.w("copy", 1, 0.3), "cheer")

# ---------------- 08 SEND RECEIPT ----------------
S = Scene("s08"); scenes.append(S)
S.phone_on([("a", "07c-upload-receipt-form.png", 1688)])
S.push(S.c("paid", -0.2), 231, 1196, 1.8); S.hl("a", "h0", (126, 1165, 336, 1228), S.c("paid"), S.c("photo"), r=20)
S.push(S.c("photo", -0.2), 300, 1330, 1.8, 0.6); S.hl("a", "h1", (60, 1275, 720, 1372), S.c("photo"), S.c("send"))
S.add("cam1", '<svg width="150" height="120" viewBox="0 0 30 24"><rect x="1" y="5" width="28" height="18" rx="4" fill="#f7f5fa" stroke="#1f1435" stroke-width="1.6"/><rect x="9" y="2" width="12" height="5" rx="2" fill="#f7f5fa" stroke="#1f1435" stroke-width="1.6"/><circle cx="15" cy="14" r="5.5" fill="#ff9e1b" stroke="#1f1435" stroke-width="1.6"/></svg>',
      "left:800px;top:220px", "a", S.c("photo", 0.3), S.c("send"), "pop", ("curated/camera-shutter-light.wav", -20))
S.push(S.c("send", -0.3), 391, 1607, 1.7, 0.6); S.tap("a", "t1", 391, 1607, S.w("send", 1, 0.1)); S.pull(S.w("send", 1, 0.6))
S.add("mst", f'<div style="width:150px;height:150px;border-radius:50%;background:{AMBER};color:{PLUM2};font-size:80px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 10px rgba(255,158,27,.3)">M</div><div style="text-align:center;font-size:40px;font-weight:800;margin-top:10px">Master</div>',
      "left:860px;top:200px;width:170px", "a", S.w("send", 1, 0.3), S.dur, "pop", ("curated/ui-pop.wav", -18))
for i in range(5):
    it = (f'<div style="width:70px;height:90px;border-radius:8px;background:#fff;border:3px solid {PLUM};padding:10px"><div style="height:6px;background:#ccc;margin:6px 0"></div><div style="height:6px;background:#ccc;margin:6px 0"></div><div style="height:6px;background:{AMBER};margin:6px 0"></div></div>'
          if i == 0 else f'<div style="width:62px;height:62px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffe08a,{AMBER});border:3px solid #b86a00;color:#7a3e00;font-size:22px;font-weight:800;display:flex;align-items:center;justify-content:center">RM</div>')
    S.add(f"fly{i}", it, "left:500px;top:1150px", "a"); S.gs(f"#fly{i}", {"opacity": 0, "scale": 0.5})
    t0 = S.w("send", 1, 0.5) + 0.18 * i
    S.tw(f"#fly{i}", t0, 0.25, {"opacity": 1, "scale": 1}, "back.out(2)")
    S.tw(f"#fly{i}", t0, 1.0, {"x": 400 - (0 if i == 0 else 10 * i)}, "power1.inOut"); S.js.append(f'tl.to("#fly{i}",{{y:-880,duration:1.0,ease:"back.in(1.1)"}},{R(t0)});')
    S.tw(f"#fly{i}", t0 + 0.9, 0.2, {"opacity": 0, "scale": 0.3}, "power2.in"); S.sfx(t0 + 0.95, "tick.wav", -20)
S.add("cash", f'<b style="color:{AMBER}">Paid cash?</b><br>Choose Cash instead.', f"left:270px;top:1580px;width:540px;padding:22px 30px;border-radius:30px 30px 30px 6px;background:{CARD};color:{PLUM};font-size:40px;font-weight:700;line-height:1.25;box-shadow:0 18px 40px rgba(0,0,0,.4)", "a", S.c("photo", 0.4), S.dur, "pop", ("curated/ui-pop.wav", -20))
M(S, S.c("paid"), "point"); M(S, S.w("send", 1, 1.4), "cheer")

# ---------------- 09 WAIT ----------------
S = Scene("s09"); scenes.append(S)
S.phone_on([("a", "07d-receipt-sent-pending.png", 1688)])
S.push(S.c("wait", -0.2), 390, 1108, 1.7); S.hl("a", "h0", (30, 1052, 752, 1168), S.c("wait"), S.dur)
S.add("hg", '<svg width="120" height="160" viewBox="0 0 24 32"><path d="M3 2h18M3 30h18M5 2c0 8 6 10 6 14S5 22 5 30M19 2c0 8-6 10-6 14s6 6 6 14" fill="none" stroke="#ff9e1b" stroke-width="2.2" stroke-linecap="round"/><path d="M8 27c2-3 6-3 8 0z" fill="#ff9e1b"/></svg>',
      "left:830px;top:240px", "a", S.c("wait", 0.2), S.c("turns"), "pop")
S.js.append(f'tl.to("#hg",{{rotation:180,duration:0.8,ease:"power2.inOut",repeat:2,repeatDelay:0.6}},{R(S.c("wait", 0.9))});')
S.add("mck", f'<div style="width:140px;height:140px;border-radius:50%;background:{AMBER};color:{PLUM2};font-size:74px;font-weight:800;display:flex;align-items:center;justify-content:center">M</div>'
      f'<svg class="a" style="left:80px;top:70px" width="100" height="100" viewBox="0 0 24 24"><circle cx="10" cy="10" r="6.5" fill="rgba(255,255,255,.4)" stroke="#fff" stroke-width="2.4"/><path d="M15 15l6 6" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>',
      "left:40px;top:220px;width:190px;height:190px", "a", S.c("check"), S.c("turns", 0.6), "pop", ("curated/ui-pop.wav", -18))
S.js.append(f'tl.to("#mck svg",{{x:-30,y:-20,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:3}},{R(S.c("check", 0.3))});')
S.ov("a", f'<div id="pd" class="a" style="left:{R(50 * K)}px;top:{R(1058 * K)}px;width:{R(690 * K)}px;height:{R(104 * K)}px;border-radius:14px;background:#e9fbf3;border-left:6px solid {GREEN};display:flex;align-items:center;gap:12px;padding-left:16px;color:#065f46;font-weight:800;font-size:24px">'
          f'<span style="width:34px;height:34px;border-radius:50%;background:{GREEN};padding:6px;display:block">{tick_svg()}</span>2026-11 · RM 50 · Paid</div>')
S.gs("#pd", {"opacity": 0, "scaleX": 0, "transformOrigin": "0 50%"}); S.tw("#pd", S.w("turns", 3, -0.1), 0.6, {"opacity": 1, "scaleX": 1}, "power3.out")
S.pull(S.w("turns", 3, 0.5)); S.burst("ok", 540, 760, S.w("turns", 3, 0.5))
M(S, S.c("check"), "talk"); M(S, S.w("turns", 3, 0.5), "cheer")

# ---------------- 10 NOTICES ----------------
S = Scene("s10"); scenes.append(S); S.step_card(4, "News and belts")
S.phone_on([("a", "08-notices.png", 1688)], t_in=1.1)
S.push(S.c("news", -0.1), 390, 330, 1.7); S.hl("a", "h0", (30, 250, 752, 410), S.c("news", 0.3), S.dur)
S.add("wa", f'''<div style="position:relative;padding:24px 30px;border-radius:28px 28px 28px 6px;background:#dcf8c6;color:#0b3d2e;box-shadow:0 18px 40px rgba(0,0,0,.4);width:520px">
   <div style="font-size:28px;font-weight:800;color:#128c7e">BeltFlow notice</div><div style="font-size:40px;font-weight:800;margin-top:6px">Belt test day! 14 Dec</div>
   <div style="font-size:28px;opacity:.75;margin-top:6px">Come in full uniform with your stick.</div></div>''', "left:300px;top:1560px", "a", None, S.dur)
S.gs("#wa", {"opacity": 0, "scale": 0.3, "x": -120, "y": -500, "transformOrigin": "0% 100%"})
S.tw("#wa", S.c("testday"), 0.8, {"opacity": 1, "scale": 1, "x": 0, "y": 0}, "back.out(1.6)"); S.sfx(S.c("testday"), "curated/ui-pop.wav", -14)
S.add("bell", '<svg width="110" height="110" viewBox="0 0 24 24"><path d="M12 3a6 6 0 0 0-6 6v4l-2 3h16l-2-3V9a6 6 0 0 0-6-6z" fill="#ff9e1b" stroke="#1f1435" stroke-width="1.4"/><circle cx="12" cy="19.5" r="2" fill="#ff9e1b" stroke="#1f1435" stroke-width="1.4"/></svg>',
      "left:860px;top:220px", "a", S.c("news", 0.2), S.dur, "pop")
S.js.append(f'tl.to("#bell",{{rotation:18,duration:0.18,ease:"sine.inOut",yoyo:true,repeat:7,transformOrigin:"50% 10%"}},{R(S.c("news", 0.8))});')
M(S, S.c("news"), "point"); M(S, S.c("testday", 0.3), "cheer")

# ---------------- 11 BELTS ----------------
S = Scene("s11"); scenes.append(S)
S.phone_on([("a", "09b-belts-full.png", 1944)])
S.hl("a", "h0", (22, 245, 760, 460), S.c("learn", 0.2), S.c("next"))
S.scroll("a", S.c("next", -0.2), 1.6, 256)
S.add("ldr", "", "left:0;top:0;width:0;height:0", "a")
for i, col in enumerate(BELTS):
    S.add(f"lb{i}", belt_svg(col, 150), f"left:{[860, 40][i % 2] if False else 880}px;top:{1180 - i * 170}px", "a", S.c("next", 0.2 + 0.32 * i), None, "up", ("tick.wav", -22))
S.add("star", f'<svg width="110" height="110" viewBox="0 0 24 24"><path d="M12 2l2.9 6.2 6.8.7-5.1 4.6 1.5 6.7L12 16.8 5.9 20.2l1.5-6.7L2.3 8.9l6.8-.7z" fill="{AMBER}" stroke="#fff" stroke-width="1"/></svg>',
      "left:900px;top:150px", "a", S.c("next", 2.3), None, "pop", ("clean-ding.wav", -16))
S.js.append(f'tl.to("#star",{{rotation:360,duration:2,ease:"power1.inOut"}},{R(S.c("next", 2.6))});')
M(S, S.c("learn"), "point"); M(S, S.c("next", 2.3), "cheer")

# ---------------- 12 STUDENTS ----------------
S = Scene("s12"); scenes.append(S); S.step_card(5, "Students and sign out")
S.phone_on([("a", "11-student-home.png", 1688)], t_in=1.1)
S.push(S.c("students", 0.1), 390, 360, 1.6); S.hl("a", "h0", (30, 250, 752, 690), S.c("students", 0.4), S.dur)
S.ring("a", "rg", 713, 59, S.c("own"), 3, 80)
S.add("own", f'<div style="display:flex;align-items:center;gap:14px"><svg width="54" height="70" viewBox="0 0 24 32"><rect x="3" y="1" width="18" height="30" rx="4" fill="none" stroke="#1f1435" stroke-width="2.4"/><circle cx="12" cy="26" r="1.6" fill="#1f1435"/></svg>Own phone</div>',
      "left:610px;top:200px", "chip am", S.c("own", 0.2), S.dur, "pop", ("curated/ui-pop.wav", -18))
M(S, S.c("students"), "wave")

# ---------------- 13 SIGN OUT ----------------
S = Scene("s13"); scenes.append(S)
S.phone_on([("a", "10-account.png", 1688)])
S.push(S.c("done", 0.1), 300, 372, 1.8); S.hl("a", "h0", (40, 330, 750, 415), S.c("out"), S.dur)
S.tap("a", "t1", 227, 372, S.w("out", 1, 0.1)); M(S, S.c("out", 0.4), "wave")

# ---------------- 14 OUTRO ----------------
S = Scene("s14"); scenes.append(S)
S.add("lg", f'''<svg width="300" height="300" viewBox="0 0 100 100"><g transform="rotate(-35 50 50)">{'<rect x="8" y="46" width="84" height="8" rx="4" fill="#c98a4b"/>'}</g><g transform="rotate(35 50 50)"><rect x="8" y="46" width="84" height="8" rx="4" fill="#c98a4b"/></g>
   <rect x="22" y="34" width="56" height="12" rx="4" fill="#fff"/><path d="M45 44 L36 66 L43 66 L50 52 L57 66 L64 66 L55 44 Z" fill="#fff"/><rect x="43" y="31" width="14" height="17" rx="3" fill="#fff"/></svg>''',
      "left:390px;top:260px", "a")
S.gs("#lg", {"opacity": 0, "scale": 0.2, "rotation": -200}); S.tw("#lg", 0.1, 1.1, {"opacity": 1, "scale": 1, "rotation": 0}, "back.out(1.5)")
S.add("ot", "BeltFlow Lite", f"left:0;top:600px;width:1080px;text-align:center;font-size:110px;font-weight:800;color:{AMBER}", "a", 0.4, None, "pop", ("thock.wav", -18))
S.add("os", "PERSATUAN SILAMBAM DAERAH SEPANG", "left:0;top:740px;width:1080px;text-align:center;font-size:36px;font-weight:800;letter-spacing:3px;opacity:.9", "a", 0.7, None, "up")
S.add("url", "beltflow-lite.vercel.app", "left:220px;top:850px;width:640px;text-align:center;font-size:48px", "chip", 1.0, None, "pop", ("curated/ui-pop.wav", -18))
S.add("pin", "Ask your Master for your PIN", f"left:0;top:1010px;width:1080px;text-align:center;font-size:52px;font-weight:700", "a", 1.4, None, "up")
for i, col in enumerate(BELTS):
    S.add(f"eb{i}", belt_svg(col, 120), f"left:{110 + i * 150}px;top:1130px", "a", 1.6 + 0.12 * i, None, "pop", ("tick.wav", -26))
S.burst("cf", 540, 520, S.c("great", 0.1), 34, tick=False); S.burst("cf2", 540, 520, S.c("bye", 0.1), 34, tick=False)
M(S, S.c("great"), "cheer"); M(S, S.c("bye"), "wave")

for S in scenes: S.write()

# ---------------- background ----------------
bg_els = [f'<div id="g1" class="a" style="left:-540px;top:-960px;width:2160px;height:3840px;background:radial-gradient(40% 30% at 30% 35%, #3b2366 0%, rgba(59,35,102,0) 70%), radial-gradient(35% 25% at 70% 65%, #2b1850 0%, rgba(43,24,80,0) 70%), linear-gradient(160deg,{PLUM},{PLUM2} 60%,#24123f)"></div>']
bg_js = [f'tl.to("#g1",{{x:300,y:420,rotation:8,duration:{R(TOTAL / 2)},ease:"sine.inOut"}},0);', f'tl.to("#g1",{{x:-120,y:-200,rotation:-4,duration:{R(TOTAL / 2)},ease:"sine.inOut"}},{R(TOTAL / 2)});']
for i in range(9):
    sz = 140 + (i * 53) % 260; x0 = (i * 263) % 1000; y0 = (i * 431) % 1800
    bg_els.append(f'<div id="o{i}" class="a" style="left:{x0}px;top:{y0}px;width:{sz}px;height:{sz}px;border-radius:50%;background:radial-gradient(circle, rgba(255,158,27,{0.22 + 0.04 * (i % 3)}) 0%, rgba(255,158,27,0) 70%)"></div>')
    seg = TOTAL / 3
    for k in range(3):
        bg_js.append(f'tl.to("#o{i}",{{x:{(-1) ** (i + k) * (120 + 40 * k)},y:{(-1) ** (i // 2 + k) * (160 + 30 * i % 90)},duration:{R(seg)},ease:"sine.inOut"}},{R(k * seg)});')
for i in range(7):
    kind = i % 2; x0 = (i * 177) % 900; y0 = 150 + (i * 291) % 1600
    art = (f'<svg width="420" height="24" viewBox="0 0 420 24"><rect x="2" y="2" width="416" height="20" rx="10" fill="none" stroke="{AMBER}" stroke-width="3"/><path d="M40 2v20M380 2v20" stroke="{AMBER}" stroke-width="3"/></svg>' if kind == 0
           else f'<svg width="150" height="82" viewBox="0 0 100 55"><rect x="2" y="12" width="96" height="16" rx="5" fill="none" stroke="{AMBER}" stroke-width="2.6"/><path d="M44 20 L30 52 L40 52 L50 30 L60 52 L70 52 L56 20 Z" fill="none" stroke="{AMBER}" stroke-width="2.6"/></svg>')
    bg_els.append(f'<div id="la{i}" class="a" style="left:{x0}px;top:{y0}px;opacity:.12">{art}</div>')
    bg_js.append(f'tl.fromTo("#la{i}",{{rotation:{-30 + i * 17},x:0,y:0}},{{rotation:{10 + i * 23},x:{(-1) ** i * 160},y:{-260 + i * 40},duration:{R(TOTAL)},ease:"none"}},0);')
open("video/compositions/bg.html", "w").write(f'''<template>
  <style>#root {{ position:absolute; inset:0; overflow:hidden; background:{PLUM2}; }} .a {{ position:absolute; }}</style>
  <div id="root" data-composition-id="bg" data-width="1080" data-height="1920">
    {(chr(10) + "    ").join(bg_els)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(bg_js)}
    tl.set({{}}, {{}}, {R(TOTAL)});
    window.__timelines["bg"] = tl;
  </script>
</template>
''')

# ---------------- mascot (stick character) + belt motif ----------------
STEP_AT = [0] + [SC[s]["start"] for s in ("s02", "s05", "s07", "s10", "s12")]
mas = f'''<div id="mas" class="a" style="left:40px;top:1556px;width:230px;height:380px">
  <svg id="mbody" width="230" height="380" viewBox="0 0 115 190" overflow="visible">
    <defs><linearGradient id="wd" x1="0" x2="1"><stop offset="0" stop-color="#d6995a"/><stop offset="1" stop-color="#8a5629"/></linearGradient></defs>
    <g id="armL" style="transform-origin:42px 92px"><path d="M42 92 L18 118" stroke="#8a5629" stroke-width="7" stroke-linecap="round"/><circle cx="16" cy="120" r="8" fill="#ffd9b0" stroke="#1f1435" stroke-width="2"/></g>
    <g id="armR" style="transform-origin:73px 92px"><path d="M73 92 L97 118" stroke="#8a5629" stroke-width="7" stroke-linecap="round"/><circle cx="99" cy="120" r="8" fill="#ffd9b0" stroke="#1f1435" stroke-width="2"/></g>
    <rect x="40" y="20" width="35" height="160" rx="17" fill="url(#wd)" stroke="#1f1435" stroke-width="2.6"/>
    <rect x="40" y="30" width="35" height="12" fill="{AMBER}"/>
    <circle cx="51" cy="62" r="7" fill="#fff" stroke="#1f1435" stroke-width="2"/><circle cx="65" cy="62" r="7" fill="#fff" stroke="#1f1435" stroke-width="2"/>
    <circle id="pl" cx="52" cy="63" r="3.4" fill="#1f1435"/><circle id="pr" cx="66" cy="63" r="3.4" fill="#1f1435"/>
    <circle cx="45" cy="74" r="3.6" fill="#ff8fab" opacity=".8"/><circle cx="71" cy="74" r="3.6" fill="#ff8fab" opacity=".8"/>
    <path id="mouth" d="M51 76 Q58 84 65 76" fill="none" stroke="#1f1435" stroke-width="2.6" stroke-linecap="round"/>
    <rect id="mbelt" x="37" y="118" width="41" height="11" rx="3" fill="#fff" stroke="#1f1435" stroke-width="2.2"/>
    <path id="mknot" d="M55 126 L49 142 L54 142 L57 132 L60 142 L65 142 L59 126 Z" fill="#fff" stroke="#1f1435" stroke-width="2"/>
    <rect x="40" y="170" width="35" height="10" rx="5" fill="{AMBER}"/>
  </svg></div>'''
ms_js, ms_init = [], ['gsap.set("#mas",{opacity:0,y:260});', 'gsap.set("#motif",{opacity:0,scale:.5});']
ms_js.append('tl.to("#mas",{opacity:1,y:0,duration:0.9,ease:"back.out(1.6)"},0.3);')
n_b = int((TOTAL - 1.5) / 2.0); ms_js.append(f'tl.to("#mas",{{y:-10,duration:1.0,ease:"sine.inOut",yoyo:true,repeat:{2 * n_b - 1}}},1.3);')
for t, act in sorted(MASCOT):
    if act == "wave":
        ms_js.append(f'tl.to("#armR",{{rotation:-140,duration:0.3,ease:"power2.out"}},{R(t)});')
        ms_js.append(f'tl.to("#armR",{{rotation:-105,duration:0.22,ease:"sine.inOut",yoyo:true,repeat:5}},{R(t + 0.3)});')
        ms_js.append(f'tl.to("#armR",{{rotation:0,duration:0.4,ease:"power2.inOut"}},{R(t + 1.7)});')
    elif act == "point":
        ms_js.append(f'tl.to("#armR",{{rotation:-95,duration:0.35,ease:"back.out(2)"}},{R(t)});')
        ms_js.append(f'tl.to("#pl,#pr",{{x:2,y:-2,duration:0.3}},{R(t)});')
        ms_js.append(f'tl.to("#armR",{{rotation:0,duration:0.4,ease:"power2.inOut"}},{R(t + 1.6)});'); ms_js.append(f'tl.to("#pl,#pr",{{x:0,y:0,duration:0.3}},{R(t + 1.6)});')
    elif act == "cheer":
        ms_js.append(f'tl.to("#armL",{{rotation:130,duration:0.3,ease:"back.out(2)"}},{R(t)});'); ms_js.append(f'tl.to("#armR",{{rotation:-130,duration:0.3,ease:"back.out(2)"}},{R(t)});')
        ms_js.append(f'tl.to("#mbody",{{y:-70,duration:0.32,ease:"power2.out",yoyo:true,repeat:3}},{R(t)});')
        ms_js.append(f'tl.to("#armL,#armR",{{rotation:0,duration:0.45,ease:"power2.inOut"}},{R(t + 1.4)});')
    elif act == "talk":
        ms_js.append(f'tl.to("#mouth",{{scaleY:1.6,transformOrigin:"50% 0%",duration:0.15,yoyo:true,repeat:7}},{R(t)});')
# belt motif (top-right) and the mascot's belt change colour at each step
motif = f'<div id="motif" class="a" style="left:40px;top:180px;width:170px;height:94px">' + "".join(f'<div id="mb{i}" class="a" style="left:0;top:0;opacity:{1 if i == 0 else 0}">{belt_svg(c, 170)}</div>' for i, c in enumerate(BELTS)) + "</div>"
ms_js.append('tl.to("#motif",{opacity:1,scale:1,duration:0.6,ease:"back.out(2)"},1.0);')
for i, t in enumerate(STEP_AT[1:], 1):
    ms_js.append(f'tl.to("#mb{i - 1}",{{opacity:0,rotationY:90,duration:0.3,ease:"power2.in"}},{R(t + 1.3)});')
    ms_js.append(f'tl.fromTo("#mb{i}",{{opacity:0,rotationY:-90}},{{opacity:1,rotationY:0,duration:0.4,ease:"back.out(2)",immediateRender:false}},{R(t + 1.6)});')
    ms_js.append(f'tl.to("#mbelt,#mknot",{{fill:"{BELTS[i]}",duration:0.4}},{R(t + 1.6)});')
    CUES.append((R(t + 1.6), "tick.wav", -20))
# hide motif on intro/outro cards
ms_js.append(f'tl.to("#motif",{{opacity:0,duration:0.4}},{R(SC["s14"]["start"])});')
open("video/compositions/mascot.html", "w").write(f'''<template>
  <style>#root {{ position:absolute; inset:0; overflow:visible; }} .a {{ position:absolute; }}</style>
  <div id="root" data-composition-id="mascot" data-width="1080" data-height="1920">
    {mas}
    {motif}
  </div>
  <script>
    {(chr(10) + "    ").join(ms_init)}
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(ms_js)}
    tl.set({{}}, {{}}, {R(TOTAL)});
    window.__timelines["mascot"] = tl;
  </script>
</template>
''')

# ---------------- captions: one group per voice line, word-by-word highlight, key words stay amber ----------------
KEY = {"Vanakkam!", "together!", "Parent", "Student.", "phone", "PIN.", "Sign", "in!", "English,", "Malay", "Tamil!", "children.", "belt", "classes", "name",
       "Green", "Red", "Orange", "tests", "fee?", "Pay.", "bank", "Copy!", "bank?", "photo", "Send", "wait.", "checks", "green!", "Notices", "test", "Belts",
       "next", "Students", "own", "done?", "out.", "Great", "job!", "class!"}
cap_els, cap_js, cap_init, srt, n = [], [], [], [], 0
fmt = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round((t % 1) * 1000)) % 1000:03d}"
lines = [(sc, l) for sc in T["scenes"] for l in sc["lines"]]
for k, (sc, l) in enumerate(lines):
    t0 = sc["start"] + l["t0"]; nxt = (lines[k + 1][0]["start"] + lines[k + 1][1]["t0"]) if k + 1 < len(lines) else TOTAL
    t_out = min(nxt - 0.12, sc["start"] + l["t1"] + 1.2)
    spans = "".join(f'<span id="c{n}w{i}" class="w">{esc(w["w"])}</span>' for i, w in enumerate(l["words"]))
    cap_els.append(f'<div id="c{n}" class="cg"><div class="cb">{spans}</div></div>')
    cap_init.append(f'gsap.set("#c{n}",{{opacity:0,scale:.82,y:40}});')
    cap_js.append(f'tl.to("#c{n}",{{opacity:1,scale:1,y:0,duration:0.42,ease:"back.out(1.9)"}},{R(t0 - 0.15)});')
    cap_js.append(f'tl.to("#c{n}",{{opacity:0,y:-30,duration:0.25,ease:"power2.in"}},{R(t_out - 0.25)});')
    for i, w in enumerate(l["words"]):
        ws, we = sc["start"] + w["s"], sc["start"] + w["e"]
        cap_js.append(f'tl.to("#c{n}w{i}",{{color:"{AMBER}",scale:1.08,duration:0.12,ease:"power2.out"}},{R(ws)});')
        if w["w"] not in KEY: cap_js.append(f'tl.to("#c{n}w{i}",{{color:"#ffffff",scale:1,duration:0.15}},{R(max(we, ws + 0.12))});')
        else: cap_js.append(f'tl.to("#c{n}w{i}",{{scale:1,duration:0.15}},{R(max(we, ws + 0.12))});')
    CUES.append((R(t0 - 0.1), "curated/ui-pop.wav", -27))
    srt.append(f"{n + 1}\n{fmt(t0)} --> {fmt(sc['start'] + l['t1'])}\n{l['text']}\n"); n += 1
open("video/compositions/captions.html", "w").write(f'''<template>
  <style>
    @font-face {{ font-family:"Jakarta"; font-weight:800; src:url("assets/fonts/plus-jakarta-sans-latin-800-normal.woff2") format("woff2"); }}
    #root {{ position:absolute; inset:0; font-family:{FONT}; }}
    .cg {{ position:absolute; left:60px; width:960px; top:1335px; height:230px; display:flex; align-items:center; justify-content:center; text-align:center; }}
    .cb {{ display:inline-block; padding:18px 34px; border-radius:36px; background:rgba(18,10,33,.82); box-shadow:0 18px 40px rgba(0,0,0,.35); font-weight:800; font-size:74px; line-height:1.12; color:#fff; }}
    .w {{ display:inline-block; margin:0 .14em; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    {(chr(10) + "    ").join(cap_els)}
  </div>
  <script>
    {(chr(10) + "    ").join(cap_init)}
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(cap_js)}
    tl.set({{}}, {{}}, {R(TOTAL)});
    window.__timelines["captions"] = tl;
  </script>
</template>
''')
open("videos/parents-students.srt", "w").write("\n".join(srt))

# ---------------- transitions at every cut ----------------
tr_els, tr_js, tr_init = [], [], []
cuts = [sc["start"] for sc in T["scenes"][1:]]
for i, b in enumerate(cuts):
    kind = ["belt", "swipe", "zoom", "stick"][i % 4]; p = f"x{i}"
    if kind == "belt":
        for j, col in enumerate(BELTS):
            tr_els.append(f'<div id="{p}s{j}" class="a" style="left:{j * 180}px;top:0;width:181px;height:1920px;background:{col}"></div>')
            tr_init.append(f'gsap.set("#{p}s{j}",{{yPercent:-100}});')
            tr_js.append(f'tl.to("#{p}s{j}",{{yPercent:0,duration:0.32,ease:"power2.in"}},{R(b - 0.4 + 0.012 * j)});')
            tr_js.append(f'tl.to("#{p}s{j}",{{yPercent:100,duration:0.34,ease:"power2.out"}},{R(b + 0.02 + 0.012 * j)});')
    elif kind == "swipe":
        tr_els.append(f'<div id="{p}p" class="a" style="left:0;top:0;width:1300px;height:1920px;background:linear-gradient(90deg,{AMBER} 0 70px,{PLUM} 70px)"></div>')
        tr_init.append(f'gsap.set("#{p}p",{{x:1100}});')
        tr_js.append(f'tl.to("#{p}p",{{x:-110,duration:0.38,ease:"power3.in"}},{R(b - 0.38)});'); tr_js.append(f'tl.to("#{p}p",{{x:-1400,duration:0.4,ease:"power3.out"}},{R(b)});')
    elif kind == "zoom":
        tr_els.append(f'<div id="{p}c" class="a" style="left:440px;top:860px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,{AMBER} 0 55%,{PLUM} 56%)"></div>')
        tr_init.append(f'gsap.set("#{p}c",{{scale:0}});')
        tr_js.append(f'tl.to("#{p}c",{{scale:13,duration:0.4,ease:"power2.in"}},{R(b - 0.4)});'); tr_js.append(f'tl.to("#{p}c",{{scale:0,duration:0.4,ease:"power2.out"}},{R(b + 0.02)});')
    else:
        tr_els.append(f'<div id="{p}w" class="a" style="left:0;top:0;width:1080px;height:1920px;background:{PLUM}"></div>')
        tr_els.append(f'<div id="{p}k" class="a" style="left:-60px;top:940px;width:1200px;height:44px">{stick_svg(1200, 44)}</div>')
        tr_init.append(f'gsap.set("#{p}w",{{clipPath:"circle(0% at 50% 50%)"}});gsap.set("#{p}k",{{opacity:0,scale:.4,rotation:0}});')
        tr_js.append(f'tl.to("#{p}w",{{clipPath:"circle(75% at 50% 50%)",duration:0.4,ease:"power2.in"}},{R(b - 0.4)});')
        tr_js.append(f'tl.to("#{p}k",{{opacity:1,scale:1,rotation:360,duration:0.8,ease:"power2.inOut"}},{R(b - 0.4)});')
        tr_js.append(f'tl.to("#{p}w",{{clipPath:"circle(0% at 50% 50%)",duration:0.4,ease:"power2.out"}},{R(b + 0.02)});')
        tr_js.append(f'tl.to("#{p}k",{{opacity:0,duration:0.2}},{R(b + 0.25)});')
    CUES.append((R(b - 0.3), "curated/zoom-swish.wav", -19))
open("video/compositions/trans.html", "w").write(f'''<template>
  <style>#root {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; }} .a {{ position:absolute; }}</style>
  <div id="root" data-composition-id="trans" data-width="1080" data-height="1920">
    {(chr(10) + "    ").join(tr_els)}
  </div>
  <script>
    {(chr(10) + "    ").join(tr_init)}
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(tr_js)}
    tl.set({{}}, {{}}, {R(TOTAL)});
    window.__timelines["trans"] = tl;
  </script>
</template>
''')

# ---------------- root ----------------
def host(cid, start, dur, z, track, kind="graphics"):
    return (f'<div id="h_{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{R(start)}" data-duration="{R(dur)}" '
            f'data-track-index="{track}" data-track-kind="{kind}" data-width="1080" data-height="1920" style="z-index:{z}"></div>')
hosts = [host("bg", 0, TOTAL, 1, 1)] + [host(sc["id"], sc["start"], sc["dur"], 2, 2) for sc in T["scenes"]] + \
        [host("mascot", 0, TOTAL, 3, 3), host("captions", 0, TOTAL, 4, 4, "captions"), host("trans", 0, TOTAL, 5, 5)]
open("video/index.html", "w").write(f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:{PLUM2}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{R(TOTAL)}" data-fps="30">
      {(chr(10) + "      ").join(hosts)}
      <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{R(TOTAL)}" data-track-index="6" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
''')
json.dump({"cues": [{"t": a, "sfx": b, "gain_db": c} for a, b, c in sorted(CUES)]}, open("video/cues.json", "w"), indent=1)
print("built", len(scenes), "scenes;", n, "caption lines;", len(CUES), "sfx; total", TOTAL)
