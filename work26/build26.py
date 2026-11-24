# BeltFlow Lite – Masters guide (1080x1920, 30 fps). -> video/ (HyperFrames project)
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
TIP = f"left:250px;top:1580px;width:580px;padding:22px 30px;border-radius:30px 30px 30px 6px;background:{CARD};color:{PLUM};font-size:38px;font-weight:700;line-height:1.25;box-shadow:0 18px 40px rgba(0,0,0,.4)"
WABUB = lambda title, body: (f'<div style="padding:24px 30px;border-radius:28px 28px 28px 6px;background:#dcf8c6;color:#0b3d2e;box-shadow:0 18px 40px rgba(0,0,0,.4);width:560px">'
                             f'<div style="font-size:28px;font-weight:800;color:#128c7e">{title}</div><div style="font-size:34px;font-weight:700;margin-top:6px;line-height:1.25">{body}</div></div>')
def fly_in(S, eid, t, x0, y0, sc=0.3):
    S.gs(f"#{eid}", {"opacity": 0, "scale": sc, "x": x0, "y": y0, "transformOrigin": "0% 100%"})
    S.tw(f"#{eid}", t, 0.8, {"opacity": 1, "scale": 1, "x": 0, "y": 0}, "back.out(1.5)"); S.sfx(t, "curated/ui-pop.wav", -14)
def counter_chip(S, eid, t, frm, to, total, x=640, y=200, cls="chip am"):
    S.add(eid, f'<span id="{eid}n">{frm}</span>/{total}', f"left:{x}px;top:{y}px;font-size:72px", cls, t, S.dur, "pop")
    S.count(f"{eid}n", t + 0.3, 1.2, to, start=frm)

# ---------------- 01 INTRO ----------------
S = Scene("s01"); scenes.append(S)
S.add("stk", stick_svg(620, 40), "left:230px;top:520px;width:620px;height:40px", "a")
S.gs("#stk", {"rotation": -360}); S.tw("#stk", 0.0, 1.4, {"rotation": 0}, "power3.out")
S.js.append('tl.to("#stk",{rotation:-8,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:2},1.5);'); S.sfx(0.1, "curated/metallic-riser.wav", -22)
S.add("tw0", "BeltFlow", f"left:0;top:620px;width:1080px;text-align:center;font-size:96px;font-weight:800;color:{AMBER}", "a")
S.add("tbf", "Master's Guide", "left:0;top:740px;width:1080px;text-align:center;font-size:132px;font-weight:800;letter-spacing:-3px;line-height:1", "a")
S.ft("#tw0", 0.0, 0.7, {"y": 30}, {"y": 0}, "power3.out"); S.ft("#tbf", 0.0, 0.9, {"scale": 0.9}, {"scale": 1}, "back.out(2)")
S.add("crown", '<svg width="150" height="110" viewBox="0 0 30 22"><path d="M2 20 L4 6 L10 12 L15 2 L20 12 L26 6 L28 20 Z" fill="#ff9e1b" stroke="#fff" stroke-width="1.2" stroke-linejoin="round"/></svg>',
      "left:465px;top:900px", "a", 0.9, None, "pop", ("clean-ding.wav", -20))
S.add("you", "You are the Master!", f"left:0;top:1060px;width:1080px;text-align:center;font-size:58px;font-weight:800", "a", 1.3, None, "up")
for i, col in enumerate(BELTS):
    S.add(f"ib{i}", belt_svg(col, 130), f"left:{75 + i * 160}px;top:1160px", "a", 1.6 + 0.15 * i, None, "pop", ("tick.wav", -26))
M(S, 0.6, "wave"); M(S, S.c("learn"), "cheer")

# ---------------- 02 SIGN IN ----------------
S = Scene("s02"); scenes.append(S); S.step_card(1, "Sign in")
S.phone_on([("a", "01-login-staff-google.png", 1688)], t_in=1.1)
G = ('<div style="width:100%;height:100%;border-radius:40px;border:2px solid #dadce0;background:#fff;display:flex;align-items:center;justify-content:center;gap:12px;font-weight:700;font-size:20px;color:#3c4043">'
     '<svg width="24" height="24" viewBox="0 0 24 24"><path d="M21.6 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3z" fill="#4285F4"/><path d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22z" fill="#34A853"/><path d="M6.4 14a6 6 0 0 1 0-3.9V7.5H3.1a10 10 0 0 0 0 9z" fill="#FBBC05"/><path d="M12 6c1.5 0 2.8.5 3.8 1.5l2.9-2.9A10 10 0 0 0 3.1 7.5l3.3 2.6C7.2 7.8 9.4 6 12 6z" fill="#EA4335"/></svg>'
     'Sign in with Google</div>')
S.ov("a", f'<div id="gbtn" class="a" style="left:{R(110 * K)}px;top:{R(880 * K)}px;width:{R(560 * K)}px;height:{R(86 * K)}px">{G}</div>')
S.push(S.c("staff", -0.2), 551, 749, 1.9); S.hl("a", "h1", (400, 720, 740, 780), S.c("staff"), S.c("google"), r=20)
S.tap("a", "t1", 551, 749, S.w("staff", 1, 0.1))
S.push(S.c("google", -0.2), 390, 923, 1.9, 0.6); S.hl("a", "h2", (100, 872, 680, 974), S.c("google"), S.dur, r=40)
S.tap("a", "t2", 390, 923, S.w("google", 2, 0.1))
S.add("tip", f'<b style="color:{AMBER}">Tip:</b> Use the Gmail<br>you gave the Admin.', TIP, "a", S.c("google", 0.4), S.dur, "pop", ("curated/ui-pop.wav", -20))
M(S, S.c("open"), "point"); M(S, S.w("google", 2, 0.3), "cheer")

# ---------------- 03 HOME ----------------
S = Scene("s03"); scenes.append(S)
S.phone_on([("a", "02b-master-home-full.png", 2216)])
S.hl("a", "h0", (40, 200, 740, 480), S.c("home", 0.2), S.c("classes"))
S.add("hi", 'Vanakkam, Master!', "left:540px;top:200px;font-size:40px", "chip am", S.c("home", 0.4), S.c("classes"), "pop")
S.scroll("a", S.c("classes", -0.5), 1.0, 640); S.hl("a", "h1", (30, 1290, 760, 1530), S.c("classes", 0.3), S.c("pay"))
S.scroll("a", S.c("pay", -0.5), 0.9, 300)
S.hl("a", "h2", (40, 665, 390, 880), S.c("pay", 0.2), S.c("rem"))
S.add("p1", '<span id="p1n">0</span> to check', "left:600px;top:200px;font-size:48px", "chip am", S.c("pay", 0.4), S.c("rem"), "pop"); S.count("p1n", S.c("pay", 0.6), 0.8, 1)
S.hl("a", "h3", (410, 665, 745, 880), S.c("rem", 0.2), S.dur)
S.add("bell", '<svg width="110" height="110" viewBox="0 0 24 24"><path d="M12 3a6 6 0 0 0-6 6v4l-2 3h16l-2-3V9a6 6 0 0 0-6-6z" fill="#ff9e1b" stroke="#1f1435" stroke-width="1.4"/><circle cx="12" cy="19.5" r="2" fill="#ff9e1b" stroke="#1f1435" stroke-width="1.4"/></svg>',
      "left:880px;top:220px", "a", S.c("rem", 0.3), S.dur, "pop")
S.js.append(f'tl.to("#bell",{{rotation:18,duration:0.18,ease:"sine.inOut",yoyo:true,repeat:5,transformOrigin:"50% 10%"}},{R(S.c("rem", 0.8))});')
M(S, S.c("home"), "wave"); M(S, S.c("pay"), "point")

# ---------------- 04 ATTENDANCE ----------------
S = Scene("s04"); scenes.append(S); S.step_card(2, "Attendance")
S.phone_on([("a", "02-master-home.png", 1688), ("b", "03-attendance-today.png", 1688)], t_in=1.1)
S.push(S.c("att", -0.2), 240, 1630, 1.8); S.ring("a", "rg", 240, 1625, S.c("att"), 2, 90); S.tap("a", "t1", 240, 1625, S.w("att", 1, 0.1))
S.swap("a", "b", S.w("att", 1, 0.5), "fade"); S.pull(S.w("att", 1, 0.5))
S.push(S.c("pick", -0.1), 390, 366, 1.8); S.hl("b", "h1", (35, 305, 750, 430), S.c("pick"), S.dur, r=20)
S.tap("b", "t2", 300, 366, S.w("pick", 2, 0.2))
S.add("clk", '19:00 · Kids Class', "left:520px;top:200px;font-size:42px", "chip", S.c("pick", 0.3), S.dur, "pop", ("curated/ui-pop.wav", -20))
M(S, S.c("att"), "point")

# ---------------- 05 STUDENTS ----------------
S = Scene("s05"); scenes.append(S)
S.phone_on([("a", "06b-attendance-full.png", 2766)])
S.ov("a", f'<div id="cover" class="a" style="left:0;top:0;width:500px;height:{R(2766 * K)}px"><img src="assets/screens/04-attendance-class-list.png" style="display:block;width:500px" alt=""></div>')
S.hl("a", "h0", (30, 700, 750, 960), S.c("kids", 0.2), S.c("one"))
S.add("kc", '<span id="kcn">0</span> students', "left:620px;top:200px;font-size:48px", "chip am", S.c("kids", 0.4), S.dur, "pop"); S.count("kcn", S.c("kids", 0.6), 1.0, 5)
S.push(S.c("one", -0.2), 390, 895, 1.9); S.hl("a", "h1", (75, 860, 715, 930), S.c("one"), S.dur, r=18)
S.ring("a", "r1", 154, 895, S.c("one", 0.4), 2, 70); S.ring("a", "r2", 301, 895, S.c("one", 0.8), 2, 70); S.ring("a", "r3", 472, 895, S.c("one", 1.2), 2, 70); S.ring("a", "r4", 635, 895, S.c("one", 1.6), 2, 70)
S.add("ptg", f'<span style="color:{GREEN}">Present</span> · <span style="color:{RED}">Absent</span> · <span style="color:{ORANGE}">Late</span> · Excused', "left:130px;top:1180px;font-size:40px", "chip", S.c("one", 0.6), S.dur, "pop")
M(S, S.c("kids"), "point")

# ---------------- 06 ALL PRESENT ----------------
S = Scene("s06"); scenes.append(S)
S.phone_on([("a", "04-attendance-class-list.png", 1688), ("b", "05-attendance-all-present.png", 1688)])
S.hl("a", "h0", (40, 360, 750, 450), S.c("came", 0.1), S.c("mark", 0.4), r=20)
S.push(S.c("mark", -0.2), 270, 404, 1.9); S.tap("a", "t1", 272, 404, S.w("mark", 1, 0.1))
S.swap("a", "b", S.w("mark", 1, 0.45), "fade")
counter_chip(S, "cc", S.w("mark", 1, 0.4), 0, 5, 5, 620, 200)
S.pull(S.w("mark", 3, 0.3)); S.hl("b", "h1", (60, 700, 740, 1560), S.c("fast"), S.dur)
S.add("fast", f'<span style="font-size:60px">⚡</span> 1 tap!', "left:640px;top:330px;font-size:56px", "chip gr", S.c("fast"), S.dur, "pop", ("clean-ding.wav", -16))
M(S, S.c("came"), "talk"); M(S, S.c("fast"), "cheer")

# ---------------- 07 ABSENT ----------------
S = Scene("s07"); scenes.append(S)
S.phone_on([("a", "05-attendance-all-present.png", 1688), ("b", "06-attendance-absent-reason.png", 1688)])
S.hl("a", "h0", (60, 1010, 740, 1250), S.c("abs", 0.1), S.c("tapabs", 0.4))
S.push(S.c("tapabs", -0.2), 317, 1205, 1.9); S.tap("a", "t1", 317, 1205, S.w("tapabs", 1, 0.1))
S.swap("a", "b", S.w("tapabs", 1, 0.45), "fade")
S.add("ab", "Absent", "left:640px;top:200px;font-size:56px", "chip rd", S.w("tapabs", 1, 0.4), S.dur, "pop")
S.push(S.c("why", -0.2), 390, 1334, 1.9, 0.6); S.hl("b", "h1", (80, 1290, 715, 1380), S.c("why"), S.dur, r=18)
S.ov("b", f'<div id="fv" class="a" style="left:{R(104 * K)}px;top:{R(1310 * K)}px;width:{R(300 * K)}px;height:{R(50 * K)}px;background:#fff8f2;font-size:22px;font-weight:600;color:#1f1435;line-height:{R(50 * K)}px;padding-left:4px">{"".join(f"<span id=fk{i}>{ch}</span>" for i, ch in enumerate("Fever"))}</div>')
for i in range(5):
    S.gs(f"#fk{i}", {"opacity": 0}); S.st(f"#fk{i}", S.w("why", 3, 0.1 * i), {"opacity": 1}); S.sfx(S.w("why", 3, 0.1 * i), "typing-tick.wav", -22)
S.add("thm", '<svg width="80" height="140" viewBox="0 0 16 28"><rect x="5" y="1" width="6" height="20" rx="3" fill="#fff" stroke="#1f1435" stroke-width="1.4"/><circle cx="8" cy="22" r="5" fill="#ef4444" stroke="#1f1435" stroke-width="1.4"/><rect x="6.6" y="8" width="2.8" height="13" fill="#ef4444"/></svg>',
      "left:900px;top:330px", "a", S.w("why", 3, 0.2), S.dur, "pop")
M(S, S.c("abs"), "talk")

# ---------------- 08 SUBMIT ----------------
S = Scene("s08"); scenes.append(S)
S.phone_on([("a", "06-attendance-absent-reason.png", 1688), ("b", "06c-attendance-saved.png", 1688)])
S.push(S.c("submit", -0.2), 416, 1612, 1.7); S.tap("a", "t1", 416, 1612, S.w("submit", 1, 0.1))
S.swap("a", "b", S.w("submit", 1, 0.45), "fade"); S.hl("b", "h1", (35, 1575, 745, 1650), S.w("submit", 1, 0.5), S.c("msg"), r=24)
S.pull(S.c("done", -0.1)); S.burst("ok", 540, 760, S.c("done"))
S.add("msg", WABUB("BeltFlow · to parent", "Bala Kumar was absent today (Fever)."), "left:250px;top:1560px", "a", None, S.dur); fly_in(S, "msg", S.c("msg", 0.2), -150, -550)
M(S, S.c("done"), "cheer")

# ---------------- 09 PAYMENTS ----------------
S = Scene("s09"); scenes.append(S); S.step_card(3, "Check payments")
S.phone_on([("a", "07-payments-to-check.png", 1688)], t_in=1.1)
for i in range(4):
    it = (f'<div style="width:80px;height:100px;border-radius:8px;background:#fff;border:3px solid {PLUM};padding:10px"><div style="height:7px;background:#ccc;margin:7px 0"></div><div style="height:7px;background:#ccc;margin:7px 0"></div><div style="height:7px;background:{AMBER};margin:7px 0"></div></div>'
          if i == 0 else f'<div style="width:64px;height:64px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffe08a,{AMBER});border:3px solid #b86a00;color:#7a3e00;font-size:22px;font-weight:800;display:flex;align-items:center;justify-content:center">RM</div>')
    S.add(f"fly{i}", it, "left:60px;top:260px", "a"); S.gs(f"#fly{i}", {"opacity": 0, "scale": 0.5})
    t0 = S.c("here", 0.3) + 0.2 * i
    S.tw(f"#fly{i}", t0, 0.25, {"opacity": 1, "scale": 1}, "back.out(2)"); S.tw(f"#fly{i}", t0, 1.0, {"x": 380 + 20 * i}, "power1.inOut")
    S.js.append(f'tl.to("#fly{i}",{{y:300,duration:1.0,ease:"back.in(1.1)"}},{R(t0)});'); S.tw(f"#fly{i}", t0 + 0.9, 0.2, {"opacity": 0, "scale": 0.3}, "power2.in"); S.sfx(t0 + 0.95, "tick.wav", -20)
S.hl("a", "h0", (20, 360, 760, 640), S.c("here", 1.2), S.c("view"))
S.push(S.c("view", -0.2), 181, 491, 2.0); S.tap("a", "t1", 181, 491, S.w("view", 1, 0.2))
S.add("rcp", f'''<div style="width:440px;padding:30px 34px;border-radius:18px;background:#fff;color:{PLUM};box-shadow:0 30px 60px rgba(0,0,0,.5)">
  <div style="font-size:26px;font-weight:800;color:#f5b301">Maybank2u</div><div style="font-size:30px;font-weight:800;margin-top:10px">Transfer successful</div>
  <div style="font-size:64px;font-weight:800;margin-top:10px">RM 50.00</div><div style="font-size:24px;opacity:.7;margin-top:8px">To: Ravi a/l Muthu</div><div style="font-size:24px;opacity:.7">Ref: Fee 2026-11 · Arjun</div></div>''',
      "left:320px;top:560px", "a", S.w("view", 1, 0.6), S.c("ack", 0.2), "pop", ("curated/ui-pop.wav", -16))
S.push(S.c("ack", -0.2), 432, 491, 2.0, 0.6); S.tap("a", "t2", 432, 491, S.w("ack", 3, 0.1))
S.ov("a", f'<div id="ackd" class="a" style="left:{R(30 * K)}px;top:{R(370 * K)}px;width:{R(720 * K)}px;height:{R(270 * K)}px;border-radius:14px;background:rgba(236,253,245,.96);border:4px solid {GREEN};display:flex;align-items:center;justify-content:center;gap:14px;color:#065f46;font-weight:800;font-size:30px">'
          f'<span style="width:44px;height:44px;border-radius:50%;background:{GREEN};padding:8px;display:block">{tick_svg()}</span>Paid · RM 50</div>')
S.gs("#ackd", {"opacity": 0, "scale": 0.7}); S.tw("#ackd", S.w("ack", 3, 0.4), 0.5, {"opacity": 1, "scale": 1}, "back.out(2)"); S.tw("#ackd", S.c("rej", -0.3), 0.3, {"opacity": 0}, "power2.in")
S.pull(S.w("ack", 3, 0.6)); S.burst("ok", 540, 1180, S.w("ack", 3, 0.6), 26, tick=False); S.sfx(S.w("ack", 3, 0.6), "clean-ding.wav", -14)
S.push(S.c("rej", -0.2), 141, 592, 2.0, 0.6); S.hl("a", "h2", (80, 560, 200, 625), S.c("rej"), S.dur, r=14)
S.add("rj", "Reject = send back", "left:520px;top:200px;font-size:44px", "chip rd", S.w("rej", 2), S.dur, "pop")
S.add("tip", f'<b style="color:{AMBER}">Cash too!</b><br>Acknowledge cash when you get it.', TIP, "a", S.c("rej", 0.6), S.dur, "pop", ("curated/ui-pop.wav", -20))
M(S, S.c("here"), "point"); M(S, S.w("ack", 3, 0.6), "cheer")

# ---------------- 10 REMINDERS ----------------
S = Scene("s10"); scenes.append(S); S.step_card(4, "Send reminders")
S.phone_on([("a", "08-reminders.png", 1688)], t_in=1.1)
S.hl("a", "h0", (20, 360, 760, 790), S.c("ready", 0.2), S.c("send"))
S.push(S.c("send", -0.2), 152, 737, 2.0); S.tap("a", "t1", 152, 737, S.w("send", 1, 0.1)); S.pull(S.w("send", 1, 0.5))
S.add("wa", WABUB("WhatsApp · Bala's parent", "Bala Kumar was marked absent today."), "left:250px;top:1560px", "a", None, S.dur); fly_in(S, "wa", S.c("wa"), -150, -550)
S.add("snd", f'<div style="width:130px;height:130px;border-radius:50%;background:#25d366;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px rgba(0,0,0,.4)"><svg width="64" height="64" viewBox="0 0 24 24"><path d="M3 20l18-8L3 4l2 7 9 1-9 1z" fill="#fff"/></svg></div>',
      "left:860px;top:1500px", "a", S.c("press", -0.2), S.dur, "pop")
S.add("tf", FINGER, "left:900px;top:1560px;width:120px;height:150px", "a"); S.gs("#tf", {"opacity": 0, "x": 120, "y": 160})
S.tw("#tf", S.c("press", 0.1), 0.5, {"opacity": 1, "x": 0, "y": 0}, "power3.out"); S.tw("#tf", S.w("press", 1, 0.2), 0.12, {"scale": 0.86}, "power2.in"); S.tw("#tf", S.w("press", 1, 0.32), 0.2, {"scale": 1}, "back.out(3)")
S.sfx(S.w("press", 1, 0.32), "curated/ui-click.wav", -12); S.tw("#wa", S.w("press", 1, 0.5), 0.7, {"x": 400, "y": -900, "opacity": 0, "scale": 0.4}, "power2.in"); S.sfx(S.w("press", 1, 0.5), "curated/zoom-swish.wav", -18)
S.add("tip", f'<b style="color:{AMBER}">Emails</b> go out by themselves<br>every evening.', "left:250px;top:200px;width:580px;padding:22px 30px;border-radius:30px 30px 30px 6px;background:#f7f5fa;color:#1f1435;font-size:38px;font-weight:700;line-height:1.25;box-shadow:0 18px 40px rgba(0,0,0,.4)",
      "a", S.c("press", 0.8), S.dur, "pop", ("curated/ui-pop.wav", -20))
M(S, S.c("ready"), "talk"); M(S, S.w("press", 1, 0.5), "cheer")

# ---------------- 11 MORE ----------------
S = Scene("s11"); scenes.append(S); S.step_card(5, "More tools")
S.phone_on([("a", "07-payments-to-check.png", 1688), ("b", "09-more-menu.png", 1688)], t_in=1.1)
S.push(S.c("more", -0.3), 692, 1640, 1.8); S.tap("a", "t1", 692, 1640, S.w("more", 1, 0.1)); S.swap("a", "b", S.w("more", 1, 0.45), "fade"); S.pull(S.w("more", 1, 0.5))
for i, (y0, y1) in enumerate(((365, 600), (705, 920), (1030, 1130))):
    S.hl("b", f"h{i}", (30, y0, 750, y1), S.w("more", 1, 0.9 + 0.5 * i), S.dur)
S.add("tl", "Gradings · Belts · Notices · Profile", "left:120px;top:1180px;font-size:38px", "chip", S.w("more", 1, 1.0), S.dur, "pop")
M(S, S.c("more"), "point")

# ---------------- 12 GRADINGS ----------------
S = Scene("s12"); scenes.append(S)
S.phone_on([("a", "10-gradings.png", 1688)])
S.hl("a", "h0", (40, 250, 740, 1190), S.c("test", 0.1), S.c("tick"))
S.push(S.c("tick", -0.2), 390, 760, 1.45)
for i, (y, t) in enumerate(((604, S.w("tick", 0, 0.3)), (929, S.w("tick", 2, 0.2)))):
    S.ov("a", f'<div id="cb{i}" class="a" style="left:{R(68 * K)}px;top:{R((y - 22) * K)}px;width:{R(44 * K)}px;height:{R(44 * K)}px;border-radius:6px;background:{AMBER};padding:3px">{tick_svg()}</div>')
    S.gs(f"#cb{i}", {"opacity": 0, "scale": 0.3}); S.tw(f"#cb{i}", t, 0.35, {"opacity": 1, "scale": 1}, "back.out(3)"); S.sfx(t, "curated/ui-click.wav", -14)
S.add("blt", f'<div style="display:flex;align-items:center;gap:14px">{belt_svg(BELTS[1], 90)}<span style="font-size:50px">→</span>{belt_svg(BELTS[2], 90)}</div>', "left:560px;top:200px", "chip", S.c("tick", 0.6), S.dur, "pop")
S.push(S.c("nom", -0.3), 388, 1154, 1.8, 0.6); S.tap("a", "t1", 388, 1154, S.w("nom", 1, 0.1)); S.pull(S.w("nom", 1, 0.5))
S.hl("a", "h1", (40, 1240, 740, 1530), S.w("nom", 1, 0.6), S.dur); S.burst("ok", 540, 760, S.w("nom", 1, 0.6))
M(S, S.c("test"), "talk"); M(S, S.w("nom", 1, 0.6), "cheer")

# ---------------- 13 BELTS ----------------
S = Scene("s13"); scenes.append(S)
S.phone_on([("a", "11-belts.png", 1688)])
S.hl("a", "h0", (20, 245, 760, 480), S.c("belts", 0.2), S.c("belts", 1.6))
S.push(S.c("belts", 1.5), 390, 1000, 1.25, 1.2)
for i, col in enumerate(BELTS):
    S.add(f"lb{i}", belt_svg(col, 150), f"left:880px;top:{1180 - i * 170}px", "a", S.c("belts", 0.3 + 0.35 * i), None, "up", ("tick.wav", -22))
S.add("star", f'<svg width="110" height="110" viewBox="0 0 24 24"><path d="M12 2l2.9 6.2 6.8.7-5.1 4.6 1.5 6.7L12 16.8 5.9 20.2l1.5-6.7L2.3 8.9l6.8-.7z" fill="{AMBER}" stroke="#fff" stroke-width="1"/></svg>',
      "left:900px;top:150px", "a", S.c("belts", 2.5), None, "pop", ("clean-ding.wav", -16))
S.js.append(f'tl.to("#star",{{rotation:360,duration:2,ease:"power1.inOut"}},{R(S.c("belts", 2.8))});')
M(S, S.c("belts"), "point")

# ---------------- 14 NOTICES ----------------
S = Scene("s14"); scenes.append(S)
S.phone_on([("a", "12-notices-post.png", 1688)])
S.hl("a", "h0", (40, 250, 740, 1000), S.c("news", 0.1), S.c("write"))
S.push(S.c("write", -0.2), 390, 640, 1.6)
def typ(eid, x, y, w, h, text, t, size=22, rate=0.07):
    S.ov("a", f'<div id="{eid}" class="a" style="left:{R(x * K)}px;top:{R(y * K)}px;width:{R(w * K)}px;height:{R(h * K)}px;font-size:{size}px;font-weight:600;color:#1f1435;line-height:1.3">{"".join(f"<span id={eid}k{i}>{c}</span>" for i, c in enumerate(text))}</div>')
    for i in range(len(text)):
        S.gs(f"#{eid}k{i}", {"opacity": 0}); S.st(f"#{eid}k{i}", t + rate * i, {"opacity": 1})
        if i % 2 == 0: S.sfx(t + rate * i, "typing-tick.wav", -24)
typ("tt", 92, 575, 580, 40, "Belt test on Sunday!", S.c("write", 0.2))
typ("tm", 92, 738, 580, 120, "Come at 8am in uniform.", S.c("write", 1.7), 20, 0.05)
S.push(S.c("post", -0.2), 390, 957, 1.8, 0.6); S.tap("a", "t1", 390, 957, S.w("post", 1, 0.1)); S.pull(S.w("post", 1, 0.5)); S.burst("ok", 540, 760, S.w("post", 1, 0.55))
S.add("ntc", WABUB("New notice", "Belt test on Sunday!"), "left:250px;top:1560px", "a", None, S.dur); fly_in(S, "ntc", S.w("post", 1, 0.8), -150, -550)
M(S, S.c("news"), "talk"); M(S, S.w("post", 1, 0.55), "cheer")

# ---------------- 15 PROFILE ----------------
S = Scene("s15"); scenes.append(S)
S.phone_on([("a", "13b-profile-full.png", 1786)])
S.hl("a", "h0", (30, 300, 750, 560), S.c("classes", 0.2), S.c("bank"))
S.push(S.c("bank", -0.2), 390, 1000, 1.3); S.hl("a", "h1", (40, 590, 740, 1240), S.c("bank", 0.1), S.c("save"))
for i, (y, t) in enumerate(((885, S.w("bank", 2, 0)), (1210, S.w("bank", 5, 0)))):
    S.ring("a", f"bk{i}", 380, y, t, 2, 110)
S.push(S.c("save", -0.3), 391, 1494, 1.8, 0.6); S.tap("a", "t1", 391, 1494, S.w("save", 1, 0.1)); S.pull(S.w("save", 1, 0.5)); S.burst("ok", 540, 760, S.w("save", 1, 0.55))
S.add("pp", f'''<div style="padding:22px 28px;border-radius:22px;background:{PLUM};border:3px solid {AMBER};box-shadow:0 18px 40px rgba(0,0,0,.45);width:520px">
   <div style="font-size:26px;font-weight:800;color:{AMBER}">Parents see · Pay to</div><div style="font-size:32px;font-weight:800;margin-top:6px">Maybank · Ravi a/l Muthu</div>
   <div style="font-size:40px;font-weight:800;margin-top:4px;letter-spacing:2px">1621 2345 6789</div></div>''', "left:270px;top:1560px", "a", None, S.dur)
fly_in(S, "pp", S.c("see", 0.1), -150, -550)
M(S, S.c("classes"), "point"); M(S, S.c("see", 0.3), "cheer")

# ---------------- 16 OUTRO ----------------
S = Scene("s16"); scenes.append(S)
S.add("lg", f'''<svg width="300" height="300" viewBox="0 0 100 100"><g transform="rotate(-35 50 50)"><rect x="8" y="46" width="84" height="8" rx="4" fill="#c98a4b"/></g><g transform="rotate(35 50 50)"><rect x="8" y="46" width="84" height="8" rx="4" fill="#c98a4b"/></g>
   <rect x="22" y="34" width="56" height="12" rx="4" fill="#fff"/><path d="M45 44 L36 66 L43 66 L50 52 L57 66 L64 66 L55 44 Z" fill="#fff"/><rect x="43" y="31" width="14" height="17" rx="3" fill="#fff"/></svg>''', "left:390px;top:260px", "a")
S.gs("#lg", {"opacity": 0, "scale": 0.2, "rotation": -200}); S.tw("#lg", 0.1, 1.1, {"opacity": 1, "scale": 1, "rotation": 0}, "back.out(1.5)")
S.add("ot", "BeltFlow Lite", f"left:0;top:600px;width:1080px;text-align:center;font-size:110px;font-weight:800;color:{AMBER}", "a", 0.4, None, "pop", ("thock.wav", -18))
S.add("os", "PERSATUAN SILAMBAM DAERAH SEPANG", "left:0;top:740px;width:1080px;text-align:center;font-size:36px;font-weight:800;letter-spacing:3px;opacity:.9", "a", 0.7, None, "up")
S.add("url", "beltflow-lite.vercel.app", "left:220px;top:850px;width:640px;text-align:center;font-size:48px", "chip", 1.0, None, "pop", ("curated/ui-pop.wav", -18))
S.add("tm", "Thank you, Master!", f"left:0;top:1010px;width:1080px;text-align:center;font-size:56px;font-weight:800", "a", 1.4, None, "up")
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
STEP_AT = [0] + [SC[s]["start"] for s in ("s02", "s04", "s09", "s10", "s11")]
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
ms_js.append(f'tl.to("#motif",{{opacity:0,duration:0.4}},{R(SC["s16"]["start"])});')
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
KEY = {"Master!", "learn", "Staff.", "Google.", "home.", "classes.", "payments", "reminders", "Attendance.", "class.", "students.", "tap", "came?", "Mark", "present.",
       "fast!", "absent?", "Absent.", "Fever.", "Submit.", "Done!", "message.", "receipts", "View", "Acknowledge.", "Reject.", "ready", "Send.", "WhatsApp", "send!",
       "More", "tools.", "test", "Tick", "Nominate.", "Belts", "learn.", "news?", "notice.", "Post.", "Profile,", "bank", "Save.", "pay!", "Great", "job,", "lucky.", "Vanakkam!"}
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
open("videos/masters.srt", "w").write("\n".join(srt))

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
