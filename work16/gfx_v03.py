# v03 cinematic layer (on top of v02's graphics; build16.py adds it when VERSION >= v03):
#  - lights-off dip: the lit opening card dips to near-black and the unlit frame fades up (hides the hard cut)
#  - warm light-leak sweep on the jump to "how to use it?"
#  - anamorphic flare streak across the first lamp on the reveal frame
#  - letterbox bars close in for the end card
#  - titles: wider tracking, soft focus-pull in on the hook title
import plan16 as P

def build(fr, R, END0):
    css, html, js, cues = [], [], [], []
    add = js.append
    css.append('''
      #dip { background: #050403; }
      #leak { position: absolute; left: -900px; top: -200px; width: 1500px; height: 2400px; mix-blend-mode: screen;
        background: linear-gradient(100deg, rgba(255,150,60,0) 20%, rgba(255,170,80,.55) 42%, rgba(255,226,170,.75) 50%, rgba(255,170,80,.5) 58%, rgba(255,150,60,0) 80%);
        transform: rotate(8deg); }
      #flare { position: absolute; left: -330px; top: 798px; width: 1100px; height: 46px; mix-blend-mode: screen;
        background: radial-gradient(ellipse 50% 50% at 50% 50%, rgba(255,236,190,.95) 0%, rgba(255,190,110,.55) 18%, rgba(255,160,80,.18) 45%, rgba(255,150,60,0) 72%); }
      #flare2 { position: absolute; left: -60px; top: 816px; width: 560px; height: 10px; mix-blend-mode: screen;
        background: linear-gradient(90deg, rgba(255,210,150,0), rgba(255,240,210,.95) 50%, rgba(255,210,150,0)); }
      .lbar { position: absolute; left: 0; width: 1080px; height: 170px; background: #050403; }
      #lbT { top: 0; } #lbB { bottom: 0; }
      #hk1 { letter-spacing: 4px !important; }
      #hk2 { letter-spacing: 12px !important; }
      #e1 { letter-spacing: 10px !important; font-size: 84px !important; }
''')
    html.append('<div id="dip" class="clip"></div><div id="leak"></div><div id="flare"></div><div id="flare2"></div>'
                '<div id="lbT" class="lbar"></div><div id="lbB" class="lbar"></div>')
    S0 = fr(P.S["story"]["o0"]); H0 = fr(P.S["howto"]["o0"])
    add('gsap.set("#dip",{opacity:0}); gsap.set("#leak",{opacity:0,x:0}); gsap.set("#flare",{opacity:0,scaleX:0.2}); gsap.set("#flare2",{opacity:0,scaleX:0.1});')
    add('gsap.set("#lbT",{yPercent:-100}); gsap.set("#lbB",{yPercent:100}); gsap.set("#hk1",{filter:"blur(3px)",opacity:0.75});')
    # hook title focus-pull (visible from frame 0)
    add('tl.to("#hk1",{filter:"blur(0px)",opacity:1,duration:0.7,ease:"power2.out"},0);')
    # lights-off dip around the first cut
    add(f'tl.to("#dip",{{opacity:0.92,duration:0.16,ease:"power1.in"}},{S0 - 0.16:.4f});')
    add(f'tl.to("#dip",{{opacity:0,duration:0.55,ease:"power2.out"}},{S0 + 0.02:.4f});')
    # light leak across the jump to the lamp question
    add(f'tl.to("#leak",{{opacity:1,duration:0.18,ease:"sine.out"}},{H0 - 0.14:.4f});')
    add(f'tl.to("#leak",{{x:1400,duration:0.7,ease:"power1.inOut"}},{H0 - 0.14:.4f});')
    add(f'tl.to("#leak",{{opacity:0,duration:0.3,ease:"sine.in"}},{H0 + 0.26:.4f});')
    # anamorphic flare on the lamp as it is revealed
    add(f'tl.to("#flare",{{opacity:1,scaleX:1,duration:0.25,ease:"power2.out"}},{R:.4f});')
    add(f'tl.to("#flare2",{{opacity:1,scaleX:1,duration:0.2,ease:"power2.out"}},{R:.4f});')
    add(f'tl.to("#flare",{{opacity:0.35,scaleX:1.25,duration:1.0,ease:"sine.out"}},{R + 0.25:.4f});')
    add(f'tl.to("#flare2",{{opacity:0,scaleX:1.4,duration:0.8,ease:"sine.out"}},{R + 0.2:.4f});')
    add(f'tl.to("#flare",{{opacity:0,duration:0.5,ease:"sine.in"}},{fr(P.S["glow"]["o1"]) - 0.45:.4f});')
    # letterbox bars for the end card
    add(f'tl.to("#lbT",{{yPercent:0,duration:0.6,ease:"power3.inOut"}},{END0:.4f});')
    add(f'tl.to("#lbB",{{yPercent:0,duration:0.6,ease:"power3.inOut"}},{END0:.4f});')
    return "".join(css), "\n        ".join(html), js, cues
