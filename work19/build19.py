# FOCA Checklist (AA/SEC/F/070) staff training video -> edit/ (HyperFrames): one scene per slide (compositions/sNN.html), chrome and
# captions layers; the mix is assets/mix.wav (mix19.py). Reveals start on the voice line that names them (timing.json, tts19.py).
# The deck's own phone screenshots, close-ups and red highlight boxes are reused (slides.json, extract19.py): rings pulse on the
# boxes, the screenshot punches in on the field, the close-up card appears beside it. A role badge on every step says who holds the
# phone. Palette from the deck: AirAsia red, ink, Security blue, Airline Rep orange; Inter.
import json, html, re, os
T = json.load(open("timing.json")); TOTAL = T["total"]; SL = {s["n"]: s for s in json.load(open("slides.json"))}
import script19; NOTES = {s["id"]: s["notes"] for s in script19.SCENES}
INK, RED, MUTED, BG, GREEN, DARK, BLUE, ORANGE = "#1a1a1a", "#c8102e", "#5f6368", "#f5f5f7", "#188038", "#121214", "#0b57d0", "#b8550d"
R = lambda v: round(v, 3); esc = html.escape
os.makedirs("edit/compositions", exist_ok=True); CUES = []
ROLE = {"SECURITY STAFF": BLUE, "AIRLINE REPRESENTATIVE": ORANGE, "SECURITY REPRESENTATIVE": BLUE}

CSS = f'''
#root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; color: {INK}; overflow: hidden; }}
.a {{ position: absolute; }}
.card {{ position: absolute; background: #fff; border-radius: 22px; box-shadow: 0 18px 40px rgba(26,26,26,.10); }}
.kick {{ font-weight: 800; font-size: 28px; letter-spacing: 3px; color: {RED}; }}
.h1 {{ font-weight: 800; font-size: 60px; line-height: 1.08; letter-spacing: -1px; }}
.h2 {{ font-weight: 800; font-size: 44px; line-height: 1.12; }}
.h3 {{ font-weight: 700; font-size: 34px; line-height: 1.22; }}
.t {{ font-weight: 500; font-size: 32px; line-height: 1.35; color: {MUTED}; }}
.num {{ width: 72px; height: 72px; border-radius: 50%; background: {RED}; color: #fff; font-weight: 800; font-size: 34px; display: flex; align-items: center; justify-content: center; flex: none; }}
.row {{ display: flex; align-items: center; gap: 24px; }}
.role {{ display: inline-flex; align-items: center; gap: 12px; padding: 10px 22px; border-radius: 40px; color: #fff; font-weight: 800; font-size: 28px; letter-spacing: 2px; }}
.chip {{ display: inline-block; padding: 12px 24px; border-radius: 40px; font-weight: 800; font-size: 30px; }}
.note {{ position: absolute; border-radius: 18px; padding: 22px 30px; font-size: 32px; font-weight: 700; line-height: 1.25; }}
.note.red {{ background: {RED}; color: #fff; }} .note.soft {{ background: #fdeaee; color: {RED}; border: 3px solid rgba(200,16,46,.3); }}
.note.ink {{ background: {INK}; color: #fff; }} .note.ok {{ background: #e6f4ea; color: {GREEN}; border: 3px solid rgba(24,128,56,.35); }}
.note.blue {{ background: #e8f0fe; color: {BLUE}; border: 3px solid rgba(11,87,208,.3); }}
.dev {{ position: absolute; background: {DARK}; border-radius: 40px; padding: 16px; box-shadow: 0 30px 70px rgba(26,26,26,.28); }}
.view {{ position: relative; overflow: hidden; border-radius: 26px; background: #fff; }}
.zoom {{ position: absolute; left: 0; top: 0; transform-origin: 0 0; }}
.zoom img {{ display: block; }}
.ring {{ position: absolute; border: 6px solid {RED}; border-radius: 12px; box-shadow: 0 0 0 6px rgba(200,16,46,.18); }}
.tap {{ position: absolute; width: 64px; height: 64px; border-radius: 50%; background: rgba(200,16,46,.35); border: 4px solid {RED}; }}
.close {{ position: absolute; background: #fff; border: 4px solid {RED}; border-radius: 16px; padding: 10px; box-shadow: 0 18px 40px rgba(26,26,26,.15); }}
.close img {{ display: block; }}
.closel {{ position: absolute; background: {RED}; color: #fff; font-weight: 800; font-size: 28px; letter-spacing: 3px; padding: 6px 14px; border-radius: 8px; }}
.flow {{ position: absolute; border-radius: 22px; background: #fff; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 0 22px;
  box-shadow: 0 18px 40px rgba(26,26,26,.10); }}
.flow b {{ font-size: 34px; line-height: 1.15; }} .flow span {{ font-size: 28px; color: {MUTED}; margin-top: 10px; line-height: 1.2; }}
.arrow {{ position: absolute; height: 6px; background: {MUTED}; border-radius: 3px; transform-origin: 0 50%; }}
.arrow:after {{ content: ""; position: absolute; right: -4px; top: -9px; border-left: 20px solid {MUTED}; border-top: 12px solid transparent; border-bottom: 12px solid transparent; }}
.btn {{ display: inline-block; padding: 18px 30px; border-radius: 14px; color: #fff; font-weight: 800; font-size: 32px; box-shadow: 0 10px 24px rgba(0,0,0,.18); }}
.ok-tick {{ width: 64px; height: 64px; border-radius: 50%; background: {GREEN}; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 36px; flex: none; }}
'''
PHONE_SVG = lambda c: f'<svg width="54" height="54" viewBox="0 0 24 24"><rect x="6.5" y="2" width="11" height="20" rx="2.4" fill="{c}"/><rect x="8" y="4.2" width="8" height="13.5" rx=".6" fill="#fff"/></svg>'
PERSON = lambda c: f'<svg width="120" height="120" viewBox="0 0 24 24"><circle cx="12" cy="7.5" r="4" fill="{c}"/><path d="M3.5 21c.9-4.6 4.2-7 8.5-7s7.6 2.4 8.5 7z" fill="{c}"/></svg>'


class Scene:
    def __init__(s, sc):
        s.sc = sc; s.id = sc["id"]; s.n = int(sc["id"][1:]); s.dur = sc["dur"]; s.start = sc["start"]; s.L = sc["lines"]; s.els, s.js, s.init = [], [], []

    def t(s, i, d=0.0): return R(s.L[min(i, len(s.L) - 1)]["t0"] + d)

    def find(s, pat, default=None, after=-1):
        for l in s.L:
            if l["i"] > after and re.search(pat, l["text"], re.I): return l["i"]
        return default

    def tw(s, sel, t, d, p, ease="power3.out"): s.js.append(f'tl.to("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in p.items())},duration:{R(d)},ease:"{ease}"}},{R(t)});')
    def st(s, sel, t, p): s.js.append(f'tl.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in p.items())}}},{R(t)});')
    def gs(s, sel, p): s.init.append(f'gsap.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in p.items())}}});')

    def add(s, eid, inner, style="", cls="a", t_in=None, t_out=None, enter="up", sfx=None):
        s.els.append(f'<div id="{eid}" class="{cls}" style="{style}">{inner}</div>')
        if t_in is not None:
            fr = {"up": {"opacity": 0, "y": 40}, "left": {"opacity": 0, "x": -70}, "right": {"opacity": 0, "x": 70}, "pop": {"opacity": 0, "scale": 0.7},
                  "fade": {"opacity": 0}, "draw": {"scaleX": 0}}[enter]
            s.gs(f"#{eid}", fr); to = {k: (1 if k in ("opacity", "scale", "scaleX") else 0) for k in fr}
            s.tw(f"#{eid}", t_in, 0.5 if enter != "pop" else 0.45, to, "back.out(1.6)" if enter == "pop" else "power3.out")
            if sfx: CUES.append((R(s.start + t_in), sfx[0], sfx[1]))
        if t_out is not None: s.tw(f"#{eid}", t_out - 0.35, 0.35, {"opacity": 0}, "power2.in")

    def pulse(s, eid, t, scale=1.06): s.tw(f"#{eid}", t, 0.22, {"scale": scale}, "power2.out"); s.tw(f"#{eid}", t + 0.22, 0.35, {"scale": 1}, "power2.inOut")

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


def deck_text(n):
    d = dict(kick=None, title=None, body=[], foot=None)
    for q in SL[n]["texts"]:
        t = q["t"]
        if t == "CLOSE-UP" or re.fullmatch(r"\d+", t): continue
        if d["kick"] is None and t.isupper(): d["kick"] = t
        elif d["title"] is None: d["title"] = t
        elif t.startswith(("Shown:", "Sample shown")): d["foot"] = t
        else: d["body"].append(t)
    return d


def role_badge(S, n, x, y, t_in):
    r = SL[n].get("role") or {}
    if r.get("text") in ROLE:
        S.add("role", f'{PHONE_SVG("#fff")}<span>{esc(r["text"])}</span>', f"left:{x}px;top:{y}px;background:{ROLE[r['text']]}", "a role", t_in, None, "left", ("curated/ui-pop.wav", -18))
        return True
    return False


def shot_device(S, n, x, y, vw, vh_max, t_in):
    """deck screenshot in a device frame; rings on the deck's boxes (inside the zoom layer) + punch-in; returns geometry"""
    sh = SL[n]["shot"]; k = vw / sh["size"][0]; ih = sh["size"][1] * k; vh = min(vh_max, ih)
    rings = ""
    for j, b in enumerate(sh["boxes"]):
        rings += f'<div id="rg{j}" class="ring" style="left:{R(b["x"] * k - 7)}px;top:{R(b["y"] * k - 7)}px;width:{R(b["w"] * k + 14)}px;height:{R(b["h"] * k + 14)}px"></div>'
    S.add("dv", f'<div class="view" style="width:{vw}px;height:{R(vh)}px"><div class="zoom" id="dv_z"><img src="assets/deck/{sh["src"]}" style="width:{vw}px;height:{R(ih)}px" alt="">{rings}</div></div>',
          f"left:{x}px;top:{y}px", "dev", t_in, None, "up")
    return dict(k=k, ih=ih, vh=vh, vw=vw, x=x, y=y, boxes=sh["boxes"])


def highlight(S, g, t_hi, t_out=None):
    """rings pop, pulse; the screenshot scrolls/punches in on the field"""
    boxes = g["boxes"]; k, vw, vh, ih = g["k"], g["vw"], g["vh"], g["ih"]
    if not boxes:
        if ih > vh + 10: S.tw("#dv_z", t_hi, max(3.0, S.dur - t_hi - 2), {"y": R(-(ih - vh))}, "power1.inOut")
        return
    for j in range(len(boxes)):
        tb = t_hi + 0.9 * j
        S.gs(f"#rg{j}", {"opacity": 0, "scale": 1.25, "transformOrigin": "50% 50%"}); S.tw(f"#rg{j}", tb, 0.4, {"opacity": 1, "scale": 1}, "back.out(1.8)")
        S.tw(f"#rg{j}", tb + 0.6, 0.5, {"scale": 1.05}, "sine.inOut"); S.tw(f"#rg{j}", tb + 1.1, 0.5, {"scale": 1}, "sine.inOut")
        CUES.append((R(S.start + tb), "curated/ui-click.wav", -18))
    x0 = min(b["x"] for b in boxes) * k; y0 = min(b["y"] for b in boxes) * k; x1 = max(b["x"] + b["w"] for b in boxes) * k; y1 = max(b["y"] + b["h"] for b in boxes) * k
    z = max(1.0, min(1.8, 0.85 * vw / max(1, x1 - x0), 0.6 * vh / max(1, y1 - y0)))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    tx = min(0, max(vw - vw * z, vw / 2 - cx * z)); ty = min(0, max(vh - ih * z, vh / 2 - cy * z))
    if abs(z - 1) > 0.05 or abs(ty) > 4:
        zt = t_hi + 0.8 + 0.9 * (len(boxes) - 1)
        S.tw("#dv_z", zt, 0.9, {"scale": R(z), "x": R(tx), "y": R(ty)}, "power3.inOut")
        S.tw("#dv_z", (t_out or S.dur) - 1.3, 0.9, {"scale": 1, "x": 0, "y": 0}, "power3.inOut")
    b = boxes[0]
    S.els.append(f'<div id="tp" class="tap" style="left:{R(g["x"] + 16 + (b["x"] + b["w"] / 2) * k - 32)}px;top:{R(g["y"] + 16 + min(vh - 20, (b["y"] + b["h"] / 2) * k) - 32)}px"></div>')
    S.gs("#tp", {"opacity": 0, "scale": 0.3}); S.st("#tp", t_hi, {"opacity": 1}); S.tw("#tp", t_hi, 0.6, {"scale": 1.6, "opacity": 0}, "power2.out")


HI = r"\b(tap|look for|look at|find|check the code|locate|enter|start with|choose|scroll|sign|read)\b"


def generic(sc):
    S = Scene(sc); n = S.n; d = deck_text(n); sh = SL[n]["shot"]; last = len(S.L) - 1
    wide = sh["size"][0] > sh["size"][1] * 1.1
    if wide:
        g = shot_device(S, n, 110, 330, 1080, 640, 0.15); x0, wtxt = 1290, 520
    else:
        g = shot_device(S, n, 200, 150, 380, 730, 0.15); x0, wtxt = 760, 1000
    ty = 150 if not wide else 150
    if d["kick"]: S.add("kick", esc(d["kick"]), f"left:{x0 if not wide else 110}px;top:{ty}px", "a kick", 0.25, None, "left")
    y = ty + 50
    if role_badge(S, n, x0 if not wide else 110, y, 0.35): y += 80
    S.add("ttl", f'<div class="h1" style="max-width:{wtxt if not wide else 1700}px">{esc(d["title"] or sc["title"])}</div>', f"left:{x0 if not wide else 110}px;top:{y}px", "a", 0.4, None, "left",
          ("curated/zoom-swish.wav", -22))
    hi = S.find(HI, 0)
    if wide:
        for j, b in enumerate(d["body"][:3]):
            S.add(f"bd{j}", esc(b), f"left:{x0}px;top:{340 + j * 170}px;width:{wtxt}px", "a t", S.t(min(1 + j, last)) + 0.2, None, "up")
    else:
        y += 150 if len(d["title"] or "") > 24 else 85
        for j, b in enumerate(d["body"][:2]):
            S.add(f"bd{j}", esc(b), f"left:{x0}px;top:{y}px;width:{wtxt}px", "a t", S.t(min(1 + j, last)) + 0.2, None, "up"); y += 100 if len(b) > 55 else 60
        cl = SL[n].get("close")
        if cl:
            cw = min(880, cl["size"][0] * 2.0); ch = cl["size"][1] * cw / cl["size"][0]
            if ch > 200: cw *= 200 / ch; ch = 200
            yc = max(y + 30, 560)
            S.add("cll", "CLOSE-UP", f"left:{x0}px;top:{R(yc - 46)}px", "closel", S.t(hi) + 0.9, None, "fade")
            S.add("cl", f'<img src="assets/deck/{cl["src"]}" style="width:{R(cw)}px;height:{R(ch)}px" alt="">', f"left:{x0}px;top:{R(yc)}px", "close", S.t(hi) + 1.0, None, "up", ("curated/ui-pop.wav", -18))
            S.tw("#cl", S.t(hi) + 1.8, 0.3, {"scale": 1.04}, "power2.out"); S.tw("#cl", S.t(hi) + 2.1, 0.4, {"scale": 1}, "power2.inOut")
    if d["foot"]: S.add("foot", esc(d["foot"]), f"left:{x0 if not wide else 110}px;top:860px;font-size:28px;color:{MUTED};font-weight:600", "a", 1.0, None, "fade")
    highlight(S, g, S.t(hi) + 0.3)
    return S


# ---------------- bespoke scenes ----------------
def s01(sc):
    S = Scene(sc); d = deck_text(1); sh = SL[1]["shot"]
    S.add("bg", "", f"left:0;top:0;width:1920px;height:1080px;background:{RED}", "a", None, None)
    S.add("k", "STAFF GUIDE · AA/SEC/F/070", "left:150px;top:260px;color:rgba(255,255,255,.85)", "a kick", None)
    S.add("ttl", "FOCA Checklist", "left:150px;top:310px;color:#fff;font-size:110px", "a h1", None)
    S.add("sub", "Fill in, sign and save on your phone", "left:150px;top:460px;color:#fff;font-size:42px;font-weight:700", "a", 0.4, None, "left")
    k = 380 / sh["size"][0]
    S.add("dv", f'<div class="view" style="width:380px;height:{R(sh["size"][1] * k)}px"><img src="assets/deck/{sh["src"]}" style="width:380px;display:block" alt=""></div>', "left:1300px;top:120px", "dev", 0.2, None, "right")
    seq = [("Security", "fills in the checklist", BLUE, 1), ("Airline Rep", "signs", ORANGE, 2), ("Security Rep", "signs and saves", BLUE, 3)]
    for i, (who, what, c, li) in enumerate(seq):
        S.add(f"sq{i}", f'<span class="role" style="background:{c}">{who}</span><span style="color:#fff;font-size:34px;font-weight:700">{what}</span>', f"left:150px;top:{600 + i * 95}px",
              "a row", S.t(li) + 0.2, None, "left", ("curated/ui-pop.wav", -17))
    S.add("same", f'{PHONE_SVG("#fff")}<span>Both representatives use the same phone</span>', "left:150px;top:900px;color:#fff;font-size:32px;font-weight:700;gap:14px", "a row", S.t(4) + 0.2, None, "up")
    return S


def s02(sc):
    S = Scene(sc)
    S.add("k", "AA/SEC/F/070", "left:150px;top:150px", "a kick", 0.2, None, "left"); S.add("ttl", "Who does what", "left:150px;top:200px", "a h1", 0.3, None, "left")
    parts = [("1", "SECURITY STAFF", BLUE, "Fill in the checklist", 1), ("2", "AIRLINE REPRESENTATIVE", ORANGE, "Check the details, type own name and ID, sign", 2),
             ("3", "SECURITY REPRESENTATIVE", BLUE, "Type own name and ID, sign, save the record", 3)]
    for i, (num, who, c, what, li) in enumerate(parts):
        x = 150 + i * 560
        S.add(f"p{i}", f'<div style="display:flex;justify-content:center;margin-top:30px">{PERSON(c)}</div><div style="text-align:center;margin-top:10px"><span class="role" style="background:{c};font-size:28px">{num} · {who}</span></div>'
              f'<div class="h3" style="text-align:center;padding:24px 30px 0">{what}</div>', f"left:{x}px;top:340px;width:520px;height:440px", "card", S.t(li) + 0.2, None, "up", ("curated/ui-pop.wav", -16))
        if i: S.add(f"pa{i}", "", f"left:{x - 36}px;top:560px;width:30px", "arrow", S.t(li) + 0.1, None, "draw")
    return S


def s03(sc):
    S = Scene(sc)
    S.add("k", "BEFORE YOU START", "left:150px;top:150px", "a kick", 0.2, None, "left"); S.add("ttl", "Rules for every FOCA", "left:150px;top:200px", "a h1", 0.3, None, "left")
    rules = [("Use your AirAsia (@airasia.com) Google account", 0), ("Type your own name and ID when it is your turn", 2), ("Sign for yourself. Never sign for someone else", 3), ("One case = one new form", 5)]
    for i, (r, li) in enumerate(rules):
        S.add(f"r{i}", f'<div class="num">{i + 1}</div><div class="h2" style="max-width:1400px">{r}</div>', f"left:150px;top:{340 + i * 135}px", "a row", S.t(li) + 0.2, None, "left", ("curated/ui-pop.wav", -17))
    S.pulse("r2", S.t(4) + 0.2)
    return S


def s04(sc):
    S = Scene(sc)
    S.add("k", "STEP 1", "left:150px;top:150px", "a kick", 0.2, None, "left"); S.add("ttl", "Get the app link", "left:150px;top:200px", "a h1", 0.3, None, "left")
    for i, (txt, li) in enumerate((("Ask your supervisor for the app link", 0), ("Or use the QR code shown here", 1), ("Open your camera, point it at the code, tap the link", 2))):
        S.add(f"st{i}", f'<div class="num">{i + 1}</div><div class="h3" style="max-width:820px">{txt}</div>', f"left:150px;top:{350 + i * 150}px", "a row", S.t(li) + 0.3, None, "left", ("curated/ui-pop.wav", -17))
    S.add("only", "The link only works for AirAsia Google accounts", f"left:150px;top:820px;width:900px", "note blue", S.t(2) + 2.0, None, "up")
    S.add("qr", '<img src="assets/deck/image-4-1.png" style="width:440px;height:440px;display:block" alt=""><div style="text-align:center;font-weight:700;font-size:30px;margin-top:10px">Scan to open the app</div>',
          "left:1230px;top:220px;padding:30px", "card", S.t(1) + 0.3, None, "pop")
    S.add("sl", "", f"left:1260px;top:252px;width:440px;height:6px;background:{RED};box-shadow:0 0 18px {RED}", "a", S.t(2) + 0.3, None, "fade")
    S.tw("#sl", S.t(2) + 0.3, 1.5, {"y": 430}, "power1.inOut"); S.tw("#sl", S.t(2) + 1.8, 1.5, {"y": 0}, "power1.inOut")
    S.pulse("qr", S.t(1) + 1.6, 1.04)
    return S


def s05(sc):
    S = Scene(sc)
    S.add("k", "STEP 2", "left:150px;top:150px", "a kick", 0.2, None, "left"); S.add("ttl", "Open the app in Chrome", "left:150px;top:200px", "a h1", 0.3, None, "left")
    steps = [("Open Chrome on your phone", 0), ("Paste the link, or open the scanned link in Chrome", 1), ("If asked, choose your AirAsia account", 3), ("Wait for the list of 4 forms", 4)]
    for i, (txt, li) in enumerate(steps):
        S.add(f"st{i}", f'<div class="num">{i + 1}</div><div class="h3" style="max-width:1000px">{txt}</div>', f"left:150px;top:{340 + i * 125}px", "a row", S.t(li) + 0.2, None, "left", ("curated/ui-pop.wav", -17))
    S.add("tip", '<div style="font-size:28px;letter-spacing:3px;opacity:.85">TIP</div>Chrome ⋮ menu → Add to Home screen: one tap next time', "left:150px;top:860px;width:1100px", "note blue", S.t(5) + 0.3, None, "up")
    for i in range(4):
        S.add(f"f{i}", "", f"left:{1400}px;top:{330 + i * 120}px;width:360px;height:96px;border-radius:16px;background:#fff;box-shadow:0 10px 24px rgba(0,0,0,.1);border-left:10px solid {RED if i == 0 else '#dadce0'}",
              "a", S.t(4) + 0.3 + 0.2 * i, None, "up")
    S.add("fl", "4 forms", f"left:1400px;top:820px;font-size:34px;font-weight:800;color:{INK}", "a", S.t(4) + 1.2, None, "fade")
    return S


def s07(sc):
    S = Scene(sc); sh = SL[7]["shot"]; k = 1180 / sh["size"][0]
    S.add("k", "THE WHOLE FORM", "left:110px;top:150px", "a kick", 0.2, None, "left"); S.add("ttl", "Scroll down to see it all", "left:110px;top:200px", "a h1", 0.3, None, "left")
    S.add("dv", f'<div class="view" style="width:1180px;height:{R(sh["size"][1] * k)}px"><img src="assets/deck/{sh["src"]}" style="width:1180px;display:block" alt=""></div>', "left:110px;top:310px", "dev", 0.4, None, "up")
    for i, (lab, li) in enumerate((("Top: flight details", 0), ("Middle: the checklist", 1), ("Bottom: blue Next button", 2))):
        S.add(f"lb{i}", f'<div class="num" style="width:56px;height:56px;font-size:28px">{i + 1}</div><div class="h3">{lab}</div>', f"left:1360px;top:{360 + i * 140}px", "a row", S.t(li) + 0.3, None, "left",
              ("curated/ui-pop.wav", -17))
    S.add("go", "Then go back to the top to start", "left:1360px;top:800px;width:470px", "note ink", S.t(4) + 0.2, None, "up")
    return S


def s17(sc):
    S = Scene(sc)
    S.add("k", "STEP 12", "left:150px;top:150px", "a kick", 0.2, None, "left"); S.add("ttl", "Phone back to Security", "left:150px;top:200px", "a h1", 0.3, None, "left")
    S.add("pa", f'<div style="display:flex;justify-content:center">{PERSON(ORANGE)}</div><div style="text-align:center"><span class="role" style="background:{ORANGE};font-size:28px">AIRLINE REPRESENTATIVE</span></div>',
          "left:160px;top:360px;width:520px;height:260px", "a", 0.4, None, "up")
    S.add("ps", f'<div style="display:flex;justify-content:center">{PERSON(BLUE)}</div><div style="text-align:center"><span class="role" style="background:{BLUE};font-size:28px">SECURITY REPRESENTATIVE</span></div>',
          "left:1240px;top:360px;width:520px;height:260px", "a", 0.6, None, "up")
    S.add("ph", f'<div style="width:150px;height:260px;border-radius:24px;background:{DARK};padding:10px"><div data-layout-ignore style="width:130px;height:240px;border-radius:16px;background:#fff;font-size:15px;font-weight:700;text-align:center;padding:30px 8px;line-height:1.3">Hand the phone back to SECURITY STAFF</div></div>',
          "left:640px;top:340px", "a", S.t(0) + 0.3, None, "pop")
    S.tw("#ph", S.t(0) + 2.0, 1.6, {"x": 470}, "power2.inOut"); CUES.append((R(S.start + S.t(0) + 2.0), "curated/zoom-swish.wav", -14))
    S.add("msg", "Screen says: “Hand the phone back to SECURITY STAFF”", "left:150px;top:690px;width:1620px;text-align:center", "note ink", S.t(0) + 0.4, None, "up")
    S.add("btn", "Security staff has the phone", f"left:660px;top:820px;background:{BLUE}", "a btn", S.t(1) + 0.3, None, "pop", ("curated/ui-click.wav", -14))
    S.pulse("btn", S.t(1) + 1.6)
    return S


def s22(sc):
    S = Scene(sc)
    S.add("k", "IF IT SAYS “NOT SAVED”", "left:150px;top:150px", "a kick", 0.2, None, "left"); S.add("ttl", "Do not start again", "left:150px;top:200px", "a h1", 0.3, None, "left")
    S.add("ns", "✕  Not saved", f"left:1280px;top:200px;background:#fdeaee;color:{RED};font-size:40px;font-weight:800;padding:20px 34px;border-radius:16px;border:3px solid {RED}", "a", S.t(0) + 0.2, None, "pop",
          ("curated/ui-click.wav", -14))
    steps = [("Stay on the same screen", 0), ("Your answers and signatures are still there", 1), ("Check your mobile data or Wi-Fi", 2), ("Tap Save again and wait for the confirmation", 3)]
    for i, (txt, li) in enumerate(steps):
        S.add(f"st{i}", f'<div class="num">{i + 1}</div><div class="h2" style="max-width:1400px">{txt}</div>', f"left:150px;top:{350 + i * 135}px", "a row", S.t(li) + 0.2, None, "left", ("curated/ui-pop.wav", -17))
    S.add("sv", f'<span class="btn" style="background:{GREEN}">Save record (PDF to Drive + Sheet)</span>', "left:1180px;top:820px", "a", S.t(3) + 1.0, None, "pop")
    return S


def s27(sc):
    S = Scene(sc)
    S.add("k", "WHERE THE PDF IS SAVED", "left:150px;top:150px", "a kick", 0.2, None, "left"); S.add("ttl", "Google Drive", "left:150px;top:200px", "a h1", 0.3, None, "left")
    i_md, i_ss, i_fo = S.find(r"My Drive"), S.find(r"Signed Forms"), S.find(r"open FOCA")
    S.add("md", "My Drive", f"left:150px;top:340px;width:520px;font-size:36px;font-weight:700;padding:18px 28px;background:#fff;border-radius:14px;box-shadow:0 10px 24px rgba(0,0,0,.08)", "a", S.t(i_md) + 0.2, None, "left",
          ("curated/ui-pop.wav", -16))
    S.add("ln1", "", f"left:200px;top:410px;width:6px;height:90px;background:#bdc1c6", "a", S.t(i_ss), None, "fade")
    S.add("ss", "AA-SEC Signed Forms (RESTRICTED)", f"left:230px;top:470px;width:700px;font-size:34px;font-weight:800;padding:18px 28px;background:{RED};color:#fff;border-radius:14px", "a", S.t(i_ss) + 0.2, None, "left",
          ("curated/ui-pop.wav", -16))
    S.add("ln2", "", f"left:280px;top:540px;width:6px;height:90px;background:#bdc1c6", "a", S.t(i_fo), None, "fade")
    S.add("fo", "FOCA", f"left:310px;top:600px;width:620px;font-size:36px;font-weight:800;padding:18px 28px;background:{BLUE};color:#fff;border-radius:14px", "a", S.t(i_fo) + 0.2, None, "left",
          ("curated/ui-pop.wav", -16))
    S.add("pdf", "📄  FOCA_&lt;flight&gt;_&lt;date&gt;_&lt;Record ID&gt;.pdf", f"left:310px;top:740px;width:900px;font-size:32px;font-weight:700;padding:18px 28px;background:#fdeaee;color:{RED};border-radius:14px;border:2px dashed {RED}",
          "a", S.t(S.find(r"file name starts")) + 0.2, None, "up")
    S.add("adds", '<b>Every save adds</b><br>• 1 new signed PDF in this folder<br>• 1 new row in the records Sheet', "left:1250px;top:340px;width:540px;font-size:32px;line-height:1.5", "card", S.t(0) + 0.4, None, "right")
    S.els[-1] = S.els[-1].replace('class="card" style="', 'class="card" style="padding:30px;')
    S.add("only", "Only authorised people open this folder", "left:1250px;top:640px;width:540px", "note soft", S.t(2) + 0.3, None, "up")
    S.add("tip", "Just saved? Tap “Open the completed PDF” on the Saved screen", "left:1250px;top:820px;width:540px;font-size:28px", "note ink", S.t(S.find(r"straight from")) + 0.3, None, "up")
    return S


def s28(sc):
    S = Scene(sc)
    S.add("k", "WHERE THE RECORD IS SAVED", "left:150px;top:150px", "a kick", 0.2, None, "left"); S.add("ttl", "Google Sheets: one row per save", "left:150px;top:200px", "a h1", 0.3, None, "left")
    S.add("sh", "Sheet: FOCA Records  ·  in the same FOCA folder as the PDFs", f"left:150px;top:320px;width:1620px;font-size:32px;font-weight:800;padding:18px 28px;background:#e6f4ea;color:{GREEN};border-radius:14px",
          "a", S.t(0) + 0.3, None, "up")
    cols = ["Record ID", "Saved at (MYT)", "Flight Number", "Airline Rep", "Security Rep", "PDF file"]
    row = ["FOCA-20261111-110458-4003", "2026-11-11 11:04:58", "TEST001", "TEST Airline Rep", "TEST Security Rep", "link to the PDF"]
    W = [400, 300, 210, 240, 260, 210]                                   # = 1620 px; one-line cells
    cell = lambda bg, col, wt: f"height:60px;line-height:60px;padding:0 12px;white-space:nowrap;overflow:hidden;background:{bg};color:{col};font-weight:{wt};font-size:26px"
    head = "".join(f'<div id="hc{i}" data-layout-ignore style="width:{w}px;{cell(GREEN, '#fff', 800)}">{c}</div>' for i, (c, w) in enumerate(zip(cols, W)))
    body = "".join(f'<div id="rc{i}" data-layout-ignore style="width:{w}px;{cell('#fff', INK, 600)};border-right:1px solid #e0e0e0">{c}</div>' for i, (c, w) in enumerate(zip(row, W)))
    S.add("tbl", f'<div style="display:flex">{head}</div><div style="display:flex;border-bottom:1px solid #e0e0e0">{body}</div><div style="font-size:28px;color:{MUTED};padding:10px 4px;font-weight:600">Example: the TEST row</div>',
          "left:150px;top:440px", "a", S.t(1) + 0.3, None, "up")
    for i in range(6):
        S.st(f"#hc{i}", S.t(1) + 0.9 + 0.5 * i, {"background": RED}); S.st(f"#hc{i}", S.t(1) + 1.4 + 0.5 * i, {"background": GREEN})
    S.add("rg", "", f"left:142px;top:494px;width:1636px;height:72px;border:6px solid {RED};border-radius:10px", "a", S.t(2) + 0.2, None, "pop", ("curated/ui-click.wav", -16))
    S.add("rg2", "", f"left:{150 + sum(W[:5]) - 8}px;top:494px;width:{W[5] + 16}px;height:72px;border:6px solid {BLUE};border-radius:10px", "a", S.t(2) + 2.0, None, "pop")
    S.add("find", "Find a checklist later: search the Record ID, tap the PDF link on that row", "left:150px;top:690px;width:1620px", "note ink", S.t(2) + 0.3, None, "up")
    S.add("auto", "The app writes the row automatically. Leave the rows as they are.", "left:150px;top:820px;width:1620px", "note soft", S.t(3) + 0.3, None, "up")
    return S


def s30(sc):
    S = Scene(sc); pr = S.find(r"practise")
    S.add("bg", "", f"left:0;top:0;width:1920px;height:1080px;background:{DARK}", "a", None, None)
    S.add("k", "FOCA · QUICK CHECK", "left:150px;top:150px;color:#ff6b7f", "a kick", 0.2, None, "left"); S.add("ttl", "Five questions, every time", "left:150px;top:200px;color:#fff", "a h1", 0.3, S.t(pr), "left")
    qs = ["Flight details and date correct?", "One answer on every checklist line?", "Airline Rep: own name and ID, signed?", "Security Rep: own name and ID, signed?", "Saw “Saved” and both signatures in the PDF?"]
    for i, q in enumerate(qs):
        S.add(f"q{i}", f'<div class="ok-tick" id="qt{i}" style="background:#3c4043">{i + 1}</div><div class="h2" style="color:#fff">{q}</div>', f"left:150px;top:{330 + i * 112}px", "a row", S.t(1 + i) + 0.1, S.t(pr), "left",
              ("curated/ui-pop.wav", -17))
        S.st(f"#qt{i}", S.t(1 + i) + 1.4, {"background": GREEN}); CUES.append((R(S.start + S.t(1 + i) + 1.4), "clean-ding.wav", -19))
    S.add("p1", "Let’s practise one case together", "left:150px;top:300px;color:#fff;width:1620px", "a h1", S.t(pr) + 0.2, None, "up")
    for i, (who, c) in enumerate((("Security staff", BLUE), ("Airline Rep", ORANGE), ("Security Rep", BLUE))):
        S.add(f"pw{i}", f'{PHONE_SVG("#fff")}<span>{who}</span>', f"left:{150 + i * 430}px;top:470px;background:{c};font-size:32px", "a role", S.t(pr + 1) + 0.4 + 0.6 * i, None, "up")
        if i: S.add(f"pwa{i}", "", f"left:{150 + i * 430 - 50}px;top:500px;width:40px;background:#9aa0a6", "arrow", S.t(pr + 1) + 0.3 + 0.6 * i, None, "draw")
    S.add("p2", "At each step: who holds the phone, and which button they tap?", "left:150px;top:600px;width:1620px;font-size:34px", "note ink", S.t(pr + 1) + 2.4, None, "up")
    S.add("p3", "At the end: show where the signed PDF is, and its row in Google Sheets", "left:150px;top:740px;width:1620px;font-size:34px", "note red", S.t(pr + 2) + 0.3, None, "up")
    return S


BESPOKE = {"s01": s01, "s02": s02, "s03": s03, "s04": s04, "s05": s05, "s07": s07, "s17": s17, "s22": s22, "s27": s27, "s28": s28, "s30": s30}
scenes = []
for sc in T["scenes"]:
    S = BESPOKE[sc["id"]](sc) if sc["id"] in BESPOKE else generic(sc); scenes.append(S); S.write()
CUES.extend((R(sc["start"]), "curated/zoom-swish.wav", -20) for sc in T["scenes"][1:])

# ---------------- chrome ----------------
ch_els = [f'<div id="ctag" class="a" style="left:110px;top:40px;font-size:28px;font-weight:700;letter-spacing:1.5px;color:{MUTED}">AA/SEC/F/070 · FOCA CHECKLIST · STAFF TRAINING</div>',
          f'<div id="pbar" class="a" style="left:0;top:1072px;width:1920px;height:8px;background:{RED};transform-origin:0 50%"></div>']
ch_init = ['gsap.set("#pbar",{scaleX:0});', 'gsap.set("#ctag",{opacity:0});']; ch_js = [f'tl.to("#pbar",{{scaleX:1,duration:{R(TOTAL)},ease:"none"}},0);']
for i, sc in enumerate(T["scenes"]):
    if sc["id"] in ("s01", "s30"): continue
    ch_els.append(f'<div id="chap{i}" class="a" style="right:110px;top:40px;font-size:28px;font-weight:700;color:{INK};text-align:right">{i + 1:02d} / {len(T["scenes"])} · {esc(sc["title"])}</div>')
    ch_init.append(f'gsap.set("#chap{i}",{{opacity:0}});')
    ch_js.append(f'tl.to("#chap{i}",{{opacity:1,duration:0.4}},{R(sc["start"] + 0.2)});'); ch_js.append(f'tl.to("#chap{i}",{{opacity:0,duration:0.3}},{R(sc["start"] + sc["dur"] - 0.3)});')
s2, s30 = T["scenes"][1], T["scenes"][-1]
ch_js.append(f'tl.to("#ctag",{{opacity:1,duration:0.4}},{R(s2["start"])});'); ch_js.append(f'tl.to("#ctag",{{opacity:0,duration:0.3}},{R(s30["start"])});')
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
    .cap span {{ display: inline; background: rgba(26,26,26,.9); color: #fff; font-size: 36px; font-weight: 600; line-height: 1.5; padding: 6px 18px; border-radius: 10px;
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
