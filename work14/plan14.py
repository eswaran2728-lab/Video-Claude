# Sangili Karuppar 3D-printed statue reel (work14) - edit plan. 1080x1920, 30 fps.
# Facts (from the creator): 3D printed in PETG filament, 6 inch, made from the customer's reference picture.
# Voice: the creator's Tamil voice-over isolated from the CapCut music (DeepFilterNet3 -> src/vo_iso.wav); long pauses tightened.
# VO EDL (source s): pauses 5.12-6.00, 11.08-11.72, 17.70-18.38, 24.88-25.64, 29.64-30.74 cut down to ~0.3 s;
# 0.0-0.40 (silence) and 34.08- (CapCut tail) dropped.
FPS = 30
VO = [(0.40, 5.25), (5.85, 11.25), (11.60, 17.85), (18.25, 25.00), (25.50, 29.80), (30.55, 34.08)]
_out = []; _t = 0.0
for a, b in VO:
    _out.append((round(_t, 4), a, b)); _t += b - a
VO_END = round(_t, 3)
TAIL = 0.9
TOTAL = round(int((VO_END + TAIL) * FPS) / FPS, 4)


def s2o(s):
    for o, a, b in _out:
        if a - 1e-6 <= s <= b + 1e-6: return round(o + s - a, 3)
    return None


# Key spoken moments (source s -> output s), from word timings in transcript*.json
W = dict(customer=s2o(0.72), picture=s2o(3.16), sangili=s2o(4.6), karuppar=s2o(6.0), inches=s2o(7.62),
         athukkaaga=s2o(11.75), photo=s2o(13.3), design=s2o(15.0), paakkalaam=s2o(18.6), colour=s2o(19.8), venum=s2o(23.46),
         karuppar2=s2o(26.1), thaaraalamaa=s2o(27.8), bio=s2o(31.2), vanakkam=s2o(33.6))

# Scenes (output s). Statue clips: (src_in, src_out, speed) from clean ranges; 'still' = frozen source frame with a slow push.
SCENES = [
    # 1 HOOK - customer's picture (HTML card); statue plate is empty bed
    dict(name="hook", t0=0.0, t1=W["picture"] + 0.45, statue=None),
    # 2 3D PRINT - hero frame prints layer by layer, then lives
    dict(name="print", t0=W["picture"] + 0.45, t1=W["athukkaaga"] - 0.1, statue=[("still", 10.0, 3.4), (9.4, 10.7, 0.5)],
         reveal=(W["picture"] + 0.6, W["karuppar"] + 1.6)),
    # 3 DESIGN -> REAL - statue in the lower half, customer picture in the upper half (HTML)
    dict(name="compare", t0=W["athukkaaga"] - 0.1, t1=W["paakkalaam"] - 0.15, statue=[(0.5, 1.4, 0.6), (2.4, 3.6, 0.6), (15.4, 16.7, 0.75)], layout="low"),
    # 4 SAME COLOUR TONE
    dict(name="colour", t0=W["paakkalaam"] - 0.15, t1=W["venum"] - 0.6, statue=[(18.4, 19.3, 0.5), (9.4, 10.7, 0.6)]),
    # 5 WANT ONE? hero
    dict(name="want", t0=W["venum"] - 0.6, t1=W["bio"] - 0.6, statue=[(19.6, 20.3, 0.45), (18.4, 19.3, 0.45), ("still", 19.0, 3.0)], layout="mid"),
    # 6 END card
    dict(name="end", t0=W["bio"] - 0.6, t1=TOTAL, statue=[("still", 10.0, 9.0)], layout="small"),
]
