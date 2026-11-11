# AA/SEC/F/042 High-Lift Escort eForm training video -> edit/ (HyperFrames): one scene per slide (compositions/sNN.html), a chrome
# layer and one captions layer; the mix is assets/mix.wav (mix17.py). Reveals start on the voice line that names them
# (timing.json from tts17.py). The deck's own phone screenshots are reused (assets/deck/), and so are its red highlight boxes:
# their exact positions are read from the slide files (slides.json from extract17.py), then drawn as pulsing rings with a punch-in
# zoom on the field. Palette from the deck: AirAsia red, ink, white panels; Inter.
import json, html, re, os
T = json.load(open("timing.json")); TOTAL = T["total"]; SL = {s["n"]: s for s in json.load(open("slides.json"))}
INK, RED, MUTED, BG, GREEN, DARK = "#16161a", "#e4002b", "#5f6170", "#f5f5f7", "#1e8a4c", "#111114"
R = lambda v: round(v, 3); esc = html.escape
os.makedirs("edit/compositions", exist_ok=True); CUES = []

CSS = f'''
#root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; color: {INK}; overflow: hidden; }}
.a {{ position: absolute; }}
.card {{ position: absolute; background: #fff; border-radius: 22px; box-shadow: 0 18px 40px rgba(22,22,26,.10); }}
.kick {{ font-weight: 800; font-size: 28px; letter-spacing: 3px; color: {RED}; }}
.h1 {{ font-weight: 800; font-size: 60px; line-height: 1.08; letter-spacing: -1px; }}
.h2 {{ font-weight: 800; font-size: 44px; line-height: 1.12; }}
.h3 {{ font-weight: 700; font-size: 34px; line-height: 1.22; }}
.t {{ font-weight: 500; font-size: 32px; line-height: 1.35; color: {MUTED}; }}
.num {{ width: 76px; height: 76px; border-radius: 50%; background: {RED}; color: #fff; font-weight: 800; font-size: 36px; display: flex; align-items: center; justify-content: center; flex: none; }}
.row {{ display: flex; align-items: center; gap: 24px; }}
.chip {{ display: inline-block; padding: 12px 24px; border-radius: 40px; font-weight: 800; font-size: 30px; }}
.sample {{ border: 3px dashed {RED}; color: {INK}; background: #fff; border-radius: 14px; padding: 14px 24px; font-size: 34px; font-weight: 700; }}
.sample b {{ color: {RED}; }}
.badge {{ background: {RED}; color: #fff; font-weight: 800; font-size: 28px; letter-spacing: 2px; padding: 8px 16px; border-radius: 8px; }}
.next {{ background: {INK}; color: #fff; }}
.note {{ position: absolute; border-radius: 18px; padding: 22px 30px; font-size: 32px; font-weight: 700; line-height: 1.25; }}
.note.red {{ background: {RED}; color: #fff; }} .note.soft {{ background: #fdeaee; color: {RED}; border: 3px solid rgba(228,0,43,.3); }}
.note.ink {{ background: {INK}; color: #fff; }} .note.ok {{ background: #e5f5ec; color: {GREEN}; border: 3px solid rgba(30,138,76,.35); }}
.dev {{ position: absolute; background: {DARK}; border-radius: 34px; padding: 16px; box-shadow: 0 30px 70px rgba(22,22,26,.28); }}
.view {{ position: relative; overflow: hidden; border-radius: 20px; background: #fff; }}
.zoom {{ position: absolute; left: 0; top: 0; transform-origin: 0 0; }}
.zoom img {{ display: block; }}
.ring {{ position: absolute; border: 7px solid {RED}; border-radius: 12px; box-shadow: 0 0 0 6px rgba(228,0,43,.18); }}
.ring.round {{ border-radius: 999px; }}
.tap {{ position: absolute; width: 70px; height: 70px; border-radius: 50%; background: rgba(228,0,43,.35); border: 4px solid {RED}; }}
.flow {{ position: absolute; height: 170px; border-radius: 22px; background: #fff; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 0 22px;
  box-shadow: 0 18px 40px rgba(22,22,26,.10); }}
.flow b {{ font-size: 34px; line-height: 1.15; }} .flow span {{ font-size: 28px; color: {MUTED}; margin-top: 10px; line-height: 1.2; }}
.flow.red {{ background: {RED}; color: #fff; }} .flow.red span {{ color: rgba(255,255,255,.88); }} .flow.ink {{ background: {INK}; color: #fff; }} .flow.ink span {{ color: rgba(255,255,255,.8); }}
.arrow {{ position: absolute; height: 6px; background: {MUTED}; border-radius: 3px; transform-origin: 0 50%; }}
.arrow:after {{ content: ""; position: absolute; right: -4px; top: -9px; border-left: 20px solid {MUTED}; border-top: 12px solid transparent; border-bottom: 12px solid transparent; }}
.x {{ width: 62px; height: 62px; border-radius: 50%; background: {RED}; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 34px; flex: none; }}
'''


class Scene:
    def __init__(s, sc):
        s.sc = sc; s.id = sc["id"]; s.dur = sc["dur"]; s.start = sc["start"]; s.L = sc["lines"]; s.els, s.js, s.init = [], [], []

    def t(s, i, d=0.0): return R(s.L[min(i, len(s.L) - 1)]["t0"] + d)

    def find(s, pat, default=None, after=-1):
        for l in s.L:
            if l["i"] > after and re.search(pat, l["text"], re.I): return l["i"]
        return default

    def tw(s, sel, t, d, props, ease="power3.out"):
        s.js.append(f'tl.to("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())},duration:{R(d)},ease:"{ease}"}},{R(t)});')

    def st(s, sel, t, props): s.js.append(f'tl.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())}}},{R(t)});')

    def gs(s, sel, props): s.init.append(f'gsap.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())}}});')

    def add(s, eid, inner, style="", cls="a", t_in=None, t_out=None, enter="up", sfx=None):
        s.els.append(f'<div id="{eid}" class="{cls}" style="{style}">{inner}</div>')
        if t_in is not None:
            fr = {"up": {"opacity": 0, "y": 40}, "left": {"opacity": 0, "x": -70}, "right": {"opacity": 0, "x": 70}, "pop": {"opacity": 0, "scale": 0.7},
                  "fade": {"opacity": 0}, "draw": {"scaleX": 0}}[enter]
            s.gs(f"#{eid}", fr); to = {k: (1 if k in ("opacity", "scale", "scaleX") else 0) for k in fr}
            s.tw(f"#{eid}", t_in, 0.5 if enter != "pop" else 0.45, to, "back.out(1.6)" if enter == "pop" else "power3.out")
            if sfx: CUES.append((R(s.start + t_in), sfx[0], sfx[1]))
        if t_out is not None: s.tw(f"#{eid}", t_out - 0.35, 0.35, {"opacity": 0}, "power2.in")

    def pulse(s, eid, t, scale=1.06):
        s.tw(f"#{eid}", t, 0.22, {"scale": scale}, "power2.out"); s.tw(f"#{eid}", t + 0.22, 0.35, {"scale": 1}, "power2.inOut")

    def write(s):
        open(f"edit/compositions/{s.id}.html", "w").write(f'''<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{s.id}" data-width="1920" data-height="1080">
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


def device(S, eid, src, size, x, y, vw, vh, t_in, enter="up"):
    """device frame with the deck screenshot at display width vw inside a vw x vh viewport; returns px-per-image-px"""
    k = vw / size[0]; ih = R(size[1] * k)
    S.add(eid, f'<div class="view" style="width:{vw}px;height:{vh}px"><div class="zoom" id="{eid}_z"><img src="assets/deck/{src}" style="width:{vw}px;height:{ih}px" alt=""></div>'
          f'<div class="a" id="{eid}_ov" style="left:0;top:0;width:{vw}px;height:{vh}px"></div></div>', f"left:{x}px;top:{y}px", "dev", t_in, None, enter)
    return k


def flow_row(S, pre, items, x0, y, w, gap, t_ins, kinds=None):
    for i, (b, sub) in enumerate(items):
        x = x0 + i * (w + gap)
        S.add(f"{pre}{i}", f"<b>{esc(b)}</b>" + (f"<span>{esc(sub)}</span>" if sub else ""), f"left:{x}px;top:{y}px;width:{w}px", f"flow {(kinds or [''] * 9)[i]}", t_ins[i], None, "up",
              ("curated/ui-pop.wav", -19))
        if i < len(items) - 1: S.add(f"{pre}a{i}", "", f"left:{x + w + 14}px;top:{y + 82}px;width:{gap - 40}px", "arrow", t_ins[i + 1] - 0.1, None, "draw")


def deck_text(n):
    """deck slide text -> kicker, step, title, body lines, sample, badge, next"""
    tx = [q["t"] for q in SL[n]["texts"]]; d = dict(kick=None, step=None, title=None, body=[], sample=None, badge=False, next=False)
    for t in tx:
        if t == "TEST / SAMPLE DATA": d["badge"] = True
        elif t == "Then tap Next": d["next"] = True
        elif re.fullmatch(r"\d+", t): d["step"] = t
        elif d["kick"] is None and (t.isupper() or re.match(r"PAGE \d", t)): d["kick"] = t
        elif d["title"] is None: d["title"] = t
        else:
            m = re.split(r"\s*Sample:\s*", t)
            if m[0]: d["body"].append(m[0])
            if len(m) > 1: d["sample"] = m[1]
    return d


SC = {s["id"]: s for s in T["scenes"]}; scenes = []; prev_src = None
VW, VH, DX, DY = 880, 647, 110, 200                     # device viewport and position


def generic(sc):
    global prev_src
    S = Scene(sc); n = sc["n"]; d = deck_text(n); sh = SL[n]["shot"]; last = len(S.L) - 1
    k = device(S, "dv", sh["src"], sh["size"], DX, DY, VW, VH, 0.15 if sh["src"] != prev_src else None)
    prev_src = sh["src"]
    tall = sh["size"][1] * k > VH + 10
    x0 = 1100
    if d["kick"]: S.add("kick", esc(d["kick"]), f"left:{x0}px;top:200px", "a kick", 0.25, None, "left")
    title_html = (f'<div class="num">{d["step"]}</div>' if d["step"] else "") + f'<div class="h1" style="max-width:{640 if d["step"] else 800}px">{esc(d["title"] or sc["title"])}</div>'
    S.add("ttl", title_html, f"left:{x0}px;top:250px", "a row", 0.35, None, "left", ("curated/zoom-swish.wav", -22))
    yb = 470 if len(d["title"] or "") > 22 else 400
    for j, b in enumerate(d["body"][:2]):
        S.add(f"bd{j}", esc(b), f"left:{x0}px;top:{yb + j * 110}px;width:760px", "a t", S.t(min(1 + j, last)) + 0.2, None, "up")
    yb += 110 * min(2, len(d["body"]))
    if d["badge"]: S.add("badge", "TEST / SAMPLE DATA", f"left:{DX + VW - 300}px;top:150px", "a badge", 0.5, None, "fade")
    si = S.find(r"demonstration|sample|for example|Sample", None)
    if d["sample"]:
        S.add("smp", f'Sample: <b>{esc(d["sample"])}</b>', f"left:{x0}px;top:{yb + 10}px", "a sample", S.t(si if si is not None else 1) + 0.3, None, "pop", ("curated/ui-pop.wav", -16))
        yb += 110
    ni = S.find(r"tap Next|tap Submit to send|Then, tap Next")
    if d["next"] or ni is not None:
        S.add("nx", "Then tap Next" if not re.search("Submit", S.L[ni]["text"] if ni is not None else "") else "Tap Submit", f"left:{x0}px;top:{yb + 10}px", "a chip next",
              S.t(ni if ni is not None else last) + 0.3, None, "pop", ("curated/ui-click.wav", -16))
        yb += 100
    ai = S.find(r"Duty Security Executive|Duty Officer")
    if ai is not None:
        S.add("dse", "Report any abnormality immediately to the Duty Security Executive", f"left:{x0}px;top:{max(yb + 20, 700)}px;width:760px", "note red", S.t(ai) + 0.3, None, "up",
              ("curated/ui-click.wav", -15))
    sv = S.find(r"supervisor")
    if sv is not None and ai is None: S.add("sup", "Not sure? Check with your supervisor", f"left:{x0}px;top:{max(yb + 20, 720)}px;width:760px", "note ink", S.t(sv) + 0.3, None, "up")
    # highlight rings + punch-in on the field
    hi = S.find(r"\b(tap|locate|select|enter|title|asterisk|error message|highlighted|Submit button|Back)\b", 0)
    boxes = sh["boxes"]
    if tall:                                                   # long page: scroll the screenshot through the viewport
        ih = sh["size"][1] * k; s0 = S.find(r"Scroll", 0); S.tw("#dv_z", S.t(s0) + 0.4, max(3, S.L[min(s0 + 1, last)]["t1"] - S.t(s0)), {"y": -(ih - VH)}, "power1.inOut")
    for j, b in enumerate(boxes):
        bx, by, bw, bh = b["x"] * k, b["y"] * k, b["w"] * k, b["h"] * k; tb = S.t(hi) + 0.3 + 0.9 * j
        S.els.append(f'<div id="rg{j}" class="ring{" round" if b.get("round") else ""}" style="left:{R(bx - 8)}px;top:{R(by - 8)}px;width:{R(bw + 16)}px;height:{R(bh + 16)}px"></div>')
        # rings live in the viewport overlay so they follow the zoom
        S.els[-1] = S.els[-1]
        S.gs(f"#rg{j}", {"opacity": 0, "scale": 1.25, "transformOrigin": "50% 50%"}); S.tw(f"#rg{j}", tb, 0.4, {"opacity": 1, "scale": 1}, "back.out(1.8)")
        S.tw(f"#rg{j}", tb + 0.6, 0.5, {"scale": 1.05}, "sine.inOut"); S.tw(f"#rg{j}", tb + 1.1, 0.5, {"scale": 1}, "sine.inOut")
        CUES.append((R(S.start + tb), "curated/ui-click.wav", -18))
    if boxes:
        # move the ring elements inside the zoom layer (positions are in viewport px of the unzoomed image)
        rings = [e for e in S.els if e.startswith('<div id="rg')]; S.els = [e for e in S.els if not e.startswith('<div id="rg')]
        S.els = [e.replace(f'<div class="zoom" id="dv_z"><img', f'<div class="zoom" id="dv_z">{"".join(rings)}<img') if e.startswith('<div id="dv"') else e for e in S.els]
        x0b = min(b["x"] for b in boxes) * k; y0b = min(b["y"] for b in boxes) * k
        x1b = max(b["x"] + b["w"] for b in boxes) * k; y1b = max(b["y"] + b["h"] for b in boxes) * k
        z = max(1.0, min(1.55, 0.8 * VW / max(1, x1b - x0b), 0.75 * VH / max(1, y1b - y0b)))
        if z > 1.08 and not tall:
            cx, cy = (x0b + x1b) / 2, (y0b + y1b) / 2
            tx = min(0, max(VW - VW * z, VW / 2 - cx * z)); ty = min(0, max(VH - sh["size"][1] * k * z, VH / 2 - cy * z))
            zt = S.t(hi) + 0.9 + 0.9 * (len(boxes) - 1)
            S.tw("#dv_z", zt, 0.9, {"scale": R(z), "x": R(tx), "y": R(ty)}, "power3.inOut")
            S.tw("#dv_z", S.dur - 1.4, 0.9, {"scale": 1, "x": 0, "y": 0}, "power3.inOut")
        # a tap ripple on the first box
        b = boxes[0]; S.els.append(f'<div id="tp" class="tap" style="left:{R(DX + 16 + (b["x"] + b["w"] / 2) * k - 35)}px;top:{R(DY + 16 + (b["y"] + b["h"] / 2) * k - 35)}px"></div>')
        S.gs("#tp", {"opacity": 0, "scale": 0.3}); tb = S.t(hi) + 0.3; S.st("#tp", tb, {"opacity": 1}); S.tw("#tp", tb, 0.6, {"scale": 1.6, "opacity": 0}, "power2.out")
    return S


# ---------------- bespoke scenes ----------------
def s01(sc):
    S = Scene(sc); end_dark = S.t(2)
    S.add("bg", "", f"left:0;top:0;width:1920px;height:1080px;background:{DARK}", "a", None, end_dark)
    S.add("k", "STAFF GUIDE", f"left:150px;top:300px", "a kick", None, end_dark)
    S.add("ttl", "High-Lift Escort eForm", "left:150px;top:350px;color:#fff;width:820px;font-size:84px", "a h1", None, end_dark)
    S.add("sub", "AA/SEC/F/042 – Hi-lift Escort Checklist", "left:150px;top:550px;color:#fff;font-size:38px;font-weight:700", "a", 0.4, end_dark, "left")
    S.add("sub2", "How to fill it in on your phone, one step at a time", "left:150px;top:610px;color:rgba(255,255,255,.7);font-size:32px;font-weight:500", "a", S.t(1) + 0.4, end_dark, "left")
    sh = SL[1]["shot"]; k = 760 / sh["size"][0]
    S.add("dv", f'<div class="view" style="width:760px;height:{R(sh["size"][1] * k)}px"><img src="assets/deck/{sh["src"]}" style="width:760px;display:block" alt=""></div>', "left:1030px;top:250px", "dev", 0.2, end_dark, "right")
    S.add("h2", "What this training covers", "left:150px;top:200px", "a h1", end_dark + 0.2, None, "left")
    flow_row(S, "fw", [("Open the form", "link or QR code"), ("Flight details", "time, flight, ETD, sector"), ("Security inspections", "prohibited items, seal and lock"),
                       ("Security sign-offs", "catering facility, aircraft"), ("Submit", "your report")], 150, 400, 300, 50,
             [end_dark + 0.6 + 1.1 * i for i in range(5)], ["", "", "", "", "red"])
    S.add("acc", "Follow each step so every escort duty is recorded accurately", "left:150px;top:680px;width:1620px;text-align:center", "note ink", S.t(3) + 0.3, None, "up", ("clean-ding.wav", -17))
    return S


def s02(sc):
    S = Scene(sc)
    S.add("k", "ABOUT THIS FORM", "left:150px;top:200px", "a kick", 0.2, None, "left"); S.add("ttl", "What is this form for?", "left:150px;top:250px", "a h1", 0.3, None, "left")
    items = [("Record one hi-lift escort", "Flight number, ETD, sector and start time.", 1), ("Checks at the catering facility", "Prohibited items in the truck / hi-lift cabin; seal and lock; truck and seal numbers.", 2),
             ("Two security sign-offs", "Catering facility security, then aircraft security.", 2)]
    for i, (h, b, li) in enumerate(items):
        S.add(f"it{i}", f'<div class="num">{i + 1}</div><div><div class="h3">{h}</div><div class="t" style="font-size:29px;max-width:760px">{b}</div></div>', f"left:150px;top:{380 + i * 150}px", "a row",
              S.t(li) + (0.3 if i < 2 else 6.5), None, "left", ("curated/ui-pop.wav", -17))
    S.add("one", "One form for each escort duty", f"left:1120px;top:390px;width:650px", "note ink", S.t(3) + 0.2, None, "pop", ("curated/ui-click.wav", -16))
    S.add("q", '<div style="font-size:26px;font-weight:800;letter-spacing:2px;opacity:.85">FROM THE FORM</div>“Please report any abnormality to Duty Security Executive immediately.”',
          f"left:1120px;top:540px;width:650px", "note red", S.t(4) + 0.3, None, "up", ("curated/ui-click.wav", -15))
    return S


def s03(sc):
    S = Scene(sc)
    S.add("k", "STEP 1 · OPEN THE FORM", "left:150px;top:200px", "a kick", 0.2, None, "left"); S.add("ttl", "Open the form on your phone", "left:150px;top:250px;width:900px", "a h1", 0.3, None, "left")
    for i, (txt, li) in enumerate((("Get the form link from your supervisor.", 0), ("Tap the link, or scan the QR code with your phone camera.", 1), ("The form opens in your web browser. No app needed.", 2))):
        S.add(f"st{i}", f'<div class="num">{i + 1}</div><div class="h3" style="max-width:820px">{txt}</div>', f"left:150px;top:{400 + i * 150}px", "a row", S.t(li) + 0.5, None, "left", ("curated/ui-pop.wav", -17))
    S.add("qr", '<img src="assets/deck/image1.png" style="width:420px;height:420px;display:block" alt=""><div style="text-align:center;font-weight:700;font-size:30px;margin-top:10px">Scan to open the form</div>',
          "left:1250px;top:230px;padding:30px", "card", S.t(1) + 0.4, None, "pop")
    S.add("sl", "", f"left:1280px;top:262px;width:420px;height:6px;background:{RED};box-shadow:0 0 18px {RED}", "a", S.t(1) + 0.9, S.t(3), "fade")
    S.tw("#sl", S.t(1) + 0.9, 1.4, {"y": 410}, "power1.inOut"); S.tw("#sl", S.t(1) + 2.3, 1.4, {"y": 0}, "power1.inOut")
    S.add("noapp", "No download. No app to install.", f"left:1250px;top:820px;width:520px;text-align:center", "note ok", S.t(3) + 0.3, None, "pop", ("clean-ding.wav", -17))
    return S


def s36(sc):
    S = Scene(sc)
    S.add("k", "AFTER YOU SUBMIT", "left:150px;top:200px", "a kick", 0.2, None, "left"); S.add("ttl", "You cannot change it after Submit", "left:150px;top:250px;width:900px", "a h1", 0.3, None, "left")
    for i, (h, b, li, sym) in enumerate((("No edit link", "Editing after submitting is turned off for this form.", 1, "✕"), ("No copy sent to you", "A copy of the response is not sent to you.", 1, "✕"),
                                         ("Made a mistake?", "Tell your supervisor straight away.", 3, "!"))):
        S.add(f"it{i}", f'<div class="x" style="{"background:" + INK if sym == "!" else ""}">{sym}</div><div><div class="h3">{h}</div><div class="t" style="font-size:29px">{b}</div></div>',
              f"left:150px;top:{420 + i * 140}px", "a row", S.t(li) + 0.3 + (2.2 if i == 1 else 0), None, "left", ("curated/ui-click.wav", -16))
    S.add("chk", "So: check every page before you tap Submit", f"left:150px;top:850px;width:880px", "note soft", S.t(2) + 0.3, None, "up")
    sh = SL[36]["shot"]; k = 640 / sh["size"][0]
    S.add("dv", f'<div class="view" style="width:640px;height:{R(sh["size"][1] * k)}px"><img src="assets/deck/{sh["src"]}" style="width:640px;display:block" alt=""></div>', "left:1150px;top:300px", "dev", 0.4, None, "right")
    return S


def s37(sc):
    S = Scene(sc); sh = SL[37]["shot"]; W7 = 1180; k = W7 / sh["size"][0]; y7 = 330
    S.add("k", "WHERE ANSWERS GO", "left:110px;top:180px", "a kick", 0.2, None, "left"); S.add("ttl", "Every Submit adds one row to a Google Sheet", "left:110px;top:230px", "a h1", 0.3, None, "left")
    S.add("dv", f'<div class="view" style="width:{W7}px;height:{R(sh["size"][1] * k)}px"><img src="assets/deck/{sh["src"]}" style="width:{W7}px;display:block" alt=""></div>', f"left:110px;top:{y7}px", "dev", S.t(1) + 0.2, None, "up")
    b = sh["boxes"][0]
    S.add("rg", "", f"left:{R(110 + 16 + b['x'] * k - 8)}px;top:{R(y7 + 16 + b['y'] * k - 8)}px;width:{R(b['w'] * k + 16)}px;height:{R(b['h'] * k + 16)}px", "ring", S.t(3) + 0.3, None, "pop",
          ("curated/ui-click.wav", -16))
    S.add("nr", "One submitted checklist = one new row", "left:1370px;top:360px;width:440px", "note ink", S.t(2) + 0.3, None, "up")
    S.add("r4", "Row 4: the TEST response made for this guide", "left:1370px;top:540px;width:440px", "note soft", S.t(3) + 0.8, None, "up")
    S.add("rv", "Reviewed by authorised personnel", "left:1370px;top:720px;width:440px", "note ok", S.t(4) + 0.3, None, "up")
    return S


def s38(sc):
    S = Scene(sc)
    S.add("k", "WHO DOES WHAT", "left:150px;top:200px", "a kick", 0.2, None, "left"); S.add("ttl", "You submit. Supervisors review.", "left:150px;top:250px", "a h1", 0.3, None, "left")
    flow_row(S, "fw", [("AVSEC staff", "do the checks, fill in the form, tap Submit"), ("Response Sheet", "each submission saved automatically as a new row"), ("Authorised supervisors", "review and manage the records")],
             150, 420, 480, 90, [S.t(1) + 0.3, S.t(2) + 0.3, S.t(3) + 0.3], ["red", "", "ink"])
    S.add("no", "Staff do not need to open or manage the response sheet", f"left:150px;top:700px;width:1620px;text-align:center", "note soft", S.t(4) + 0.3, None, "up")
    return S


def s39(sc):
    S = Scene(sc); p2, p3, p4, p5 = S.t(2), S.t(4), S.t(8), S.t(11)
    S.add("k", "TROUBLESHOOTING", "left:150px;top:200px", "a kick", 0.2, p3, "left"); S.add("ttl", "Need help?", "left:150px;top:250px", "a h1", 0.3, p3, "left")
    for i, (h, b) in enumerate((("Form will not open?", "Use the correct link or QR code from your supervisor."), ("Page will not load or submit?", "Check your internet connection (data or Wi-Fi), then try again."))):
        S.add(f"tr{i}", f'<div class="num">{i + 1}</div><div><div class="h3">{h}</div><div class="t" style="font-size:29px">{b}</div></div>', f"left:150px;top:{380 + i * 140}px", "a row", S.t(1) + 0.5 + 3 * i, p2, "left",
              ("curated/ui-pop.wav", -17))
    S.add("h2", "Problem continues?", "left:150px;top:370px", "a h2", p2 + 0.2, p3, "left")
    flow_row(S, "fw", [("You", "report immediately"), ("Respective supervisor", "escalates the issue"), ("System Unit", "immediate rectification")], 150, 460, 480, 90,
             [p2 + 0.5, p2 + 2.5, S.t(3) + 0.3], ["red", "", "ink"])
    for i in range(3): S.tw(f"#fw{i}", p3 - 0.35, 0.35, {"opacity": 0}, "power2.in")
    for i in range(2): S.tw(f"#fwa{i}", p3 - 0.35, 0.35, {"opacity": 0}, "power2.in")
    S.add("k2", "SYSTEM DISRUPTION", "left:150px;top:200px", "a kick", p3 + 0.2, p4, "left"); S.add("t2", "Manual form: a temporary alternative", "left:150px;top:250px", "a h1", p3 + 0.3, p4, "left")
    S.add("hod", "Only with approval from the Head of Department", f"left:150px;top:420px;width:1000px", "note red", S.t(5) + 0.3, p4, "up", ("curated/ui-click.wav", -15))
    S.add("nosw", "✕  No switching to manual documentation without approval", f"left:150px;top:560px;width:1000px", "note soft", S.t(6) + 0.3, p4, "up")
    S.add("res", "✓  System restored: resume the eForm as your supervisor instructs", f"left:150px;top:700px;width:1000px", "note ok", S.t(7) + 0.3, p4, "up")
    S.add("k3", "AT ALL TIMES", "left:150px;top:200px", "a kick", p4 + 0.2, p5, "left")
    for i, w in enumerate(("Accurate documentation", "Timely reporting", "Compliance with security procedures")):
        S.add(f"aa{i}", f'<b style="font-size:38px">{w}</b>', f"left:{150 + i * 560}px;top:300px;width:500px", "flow", p4 + 0.6 + 1.2 * i, p5, "up", ("curated/ui-pop.wav", -17))
    S.add("chk", "Every required security check: properly conducted and accurately recorded", f"left:150px;top:540px;width:1620px;text-align:center", "note ink", S.t(9) + 0.3, p5, "up")
    S.add("dse", "Any abnormality? Report it immediately to the Duty Security Executive", f"left:150px;top:680px;width:1620px;text-align:center", "note red", S.t(10) + 0.3, p5, "up")
    S.add("bg", "", f"left:0;top:0;width:1920px;height:1080px;background:{DARK}", "a", p5, None, "fade")
    S.add("ty", "Thank you", "left:0;width:1920px;top:260px;text-align:center;color:#fff;font-size:110px;font-weight:800", "a", p5 + 0.3, None, "up", ("sparkle.wav", -16))
    S.add("sa", f'Stay alert. Follow the required procedures.<br><span style="color:{RED}">Always prioritise aviation security.</span>', "left:0;width:1920px;top:430px;text-align:center;color:#fff;font-size:50px;font-weight:800;line-height:1.3",
          "a", S.t(12) + 0.2, None, "up")
    S.add("end", "AA/SEC/F/042 – High-Lift Escort eForm · Staff Training", "left:0;width:1920px;top:640px;text-align:center;color:rgba(255,255,255,.75);font-size:34px;font-weight:700;letter-spacing:1px",
          "a", S.t(13) + 0.2, None, "up")
    return S


BESPOKE = {"s01": s01, "s02": s02, "s03": s03, "s36": s36, "s37": s37, "s38": s38, "s39": s39}
for sc in T["scenes"]:
    sc["n"] = int(sc["id"][1:])
    S = BESPOKE[sc["id"]](sc) if sc["id"] in BESPOKE else generic(sc)
    if sc["id"] in BESPOKE: prev_src = None
    scenes.append(S); S.write()
CUES.extend((R(sc["start"]), "curated/zoom-swish.wav", -20) for sc in T["scenes"][1:])

# ---------------- chrome ----------------
ch_els = [f'<div id="ctag" class="a" style="left:110px;top:40px;font-size:28px;font-weight:700;letter-spacing:1.5px;color:{MUTED}">AA/SEC/F/042 · HI-LIFT ESCORT eFORM · STAFF TRAINING</div>',
          f'<div id="pbar" class="a" style="left:0;top:1072px;width:1920px;height:8px;background:{RED};transform-origin:0 50%"></div>']
ch_init = ['gsap.set("#pbar",{scaleX:0});', 'gsap.set("#ctag",{opacity:0});']; ch_js = [f'tl.to("#pbar",{{scaleX:1,duration:{R(TOTAL)},ease:"none"}},0);']
for i, sc in enumerate(T["scenes"]):
    ch_els.append(f'<div id="chap{i}" class="a" style="right:110px;top:40px;font-size:28px;font-weight:700;color:{INK};text-align:right">{i + 1:02d} / {len(T["scenes"])} · {esc(sc["title"])}</div>')
    ch_init.append(f'gsap.set("#chap{i}",{{opacity:0}});')
    a = sc["start"] + (sc["lines"][2]["t0"] if i == 0 else 0.2); ch_js.append(f'tl.to("#chap{i}",{{opacity:1,duration:0.4}},{R(a)});')
    ch_js.append(f'tl.to("#chap{i}",{{opacity:0,duration:0.3}},{R(sc["start"] + sc["dur"] - 0.3)});')
s0, s39_ = T["scenes"][0], T["scenes"][-1]
ch_js.append(f'tl.to("#ctag",{{opacity:1,duration:0.4}},{R(s0["start"] + s0["lines"][2]["t0"])});')
ch_js.append(f'tl.to("#ctag",{{opacity:0,duration:0.3}},{R(s39_["start"] + s39_["lines"][11]["t0"])});')
ch_js.append(f'tl.to("#chap{len(T["scenes"]) - 1}",{{opacity:0,duration:0.3}},{R(s39_["start"] + s39_["lines"][11]["t0"])});')
open("edit/compositions/chrome.html", "w").write(f'''<template>
  <style>#root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; }} .a {{ position: absolute; }}</style>
  <div id="root" data-composition-id="chrome" data-width="1920" data-height="1080">
    {(chr(10) + "    ").join(ch_els)}
  </div>
  <script>
    {(chr(10) + "    ").join(ch_init)}
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(ch_js)}
    tl.set({{}}, {{}}, {R(TOTAL)});
    window.__timelines["chrome"] = tl;
  </script>
</template>
''')


# ---------------- captions ----------------
def chunks(text):
    words = text.split(); out, cur = [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > 88: out.append(" ".join(cur)); cur = []
        cur.append(w)
        if re.search(r"[.?!:;]$", w) and len(" ".join(cur)) > 40 and w != words[-1]: out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    if len(out) > 1 and len(out[-1]) < 22: last = out.pop(); out[-1] += " " + last
    return out


cap_els, cap_js, n = [], [], 0
for sc in T["scenes"]:
    for l in sc["lines"]:
        parts = chunks(l["text"]); tot = sum(len(p) for p in parts); t = sc["start"] + l["t0"]; d = l["t1"] - l["t0"]
        for p in parts:
            dd = d * len(p) / tot
            cap_els.append(f'<div id="cg{n}" class="cap"><span>{esc(p)}</span></div>')
            cap_js.append(f'tl.set("#cg{n}",{{opacity:1}},{R(t)});tl.set("#cg{n}",{{opacity:0}},{R(t + dd - 0.02)});'); t += dd; n += 1
open("edit/compositions/captions.html", "w").write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; }}
    .cap {{ position: absolute; left: 210px; width: 1500px; bottom: 74px; text-align: center; opacity: 0; }}
    .cap span {{ display: inline; background: rgba(22,22,26,.9); color: #fff; font-size: 36px; font-weight: 600; line-height: 1.5; padding: 6px 18px; border-radius: 10px;
      -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080">
    {(chr(10) + "    ").join(cap_els)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(cap_js)}
    tl.set({{}}, {{}}, {R(TOTAL)});
    window.__timelines["captions"] = tl;
  </script>
</template>
''')

# ---------------- root ----------------
hosts = "\n      ".join(f'<div id="h_{sc["id"]}" class="clip" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" data-start="{R(sc["start"])}" '
                        f'data-duration="{R(sc["dur"])}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:2"></div>' for sc in T["scenes"])
open("edit/index.html", "w").write(f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: {BG}; }}
      #bg {{ position: absolute; inset: 0; background: {BG}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-start="0" data-duration="{R(TOTAL)}">
      <div id="bg" class="clip" data-start="0" data-duration="{R(TOTAL)}" data-track-index="1" style="z-index:1"></div>
      {hosts}
      <div id="h_chrome" class="clip" data-composition-id="chrome" data-composition-src="compositions/chrome.html" data-start="0" data-duration="{R(TOTAL)}" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:5"></div>
      <div id="h_caps" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{R(TOTAL)}" data-track-index="4" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index:6"></div>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{R(TOTAL)}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
''')
json.dump({"cues": [{"t": a, "sfx": b, "gain_db": c} for a, b, c in sorted(CUES)]}, open("edit/cues.json", "w"), indent=1)
print("built", len(scenes), "scenes,", n, "caption chunks,", len(CUES), "sfx cues, total", TOTAL)
