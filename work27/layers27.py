# Shared layers for build27.py (exec'd inside it): bg, tab-map strip, mascot, captions, transitions, root index.html.
import shutil
def comp(cid, els, js, init=(), style=""):
    open(f"{OUT}/compositions/{cid}.html", "w").write(f'''<template>
  <style>#root {{ position:absolute; inset:0; overflow:hidden; font-family:{FONT}; }} .a {{ position:absolute; }} {style}</style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
    {(chr(10) + "    ").join(els)}
  </div>
  <script>
    {(chr(10) + "    ").join(init)}
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(js)}
    tl.set({{}}, {{}}, {R(TOTAL)});
    window.__timelines["{cid}"] = tl;
  </script>
</template>
''')

# ---------------- background ----------------
bg_els = [f'<div id="g1" class="a" style="left:{-W // 2}px;top:{-H // 2}px;width:{2 * W}px;height:{2 * H}px;background:radial-gradient(40% 30% at 30% 35%, #3b2366 0%, rgba(59,35,102,0) 70%), radial-gradient(35% 25% at 70% 65%, #2b1850 0%, rgba(43,24,80,0) 70%), linear-gradient(160deg,{PLUM},{PLUM2} 60%,#24123f)"></div>']
bg_js = [f'tl.to("#g1",{{x:{R(W * .25)},y:{R(H * .2)},rotation:8,duration:{R(TOTAL / 2)},ease:"sine.inOut"}},0);', f'tl.to("#g1",{{x:{R(-W * .1)},y:{R(-H * .1)},rotation:-4,duration:{R(TOTAL / 2)},ease:"sine.inOut"}},{R(TOTAL / 2)});']
for i in range(9):
    sz = 160 + (i * 53) % 280; x0 = (i * 263) % (W - 100); y0 = (i * 431) % (H - 100)
    bg_els.append(f'<div id="o{i}" class="a" style="left:{x0}px;top:{y0}px;width:{sz}px;height:{sz}px;border-radius:50%;background:radial-gradient(circle, rgba(255,158,27,{0.22 + 0.04 * (i % 3)}) 0%, rgba(255,158,27,0) 70%)"></div>')
    seg = TOTAL / 3
    for k in range(3):
        bg_js.append(f'tl.to("#o{i}",{{x:{(-1) ** (i + k) * (120 + 40 * k)},y:{(-1) ** (i // 2 + k) * (140 + 30 * i % 90)},duration:{R(seg)},ease:"sine.inOut"}},{R(k * seg)});')
for i in range(7):
    kind = i % 2; x0 = (i * 277) % (W - 300); y0 = 100 + (i * 291) % (H - 200)
    art = (f'<svg width="420" height="24" viewBox="0 0 420 24"><rect x="2" y="2" width="416" height="20" rx="10" fill="none" stroke="{AMBER}" stroke-width="3"/><path d="M40 2v20M380 2v20" stroke="{AMBER}" stroke-width="3"/></svg>' if kind == 0
           else f'<svg width="150" height="82" viewBox="0 0 100 55"><rect x="2" y="12" width="96" height="16" rx="5" fill="none" stroke="{AMBER}" stroke-width="2.6"/><path d="M44 20 L30 52 L40 52 L50 30 L60 52 L70 52 L56 20 Z" fill="none" stroke="{AMBER}" stroke-width="2.6"/></svg>')
    bg_els.append(f'<div id="la{i}" class="a" style="left:{x0}px;top:{y0}px;opacity:.12">{art}</div>')
    bg_js.append(f'tl.fromTo("#la{i}",{{rotation:{-30 + i * 17},x:0,y:0}},{{rotation:{10 + i * 23},x:{(-1) ** i * 160},y:{-200 + i * 40},duration:{R(TOTAL)},ease:"none",immediateRender:false}},0);')
comp("bg", bg_els, bg_js, style=f"#root {{ background:{PLUM2}; }}")

# ---------------- tab map strip (numbered tabs; current = amber, done = green tick; app tabs light green) ----------------
tm_els, tm_js, tm_init = [], [], ['gsap.set("#tm",{opacity:0,y:60});']
for i, t in enumerate(TABS + APP_TABS):
    x, y, w, h = TR[t]; app = t in APP_TABS; tid = f"t{i}"
    fs = (26 if O == "h" else 30) if not app else (21 if O == "h" else 24)
    num = "" if app else f'<span style="font-weight:800;opacity:.75;margin-right:6px">{i + 1}</span>'
    lab = f'<div class="a" style="inset:0;display:flex;align-items:center;justify-content:center;font-size:{fs}px;font-weight:800;white-space:nowrap">{num}{t}</div>'
    tm_els.append(f'<div id="{tid}" class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{h / 2}px;'
                  f'background:rgba(255,255,255,.08);border:2px {"dashed" if app else "solid"} rgba(255,255,255,.28);color:rgba(255,255,255,.75)">'
                  f'<div id="{tid}a" class="a" style="inset:0;border-radius:inherit;background:{AMBER}"></div><div id="{tid}g" class="a" style="inset:0;border-radius:inherit;background:#047857"></div>{lab}'
                  f'<div id="{tid}k" class="a" style="right:-9px;top:-12px;width:30px;height:30px;border-radius:50%;background:#fff;padding:4px;box-shadow:0 3px 8px rgba(0,0,0,.4)">{tick_svg("#047857")}</div></div>')
    tm_init.append(f'gsap.set("#{tid}a,#{tid}g,#{tid}k",{{opacity:0}});')
if O == "h":
    ax = TR["Fees"][0] - 46
    tm_els.append(f'<div class="a" style="left:{ax}px;top:{TR["Fees"][1] + 2}px;width:40px;height:44px">{SHEET_ICON.replace("#0f9d58", "#6b5a8a")}</div>')
else:
    tm_els.append(f'<div class="a" style="left:50px;top:{TR["Fees"][1] + 8}px;font-size:28px;font-weight:800;color:rgba(255,255,255,.6)">App fills:</div>')
tm_els = [f'<div id="tm" class="a" style="left:0;top:0;width:{W}px;height:{H}px">' + "".join(tm_els) + "</div>"]
idx = {t: i for i, t in enumerate(TABS + APP_TABS)}
tm_js.append(f'tl.to("#tm",{{opacity:1,y:0,duration:0.7,ease:"back.out(1.6)"}},{R(SC["s02"]["start"] + 0.2)});')
tm_js.append(f'tl.to("#tm",{{opacity:0,y:60,duration:0.5,ease:"power2.in"}},{R(SC["s24"]["start"])});')
for t, name, state in sorted(TAB_ON):
    p = f"#t{idx[name]}"
    if state == "on":
        tm_js.append(f'tl.to("{p}a",{{opacity:1,duration:0.3}},{R(t)});'); tm_js.append(f'tl.to("{p}",{{color:"{PLUM2}",scale:1.1,duration:0.35,ease:"back.out(3)"}},{R(t)});')
        CUES.append((R(t), "tick.wav", -22))
    elif state == "done":
        tm_js.append(f'tl.to("{p}g,{p}k",{{opacity:1,duration:0.3}},{R(t)});'); tm_js.append(f'tl.to("{p}a",{{opacity:0,duration:0.3}},{R(t + 0.2)});')
        tm_js.append(f'tl.to("{p}",{{color:"#ffffff",scale:1,duration:0.35}},{R(t)});')
        tm_js.append(f'tl.fromTo("{p}k",{{scale:0.2}},{{scale:1,duration:0.4,ease:"back.out(3)",immediateRender:false}},{R(t)});')
    elif state == "flash":
        tm_js.append(f'tl.fromTo("{p}a",{{opacity:1}},{{opacity:0,duration:0.6,ease:"power2.in",immediateRender:false}},{R(t)});')
        tm_js.append(f'tl.fromTo("{p}",{{scale:1.15}},{{scale:1,duration:0.5,ease:"power2.out",immediateRender:false}},{R(t)});')
    elif state == "app":
        tm_js.append(f'tl.to("{p}g",{{opacity:0.85,duration:0.3}},{R(t)});'); tm_js.append(f'tl.to("{p}",{{color:"#ffffff",duration:0.3}},{R(t)});')
        tm_js.append(f'tl.fromTo("{p}",{{scale:1.2}},{{scale:1,duration:0.4,ease:"back.out(3)",immediateRender:false}},{R(t)});')
comp("tabmap", tm_els, tm_js, tm_init)

# ---------------- mascot ----------------
mx, my = LAY["mas"]; flip = "transform:scaleX(-1);" if O == "v" else ""
THUMB = f'<svg width="100%" height="100%" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="{GREEN}"/><path transform="translate(4.2 4.2) scale(.65)" d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z" fill="#fff"/></svg>'
mas = f'''<div id="masw" class="a" style="left:{mx}px;top:{my}px;width:230px;height:380px;transform:scale({0.68 if O == "v" else 1});transform-origin:0 0"><div id="mas" class="a" style="left:0;top:0;width:230px;height:380px">
  <div class="a" style="left:0;top:0;width:230px;height:380px;{flip}">
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
  </svg></div>
  <div id="thb" class="a" style="left:{-10 if O == "v" else 150}px;top:-30px;width:96px;height:96px;filter:drop-shadow(0 8px 14px rgba(0,0,0,.45))">{THUMB}</div></div></div>'''
ms_js, ms_init = [], ['gsap.set("#mas",{opacity:0,y:260});', 'gsap.set("#thb",{opacity:0,scale:.3});']
ms_js.append('tl.to("#mas",{opacity:1,y:0,duration:0.9,ease:"back.out(1.6)"},0.3);')
n_b = int((TOTAL - 1.5) / 2.0); ms_js.append(f'tl.to("#mbody",{{y:-10,duration:1.0,ease:"sine.inOut",yoyo:true,repeat:{2 * n_b - 1}}},1.3);')
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
        ms_js.append(f'tl.to("#mas",{{y:-60,duration:0.32,ease:"power2.out",yoyo:true,repeat:3}},{R(t)});')
        ms_js.append(f'tl.to("#armL,#armR",{{rotation:0,duration:0.45,ease:"power2.inOut"}},{R(t + 1.4)});')
    elif act == "thumb":
        ms_js.append(f'tl.to("#armR",{{rotation:-150,duration:0.3,ease:"back.out(2)"}},{R(t)});')
        ms_js.append(f'tl.to("#thb",{{opacity:1,scale:1,duration:0.45,ease:"back.out(3)"}},{R(t + 0.1)});')
        ms_js.append(f'tl.to("#thb",{{rotation:-12,duration:0.18,yoyo:true,repeat:3,ease:"sine.inOut"}},{R(t + 0.5)});')
        ms_js.append(f'tl.to("#mouth",{{scaleY:1.5,transformOrigin:"50% 0%",duration:0.2,yoyo:true,repeat:1}},{R(t)});')
        ms_js.append(f'tl.to("#thb",{{opacity:0,scale:.4,duration:0.3,ease:"power2.in"}},{R(t + 1.5)});')
        ms_js.append(f'tl.to("#armR",{{rotation:0,duration:0.4,ease:"power2.inOut"}},{R(t + 1.5)});')
        CUES.append((R(t + 0.1), "curated/ui-pop.wav", -20))
    elif act == "talk":
        ms_js.append(f'tl.to("#mouth",{{scaleY:1.6,transformOrigin:"50% 0%",duration:0.15,yoyo:true,repeat:7}},{R(t)});')
# mascot belt climbs a colour each time a tab is done
done_t = sorted({t for t, n_, st in TAB_ON if st == "done" and n_ in TABS})
for i, t in enumerate(done_t[:5]):
    ms_js.append(f'tl.to("#mbelt,#mknot",{{fill:"{BELTS[i + 1]}",duration:0.4}},{R(t)});')
comp("mascot", [mas], ms_js, ms_init, style="#root { overflow:visible; }")

# ---------------- captions ----------------
KEY = {"vanakkam", "admin", "together", "config", "belts", "masters", "classes", "students", "enrolments", "parents", "access", "persatuan", "app",
       "order", "colour", "paints", "easy", "gmail", "bank", "id", "place", "time", "master", "arrow", "ic", "twice", "important", "belt", "list", "here",
       "fee", "yes", "done", "row", "numbers", "finds", "class", "children", "comma", "role", "parent", "student", "pin", "fees", "green", "paid", "red", "due",
       "gradings", "attendance", "dont", "notices", "rest", "golden", "rules", "never", "top", "lists", "no", "great", "job", "itself", "every"}
norm = lambda w: "".join(c for c in w.lower() if c.isalnum())
cx, cyy, cw, chh, cfs = LAY["cap"]
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
        if norm(w["w"]) not in KEY: cap_js.append(f'tl.to("#c{n}w{i}",{{color:"#ffffff",scale:1,duration:0.15}},{R(max(we, ws + 0.12))});')
        else: cap_js.append(f'tl.to("#c{n}w{i}",{{scale:1,duration:0.15}},{R(max(we, ws + 0.12))});')
    CUES.append((R(t0 - 0.1), "curated/ui-pop.wav", -28))
    srt.append(f"{n + 1}\n{fmt(t0)} --> {fmt(sc['start'] + l['t1'])}\n{l['text']}\n"); n += 1
comp("captions", cap_els, cap_js, cap_init, style=f'''
    @font-face {{ font-family:"Jakarta"; font-weight:800; src:url("assets/fonts/plus-jakarta-sans-latin-800-normal.woff2") format("woff2"); }}
    .cg {{ position:absolute; left:{cx}px; width:{cw}px; top:{cyy}px; height:{chh}px; display:flex; align-items:center; justify-content:center; text-align:center; }}
    .cb {{ display:inline-block; padding:14px 32px; border-radius:34px; background:rgba(18,10,33,.84); box-shadow:0 18px 40px rgba(0,0,0,.35); font-weight:800; font-size:{cfs}px; line-height:1.12; color:#fff; }}
    .w {{ display:inline-block; margin:0 .14em; }}''')
os.makedirs("videos", exist_ok=True); open(f"{OUT}/captions.srt", "w").write("\n".join(srt))

# ---------------- transitions at every cut ----------------
tr_els, tr_js, tr_init = [], [], []
cuts = [sc["start"] for sc in T["scenes"][1:]]
for i, b in enumerate(cuts):
    kind = ["belt", "swipe", "zoom", "stick"][i % 4]; p = f"x{i}"
    if kind == "belt":
        sw = W / 6
        for j, col in enumerate(BELTS):
            tr_els.append(f'<div id="{p}s{j}" class="a" style="left:{R(j * sw)}px;top:0;width:{R(sw + 1)}px;height:{H}px;background:{col}"></div>')
            tr_init.append(f'gsap.set("#{p}s{j}",{{yPercent:-100}});')
            tr_js.append(f'tl.to("#{p}s{j}",{{yPercent:0,duration:0.32,ease:"power2.in"}},{R(b - 0.4 + 0.012 * j)});')
            tr_js.append(f'tl.to("#{p}s{j}",{{yPercent:100,duration:0.34,ease:"power2.out"}},{R(b + 0.02 + 0.012 * j)});')
    elif kind == "swipe":
        tr_els.append(f'<div id="{p}p" class="a" style="left:0;top:0;width:{W + 220}px;height:{H}px;background:linear-gradient(90deg,{AMBER} 0 70px,{PLUM} 70px)"></div>')
        tr_init.append(f'gsap.set("#{p}p",{{x:{W + 20}}});')
        tr_js.append(f'tl.to("#{p}p",{{x:-110,duration:0.38,ease:"power3.in"}},{R(b - 0.38)});'); tr_js.append(f'tl.to("#{p}p",{{x:{-(W + 320)},duration:0.4,ease:"power3.out"}},{R(b)});')
    elif kind == "zoom":
        tr_els.append(f'<div id="{p}c" class="a" style="left:{W / 2 - 100}px;top:{H / 2 - 100}px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,{AMBER} 0 55%,{PLUM} 56%)"></div>')
        tr_init.append(f'gsap.set("#{p}c",{{scale:0}});')
        tr_js.append(f'tl.to("#{p}c",{{scale:14,duration:0.4,ease:"power2.in"}},{R(b - 0.4)});'); tr_js.append(f'tl.to("#{p}c",{{scale:0,duration:0.4,ease:"power2.out"}},{R(b + 0.02)});')
    else:
        tr_els.append(f'<div id="{p}w" class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:{PLUM}"></div>')
        tr_els.append(f'<div id="{p}k" class="a" style="left:-60px;top:{H / 2 - 22}px;width:{W + 120}px;height:44px">{stick_svg(W + 120, 44)}</div>')
        tr_init.append(f'gsap.set("#{p}w",{{clipPath:"circle(0% at 50% 50%)"}});gsap.set("#{p}k",{{opacity:0,scale:.4,rotation:0}});')
        tr_js.append(f'tl.to("#{p}w",{{clipPath:"circle(75% at 50% 50%)",duration:0.4,ease:"power2.in"}},{R(b - 0.4)});')
        tr_js.append(f'tl.set("#{p}k",{{opacity:1}},{R(b - 0.4)});'); tr_js.append(f'tl.to("#{p}k",{{scale:1,rotation:360,duration:0.8,ease:"power2.inOut"}},{R(b - 0.4)});')
        tr_js.append(f'tl.to("#{p}w",{{clipPath:"circle(0% at 50% 50%)",duration:0.4,ease:"power2.out"}},{R(b + 0.02)});')
        tr_js.append(f'tl.to("#{p}k",{{opacity:0,duration:0.2}},{R(b + 0.25)});')
    CUES.append((R(b - 0.3), "curated/zoom-swish.wav", -19))
comp("trans", tr_els, tr_js, tr_init, style="#root { pointer-events:none; }")

# ---------------- root ----------------
def host(cid, start, dur, z, track, kind="graphics"):
    return (f'<div id="h_{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{R(start)}" data-duration="{R(dur)}" '
            f'data-track-index="{track}" data-track-kind="{kind}" data-width="{W}" data-height="{H}" style="z-index:{z}"></div>')
hosts = [host("bg", 0, TOTAL, 1, 1)] + [host(sc["id"], sc["start"], sc["dur"], 2, 2) for sc in T["scenes"]] + \
        [host("tabmap", 0, TOTAL, 3, 3), host("mascot", 0, TOTAL, 4, 4), host("captions", 0, TOTAL, 5, 5, "captions"), host("trans", 0, TOTAL, 6, 6)]
open(f"{OUT}/index.html", "w").write(f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{PLUM2}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="{W}" data-height="{H}" data-start="0" data-duration="{R(TOTAL)}" data-fps="30">
      {(chr(10) + "      ").join(hosts)}
      <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{R(TOTAL)}" data-track-index="7" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
''')
json.dump({"cues": [{"t": a, "sfx": b, "gain_db": c} for a, b, c in sorted(CUES)]}, open(f"{OUT}/cues.json", "w"), indent=1)
# assets: sheets + fonts copied into the project (renderer serves only the project folder)
if not os.path.isdir(f"{OUT}/assets/sheets"): shutil.copytree("video/assets/sheets", f"{OUT}/assets/sheets")
if not os.path.isdir(f"{OUT}/assets/fonts"): shutil.copytree("../work25/video/assets/fonts", f"{OUT}/assets/fonts")
print(O, "built", len(scenes), "scenes;", n, "caption lines;", len(CUES), "sfx; total", TOTAL)
