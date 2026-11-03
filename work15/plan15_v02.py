# v02 (creator: "add this song ... add that video at last ... remove the song of the video ... make sure the song beat and sound sync")
# Music: the creator-supplied song "Nimirndhu Nil" (Shankar Mahadevan, film Saroja 2008; music/nimirndhu_nil_creator_supplied.m4a).
#   125 bpm: beat 0.48005 s, bar 1.920 s. Its drop after the break (song 45.645 s) is the first frame of the video, so every
#   cut, card change, badge reveal and the grand total are placed on that beat grid.
# The creator's credits clip (VID-20261102-WA01232.mp4, 15 s: Mahaguru, masters, "Thanks for watching") closes the video; its own
#   song is removed - the supplied song plays under it and fades out at the end.
# Everything else (facts, photos, results) as v01 (plan15.py).
from plan15 import ZONES as _Z, OVERALL, HOOK_PHOTOS as _HP, CONGRATS, TALLY_BG
import copy
FPS = 30
MUSIC = "music/nimirndhu_nil_creator_supplied.m4a"; M = 45.645; MUSIC_FADE_IN = 0.02
BEAT = 0.48005; BAR = 4 * BEAT          # fitted on the song: grid within 5 ms of its beats over the whole 96 s
b = lambda n: round(BEAT * n, 3)                  # output time of beat n (beat 0 = the song's drop = 0.0 s)
DROP = b(64)                                      # results start (30.82)
bar = lambda k: round(DROP + BAR * k, 3)

CREDITS_T0 = b(168); CREDITS_DUR = 15.0
TOTAL = round(int((CREDITS_T0 + CREDITS_DUR) * FPS) / FPS, 4)
SEGS = [
    dict(id="hook_bout", clip="IMG_5215", src_in=22.55, t0=0.0, t1=b(4), speed=1.0, kind="p"),
    dict(id="hook_bg", clip="IMG_5221", src_in=2.0, t0=b(8), t1=b(12), speed=1.0, kind="bg"),
    # THE DAY (32 beats)
    dict(id="arena", clip="IMG_5233", src_in=0.2, t0=b(32), t1=b(36), speed=1.0, kind="p"),
    dict(id="athletes", clip="IMG_5206", src_in=2.0, t0=b(36), t1=b(40), speed=1.0, kind="p"),
    dict(id="march", clip="IMG_5212", src_in=2.9, t0=b(40), t1=b(44), speed=1.0, kind="p"),
    dict(id="honour", clip="IMG_5213", src_in=4.4, t0=b(44), t1=b(48), speed=1.0, kind="p"),
    dict(id="bout", clip="IMG_5215", src_in=8.0, t0=b(48), t1=b(54), speed=1.0, kind="p"),
    dict(id="bout_slow", clip="IMG_5215", src_in=12.15, t0=b(54), t1=b(60), speed=0.5, kind="p"),
    dict(id="bout2", clip="IMG_5215", src_in=18.6, t0=b(60), t1=b(64), speed=1.0, kind="p"),
    # RESULTS background
    dict(id="results_bg", clip="IMG_5221", src_in=0.0, t0=b(64), t1=b(116), speed=0.9, kind="bg"),
    # the creator's credits clip, untouched picture (scaled 576x1024 -> 1080x1920)
    dict(id="credits", clip="VID-20261102-WA01232", src_in=0.0, t0=CREDITS_T0, t1=TOTAL, speed=1.0, kind="raw"),
]
# hook photos on beats 4, 5.33.. -> one per beat + a third
HOOK_PHOTOS = [(_HP[0][0], b(4), b(5.33)), (_HP[1][0], b(5.33), b(6.67)), (_HP[2][0], b(6.67), b(8))]
CONGRATS_T0, CONGRATS_STEP = b(136), b(3)         # 8 photos, one every 3 beats -> to b(160)
SEC = dict(hook=(0.0, b(12)), poster=(b(12), b(32)), day=(b(32), DROP), results=(DROP, b(116)),
           tally=(b(116), b(136)), congrats=(b(136), b(160)), end=(b(160), CREDITS_T0), credits=(CREDITS_T0, TOTAL))
GT = b(124)                                       # grand total on a downbeat
ZONES = copy.deepcopy(_Z)
for z, (a, e) in zip(ZONES, [(64, 74), (74, 90), (90, 98), (98, 106), (106, 116)]): z["t0"], z["t1"] = b(a), b(e)
POSTER_LIFT_BEATS = (2, 3, 4, 5); POSTER_REGROUP_BEAT = 7
