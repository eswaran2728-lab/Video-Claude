# v02 motion graphics, each tied to what he says and to something real on the frame:
#  1. "we call it 3D wall frame art" → tracked callouts on the real layers: GOLD CUT-OUT (mountain peak) and
#     SHIVA & PARVATI (the crescent on Shiva's hair) — track16.py "callouts".
#  2. "a customer messaged me" → message card; "key holder" types in when he says it; its key flies down to the hooks.
#  3. "see this lamp" → pulsing rings tracked onto both lamps (track_lamps16.py).
#  4. "hold the lamp, turn it here… it turns on" → hold + turn diagram, arrow turning; its bulb lights on the reveal frame.
#  5. End card → recap chips (3D WALL ART · 5 KEY HOOKS · LAMPS) before the name.
# build16.py imports this when VERSION >= v02. Returns css, html, js lines, sound cues.
import json, math
import plan16 as P

def build(fr, R, END0):
    FPS = P.FPS; css, html, js, cues = [], [], [], []
    add = js.append

    def follow(sel, frames, dx=0, dy=0, idx=0):
        """Per-frame position keys from a tracking file (anchor idx), as zero-ease tweens."""
        ks = sorted(int(k) for k in frames)
        x0, y0 = frames[str(ks[0])][idx]
        add(f'gsap.set("{sel}",{{x:{x0 + dx:.1f},y:{y0 + dy:.1f}}});')
        for ka, kb in zip(ks, ks[1:]):
            xb, yb = frames[str(kb)][idx]
            add(f'tl.to("{sel}",{{x:{xb + dx:.1f},y:{yb + dy:.1f},duration:{1 / FPS:.5f},ease:"none"}},{ka / FPS:.4f});')

    css.append('''
      .co { position: absolute; left: 0; top: 0; width: 0; height: 0; }
      .co .dot { position: absolute; left: -13px; top: -13px; width: 26px; height: 26px; border-radius: 50%;
        border: 4px solid var(--gold); background: rgba(233,193,107,.35); box-shadow: 0 0 14px rgba(233,193,107,.8); }
      .co .ln { position: absolute; left: 0; top: -2px; height: 4px; border-radius: 2px; background: var(--gold); transform-origin: 0 50%; }
      .co .lab { position: absolute; transform: translate(-50%, -50%); white-space: nowrap; padding: 10px 22px; border-radius: 14px;
        background: var(--ink); border: 2px solid var(--gold); font-family: "IDB"; font-size: 33px; letter-spacing: 2px; color: var(--cream); }
      #msg { position: absolute; left: 150px; top: 290px; width: 780px; height: 150px; border-radius: 30px; display: flex; align-items: center; gap: 24px;
        padding: 0 30px; background: rgba(20,15,11,.86); border: 2px solid rgba(233,193,107,.75); box-shadow: 0 18px 50px rgba(0,0,0,.55); }
      #msg .av { flex: none; width: 86px; height: 86px; border-radius: 50%; background: var(--gold); display: flex; align-items: center; justify-content: center; }
      #msg .av svg { width: 50px; height: 50px; fill: #1a120b; }
      #msg .m1 { font-family: "ISB"; font-size: 27px; letter-spacing: 3px; color: var(--gold); }
      #msg .m2 { position: relative; height: 58px; margin-top: 6px; font-family: "IDBo"; font-size: 42px; color: var(--cream); white-space: nowrap; }
      #msg .m2 b { font-family: "IDB"; color: var(--gold); }
      #dots { position: absolute; left: 0; top: 18px; display: flex; gap: 10px; }
      #dots i { display: block; width: 16px; height: 16px; border-radius: 50%; background: var(--cream); }
      #req { position: absolute; left: 0; top: 0; }
      #mkey { width: 64px; height: 64px; }
      #mkey svg { display: block; width: 64px; height: 64px; fill: none; stroke: var(--gold); stroke-width: 3.4; stroke-linecap: round; stroke-linejoin: round; }
      #flykey { width: 88px; height: 88px; border-radius: 50%; background: var(--gold); display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 0 4px rgba(26,18,11,.85), 0 0 26px 6px rgba(255,205,120,.75); }
      #flykey svg { display: block; width: 58px; height: 58px; fill: none; stroke: #1a120b; stroke-width: 4.5; stroke-linecap: round; stroke-linejoin: round; }
      #mkey { position: absolute; left: 470px; top: -4px; }
      #flykey { position: absolute; left: 0; top: 0; }
      .lr { position: absolute; left: 0; top: 0; width: 0; height: 0; }
      .lr i { position: absolute; left: -46px; top: -46px; width: 92px; height: 92px; border-radius: 50%; border: 5px solid var(--gold);
        box-shadow: 0 0 18px rgba(233,193,107,.8), inset 0 0 12px rgba(233,193,107,.5); }
      .lr b { position: absolute; left: -46px; top: -46px; width: 92px; height: 92px; border-radius: 50%; border: 3px solid var(--gold); }
      #ht { position: absolute; left: 200px; top: 290px; width: 680px; height: 176px; border-radius: 30px; display: flex; align-items: center; gap: 34px;
        padding: 0 32px; background: rgba(20,15,11,.86); border: 2px solid rgba(233,193,107,.75); box-shadow: 0 18px 50px rgba(0,0,0,.55); }
      #ht .icon { position: relative; flex: none; width: 128px; height: 128px; }
      #ht .icon svg { position: absolute; inset: 0; width: 128px; height: 128px; overflow: visible; }

      #ht .h1 { font-family: "IDB"; font-size: 46px; color: var(--cream); letter-spacing: 1px; }
      #ht .h2 { position: relative; height: 44px; margin-top: 6px; font-family: "IDB"; font-size: 34px; letter-spacing: 3px; white-space: nowrap; }
      #h2a { position: absolute; left: 0; top: 0; color: rgba(255,244,226,.6); }
      #h2b { position: absolute; left: 0; top: 0; color: var(--gold); text-shadow: 0 0 16px rgba(255,200,110,.9); }
      #recap { position: absolute; left: 0; width: 1080px; top: 600px; display: flex; justify-content: center; gap: 14px; }
      #recap .chip { height: 64px; font-size: 28px; padding: 0 20px 0 14px; }
      #recap .ic { width: 34px; height: 34px; }
''')
    KEY = '<path d="M15 32a9 9 0 1 1 6.4-15.4L52 46M44 38l6-6M38 32l5-5"/><circle cx="15" cy="23" r="3"/>'
    LAYERS = '<svg viewBox="0 0 40 40" class="ic"><path d="M20 6 35 13 20 20 5 13z"/><path d="M5 20l15 7 15-7"/><path d="M5 27l15 7 15-7"/></svg>'
    KEYI = '<svg viewBox="0 0 40 40" class="ic"><circle cx="13" cy="20" r="7"/><path d="M20 20h16M30 20v6M35 20v4"/></svg>'
    BULB = '<svg viewBox="0 0 40 40" class="ic"><path d="M20 5a11 11 0 0 0-6 20v4h12v-4A11 11 0 0 0 20 5z"/><path d="M15 33h10M16 37h8"/></svg>'

    # 1 — tracked layer callouts
    tr = json.load(open("edit/track_callouts.json"))
    CO = [("coA", "GOLD CUT-OUT", 175, -175, 0, 5.05), ("coB", "SHIVA &amp; PARVATI", -110, -190, 1, 5.45)]
    for cid, text, dx, dy, idx, t_in in CO:
        L = math.hypot(dx, dy); ang = math.degrees(math.atan2(dy, dx))
        html.append(f'<div id="{cid}" class="co"><div class="ln" style="width:{L:.0f}px;transform:rotate({ang:.1f}deg)"></div>'
                    f'<div class="dot"></div><div class="lab" style="left:{dx}px;top:{dy}px">{text}</div></div>')
        add(f'gsap.set("#{cid} .dot",{{scale:0}}); gsap.set("#{cid} .ln",{{scaleX:0}}); gsap.set("#{cid} .lab",{{opacity:0,scale:0.8}});')
        follow(f"#{cid}", tr["frames"], idx=idx)
        add(f'tl.to("#{cid} .dot",{{scale:1,duration:0.22,ease:"back.out(2.4)"}},{t_in});')
        add(f'tl.to("#{cid} .ln",{{scaleX:1,duration:0.3,ease:"power3.out"}},{t_in + 0.12:.3f});')
        add(f'tl.to("#{cid} .lab",{{opacity:1,scale:1,duration:0.26,ease:"back.out(1.8)"}},{t_in + 0.3:.3f});')
        add(f'tl.to("#{cid}",{{opacity:0,duration:0.18,ease:"power2.in"}},{fr(P.out_t("story", 11.30)) - 0.32:.3f});')
        cues.append((t_in, "tick.wav", -15, f"callout {text}"))

    # 2 — customer message card → "KEY HOLDER" → key flies to the hooks
    t_msg, t_kh = fr(P.out_t("story", 14.98)) + 0.07, fr(P.out_t("story", 18.80))
    t_fly = fr(P.out_t("story", 19.40))
    html.append('<div id="msg"><div class="av"><svg viewBox="0 0 40 40"><path d="M6 8h28a3 3 0 0 1 3 3v15a3 3 0 0 1-3 3H17l-8 7v-7H6a3 3 0 0 1-3-3V11a3 3 0 0 1 3-3z"/></svg></div>'
                '<div><div class="m1">NEW MESSAGE · CUSTOMER</div><div class="m2"><span id="dots"><i></i><i></i><i></i></span>'
                f'<span id="req">Request: <b>KEY HOLDER</b></span><div id="mkey"><svg viewBox="0 0 64 64">{KEY}</svg></div></div></div></div>'
                f'<div id="flykey"><svg viewBox="0 0 64 64">{KEY}</svg></div>')
    add('gsap.set("#msg",{opacity:0,y:-40,scale:0.96}); gsap.set("#req",{opacity:0,x:-10}); gsap.set("#mkey",{opacity:0,scale:0.5,rotation:-30}); gsap.set("#flykey",{opacity:0,x:748,y:338,scale:0.75});')
    add(f'tl.to("#msg",{{opacity:1,y:0,scale:1,duration:0.38,ease:"back.out(1.5)"}},{t_msg});')
    for j in range(3):                                         # typing dots bounce until he says "key holder"
        t = t_msg + 0.4
        while t < t_kh - 0.3:
            add(f'tl.to("#dots i:nth-child({j + 1})",{{y:-10,opacity:1,duration:0.18,ease:"sine.out"}},{t + j * 0.12:.3f});')
            add(f'tl.to("#dots i:nth-child({j + 1})",{{y:0,opacity:0.45,duration:0.18,ease:"sine.in"}},{t + j * 0.12 + 0.18:.3f});')
            t += 0.72
    add(f'tl.to("#dots",{{opacity:0,duration:0.12}},{t_kh - 0.05:.3f});')
    add(f'tl.to("#req",{{opacity:1,x:0,duration:0.25,ease:"power3.out"}},{t_kh});')
    add(f'tl.to("#mkey",{{opacity:1,scale:1,rotation:0,duration:0.35,ease:"back.out(2)"}},{t_kh + 0.12:.3f});')
    add(f'tl.set("#mkey",{{opacity:0}},{t_fly}); tl.set("#flykey",{{opacity:1}},{t_fly});')
    add(f'tl.to("#flykey",{{x:496,y:996,scale:1.25,rotation:360,duration:0.62,ease:"power2.inOut"}},{t_fly});')
    add(f'tl.to("#flykey",{{opacity:0,scale:0.6,duration:0.16,ease:"power1.in"}},{t_fly + 0.62:.3f});')
    add(f'tl.to("#msg",{{opacity:0,y:-30,duration:0.28,ease:"power2.in"}},{t_fly + 0.05:.3f});')
    cues += [(t_msg, "curated/ui-pop.wav", -11, "message card"), (t_kh, "curated/ui-click.wav", -11, "KEY HOLDER appears"),
             (t_fly + 0.62, "latch.wav", -14, "key lands on the hooks")]

    # 3 — rings tracked on both lamps
    lp = json.load(open("edit/lamp_rings.json"))
    for i in range(2):
        html.append(f'<div id="lr{i}" class="lr"><b></b><i></i></div>')
        add(f'gsap.set("#lr{i} i",{{scale:0,opacity:0}}); gsap.set("#lr{i} b",{{scale:1,opacity:0}});')
        follow(f"#lr{i}", lp["frames"], idx=i)
        t = lp["show"] + 0.1 * i
        add(f'tl.to("#lr{i} i",{{scale:1,opacity:1,duration:0.25,ease:"back.out(2.2)"}},{t:.3f});')
        for k in range(2):
            t0 = t + 0.15 + 0.6 * k
            add(f'tl.set("#lr{i} b",{{scale:1,opacity:0.9}},{t0:.3f}); tl.to("#lr{i} b",{{scale:1.9,opacity:0,duration:0.5,ease:"sine.out"}},{t0 + 0.001:.3f});')
        add(f'tl.to("#lr{i}",{{opacity:0,duration:0.14}},{lp["hide"]:.3f});')
    cues.append((lp["show"], "tick.wav", -13, "lamp rings"))

    # 4 — hold + turn diagram; the bulb lights on the real reveal frame
    t_ht = fr(P.S["reveal"]["o0"]) + 0.1
    html.append('<div id="ht"><div class="icon"><svg viewBox="0 0 128 128">'
                '<circle id="glowc" cx="64" cy="50" r="40" fill="rgba(255,205,120,.0)"/>'
                '<path d="M46 74h36v26a6 6 0 0 1-6 6H52a6 6 0 0 1-6-6z" fill="none" stroke="#fff4e2" stroke-width="5"/>'
                '<circle id="bulb" cx="64" cy="54" r="18" fill="#3a2f22" stroke="#fff4e2" stroke-width="5"/>'
                '<g id="rot"><path d="M64 14a50 50 0 0 1 47 33" fill="none" stroke="#e9c16b" stroke-width="7" stroke-linecap="round"/>'
                '<path d="M100 40l11 9 4-14" fill="none" stroke="#e9c16b" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>'
                '</svg></div><div><div class="h1">HOLD + TURN</div><div class="h2"><span id="h2a">TO SWITCH ON</span><span id="h2b">LAMP ON</span></div></div></div>')
    add('gsap.set("#ht",{opacity:0,y:-40,scale:0.96}); gsap.set("#h2b",{opacity:0,y:10}); gsap.set("#rot",{svgOrigin:"64 64",rotation:-40});')
    add(f'tl.to("#ht",{{opacity:1,y:0,scale:1,duration:0.38,ease:"back.out(1.5)"}},{t_ht:.3f});')
    t = t_ht + 0.4; n = 0
    while t + 0.9 <= R - 0.1:                                 # quarter-turn twists, like turning the lamp
        add(f'tl.to("#rot",{{rotation:"+=90",duration:0.45,ease:"power2.inOut"}},{t:.3f});'); t += 0.9; n += 1
        if n in (1, 3): cues.append((t - 0.9 + 0.05, "ratchet.wav", -17, "turn arrow"))
    add(f'tl.to("#rot",{{opacity:0,duration:0.2}},{R - 0.05:.3f});')
    add(f'tl.to("#bulb",{{attr:{{fill:"#ffd88a"}},duration:0.12,ease:"none"}},{R:.3f});')
    add(f'tl.to("#glowc",{{attr:{{fill:"rgba(255,205,120,.55)",r:58}},duration:0.3,ease:"power2.out"}},{R:.3f});')
    add(f'tl.to("#h2a",{{opacity:0,y:-10,duration:0.15}},{R:.3f}); tl.to("#h2b",{{opacity:1,y:0,duration:0.25,ease:"back.out(2)"}},{R + 0.05:.3f});')
    add(f'tl.to("#ht",{{borderColor:"rgba(255,214,140,1)",boxShadow:"0 0 60px rgba(255,200,110,.55)",duration:0.3}},{R:.3f});')
    add(f'tl.to("#ht",{{opacity:0,y:-30,duration:0.3,ease:"power2.in"}},{fr(P.S["glow"]["o1"]) - 0.35:.3f});')
    cues.append((t_ht, "curated/ui-pop.wav", -13, "how-to card"))

    # 5 — end recap chips, then the name
    html.append(f'<div id="recap"><div class="chip">{LAYERS}3D WALL ART</div><div class="chip">{KEYI}5 KEY HOOKS</div><div class="chip">{BULB}LAMPS</div></div>')
    add('gsap.set("#recap .chip",{opacity:0,y:18});')
    for i in range(3):
        add(f'tl.to("#recap .chip:nth-child({i + 1})",{{opacity:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{END0 + 0.15 + 0.14 * i:.3f});')
    cues += [(END0 + 0.15, "curated/ui-pop.wav", -14, "recap chips"), (END0 + 0.6, "thock.wav", -12, "end card name lands"),
             (END0 + 1.1, "curated/ui-pop.wav", -14, "handle pill pops")]
    # a fade/scale-in first shows on the frame after its tween starts → arrival sounds move one frame later
    ARRIVE = {"tick.wav", "curated/ui-pop.wav", "curated/ui-click.wav"}
    cues = [(t + (1 / FPS if s in ARRIVE else 0), s, g, l) for t, s, g, l in cues]
    return "".join(css), "\n        ".join(html), js, cues, 0.35          # last: end-card text delay (s) after the chips
