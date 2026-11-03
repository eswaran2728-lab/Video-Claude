# HyperFrames composition for the Sepang team recap -> edit/index.html (+ edit/cues.json for mix15.py).
# Motion design adapted (not copied) from three Prompt Motion entries:
#  - "Poster breaking its frame" (prompt-motion.com/pankajkumar-dev-0bee87): the creator's poster tilts in as a card, its own
#    title pieces tear out of it, lift off the paper and break past its edges, then regroup as a title stack + info row.
#  - "Badge unlock screen animation" (prompt-motion.com/bthreeagency-b9b8d9): medals as solid metallic badges that spin in on
#    a 3D axis, settle without bounce and release a short burst of particles; the grand total gets gold particles + rays.
#  - "Festival lineup promo reel" (prompt-motion.com/gonzalomacagno-2de1a9): results set as a lineup poster - zone name as the
#    headline, school rows rising out of a mask line, a counter footer.
# Every name and number comes from the creator's results brief (plan15.ZONES / OVERALL) or the poster.
import json, html, math, random
import plan15 as P
T = P.TOTAL; R = lambda v: round(v, 3); BEAT = P.BEAT
GOLD, RED, INK, SILVER, BRONZE = "#f2b705", "#d7192d", "#0e0b10", "#d9dde2", "#cd7f32"
els, js, init, cues = [], [], [], []
E, J, I = els.append, js.append, init.append
rnd = random.Random(15)


def cue(t, sfx, gain): cues.append((R(t), sfx, gain))


def tw(sel, t, d, props, ease="power3.out"):
    J(f'tl.to("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())},duration:{R(d)},ease:"{ease}"}},{R(t)});')


def st(sel, t, props):
    J(f'tl.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())}}},{R(t)});')


def gs(sel, props):
    I(f'gsap.set("{sel}",{{{",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())}}});')


def esc(s): return html.escape(s)


# ---------- reusable pieces ----------
def odometer(oid, value, size, color="#fff", cls=""):
    """digit columns that roll from 0 to value (deterministic transforms, no text updates)"""
    nd = max(1, len(str(value))); cols = []
    for d in range(nd):
        p = 10 ** (nd - 1 - d); seq = "".join(f"<b>{(i // p) % 10 if (i >= p or p == 1 or d == nd - 1) else '&nbsp;'}</b>" for i in range(value + 1))
        cols.append(f'<span class="odc" style="height:{size}px"><span class="ods" id="{oid}d{d}">{seq}</span></span>')
    return f'<span class="odo {cls}" id="{oid}" style="font-size:{size}px;line-height:{size}px;color:{color}">{"".join(cols)}</span>', nd


def roll(oid, nd, value, t, d, size):
    for k in range(nd): tw(f"#{oid}d{k}", t, d, {"y": -value * size}, "power2.out")


def badge_html(bid, kind, num=None, size=96, label=True):
    lab = f'<div class="blab">{kind.upper()}</div>' if label else ""
    n = f"<span>{num}</span>" if num is not None else ""
    return (f'<div class="badge {kind}" id="{bid}" style="width:{size}px"><div class="rib"><i></i><i></i></div>'
            f'<div class="disc" style="width:{size}px;height:{size}px;font-size:{round(size * .5)}px">{n}</div>{lab}</div>')


def particles(pid, x, y, n, colors, spread=150, t=0.0, d=0.8, size=9):
    """burst of n dots from (x,y) - positions precomputed (seeded), gravity pulls them down"""
    dots = []
    for k in range(n):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(0.45, 1.0) * spread; s = rnd.uniform(0.6, 1.3) * size
        c = colors[k % len(colors)]
        dots.append(f'<i id="{pid}_{k}" style="left:{x}px;top:{y}px;width:{s:.0f}px;height:{s:.0f}px;background:{c}"></i>')
        gs(f"#{pid}_{k}", {"xPercent": -50, "yPercent": -50, "opacity": 0, "scale": 0.4})
        st(f"#{pid}_{k}", t, {"opacity": 1})
        tw(f"#{pid}_{k}", t, d, {"x": R(math.cos(a) * r), "y": R(math.sin(a) * r * 0.8 + spread * 0.35), "scale": 1, "opacity": 0}, "power2.out")
    E(f'<div class="pt" id="{pid}">{"".join(dots)}</div>')


def unlock(bid, t, x, y, kind):
    """badge unlock: spins in on Y, settles (no bounce), shine sweep + particle burst"""
    gs(f"#{bid}", {"scale": 0, "rotationY": -540, "opacity": 0})
    st(f"#{bid}", t, {"opacity": 1})
    tw(f"#{bid}", t, 0.55, {"scale": 1, "rotationY": 0}, "power3.out")
    col = {"silver": ["#ffffff", SILVER, "#9aa3ad"], "bronze": ["#ffd2a1", BRONZE, "#8a4b1c"], "gold": ["#fff4bf", GOLD, "#c8921a"]}[kind]
    particles(f"{bid}p", x, y, 12, col, spread=110, t=t + 0.25, d=0.75, size=8)
    cue(t + 0.25, "shimmer.wav", -17)


def chip(cid, text, t0, t1, y=440, color=RED):
    E(f'<div id="{cid}" class="chip" style="top:{y}px;background:{color}">{esc(text)}</div>')
    gs(f"#{cid}", {"xPercent": -50, "opacity": 0, "y": 16})
    tw(f"#{cid}", t0, 0.3, {"opacity": 1, "y": 0}); tw(f"#{cid}", t1 - 0.25, 0.22, {"opacity": 0, "y": -10}, "power2.in")
    cue(t0, "curated/ui-pop.wav", -15)


# ---------- header: the creator's three logos + gold MAHAGURU SRI S ARUMUGAM / STUDENTS ----------
E('<div id="hshade"></div><div id="hdr"><div class="hlogos">'
  '<div class="hwhite"><img src="assets/logos/silambam_malaysia_onwhite.jpg" alt=""></div>'
  '<img class="hm" src="assets/logos/mahaguru.png" alt="">'
  '<img class="hs" src="assets/logos/silambam_selangor.png" alt=""></div>'
  '<div class="hl1">MAHAGURU SRI S ARUMUGAM</div><div class="hl2"><i></i>STUDENTS<i></i></div></div>')
gs("#hdr", {"xPercent": -50, "opacity": 0, "y": -20}); gs("#hshade", {"opacity": 0})
tw("#hdr", 0.15, 0.5, {"opacity": 1, "y": 0}); tw("#hshade", 0.0, 0.4, {"opacity": 1})
tw("#hdr", P.SEC["end"][0] - 0.3, 0.3, {"opacity": 0, "y": -20}, "power2.in"); tw("#hshade", P.SEC["end"][0] - 0.3, 0.3, {"opacity": 0}, "power2.in")

# ---------- 1 HOOK ----------
cue(0.0, "curated/hook-impact.wav", -10)
E('<div id="hk_tag" class="tagline">KEJOHANAN SILAMBAM 2026</div>')
gs("#hk_tag", {"xPercent": -50, "opacity": 0, "y": 20}); tw("#hk_tag", 0.25, 0.35, {"opacity": 1, "y": 0}); tw("#hk_tag", 1.6, 0.2, {"opacity": 0})
for k, (n, a, b) in enumerate(P.HOOK_PHOTOS):
    E(f'<div class="ph" id="hp{k}"><img src="assets/photos/{n}.jpg" alt=""></div>')
    gs(f"#hp{k}", {"opacity": 0}); st(f"#hp{k}", a, {"opacity": 1}); st(f"#hp{k}", b, {"opacity": 0})
    gs(f"#hp{k} img", {"scale": 1.12}); tw(f"#hp{k} img", a, b - a, {"scale": 1.0}, "power2.out")
    cue(a, "curated/camera-shutter-light.wav", -14)
E('<div id="hk_low" class="lowgrad"></div>')
o, nd = odometer("hk_odo", 13, 300, GOLD, "goldtxt")
E(f'<div id="hk_count">{o}<div class="hk_m">MEDALS</div></div>')
E('<div id="hk_team"><div class="team1">SEPANG TEAM</div><div class="team2">KEJOHANAN SILAMBAM 2026</div></div>')
h0, h1 = P.HOOK_PHOTOS[0][1], P.SEC["hook"][1]
gs("#hk_low", {"opacity": 0}); gs("#hk_count", {"xPercent": -50, "opacity": 0, "y": 30}); gs("#hk_team", {"xPercent": -50, "opacity": 0, "y": 20})
tw("#hk_low", h0, 0.25, {"opacity": 1}); tw("#hk_count", h0, 0.3, {"opacity": 1, "y": 0})
roll("hk_odo", nd, 13, h0, 1.8, 300); cue(h0 + 0.1, "ratchet.wav", -13)
lock = P.HOOK_PHOTOS[-1][2]
tw("#hk_count", lock, 0.45, {"y": -520, "scale": 1.12}, "power3.inOut"); tw("#hk_low", lock, 0.3, {"opacity": 0})
tw("#hk_team", lock + 0.3, 0.4, {"opacity": 1, "y": 0})
particles("hkp", 540, 760, 26, ["#fff4bf", GOLD, "#c8921a", "#ffffff"], spread=420, t=lock + 0.2, d=1.2, size=12)
cue(lock + 0.05, "sub-impact.wav", -9); cue(lock + 0.2, "sparkle.wav", -14)
tw("#hk_count", h1 - 0.3, 0.3, {"opacity": 0, "scale": 1.3}, "power2.in"); tw("#hk_team", h1 - 0.3, 0.25, {"opacity": 0, "y": -20}, "power2.in")

# ---------- 2 POSTER -> motion graphics ----------
PM = json.load(open("edit/assets/poster/pieces.json")); PW, PH = PM["poster"]
p0, p1 = P.SEC["poster"]
CW = 800; k = CW / PW; CX0, CY0 = 540 - CW / 2, 470            # card on screen
E(f'<div id="pst_bg"></div><div id="pst_stage"><div id="card" style="left:{CX0}px;top:{CY0}px;width:{CW}px;height:{R(PH * k)}px">'
  f'<img src="assets/poster/full.jpg" alt=""><div id="card_sheen"></div>' +
  "".join(f'<div class="hole" id="hole_{n}" style="left:{R((b["box"][0]) * k)}px;top:{R(b["box"][1] * k)}px;'
          f'width:{R((b["box"][2] - b["box"][0]) * k)}px;height:{R((b["box"][3] - b["box"][1]) * k)}px"></div>'
          for n, b in PM["pieces"].items() if n != "logos") + '</div></div>')
# final layout: centre (x, y) on screen and size scale (screen px per poster px)
FINAL = {"kejohanan": (540, 520, 1.22), "silambam": (540, 690, 1.27), "peringkat": (540, 868, 1.22), "y2026": (540, 1000, 1.08),
         "date": (205, 1180, 1.25), "time": (543, 1180, 1.25), "venue": (877, 1180, 1.25), "tamil": (540, 1362, 1.22),
         "anjuran": (540, 1530, 0.82)}
LIFT = {"kejohanan": (p0 + 2 * BEAT, -3), "silambam": (p0 + 3 * BEAT, 2), "peringkat": (p0 + 4 * BEAT, -2), "y2026": (p0 + 5 * BEAT, 3)}
for n, (fx, fy, fs) in FINAL.items():
    b = PM["pieces"][n]; x0, y0, x1, y1 = b["box"]; pad = b["pad"]
    w = b["png"][0] / PM["scale"] * k; h = b["png"][1] / PM["scale"] * k
    left = CX0 + (x0 - pad) * k; top = CY0 + (y0 - pad) * k
    E(f'<img class="piece" id="pc_{n}" src="assets/poster/{n}.png" style="left:{R(left)}px;top:{R(top)}px;width:{R(w)}px;height:{R(h)}px" alt="">')
    gs(f"#pc_{n}", {"opacity": 0, "filter": "drop-shadow(0px 0px 0px rgba(0,0,0,0))"})
    cx, cy = left + w / 2, top + h / 2; sc = fs / k
    FINAL[n] = (fx - cx, fy - cy, sc)
gs("#pst_bg", {"opacity": 0}); gs("#card", {"opacity": 0, "rotationX": 28, "rotationY": -24, "scale": 0.62, "y": 260, "transformPerspective": 1600})
gs(".hole", {"opacity": 0}); gs("#card_sheen", {"xPercent": -160})
st("#pst_bg", p0, {"opacity": 1}); tw("#card", p0, 0.75, {"opacity": 1, "rotationX": 0, "rotationY": 0, "scale": 1, "y": 0}, "power3.out")
for n in FINAL: st(f"#pc_{n}", p0 + 0.75, {"opacity": 1})          # pieces sit exactly on the card, invisible seam
cue(p0, "curated/zoom-swish.wav", -12)
tw("#card_sheen", p0 + 0.55, 0.7, {"xPercent": 160}, "power2.inOut")
for n, (t, rot) in LIFT.items():                                  # tear out + lift off the paper (break the frame)
    st(f"#hole_{n}", t, {"opacity": 1})
    tw(f"#pc_{n}", t, 0.45, {"scale": 1.12 if n != "silambam" else 1.3, "rotation": rot, "y": -26, "filter": "drop-shadow(0px 26px 26px rgba(0,0,0,0.65))"}, "back.out(1.4)")
    cue(t, "thock.wav", -9); cue(t - 0.06, "curated/zoom-swish.wav", -19)
cue(p0 + 5 * BEAT, "sub-impact.wav", -12)
reg = p0 + 6.5 * BEAT                                            # 9.6: card recedes, pieces regroup into the title stack
tw("#card", reg, 0.6, {"scale": 0.9, "opacity": 0.14}, "power2.inOut")
for j, n in enumerate(["kejohanan", "silambam", "peringkat", "y2026"]):
    dx, dy, sc = FINAL[n]; tw(f"#pc_{n}", reg + 0.06 * j, 0.7, {"x": R(dx), "y": R(dy), "scale": R(sc), "rotation": 0}, "power3.inOut")
for j, n in enumerate(["date", "time", "venue", "tamil", "anjuran"]):
    t = reg + 0.75 + (BEAT / 2) * j; dx, dy, sc = FINAL[n]
    st(f"#hole_{n}", t, {"opacity": 1})
    tw(f"#pc_{n}", t, 0.6, {"x": R(dx), "y": R(dy), "scale": R(sc), "filter": "drop-shadow(0px 18px 20px rgba(0,0,0,0.6))"}, "power3.out")
    cue(t, "curated/ui-pop.wav", -14)
for j, n in enumerate(FINAL):                                     # exit
    tw(f"#pc_{n}", p1 - 0.42 + 0.025 * j, 0.32, {"y": f"-=160", "opacity": 0}, "power2.in")
tw("#card", p1 - 0.4, 0.3, {"opacity": 0}, "power2.in"); tw("#pst_bg", p1 - 0.2, 0.2, {"opacity": 0})
cue(p1 - 0.35, "curated/zoom-swish.wav", -13)

# ---------- 3 THE DAY (plate footage) ----------
S = {s["id"]: s for s in P.SEGS}
chip("ch_arena", "THE ARENA", S["arena"]["t0"] + 0.15, S["arena"]["t1"])
chip("ch_ath", "THE ATHLETES", S["athletes"]["t0"] + 0.1, S["march"]["t1"], color="#1d4fd8")
chip("ch_bout", "THE BOUTS", S["bout"]["t0"] + 0.1, S["bout_slow"]["t0"])
chip("ch_slow", "SLOW-MO", S["bout_slow"]["t0"] + 0.05, S["bout_slow"]["t1"] - 0.1, color="#3a3340")
E('<div id="flash1" class="flash"></div>'); gs("#flash1", {"opacity": 0})
st("#flash1", S["bout"]["t0"], {"opacity": 0.6}); tw("#flash1", S["bout"]["t0"] + 0.02, 0.25, {"opacity": 0}, "power2.out")
for s in ("arena", "athletes", "march", "bout"): cue(S[s]["t0"], "curated/zoom-swish.wav", -18)
cue(S["bout_slow"]["t0"], "curated/metallic-riser.wav", -20)

# ---------- 4 RESULTS by zone ----------
r0, r1 = P.SEC["results"]
E('<div id="res_head"><div class="rh1">SEPANG TEAM · RESULTS</div></div>')
gs("#res_head", {"xPercent": -50, "opacity": 0}); tw("#res_head", r0, 0.3, {"opacity": 1}); tw("#res_head", r1 - 0.3, 0.3, {"opacity": 0})
ROWY0, ROWH = 812, 150
for zi, z in enumerate(P.ZONES):
    t0, t1 = z["t0"], z["t1"]; dots = "".join(f'<i class="{"on" if j == zi else ""}"></i>' for j in range(len(P.ZONES)))
    rows = []
    for si, (name, sv, bz) in enumerate(z["schools"]):
        b = []
        if sv: b.append(badge_html(f"z{zi}s{si}sv", "silver", sv, 92))
        if bz: b.append(badge_html(f"z{zi}s{si}bz", "bronze", bz, 92))
        right = "".join(b) if b else '<div class="part">PARTICIPATED</div>'
        rows.append(f'<div class="row" style="top:{ROWY0 + ROWH * si - 470}px"><div class="rowi" id="z{zi}r{si}"><div class="sname">{esc(name)}</div>'
                    f'<div class="sbad">{right}</div></div></div>')
    tot = sum(z["total"]); o, nd = odometer(f"z{zi}o", tot, 120, "#fff")
    brk = " · ".join(x for x in [f'{z["total"][1]} SILVER' if z["total"][1] else "", f'{z["total"][2]} BRONZE' if z["total"][2] else ""] if x)
    zh = 342 + ROWH * len(z["schools"]) + 300
    E(f'<div class="zone" id="z{zi}" style="height:{zh}px"><div class="zdots">{dots}<span>ZONE {zi + 1} / {len(P.ZONES)}</span></div>'
      f'<div class="zmask"><div class="zname" id="z{zi}n">{esc(z["name"])}</div></div><div class="zrule" id="z{zi}u"></div>'
      f'{"".join(rows)}<div class="ztot" id="z{zi}t"><div class="ztl">ZONE TOTAL</div><div class="ztn">{o}<span class="ztm">{"MEDAL" if tot == 1 else "MEDALS"}</span></div>'
      f'<div class="ztb">{brk}</div></div></div>')
    gs(f"#z{zi}", {"opacity": 0, "x": 140}); gs(f"#z{zi}n", {"yPercent": 110}); gs(f"#z{zi}u", {"scaleX": 0}); gs(f"#z{zi}t", {"opacity": 0, "y": 30})
    tw(f"#z{zi}", t0, 0.4, {"opacity": 1, "x": 0}, "power3.out"); cue(t0, "curated/zoom-swish.wav", -14)
    tw(f"#z{zi}n", t0 + 0.1, 0.45, {"yPercent": 0}, "power4.out"); tw(f"#z{zi}u", t0 + 0.25, 0.4, {"scaleX": 1}, "power3.inOut")
    n = len(z["schools"]); avail = (t1 - t0) - 2.3; step = min(BEAT * 1.5, avail / max(n, 1))
    for si, (name, sv, bz) in enumerate(z["schools"]):
        ts = t0 + 0.55 + step * si
        gs(f"#z{zi}r{si}", {"yPercent": 105})
        tw(f"#z{zi}r{si}", ts, 0.42, {"yPercent": 0}, "power3.out"); cue(ts, "curated/ui-click.wav", -16)
        y = ROWY0 + ROWH * si + 66
        if sv: unlock(f"z{zi}s{si}sv", ts + 0.2, 810 if bz else 920, y, "silver")
        if bz: unlock(f"z{zi}s{si}bz", ts + 0.2 + (0.18 if sv else 0), 920, y, "bronze")
    tt = t1 - 1.75
    tw(f"#z{zi}t", tt, 0.35, {"opacity": 1, "y": 0}); roll(f"z{zi}o", nd, tot, tt, 0.7, 120); cue(tt, "ratchet.wav", -15)
    cue(tt + 0.6, "clean-ding.wav", -14)
    if zi < len(P.ZONES) - 1: tw(f"#z{zi}", t1 - 0.3, 0.3, {"opacity": 0, "x": -140}, "power2.in")
    else: tw(f"#z{zi}", t1 - 0.3, 0.3, {"opacity": 0, "scale": 0.94}, "power2.in")

# ---------- 5 OVERALL TALLY ----------
a0, a1 = P.SEC["tally"]
E(f'<div class="ph" id="tal_bg"><img src="assets/photos/{P.TALLY_BG}_blur.jpg" alt=""></div>')
gs("#tal_bg", {"opacity": 0}); tw("#tal_bg", a0, 0.4, {"opacity": 1}); tw("#tal_bg", a1 - 0.3, 0.3, {"opacity": 0})
gs("#tal_bg img", {"scale": 1.18}); tw("#tal_bg img", a0, a1 - a0, {"scale": 1.04}, "none")
cols = []
for j, (kind, val) in enumerate([("gold", P.OVERALL["gold"]), ("silver", P.OVERALL["silver"]), ("bronze", P.OVERALL["bronze"])]):
    o, nd = odometer(f"tc{j}o", val, 110, "#fff"); cols.append((kind, val, nd))
    E(f'<div class="tcol{" dim" if val == 0 else ""}" id="tc{j}" style="left:{200 + 340 * j}px">{badge_html(f"tc{j}b", kind, None, 140, False)}'
      f'<div class="tnum">{o}</div><div class="tlab">{kind.upper()}</div></div>')
    gs(f"#tc{j}", {"xPercent": -50, "opacity": 0, "y": 40})
E('<div id="tal_title"><div class="tt1">OVERALL MEDAL TALLY</div><div class="tt2">SEPANG TEAM</div></div>')
gs("#tal_title", {"xPercent": -50, "opacity": 0, "y": 30}); tw("#tal_title", a0 + 0.1, 0.45, {"opacity": 1, "y": 0})
for j, (kind, val, nd) in enumerate(cols):
    t = a0 + 0.5 + BEAT * j
    tw(f"#tc{j}", t, 0.4, {"opacity": 1, "y": 0}); unlock(f"tc{j}b", t, 200 + 340 * j, 690, kind)
    if val: roll(f"tc{j}o", nd, val, t + 0.25, 0.9, 110); cue(t + 0.3, "ratchet.wav", -15)
# the stack: medals per zone, silver + bronze segments, sorted by total
ZS = sorted(P.ZONES, key=lambda z: -sum(z["total"])); UNIT = 112; sy0 = 1000
bars = []
for j, z in enumerate(ZS):
    sv, bz = z["total"][1], z["total"][2]
    bars.append(f'<div class="srow" style="top:{sy0 + 72 * j}px"><div class="slab">{esc(z["name"])}</div><div class="sbar" id="sb{j}">'
                f'<i class="sv" style="width:{sv * UNIT}px"></i><i class="bz" style="width:{bz * UNIT}px"></i></div>'
                f'<div class="sval" id="sv{j}" style="left:{318 + (sv + bz) * UNIT + 16}px">{sv + bz}</div></div>')
E(f'<div id="stack">{"".join(bars)}</div>')
gs("#stack", {"opacity": 0}); ts0 = a0 + 0.5 + BEAT * 3 + 0.2
st("#stack", ts0, {"opacity": 1})
for j in range(len(ZS)):
    gs(f"#sb{j}", {"scaleX": 0, "transformOrigin": "0% 50%"}); gs(f"#sv{j}", {"opacity": 0})
    tw(f"#sb{j}", ts0 + 0.12 * j, 0.6, {"scaleX": 1}, "power3.out"); tw(f"#sv{j}", ts0 + 0.12 * j + 0.45, 0.25, {"opacity": 1})
cue(ts0, "curated/ui-pop.wav", -15)
# grand total
gt = P.bar(12)                                                    # 53.99, on a downbeat
o, nd = odometer("gto", 13, 250, "#2a1a00")
E(f'<div id="gtw"><div id="rays"></div><div id="gtb"><div class="gtd">{o}</div></div>'
  f'<div id="gtl"><div class="g1">GRAND TOTAL</div><div class="g2">13 MEDALS</div></div></div><div id="flash2" class="flash"></div>')
gs("#gtw", {"opacity": 0}); gs("#gtb", {"scale": 0, "rotationY": -540}); gs("#gtl", {"opacity": 0, "y": 30}); gs("#rays", {"opacity": 0, "scale": 0.6})
gs("#flash2", {"opacity": 0})
cue(gt - 1.6, "curated/metallic-riser.wav", -14)
tw("#tal_title", gt - 0.3, 0.3, {"opacity": 0, "y": -30}, "power2.in"); tw("#stack", gt - 0.3, 0.3, {"opacity": 0.0}, "power2.in")
for j in range(3): tw(f"#tc{j}", gt - 0.3, 0.3, {"opacity": 0, "y": -30}, "power2.in")
st("#gtw", gt, {"opacity": 1}); st("#flash2", gt, {"opacity": 0.7}); tw("#flash2", gt + 0.02, 0.3, {"opacity": 0}, "power2.out")
tw("#gtb", gt, 0.6, {"scale": 1, "rotationY": 0}, "power3.out"); roll("gto", nd, 13, gt + 0.1, 1.0, 250)
tw("#rays", gt, 0.6, {"opacity": 1, "scale": 1}, "power2.out"); tw("#rays", gt, a1 - gt, {"rotation": 40}, "none")
tw("#gtl", gt + 0.5, 0.4, {"opacity": 1, "y": 0})
particles("gtp", 540, 900, 40, ["#fff4bf", GOLD, "#c8921a", "#ffffff", "#ffe28c"], spread=520, t=gt + 0.3, d=1.6, size=14)
particles("gtp2", 540, 900, 30, ["#fff4bf", GOLD, "#ffe28c"], spread=380, t=gt + 1.6, d=1.4, size=10)
cue(gt, "sub-impact.wav", -7); cue(gt + 0.02, "curated/hook-impact.wav", -12); cue(gt + 0.3, "sparkle.wav", -12); cue(gt + 1.6, "shimmer.wav", -15)
tw("#gtw", a1 - 0.35, 0.35, {"opacity": 0, "scale": 1.1}, "power2.in")

# ---------- 6 CONGRATULATIONS ----------
c0, c1 = P.SEC["congrats"]
for j, (n, fx) in enumerate(P.CONGRATS):
    t = P.CONGRATS_T0 + P.CONGRATS_STEP * j; te = t + P.CONGRATS_STEP
    from PIL import Image as _Im
    _w, _h = _Im.open(f"edit/assets/photos/{n}.jpg").size; pos = "50% 30%" if _w > _h else "50% 50%"   # landscape: above the text block
    E(f'<div class="ph cph" id="cp{j}"><img class="cbg" src="assets/photos/{n}_blur.jpg" alt=""><img class="cfg" src="assets/photos/{n}_c.jpg" style="object-position:{pos}" alt=""></div>')
    gs(f"#cp{j}", {"opacity": 0}); gs(f"#cp{j} .cfg", {"scale": 1.08 if j % 2 else 1.0})
    tw(f"#cp{j}", t, 0.25, {"opacity": 1}, "power1.out")
    tw(f"#cp{j} .cfg", t, P.CONGRATS_STEP + 0.3, {"scale": 1.0 if j % 2 else 1.08}, "none")
    if j < len(P.CONGRATS) - 1: st(f"#cp{j}", te + 0.26, {"opacity": 0})
    else: tw(f"#cp{j}", c1 - 0.3, 0.3, {"opacity": 0})
    cue(t, "curated/camera-shutter-light.wav", -17)
E('<div id="cg_low" class="lowgrad tall"></div><div id="cg"><div class="cg1" id="cg1">TAHNIAH!</div><div class="cg2" id="cg2">CONGRATULATIONS</div>'
  '<div class="cg3" id="cg3a">to all our students, masters<br>&amp; participating schools</div>'
  '<div class="cg3" id="cg3b">for their hard work, dedication<br>&amp; achievements</div></div>')
gs("#cg_low", {"opacity": 0}); gs("#cg", {"xPercent": -50}); gs("#cg1", {"opacity": 0, "scale": 1.4}); gs("#cg2", {"opacity": 0, "y": 20})
gs("#cg3a", {"opacity": 0, "y": 16}); gs("#cg3b", {"opacity": 0, "y": 16})
tw("#cg_low", c0, 0.4, {"opacity": 1}); tw("#cg1", c0 + 0.3, 0.45, {"opacity": 1, "scale": 1}, "expo.out")
tw("#cg2", c0 + 0.6, 0.4, {"opacity": 1, "y": 0}); tw("#cg3a", c0 + 1.0, 0.4, {"opacity": 1, "y": 0})
mid = P.CONGRATS_T0 + P.CONGRATS_STEP * 4
tw("#cg3a", mid - 0.25, 0.25, {"opacity": 0, "y": -12}, "power2.in"); tw("#cg3b", mid, 0.4, {"opacity": 1, "y": 0})
for s in ("#cg_low", "#cg1", "#cg2", "#cg3b"): tw(s, c1 - 0.3, 0.3, {"opacity": 0}, "power2.in")
particles("cgp", 540, 1330, 22, ["#fff4bf", GOLD, "#ffffff"], spread=360, t=c0 + 0.35, d=1.3, size=11)
cue(c0 + 0.3, "sparkle.wav", -13)

# ---------- 7 END CARD ----------
e0 = P.SEC["end"][0]
E('<div id="end"><div id="endglow"></div><div id="logocard" class="lc">'
  '<img src="assets/logos/silambam_malaysia_onwhite_end.jpg" alt=""><img src="assets/logos/mahaguru_end.png" alt=""><img src="assets/logos/silambam_selangor_end.png" alt=""></div>'
  '<div class="e1" id="e1">PERSATUAN SILAMBAM MALAYSIA</div><div class="e2" id="e2">DAERAH SEPANG</div>'
  '<div class="e3" id="e3"><div class="hl1">MAHAGURU SRI S ARUMUGAM</div><div class="hl2"><i></i>STUDENTS<i></i></div></div>'
  '<img id="etamil" src="assets/poster/tamil_end.png" alt=""><div class="e4" id="e4">KEJOHANAN SILAMBAM 2026 · 31.10.2026</div></div>')
gs("#end", {"opacity": 0}); gs("#logocard", {"xPercent": -50, "scale": 0.8, "opacity": 0, "y": 30})
for s in ("#e1", "#e2", "#e3", "#etamil", "#e4"): gs(s, {"xPercent": -50, "opacity": 0, "y": 24})
st("#end", e0, {"opacity": 1}); tw("#logocard", e0 + 0.1, 0.6, {"scale": 1, "opacity": 1, "y": 0}, "power3.out")
for j, s in enumerate(("#e1", "#e2", "#e3", "#etamil", "#e4")): tw(s, e0 + 0.45 + 0.18 * j, 0.45, {"opacity": 1, "y": 0})
particles("ep", 540, 640, 24, ["#fff4bf", GOLD, "#ffe28c"], spread=480, t=e0 + 0.2, d=1.8, size=10)
cue(e0 + 0.1, "curated/zoom-swish.wav", -15); cue(e0 + 0.3, "shimmer.wav", -15)
tw("#end", T - 0.6, 0.6, {"opacity": 0}, "power1.in")

CSS = f'''
@font-face {{ font-family: "IDB"; src: url("assets/fonts/InterDisplay-Black.otf"); font-weight: 900; }}
@font-face {{ font-family: "IDBo"; src: url("assets/fonts/InterDisplay-Bold.otf"); font-weight: 700; }}
@font-face {{ font-family: "ISB"; src: url("assets/fonts/Inter-SemiBold.otf"); font-weight: 600; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
.clip {{ position: absolute; inset: 0; }} .vid {{ width: 1080px; height: 1920px; object-fit: cover; }}
#gfx {{ z-index: 10; pointer-events: none; overflow: hidden; }}
.goldtxt b, .hl1, .hl2, .g1, .cg1, .tt2, .team1 {{ background: linear-gradient(180deg, #fff4bf 0%, #f6cf55 34%, #c8921a 62%, #ffe28c 84%, #b27c10 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; }}
#hshade {{ position: absolute; left: 0; top: 0; width: 1080px; height: 470px; z-index: 50; background: linear-gradient(180deg, rgba(8,6,10,.72), rgba(8,6,10,.38) 60%, rgba(8,6,10,0)); }}
#hdr {{ position: absolute; left: 540px; top: 150px; z-index: 51; text-align: center; }}
.hlogos {{ display: flex; align-items: center; justify-content: center; gap: 26px; height: 112px; margin-bottom: 8px; }}
.hwhite {{ width: 112px; height: 112px; border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,.45); }}
.hwhite img {{ width: 100px; height: 100px; object-fit: contain; }}
.hm {{ height: 112px; filter: drop-shadow(0 4px 10px rgba(0,0,0,.55)); }} .hs {{ height: 106px; filter: drop-shadow(0 4px 10px rgba(0,0,0,.55)); }}
.hl1 {{ font-family: "IDB"; font-size: 38px; letter-spacing: 2px; line-height: 1.12; white-space: nowrap; filter: drop-shadow(0 3px 4px rgba(0,0,0,.8)); }}
.hl2 {{ font-family: "IDB"; font-size: 25px; letter-spacing: 12px; line-height: 1.35; display: flex; align-items: center; justify-content: center; gap: 14px; filter: drop-shadow(0 3px 4px rgba(0,0,0,.8)); }}
.hl2 i {{ display: block; width: 64px; height: 3px; background: linear-gradient(90deg, #b27c10, #ffe28c); }}
.tagline {{ position: absolute; left: 540px; top: 1480px; font-family: "IDB"; font-size: 40px; letter-spacing: 6px; color: #fff; background: {RED}; padding: 12px 26px; border-radius: 10px; white-space: nowrap; }}
.ph {{ position: absolute; inset: 0; overflow: hidden; background: {INK}; }}
.ph img {{ width: 1080px; height: 1920px; object-fit: cover; }}
.cph .cbg {{ position: absolute; inset: 0; }}
.cph .cfg {{ position: absolute; inset: 0; object-fit: contain; }}
.lowgrad {{ position: absolute; left: 0; top: 1060px; width: 1080px; height: 860px; background: linear-gradient(180deg, rgba(14,11,16,0), rgba(14,11,16,.82) 40%, rgba(14,11,16,.92)); }}
.lowgrad.tall {{ top: 980px; height: 940px; }}
.odo {{ display: inline-flex; font-family: "IDB"; letter-spacing: -4px; }}
.odc {{ display: inline-block; overflow: hidden; }} .ods {{ display: flex; flex-direction: column; }} .ods b {{ display: block; font-weight: 900; text-align: center; }}
#hk_count {{ position: absolute; left: 540px; top: 1180px; text-align: center; filter: drop-shadow(0 10px 24px rgba(0,0,0,.6)); }}
.hk_m {{ font-family: "IDB"; font-size: 92px; letter-spacing: 10px; color: #fff; margin-top: -10px; }}
#hk_team {{ position: absolute; left: 540px; top: 1110px; text-align: center; width: 980px; }}
.team1 {{ font-family: "IDB"; font-size: 76px; letter-spacing: 4px; filter: drop-shadow(0 4px 6px rgba(0,0,0,.8)); }}
.team2 {{ font-family: "ISB"; font-size: 34px; line-height: 1.4; color: #fff; margin-top: 14px; text-shadow: 0 3px 10px rgba(0,0,0,.8); }}
#pst_bg {{ position: absolute; inset: 0; background: linear-gradient(180deg, {INK} 0%, #3a0a10 35%, #4a0c13 55%, #1f060a 80%, {INK} 100%); }}
#pst_stage {{ position: absolute; inset: 0; perspective: 1600px; }}
#card {{ position: absolute; overflow: hidden; border-radius: 6px; box-shadow: 0 40px 90px rgba(0,0,0,.6); }}
#card > img {{ width: 100%; height: 100%; display: block; }}
#card_sheen {{ position: absolute; top: -10%; left: 0; width: 45%; height: 120%; background: linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.38), rgba(255,255,255,0)); }}
.hole {{ position: absolute; background: #1c090c; box-shadow: inset 0 6px 18px rgba(0,0,0,.9); }}
.piece {{ position: absolute; transform-origin: 50% 50%; }}
.chip {{ position: absolute; left: 540px; height: 64px; line-height: 64px; padding: 0 28px; border-radius: 8px; color: #fff; font-family: "IDB"; font-size: 34px;
  letter-spacing: 6px; white-space: nowrap; box-shadow: 0 10px 26px rgba(0,0,0,.35); }}
.flash {{ position: absolute; inset: 0; background: #fff; }}
#res_head {{ position: absolute; z-index: 52; left: 540px; top: 418px; font-family: "IDB"; font-size: 30px; letter-spacing: 8px; color: {GOLD}; white-space: nowrap; }}
.zone {{ position: absolute; left: 60px; top: 470px; width: 960px; height: 1120px; border-radius: 30px; background: rgba(12,9,16,.74);
  border: 2px solid rgba(242,183,5,.35); box-shadow: 0 30px 80px rgba(0,0,0,.5); }}
.zdots {{ position: absolute; left: 50px; top: 40px; display: flex; align-items: center; gap: 10px; font-family: "ISB"; font-size: 26px; letter-spacing: 4px; color: rgba(255,255,255,.7); }}
.zdots i {{ display: block; width: 14px; height: 14px; border-radius: 50%; background: rgba(255,255,255,.22); }} .zdots i.on {{ background: {GOLD}; }}
.zdots span {{ margin-left: 10px; }}
.zmask {{ position: absolute; left: 50px; top: 90px; width: 860px; overflow: hidden; }}
.zname {{ font-family: "IDB"; font-size: 104px; line-height: 1.08; letter-spacing: -3px; color: #fff; white-space: nowrap; }}
.zrule {{ position: absolute; left: 50px; top: 232px; width: 860px; height: 6px; background: linear-gradient(90deg, {GOLD}, {RED}); transform-origin: 0 50%; }}
.row {{ position: absolute; left: 50px; width: 860px; height: 132px; overflow: hidden; }}
.rowi {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,.12); }}
.sname {{ font-family: "IDBo"; font-size: 44px; color: #fff; max-width: 560px; line-height: 1.12; }}
.sbad {{ display: flex; gap: 18px; align-items: center; }}
.part {{ font-family: "ISB"; font-size: 24px; letter-spacing: 4px; color: rgba(255,255,255,.62); border: 2px solid rgba(255,255,255,.28); padding: 10px 18px; border-radius: 30px; }}
.badge {{ position: relative; display: flex; flex-direction: column; align-items: center; }}
.rib {{ display: flex; gap: 0; height: 22px; margin-bottom: -6px; }} .rib i {{ display: block; width: 18px; height: 26px; background: {RED}; transform: skewX(18deg); }}
.rib i:nth-child(2) {{ background: #1d4fd8; transform: skewX(-18deg); }}
.disc {{ border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: "IDB"; color: #2a1a00; box-shadow: inset 0 -6px 12px rgba(0,0,0,.35), inset 0 6px 10px rgba(255,255,255,.6), 0 8px 18px rgba(0,0,0,.5); }}
.silver .disc {{ background: linear-gradient(145deg, #ffffff 0%, #d9dde2 40%, #8f98a3 100%); color: #2b3138; }}
.bronze .disc {{ background: linear-gradient(145deg, #ffe0bd 0%, #cd7f32 45%, #7a3f12 100%); color: #3a1c05; }}
.gold .disc {{ background: linear-gradient(145deg, #fff6c8 0%, #f2b705 45%, #a76f05 100%); }}
.blab {{ font-family: "ISB"; font-size: 18px; letter-spacing: 3px; color: rgba(255,255,255,.8); margin-top: 6px; }}
.ztot {{ position: absolute; left: 50px; bottom: 40px; width: 860px; height: 230px; border-radius: 22px; background: linear-gradient(135deg, rgba(242,183,5,.22), rgba(215,25,45,.22)); border: 2px solid rgba(242,183,5,.45); }}
.ztl {{ position: absolute; left: 36px; top: 28px; font-family: "IDB"; font-size: 28px; letter-spacing: 6px; color: {GOLD}; }}
.ztn {{ position: absolute; left: 36px; top: 70px; display: flex; align-items: baseline; gap: 18px; }}
.ztm {{ font-family: "IDB"; font-size: 48px; color: #fff; letter-spacing: 2px; }}
.ztb {{ position: absolute; right: 36px; top: 30px; font-family: "ISB"; font-size: 26px; letter-spacing: 3px; color: rgba(255,255,255,.82); }}
.pt {{ position: absolute; inset: 0; }} .pt i {{ position: absolute; border-radius: 50%; display: block; }}
#tal_title {{ position: absolute; left: 540px; top: 420px; text-align: center; white-space: nowrap; }}
.tt1 {{ font-family: "IDB"; font-size: 68px; color: #fff; letter-spacing: -1px; }} .tt2 {{ font-family: "IDB"; font-size: 36px; letter-spacing: 10px; margin-top: 4px; }}
.tcol {{ position: absolute; top: 600px; text-align: center; display: flex; flex-direction: column; align-items: center; }}
.tcol.dim {{ filter: saturate(.35) brightness(.7); }}
.tnum {{ margin-top: 10px; }} .tlab {{ font-family: "IDB"; font-size: 28px; letter-spacing: 6px; color: rgba(255,255,255,.85); }}
#stack {{ position: absolute; inset: 0; }}
.srow {{ position: absolute; left: 60px; width: 960px; height: 58px; }}
.slab {{ position: absolute; left: 0; width: 300px; top: 10px; text-align: right; font-family: "IDBo"; font-size: 30px; color: #fff; white-space: nowrap; }}
.sbar {{ position: absolute; left: 318px; top: 6px; height: 46px; display: flex; border-radius: 8px; overflow: hidden; }}
.sbar i {{ display: block; height: 46px; }} .sbar .sv {{ background: linear-gradient(180deg, #ffffff, #a9b1bb); }} .sbar .bz {{ background: linear-gradient(180deg, #f0b27a, #9a5420); }}
.sval {{ position: absolute; top: 4px; font-family: "IDB"; font-size: 40px; color: #fff; }}
#gtw {{ position: absolute; inset: 0; }}
#rays {{ position: absolute; left: 40px; top: 400px; width: 1000px; height: 1000px; border-radius: 50%;
  background: repeating-conic-gradient(from 0deg, rgba(242,183,5,.22) 0deg 7deg, rgba(242,183,5,0) 7deg 18deg);
  -webkit-mask-image: radial-gradient(circle, #000 25%, transparent 70%); mask-image: radial-gradient(circle, #000 25%, transparent 70%); }}
#gtb {{ position: absolute; left: 340px; top: 700px; width: 400px; height: 400px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(145deg, #fff6c8 0%, #f2b705 42%, #a76f05 100%);
  box-shadow: inset 0 -14px 26px rgba(0,0,0,.35), inset 0 12px 20px rgba(255,255,255,.6), 0 0 80px rgba(242,183,5,.55), 0 30px 60px rgba(0,0,0,.6); }}
#gtl {{ position: absolute; left: 0; width: 1080px; top: 1150px; text-align: center; }}
.g1 {{ font-family: "IDB"; font-size: 64px; letter-spacing: 10px; filter: drop-shadow(0 4px 6px rgba(0,0,0,.8)); }}
.g2 {{ font-family: "IDB"; font-size: 110px; color: #fff; letter-spacing: -2px; text-shadow: 0 10px 30px rgba(0,0,0,.6); }}
#cg {{ position: absolute; left: 540px; top: 1240px; width: 1000px; text-align: center; }}
.cg1 {{ font-family: "IDB"; font-size: 150px; letter-spacing: -2px; line-height: 1; filter: drop-shadow(0 6px 10px rgba(0,0,0,.8)); }}
.cg2 {{ font-family: "IDB"; font-size: 58px; letter-spacing: 8px; color: #fff; margin-top: 6px; }}
.cg3 {{ position: absolute; left: 0; width: 1000px; top: 236px; font-family: "ISB"; font-size: 38px; line-height: 1.32; color: #fff; text-shadow: 0 3px 10px rgba(0,0,0,.9); }}
#end {{ position: absolute; inset: 0; background: linear-gradient(180deg, {INK} 0%, #2e1f07 30%, #24180a 55%, {INK} 100%); }}
#endglow {{ display: none; }}
.lc {{ position: absolute; left: 540px; top: 470px; display: flex; align-items: center; gap: 40px; padding: 28px 46px; border-radius: 32px; background: #fff; box-shadow: 0 30px 70px rgba(0,0,0,.55); }}
.lc img {{ height: 220px; width: auto; }}
.e1, .e2, .e3, .e4, #etamil {{ position: absolute; left: 540px; text-align: center; white-space: nowrap; }}
.e1 {{ top: 830px; font-family: "IDB"; font-size: 56px; color: #fff; letter-spacing: 1px; }}
.e2 {{ top: 900px; font-family: "IDB"; font-size: 76px; color: {GOLD}; letter-spacing: 6px; }}
.e3 {{ top: 1030px; }} .e3 .hl1 {{ font-size: 46px; }} .e3 .hl2 {{ font-size: 30px; }}
#etamil {{ top: 1190px; width: 700px; }}
.e4 {{ top: 1360px; font-family: "ISB"; font-size: 30px; letter-spacing: 4px; color: rgba(255,255,255,.75); }}
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
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{T}">
      <video id="plate" class="clip vid" src="assets/v/plate.mp4" muted playsinline data-start="0" data-duration="{T}" data-track-index="1" style="z-index:1"></video>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{T}" data-track-index="2" data-volume="1"></audio>
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
open("edit/index.html", "w").write(doc)
json.dump({"cues": [{"t": a, "sfx": b, "gain_db": c} for a, b, c in sorted(cues)]}, open("edit/cues.json", "w"), indent=1)
print("built", T, len(js), "tweens", len(cues), "cues")
