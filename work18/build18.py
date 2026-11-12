# Promo reel: "I recreate movie scenes" - 9:16, 1080x1920, 30 fps -> edit/index.html (+ edit/cues.json for mix18.py)
#  0      intro MG + AI voice: "Check this out! This is the original scene from the movie."
#  4.4    the original scene (creator's clip, 0-17.4 s; the TikTok logo end card is cut), with its own song
#  21.8   MG + voice: "Now... I recreated this exact scene, just for me!"
#  26.0   the creator's recreation, full 32.17 s, with its own song
#  58.17  CTA MG + voice: DM me / RM20 per video / today & tomorrow only (Thu 12 & Fri 13 Nov 2026) / DM me now
import json, math, random, html
V = json.load(open("vo_timing.json")); R = lambda v: round(v, 3); esc = html.escape
I1, C1 = 4.4, 17.4; M0 = I1 + C1; M1 = M0 + 4.2; C2 = 965 / 30; Z0 = M1 + C2; TOTAL = R(Z0 + 15.0)
VO = {"intro": 0.0, "mid": M0, "cta": Z0}
vt = lambda part, i: R(VO[part] + V[part]["lines"][i]["t0"])
GOLD, RED, INK, CREAM = "#f5b72c", "#e8213a", "#0b0a10", "#fff3d6"
els, js, init, cues = [], [], [], []
E, J, I = els.append, js.append, init.append
rnd = random.Random(18)


def cue(t, s, g): cues.append((R(t), s, g))
def tw(sel, t, d, p, ease="power3.out"): J(f'tl.to("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in p.items())},duration:{R(d)},ease:"{ease}"}},{R(t)});')
def st(sel, t, p): J(f'tl.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in p.items())}}},{R(t)});')
def gs(sel, p): I(f'gsap.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in p.items())}}});')


def show(eid, t_in, t_out=None, how="up", d=0.5):
    fr = {"up": {"opacity": 0, "y": 60}, "pop": {"opacity": 0, "scale": 0.5}, "punch": {"opacity": 0, "scale": 1.6}, "left": {"opacity": 0, "x": -120},
          "right": {"opacity": 0, "x": 120}, "fade": {"opacity": 0}}[how]
    gs(f"#{eid}", fr); to = {k: (1 if k in ("opacity", "scale") else 0) for k in fr}
    tw(f"#{eid}", t_in, d, to, "back.out(1.7)" if how == "pop" else ("expo.out" if how == "punch" else "power3.out"))
    if t_out is not None: tw(f"#{eid}", t_out - 0.3, 0.3, {"opacity": 0}, "power2.in")


def section(sid, t0, t1, inner, bg):
    E(f'<div id="{sid}" class="sec" style="background:{bg}">{inner}</div>'); gs(f"#{sid}", {"opacity": 0}); st(f"#{sid}", t0, {"opacity": 1})
    if t1 < TOTAL: st(f"#{sid}", t1, {"opacity": 0})


def particles(pid, x, y, n, colors, spread, t, d=1.2, size=12):
    dots = []
    for k in range(n):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(0.4, 1.0) * spread; s = rnd.uniform(0.6, 1.4) * size
        dots.append(f'<i id="{pid}{k}" style="left:{x}px;top:{y}px;width:{s:.0f}px;height:{s:.0f}px;background:{colors[k % len(colors)]}"></i>')
        gs(f"#{pid}{k}", {"xPercent": -50, "yPercent": -50, "opacity": 0, "scale": 0.4}); st(f"#{pid}{k}", t, {"opacity": 1})
        tw(f"#{pid}{k}", t, d, {"x": R(math.cos(a) * r), "y": R(math.sin(a) * r * 0.8 + spread * 0.3), "scale": 1, "opacity": 0}, "power2.out")
    E(f'<div class="pt">{"".join(dots)}</div>')


def wipe(wid, t):
    """gold bar sweeps down over the cut"""
    E(f'<div id="{wid}" class="wipe" data-layout-allow-overflow></div>'); gs(f"#{wid}", {"yPercent": -101})
    tw(f"#{wid}", t - 0.35, 0.35, {"yPercent": 0}, "power3.in"); tw(f"#{wid}", t, 0.4, {"yPercent": 101}, "power3.out"); cue(t - 0.3, "curated/zoom-swish.wav", -10)


BG = f"radial-gradient(ellipse at 50% 40%, #3a2208 0%, #170d06 45%, {INK} 80%)"
FILM = '<div class="film l"></div><div class="film r"></div>'

# ---------- videos (muted: the clips' own songs are in the mix) ----------
VIDS = f'''
      <video id="v1bg" class="clip vb" src="assets/v/orig_bg.mp4" muted playsinline data-start="{I1}" data-duration="{C1}" data-track-index="1"></video>
      <video id="v1" class="clip vf" src="assets/v/orig_fg.mp4" muted playsinline data-start="{I1}" data-duration="{C1}" data-track-index="2" style="left:50px;top:300px;width:980px;height:1148px"></video>
      <video id="v2bg" class="clip vb" src="assets/v/rec_bg.mp4" muted playsinline data-start="{R(M1)}" data-duration="{R(C2)}" data-track-index="1"></video>
      <video id="v2" class="clip vf" src="assets/v/rec_fg.mp4" muted playsinline data-start="{R(M1)}" data-duration="{R(C2)}" data-track-index="2" style="left:90px;top:190px;width:900px;height:1600px"></video>'''

# ---------- 1 INTRO ----------
section("intro", 0, I1, FILM + '<div class="spot" id="spot"></div>', BG)
E('<div id="i_k" class="kick">CHECK THIS OUT!</div>'); tw("#i_k", 0.05, 0.2, {"scale": 1.12}, "power2.out"); tw("#i_k", 0.25, 0.3, {"scale": 1}, "power2.inOut"); tw("#i_k", I1 - 0.3, 0.3, {"opacity": 0}, "power2.in")
E(f'<div id="i_t1" class="huge" style="top:640px">THE ORIGINAL</div><div id="i_t2" class="huge gold" style="top:800px;font-size:150px">MOVIE SCENE</div>')
show("i_t1", vt("intro", 1), I1, "left"); show("i_t2", vt("intro", 1) + 0.25, I1, "right"); cue(vt("intro", 1), "curated/hook-impact.wav", -12)
E('<div id="i_w" class="pw" style="top:1080px"><span class="pill dark">▼  Watch this first</span></div>'); show("i_w", vt("intro", 1) + 1.0, I1, "up")
tw("#spot", 0.0, I1, {"x": 260}, "sine.inOut"); gs("#spot", {"x": -260})
cue(0.05, "curated/hook-impact.wav", -14)
wipe("w1", I1)

# ---------- during the original ----------
E('<div id="o_chip" class="chip">🎬  ORIGINAL SCENE · FROM THE MOVIE</div>'); show("o_chip", I1 + 0.3, M0, "up")
E('<div id="o_next" class="pw" style="top:1530px"><span class="pill gold-b">NEXT: MY VERSION ▶</span></div>'); show("o_next", M0 - 3.2, M0, "pop"); cue(M0 - 3.2, "curated/ui-pop.wav", -16)

# ---------- 2 MID ----------
section("mid", M0, M1, FILM, BG)
E('<div id="m_k" class="kick" style="top:560px">NOW…</div>'); show("m_k", vt("mid", 0), M1, "fade")
E('<div id="m_t1" class="huge gold" style="top:660px;font-size:150px">I RECREATED</div><div id="m_t2" class="huge" style="top:830px;font-size:96px">THIS EXACT SCENE</div>')
show("m_t1", vt("mid", 0) + 0.5, M1, "punch"); show("m_t2", vt("mid", 0) + 0.9, M1, "up"); cue(vt("mid", 0) + 0.5, "sub-impact.wav", -10)
E('<div id="m_t3" class="script">just for me ✨</div>'); show("m_t3", vt("mid", 1), M1, "pop"); cue(vt("mid", 1), "sparkle.wav", -14)
particles("mp", 540, 1030, 26, [GOLD, CREAM, "#ffd36e", "#ffffff"], 420, vt("mid", 1) + 0.1)
wipe("w2", M1)

# ---------- during the recreation ----------
E('<div id="r_chip" class="chip gold-c" style="top:96px">✨  MY RECREATION</div>'); show("r_chip", M1 + 0.3, Z0, "up")
E(f'<div id="r_stk" class="sticker"><b>WANT YOURS?</b><span>RM20</span><i>per video</i></div>')
gs("#r_stk", {"opacity": 0, "scale": 0.3, "rotation": -30}); tw("#r_stk", Z0 - 8.0, 0.55, {"opacity": 1, "scale": 1, "rotation": -8}, "back.out(1.8)")
tw("#r_stk", Z0 - 7.3, 0.4, {"scale": 1.08}, "sine.inOut"); tw("#r_stk", Z0 - 6.9, 0.4, {"scale": 1}, "sine.inOut"); tw("#r_stk", Z0 - 0.3, 0.3, {"opacity": 0}, "power2.in")
cue(Z0 - 8.0, "curated/ui-pop.wav", -14)

# ---------- 3 CTA ----------
section("cta", Z0, TOTAL, FILM + '<div class="rays" id="rays"></div>', BG)
tw("#rays", Z0, TOTAL - Z0, {"rotation": 60}, "none")
E('<div id="c_q" class="huge" style="top:250px;font-size:96px">WANT YOUR<br><span class="gold">OWN VERSION?</span></div>'); show("c_q", vt("cta", 0), None, "punch"); cue(vt("cta", 0), "curated/hook-impact.wav", -13)
DM = '<svg width="96" height="96" viewBox="0 0 24 24"><path d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" fill="#0b0a10"/><circle cx="8" cy="11" r="1.4" fill="#f5b72c"/><circle cx="12" cy="11" r="1.4" fill="#f5b72c"/><circle cx="16" cy="11" r="1.4" fill="#f5b72c"/></svg>'
E(f'<div id="c_dm" class="pw" style="top:540px"><span class="dm">{DM}<span>DM ME</span></span></div>'); show("c_dm", vt("cta", 1), None, "pop"); cue(vt("cta", 1), "curated/ui-pop.wav", -12)
E('<div id="c_price" class="price"><div class="pin">ONLY</div><div class="amt">RM20</div><div class="per">PER VIDEO</div></div>')
gs("#c_price", {"opacity": 0, "scale": 0.2, "rotation": -25}); tw("#c_price", vt("cta", 2), 0.6, {"opacity": 1, "scale": 1, "rotation": -6}, "back.out(1.6)")
tw("#c_price", vt("cta", 2) + 0.8, 0.5, {"scale": 1.06}, "sine.inOut"); tw("#c_price", vt("cta", 2) + 1.3, 0.5, {"scale": 1}, "sine.inOut")
particles("cp", 540, 860, 34, [GOLD, CREAM, "#ffd36e", RED, "#ffffff"], 480, vt("cta", 2) + 0.2, 1.4, 14)
cue(vt("cta", 2), "sub-impact.wav", -9); cue(vt("cta", 2) + 0.2, "sparkle.wav", -12)
E('<div id="c_rib" class="ribbon">⏰ PROMO · TODAY &amp; TOMORROW ONLY</div>'); show("c_rib", vt("cta", 3), None, "left"); cue(vt("cta", 3), "curated/zoom-swish.wav", -14)
for i, (dow, d, lab) in enumerate((("THU", "12", "TODAY"), ("FRI", "13", "TOMORROW"))):
    E(f'<div id="c_d{i}" class="cal" style="left:{170 + i * 400}px"><div class="cm">NOV 2026</div><div class="cd">{d}</div><div class="cw">{dow}</div><div class="cl">{lab}</div></div>')
    show(f"c_d{i}", vt("cta", 3) + 2.3 + 0.9 * i, None, "pop"); cue(vt("cta", 3) + 2.3 + 0.9 * i, "curated/ui-pop.wav", -13)
E('<div id="c_go" class="go">DM ME NOW · OFFER ENDS 13 NOV</div>'); show("c_go", vt("cta", 4), None, "up"); cue(vt("cta", 4), "clean-ding.wav", -12)
for k in range(4): tw("#c_go", vt("cta", 4) + 0.8 + 0.9 * k, 0.45, {"scale": 1.05}, "sine.inOut"); tw("#c_go", vt("cta", 4) + 1.25 + 0.9 * k, 0.45, {"scale": 1}, "sine.inOut")
E('<div id="fade" class="fadeout"></div>'); gs("#fade", {"opacity": 0}); tw("#fade", TOTAL - 0.6, 0.6, {"opacity": 1}, "power1.in")

CSS = f'''
@font-face {{ font-family: "IDB"; src: url("assets/fonts/InterDisplay-Black.otf"); font-weight: 900; }}
@font-face {{ font-family: "IDBo"; src: url("assets/fonts/InterDisplay-Bold.otf"); font-weight: 700; }}
@font-face {{ font-family: "ISB"; src: url("assets/fonts/Inter-SemiBold.otf"); font-weight: 600; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
.vb {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; z-index: 1; }}
.vf {{ position: absolute; z-index: 2; object-fit: cover; border-radius: 34px; box-shadow: 0 0 0 5px rgba(245,183,44,.85), 0 40px 90px rgba(0,0,0,.65); }}
#gfx {{ z-index: 10; pointer-events: none; overflow: hidden; }}
.sec {{ position: absolute; inset: 0; }}
.film {{ position: absolute; top: 0; bottom: 0; width: 58px; background: repeating-linear-gradient(180deg, #000 0 26px, rgba(255,255,255,.14) 26px 52px); opacity: .55; }}
.film.l {{ left: 0; }} .film.r {{ right: 0; }}
.spot {{ position: absolute; left: 140px; top: 300px; width: 800px; height: 1100px; background: radial-gradient(ellipse, rgba(255,214,120,.22), rgba(255,214,120,0) 65%); }}
.rays {{ position: absolute; left: -460px; top: -100px; width: 2000px; height: 2000px; border-radius: 50%;
  background: repeating-conic-gradient(from 0deg, rgba(245,183,44,.10) 0deg 8deg, rgba(245,183,44,0) 8deg 20deg); }}
.kick {{ position: absolute; left: 0; width: 1080px; top: 470px; text-align: center; font-family: "IDB"; font-size: 64px; letter-spacing: 8px; color: {CREAM}; }}
.huge {{ position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDB"; font-size: 128px; line-height: 1.02; letter-spacing: -2px; color: #fff;
  text-shadow: 0 14px 40px rgba(0,0,0,.6); }}
.gold, .huge.gold {{ background: linear-gradient(180deg, #fff1b8 0%, #f5b72c 45%, #c47f0a 75%, #ffe08a 100%); -webkit-background-clip: text; background-clip: text; color: transparent; text-shadow: none;
  filter: drop-shadow(0 10px 24px rgba(0,0,0,.6)); }}
.script {{ position: absolute; left: 0; width: 1080px; top: 1000px; text-align: center; font-family: "IDBo"; font-style: italic; font-size: 92px; color: {CREAM}; }}
.pw {{ position: absolute; left: 0; width: 1080px; text-align: center; }}
.pill {{ display: inline-block; white-space: nowrap; font-family: "IDB"; font-size: 46px; letter-spacing: 3px; padding: 18px 40px; border-radius: 60px; }}
.pill.dark {{ background: rgba(255,255,255,.12); color: #fff; border: 2px solid rgba(255,255,255,.35); }}
.pill.gold-b {{ background: {GOLD}; color: {INK}; box-shadow: 0 16px 40px rgba(0,0,0,.5); }}
.chip {{ position: absolute; left: 0; width: 1080px; top: 190px; text-align: center; }}
.chip, .chip.gold-c {{ font-family: "IDB"; font-size: 40px; letter-spacing: 3px; color: #fff; text-shadow: 0 4px 14px rgba(0,0,0,.85); }}
.chip.gold-c {{ color: {GOLD}; }}
.sticker {{ position: absolute; left: 700px; top: 1500px; width: 320px; height: 320px; border-radius: 50%; background: {RED}; color: #fff; display: flex; flex-direction: column;
  align-items: center; justify-content: center; box-shadow: 0 0 0 8px {GOLD}, 0 24px 60px rgba(0,0,0,.6); text-align: center; }}
.sticker b {{ font-family: "IDB"; font-size: 34px; letter-spacing: 1px; }} .sticker span {{ font-family: "IDB"; font-size: 96px; line-height: 1; }} .sticker i {{ font-family: "ISB"; font-style: normal; font-size: 30px; }}
.dm {{ display: inline-flex; align-items: center; gap: 20px; background: {GOLD}; color: {INK}; padding: 22px 54px 22px 36px;
  border-radius: 80px; font-family: "IDB"; font-size: 84px; white-space: nowrap; box-shadow: 0 20px 50px rgba(0,0,0,.55); }}
.price {{ position: absolute; left: 290px; top: 720px; width: 500px; height: 500px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center;
  background: radial-gradient(circle at 35% 30%, #fff3c4, {GOLD} 45%, #b9760a 100%); box-shadow: 0 0 0 10px {RED}, 0 0 90px rgba(245,183,44,.6), 0 30px 70px rgba(0,0,0,.6); color: {INK}; }}
.price .pin {{ font-family: "IDB"; font-size: 44px; letter-spacing: 6px; }} .price .amt {{ font-family: "IDB"; font-size: 158px; line-height: .95; letter-spacing: -6px; }}
.price .per {{ font-family: "IDB"; font-size: 46px; letter-spacing: 4px; }}
.ribbon {{ position: absolute; left: 40px; width: 1000px; top: 1290px; text-align: center; background: {RED}; color: #fff; font-family: "IDB"; font-size: 44px; letter-spacing: 0; white-space: nowrap;
  padding: 20px 10px; border-radius: 16px; box-shadow: 0 16px 40px rgba(0,0,0,.5); }}
.cal {{ position: absolute; top: 1420px; width: 340px; height: 290px; border-radius: 24px; background: #fff; overflow: hidden; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,.5); }}
.cal .cm {{ background: {RED}; color: #fff; font-family: "IDB"; font-size: 34px; letter-spacing: 4px; padding: 10px 0; }}
.cal .cd {{ font-family: "IDB"; font-size: 120px; line-height: 1.05; color: {INK}; }} .cal .cw {{ font-family: "IDB"; font-size: 34px; color: #555; letter-spacing: 6px; }}
.cal .cl {{ font-family: "IDB"; font-size: 30px; color: {RED}; letter-spacing: 4px; margin-top: 4px; }}
.go {{ position: absolute; left: 60px; width: 960px; top: 1755px; text-align: center; background: {GOLD}; color: {INK}; font-family: "IDB"; font-size: 46px; padding: 20px 0; border-radius: 60px;
  box-shadow: 0 16px 40px rgba(0,0,0,.5); }}
.wipe {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: linear-gradient(180deg, {GOLD}, #c47f0a); z-index: 30; }}
.pt {{ position: absolute; inset: 0; }} .pt i {{ position: absolute; border-radius: 50%; display: block; }}
.fadeout {{ position: absolute; inset: 0; background: #000; z-index: 40; }}
'''
doc = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{TOTAL}">
      {VIDS}
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-volume="1"></audio>
      <div id="gfx" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="3" style="position:absolute;inset:0">
        {(chr(10) + "        ").join(els)}
      </div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      {(chr(10) + "      ").join(init)}
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(js)}
      tl.set({{}}, {{}}, {TOTAL});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("edit/index.html", "w").write(doc)
json.dump({"total": TOTAL, "intro": [0, I1], "orig": [I1, R(M0)], "mid": [R(M0), R(M1)], "rec": [R(M1), R(Z0)], "cta": [R(Z0), TOTAL], "vo": VO,
           "cues": [{"t": a, "sfx": b, "gain_db": c} for a, b, c in sorted(cues)]}, open("edit/cues.json", "w"), indent=1)
print("built", TOTAL)
