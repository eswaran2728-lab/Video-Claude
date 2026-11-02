# v02 of the two-part Silambam reel (creator on v01: "cinematic look", "make the videos run a bit longer so can see the
# shows", gold Mahaguru Sri S Arumugam header + logo). Same footage and story as plan13.py (v01), but each performance shot
# is held ~3 s (4 beats) instead of 0.7-1.5 s, and the team's own introduction ("...Mahaguru Sri S Arumugam avargalin
# maanavargal" = students of Mahaguru Sri S Arumugam, v_215647 30.85-33.95, name confirmed by the creator) opens Part 1.
# Segment = (clip, src_in, src_out, speed, kind) as in plan13.py.
BEAT = 0.743
B4 = 4 * BEAT                                       # 2.972 s performance shot

PART1 = [
    # HOOK - watermelon on the bed of spikes, real speed -> 0.25x through the impact (33.95) -> real speed
    ("v_215609", 32.40, 33.85, 1.0, "p"), ("v_215609", 33.85, 34.35, 0.25, "p"), ("v_215609", 34.35, 35.60, 1.0, "p"),
    # TITLE over the team on stage
    ("v_215647", 1.0, 4.5, 1.0, "lt"),
    # the team introduces itself: "...Mahaguru Sri S Arumugam avargalin maanavargal"
    ("v_215647", 30.85, 33.95, 1.0, "l"),
    # BACKSTAGE - huddle, hands-in, MC "Thank you. Right after this we have the next performance."
    ("v_215627", 2.0, 5.0, 1.0, "p"), ("v_215630", 0.0, 3.1, 1.0, "p"), ("v_215629", 0.0, 1.3, 1.0, "p"), ("v_215628", 0.6, 4.6, 1.0, "p"),
    # salute "Vanakkam guru, vanakkam"
    ("v_213143", 0.0, 3.0, 1.0, "l"),
    # "Ready?" (audio J-cut from v_215603 0.0) over the wide stage
    ("v_215603", 26.5, 28.0, 1.0, "l"),
    # STICK DEMO - longer shots so each routine reads
    ("v_214108", 30.0, 30.0 + B4, 1.0, "l"), ("v_215535", 20.0, 20.0 + B4, 1.0, "l"), ("v_215638", 3.0, 3.0 + B4, 1.0, "l"),
    ("v_220303", 11.0, 11.0 + B4, 1.0, "l"), ("v_215604", 0.0, 1.0, 1.0, "l"), ("v_225612", 3.0, 3.0 + B4, 1.0, "l"),
    ("v_220311", 6.0, 6.0 + B4, 1.0, "l"), ("v_225535", 12.0, 12.0 + B4, 1.0, "l"), ("v_215638", 38.5, 38.5 + B4, 1.0, "l"),
    # BRICK - set-up, hammer, impact 24.0 in 0.25x, replay from the other angle (0.33x), aftermath
    ("v_215613", 6.5, 8.5, 1.0, "p"), ("v_215613", 21.5, 23.95, 1.0, "p"), ("v_215613", 23.95, 24.45, 0.25, "p"),
    ("v_225624", 28.3, 28.9, 0.33, "l"), ("v_215613", 24.45, 26.5, 1.0, "p"),
    # TEASE Part 2
    ("v_225554", 20.0, 20.6, 0.5, "l"), ("v_215617", 30.0, 33.6, 1.0, "p"),
]

PART2 = [
    # HOOK - watermelon, second angle (impact 19.45)
    ("v_225618", 17.80, 19.45, 1.0, "l"), ("v_225618", 19.45, 19.95, 0.25, "l"), ("v_225618", 19.95, 21.20, 1.0, "l"),
    # MC (Tamil) "...ungaludaiya aadharavu romba romba mukkiyam ... romba nandri", emcees "Let's go."
    ("v_213120", 1.0, 4.7, 1.0, "l"), ("v_215631", 0.0, 1.5, 1.0, "l"),
    # SELF-DEFENCE - takedowns and throws, longer holds, slow motion on the big ones
    ("v_225545", 5.5, 7.8, 1.0, "l"), ("v_225545", 7.8, 9.0, 0.4, "l"), ("v_225545", 9.0, 10.5, 1.0, "l"),
    ("v_225539", 9.0, 9.0 + B4, 1.0, "l"), ("v_225605", 11.0, 11.0 + B4, 1.0, "l"),
    ("v_225554", 17.8, 19.8, 1.0, "l"), ("v_225554", 19.8, 21.0, 0.4, "l"), ("v_225554", 21.0, 22.5, 1.0, "l"),
    ("v_225605", 26.0, 26.0 + B4, 1.0, "l"), ("v_225535", 46.0, 46.0 + B4, 1.0, "l"),
    # TEAMWORK - the human pyramid building up
    ("v_215617", 22.0, 32.0, 1.4, "p"),
    # CROWD + FINALE
    ("v_215619", 9.0, 13.0, 1.0, "p"), ("v_225626", 0.5, 5.0, 1.0, "l"), ("v_225628", 2.0, 6.5, 1.0, "l"),
    ("v_220303", 29.0, 29.0 + B4, 1.0, "l"),
    ("v_215627", 21.0, 25.0, 1.0, "p"),
]

ALL = ["v_213120", "v_213143", "v_214108", "v_215535", "v_215603", "v_215604", "v_215609", "v_215613", "v_215617", "v_215619",
       "v_215627", "v_215628", "v_215629", "v_215630", "v_215631", "v_215638", "v_215647", "v_220303", "v_220311", "v_225535",
       "v_225539", "v_225545", "v_225554", "v_225605", "v_225612", "v_225618", "v_225624", "v_225626", "v_225628"]
READY = ("part1", [i for i, s in enumerate(PART1) if s[0] == "v_215603"][0], "v_215603", 0.0, 0.40)


def timeline(segs):
    out, t = [], 0.0
    for c, a, b, sp, k in segs:
        d = round((b - a) / sp, 3); out.append(dict(clip=c, src_in=a, src_out=b, speed=sp, kind=k, out_start=round(t, 3), out_end=round(t + d, 3))); t += d
    return out, round(t, 3)


def check_coverage():
    used = {s[0] for s in PART1 + PART2}; return [c for c in ALL if c not in used]


def idx(part, clip, src_in):
    segs = PART1 if part == "part1" else PART2
    return [i for i, s in enumerate(segs) if s[0] == clip and abs(s[1] - src_in) < 1e-6][0]
