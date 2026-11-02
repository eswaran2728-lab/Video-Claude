# Silambam @ Festival Kesenian & Kebudayaan Malaysia 2026 — two-part highlight reel (9:16, 30 fps).
# Source: the creator's WeTransfer zip of WhatsApp exports (src/wa -> 30 fps working copies in src/norm). Every one of the 29
# videos is used at least once across the two parts (check_coverage()). Times are SOURCE seconds in src/norm/<clip>.mp4.
# Segment = (clip, src_in, src_out, speed, kind) ; speed < 1 = interpolated slow motion ; kind: 'p' portrait full frame,
# 'l' landscape band (zoomed band over a blurred copy), 'lt' landscape title background (blurred, darker).
# Beat grid: music "Epical Drums 02" (Mixkit #677) ~80.75 BPM -> beat 0.743 s; montage cuts are 1 or 2 beats long.
BEAT = 0.743

PART1 = [
    # HOOK - watermelon smashed on a man lying on a bed of spikes (portrait angle), impact at 33.95
    ("v_215609", 33.20, 33.85, 1.0, "p"), ("v_215609", 33.85, 34.35, 0.25, "p"), ("v_215609", 34.35, 34.95, 1.0, "p"),
    # TITLE card over the team lined up on stage
    ("v_215647", 1.0, 4.0, 1.0, "lt"),
    # BACKSTAGE - line-up, huddle, hands-in cheers
    ("v_215627", 3.0, 4.6, 1.0, "p"), ("v_215630", 0.3, 1.8, 1.0, "p"), ("v_215629", 0.0, 1.3, 1.0, "p"),
    # MC (off-screen, English): "Thank you. Right after this we have the next performance." over the backstage line-up
    ("v_215628", 0.6, 4.6, 1.0, "p"),
    # "Vanakkam guru, vanakkam" - the salute (their own audio)
    ("v_213143", 0.0, 2.0, 1.0, "l"),
    # FAST DEMO - stick sparring, cut on the beat
    ("v_215603", 26.5, 26.5 + BEAT, 1.0, "l"),                      # picture: wide stage; audio "Ready?" from 0.0 (mix13 READY)
    ("v_214108", 30.5, 30.5 + 2 * BEAT, 1.0, "l"), ("v_215535", 21.0, 21.0 + BEAT, 1.0, "l"), ("v_215638", 4.0, 4.0 + 2 * BEAT, 1.0, "l"),
    ("v_220303", 12.0, 12.0 + BEAT, 1.0, "l"), ("v_215535", 38.0, 38.0 + 2 * BEAT, 1.0, "l"), ("v_225612", 4.0, 4.0 + BEAT, 1.0, "l"),
    ("v_215638", 33.0, 33.0 + 2 * BEAT, 1.0, "l"), ("v_220311", 7.0, 7.0 + BEAT, 1.0, "l"), ("v_225535", 13.0, 13.0 + 2 * BEAT, 1.0, "l"),
    ("v_214108", 44.0, 44.0 + BEAT, 1.0, "l"), ("v_215604", 0.0, BEAT, 1.0, "l"),
    ("v_215638", 39.5, 39.5 + 2 * BEAT, 1.0, "l"), ("v_220303", 40.0, 40.0 + BEAT, 1.0, "l"), ("v_225612", 15.0, 15.0 + 2 * BEAT, 1.0, "l"),
    # BRICK - concrete block on a man's head, hammer, impact at 24.0 (portrait) + replay from the other angle (impact ~28.6)
    ("v_215613", 6.5, 8.5, 1.0, "p"), ("v_215613", 22.6, 23.95, 1.0, "p"), ("v_215613", 23.95, 24.45, 0.25, "p"),
    ("v_225624", 28.3, 28.9, 0.33, "l"), ("v_215613", 24.45, 26.0, 1.0, "p"),
    # TEASE Part 2 - a throw, then the human-pyramid pose under the "Part 2" card
    ("v_225554", 20.0, 20.6, 0.5, "l"), ("v_215617", 30.0, 32.4, 1.0, "p"),
]

PART2 = [
    # HOOK - the watermelon from the second camera angle, impact at 19.45
    ("v_225618", 18.6, 19.45, 1.0, "l"), ("v_225618", 19.45, 19.95, 0.25, "l"), ("v_225618", 19.95, 20.6, 1.0, "l"),
    # MC in Tamil: "...ungaludaiya aadharavu romba romba mukkiyam ... romba nandri"; then "Let's go." from the emcees
    ("v_213120", 1.0, 4.7, 1.0, "l"), ("v_215631", 0.0, 1.5, 1.0, "l"),
    # SELF-DEFENCE - takedowns and throws, slow motion on the big ones
    ("v_225545", 6.6, 7.8, 1.0, "l"), ("v_225545", 7.8, 9.0, 0.4, "l"),
    ("v_225539", 10.0, 10.0 + 2 * BEAT, 1.0, "l"), ("v_225605", 12.0, 12.0 + 2 * BEAT, 1.0, "l"),
    ("v_225554", 18.8, 19.8, 1.0, "l"), ("v_225554", 19.8, 21.0, 0.4, "l"), ("v_225554", 21.0, 21.8, 1.0, "l"),
    ("v_225605", 27.0, 27.0 + 2 * BEAT, 1.0, "l"), ("v_225535", 47.0, 47.0 + 2 * BEAT, 1.0, "l"), ("v_220303", 30.0, 30.0 + 2 * BEAT, 1.0, "l"),
    # TEAMWORK - the human-pyramid pose (portrait), sped up a little
    ("v_215617", 25.0, 33.0, 1.6, "p"),
    # CROWD + FINALE
    ("v_215619", 9.5, 12.5, 1.0, "p"), ("v_225626", 1.0, 4.0, 1.0, "l"), ("v_225628", 3.0, 5.5, 1.0, "l"),
    ("v_215627", 22.0, 25.0, 1.0, "p"),
]

ALL = ["v_213120", "v_213143", "v_214108", "v_215535", "v_215603", "v_215604", "v_215609", "v_215613", "v_215617", "v_215619",
       "v_215627", "v_215628", "v_215629", "v_215630", "v_215631", "v_215638", "v_215647", "v_220303", "v_220311", "v_225535",
       "v_225539", "v_225545", "v_225554", "v_225605", "v_225612", "v_225618", "v_225624", "v_225626", "v_225628"]


def timeline(segs):
    out, t = [], 0.0
    for c, a, b, sp, k in segs:
        d = round((b - a) / sp, 3); out.append(dict(clip=c, src_in=a, src_out=b, speed=sp, kind=k, out_start=round(t, 3), out_end=round(t + d, 3))); t += d
    return out, round(t, 3)


def check_coverage():
    used = {s[0] for s in PART1 + PART2}; missing = [c for c in ALL if c not in used]
    return missing

# Spoken lines laid onto the timeline independently of the picture (J-cuts): (part, segment index it starts with, clip, src_in, src_out)
READY = ("part1", 9, "v_215603", 0.0, 0.40)
