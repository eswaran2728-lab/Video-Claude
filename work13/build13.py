# HyperFrames composition for one part -> edit/index.html (usage: python3 build13.py part1|part2).
# Graphics follow two Prompt Motion references, adapted (not copied):
#  - "Festival lineup promo reel" (prompt-motion.com/gonzalomacagno-2de1a9): vertical poster system - colour date bar,
#    one huge headline, stacked lines rising out of a mask line -> title card, Part 2 tease and end card.
#  - "Bold kinetic type showreel" (prompt-motion.com/shneural-2abdfa): one giant word that punches in on the hit and
#    repeating marquee type rows -> impact words on the stunts, marquee wipe into each action section.
# Only text visible in the footage is used for the event (banner: FESTIVAL KESENIAN & KEBUDAYAAN MALAYSIA 2026,
# 31/10/2026 & 1/11/2026; shirts: SILAMBAM). Every timing comes from the rendered plate (edit/<part>_audio.json).
import json, sys, os, html, importlib
part = sys.argv[1] if len(sys.argv) > 1 else "part1"
VERSION = os.environ.get("VERSION", "v01"); SUF = "" if VERSION == "v01" else "_" + VERSION
P = importlib.import_module("plan13" if VERSION == "v01" else f"plan13_{VERSION}")
LOGO = "assets/logo_arumugam.png"            # v02: creator's Mahaguru logo (cut out), shown beside the header wording if present
A = json.load(open(f"edit/{part}_audio{SUF}.json")); S = A["seg_starts"]; T = A["total"]; R = lambda v: round(v, 3)
RED, GOLD, INK = "#e1124b", "#f2b705", "#0e0b10"
els, js, init = [], [], []
E, J, I = els.append, js.append, init.append


def tw(sel, t, d, props, ease="power3.out"):
    J(f'tl.to("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())},duration:{R(d)},ease:"{ease}"}},{R(t)});')


def st(sel, t, props):
    J(f'tl.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())}}},{R(t)});')


def chip(i, text, t0, t1, y=1150, color=RED):
    E(f'<div id="chip{i}" class="chip" style="top:{y}px;background:{color}">{html.escape(text)}</div>')
    I(f'gsap.set("#chip{i}",{{xPercent:-50,opacity:0,y:16}});')
    tw(f"#chip{i}", t0, 0.3, {"opacity": 1, "y": 0}); tw(f"#chip{i}", t1 - 0.25, 0.25, {"opacity": 0, "y": -10}, "power2.in")


def caption(i, lines, t0, t1, sub=None):
    body = "<br>".join(f'<span class="t">{html.escape(l)}</span>' for l in lines)
    if sub: body += f'<br><span class="sub">{html.escape(sub)}</span>'
    E(f'<div id="cap{i}" class="cap">{body}</div>')
    I(f'gsap.set("#cap{i}",{{opacity:0,y:12}});')
    tw(f"#cap{i}", t0, 0.18, {"opacity": 1, "y": 0}, "power2.out"); st(f"#cap{i}", t1, {"opacity": 0})


def impact_word(i, word, t, hold=1.1, size=200):
    E(f'<div id="kw{i}" class="kw" style="font-size:{size}px">{html.escape(word)}<span class="dot">.</span></div>')
    E(f'<div id="fl{i}" class="flash"></div>')
    I(f'gsap.set("#kw{i}",{{xPercent:-50,yPercent:-50,opacity:0,scale:1.45}}); gsap.set("#fl{i}",{{opacity:0}});')
    st(f"#fl{i}", t, {"opacity": 0.75}); tw(f"#fl{i}", t + 0.02, 0.22, {"opacity": 0}, "power2.out")
    st(f"#kw{i}", t, {"opacity": 1}); tw(f"#kw{i}", t, 0.2, {"scale": 1}, "expo.out")
    tw(f"#kw{i}", t + hold, 0.22, {"opacity": 0, "scale": 0.92}, "power2.in")


def marquee(i, word, t, d=0.9):
    rows = "".join(f'<div class="mrow" id="mq{i}r{k}" style="top:{560 + k * 280}px;color:{RED if k % 2 else "#ffffff"}">'
                   + (f"{word} · " * 8) + "</div>" for k in range(3))
    E(f'<div id="mq{i}" class="mq">{rows}</div>')
    I(f'gsap.set("#mq{i}",{{opacity:0}});')
    for k in range(3):
        I(f'gsap.set("#mq{i}r{k}",{{x:{-200 if k % 2 else -900}}});')
        tw(f"#mq{i}r{k}", t, d, {"x": -900 if k % 2 else -200}, "none")
    st(f"#mq{i}", t, {"opacity": 1}); tw(f"#mq{i}", t + d - 0.2, 0.2, {"opacity": 0}, "power2.in")


def poster(i, t0, t1, top, head, lines, cta=None, dark=True):
    """festival-lineup card: colour bar + date strip, huge headline, stacked lines rising out of a mask"""
    ls = "".join(f'<div class="pl"><div class="pli" id="p{i}l{k}">{html.escape(l)}</div></div>' for k, l in enumerate(lines))
    c = f'<div class="pcta" id="p{i}c">{html.escape(cta)}</div>' if cta else ""
    E(f'<div id="p{i}" class="poster{" dark" if dark else ""}"><div class="pbar" id="p{i}b"><i></i><i></i><span>{html.escape(top)}</span></div>'
      f'<div class="ph"><div class="phi" id="p{i}h">{html.escape(head)}</div></div>{ls}{c}</div>')
    I(f'gsap.set("#p{i}",{{opacity:0}}); gsap.set("#p{i}b",{{scaleX:0}}); gsap.set("#p{i}h",{{yPercent:110}});')
    for k in range(len(lines)): I(f'gsap.set("#p{i}l{k}",{{yPercent:110}});')
    if cta: I(f'gsap.set("#p{i}c",{{opacity:0,y:20}});')
    st(f"#p{i}", t0, {"opacity": 1}); tw(f"#p{i}b", t0, 0.35, {"scaleX": 1}, "power3.inOut")
    tw(f"#p{i}h", t0 + 0.15, 0.45, {"yPercent": 0}, "power4.out")
    for k in range(len(lines)): tw(f"#p{i}l{k}", t0 + 0.35 + 0.12 * k, 0.4, {"yPercent": 0}, "power3.out")
    if cta: tw(f"#p{i}c", t0 + 0.7, 0.35, {"opacity": 1, "y": 0}, "power3.out")
    if t1 < T - 0.01: tw(f"#p{i}", t1 - 0.25, 0.25, {"opacity": 0}, "power2.in")


imp = {x["seg"]: x["t"] for x in A["impacts"]}
X = lambda clip, src_in: S[P.idx(part, clip, src_in)] if VERSION != "v01" else None


def header():
    """v02: gold 'MAHAGURU SRI S ARUMUGAM / STUDENTS' lockup at the top for the whole part, logo beside it when supplied"""
    has_logo = os.path.exists(os.path.join("edit", LOGO))
    logo = f'<img class="hlogo" src="{LOGO}" alt="" />' if has_logo else ""
    E(f'<div id="hshade"></div><div id="hdr">{logo}<div class="htext"><div class="hl1">MAHAGURU SRI S ARUMUGAM</div>'
      f'<div class="hl2"><i></i>STUDENTS<i></i></div></div></div>')
    I('gsap.set("#hdr",{xPercent:-50});')
    return has_logo


if VERSION != "v01":
    has_logo = header()
    if part == "part1":
        chip(0, "PART 1", 0.0, S[3], y=430)
        impact_word(0, "SMASH", imp[1], hold=1.2)
        poster(0, S[3], S[4], "31.10 & 1.11.2026", "SILAMBAM", ["FESTIVAL KESENIAN & KEBUDAYAAN", "MALAYSIA 2026"])
        caption(9, ["Mahaguru Sri S Arumugam", "avargalin maanavargal"], S[4] + 0.1, S[5], sub="students of Mahaguru Sri S Arumugam")
        i8 = P.idx(part, "v_215628", 0.6); i9 = P.idx(part, "v_213143", 0.0); i10 = P.idx(part, "v_215603", 26.5)
        chip(1, "BACKSTAGE", S[5] + 0.2, S[i9])
        caption(0, ["Thank you. Right after this", "we have the next performance."], S[i8] + 0.7, S[i9])
        caption(1, ["Vanakkam guru, vanakkam!"], S[i9], S[i10], sub="salute to the master")
        caption(2, ["Ready?"], S[i10], S[i10] + 0.7)
        marquee(0, "SILAMBAM", S[i10] + 0.7, 0.8)
        ib = P.idx(part, "v_215613", 6.5); isl = P.idx(part, "v_215613", 23.95); irp = P.idx(part, "v_225624", 28.3)
        chip(2, "STICK DEMO", S[i10] + 1.6, S[ib] - 0.1)
        chip(3, "STUNT", S[ib] + 0.1, S[isl])
        impact_word(1, "UNBREAKABLE", imp[isl], hold=1.4, size=112)
        chip(4, "REPLAY", S[irp] + 0.05, S[irp + 1], color=GOLD)
        poster(1, S[-1], T, "COMING NEXT", "PART 2", ["SELF-DEFENCE · TEAMWORK · FINALE"], cta="WATCH PART 2 →")
    else:
        chip(0, "PART 2", 0.0, S[3], y=430)
        chip(1, "2ND ANGLE", 0.25, S[3], y=510, color=GOLD)
        impact_word(0, "AGAIN", imp[1], hold=1.2)
        caption(0, ["ungaludaiya aadharavu", "romba romba mukkiyam"], S[3] + 0.1, S[3] + 2.1, sub="your support is very important")
        caption(1, ["romba nandri!"], S[3] + 2.1, S[4], sub="thank you very much")
        caption(2, ["Let's go!"], S[4], S[4] + 1.0)
        marquee(0, "SELF-DEFENCE", S[5], 0.8)
        it = P.idx(part, "v_215617", 22.0); ic = P.idx(part, "v_215619", 9.0); ifn = P.idx(part, "v_225626", 0.5)
        chip(2, "SELF-DEFENCE", S[5] + 0.9, S[it] - 0.1)
        impact_word(1, "TAKEDOWN", imp[P.idx(part, "v_225545", 7.8)], hold=1.3, size=150)
        chip(3, "TEAMWORK", S[it] + 0.2, S[ic] - 0.1)
        chip(4, "THE CROWD", S[ic] + 0.2, S[ifn] - 0.1)
        chip(5, "FINALE", S[ifn] + 0.2, S[-1] - 0.1)
        poster(0, S[-1], T, "31.10 & 1.11.2026", "SILAMBAM", ["FESTIVAL KESENIAN & KEBUDAYAAN", "MALAYSIA 2026"], cta="TERIMA KASIH · THANK YOU")
elif part == "part1":
    chip(0, "PART 1", 0.0, S[3], y=300)
    impact_word(0, "SMASH", imp[1], hold=1.2)
    poster(0, S[3], S[4], "31.10 & 1.11.2026", "SILAMBAM", ["FESTIVAL KESENIAN & KEBUDAYAAN", "MALAYSIA 2026"])
    chip(1, "BACKSTAGE", S[4] + 0.2, S[7] + 4.0)
    caption(0, ["Thank you. Right after this", "we have the next performance."], S[7] + 0.7, S[8])
    caption(1, ["Vanakkam guru, vanakkam!"], S[8], S[9], sub="salute to the master")
    caption(2, ["Ready?"], S[9], S[9] + 0.7)
    marquee(0, "SILAMBAM", S[9] + 0.7, 0.9)
    chip(2, "STICK DEMO", S[9] + 1.7, S[24] - 0.1)
    chip(3, "STUNT", S[24] + 0.1, S[26])
    impact_word(1, "UNBREAKABLE", imp[26], hold=1.4, size=112)
    chip(4, "REPLAY", S[27] + 0.05, S[28], color=GOLD)
    poster(1, S[30], T, "COMING NEXT", "PART 2", ["SELF-DEFENCE · TEAMWORK · FINALE"], cta="WATCH PART 2 →")
else:
    chip(0, "PART 2", 0.0, S[3], y=300)
    chip(1, "2ND ANGLE", 0.25, S[3], y=380, color=GOLD)
    impact_word(0, "AGAIN", imp[1], hold=1.2)
    caption(0, ["ungaludaiya aadharavu", "romba romba mukkiyam"], S[3] + 0.1, S[3] + 2.1, sub="your support is very important")
    caption(1, ["romba nandri!"], S[3] + 2.1, S[4], sub="thank you very much")
    caption(2, ["Let's go!"], S[4], S[4] + 1.0)
    marquee(0, "SELF-DEFENCE", S[5], 0.9)
    chip(2, "SELF-DEFENCE", S[5] + 0.9, S[15] - 0.1)
    impact_word(1, "TAKEDOWN", imp[6], hold=1.3, size=150)
    chip(3, "TEAMWORK", S[15] + 0.2, S[16] - 0.1)
    chip(4, "THE CROWD", S[16] + 0.2, S[17] - 0.1)
    chip(5, "FINALE", S[17] + 0.2, S[19] - 0.1)
    poster(0, S[19], T, "31.10 & 1.11.2026", "SILAMBAM", ["FESTIVAL KESENIAN & KEBUDAYAAN", "MALAYSIA 2026"], cta="TERIMA KASIH · THANK YOU")

doc = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "IDB"; src: url("assets/fonts/InterDisplay-Black.otf"); font-weight: 900; }}
      @font-face {{ font-family: "IDBo"; src: url("assets/fonts/InterDisplay-Bold.otf"); font-weight: 700; }}
      @font-face {{ font-family: "ISB"; src: url("assets/fonts/Inter-SemiBold.otf"); font-weight: 600; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
      .clip {{ position: absolute; inset: 0; }}
      .vid {{ width: 1080px; height: 1920px; object-fit: cover; }}
      #gfx {{ z-index: 10; pointer-events: none; }}
      .chip {{ position: absolute; left: 540px; height: 64px; line-height: 64px; padding: 0 28px; border-radius: 8px; color: #fff;
        font-family: "IDB"; font-size: 34px; letter-spacing: 6px; white-space: nowrap; box-shadow: 0 10px 26px rgba(0,0,0,.35); }}
      .cap {{ position: absolute; left: 140px; width: 800px; top: {290 if VERSION == "v01" else 420}px; text-align: center; }}
      #hshade {{ position: absolute; left: 0; top: 0; width: 1080px; height: 470px; background: linear-gradient(180deg, rgba(8,6,10,.62), rgba(8,6,10,.30) 55%, rgba(8,6,10,0)); }}
      #hdr {{ position: absolute; left: 540px; top: 205px; display: flex; align-items: center; gap: 18px; }}
      #hdr .hlogo {{ height: 150px; width: auto; filter: drop-shadow(0 4px 10px rgba(0,0,0,.55)); }}
      #hdr .htext {{ text-align: center; }}
      .hl1, .hl2 {{ background: linear-gradient(180deg, #fff4bf 0%, #f6cf55 34%, #c8921a 62%, #ffe28c 84%, #b27c10 100%);
        -webkit-background-clip: text; background-clip: text; color: transparent; filter: drop-shadow(0 3px 5px rgba(0,0,0,.7)); }}
      .hl1 {{ font-family: "IDB"; font-size: 40px; letter-spacing: 2px; line-height: 1.1; white-space: nowrap; }}
      .hl2 {{ font-family: "IDB"; font-size: 28px; letter-spacing: 12px; line-height: 1.3; display: flex; align-items: center; justify-content: center; gap: 14px; }}
      .hl2 i {{ display: block; width: 70px; height: 3px; background: linear-gradient(90deg, #b27c10, #ffe28c); }}
      .cap .t {{ display: inline; font-family: "IDBo"; font-size: 54px; line-height: 1.32; color: #fff; padding: 6px 18px; border-radius: 10px;
        background: rgba(14,11,16,.82); -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
      .cap .sub {{ display: inline-block; margin-top: 12px; font-family: "ISB"; font-size: 32px; color: {GOLD}; padding: 4px 14px; border-radius: 8px;
        background: rgba(14,11,16,.7); }}
      .kw {{ position: absolute; left: 540px; top: 640px; font-family: "IDB"; color: #fff; letter-spacing: -3px; line-height: 1; white-space: nowrap;
        text-shadow: 0 0 0 {RED}, 6px 6px 0 {RED}, 0 18px 40px rgba(0,0,0,.55); }}
      .kw .dot {{ color: {GOLD}; }}
      .flash {{ position: absolute; inset: 0; background: #fff; }}
      .mq {{ position: absolute; inset: 0; background: rgba(14,11,16,.35); }}
      .mrow {{ position: absolute; left: 0; white-space: nowrap; font-family: "IDB"; font-size: 210px; letter-spacing: -4px; line-height: 1; opacity: .92; }}
      .poster {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; padding-top: 520px; }}
      .poster.dark {{ background: linear-gradient(180deg, rgba(14,11,16,.15), rgba(14,11,16,.55) 40%, rgba(14,11,16,.55) 70%, rgba(14,11,16,.2)); }}
      .pbar {{ width: 700px; transform-origin: 50% 50%; position: relative; text-align: center; }}
      .pbar i {{ display: block; height: 9px; }} .pbar i:nth-child(1) {{ background: {RED}; }} .pbar i:nth-child(2) {{ background: {GOLD}; }}
      .pbar span {{ display: block; background: #fff; color: {INK}; font-family: "IDB"; font-size: 40px; letter-spacing: 4px; line-height: 70px; }}
      .ph {{ overflow: hidden; margin-top: 26px; }}
      .phi {{ font-family: "IDB"; font-size: 178px; color: #fff; letter-spacing: -5px; line-height: 1.02; text-shadow: 0 14px 40px rgba(0,0,0,.45); }}
      .pl {{ overflow: hidden; margin-top: 6px; }}
      .pli {{ font-family: "IDBo"; font-size: 44px; color: #fff; letter-spacing: 1px; text-align: center; text-shadow: 0 6px 20px rgba(0,0,0,.6); }}
      .pcta {{ margin-top: 40px; background: {RED}; color: #fff; font-family: "IDB"; font-size: 40px; letter-spacing: 3px; padding: 18px 34px; border-radius: 12px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{T}">
      <video id="plate" class="clip vid" src="assets/v/{part}_plate{SUF}.mp4" muted playsinline data-start="0" data-duration="{T}" data-track-index="1" style="z-index:1"></video>
      <audio id="mix" src="assets/{part}_mix{SUF}.wav" data-start="0" data-duration="{T}" data-track-index="2" data-volume="1"></audio>
      <div id="gfx" class="clip" data-start="0" data-duration="{T}" data-track-index="3">
        {(chr(10) + "        ").join(els)}
      </div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      {(chr(10) + "      ").join(init)}
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(js)}
      tl.set({{}}, {{}}, {T});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
OUTDIR = "edit" if part == "part1" else "edit_p2"            # one HyperFrames project per part (edit_p2/assets -> ../edit/assets)
open(f"{OUTDIR}/index.html", "w").write(doc)
print("built", part, T, len(js), "timeline entries")
