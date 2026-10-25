# Edit decision list (source clip, in, out) -> output timeline. Shooting order by creation time: d67f 08:18, e5dd 08:20,
# b5ae 08:22, a336 08:24 (filenames are hashes). Speech is Tamil with English keywords; captions are English
# translations that keep his own English words (quality / cheap / fast / choose / drop).
# Cut: b5ae 0-4.8 (greeting/setup), the repeated pair statements b5ae 13.7-25.8 ("similarly..." / "another option..."
# say the QUALITY+CHEAP case again), the 4 s pause at b5ae 34.3-39.8, "fun fact" + "my opinion" b5ae 51-60 (said
# again in a336), d67f 2.4-16.9 (garbled "business luxury" line), e5dd 10.7-14.8 (the choose-two rule, already in the
# hook), a336 0-2.2 (false start) and a336 7.7-18.4 (an unclear cheap+quality DM line that, as transcribed, would
# contradict the rule; plus a second "comment below").
SEG = [  # (clip, in, out, role)
    ("b5ae", 4.82, 7.72, "hook: of these three you can only choose two"),
    ("d67f", 0.00, 2.38, "okay guys, here's a diagram"),
    ("e5dd", 0.00, 4.38, "this is quality, cheap and fast - a psychology"),
    ("e5dd", 5.15, 10.68, "you're buying a product: remember these three"),
    ("b5ae", 7.72, 13.72, "quality + cheap -> won't come fast"),
    ("b5ae", 25.85, 34.28, "use it for every product; with me: choose two, drop one"),
    ("b5ae", 39.82, 51.15, "quality + fast -> not cheap; fast + cheap -> not quality"),
    ("a336", 2.25, 7.72, "takeaway: my ideology; comment below"),
]
GAP = 0.0
OUT, t = [], 0.0
for clip, a, b, role in SEG:
    OUT.append((round(t, 3), round(t + b - a, 3), clip, a, b)); t += b - a + GAP
SPEECH_END = round(t, 3)
TOTAL = round(SPEECH_END + 2.2, 3)              # end card
def out_of(i, src_t):                            # source time inside segment i -> output time
    return round(OUT[i][0] + (src_t - OUT[i][3]), 3)
