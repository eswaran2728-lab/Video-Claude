# v02 Cyber Roadshow 2026 recap (writes edit/index.html; v01 = build.py). 45.0 s, 1080x1920, 30 fps.
# Creator's notes on v01: no GTR content; use all the images and videos; a visually stunning recap.
# Sections: hook (photo punches + title) / set-up (b048) / the booth (IMG_6425 + landing photo cards) / the crowd (dc95 +
# IMG_6461) / the stage (IMG_6421 in sync with its own song, three lyric tip cards, the deepfake talk) / the people
# (two-beat photo montage) / finale (all 19 photos + a stage frame as a mosaic wall, AIRASIA AVSEC sign-off).
# Music beats: 0 + n*0.4878 s (House Fest, 123 BPM); song section beats: 15.106 + n*0.491 s.
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
C = json.load(open("content.json")); TOTAL = 45.0
MB = lambda n: round(n * 60 / 123.0, 3)            # music beat n (out time)
SO = 14.826                                         # out = song time + SO
at = lambda t: round(t, 3)
PW, PH = 3840, 2160
L, INIT, JS = [], [], []                            # layers, frame-0 sets, timeline
I, A = INIT.append, JS.append
z = [10]
def nz(): z[0] += 1; return z[0]

def photo(pid, f, a, b, c0, c1, punch=True, extra=""):
    L.append(f'''      <div id="{pid}" class="clip ph" data-start="{at(a)}" data-duration="{at(b - a)}" data-track-index="2" style="z-index:{nz()}"><div class="push" id="{pid}push"><div class="pan" id="{pid}pan">
        <img src="assets/p/{f}.jpg" alt="{f}" />{extra}</div></div></div>''')
    I(f'gsap.set("#{pid}pan",{{x:{540 - c0 * PW:.0f}}}); gsap.set("#{pid}push",{{transformOrigin:"540px 960px"}});')
    A(f'tl.to("#{pid}pan",{{x:{540 - c1 * PW:.0f},duration:{at(b - a)},ease:"none"}},{at(a)});')
    if punch: A(f'tl.fromTo("#{pid}push",{{scale:1.09}},{{scale:1.0,duration:0.32,ease:"power3.out"}},{at(a)}); tl.to("#{pid}push",{{scale:1.035,duration:{at(b - a - 0.32)},ease:"none"}},{at(a + 0.32)});')
    else: A(f'tl.fromTo("#{pid}push",{{scale:1.0}},{{scale:1.05,duration:{at(b - a)},ease:"none"}},{at(a)});')

def video(vid, src, a, b, extra_cls="vid"):
    L.append(f'      <video id="{vid}" class="clip {extra_cls}" src="{src}" muted playsinline data-start="{at(a)}" data-duration="{at(b - a)}" data-track-index="1" style="z-index:{nz()}"></video>')

def label(n, text, a, b):
    L.append(f'      <div id="lb{n}" class="clip lbl" data-start="{at(a)}" data-duration="{at(b - a)}" data-track-index="7" style="z-index:60"><div class="pill" id="lbp{n}"><b>{n:02d}</b>{text}</div></div>')
    I(f'gsap.set("#lbp{n}",{{x:-60,opacity:0}});')
    A(f'tl.to("#lbp{n}",{{x:0,opacity:1,duration:0.3,ease:"power3.out"}},{at(a)}); tl.to("#lbp{n}",{{x:-40,opacity:0,duration:0.22,ease:"power2.in"}},{at(b - 0.22)});')

# ---------------- A. hook: four photo punches on two-beat steps + title ----------------
HOOK = [("IMG_6426", .32, .38), ("IMG_6436", .28, .32), ("2ee1beb9", .52, .56), ("IMG_6427", .46, .52)]
for k, (f, c0, c1) in enumerate(HOOK): photo(f"h{k}", f, MB(2 * k), MB(2 * k + 2), c0, c1)
t = C["title"]
L.append(f'''      <div id="title" class="clip" data-start="0" data-duration="{MB(8)}" data-track-index="5" style="z-index:50">
        <div class="scrim"></div>
        <div class="tbox"><div class="chip" id="tchip">{t["chip"]}</div>{"".join(f'<div class="tm"><div class="tl" id="tl{k}">{w}</div></div>' for k, w in enumerate(t["lines"]))}<div class="tsub" id="tsub">{t["sub"]}</div></div>
      </div>''')
I('gsap.set("#title .tl",{yPercent:110}); gsap.set("#tchip,#tsub",{opacity:0,y:16});')
A('tl.to("#tchip",{opacity:1,y:0,duration:0.25,ease:"power2.out"},0.03);')
for k in range(3): A(f'tl.to("#tl{k}",{{yPercent:0,duration:0.35,ease:"power4.out"}},{MB(k)});')
A(f'tl.to("#tsub",{{opacity:1,y:0,duration:0.25,ease:"power2.out"}},{MB(3)});')
A(f'tl.to("#title .tbox",{{y:-40,opacity:0,duration:0.22,ease:"power2.in"}},{MB(8) - 0.24});')

# ---------------- B. set-up: b048 phone clip framed ----------------
def phoneclip(pid, name, a, b):
    video(f"{pid}bg", f"assets/v2/{name}_bg.mp4", a, b)
    L.append(f'      <video id="{pid}card" class="clip phonev" src="assets/v2/{name}_card.mp4" muted playsinline data-start="{at(a)}" data-duration="{at(b - a)}" data-track-index="3" style="z-index:{nz()}"></video>')
    I(f'gsap.set("#{pid}card",{{y:120,scale:0.9,opacity:0}});')
    A(f'tl.to("#{pid}card",{{y:0,scale:1,opacity:1,duration:0.42,ease:"power3.out"}},{at(a)});')
phoneclip("pb", "b048", MB(8), MB(16))
label(1, "SET-UP", MB(8) + 0.1, MB(15))

# ---------------- C. the booth: IMG_6425 then photo cards landing on the beat ----------------
video("vbooth", "assets/v2/v_booth.mp4", MB(16), MB(28))
L.append(f'      <div id="bdim" class="clip" data-start="{MB(16)}" data-duration="{at(MB(28) - MB(16))}" data-track-index="3" style="z-index:{nz()}"><div class="dimfill" id="bdimf"></div></div>')
I('gsap.set("#bdimf",{opacity:0});'); A(f'tl.to("#bdimf",{{opacity:0.62,duration:0.4}},{MB(20) - 0.2});')
CARDS = [("912ed0e8", 50, -5, -30, 0), ("38af901c", 40, 4, 40, -20), ("ACAE9274", 35, -3, -20, 30), ("IMG_6433", 33, 5, 30, 10)]
for k, (f, fx, rot, dx, dy) in enumerate(CARDS):
    a = MB(20 + 2 * k)
    L.append(f'      <div id="cd{k}" class="clip" data-start="{at(a)}" data-duration="{at(MB(28) - a)}" data-track-index="4" style="z-index:{nz()}"><div class="pcard" id="pc{k}"><img src="assets/p/{f}.jpg" alt="{f}" style="object-position:{fx}% 50%" /></div></div>')
    I(f'gsap.set("#pc{k}",{{rotation:{rot + (8 if rot > 0 else -8)},x:{dx},y:{dy - 80},scale:1.3,opacity:0}});')
    A(f'tl.to("#pc{k}",{{rotation:{rot},y:{dy},scale:1,opacity:1,duration:0.34,ease:"back.out(1.4)"}},{at(a)});')
A(f'tl.to("#pc3",{{scale:1.04,duration:{at(MB(28) - MB(26))},ease:"none"}},{MB(26) + 0.34});')
label(2, "THE BOOTH", MB(16) + 0.1, MB(19.5))

# ---------------- D. the crowd: dc95 phone clip + IMG_6461 ----------------
phoneclip("pc95", "dc95", MB(28), MB(32))
photo("crowd", "IMG_6461", MB(32), MB(36) + 0.4, .33, .40, punch=True)
label(3, "THE CROWD", MB(28) + 0.1, MB(31.5))

# ---------------- E. the stage: IMG_6421 in sync with its song; slide-up entrance on the music change ----------------
S = lambda s: round(s + SO, 3)
for vid, a, b in [("v_walk", 2.733, 4.205), ("v_stage1", 4.205, 9.603), ("v_stage2", 9.603, 12.547), ("v_stage3", 15.0, 16.472)]:
    video(f"s_{vid}", f"assets/v/{vid}.mp4", S(a), S(b))
I(f'gsap.set("#s_v_walk",{{y:1920}});'); A(f'tl.to("#s_v_walk",{{y:0,duration:0.38,ease:"power3.inOut"}},{S(2.733) - 0.38});')
L[-4] = L[-4].replace(f'data-start="{S(2.733)}" data-duration="{at(S(4.205) - S(2.733))}"', f'data-start="{at(S(2.733) - 0.38)}" data-duration="{at(S(4.205) - S(2.733) + 0.38)}"')
label(4, "THE STAGE", S(2.733) + 0.05, S(3.6))
for k, (f, a, b) in enumerate([("IMG_6429", 12.547, 13.773), ("IMG_6430", 13.773, 15.0)]):
    L.append(f'''      <div id="tk{k}" class="clip ph" data-start="{S(a)}" data-duration="{at(b - a)}" data-track-index="2" style="z-index:{nz()}">
        <img class="bgblur" src="assets/p/{f}.jpg" alt="" /><div class="card" id="tkc{k}"><img id="tki{k}" src="assets/p/{f}.jpg" alt="{f} deepfake talk" /></div></div>''')
    I(f'gsap.set("#tkc{k}",{{scale:{0.92 if k == 0 else 1},opacity:{0 if k == 0 else 1}}}); gsap.set("#tki{k}",{{transformOrigin:"35% 45%"}});')
    if k == 0: A(f'tl.to("#tkc0",{{scale:1,opacity:1,duration:0.32,ease:"power3.out"}},{S(a)});')
    A(f'tl.fromTo("#tki{k}",{{scale:{1.0 + 0.06 * k}}},{{scale:{1.06 + 0.06 * k},duration:{at(b - a)},ease:"none"}},{S(a)});')
TIPS = [(3.715, 6.62), (10.093, 12.42), (15.0, 18.4)]
for k, (tip, (a, b)) in enumerate(zip(C["tips"], TIPS)):
    a, b = S(a), S(b)
    L.append(f'''      <div id="tip{k}" class="clip tip" data-start="{at(a)}" data-duration="{at(b - a + 0.05)}" data-track-index="6" style="z-index:70">
        <div class="tcard" id="tc{k}"><div class="tlab"><i>{k + 1:02d}</i>{tip["label"]}</div><div class="ttxt">{"".join(f'<span class="w">{w}</span> ' for w in tip["text"].split())}</div></div></div>''')
    I(f'gsap.set("#tc{k}",{{opacity:0,y:40,scale:0.94}}); gsap.set("#tc{k} .w",{{opacity:0,y:18}});')
    A(f'tl.to("#tc{k}",{{opacity:1,y:0,scale:1,duration:0.38,ease:"back.out(1.6)"}},{at(a)}); tl.to("#tc{k} .w",{{opacity:1,y:0,duration:0.25,stagger:0.07,ease:"power2.out"}},{at(a + 0.12)}); tl.to("#tc{k}",{{opacity:0,y:-24,duration:0.22,ease:"power2.in"}},{at(b - 0.2)});')

# ---------------- F. the people: two-beat montage on the song ----------------
SB = lambda n: round(15.106 + n * 0.491, 3)        # song beat in out time (n=33 -> s 16.483, where v_stage3 ends)
PEOPLE = [("IMG_6437", .36, .39), ("IMG_6438", .35, .38), ("IMG_6439", .35, .38), ("IMG_6440", .40, .46),
          ("IMG_6435", .52, .56), ("IMG_6419", .48, .52), ("IMG_6420", .48, .52), ("IMG_6423", .42, .46)]
for k, (f, c0, c1) in enumerate(PEOPLE):
    a = SB(33 + 2 * k); b = SB(35 + 2 * k) if k < len(PEOPLE) - 1 else S(24.37)
    extra = ""
    if f == "IMG_6439":
        x0, y0, x1, y1 = 0.425 * PW, 0.43 * PH, 0.485 * PW, 0.68 * PH
        extra = f'<div class="ring" id="ring" style="left:{x0:.0f}px;top:{y0:.0f}px;width:{x1 - x0:.0f}px;height:{y1 - y0:.0f}px"></div>'
        I('gsap.set("#ring",{opacity:0,scale:1.25,transformOrigin:"50% 50%"});')
        A(f'tl.to("#ring",{{opacity:1,scale:1,duration:0.26,ease:"back.out(1.8)"}},{at(a + 0.1)});')
    photo(f"pp{k}", f, a, b, c0, c1, extra=extra)
label(5, "THE PEOPLE", SB(37) + 0.1, SB(41))

# ---------------- G. finale: mosaic wall of every photo, then the AVSEC sign-off ----------------
F0 = S(24.37)
TILES = ["IMG_6426", "IMG_6427", "IMG_6461", "IMG_6436", "2ee1beb9", "38af901c", "912ed0e8", "ACAE9274", "IMG_6433", "stage_frame",
         "IMG_6429", "IMG_6430", "IMG_6437", "IMG_6438", "IMG_6439", "IMG_6440", "IMG_6435", "IMG_6419", "IMG_6420", "IMG_6423"]
tiles = "".join(f'<div class="tile" id="tile{k}" style="left:{(k % 4) * 270}px;top:{(k // 4) * 384}px"><img src="assets/tiles/{f}.jpg" alt="" /></div>' for k, f in enumerate(TILES))
c = C["close"]
L.append(f'''      <div id="fin" class="clip" data-start="{at(F0 - 0.38)}" data-duration="{at(TOTAL - F0 + 0.38)}" data-track-index="8" style="z-index:80">
        <div class="wallwrap" id="wallwrap"><div class="wall" id="wall">{tiles}</div></div>
        <div class="dim2" id="dim2"></div>
        <div class="lock" id="lock"><div class="org">{c["org"]}</div><div class="rule" id="rule"></div><div class="tag">{c["tagline"]}</div><div class="ev">{c["event"]}</div></div>
        <div class="black" id="black"></div>
      </div>''')
I('gsap.set("#wallwrap",{y:1920}); gsap.set("#wall",{scale:1.55,transformOrigin:"540px 960px"}); gsap.set("#dim2,#black",{opacity:0}); gsap.set("#lock",{opacity:0,y:26}); gsap.set("#rule",{scaleX:0});')
I('gsap.set("#wall .tile",{opacity:0,scale:0.6});')
A(f'tl.to("#wallwrap",{{y:0,duration:0.38,ease:"power3.inOut"}},{at(F0 - 0.38)});')
order = sorted(range(20), key=lambda k: abs(k % 4 - 1.5) + abs(k // 4 - 2))
for j, k in enumerate(order): A(f'tl.to("#tile{k}",{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.5)"}},{at(F0 - 0.3 + 0.035 * j)});')
A(f'tl.to("#wall",{{scale:1.0,duration:2.0,ease:"power2.inOut"}},{at(F0)});')
A(f'tl.to("#dim2",{{opacity:1,duration:0.4}},{at(F0 + 1.9)}); tl.to("#lock",{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{at(F0 + 2.05)}); tl.to("#rule",{{scaleX:1,duration:0.35,ease:"power3.out"}},{at(F0 + 2.15)});')
A(f'tl.to("#wall",{{scale:1.04,duration:{at(TOTAL - F0 - 2.0)},ease:"none"}},{at(F0 + 2.0)});')
A(f'tl.to("#black",{{opacity:1,duration:0.4,ease:"power1.in"}},{at(TOTAL - 0.4)});')

# ---------------- sound cues ----------------
SFX = [(MB(20 + 2 * k), "thock.wav", 0.28) for k in range(4)] + [(S(3.715), "ui-pop.wav", 0.2), (S(10.093), "ui-pop.wav", 0.2), (S(15.0), "ui-pop.wav", 0.2),
       (S(2.733) - 0.38, "zoom-swish.wav", 0.24), (F0 - 0.38, "zoom-swish.wav", 0.24)]
sfx = "\n".join(f'      <audio id="sx{k}" class="clip" src="assets/sfx/{f}" data-start="{at(t)}" data-duration="0.8" data-volume="{v}"></audio>' for k, (t, f, v) in enumerate(SFX))

html = open("index_v02.tpl.html").read()
for k, v in {"%%TOTAL%%": str(TOTAL), "%%LAYERS%%": "\n".join(L), "%%SFX%%": sfx, "%%INIT%%": "\n".join("      " + x for x in INIT), "%%JS%%": "\n".join("      " + x for x in JS)}.items():
    html = html.replace(k, v)
open("edit/index.html", "w").write(html)
json.dump({"duration": TOTAL, "music_beats": "n*0.4878 s", "song_out_offset": SO,
           "hook": [[f, MB(2 * k), MB(2 * k + 2)] for k, (f, *_r) in enumerate(HOOK)], "setup_b048": [MB(8), MB(16), "b048.mp4 9.0-12.95 s"],
           "booth": [MB(16), MB(28), "IMG_6425.MOV 0-3.97 s slowed x1.476; cards " + ", ".join(f[0] for f in CARDS)],
           "crowd": [[MB(28), MB(32), "dc95.mp4 18.0-20.0 s"], [MB(32), MB(36) + 0.4, "IMG_6461"]],
           "stage": [[S(a), S(b), f"IMG_6421.MOV {a}-{b} s"] for a, b in [(2.733, 4.205), (4.205, 9.603), (9.603, 12.547), (15.0, 16.472)]] +
                    [[S(12.547), S(13.773), "IMG_6429"], [S(13.773), S(15.0), "IMG_6430"]],
           "tips": [[S(a), S(b)] for a, b in TIPS],
           "people": [[f, SB(33 + 2 * k), SB(35 + 2 * k) if k < 7 else S(24.37)] for k, (f, *_r) in enumerate(PEOPLE)],
           "finale": [F0 - 0.38, TOTAL, "mosaic of all 19 photos + IMG_6421 stage frame; AIRASIA AVSEC sign-off"],
           "sfx": [dict(t=at(t), file=f, gain=v) for t, f, v in SFX]}, open("edit/timing_map_v02.json", "w"), indent=1)
chk = subprocess.run(["node", "-e", "const s=require('fs').readFileSync('edit/index.html','utf8');new Function(s.split('<script>')[1].split('</script>')[0])"], capture_output=True, text=True)
if chk.returncode: raise SystemExit("timeline JS does not parse:\n" + chk.stderr[-600:])
print("built v02", TOTAL, len(JS), "timeline entries")
