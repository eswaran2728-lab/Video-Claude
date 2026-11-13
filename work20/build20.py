# Partner-briefing video builder (HyperFrames). Usage: python3 build20.py v1_foca
# Layout (1920x1080): the ORIGINAL slide (3840 px export) on a 1440x810 stage at (240,70) with a camera (full slide first, then
# zoom into one panel at a time); rings/highlights live in slide coordinates inside the camera so they stay on the real buttons.
# Top row: form code + stage label. Below the stage: who has the phone (blue Security / orange next signer, role name in text),
# scene title or plain-text callout. Bottom band: captions (max 2 lines), also written as <export>.srt.
# The plan for each video (plan_<v>.py) places shots / rings / motion graphics on the voiceover's sentence and word times.
import json, sys, html, re, os, shutil, importlib, subprocess
import numpy as np, soundfile as sf, scipy.signal as ss
import scripts20
v = sys.argv[1]; VER = os.environ.get("VER", "v01"); D = (scripts20.VIDEOS2 if VER == "v02" else scripts20.VIDEOS)[v]; O = v if VER == "v01" else f"{v}/{VER}"
PL = importlib.import_module(f"plan_{v}" if VER == "v01" else f"plan2_{v}")
T = json.load(open(f"{O}/timing.json")); R = lambda x: round(float(x), 3); esc = html.escape
BLUE, ORANGE, INK, BG, AMBER, GREEN, RED = "#0b57d0", "#b8550d", "#1a1a1d", "#16161a", "#ffb000", "#188038", "#c8102e"
SX, SY, SW, SH = 240, 70, 1440, 810; BASE = SW / 1920

# ---------- layout with read holds ----------
HOLDS = getattr(PL, "HOLDS", {}); END = getattr(PL, "END_HOLD", 0.0)
for (n_, j_), sec_ in getattr(PL, "HOLDS_S", {}).items():                 # v02 plans give holds per (slide, sentence on that slide)
    HOLDS = dict(HOLDS); HOLDS[[l for l in T["lines"] if l.get("slide") == n_][j_]["i"]] = sec_
shift, acc = {}, 0.0
for l in T["lines"]: shift[l["i"]] = acc; acc += HOLDS.get(l["i"], 0.0)
LINES = []
for l in T["lines"]:
    s = shift[l["i"]]; LINES.append(dict(l, t0=R(l["t0"] + s), t1=R(l["t1"] + s), words=[dict(w, t=R(w["t"] + s), e=R(w["e"] + s)) for w in l["words"]]))
TOTAL = R(T["total"] + acc + END)
NS = len(D["scenes"]); first = [next(l for l in LINES if l["scene"] == k) for k in range(NS)]
PRE = getattr(PL, "PRE", {})
SCN = [(0.0 if k == 0 else R(first[k]["t0"] - PRE.get(k, 0.45))) for k in range(NS)]; SCN_END = SCN[1:] + [TOTAL]


SHAPES = {x["n"]: x["shapes"] for x in json.load(open(f"{v}/shapes.json"))}


class Plan:
    total = TOTAL
    def txt(s, slide, sub):
        d = next(d for d in SHAPES[slide] if d["kind"] != "pic" and sub.lower() in d.get("t", "").lower()); return (d["x"], d["y"], d["w"], d["h"])
    def L(s, i, d=0.0): return R(LINES[i]["t0"] + d)
    def E(s, i, d=0.0): return R(LINES[i]["t1"] + d)
    def W(s, i, word, k=0, d=0.0):
        hits = [w for w in LINES[i]["words"] if w["w"] == word.lower()]
        return R((hits[k]["t"] if len(hits) > k else LINES[i]["t0"]) + d)
    def S(s, k): return SCN[k]
    def sl(s, n, j=0): return [l["i"] for l in LINES if l.get("slide") == n][j]          # global line index of the j-th sentence on slide n
    def nsl(s, n): return sum(1 for l in LINES if l.get("slide") == n)
    def A(s, n, d=0.0): return s.L(s.sl(n), d)                                         # first sentence on slide n starts
    def Z(s, n, d=0.0): return s.E(s.sl(n, -1), d)                                     # last sentence on slide n ends
    def Wn(s, n, j, word, k=0, d=0.0): return s.W(s.sl(n, j), word, k, d)
    def Se(s, k): return SCN_END[k]


P = Plan()
SCENE_EL = [dict(els=[], js=[], init=[]) for _ in range(NS)]; CH = dict(els=[], js=[], init=[]); CUES = []; UID = [0]


def uid(p): UID[0] += 1; return f"{p}{UID[0]}"
def scene_of(t): return max(k for k in range(NS) if SCN[k] <= t + 1e-6)
def J(B, sel, t, d, props, ease="power3.out", base=0.0):
    B["js"].append(f'tl.to("{sel}",{{{",".join(f"{k}:{json.dumps(x)}" for k, x in props.items())},duration:{R(d)},ease:"{ease}"}},{R(t - base)});')
def SET(B, sel, t, props, base=0.0): B["js"].append(f'tl.set("{sel}",{{{",".join(f"{k}:{json.dumps(x)}" for k, x in props.items())}}},{R(t - base)});')
def INIT(B, sel, props): B["init"].append(f'gsap.set("{sel}",{{{",".join(f"{k}:{json.dumps(x)}" for k, x in props.items())}}});')


def cam_tf(cx, cy, w):
    z = 1920 / w; s = BASE * z; x = SW / 2 - cx * s; y = SH / 2 - cy * s
    x = min(0, max(SW - 1920 * s, x)); y = min(0, max(SH - 1080 * s, y)); return dict(x=R(x), y=R(y), scale=R(s))


def fit(x, y, w, h, pad=1.35, wmin=420):
    return (x + w / 2, y + h / 2, max(wmin, w * pad, h * pad * 16 / 9))


class Shot:
    """an original slide on the stage, visible [t0, t1)"""
    def __init__(s, slide, t0, t1, fade=0.35):
        s.k = scene_of(t0); s.B = SCENE_EL[s.k]; s.base = SCN[s.k]; s.id = uid("sh"); s.t0, s.t1 = t0, t1; s.inner = []
        s.slide = slide; s.fade = fade; s.cams = []
    def cam(s, t, cx, cy, w, d=0.9): s.cams.append((t, cx, cy, w, d)); return s
    def camfit(s, t, rect, d=0.9, pad=1.35, wmin=420): cx, cy, w = fit(*rect, pad=pad, wmin=wmin); return s.cam(t, cx, cy, w, d)
    def ring(s, t, rect, t_end=None, color=AMBER, round_=False, sfx=True):
        x, y, w, h = rect; rid = uid("rg")
        s.inner.append(f'<div id="{rid}" class="ring" style="left:{R(x - 9)}px;top:{R(y - 9)}px;width:{R(w + 18)}px;height:{R(h + 18)}px;border-color:{color};'
                       f'border-radius:{"999px" if round_ else "14px"};box-shadow:0 0 0 7px {color}55, 0 0 26px {color}"></div>')
        INIT(s.B, f"#{rid}", {"opacity": 0, "scale": 1.3, "transformOrigin": "50% 50%"})
        J(s.B, f"#{rid}", t, 0.35, {"opacity": 1, "scale": 1}, "back.out(1.8)", s.base)
        for k in range(2): J(s.B, f"#{rid}", t + 0.45 + 0.7 * k, 0.3, {"scale": 1.07}, "sine.inOut", s.base); J(s.B, f"#{rid}", t + 0.75 + 0.7 * k, 0.3, {"scale": 1}, "sine.inOut", s.base)
        if t_end: J(s.B, f"#{rid}", max(t_end - 0.25, t + 1.9), 0.25, {"opacity": 0}, "power2.in", s.base)
        if sfx: CUES.append((R(t), "curated/ui-click.wav", -15))
        return s
    def hl(s, t, rect, t_end=None, color=AMBER):
        x, y, w, h = rect; hid = uid("hl")
        s.inner.append(f'<div id="{hid}" class="hlb" style="left:{R(x - 6)}px;top:{R(y - 6)}px;width:{R(w + 12)}px;height:{R(h + 12)}px;border-color:{color};background:{color}22"></div>')
        INIT(s.B, f"#{hid}", {"opacity": 0}); J(s.B, f"#{hid}", t, 0.35, {"opacity": 1}, "power2.out", s.base)
        if t_end: J(s.B, f"#{hid}", max(t_end - 0.25, t + 0.37), 0.25, {"opacity": 0}, "power2.in", s.base)
        return s
    def chip(s, t, x, y, text, color, t_end=None, size=40):
        cid = uid("cp")
        s.inner.append(f'<div id="{cid}" class="chipx" style="left:{R(x)}px;top:{R(y)}px;background:{color};font-size:{size}px">{text}</div>')
        INIT(s.B, f"#{cid}", {"opacity": 0, "x": -30}); J(s.B, f"#{cid}", t, 0.4, {"opacity": 1, "x": 0}, "back.out(1.6)", s.base)
        if t_end: J(s.B, f"#{cid}", t_end - 0.25, 0.25, {"opacity": 0}, "power2.in", s.base)
        CUES.append((R(t), "curated/ui-pop.wav", -17)); return s
    def done(s):
        cid = f"{s.id}c"
        s.B["els"].append(f'<div id="{s.id}" class="shot"><div id="{cid}" class="cam"><img src="assets/slides/{s.slide if isinstance(s.slide, str) else f"s-{s.slide:02d}"}.jpg" alt="">{"".join(s.inner)}</div></div>')
        INIT(s.B, f"#{s.id}", {"opacity": 0}); INIT(s.B, f"#{cid}", dict(cam_tf(960, 540, 1920), transformOrigin="0px 0px"))
        J(s.B, f"#{s.id}", s.t0, s.fade, {"opacity": 1}, "power1.out", s.base)
        if s.t1 < SCN_END[s.k] - 1e-3: SET(s.B, f"#{s.id}", s.t1 + 0.35, {"opacity": 0}, s.base)
        busy = s.t0
        for t, cx, cy, w, d in sorted(s.cams):
            if t <= s.t0 + 1e-3: SET(s.B, f"#{cid}", s.t0, cam_tf(cx, cy, w), s.base)
            else: t = max(t, busy + 0.02); J(s.B, f"#{cid}", t, d, cam_tf(cx, cy, w), "power2.inOut", s.base); busy = t + d
        CUES.append((R(s.t0), "curated/zoom-swish.wav", -22))


# ---------- motion-graphic cards (on the stage) ----------
PHONE = lambda c="#1a1a1d": f'<svg width="70" height="118" viewBox="0 0 24 40"><rect x="1" y="1" width="22" height="38" rx="4" fill="{c}"/><rect x="3" y="5" width="18" height="28" rx="1.5" fill="#fff"/><circle cx="12" cy="36" r="1.4" fill="#fff"/></svg>'
PERSON = lambda c: f'<svg width="150" height="150" viewBox="0 0 24 24"><circle cx="12" cy="7.5" r="4.2" fill="{c}"/><path d="M3.2 22c.9-5 4.4-7.6 8.8-7.6s7.9 2.6 8.8 7.6z" fill="{c}"/></svg>'
ICON = {
    "pdf": '<svg data-layout-ignore width="120" height="140" viewBox="0 0 24 28"><path d="M3 1h12l6 6v20H3z" fill="#fff" stroke="#c8102e" stroke-width="1.6"/><path d="M15 1v6h6" fill="none" stroke="#c8102e" stroke-width="1.6"/><rect x="5" y="16" width="14" height="6" rx="1" fill="#c8102e"/><text x="12" y="20.6" font-size="4.6" font-family="Inter" font-weight="800" fill="#fff" text-anchor="middle">PDF</text></svg>',
    "folder": '<svg width="150" height="120" viewBox="0 0 30 24"><path d="M1 4h10l3 3h15v16H1z" fill="#0b57d0"/><rect x="11" y="11" width="8" height="7" rx="1" fill="#fff"/><path d="M12.5 11V9a2.5 2.5 0 015 0v2" fill="none" stroke="#fff" stroke-width="1.6"/></svg>',
    "log": '<svg width="130" height="120" viewBox="0 0 26 24"><rect x="1" y="1" width="24" height="22" rx="2" fill="#fff" stroke="#188038" stroke-width="1.6"/><rect x="1" y="1" width="24" height="5" fill="#188038"/><path d="M1 11h24M1 16h24M9 6v17M17 6v17" stroke="#188038" stroke-width="1"/></svg>',
    "mail": '<svg width="150" height="110" viewBox="0 0 30 22"><rect x="1" y="1" width="28" height="20" rx="2" fill="#fff" stroke="#b8550d" stroke-width="1.6"/><path d="M1.5 2l13.5 10L28.5 2" fill="none" stroke="#b8550d" stroke-width="1.6"/></svg>',
    "box": '<svg width="110" height="100" viewBox="0 0 24 22"><path d="M2 6l10-5 10 5v11l-10 5-10-5z" fill="#c98b4a"/><path d="M2 6l10 5 10-5M12 11v11" stroke="#8a5a2b" stroke-width="1.2" fill="none"/></svg>',
}


class Card:
    def __init__(s, t0, t1, title=None, bg="#ffffff"):
        s.k = scene_of(t0); s.B = SCENE_EL[s.k]; s.base = SCN[s.k]; s.id = uid("mg"); s.t0, s.t1 = t0, t1; s.inner = []; s.bg = bg
        if title: s.inner.append(f'<div class="mgt" style="color:{"#ffffff" if bg == "#1a1a1d" else INK}">{esc(title)}</div>')
    def el(s, html_, x, y, t=None, t_end=None, enter="up", sfx=None, extra_style=""):
        eid = uid("me"); s.inner.append(f'<div id="{eid}" class="mge" style="left:{R(x)}px;top:{R(y)}px;{extra_style}">{html_}</div>')
        if t is not None:
            fr = {"up": {"opacity": 0, "y": 30}, "pop": {"opacity": 0, "scale": 0.6}, "fade": {"opacity": 0}, "draw": {"scaleX": 0}}[enter]
            INIT(s.B, f"#{eid}", fr); J(s.B, f"#{eid}", t, 0.45, {k: (1 if k in ("opacity", "scale", "scaleX") else 0) for k in fr}, "back.out(1.6)" if enter == "pop" else "power3.out", s.base)
            if sfx: CUES.append((R(t), sfx, -16))
        if t_end: J(s.B, f"#{eid}", t_end - 0.25, 0.25, {"opacity": 0}, "power2.in", s.base)
        return eid
    def move(s, eid, t, d, dx, dy=0): J(s.B, f"#{eid}", t, d, {"x": dx, "y": dy}, "power2.inOut", s.base); CUES.append((R(t), "curated/zoom-swish.wav", -15))
    def done(s):
        s.B["els"].append(f'<div id="{s.id}" class="mg" style="background:{s.bg}">{"".join(s.inner)}</div>')
        INIT(s.B, f"#{s.id}", {"opacity": 0}); J(s.B, f"#{s.id}", s.t0, 0.35, {"opacity": 1}, "power1.out", s.base)
        if s.t1 < SCN_END[s.k] - 1e-3: J(s.B, f"#{s.id}", s.t1 - 0.3, 0.3, {"opacity": 0}, "power1.in", s.base)


def role_chip(name, color, size=34): return f'<span class="rchip" style="background:{color};font-size:{size}px">{esc(name)}</span>'


def person(name, color): return f'<div style="text-align:center;width:460px">{PERSON(color)}<div style="margin-top:8px">{role_chip(name, color, 28)}</div></div>'


def handover(t0, t1, frm, to, title, t_move=None, back_to=None, t_back=None):
    """two people, the phone moves from one to the other (optionally back)"""
    c = Card(t0, t1, title)
    c.el(person(frm[0], frm[1]), 90, 200, t0 + 0.1, enter="up")
    c.el(person(to[0], to[1]), 890, 200, t0 + 0.3, enter="up")
    c.el('<div class="arrowx" style="width:300px"></div>', 590, 315, t0 + 0.5, enter="draw")
    ph = c.el(PHONE(), 285, 470, t0 + 0.4, enter="pop")
    tm = t_move or (t0 + 1.0); c.move(ph, tm, 1.3, 800)
    if back_to: c.move(ph, t_back, 1.3, 0)
    c.done(); return c


def flow(t0, t1, title, steps):
    """steps: (icon, text, t) left->right with arrows"""
    c = Card(t0, t1, title); n = len(steps); W = 1440 / n
    for j, (ic, text, t) in enumerate(steps):
        x = W * j + W / 2 - 150
        c.el(f'<div style="width:300px;text-align:center">{ICON[ic]}<div class="mgs">{text}</div></div>', x, 250, t, enter="pop", sfx="curated/ui-pop.wav")
        if j: c.el('<div class="arrowx"></div>', W * j - 40, 330, t - 0.15, enter="draw")
    c.done(); return c


def summary(t0, t1, steps, sub=None, title="Your part"):
    c = Card(t0, t1, title, bg="#1a1a1d"); n = len(steps); x0 = 720 - (n * 300 + (n - 1) * 40) / 2
    for j, s_ in enumerate(steps):
        c.el(f'<div class="sumc" style="background:{ORANGE if j < n - 1 else BLUE}">{esc(s_)}</div>', x0 + j * 340, 330, t0 + 0.3 + 0.55 * j, enter="pop", sfx="curated/ui-pop.wav")
        if j: c.el('<div class="arrowx w"></div>', x0 + j * 340 - 36, 388, t0 + 0.2 + 0.55 * j, enter="draw")
    if sub: c.el(f'<div class="mgsub">{esc(sub)}</div>', 0, 560, t0 + 0.4 + 0.55 * n, extra_style="width:1440px;text-align:center")
    c.done(); CUES.append((R(t0 + 0.3 + 0.55 * n), "clean-ding.wav", -15)); return c


def before_now(t0, t1, paper, t_now, t_pdf=None, title="From paper to one phone"):
    """BEFORE: the real paper form from the deck  ->  NOW: the real app screen on Security's phone"""
    c = Card(t0, t1, title)
    c.el(f'<div style="width:640px;text-align:center"><span class="rchip" style="background:#5f6368;font-size:30px">BEFORE</span></div>', 40, 160, t0 + 0.1)
    c.el(f'<div style="width:640px;height:400px;display:flex;align-items:center;justify-content:center"><img src="assets/media/{paper}" style="max-width:600px;max-height:400px;'
         f'border:2px solid #c9cbd1;border-radius:8px;box-shadow:0 10px 26px rgba(0,0,0,.18)"></div>', 40, 225, t0 + 0.2)
    c.el('<div class="mgs" style="width:640px;text-align:center">Printed paper form,<br>signed with a pen</div>', 40, 640, t0 + 0.4)
    c.el('<div class="arrowx" style="width:110px"></div>', 668, 420, t_now - 0.2, enter="draw")
    c.el(f'<div style="width:400px;text-align:center"><span class="rchip" style="background:{RED};font-size:30px">NOW</span></div>', 760, 160, t_now)
    c.el('<div style="width:400px;height:400px;display:flex;align-items:center;justify-content:center"><img src="assets/media/image-1-1.jpg" style="height:400px;'
         'border:8px solid #1f1f24;border-radius:22px;box-shadow:0 10px 26px rgba(0,0,0,.25)"></div>', 760, 225, t_now + 0.1, enter="pop", sfx="curated/ui-pop.wav")
    c.el('<div class="mgs" style="width:400px;text-align:center">Same form, on the<br>Security officer’s phone</div>', 760, 640, t_now + 0.4)
    if t_pdf: c.el(f'<div style="width:250px;text-align:center">{ICON["pdf"].replace("width=\"120\" height=\"140\"", "width=\"56\" height=\"66\"")}'
                   f'<div class="mgs" style="font-size:28px;color:{GREEN}">Signed PDF<br>saved<br>automatically</div></div>', 1175, 330, t_pdf, enter="pop", sfx="curated/ui-pop.wav")
    c.done(); return c


# ---------- chrome: phone holder, scene title, callouts, stage labels ----------
def role(t, name, color):
    rid = uid("ro"); CH["els"].append(f'<div id="{rid}" class="role" style="background:{color}">{PHONE("#fff").replace("width=\"70\" height=\"118\"", "width=\"26\" height=\"44\"")}<span>PHONE: {esc(name)}</span></div>')
    INIT(CH, f"#{rid}", {"opacity": 0}); CH.setdefault("roles", []).append((t, rid))


def callout(t0, t1, text, kind="info"):
    cid = uid("co"); col = {"info": "#ffffff", "warn": "#ffe3e3", "note": "#fff4d6"}[kind]; fg = {"info": INK, "warn": RED, "note": "#7a4b00"}[kind]
    CH["els"].append(f'<div id="{cid}" class="callout" style="background:{col};color:{fg}">{esc(text)}</div>')
    INIT(CH, f"#{cid}", {"opacity": 0, "y": 10}); J(CH, f"#{cid}", t0, 0.35, {"opacity": 1, "y": 0}); J(CH, f"#{cid}", t1 - 0.3, 0.3, {"opacity": 0}, "power2.in")
    CH.setdefault("callouts", []).append((t0, t1)); CUES.append((R(t0), "curated/ui-pop.wav", -17))


def stage_label(t0, t1, text, color="#ffffff"):
    lid = uid("sl"); CH["els"].append(f'<div id="{lid}" class="slabel" style="color:{color}">{esc(text)}</div>')
    INIT(CH, f"#{lid}", {"opacity": 0}); J(CH, f"#{lid}", t0, 0.3, {"opacity": 1}); J(CH, f"#{lid}", t1 - 0.3, 0.3, {"opacity": 0}, "power2.in")


# ---------- run the plan ----------
PL.build(P, dict(Shot=Shot, handover=handover, flow=flow, summary=summary, role=role, callout=callout, stage_label=stage_label, Card=Card, before_now=before_now, SHAPES=SHAPES, LINES=LINES,
                 BLUE=BLUE, ORANGE=ORANGE, GREEN=GREEN, AMBER=AMBER, RED=RED, person=person, role_chip=role_chip, ICON=ICON, fit=fit))
roles = sorted(CH.get("roles", []))
for j, (t, rid) in enumerate(roles):
    J(CH, f"#{rid}", t, 0.3, {"opacity": 1}, "power1.out")
    if j + 1 < len(roles): J(CH, f"#{rid}", roles[j + 1][0] - 0.16, 0.15, {"opacity": 0}, "power1.in")
    CUES.append((R(t), "curated/ui-pop.wav", -18))
merged = []                                                     # callouts closer than 0.8 s count as one (no title flash)
for c0, c1 in sorted(CH.get("callouts", [])):
    if merged and c0 - merged[-1][1] < 0.8: merged[-1][1] = max(merged[-1][1], c1)
    else: merged.append([c0, c1])
for k in range(NS):                                             # scene titles (hidden while a callout shows)
    tid = f"st{k}"; t0, t1 = SCN[k], SCN_END[k]
    CH["els"].append(f'<div id="{tid}" class="stitle">{k + 1} / {NS} · {esc(D["scenes"][k][0])}</div>')
    INIT(CH, f"#{tid}", {"opacity": 0}); J(CH, f"#{tid}", t0 + 0.2, 0.3, {"opacity": 1})
    hide_end = any(t0 + 0.6 < c0 < t1 and c1 >= t1 - 0.8 for c0, c1 in merged)
    if not hide_end: J(CH, f"#{tid}", t1 - 0.25, 0.25, {"opacity": 0})
    for c0, c1 in merged:
        if t0 + 0.6 < c0 < t1:
            J(CH, f"#{tid}", c0 - 0.2, 0.15, {"opacity": 0})
            if c1 < t1 - 0.8: J(CH, f"#{tid}", c1 + 0.05, 0.3, {"opacity": 1})

# ---------- captions + SRT ----------
def chunks(text):
    words = text.split(); out, cur = [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > 84: out.append(" ".join(cur)); cur = []
        cur.append(w)
    if cur: out.append(" ".join(cur))
    if len(out) > 1 and len(out[-1]) < 20: last = out.pop(); out[-1] += " " + last
    return out


CAP = dict(els=[], js=[], init=[]); srt = []; n = 0
for l in LINES:
    parts = chunks(l["text"]); tot = sum(len(p) for p in parts); t = l["t0"]; d = l["t1"] - l["t0"]
    for p in parts:
        dd = d * len(p) / tot; CAP["els"].append(f'<div id="cg{n}" class="cap"><span>{esc(p)}</span></div>')
        SET(CAP, f"#cg{n}", t, {"opacity": 1}); SET(CAP, f"#cg{n}", t + dd - 0.02, {"opacity": 0}); srt.append((t, t + dd, p)); t += dd; n += 1
fmt = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round((x % 1) * 1000)) % 1000:03d}"
open(f"{O}/{D['export'].replace('.mp4', '.srt')}", "w").write("".join(f"{i + 1}\n{fmt(a)} --> {fmt(b)}\n{p}\n\n" for i, (a, b, p) in enumerate(srt)))

# ---------- write HyperFrames project ----------
E = f"{O}/edit"; os.makedirs(f"{E}/compositions", exist_ok=True); os.makedirs(f"{E}/assets/slides", exist_ok=True)
for f in os.listdir(f"{v}/slides"):
    if not os.path.exists(f"{E}/assets/slides/{f}"): shutil.copy(f"{v}/slides/{f}", f"{E}/assets/slides/{f}")
if VER != "v01" and not os.path.isdir(f"{E}/assets/media"): shutil.copytree(f"{v}/edit/assets/media", f"{E}/assets/media")
if VER != "v01" and os.path.isdir(f"{v}/orig/media"): shutil.copytree(f"{v}/orig/media", f"{E}/assets/media", dirs_exist_ok=True)
CSS = f'''
#root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; overflow: hidden; }}
.shot, .mg {{ position: absolute; left: {SX}px; top: {SY}px; width: {SW}px; height: {SH}px; overflow: hidden; border-radius: 18px; background: #fff; }}
.cam {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
.cam > img {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
.ring {{ position: absolute; border: 6px solid; }}
.hlb {{ position: absolute; border: 5px solid; border-radius: 12px; }}
.chipx {{ position: absolute; color: #fff; font-weight: 800; padding: 8px 20px; border-radius: 12px; white-space: nowrap; box-shadow: 0 8px 20px rgba(0,0,0,.25); }}
.mge {{ position: absolute; }}
.mgt {{ position: absolute; left: 0; top: 70px; width: {SW}px; text-align: center; font-weight: 800; font-size: 54px; color: {INK}; }}
.mg[style*="#1a1a1d"] .mgt {{ color: #fff; }}
.mgs {{ font-weight: 700; font-size: 32px; line-height: 1.25; color: {INK}; margin-top: 14px; }}
.mgsub {{ font-weight: 700; font-size: 40px; color: #fff; }}
.rchip {{ display: inline-block; white-space: nowrap; color: #fff; font-weight: 800; letter-spacing: 1px; padding: 10px 22px; border-radius: 40px; }}
.sumc {{ width: 300px; height: 130px; border-radius: 22px; color: #fff; font-weight: 800; font-size: 42px; display: flex; align-items: center; justify-content: center; }}
.arrowx {{ width: 60px; height: 8px; background: #9aa0a6; border-radius: 4px; transform-origin: 0 50%; position: relative; }}
.arrowx:after {{ content: ""; position: absolute; right: -6px; top: -11px; border-left: 22px solid #9aa0a6; border-top: 15px solid transparent; border-bottom: 15px solid transparent; }}
.arrowx.w {{ width: 30px; }}
'''
CCSS = f'''
#root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; }}
.code {{ position: absolute; left: {SX}px; top: 18px; color: #c9cbd1; font-weight: 700; font-size: 28px; letter-spacing: 1px; }}
.slabel {{ position: absolute; right: {1920 - SX - SW}px; top: 16px; font-weight: 800; font-size: 30px; letter-spacing: 2px; text-align: right; }}
.role {{ position: absolute; left: {SX}px; top: 896px; height: 52px; display: flex; align-items: center; gap: 12px; padding: 0 22px 0 16px; border-radius: 30px; color: #fff; font-weight: 800; font-size: 28px; letter-spacing: 1px; }}
.stitle {{ position: absolute; right: {1920 - SX - SW}px; top: 904px; color: #e8e9ec; font-weight: 700; font-size: 30px; text-align: right; }}
.callout {{ position: absolute; right: {1920 - SX - SW}px; top: 893px; padding: 10px 22px; border-radius: 14px; font-weight: 800; font-size: 28px; line-height: 1.2; white-space: nowrap; }}
.pbar {{ position: absolute; left: 0; top: 1074px; width: 1920px; height: 6px; background: {RED}; transform-origin: 0 50%; }}
'''
TPL = lambda cid, css, B, dur: f'''<template>
  <style>{css}</style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
    {(chr(10) + "    ").join(B["els"])}
  </div>
  <script>
    {(chr(10) + "    ").join(B["init"])}
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(B["js"])}
    tl.set({{}}, {{}}, {R(dur)});
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''
for k in range(NS): open(f"{E}/compositions/scene{k + 1}.html", "w").write(TPL(f"scene{k + 1}", CSS, SCENE_EL[k], SCN_END[k] - SCN[k]))
CH["els"].insert(0, f'<div class="code">{esc(D["code"])} · {esc(D["name"])}</div><div id="pbar" class="pbar"></div>')
INIT(CH, "#pbar", {"scaleX": 0}); J(CH, "#pbar", 0, TOTAL, {"scaleX": 1}, "none")
open(f"{E}/compositions/chrome.html", "w").write(TPL("chrome", CCSS, CH, TOTAL))
CAPCSS = '''#root { position: absolute; inset: 0; font-family: "Inter", sans-serif; }
.cap { position: absolute; left: 240px; width: 1440px; top: 962px; text-align: center; opacity: 0; }
.cap span { display: inline; background: rgba(0,0,0,.72); color: #fff; font-size: 36px; font-weight: 600; line-height: 1.45; padding: 4px 16px; border-radius: 10px; -webkit-box-decoration-break: clone; box-decoration-break: clone; }'''
open(f"{E}/compositions/captions.html", "w").write(TPL("captions", CAPCSS, CAP, TOTAL))
hosts = "\n      ".join(f'<div id="h_scene{k + 1}" class="clip" data-composition-id="scene{k + 1}" data-composition-src="compositions/scene{k + 1}.html" data-start="{R(SCN[k])}" '
                        f'data-duration="{R(SCN_END[k] - SCN[k])}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:2"></div>' for k in range(NS))
open(f"{E}/index.html", "w").write(f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: {BG}; }}
      #bg {{ position: absolute; inset: 0; background: {BG}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-start="0" data-duration="{TOTAL}">
      <div id="bg" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="1" style="z-index:1"></div>
      {hosts}
      <div id="h_chrome" class="clip" data-composition-id="chrome" data-composition-src="compositions/chrome.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:5"></div>
      <div id="h_caps" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index:6"></div>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
''')

# ---------- audio: voice at the laid-out times + low music bed + SFX ----------
SR = 48000; L = int(round(TOTAL * SR)); db = lambda g: 10 ** (g / 20); vo = np.zeros(L)
for l in LINES:
    a, sr = sf.read(f"{O}/vo/lines/{l['scene']}_{[x for x in T['lines'] if x['scene'] == l['scene']].index(next(x for x in T['lines'] if x['i'] == l['i'])):02d}.wav")
    a = ss.resample_poly(a, SR, sr); i = int(round(l["t0"] * SR)); vo[i:i + len(a)] += a[:L - i]
sf.write(f"{O}/vo/vo_laid.wav", vo, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{O}/vo/vo_laid.wav", "-af", "highpass=f=70,equalizer=f=3500:t=q:w=1.2:g=1.5,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=120:makeup=2",
                "-ar", str(SR), "-c:a", "pcm_f32le", f"{O}/vo/vo_proc.wav"], check=True)
vv, _ = sf.read(f"{O}/vo/vo_proc.wav"); vv = np.pad(vv, (0, max(0, L - len(vv))))[:L]
mus = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "music/mixkit_33_motivating_mornings.mp3", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout,
                    np.float32).reshape(-1, 2).astype(np.float64)[:L]
mus = np.pad(mus, ((0, L - len(mus)), (0, 0))); fi, fo = int(1.0 * SR), int(2.5 * SR); mus[:fi] *= np.linspace(0, 1, fi)[:, None]; mus[-fo:] *= np.linspace(1, 0, fo)[:, None]
h = SR // 50; e = np.array([np.sqrt(np.mean(vv[i:i + h] ** 2)) for i in range(0, L, h)])
act = np.convolve((20 * np.log10(e + 1e-9) > -42).astype(float), np.ones(25), "same") > 0
g = np.repeat(np.where(act, db(-30), db(-21)), h)[:L]; g = np.pad(g, (0, L - len(g)), mode="edge"); g = np.convolve(g, np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
fx = np.zeros(L); SFX = "/root/.claude/skills/edit-video/assets/sfx/"
for t, f, gain in sorted(CUES):
    x, s2 = sf.read(SFX + f); x = x if x.ndim == 1 else x.mean(1)
    if s2 != SR: x = ss.resample_poly(x, SR, s2)
    pk = int(np.argmax(np.abs(x))); i0 = int(round(t * SR)) - pk; x = x[max(0, -i0):] * db(gain - 3); i0 = max(0, i0); m = min(len(x), L - i0); fx[i0:i0 + m] += x[:m]
mix = vv[:, None] + mus * g[:, None] + fx[:, None]; pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
sf.write(f"{E}/assets/mix_pre.wav", mix, SR, subtype="PCM_24")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{E}/assets/mix_pre.wav", "-af", "alimiter=limit=0.595:attack=3:release=60:level=false", "-ar", str(SR), "-c:a", "pcm_s24le",
                f"{E}/assets/mix.wav"], check=True); os.remove(f"{E}/assets/mix_pre.wav")
json.dump(dict(total=TOTAL, scenes=[dict(title=D["scenes"][k][0], t0=SCN[k], t1=SCN_END[k]) for k in range(NS)], lines=[dict(i=l["i"], text=l["text"], t0=l["t0"], t1=l["t1"]) for l in LINES]),
          open(f"{O}/layout.json", "w"), indent=1)
print(v, "built", TOTAL, "s,", n, "caption chunks,", len(CUES), "sfx")
