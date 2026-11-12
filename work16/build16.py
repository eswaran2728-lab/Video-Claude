# AA/SEC/F/077 attendance training video -> edit/ (HyperFrames project): index.html mounts one scene per slide
# (compositions/sNN.html), a chrome layer (form code, chapter, progress) and one captions layer; the voice + music + SFX mix is
# assets/mix.wav (mix16.py). Every reveal is placed at the start of the voice line that names it (timing.json from tts16.py).
# Visual language follows the creator's deck: navy ink, Check-in green, Check-out red, light panels, Inter; the deck's own
# sample QR images and Google Form / Sheet screenshots are reused (assets/deck/).
import json, html, math, os, re
T = json.load(open("timing.json")); TOTAL = T["total"]
INK, NAVY, GREEN, RED, BG, MUTED, AMBER = "#14213d", "#1b2a4a", "#1e8a4c", "#d6203a", "#f3f5f9", "#5b6577", "#f5a524"
R = lambda v: round(v, 3); esc = html.escape
os.makedirs("edit/compositions", exist_ok=True)
CUES = []                                                          # (abs time, sfx, gain) for mix16.py

COMMON_CSS = f'''
#root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; color: {INK}; overflow: hidden; }}
.a {{ position: absolute; }}
.card {{ position: absolute; background: #fff; border-radius: 22px; box-shadow: 0 18px 40px rgba(20,33,61,.12); }}
.pill {{ display: inline-block; padding: 10px 26px; border-radius: 40px; color: #fff; font-weight: 800; letter-spacing: 1.5px; font-size: 30px; }}
.g {{ background: {GREEN}; }} .r {{ background: {RED}; }} .n {{ background: {NAVY}; }} .am {{ background: {AMBER}; }}
.h1 {{ font-weight: 800; font-size: 64px; line-height: 1.08; letter-spacing: -1px; }}
.h2 {{ font-weight: 800; font-size: 46px; line-height: 1.12; }}
.h3 {{ font-weight: 700; font-size: 36px; line-height: 1.2; }}
.t {{ font-weight: 500; font-size: 30px; line-height: 1.32; color: {MUTED}; }}
.num {{ width: 64px; height: 64px; border-radius: 50%; color: #fff; font-weight: 800; font-size: 32px; display: flex; align-items: center; justify-content: center; }}
.row {{ display: flex; align-items: center; gap: 22px; }}
.ok {{ color: {GREEN}; }} .bad {{ color: {RED}; }}
.note {{ position: absolute; border-radius: 18px; padding: 22px 30px; font-size: 32px; font-weight: 700; line-height: 1.25; }}
.note.red {{ background: #fde8eb; color: {RED}; border: 3px solid rgba(214,32,58,.35); }}
.note.green {{ background: #e5f5ec; color: {GREEN}; border: 3px solid rgba(30,138,76,.35); }}
.note.navy {{ background: {NAVY}; color: #fff; }}
.hl {{ position: absolute; border: 6px solid {AMBER}; border-radius: 12px; box-shadow: 0 0 0 9999px rgba(20,33,61,0); }}
.shot {{ position: absolute; border-radius: 16px; box-shadow: 0 18px 40px rgba(20,33,61,.18); background: #fff; overflow: hidden; }}
.shot img {{ display: block; width: 100%; height: 100%; }}
.qr {{ position: absolute; background: #fff; border-radius: 22px; padding: 18px; box-shadow: 0 18px 40px rgba(20,33,61,.15); }}
.qr img {{ display: block; width: 100%; height: 100%; }}
.x, .v {{ width: 58px; height: 58px; border-radius: 50%; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 34px; flex: none; }}
.x {{ background: {RED}; }} .v {{ background: {GREEN}; }}
.phone {{ position: absolute; width: 400px; height: 760px; border-radius: 56px; background: #0f1830; padding: 18px; box-shadow: 0 30px 60px rgba(20,33,61,.3); }}
.screen {{ position: absolute; left: 18px; top: 18px; right: 18px; bottom: 18px; border-radius: 40px; background: #fff; overflow: hidden; }}
.gf {{ position: absolute; inset: 0; background: #ede7f6; }}
.gfc {{ position: absolute; left: 16px; right: 16px; background: #fff; border-radius: 12px; }}
.gfbar {{ height: 12px; background: #673ab7; border-radius: 12px 12px 0 0; }}
.gft {{ padding: 16px 18px; font-size: 25px; line-height: 1.25; color: #202124; }}
.arrow {{ position: absolute; height: 6px; background: {MUTED}; border-radius: 3px; transform-origin: 0 50%; }}
.arrow:after {{ content: ""; position: absolute; right: -4px; top: -9px; border-left: 20px solid {MUTED}; border-top: 12px solid transparent; border-bottom: 12px solid transparent; }}
.flow {{ position: absolute; height: 150px; border-radius: 20px; background: {NAVY}; color: #fff; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 0 18px; }}
.flow b {{ font-size: 32px; line-height: 1.15; }} .flow span {{ font-size: 28px; opacity: .85; margin-top: 8px; line-height: 1.2; }}
.chk {{ display: flex; align-items: center; gap: 22px; font-size: 34px; font-weight: 700; }}
.box {{ width: 50px; height: 50px; border-radius: 10px; border: 4px solid #b7c0cf; display: flex; align-items: center; justify-content: center; flex: none; background: #fff; }}
.tick {{ color: #fff; font-weight: 900; font-size: 32px; }}
'''


class Scene:
    def __init__(s, sc):
        s.sc = sc; s.id = sc["id"]; s.dur = sc["dur"]; s.start = sc["start"]
        s.cue = {l["cue"]: l["t0"] for l in sc["lines"] if l["cue"]}; s.els, s.js, s.init = [], [], []
        s.lines = sc["lines"]

    def c(s, cue, d=0.0): return R(s.cue[cue] + d)

    def tw(s, sel, t, d, props, ease="power3.out"):
        s.js.append(f'tl.to("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())},duration:{R(d)},ease:"{ease}"}},{R(t)});')

    def st(s, sel, t, props): s.js.append(f'tl.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())}}},{R(t)});')

    def gs(s, sel, props): s.init.append(f'gsap.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())}}});')

    def add(s, eid, inner, style="", cls="a", t_in=None, t_out=None, enter="up", sfx=None):
        """element (absolute, in stage px). t_in None = visible from the scene start; t_out = fades out just before."""
        s.els.append(f'<div id="{eid}" class="{cls}" style="{style}">{inner}</div>')
        if t_in is not None:
            fr = {"up": {"opacity": 0, "y": 40}, "down": {"opacity": 0, "y": -40}, "left": {"opacity": 0, "x": -70}, "right": {"opacity": 0, "x": 70},
                  "pop": {"opacity": 0, "scale": 0.7}, "fade": {"opacity": 0}, "draw": {"scaleX": 0}}[enter]
            s.gs(f"#{eid}", fr)
            to = {k: (1 if k in ("opacity", "scale", "scaleX") else 0) for k in fr}
            s.tw(f"#{eid}", t_in, 0.5 if enter != "pop" else 0.45, to, "back.out(1.6)" if enter == "pop" else "power3.out")
            if sfx: CUES.append((R(s.start + t_in), sfx[0], sfx[1]))
        if t_out is not None: s.tw(f"#{eid}", t_out - 0.35, 0.35, {"opacity": 0}, "power2.in")

    def pulse(s, eid, t, scale=1.06):
        s.tw(f"#{eid}", t, 0.22, {"scale": scale}, "power2.out"); s.tw(f"#{eid}", t + 0.22, 0.35, {"scale": 1}, "power2.inOut")

    def hl(s, eid, x, y, w, h, t_in, t_out):
        s.add(eid, "", f"left:{R(x)}px;top:{R(y)}px;width:{R(w)}px;height:{R(h)}px", "hl", t_in, t_out, "pop", ("curated/ui-click.wav", -20))

    def write(s):
        doc = f'''<template>
  <style>{COMMON_CSS}</style>
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
'''
        open(f"edit/compositions/{s.id}.html", "w").write(doc)


def shot(S, eid, src, x, y, w, nat, t_in=None, t_out=None, enter="up"):
    h = w * nat[1] / nat[0]
    S.add(eid, f'<img src="assets/deck/{src}" alt="">', f"left:{x}px;top:{y}px;width:{w}px;height:{R(h)}px", "shot", t_in, t_out, enter)
    return w / nat[0]                                              # scale for highlight boxes


def qr(S, eid, kind, x, y, size, t_in=None, t_out=None, enter="pop"):
    src = "image-1-1.png" if kind == "g" else "image-1-2.png"
    S.add(eid, f'<img src="assets/deck/{src}" alt="">', f"left:{x}px;top:{y}px;width:{size}px;height:{size}px", "qr", t_in, t_out, enter)


def phone_form(S, eid, x, y, kind, t_in, t_out=None, title_ok_cue=None):
    """phone with the scanned QR, then the Google Form header (mock of the real form: purple bar, title)"""
    col = GREEN if kind == "g" else RED; word = "Check-in" if kind == "g" else "Check-out"
    S.add(eid, f'''<div class="screen" data-layout-ignore>
        <div class="a" id="{eid}_scan" style="inset:0;background:#0b0f1a">
          <img src="assets/deck/{"image-1-1.png" if kind == "g" else "image-1-2.png"}" style="position:absolute;left:52px;top:170px;width:260px;height:260px;border-radius:12px" alt="">
          <div class="a" style="left:40px;top:158px;width:284px;height:284px;border:5px solid #fff;border-radius:18px"></div>
          <div class="a" id="{eid}_line" style="left:46px;top:170px;width:272px;height:5px;background:{col};box-shadow:0 0 18px {col}"></div>
          <div class="a" style="left:0;right:0;top:480px;text-align:center;color:#fff;font-size:26px;font-weight:600">Scanning…</div></div>
        <div class="gf" id="{eid}_form">
          <div class="gfc" style="top:30px"><div class="gfbar"></div><div class="gft"><b id="{eid}_title" data-layout-allow-overlap>AA/SEC/F/077 Attendance Record – {word}</b></div></div>
          <div class="gfc" style="top:205px;padding:14px 18px;font-size:21px;color:#3c4043" id="{eid}_acct">● AirAsia Google account</div>
          <div class="gfc" style="top:285px;height:120px"></div><div class="gfc" style="top:420px;height:120px"></div><div class="gfc" style="top:555px;height:120px"></div>
        </div></div>''', f"left:{x}px;top:{y}px", "phone", t_in, t_out, "up")
    S.gs(f"#{eid}_form", {"opacity": 0}); S.gs(f"#{eid}_line", {"y": 0})
    S.tw(f"#{eid}_line", t_in + 0.3, 1.1, {"y": 268}, "power1.inOut"); S.tw(f"#{eid}_line", t_in + 1.4, 1.1, {"y": 0}, "power1.inOut")


def flow_row(S, pre, items, x0, y, w, gap, t_ins, t_out=None, colors=None):
    for i, (b, sub) in enumerate(items):
        x = x0 + i * (w + gap); col = (colors or [NAVY] * len(items))[i]
        S.add(f"{pre}{i}", f"<b>{esc(b)}</b>" + (f"<span>{esc(sub)}</span>" if sub else ""), f"left:{x}px;top:{y}px;width:{w}px;background:{col}", "flow", t_ins[i], t_out, "up",
              ("curated/ui-pop.wav", -19))
        if i < len(items) - 1:
            S.add(f"{pre}a{i}", "", f"left:{x + w + 12}px;top:{y + 72}px;width:{gap - 34}px", "arrow", t_ins[i + 1] - 0.1 if t_ins[i + 1] else None, t_out, "draw")


SC = {s["id"]: s for s in T["scenes"]}
scenes = []

# ---------------- S01 INTRODUCTION ----------------
S = Scene(SC["s01"]); scenes.append(S); B = S.c("span")
S.add("bg", "", f"left:0;top:0;width:1920px;height:1080px;background:{INK}", t_out=B, enter="fade")
S.add("k", "AA/SEC/F/077 ATTENDANCE RECORD", f"left:150px;top:250px;font-weight:800;font-size:30px;letter-spacing:3px;color:{AMBER}", t_in=None, t_out=B)
S.add("ttl", "How to Check In<br>and Check Out", "left:150px;top:310px;color:#fff", "a h1", None, B)
S.add("sub", "Staff training briefing<br><span style='opacity:.7'>Scan, fill in, submit, recorded</span>", "left:150px;top:500px;color:#fff;font-size:34px;line-height:1.4;font-weight:500", "a", 1.1, B, "left")
for i, (k, lab, sub) in enumerate((("g", "CHECK-IN", "Start of shift"), ("r", "CHECK-OUT", "End of shift"))):
    x = 1040 + i * 390
    S.add(f"qc{i}", f'<div style="text-align:center;margin-top:22px"><span class="pill {k}">{lab}</span></div>'
          f'<img src="assets/deck/image-1-{i + 1}.png" style="display:block;width:280px;height:280px;margin:22px auto 0" alt="">'
          f'<div style="text-align:center;font-size:32px;font-weight:700;margin-top:14px;color:{GREEN if k == "g" else RED}">{sub}</div>',
          f"left:{x}px;top:210px;width:350px;height:460px", "card", 1.3 + 0.25 * i, B, "pop", ("curated/ui-pop.wav", -16))
S.pulse("k", S.c("form") + 1.2)
# journey + what you need
S.add("jl", "", f"left:240px;top:330px;width:1440px;height:10px;background:linear-gradient(90deg,{GREEN},{RED});border-radius:6px", "a", B, S.c("agenda"), "draw")
S.add("j0", f'<span class="pill g">CHECK-IN</span><div class="t" style="margin-top:12px">Beginning of shift</div>', "left:150px;top:190px;width:300px", "a", B + 0.3, S.c("agenda"), "up")
S.add("j1", f'<span class="pill r">CHECK-OUT</span><div class="t" style="margin-top:12px">Completion of duty</div>', "left:1540px;top:190px;width:330px", "a", B + 0.6, S.c("agenda"), "up")
S.add("jd", "", f"left:232px;top:318px;width:34px;height:34px;border-radius:50%;background:#fff;border:6px solid {INK}", "a", B + 0.6, S.c("agenda"), "pop")
S.tw("#jd", B + 0.9, 3.0, {"x": 1420}, "power1.inOut")
S.add("jr", "Recorded accurately, every shift", f"left:0;width:1920px;top:380px;text-align:center;font-weight:800;font-size:38px", "a", B + 2.0, S.c("agenda"), "up")
ICON = {"phone": '<svg width="90" height="90" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="2.5" fill="none" stroke="#14213d" stroke-width="1.8"/><circle cx="12" cy="18.3" r="1" fill="#14213d"/></svg>',
        "acct": '<svg width="90" height="90" viewBox="0 0 24 24"><circle cx="12" cy="8.5" r="4" fill="none" stroke="#14213d" stroke-width="1.8"/><path d="M4 20c1.5-4 4.5-5.5 8-5.5s6.5 1.5 8 5.5" fill="none" stroke="#14213d" stroke-width="1.8"/></svg>',
        "qr": '<svg width="90" height="90" viewBox="0 0 24 24" fill="#14213d"><rect x="3" y="3" width="7" height="7" rx="1" fill="none" stroke="#14213d" stroke-width="1.8"/><rect x="14" y="3" width="7" height="7" rx="1" fill="none" stroke="#14213d" stroke-width="1.8"/><rect x="3" y="14" width="7" height="7" rx="1" fill="none" stroke="#14213d" stroke-width="1.8"/><rect x="14" y="14" width="3" height="3"/><rect x="18" y="18" width="3" height="3"/><rect x="18" y="14" width="3" height="2"/><rect x="14" y="19" width="2" height="2"/></svg>'}
need = S.c("need")
for i, (ic, lab) in enumerate((("phone", "Your mobile phone"), ("acct", "Official AirAsia Google account"), ("qr", "The correct QR code"))):
    S.add(f"nd{i}", f'<div style="margin-top:46px">{ICON[ic]}</div><div class="h3" style="margin-top:20px;padding:0 20px">{lab}</div>',
          f"left:{240 + i * 500}px;top:470px;width:440px;height:330px;text-align:center", "card", need + 1.2 * i + 0.6, S.c("agenda"), "up", ("curated/ui-pop.wav", -17))
ag = S.c("agenda")
for i, (lab, col) in enumerate((("Step by step", NAVY), ("Common mistakes to avoid", AMBER), ("If you submit incorrect information", RED))):
    S.add(f"ag{i}", f'<div class="num" style="background:{col}">{i + 1}</div><div class="h2">{lab}</div>', f"left:330px;top:{230 + i * 150}px", "a row", ag + 0.5 + 1.6 * i, None, "left", ("curated/ui-pop.wav", -17))
S.add("goal", "✓ Complete your attendance independently and correctly", f"left:330px;top:720px", "note green", S.c("goal") + 0.3, None, "up", ("clean-ding.wav", -16))

# ---------------- S02 TWO QR CODES ----------------
S = Scene(SC["s02"]); scenes.append(S); stp = S.c("steps")
S.add("h", "Two QR codes. Two moments.", "left:150px;top:130px", "a h1", S.c("two"), stp, "left")
for i, (k, cue, cue2, lab, when, mem) in enumerate((("g", "green", "green_t", "CHECK-IN", "START of shift", "mem_g"), ("r", "red", "red_t", "CHECK-OUT", "END of shift", "mem_r"))):
    x = 150 + i * 840
    S.add(f"c{i}", f'<div style="margin:28px 0 0 30px"><span class="pill {k}">{lab}</span></div>'
          f'<img src="assets/deck/image-1-{i + 1}.png" style="position:absolute;left:30px;top:110px;width:330px;height:330px" alt="">'
          f'<div class="h2" style="position:absolute;left:400px;top:150px;color:{GREEN if k == "g" else RED}">{when}</div>',
          f"left:{x}px;top:270px;width:780px;height:480px", "card", S.c(cue), stp, "pop", ("curated/ui-pop.wav", -15))
    S.add(f"cw{i}", f'Scan when you {"start" if k == "g" else "finish"}<br>your shift', f"left:{x + 400}px;top:520px;font-size:32px;font-weight:600;color:{MUTED};line-height:1.3", "a", S.c(cue2), stp, "up")
    S.pulse(f"c{i}", S.c(mem))
S.add("sw", "Never swap them", f"left:760px;top:770px;width:400px;text-align:center", "note red", S.c("swap") + 0.6, stp, "pop", ("curated/ui-click.wav", -16))
labels = [("1  Scan", NAVY), ("2  Fill in form", NAVY), ("3  Submit", NAVY), ("4  Recorded", GREEN)]
S.add("h2", "Four basic steps, for both procedures", "left:150px;top:180px", "a h1", stp + 0.2, None, "left")
for i, (lab, col) in enumerate(labels):
    x = 150 + i * 420
    S.add(f"st{i}", f'<b style="font-size:40px">{lab}</b>', f"left:{x}px;top:420px;width:360px;height:180px;background:{col}", "flow", S.c(f"st{i + 1}"), None, "up", ("curated/ui-pop.wav", -16))
    if i: S.add(f"sa{i}", "", f"left:{x - 52}px;top:507px;width:30px", "arrow", S.c(f"st{i + 1}") - 0.1, None, "draw")
S.add("stn", "Check-in at the start. Check-out at the end.", f"left:150px;top:680px;color:{RED};font-size:36px;font-weight:700", "a", S.c("st4") + 1.0, None, "up")

# ---------------- S02b WHERE TO SCAN (v02, from the creator's notice) ----------------
S = Scene(SC["s02b"]); scenes.append(S); bn = S.c("ban")
PIN = '<svg width="64" height="64" viewBox="0 0 24 24"><path d="M12 2c-3.9 0-7 3.1-7 7 0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7z" fill="#d6203a"/><circle cx="12" cy="9" r="2.6" fill="#fff"/></svg>'
CAM = '<svg width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#14213d" stroke-width="1.8"><rect x="3" y="7" width="13" height="8" rx="1.5"/><path d="M16 9l5-2v8l-5-2"/><path d="M7 15v4M4 19h6"/></svg>'
S.add("h", "Where to scan your attendance QR", "left:150px;top:120px", "a h1", 0.3, None, "left")
S.add("sub", "QR codes are provided at the respective offices", f"left:150px;top:205px;font-size:34px;font-weight:600;color:{MUTED}", "a", S.c("intro") + 0.6, None, "up")
for i, (cue, name, where, extra) in enumerate((("redq", "RedQ Office", "Displayed at the RedQ Office", "For staff reporting to RedQ"),
                                              ("gso", "Group Security Operation Office", "Displayed at the DSE workstation", f'{CAM}<span>Under CCTV surveillance</span>'))):
    x = 150 + i * 840
    S.add(f"loc{i}", f'<div class="row" style="gap:18px">{PIN}<div class="h2" style="max-width:560px">{name}</div></div>'
          f'<div class="h3" style="margin-top:26px">{where}</div>'
          f'<div class="row" style="margin-top:18px;gap:14px;font-size:30px;font-weight:600;color:{MUTED}">{extra}</div>'
          f'<div style="position:absolute;right:34px;top:34px;display:flex;gap:10px"><img src="assets/deck/image-1-1.png" style="width:92px;height:92px" alt=""><img src="assets/deck/image-1-2.png" style="width:92px;height:92px" alt=""></div>',
          f"left:{x}px;top:290px;width:780px;height:320px;padding:36px", "card", S.c(cue) + 0.3, None, "up", ("curated/ui-pop.wav", -15))
S.add("all", "✓ Scan the QR code at your own office premises", f"left:150px;top:650px;width:1620px;text-align:center", "note green", S.c("all") + 0.3, bn, "up", ("clean-ding.wav", -17))
S.add("ban", '<div style="font-size:30px;letter-spacing:3px;opacity:.9">⛔ STRICTLY PROHIBITED</div>Scanning or submitting your attendance QR outside your designated office premises',
      f"left:150px;top:620px;width:1620px;background:{RED};color:#fff;text-align:center", "note", bn + 0.2, None, "pop", ("curated/hook-impact.wav", -16))
S.add("disc", "Violations will be subject to disciplinary action", f"left:150px;top:775px;width:1620px;text-align:center;font-size:34px", "note red", S.c("disc") + 0.3, None, "up", ("curated/ui-click.wav", -14))

# ---------------- S03 / S07 SCAN + TITLE ----------------
def scan_scene(S, kind):
    g = kind == "g"; col = GREEN if g else RED; word = "Check-in" if g else "Check-out"; other = "Check-out" if g else "Check-in"
    S.add("h", f'<div class="num" style="background:{col}">{1 if g else 5}</div><div class="h1">{"Start" if g else "End"} of shift: scan the {word} QR</div>', "left:150px;top:120px", "a row", 0.3, None, "left")
    qr(S, "q", kind, 230, 300, 420, S.c("qr"), S.c("form"))
    phone_form(S, "ph", 240, 250, kind, S.c("form") - 2.6 if S.c("form") - S.c("qr") > 3 else S.c("form"))
    S.st("#ph_scan", S.c("form") + 0.4, {"opacity": 0}); S.tw("#ph_form", S.c("form") + 0.4, 0.4, {"opacity": 1}, "power2.out")
    items = [("a", f"Scan at the {'START' if g else 'END'} of your shift", "qr"), ("b", "Sign in with your official AirAsia Google account", "acct"), ("c", f"Title must say {word}", "title")]
    for i, (L, txt, cue) in enumerate(items):
        S.add(f"it{i}", f'<div class="num" style="background:{col}">{L}</div><div class="h3" style="max-width:900px">{txt}</div>', f"left:800px;top:{300 + i * 150}px", "a row", S.c(cue) + 0.2, None, "left", ("curated/ui-pop.wav", -17))
    if g:
        S.add("ng", '<span style="text-decoration:line-through">Personal Gmail</span>  ✗', f"left:888px;top:520px;font-size:30px;font-weight:700;color:{RED}", "a", S.c("nogmail") + 0.2, None, "up")
        S.pulse("ph_acct", S.c("acct") + 0.5)
    else:
        S.add("ng", f'<img src="assets/deck/image-1-1.png" style="width:110px;height:110px;vertical-align:middle;opacity:.55" alt=""> <span style="vertical-align:middle;font-size:32px;font-weight:700;color:{RED};margin-left:14px">Not the green Check-in QR again ✗</span>',
              "left:800px;top:760px", "a", S.c("not_green") + 0.2, S.c("shorter"), "up")
    S.add("tbox", "", f"left:262px;top:284px;width:356px;height:148px;border:6px solid {col};border-radius:14px", "a", S.c("title_ok"), None, "pop", ("clean-ding.wav", -17))
    S.add("tok", f"✓ {word}", f"left:430px;top:445px;background:{col};color:#fff;font-weight:800;font-size:28px;padding:8px 18px;border-radius:30px", "a", S.c("title_ok") + 0.2, S.c("wrong") if g else None, "pop")
    if g:
        w0, b0, v0 = S.c("wrong"), S.c("back"), S.c("verify")
        S.st("#ph_title", w0, {"color": RED}); S.add("tbad", f'<span id="tbadx" data-layout-allow-overlap>AA/SEC/F/077 Attendance Record – {other}</span>',
             f"left:275px;top:316px;width:330px;font-size:25px;line-height:1.25;font-weight:700;color:{RED};background:#fff;padding:0 4px", "a", w0, b0, "fade")
        S.st("#tbox", w0, {"borderColor": RED})
        S.add("wq", f"Wrong QR = wrong form", f"left:800px;top:780px", "note red", w0 + 0.3, None, "up", ("curated/ui-click.wav", -15))
        S.add("bk", f"Go back and scan the correct green QR", f"left:1260px;top:780px;width:520px", "note green", b0 + 0.3, None, "up")
        S.st("#tbox", b0 + 0.3, {"borderColor": GREEN}); S.st("#ph_title", b0 + 0.3, {"color": "#202124"})
        S.pulse("it2", v0 + 0.2)
    else:
        S.add("cmp", f'''<div class="row" style="align-items:flex-end;gap:60px">
            <div style="text-align:center"><div style="width:150px;height:230px;border-radius:18px;background:#e5f5ec;border:4px solid {GREEN}"></div><div class="h3 ok" style="margin-top:12px">Check-in form</div></div>
            <div style="text-align:center"><div style="width:150px;height:140px;border-radius:18px;background:#fde8eb;border:4px solid {RED}"></div><div class="h3 bad" style="margin-top:12px">Check-out form</div></div>
            <div class="h2" style="max-width:420px;margin-bottom:60px">Shorter, with fewer details</div></div>''', "left:800px;top:560px", "a", S.c("shorter") + 0.3, None, "up", ("curated/ui-pop.wav", -16))


S = Scene(SC["s03"]); scenes.append(S); scan_scene(S, "g")
S = Scene(SC["s07"]); scan_out = S; scan_scene(S, "r")

# ---------------- S04 CHECK-IN FORM ----------------
S = Scene(SC["s04"]); scenes.append(S)
S.add("h", f'<div class="num" style="background:{GREEN}">2</div><div class="h1">Fill in the Check-in form</div>', "left:150px;top:120px", "a row", 0.3, None, "left")
fd = S.c("f_date")
k1 = shot(S, "sh1", "v02_designation.png", 150, 270, 700, (780, 641), S.c("f_email"), fd)       # v02: creator's new screenshot (email hidden)
S.hl("hle", 150 + 28 * k1, 270 + 86 * k1, 640 * k1, 40 * k1, S.c("email_tick"), S.c("f_desig"))
S.add("tick", "✓", f"left:{R(150 + 36 * k1)}px;top:{R(270 + 94 * k1)}px;width:{R(25 * k1)}px;height:{R(25 * k1)}px;background:{GREEN};color:#fff;font-weight:900;font-size:22px;text-align:center;line-height:{R(25 * k1)}px;border-radius:5px", "a",
      S.c("email_tick") + 0.6, fd, "pop", ("curated/ui-click.wav", -14))
DESIG = (("d1", 345), ("d2", 403), ("d3", 460), ("d4", 518), ("d5", 575))       # ASO, SO, SSO, SE, SM rows
for i, (cue, y) in enumerate(DESIG):
    S.hl(f"hld{i}", 150 + 30 * k1, 270 + y * k1, 335 * k1, 40 * k1, S.c(cue), S.c("aso_pick") if i else fd)
S.st("#hld0", S.c("aso_pick") + 0.3, {"borderColor": GREEN})
for i, (ab, (cue, y)) in enumerate(zip(("ASO", "SO", "SSO", "SE", "SM"), DESIG)):      # big labels beside each dropdown row
    S.add(f"dg{i}", ab, f"left:{R(150 + 395 * k1)}px;top:{R(270 + (y - 2) * k1)}px;width:130px;height:46px;line-height:46px;text-align:center;border-radius:23px;background:{NAVY};color:#fff;font-weight:800;font-size:30px",
          "a", S.c(cue) + 0.1, fd, "left", ("curated/ui-pop.wav", -18))
S.st("#dg0", S.c("aso_pick") + 0.3, {"background": GREEN}); S.pulse("dg0", S.c("aso_pick") + 0.3)
# date / name / staff id mock fields (after designation)
k2 = shot(S, "sh2", "v02_date.png", 150, 290, 600, (646, 165), fd, S.c("f_name"))
S.hl("hlt", 150 + 22 * k2, 290 + 28 * k2, 300 * k2, 100 * k2, fd + 0.5, S.c("f_name"))
S.add("dm", "Matches your Check-in and Check-out records", f"left:150px;top:{R(290 + 165 * k2 + 40)}px;width:600px", "note navy", S.c("date_match") + 0.6, S.c("f_name"), "up")
for i, (lab, cue, t_out) in enumerate((("Name", "f_name", None), ("Staff ID", "f_id", None))):
    S.add(f"in{i}", f'<div style="font-size:30px;color:#202124">{lab} <span style="color:{RED}">*</span></div><div style="margin-top:26px;border-bottom:2px solid #c5c9d1;width:460px;font-size:26px;color:#9aa0a6;padding-bottom:8px">Your answer</div>',
          f"left:150px;top:{300 + i * 230}px;width:700px;height:190px;padding:30px 36px", "card", S.c(cue), None, "up")
S.add("idm", "Identifies you and matches your attendance", f"left:150px;top:770px;width:700px", "note navy", S.c("id_match") + 0.6, None, "up")
# right: what the form asks
S.add("wl", "What the form asks", "left:1100px;top:270px", "a h2", 0.8, None, "up")
for i, (lab, sub, cue) in enumerate((("Email", "tick the Record email box", "f_email"), ("Designation", "ASO, SO, SSO, SE or SM", "f_desig"), ("Shift start date", "the date your shift starts", "f_date"),
                                     ("Name", "your name, accurately", "f_name"), ("Staff ID", "check it carefully", "f_id"))):
    S.add(f"fl{i}", f'<div class="num" style="background:{GREEN};width:54px;height:54px;font-size:28px">{i + 1}</div><div><div class="h3">{lab}</div><div class="t" style="font-size:28px">{sub}</div></div>',
          f"left:1100px;top:{360 + i * 100}px", "a row", S.c(cue), None, "left", ("curated/ui-pop.wav", -18))
S.add("tm", '<span style="font-weight:700">Team</span>: next', f"left:1176px;top:870px;font-size:28px;color:{MUTED}", "a", S.c("f_id") + 1.0, None, "fade")

# ---------------- S05 TEAMS ----------------
S = Scene(SC["s05"]); scenes.append(S); fa = S.c("fix_after")
S.add("h", f'<div class="num" style="background:{GREEN}">3</div><div class="h1">Select your team</div>', "left:150px;top:120px", "a row", 0.3, fa, "left")
k = shot(S, "sh", "v02_team_list.png", 150, 270, 470, (400, 348), 0.5, fa)                # v02: creator's new screenshot (with REDQ)
S.hl("hlteam", 150 + 18 * k, 270 + 78 * k, 250 * k, 240 * k, S.c("teams"), S.c("why"))
TEAMS = ["ALPHA", "BRAVO", "CHARLIE", "DELTA", "REDQ"]
for i, tm in enumerate(TEAMS):
    x, y = 820 + (i % 3) * 320, 280 + (i // 3) * 150
    S.add(f"tm{i}", f'<b style="font-size:42px;letter-spacing:2px">{tm}</b>', f"left:{x}px;top:{y}px;width:300px;height:125px;background:{NAVY}", "flow", S.c(["t_a", "t_b", "t_c", "t_d", "t_e"][i]), fa, "pop",
          ("curated/ui-pop.wav", -16))
S.add("why", "Why does it matter?", f"left:1460px;top:440px;width:300px", "note navy", S.c("why"), S.c("ex_pick"), "pop")
# sheet tabs
S.add("tabs", "".join(f'<div id="tab{i}" style="padding:14px 24px;border-radius:14px 14px 0 0;background:#e9edf3;font-weight:700;font-size:30px;color:{MUTED}">{t if t == "REDQ" else t.title()}</div>' for i, t in enumerate(TEAMS)),
      "left:820px;top:690px;display:flex;gap:10px;border-bottom:5px solid #c9d1de", "a", S.c("tabs") + 0.5, fa, "up")
S.add("tabl", "Your team = your tab in the central Google Sheet", f"left:820px;top:790px;font-size:30px;font-weight:700;color:{INK}", "a", S.c("tabs") + 1.4, fa, "up")
S.add("you", f'You belong to <b style="color:{GREEN}">BRAVO</b>', f"left:150px;top:{R(270 + 348 * k + 30)}px;font-size:34px", "a", S.c("ex_pick") + 0.3, fa, "up")
S.st("#tm0", S.c("ex_pick") + 2.5, {"background": RED}); S.pulse("tm0", S.c("ex_pick") + 2.5)
S.add("rec", "Your record", f"left:1000px;top:560px;background:#fff;border:3px solid {RED};padding:10px 22px;border-radius:12px;font-weight:700;font-size:30px;color:{RED}", "a", S.c("ex_land"), S.c("fix_before"), "pop")
S.tw("#rec", S.c("ex_land") + 0.7, 1.0, {"x": -175, "y": 95, "scale": 0.8}, "power2.inOut")
S.st("#tab0", S.c("ex_land") + 1.7, {"background": "#fde8eb", "color": RED})
S.add("wr", "✗ Incorrect attendance record", f"left:820px;top:860px", "note red", S.c("ex_wrong") + 0.2, S.c("fix_before") + 0.2, "up", ("curated/ui-click.wav", -15))
S.add("fb", "Before Submit? Just correct your selection.", f"left:820px;top:860px", "note green", S.c("fix_before") + 0.4, fa, "up")
# escalation flow
S.add("h2", "Already submitted with the wrong team?", "left:150px;top:150px", "a h1", fa + 0.2, None, "left")
flow_row(S, "fw", [("Staff", "you"), ("Respective DSE", "inform immediately"), ("Operations Security Manager", "DSE reports the error"), ("Attendance correction", "")],
         150, 380, 360, 80, [fa + 1.2, fa + 3.0, S.c("osm") + 1.5, S.c("osm") + 3.6], colors=[NAVY, NAVY, NAVY, GREEN])
S.add("nr", "Do not submit another response unless an authorised supervisor tells you to", f"left:150px;top:640px;width:1620px", "note red", S.c("no_resubmit") + 0.3, None, "up", ("curated/ui-click.wav", -15))
for i in range(4): S.pulse(f"fw{i}", S.c("flow_all") + 0.9 * i, 1.05)
S.add("dc", "Always double-check your team before pressing Submit", f"left:150px;top:780px;width:1620px", "note green", S.c("double") + 0.3, None, "up", ("clean-ding.wav", -17))

# ---------------- S06 REVIEW + SUBMIT ----------------
S = Scene(SC["s06"]); scenes.append(S); nc = S.c("noconf")
S.add("h", f'<div class="num" style="background:{GREEN}">4</div><div class="h1">Review, submit and confirm</div>', "left:150px;top:120px", "a row", 0.3, nc, "left")
S.add("hold", "Don't press Submit yet: review first", f"left:150px;top:260px", "note navy", S.c("hold") + 0.3, S.c("check"), "up")
for i, (lab, cue) in enumerate((("Company email selected", "c1"), ("Designation", "c2"), ("Shift start date", "c3"), ("Assigned team", "c4"), ("Name", "c5"), ("Staff ID", "c6"))):
    S.add(f"ck{i}", f'<div class="box" id="ckb{i}"><span class="tick">✓</span></div><span>{lab}</span>', f"left:150px;top:{260 + i * 92}px", "a chk", S.c("check") + 0.15 * i, nc, "left")
    S.st(f"#ckb{i}", S.c(cue) + 0.15, {"background": GREEN, "borderColor": GREEN}); CUES.append((R(S.start + S.c(cue) + 0.15), "curated/ui-click.wav", -17))
S.add("btn", "Submit", f"left:900px;top:300px;width:300px;height:90px;border-radius:12px;background:#673ab7;color:#fff;font-size:38px;font-weight:700;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(103,58,183,.35)",
      "a", S.c("submit"), nc, "pop")
S.tw("#btn", S.c("submit") + 1.2, 0.12, {"scale": 0.9}, "power2.in"); S.tw("#btn", S.c("submit") + 1.32, 0.2, {"scale": 1}, "power2.out"); CUES.append((R(S.start + S.c("submit") + 1.25), "curated/ui-click.wav", -12))
S.add("once", "Once per shift", f"left:1240px;top:315px", "a pill n", S.c("once") + 0.2, nc, "pop")
S.add("ysts", "YOU SHOULD SEE THIS", "left:900px;top:440px", "a pill g", S.c("recorded") - 0.3, nc, "up")
k = shot(S, "conf", "image-6-1.png", 900, 520, 860, (646, 232), S.c("recorded"), nc, "pop")
S.hl("hlc", 900 + 18 * k, 520 + 140 * k, 230 * k, 30 * k, S.c("recorded") + 0.6, nc)
S.add("wt", "Wait for the confirmation…", f"left:900px;top:560px;font-size:34px;font-weight:600;color:{MUTED}", "a", S.c("wait") + 0.3, S.c("recorded"), "fade")
S.add("cpl", "✓ Check-in complete", f"left:900px;top:{R(520 + 232 * k + 30)}px", "note green", S.c("complete") + 0.2, nc, "up", ("clean-ding.wav", -15))
S.add("h2", "No confirmation screen?", "left:150px;top:150px", "a h1", nc + 0.1, None, "left")
for i, lab in enumerate(("Missing fields", "Form errors", "Internet connection")):
    S.add(f"nc{i}", f'<div class="num" style="background:{AMBER}">?</div><div class="h2">{lab}</div>', f"left:150px;top:{300 + i * 115}px", "a row", nc + 1.6 + 0.9 * i, None, "left", ("curated/ui-pop.wav", -17))
S.add("un", "Unsure it was sent? Inform your supervisor. Don't keep submitting.", f"left:150px;top:670px;width:1620px", "note navy", S.c("unsure") + 0.3, None, "up")
S.add("dp", "Multiple submissions can create duplicate attendance records", f"left:150px;top:800px;width:1620px", "note red", S.c("dupes") + 0.3, None, "up", ("curated/ui-click.wav", -15))
for i in range(3): S.add(f"dup{i}", "", f"left:{1250 + i * 26}px;top:{300 + i * 26}px;width:380px;height:240px;border-radius:16px;background:#fff;border:3px solid {RED};box-shadow:0 10px 24px rgba(20,33,61,.15)",
                         "a", S.c("dupes") + 0.6 + 0.15 * i, None, "pop")

# ---------------- S07 (built above, order) ----------------
scenes.append(scan_out)

# ---------------- S08 CHECK-OUT FORM ----------------
S = Scene(SC["s08"]); scenes.append(S); at, tm = S.c("attn"), S.c("team")
S.add("h", f'<div class="num" style="background:{RED}">6</div><div class="h1">Complete the Check-out form</div>', "left:150px;top:120px", "a row", 0.3, at, "left")
k = shot(S, "sh", "v02_checkout_form.png", 150, 250, 540, (525, 587), 0.6, at)      # v02: team card with REDQ
for nm, (y0, y1), cue in (("e", (20, 78), "email"), ("i", (125, 198), "id"), ("d", (250, 328), "date")):
    S.hl(f"hl{nm}", 150 + 15 * k, 250 + y0 * k, 470 * k, (y1 - y0) * k, S.c(cue), at)
for i, (lab, sub, cue) in enumerate((("Email", "tick the Record email box", "email"), ("Staff ID", "the SAME Staff ID as Check-in", "id"), ("Shift start date", "the date your shift STARTED", "date"))):
    S.add(f"fl{i}", f'<div class="num" style="background:{RED};width:54px;height:54px;font-size:28px">{i + 1}</div><div><div class="h3">{lab}</div><div class="t" style="font-size:28px">{sub}</div></div>',
          f"left:830px;top:{300 + i * 130}px", "a row", S.c(cue), at, "left", ("curated/ui-pop.wav", -18))
S.pulse("fl1", S.c("id_same") + 0.4)
# overnight example
S.add("h2", "Overnight shifts: which date?", "left:150px;top:140px", "a h1", at + 0.2, tm, "left")
S.add("night", "", f"left:150px;top:420px;width:1620px;height:120px;border-radius:20px;background:linear-gradient(90deg,#f7c873,#1b2a4a 30%,#0f1830 70%,#f7c873)", "a", S.c("night"), tm, "draw")
for i, (d, tt, x) in enumerate((("11 Nov", "8:00 PM · shift starts", 150), ("12 Nov", "8:00 AM · shift ends", 1370))):
    S.add(f"nd{i}", f'<div class="h2">{d}</div><div class="t">{tt}</div>', f"left:{x}px;top:290px;width:420px", "a", S.c("night") + 0.6 + 2.0 * i, tm, "up")
S.add("q", "Checking out on 12 Nov. Which date do you select?", f"left:150px;top:600px", "a h2", S.c("q"), tm, "up")
S.add("ans", "✓ 11 November: the shift START date", f"left:150px;top:700px", "note green", S.c("ans") + 0.3, tm, "pop", ("clean-ding.wav", -14))
S.add("n12", "✗ Not 12 November", f"left:1000px;top:700px", "note red", S.c("not12") + 0.3, tm, "pop", ("curated/ui-click.wav", -15))
# team + no name/designation + submit
S.add("h3", "Same team as your Check-in", "left:150px;top:140px", "a h1", tm + 0.2, None, "left")
S.add("bin", f'<span class="pill g">CHECK-IN</span><div class="h2" style="margin-top:20px">BRAVO</div>', "left:150px;top:290px;width:400px;height:220px;padding:34px", "card", S.c("bravo") + 0.2, None, "up")
S.add("bout", f'<span class="pill r">CHECK-OUT</span><div class="h2" style="margin-top:20px">BRAVO</div>', "left:650px;top:290px;width:400px;height:220px;padding:34px", "card", S.c("bravo") + 2.2, None, "up")
S.add("beq", "=", "left:575px;top:340px;font-size:80px;font-weight:800;color:#2b3a5c", "a", S.c("bravo") + 2.4, None, "pop", ("clean-ding.wav", -17))
S.add("dse", "Check-in had the wrong team? Inform your respective DSE", f"left:150px;top:560px;width:900px", "note navy", S.c("dse") + 0.4, S.c("noname"), "up")
S.add("nn", f'<span style="text-decoration:line-through">Name</span> · <span style="text-decoration:line-through">Designation</span><div class="t" style="margin-top:8px">Not on this form: already given at Check-in</div>',
      f"left:150px;top:560px;width:900px;font-size:40px;font-weight:800;color:{MUTED}", "a", S.c("noname") + 0.3, None, "up")
S.add("ysts", "THEN SUBMIT ONCE: YOU SHOULD SEE THIS", "left:1150px;top:300px", "a pill r", S.c("submit") + 0.2, None, "up")
k = shot(S, "conf", "image-8-2.png", 1150, 380, 640, (646, 232), S.c("recorded"), None, "pop")
S.add("cpl", "✓ Check-out complete", f"left:1150px;top:{R(380 + 232 * k + 30)}px", "note green", S.c("complete") + 0.2, None, "up", ("clean-ding.wav", -15))

# ---------------- S09 TIME AUTOMATIC ----------------
S = Scene(SC["s09"]); scenes.append(S); sh = S.c("sheet")
S.add("h", f'<div class="num" style="background:{NAVY}">7</div><div class="h1">Times are recorded automatically</div>', "left:150px;top:120px", "a row", 0.3, None, "left")
S.add("nm", "No manual time entry", f"left:150px;top:260px", "note red", S.c("nomanual") + 0.3, sh, "pop", ("curated/ui-click.wav", -16))
for i, (lab, sub, cue, tval) in enumerate((("CHECK-IN TIME", "Saved when you press Submit on the Check-in form", "ex_in", "8:05 AM"), ("CHECK-OUT TIME", "Saved when you press Submit on the Check-out form", "ex_out", "8:10 PM"))):
    S.add(f"tc{i}", f'<span class="pill {"g" if i == 0 else "r"}">{lab}</span><div class="h3" style="margin-top:24px;max-width:600px">{sub}</div>'
          f'<div id="tv{i}" style="margin-top:28px;font-size:72px;font-weight:800;color:{GREEN if i == 0 else RED}">{tval}</div>',
          f"left:{150 + i * 830}px;top:400px;width:780px;height:400px;padding:40px", "card", S.c("auto") + 0.4 + 0.3 * i, sh, "up")
    S.gs(f"#tv{i}", {"opacity": 0, "scale": 1.6}); S.tw(f"#tv{i}", S.c(cue) + 2.0, 0.35, {"opacity": 1, "scale": 1}, "back.out(2)")
    CUES.append((R(S.start + S.c(cue) + 2.0), "thock.wav", -12))
S.add("ex", "Shift starts 8:00 AM", f"left:700px;top:260px", "note navy", S.c("ex_start") + 0.3, S.c("ex_out"), "up")
S.add("nf", '<span style="text-decoration:line-through">Time field</span>: the forms do not have one', f"left:1100px;top:260px;width:680px", "note red", S.c("nofield") + 0.3, sh, "up")
k = shot(S, "sheet", "image-10-1.png", 150, 420, 1620, (1410, 153), sh + 0.2, None, "up")
S.hl("hli", 150 + 48 * k, 420 + 25 * k, 170 * k, 80 * k, sh + 1.0, None); S.hl("hlo", 150 + 1198 * k, 420 + 25 * k, 145 * k, 80 * k, sh + 1.6, None)
S.add("shl", "Timestamps land in the attendance Google Sheet", f"left:150px;top:300px", "a h2", sh + 0.4, None, "up")
S.add("rule", "Remember: no manual time entry is required.", f"left:150px;top:680px;width:1620px;text-align:center;font-size:44px", "note navy", S.c("rule") + 0.2, None, "pop", ("clean-ding.wav", -14))

# ---------------- S10 WHERE IT GOES ----------------
S = Scene(SC["s10"]); scenes.append(S)
S.add("h", "Where your attendance goes", "left:150px;top:120px", "a h1", 0.3, None, "left")
flow_row(S, "fw", [("Staff scans QR", "Check-in or Check-out"), ("Submits the form", "Check-in or Check-out form"), ("Google Sheet records the time", "automatically"), ("Appears under your team", "Alpha, Bravo, Charlie, Delta or REDQ")],
         150, 250, 360, 60, [S.c("p1"), S.c("p1") + 1.6, S.c("p1") + 3.6, S.c("p2") + 0.5], colors=[NAVY, NAVY, NAVY, GREEN])
tm_ = S.c("times")
k = shot(S, "sheet", "v02_sheet_strip.png", 150, 470, 1620, (1874, 271), S.c("p2") + 1.2, tm_ + 2.4, "up")    # v02: creator's new Sheet (staff details hidden)
for i, (cue, x0, x1) in enumerate((("alpha", 536, 634), ("bravo", 636, 735), ("cd", 737, 846), ("cd", 848, 942), ("cd", 944, 1042))):
    S.hl(f"hlt{i}", 150 + x0 * k, 470 + 230 * k, (x1 - x0) * k, 42 * k, S.c(cue) + (0.4 if i < 2 else 1.0 + 0.6 * (i - 2)), tm_ + 2.4)
k = shot(S, "sheet2", "image-10-1.png", 150, 470, 1620, (1410, 153), tm_ + 2.2, None, "fade")
S.hl("hli", 150 + 48 * k, 470 + 25 * k, 170 * k, 80 * k, tm_ + 2.9, S.c("resp")); S.hl("hlo", 150 + 1198 * k, 470 + 25 * k, 145 * k, 80 * k, tm_ + 3.6, S.c("resp"))
S.add("sm", "Sample view, staff details hidden", f"left:150px;top:{R(470 + 271 * 1620 / 1874 + 12)}px;font-size:28px;color:{MUTED}", "a", S.c("p2") + 1.5, None, "fade")
S.add("sup", "Reviewed by authorised supervisors", f"left:150px;top:720px", "note navy", S.c("sup") + 0.3, None, "up")
S.add("ns", "Staff: no need to open or update the Sheet", f"left:900px;top:720px", "note green", S.c("nostaff") + 0.3, S.c("resp"), "up")
for i, lab in enumerate(("Use the correct QR codes", "Complete the forms accurately", "Verify each submission")):
    S.add(f"rs{i}", f"✓ {lab}", f"left:{150 + i * 560}px;top:820px;width:520px;font-size:30px", "note green", S.c("resp") + 0.6 + 1.3 * i, None, "up", ("curated/ui-pop.wav", -17))

# ---------------- S11 MISTAKES ----------------
S = Scene(SC["s11"]); scenes.append(S)
S.add("h", "Common mistakes to avoid", "left:150px;top:110px", "a h1", 0.3, None, "left")
MIS = [("Scanned the wrong QR", "Green for Check-in, red for Check-out"), ("Selected the wrong team", "Verify your assigned team before Submit"), ("Wrong shift start date", "Same start date at Check-in and Check-out"),
       ("Used a personal Gmail account", "Use your official AirAsia Google account"), ("Submitted multiple responses", "One Check-in and one Check-out per shift"), ("Forgot to check out", "Submit your Check-out before leaving duty")]
for i, (bad, good) in enumerate(MIS):
    y = 220 + i * 98
    S.add(f"mb{i}", f'<div class="x">✗</div><div style="font-size:31px;font-weight:700;color:{RED}">{bad}</div>', f"left:150px;top:{y}px;width:760px;height:84px;background:#fff;border-radius:16px;padding:0 20px", "a row",
          S.c(f"m{i + 1}"), None, "left", ("curated/ui-click.wav", -17))
    S.add(f"mg{i}", f'<div class="v">✓</div><div style="font-size:29px;font-weight:600">{good}</div>', f"left:960px;top:{y}px;width:810px;height:84px;background:#fff;border-radius:16px;padding:0 20px", "a row",
          S.c(f"m{i + 1}_ok"), None, "right", ("curated/ui-pop.wav", -18))
S.add("rp", "Any issue or incorrect submission? Inform your respective DSE", f"left:150px;top:810px;width:1620px;text-align:center", "note navy", S.c("report") + 0.3, None, "up")

# ---------------- S12 RECAP ----------------
S = Scene(SC["s12"]); scenes.append(S); rl = S.c("rules"); en = S.c("end")
S.add("h", "Quick recap", "left:150px;top:110px", "a h1", 0.3, rl, "left")
for c, (k_, lab, steps) in enumerate((("g", "CHECK-IN: START of shift", ["Scan the green Check-in QR", "Sign in: official AirAsia Google account", "Designation, date, team, name, Staff ID", "Review, Submit once, see “recorded”"]),
                                      ("r", "CHECK-OUT: END of shift", ["Scan the red Check-out QR", "Same official AirAsia Google account", "Same Staff ID and start date, correct team", "Submit once, wait for confirmation"]))):
    x = 150 + c * 830; pre = "in" if c == 0 else "out"
    S.add(f"col{c}", f'<span class="pill {k_}" style="font-size:30px">{lab}</span>', f"left:{x}px;top:230px", "a", S.c(pre), rl, "up")
    for i, st_ in enumerate(steps):
        S.add(f"rc{c}{i}", f'<div class="num" style="background:{GREEN if c == 0 else RED};width:52px;height:52px;font-size:28px">{i + 1}</div><div style="font-size:31px;font-weight:600;max-width:680px">{st_}</div>',
              f"left:{x}px;top:{330 + i * 120}px", "a row", S.c(f"{pre}{i + 1}"), rl, "left", ("curated/ui-pop.wav", -18))
S.add("h2", "Three rules", "left:150px;top:110px", "a h1", rl + 0.2, en, "left")
for i, (lab, cue) in enumerate((("Always use your official AirAsia Google account", "r1"), ("Never enter or change the attendance time: it is recorded automatically", "r2"),
                                ("Submit each form once per shift and verify the confirmation", "r3"))):
    S.add(f"rr{i}", f'<div class="num" style="background:{NAVY}">{i + 1}</div><div class="h3" style="max-width:1400px">{lab}</div>', f"left:150px;top:{240 + i * 120}px", "a row", S.c(cue), en, "left", ("curated/ui-pop.wav", -16))
flow_row(S, "fw", [("Staff", "incorrect info submitted"), ("Respective DSE", "report immediately"), ("Operations Security Manager", "necessary correction")], 150, 630, 480, 90,
         [S.c("rem") + 0.3, S.c("rem") + 2.5, S.c("rem2") + 1.5], en)
S.add("pp", "Accurate  ·  Properly organised  ·  Available for supervisory review", f"left:150px;top:830px;width:1620px;text-align:center", "note green", S.c("purpose") + 0.3, en, "up")
S.add("endbg", "", f"left:0;top:0;width:1920px;height:1080px;background:{INK}", "a", en, None, "fade")
S.add("ty", "Thank you", "left:0;width:1920px;top:330px;text-align:center;color:#fff;font-size:110px;font-weight:800", "a", S.c("thanks"), None, "up", ("sparkle.wav", -16))
S.add("ty2", "AA/SEC/F/077 Attendance Record briefing", f"left:0;width:1920px;top:480px;text-align:center;color:{AMBER};font-size:36px;font-weight:700;letter-spacing:2px", "a", en + 0.3, None, "up")
S.add("qs", "Any questions about Check-in or Check-out?", "left:0;width:1920px;top:600px;text-align:center;color:#fff;font-size:44px;font-weight:600", "a", S.c("qs") + 0.3, None, "up")

# ---------------- S13 Q&A ----------------
S = Scene(SC["s13"]); scenes.append(S); L = {l["cue"]: l for l in S.lines}
S.add("h", "Staff understanding check", "left:150px;top:110px", "a h1", 0.3, L["end"]["t0"], "left")
for i in range(10):
    q, a = L[f"q{i + 1}"], L[f"a{i + 1}"]; t_out = L[f"q{i + 2}"]["t0"] if i < 9 else L["end"]["t0"]
    S.add(f"qn{i}", f"QUESTION {i + 1} / 10", f"left:150px;top:250px;font-weight:800;font-size:30px;letter-spacing:3px;color:#a35a00", "a", q["t0"], t_out, "up")
    S.add(f"qq{i}", esc(q["text"]), "left:150px;top:310px;width:1620px", "a h2", q["t0"] + 0.1, t_out, "up", ("curated/ui-pop.wav", -15))
    # think ring
    S.add(f"rg{i}", f'<svg width="140" height="140" viewBox="0 0 140 140"><circle cx="70" cy="70" r="58" fill="none" stroke="#dfe4ec" stroke-width="12"/>'
          f'<circle id="rc{i}" cx="70" cy="70" r="58" fill="none" stroke="{AMBER}" stroke-width="12" stroke-linecap="round" transform="rotate(-90 70 70)" stroke-dasharray="364.4" stroke-dashoffset="0"/></svg>'
          f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:30px;color:{MUTED}">Think</div>',
          "left:1630px;top:560px;width:140px;height:140px", "a", q["t1"], a["t0"] + 0.2, "pop")
    S.tw(f"#rc{i}", q["t1"], a["t0"] - q["t1"], {"strokeDashoffset": 364.4}, "none")
    S.add(f"aa{i}", "✓ " + esc(a["text"]), "left:150px;top:560px;width:1420px;font-size:38px", "note green", a["t0"], t_out, "pop", ("clean-ding.wav", -15))
S.add("endbg", "", f"left:0;top:0;width:1920px;height:1080px;background:{INK}", "a", L["end"]["t0"], None, "fade")
S.add("e1", "END OF TRAINING", f"left:0;width:1920px;top:380px;text-align:center;color:{AMBER};font-size:40px;font-weight:800;letter-spacing:6px", "a", L["end"]["t0"] + 0.3, None, "up")
S.add("e2", "AA/SEC/F/077 – Attendance Record<br>Staff Guidance", "left:0;width:1920px;top:450px;text-align:center;color:#fff;font-size:70px;font-weight:800;line-height:1.15", "a", L["end"]["t0"] + 0.6, None, "up")

for S in scenes: S.write()
CUES.extend((R(sc["start"]), "curated/zoom-swish.wav", -18) for sc in T["scenes"][1:])

# ---------------- chrome: form code, chapter, progress ----------------
ch_els, ch_js, ch_init = [], [], []
ch_els.append(f'<div id="ctag" class="a" style="left:150px;top:40px;font-size:28px;font-weight:700;letter-spacing:1.5px;color:{MUTED}">AA/SEC/F/077 ATTENDANCE RECORD · STAFF TRAINING</div>')
ch_els.append(f'<div id="pbar" class="a" style="left:0;top:1072px;width:1920px;height:8px;background:{GREEN};transform-origin:0 50%"></div>')
ch_init.append('gsap.set("#pbar",{scaleX:0});'); ch_js.append(f'tl.to("#pbar",{{scaleX:1,duration:{R(TOTAL)},ease:"none"}},0);')
for i, sc in enumerate(T["scenes"]):
    lab = f"{i + 1:02d} / {len(T['scenes'])} · {sc['title']}" if sc["id"] != "s13" else f"Q&A · {sc['title']}"
    ch_els.append(f'<div id="chap{i}" class="a" style="right:150px;top:40px;font-size:28px;font-weight:700;color:{INK};text-align:right">{esc(lab)}</div>')
    ch_init.append(f'gsap.set("#chap{i}",{{opacity:0}});')
    ch_js.append(f'tl.to("#chap{i}",{{opacity:1,duration:0.4}},{R(sc["start"] + 0.2)});')
    ch_js.append(f'tl.to("#chap{i}",{{opacity:0,duration:0.3}},{R(sc["start"] + sc["dur"] - 0.3)});')
# hide the chrome text on the dark title / end cards
s01 = SC["s01"]; ch_init.append('gsap.set("#ctag",{opacity:0});')
ch_js.append(f'tl.to("#ctag",{{opacity:1,duration:0.4}},{R(next(l["t0"] for l in s01["lines"] if l["cue"] == "span"))});')
s12 = SC["s12"]; ch_js.append(f'tl.to("#ctag",{{opacity:0,duration:0.3}},{R(s12["start"] + next(l["t0"] for l in s12["lines"] if l["cue"] == "end"))});')
ch_js.append(f'tl.to("#ctag",{{opacity:1,duration:0.3}},{R(SC["s13"]["start"])});')
ch_js.append(f'tl.to("#ctag",{{opacity:0,duration:0.3}},{R(SC["s13"]["start"] + next(l["t0"] for l in SC["s13"]["lines"] if l["cue"] == "end"))});')
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

# ---------------- captions: every spoken line, split into readable chunks (<= ~88 chars, 2 lines) ----------------
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
        if l.get("silent"): continue
        parts = chunks(l["text"]); tot = sum(len(p) for p in parts); t = sc["start"] + l["t0"]; d = l["t1"] - l["t0"]
        for p in parts:
            dd = d * len(p) / tot
            cap_els.append(f'<div id="cg{n}" class="cap"><span>{esc(p)}</span></div>')
            cap_js.append(f'tl.set("#cg{n}",{{opacity:1}},{R(t)});tl.set("#cg{n}",{{opacity:0}},{R(t + dd - 0.02)});'); t += dd; n += 1
open("edit/compositions/captions.html", "w").write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; }}
    .cap {{ position: absolute; left: 210px; width: 1500px; bottom: 74px; text-align: center; opacity: 0; }}
    .cap span {{ display: inline; background: rgba(20,33,61,.9); color: #fff; font-size: 36px; font-weight: 600; line-height: 1.5; padding: 6px 18px; border-radius: 10px;
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
hosts = "\n      ".join(f'<div id="h_{sc["id"]}" class="clip" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" data-start="{R(sc["start"])}" data-duration="{R(sc["dur"])}" '
                        f'data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:2"></div>' for sc in T["scenes"])
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
