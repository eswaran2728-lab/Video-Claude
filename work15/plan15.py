# Sepang team recap + congratulations - Kejohanan Silambam Antara Sekolah Tamil Peringkat Negeri Selangor 2026 (work15).
# 1080x1920, 30 fps. All times are OUTPUT seconds unless prefixed src_.
# Music: "Driving Ambition" (Ahjay Stelino, Mixkit #32, Mixkit Stock Music Free License), ~99.4 bpm (beat 0.604 s, bar 2.416 s).
# The track's drop (music 38.46 s) is placed on the start of the RESULTS (output 25.00 s) -> music offset M = 13.46 s;
# its outro (music 86.9 s) lands on the end card (output ~73.4 s).
# Facts used (creator's brief + poster only): results per zone/school, totals (0 gold, 4 silver, 9 bronze, 13 medals), team name
# "Persatuan Silambam Malaysia Daerah Sepang", poster wording (tournament, organiser, date, time, venue, Tamil slogan).
FPS = 30
BEAT = 0.604; BAR = 4 * BEAT; M = 13.46
DROP = 25.0
bar = lambda k: round(DROP + BAR * k, 3)          # downbeats: bar(-10)=0.84 ... bar(0)=25.0 ... bar(20)=73.32

# ---- video segments (pre-rendered by render15.py) ----
# kind 'p' portrait cover; 'l' landscape band over its own blurred copy; 'bg' blurred dark background copy
SEGS = [
    # HOOK
    dict(id="hook_bout", clip="IMG_5215", src_in=22.55, t0=0.0, t1=1.81, speed=1.0, kind="p"),
    dict(id="hook_bg", clip="IMG_5221", src_in=2.0, t0=3.62, t1=5.67, speed=1.0, kind="bg"),
    # THE DAY
    dict(id="arena", clip="IMG_5233", src_in=0.2, t0=15.34, t1=17.15, speed=1.0, kind="p"),  # landscape crowd pan: cover crop fills the frame with the crowd
    dict(id="athletes", clip="IMG_5206", src_in=2.0, t0=17.15, t1=18.96, speed=1.0, kind="p"),
    dict(id="march", clip="IMG_5212", src_in=2.9, t0=18.96, t1=20.17, speed=1.0, kind="p"),
    dict(id="bout", clip="IMG_5215", src_in=8.0, t0=20.17, t1=22.58, speed=1.0, kind="p"),
    dict(id="bout_slow", clip="IMG_5215", src_in=12.15, t0=22.58, t1=25.0, speed=0.5, kind="p"),
    # RESULTS background (podium presentations, blurred under the cards)
    dict(id="results_bg", clip="IMG_5221", src_in=0.0, t0=25.0, t1=49.16, speed=0.93, kind="bg"),
]

# ---- photos (HTML <img>, slow push) ----
HOOK_PHOTOS = [("adaad1cb-2ee5-4d85-bbe1-3d5def406c5b", 1.81, 2.42), ("b5152ecb-182d-4fd1-be68-7b6ba654ad2d", 2.42, 3.02),
               ("ce147f4f-1916-4cbf-9fa8-b77cd67e7ada", 3.02, 3.62)]
TALLY_BG = "IMG_6655"
CONGRATS = [("adaad1cb-2ee5-4d85-bbe1-3d5def406c5b", 0.5), ("b5152ecb-182d-4fd1-be68-7b6ba654ad2d", 0.5),
            ("ce147f4f-1916-4cbf-9fa8-b77cd67e7ada", 0.5), ("2ba105e8-7080-4913-8bf5-05505fd29650", 0.5),
            ("e490e7c9-2dde-4a91-94d0-7e565aa5268d", 0.5), ("0d27d5ad-f8f5-4fb0-96c7-8590a772ffd4", 0.5),
            ("IMG_6667", 0.5), ("IMG_5223", 0.5)]          # (photo, focus x 0..1)
CONGRATS_T0, CONGRATS_STEP = bar(14), 3 * BEAT           # 58.82, one photo every 3 beats -> 8 photos to 73.32

# ---- sections ----
SEC = dict(hook=(0.0, bar(-8)), poster=(bar(-8), bar(-4)), day=(bar(-4), DROP), results=(DROP, bar(10)),
           tally=(bar(10), bar(14)), congrats=(bar(14), bar(20)), end=(bar(20), 80.0))
TOTAL = 80.0

# ---- results (creator's brief, exact) ----
ZONES = [
    dict(name="SUNGAI PELEK", schools=[("SJK(T) Ladang Ijok", 0, 1), ("SJK(T) Teluk Merbau", 0, 1), ("SJK(T) Sepang", 0, 0)],
         total=(0, 0, 2), t0=DROP, t1=bar(2)),
    dict(name="DENGKIL", schools=[("SJK(T) Dengkil", 0, 0), ("SJK(T) Ladang Ampar Tenang", 0, 0), ("SJK(T) Taman Permata", 2, 3)],
         total=(0, 2, 3), t0=bar(2), t1=bar(5)),
    dict(name="BBST", schools=[("SJK(T) BBST", 0, 1)], total=(0, 0, 1), t0=bar(5), t1=round(bar(5) + 6 * BEAT, 3)),
    dict(name="WEST COUNTRY", schools=[("SJK(T) West Country Timur", 0, 2)], total=(0, 0, 2), t0=round(bar(5) + 6 * BEAT, 3), t1=bar(8)),
    dict(name="BANGI", schools=[("SJK(T) Bangi", 2, 1)], total=(0, 2, 1), t0=bar(8), t1=bar(10)),
]                                                        # school tuple: (name, silver, bronze); no school won gold
OVERALL = dict(gold=0, silver=4, bronze=9, total=13)
assert sum(z["total"][1] for z in ZONES) == OVERALL["silver"] and sum(z["total"][2] for z in ZONES) == OVERALL["bronze"]
assert all(sum(s[1] for s in z["schools"]) == z["total"][1] and sum(s[2] for s in z["schools"]) == z["total"][2] for z in ZONES)
