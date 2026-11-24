# BeltFlow Lite – Admin Sheet guide. One builder, two layouts: ORIENT=h (1920x1080) or ORIENT=v (1080x1920).
# -> video_h/ or video_v/ (HyperFrames project). Same engine and look as the Parents/Masters guides (work25/26):
# plum gradient bg + amber orbs + stick/belt line-art, stick mascot, word-by-word captions, belt/swipe/zoom/stick transitions.
# Screenshots sit in a laptop frame; the camera pushes in to cells; crisp "magnifier" cards repeat small cell text.
import json, html, math, os, sys
O = os.environ.get("ORIENT", "h")
T = json.load(open("timing.json")); TOTAL = T["total"]; SC = {s["id"]: s for s in T["scenes"]}
PLUM, PLUM2, AMBER, CARD, GREEN, RED = "#1f1435", "#120a21", "#ff9e1b", "#f7f5fa", "#10b981", "#ef4444"
BELTS = ["#ffffff", "#facc15", "#f97316", "#16a34a", "#2563eb", "#111111"]
R = lambda v: round(v, 3); esc = html.escape
if O == "h":
    W, H = 1920, 1080
    LAY = dict(LX=410, LY=66, LW=1100, FX=960, FY=300, mag=(470, 430, 980), tip=(1556, 150, 340), chip=(1560, 520), mas=(70, 500),
               cap=(300, 768, 1320, 170, 54), tm="row", tmy=966, CY=330, big=1)
else:
    W, H = 1080, 1920
    LAY = dict(LX=40, LY=560, LW=1000, FX=540, FY=780, mag=(40, 180, 760), tip=(40, 1735, 1000), chip=(40, 400), mas=(895, 24),
               cap=(50, 1210, 980, 250, 64), tm="grid", tmy=1490, CY=640, big=1)
LX, LY, LW = LAY["LX"], LAY["LY"], LAY["LW"]; K = LW / 800; LH = 465 * K; BZ = 16; FX, FY = LAY["FX"], LAY["FY"]
OUT = f"video_{O}"; os.makedirs(f"{OUT}/compositions", exist_ok=True)
CUES = []
FONT = '"Jakarta", "Inter", sans-serif'
TABS = ["Config", "Belts", "Masters", "Classes", "Students", "Enrolments", "Parents", "Access"]
APP_TABS = ["Fees", "Gradings", "Attendance", "Notices"]

CSS = f'''
@font-face {{ font-family:"Jakarta"; font-weight:400; src:url("assets/fonts/plus-jakarta-sans-latin-400-normal.woff2") format("woff2"); }}
@font-face {{ font-family:"Jakarta"; font-weight:700; src:url("assets/fonts/plus-jakarta-sans-latin-700-normal.woff2") format("woff2"); }}
@font-face {{ font-family:"Jakarta"; font-weight:800; src:url("assets/fonts/plus-jakarta-sans-latin-800-normal.woff2") format("woff2"); }}
#root {{ position:absolute; inset:0; font-family:{FONT}; color:#fff; overflow:hidden; }}
.a {{ position:absolute; }}
.cam {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; transform-origin:0 0; }}
.lap {{ position:absolute; left:{LX - BZ}px; top:{LY - BZ}px; width:{R(LW + 2 * BZ)}px; height:{R(LH + 2 * BZ)}px; border-radius:22px; background:linear-gradient(160deg,#3a2d55,#0d0718);
  box-shadow:0 40px 90px rgba(0,0,0,.55), inset 0 0 0 3px rgba(255,255,255,.12); }}
.base {{ position:absolute; left:{R(LX - 0.1 * LW)}px; top:{R(LY + LH + BZ)}px; width:{R(1.2 * LW)}px; height:26px; border-radius:0 0 26px 26px;
  background:linear-gradient(#5a4a78,#241a38); clip-path:polygon(2% 0,98% 0,100% 100%,0 100%); box-shadow:0 20px 40px rgba(0,0,0,.5); }}
.scr {{ position:absolute; left:{BZ}px; top:{BZ}px; width:{R(LW)}px; height:{R(LH)}px; border-radius:8px; overflow:hidden; background:#fff; }}
.ly {{ position:absolute; left:0; top:0; width:{R(LW)}px; height:{R(LH)}px; }}
.ly > img {{ display:block; width:{R(LW)}px; height:{R(LH)}px; }}
.hl {{ position:absolute; border:{R(3 * K / 1.375)}px solid {AMBER}; border-radius:6px; box-shadow:0 0 0 3000px rgba(18,10,33,.5), 0 0 14px rgba(255,158,27,.9); }}
.pulse {{ position:absolute; border:4px solid {AMBER}; border-radius:50%; }}
.chip {{ position:absolute; padding:16px 28px; border-radius:30px; background:{CARD}; color:{PLUM}; font-weight:800; font-size:40px; box-shadow:0 18px 40px rgba(0,0,0,.4); white-space:nowrap; }}
.chip.am {{ background:{AMBER}; color:{PLUM2}; }} .chip.gr {{ background:{GREEN}; color:#fff; }} .chip.rd {{ background:{RED}; color:#fff; }}
.mag {{ position:absolute; padding:22px 32px; border-radius:22px; background:#fff; color:#202124; box-shadow:0 24px 60px rgba(0,0,0,.55); border:5px solid {AMBER}; }}
.mag .k {{ font-size:28px; font-weight:800; color:#b45f00; letter-spacing:1px; }}
.mag .v {{ font-family:Roboto, Arial, sans-serif; font-size:{56 if O == "h" else 50}px; font-weight:500; margin-top:6px; line-height:1.15; }}
.tip {{ position:absolute; padding:20px 28px; border-radius:26px 26px 26px 6px; background:{CARD}; color:{PLUM}; font-weight:700; font-size:{34 if O == "h" else 36}px; line-height:1.25; box-shadow:0 18px 40px rgba(0,0,0,.4); }}
.ty {{ position:absolute; background:#fff; color:#202124; font-family:Arial, Roboto, sans-serif; font-size:{R(8.6 * K)}px; line-height:{R(15 * K)}px; padding-left:{R(2 * K)}px; white-space:nowrap; overflow:visible; }}
.ty .cur {{ display:inline-block; width:{max(1, R(K))}px; height:{R(11 * K)}px; background:#202124; vertical-align:middle; margin-left:1px; }}
.glow {{ position:absolute; border-radius:{R(3 * K)}px; background:rgba(255,158,27,.35); box-shadow:0 0 0 {R(1.6 * K)}px {AMBER}, 0 0 16px rgba(255,158,27,.9); }}
'''

FINGER = '''<svg width="100%" height="100%" viewBox="0 0 60 75"><path d="M22 4c3 0 5 2 5 5v20l3-1c3-1 5 1 6 3l1 3 3-1c3 0 5 2 5 4l1 2 3-1c3 0 5 2 5 5v14c0 10-8 18-18 18h-4c-6 0-11-3-14-8L4 47c-2-3-1-6 2-7 2-1 5 0 6 2l5 6V9c0-3 2-5 5-5z"
 fill="#fff7ec" stroke="#1f1435" stroke-width="2.6" stroke-linejoin="round"/></svg>'''
def tick_svg(col="#fff"):
    return f'<svg viewBox="0 0 24 24" width="100%" height="100%"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="{col}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def belt_svg(col, w=170):
    h = w * 0.55; s = "#2a1f3d"
    return (f'<svg width="{w}" height="{R(h)}" viewBox="0 0 100 55"><rect x="2" y="12" width="96" height="16" rx="5" fill="{col}" stroke="{s}" stroke-width="2.4"/>'
            f'<path d="M44 20 L30 52 L40 52 L50 30 L60 52 L70 52 L56 20 Z" fill="{col}" stroke="{s}" stroke-width="2.4" stroke-linejoin="round"/><rect x="41" y="9" width="18" height="22" rx="4" fill="{col}" stroke="{s}" stroke-width="2.4"/></svg>')
def stick_svg(w=520, h=34):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><linearGradient id="sg{w}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c98a4b"/><stop offset="1" stop-color="#7a4b22"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="{h / 2}" fill="url(#sg{w})"/><rect x="{w * 0.08}" y="0" width="{h * 0.9}" height="{h}" fill="{AMBER}"/><rect x="{w * 0.92 - h * 0.9}" y="0" width="{h * 0.9}" height="{h}" fill="{AMBER}"/></svg>')
SHEET_ICON = '<svg width="100%" height="100%" viewBox="0 0 24 24"><rect x="3" y="2" width="18" height="20" rx="3" fill="#0f9d58"/><rect x="6" y="7" width="12" height="11" fill="#fff"/><path d="M6 10.6h12M6 14.3h12M10 7v11" stroke="#0f9d58" stroke-width="1.3"/></svg>'

# ---- tab map geometry (shared by the persistent strip and arrows) ----
def tab_rects():
    r = {}
    if LAY["tm"] == "row":
        x = 70; y = LAY["tmy"]
        for i, t in enumerate(TABS): w = 150 if t not in ("Enrolments",) else 176; r[t] = (x, y, w, 64); x += w + 10
        x += 56
        for t in APP_TABS: w = 108 if t != "Attendance" else 136; r[t] = (x, y + 8, w, 48); x += w + 8
    else:
        y = LAY["tmy"]
        for i, t in enumerate(TABS): r[t] = (50 + (i % 4) * 248, y + (i // 4) * 80, 236, 64)
        x = 230
        for t in APP_TABS: w = 160 if t != "Attendance" else 196; r[t] = (x, y + 172, w, 50); x += w + 10
    return r
TR = tab_rects()
def tab_center(t): x, y, w, h = TR[t]; return (x + w / 2, y)


class Scene:
    def __init__(s, sid):
        sc = SC[sid]; s.id = sid; s.dur = sc["dur"]; s.start = sc["start"]
        s.L = {l["cue"]: l for l in sc["lines"]}; s.els, s.js, s.init, s.layers, s.lap = [], [], [], [], False
        s.cam_state = (1, 0, 0)

    def c(s, cue, d=0.0): return R(s.L[cue]["t0"] + d)
    def e(s, cue, d=0.0): return R(s.L[cue]["t1"] + d)
    def w(s, cue, i, d=0.0): return R(s.L[cue]["words"][i]["s"] + d)
    def props(s, p): return ",".join(f"{k}:{json.dumps(v)}" for k, v in p.items())
    def tw(s, sel, t, d, p, ease="power3.out"): s.js.append(f'tl.to("{sel}",{{{s.props(p)},duration:{R(d)},ease:"{ease}"}},{R(max(0, t))});')
    def ft(s, sel, t, d, p0, p1, ease="power3.out"): s.js.append(f'tl.fromTo("{sel}",{{{s.props(p0)}}},{{{s.props(p1)},duration:{R(d)},ease:"{ease}",immediateRender:false}},{R(max(0, t))});')
    def st(s, sel, t, p): s.js.append(f'tl.set("{sel}",{{{s.props(p)}}},{R(max(0, t))});')
    def gs(s, sel, p): s.init.append(f'gsap.set("{sel}",{{{s.props(p)}}});')
    def sfx(s, t, f, g): CUES.append((R(s.start + max(0, t)), f, g))

    def add(s, eid, inner, style="", cls="a", t_in=None, t_out=None, enter="pop", sfx=None):
        s.els.append(f'<div id="{eid}" class="{cls}" style="{style}">{inner}</div>')
        if t_in is not None:
            fr = {"pop": {"opacity": 0, "scale": 0.4}, "up": {"opacity": 0, "y": 60}, "down": {"opacity": 0, "y": -60}, "left": {"opacity": 0, "x": -120},
                  "right": {"opacity": 0, "x": 120}, "fade": {"opacity": 0}}[enter]
            s.gs(f"#{eid}", fr); to = {k: (1 if k in ("opacity", "scale") else 0) for k in fr}
            s.tw(f"#{eid}", t_in, 0.6, to, "back.out(2.2)" if enter == "pop" else "power3.out")
            if sfx: s.sfx(t_in, *sfx)
        if t_out is not None:
            s.tw(f"#{eid}", t_out - 0.35, 0.35, {"opacity": 0, "scale": 0.8} if enter == "pop" else {"opacity": 0}, "power2.in")

    # ---------- laptop ----------
    def laptop(s, layers, t_in=None):
        """layers: [(id, src under assets/)] stacked bottom->top; later ones start hidden unless shown with show()"""
        s.lap = True; s.lys = layers; s.ov = {lid: [] for lid, _ in layers}
        for i, (lid, src) in enumerate(layers):
            if i: s.gs(f"#L{lid}", {"opacity": 0})
        if t_in is None:
            s.gs("#lapw", {"scale": 0.97, "transformOrigin": "50% 50%"}); s.tw("#lapw", 0.05, 0.8, {"scale": 1}, "back.out(1.6)")
        else:
            s.gs("#lapw", {"y": H * 0.9, "rotationX": 30, "rotationY": -20, "rotationZ": -5, "transformPerspective": 2200, "opacity": 0})
            s.tw("#lapw", t_in, 1.1, {"y": 0, "rotationX": 0, "rotationY": 0, "rotationZ": 0, "opacity": 1}, "back.out(1.1)"); s.sfx(t_in, "curated/zoom-swish.wav", -20)
        f0 = (t_in or 0) + 1.2; n = max(1, int((s.dur - f0) / 2.6))
        s.js.append(f'tl.to("#flt",{{y:-10,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{2 * n - 1}}},{R(f0)});')

    def show(s, lid, t, d=0.5): s.tw(f"#L{lid}", t, d, {"opacity": 1}, "power2.inOut")
    def P(s, px, py): return (LX + px * K, LY + py * K)          # screenshot px -> stage px (camera at rest)

    def push(s, t, px, py, Z=2.0, d=0.9):
        sx, sy = s.P(px, py); x, y = R(FX - Z * sx), R(FY - Z * sy); s.cam_state = (Z, x, y)
        s.tw("#cam", t, d, {"scale": Z, "x": x, "y": y}, "power3.inOut"); s.sfx(t, "curated/zoom-swish.wav", -26)
    def pull(s, t, d=0.8): s.tw("#cam", t, d, {"scale": 1, "x": 0, "y": 0}, "power3.inOut")
    def stage_at(s, px, py, Z, cx, cy):                            # where a screenshot point sits on stage under a given camera
        sx, sy = s.P(px, py); return (cx + Z * sx, cy + Z * sy)

    def o(s, lid, html_): s.ov[lid].append(html_)
    def hl(s, lid, rid, box, t_in, t_out, pad=2):
        x0, y0, x1, y1 = box
        s.o(lid, f'<div id="{rid}" class="hl" style="left:{R(x0 * K - pad * K)}px;top:{R(y0 * K - pad * K)}px;width:{R((x1 - x0 + 2 * pad) * K)}px;height:{R((y1 - y0 + 2 * pad) * K)}px"></div>')
        s.gs(f"#{rid}", {"opacity": 0, "scale": 1.25}); s.tw(f"#{rid}", t_in, 0.55, {"opacity": 1, "scale": 1}, "back.out(1.8)")
        s.tw(f"#{rid}", t_out - 0.3, 0.3, {"opacity": 0}, "power2.in"); s.sfx(t_in, "curated/ui-pop.wav", -24)

    def tap(s, lid, rid, px, py, t, size=34):
        cx, cy = px * K, py * K; fs = size * K
        s.o(lid, f'<div id="{rid}r" class="pulse" style="left:{R(cx - fs * .35)}px;top:{R(cy - fs * .35)}px;width:{R(fs * .7)}px;height:{R(fs * .7)}px;border-width:{R(2 * K)}px"></div>'
                 f'<div id="{rid}" class="a" style="left:{R(cx - fs * .28)}px;top:{R(cy - fs * .07)}px;width:{R(fs)}px;height:{R(fs * 1.25)}px;filter:drop-shadow(0 4px 6px rgba(0,0,0,.35))">{FINGER}</div>')
        s.gs(f"#{rid}", {"opacity": 0, "x": R(fs), "y": R(fs * 1.3), "transformOrigin": "30% 10%"}); s.gs(f"#{rid}r", {"opacity": 0, "scale": 0.3})
        s.tw(f"#{rid}", t - 0.75, 0.6, {"opacity": 1, "x": 0, "y": 0}, "power3.out")
        s.tw(f"#{rid}", t - 0.12, 0.12, {"scale": 0.86}, "power2.in"); s.tw(f"#{rid}", t, 0.25, {"scale": 1}, "back.out(3)")
        s.ft(f"#{rid}r", t, 0.7, {"opacity": 1, "scale": 0.3}, {"opacity": 0, "scale": 2.6}, "power2.out")
        s.tw(f"#{rid}", t + 0.9, 0.45, {"opacity": 0, "x": R(fs * .8), "y": R(fs)}, "power2.in"); s.sfx(t, "curated/ui-click.wav", -12)

    def typing(s, lid, tid, box, text, t0, rate=0.075, mag=None):
        """letter-by-letter text over a cell (box in screenshot px), blinking cursor; optional matching magnifier card"""
        x0, y0, x1, y1 = box
        chars = "".join(f'<span id="{tid}k{i}" style="display:none">{esc(c)}</span>' for i, c in enumerate(text))
        s.o(lid, f'<div id="{tid}" class="ty" style="left:{R(x0 * K)}px;top:{R(y0 * K)}px;width:{R((x1 - x0) * K)}px;height:{R((y1 - y0) * K)}px">{chars}<span id="{tid}c" class="cur"></span></div>')
        s.gs(f"#{tid}", {"opacity": 0}); s.st(f"#{tid}", t0 - 0.2, {"opacity": 1})
        for i in range(len(text)):
            s.st(f"#{tid}k{i}", t0 + i * rate, {"display": "inline"})
            if text[i] != " ": s.sfx(t0 + i * rate, "typing-tick.wav", -23)
        tend = t0 + len(text) * rate
        n = int((tend - t0 + 0.3) / 0.25)
        s.js.append(f'tl.to("#{tid}c",{{opacity:0,duration:0.25,ease:"steps(1)",yoyo:true,repeat:{max(1, n)}}},{R(t0 - 0.2)});')
        s.st(f"#{tid}c", tend + 0.6, {"opacity": 0})
        if mag:
            s.magcard(f"m{tid}", mag[0], text, t0 - 0.3, mag[1], typed=(t0, rate))
        return tend

    def magcard(s, mid, key, val, t_in, t_out, typed=None, slot=None):
        x, y, w = slot or LAY["mag"]
        if typed:
            t0, rate = typed
            v = "".join(f'<span id="{mid}k{i}" style="display:none">{esc(c)}</span>' for i, c in enumerate(val)) + f'<span id="{mid}c" style="display:inline-block;width:4px;height:0.95em;background:#202124;vertical-align:-0.1em;margin-left:3px"></span>'
            for i in range(len(val)): s.st(f"#{mid}k{i}", t0 + i * rate, {"display": "inline"})
            n = int((len(val) * rate + 0.6) / 0.25); s.js.append(f'tl.to("#{mid}c",{{opacity:0,duration:0.25,ease:"steps(1)",yoyo:true,repeat:{max(1, n)}}},{R(t0)});')
        else: v = val
        s.add(mid, f'<div class="k">{esc(key)}</div><div class="v">{v}</div>', f"left:{x}px;top:{y}px;width:{w}px", "mag", t_in, t_out, "pop", ("curated/ui-pop.wav", -20))

    def popup(s, lid, pid, src, box, t, items=None):
        """dropdown list (cropped from the real screenshot) pops open under its cell with a bounce"""
        x0, y0, x1, y1 = box
        s.o(lid, f'<div id="{pid}" class="a" style="left:{R(x0 * K)}px;top:{R(y0 * K)}px;width:{R((x1 - x0) * K)}px;height:{R((y1 - y0) * K)}px;box-shadow:0 6px 18px rgba(0,0,0,.25)">'
                 f'<img src="assets/sheets/gen/{src}" style="display:block;width:100%;height:100%" alt=""></div>')
        s.gs(f"#{pid}", {"opacity": 0, "scaleY": 0.2, "transformOrigin": "50% 0%"}); s.tw(f"#{pid}", t, 0.55, {"opacity": 1, "scaleY": 1}, "back.out(2)"); s.sfx(t, "curated/ui-pop.wav", -16)

    def glow(s, lid, gid, box, t, t_out=None):
        x0, y0, x1, y1 = box
        s.o(lid, f'<div id="{gid}" class="glow" style="left:{R(x0 * K)}px;top:{R(y0 * K)}px;width:{R((x1 - x0) * K)}px;height:{R((y1 - y0) * K)}px"></div>')
        s.gs(f"#{gid}", {"opacity": 0}); s.tw(f"#{gid}", t, 0.3, {"opacity": 1}, "power2.out")
        rep = 3 if not t_out else max(0, min(3, int((t_out - 0.35 - (t + 0.35)) / 0.35) - 1))
        rep = rep if rep % 2 else rep - 1
        if rep > 0: s.js.append(f'tl.to("#{gid}",{{opacity:0.45,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:{rep}}},{R(t + 0.35)});')
        if t_out: s.tw(f"#{gid}", t_out - 0.3, 0.3, {"opacity": 0})
        s.sfx(t, "clean-ding.wav", -20)

    def tip(s, tid, html_, t_in, t_out=None, slot=None):
        x, y, w = slot or LAY["tip"]
        s.add(tid, html_, f"left:{x}px;top:{y}px;width:{w}px", "tip", t_in, t_out, "pop", ("curated/ui-pop.wav", -20))

    def chip(s, cid, html_, t_in, t_out=None, cls="chip am", slot=None, size=40):
        x, y = slot or LAY["chip"]
        pos = f"right:40px;top:{y}px" if (O == "h" and slot is None) else f"left:{x}px;top:{y}px"
        s.add(cid, html_, f"{pos};font-size:{size}px", cls, t_in, t_out, "pop")

    def arrow(s, aid, p0, p1, t, t_out=None, bend=-0.25, col=AMBER):
        """self-drawing curved arrow between two stage points"""
        (x0, y0), (x1, y1) = p0, p1; mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dx, dy = x1 - x0, y1 - y0
        cx, cy = mx - dy * bend, my + dx * bend
        ang = math.atan2(y1 - cy, x1 - cx); hs = 26
        hp = f"{x1},{y1} {R(x1 - hs * math.cos(ang - 0.45))},{R(y1 - hs * math.sin(ang - 0.45))} {R(x1 - hs * math.cos(ang + 0.45))},{R(y1 - hs * math.sin(ang + 0.45))}"
        s.add(aid, f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0;overflow:visible"><path id="{aid}p" pathLength="1" d="M{R(x0)},{R(y0)} Q{R(cx)},{R(cy)} {R(x1)},{R(y1)}" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="butt" stroke-dasharray="1" stroke-dashoffset="1" style="filter:drop-shadow(0 0 8px rgba(255,158,27,.8))"/>'
                   f'<polygon id="{aid}h" points="{hp}" fill="{col}"/></svg>', f"left:0;top:0;width:{W}px;height:{H}px;z-index:30", "a", None, t_out)
        s.gs(f"#{aid}h", {"opacity": 0}); s.gs(f"#{aid}p", {"opacity": 0}); s.st(f"#{aid}p", t, {"opacity": 1}); s.tw(f"#{aid}p", t, 0.8, {"strokeDashoffset": 0}, "power2.inOut"); s.tw(f"#{aid}h", t + 0.7, 0.2, {"opacity": 1}); s.sfx(t, "curated/zoom-swish.wav", -24)

    def burst(s, eid, x, y, t, n=26, tick=True):
        cols = [AMBER, "#ffd166", GREEN, "#60a5fa", "#f472b6", "#fff"]
        if tick:
            s.add(f"{eid}tk", f'<div style="width:140px;height:140px;border-radius:50%;background:{GREEN};padding:22px;box-shadow:0 0 0 14px rgba(16,185,129,.25)">{tick_svg()}</div>', f"left:{x - 70}px;top:{y - 70}px", "a")
            s.gs(f"#{eid}tk", {"opacity": 0, "scale": 0.2}); s.tw(f"#{eid}tk", t, 0.55, {"opacity": 1, "scale": 1}, "back.out(2.6)"); s.tw(f"#{eid}tk", t + 1.6, 0.4, {"opacity": 0, "scale": 0.6}, "power2.in")
        for i in range(n):
            a = 2 * math.pi * i / n + 0.3 * math.sin(i * 7.1); dist = 170 + 90 * ((i * 37) % 10) / 10; w_, h_ = (14, 22) if i % 3 else (16, 16)
            s.add(f"{eid}c{i}", "", f"left:{x}px;top:{y}px;width:{w_}px;height:{h_}px;border-radius:{50 if i % 3 == 0 else 3}%;background:{cols[i % 6]}", "a")
            s.gs(f"#{eid}c{i}", {"opacity": 0})
            s.ft(f"#{eid}c{i}", t + 0.05, 0.7, {"opacity": 1, "x": 0, "y": 0, "rotation": 0}, {"opacity": 1, "x": R(math.cos(a) * dist), "y": R(math.sin(a) * dist - 40), "rotation": 220 + i * 13}, "power3.out")
            s.tw(f"#{eid}c{i}", t + 0.75, 0.9, {"y": R(math.sin(a) * dist + 120), "opacity": 0}, "power1.in")
        s.sfx(t, "clean-ding.wav", -12); s.sfx(t + 0.05, "sparkle.wav", -20)

    def tab_card(s, n, label):
        txt = f"Tab {n}" if n else "App tabs"
        s.add("tbc", f'''<div class="a" style="left:0;top:{R(H * 0.3)}px;width:{W}px;text-align:center;font-weight:800;font-size:{56 if O == "h" else 60}px;color:{AMBER};letter-spacing:8px">{txt.upper()}</div>
          <div class="a" style="left:{R(W / 2 - 60)}px;top:{R(H * 0.3 + 90)}px;width:120px;height:120px">{SHEET_ICON}</div>
          <div class="a" style="left:0;top:{R(H * 0.3 + 240)}px;width:{W}px;text-align:center;font-weight:800;font-size:{110 if O == "h" else 96}px">{esc(label)}</div>''',
              f"left:0;top:0;width:{W}px;height:{H}px;background:radial-gradient(70% 55% at 50% 42%, #3a2463, {PLUM} 70%)", "a")
        s.gs("#tbc", {"opacity": 0, "scale": 1.08}); s.tw("#tbc", 0.0, 0.35, {"opacity": 1, "scale": 1}, "power2.out"); s.sfx(0.1, "tick.wav", -18)
        s.tw("#tbc", 1.1, 0.4, {"xPercent": -100, "opacity": 0.3}, "power3.in"); s.sfx(1.1, "curated/zoom-swish.wav", -22)

    def write(s):
        lapd = ""
        if s.lap:
            lys = "".join(f'<div id="L{lid}" class="ly" style="z-index:{i + 1}"><img src="assets/{src}" alt="">{"".join(s.ov[lid])}</div>' for i, (lid, src) in enumerate(s.lys))
            lapd = (f'<div id="cam" class="cam"><div id="flt" class="a" style="left:0;top:0;width:{W}px;height:{H}px"><div id="lapw" class="a" style="left:0;top:0;width:{W}px;height:{H}px">'
                    f'<div class="base"></div><div class="lap"><div class="scr">{lys}</div></div></div></div></div>')
        open(f"{OUT}/compositions/{s.id}.html", "w").write(f'''<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{s.id}" data-width="{W}" data-height="{H}">
    {lapd}
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


scenes = []; MASCOT = []; TAB_ON = []          # (abs t, action) ; (abs t, tab name, state)
def M(S, t, act): MASCOT.append((R(S.start + t), act))
def TAB(S, t, name, state="on"): TAB_ON.append((R(S.start + t), name, state))
SH = lambda n: f"sheets/{n}.jpg"; GN = lambda n: f"sheets/gen/{n}"
exec(open("scenes27.py").read())

for S in scenes: S.write()
exec(open("layers27.py").read())
