# work21 v01 plan: Silambam at Majlis Perasmian Hari Sukan Negara, Peringkat Daerah Sepang 2026 (15.11.2026, UniKL MIAT Dengkil).
# Source -> output timing map. Output is locked to the music: "Driving Ambition" (Mixkit #32) at 99.38 BPM, started at
# 29.08 s into the track so its drop (track 38.74 s, beat 64) lands on output beat 16 and its outro (track 87.04 s) on beat 96.
BPM = 99.38
B = 60 / BPM                      # one beat = 0.6037 s
MUSIC_IN = 29.08                  # track time at output 0
def b(k): return round(k * B, 3)  # output seconds of beat k

# ---- video plate segments: clip, source in (s), output beats [k0, k1), speed, zoom (follow-crop on the tracked performer) ----
SEGS = [
    # HOOK (beats 0-8)
    dict(id="h1", clip="IMG_1921", src=5.20, k0=0, k1=2),            # jump kick into a floor move
    dict(id="h2", clip="IMG_1921", src=18.40, k0=2, k1=4),           # jumping spin
    dict(id="h3", clip="IMG_1921", src=41.45, k0=4, k1=8),           # rises from the floor: the shout, stick overhead (SILAMBAM slams in)
    # CONTEXT (beats 8-16): the boy on stage in front of the event banner, full frame
    dict(id="c1", clip="IMG_1918", src=0.00, k0=8, k1=16),
    # PERFORMANCES (beats 16-40), the music's drop on beat 16
    dict(id="p1", clip="IMG_1921", src=12.40, k0=16, k1=20),         # low-stance strikes
    dict(id="p2", clip="IMG_1918", src=15.40, k0=20, k1=24, zoom=1.45),   # overhead swings, follow-crop
    dict(id="p3", clip="IMG_1921", src=25.40, k0=24, k1=28),         # overhead swing into a lunge
    dict(id="p4", clip="IMG_1921", src=18.80, k0=28, k1=32, speed=0.5),   # the jumping spin again, half speed
    dict(id="p5", clip="IMG_1918", src=22.20, k0=32, k1=36, zoom=1.45),   # low-stance finish
    dict(id="p6", clip="IMG_1921", src=35.00, k0=36, k1=40),         # kneeling stick salute
    # PAYOFF: the medal group on stage (beats 80-88)
    dict(id="g1", clip="IMG_2025", src=0.30, k0=80, k1=88),
]

# ---- photos (HTML layer). mode 'cover' = 9:16 crop at focus fx (0..1 across the 3:4 photo); 'card' = whole photo, full width ----
PRESENT = [("094", 2, "cover", .62), ("093", 3, "card", .5), ("095", 2, "cover", .40), ("096", 3, "cover", .60), ("006", 2, "cover", .50),
           ("010", 2, "cover", .58), ("027", 2, "cover", .45), ("028", 2, "cover", .50), ("029", 2, "cover", .50), ("044", 2, "cover", .52),
           ("050", 2, "cover", .50), ("052", 2, "cover", .55), ("097", 2, "cover", .50), ("099", 4, "cover", .45)]
PHOTOS, k = [], 40
for pid, nb, mode, fx in PRESENT:
    PHOTOS.append(dict(id=pid, k0=k, k1=k + nb, mode=mode, fx=fx)); k += nb
assert k == 72, k
PHOTOS += [dict(id="041", k0=72, k1=76, mode="card", fx=.5), dict(id="076", k0=76, k1=80, mode="card", fx=.5)]
END_BG = "077"                      # blurred group photo behind the end card
K_END = 88                          # end card from beat 88
TOTAL = 61.0                        # music outro (beat 96 = 57.96 s) decays, faded out by 61 s

# ---- on-screen text (exact banner wording; nothing beyond what the media shows) ----
EVENT_SMALL = "MAJLIS PERASMIAN"
EVENT_BIG = ["HARI", "SUKAN", "NEGARA"]
EVENT_SUB = "PERINGKAT DAERAH SEPANG 2026"
EVENT_DATE = "15 NOVEMBER 2026 (AHAD)"
EVENT_VENUE = "UNIKL MIAT, DENGKIL"
TAG = "HARI SUKAN NEGARA · SEPANG 2026"
