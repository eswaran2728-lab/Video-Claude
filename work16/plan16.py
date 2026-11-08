# Edit plan v01 — Eshan Creations "3D wall frame art → key holder with lamps" reel.
# Single source of truth: segments (source in/out → output timeline), zoom keyframes, captions, sound cues.
# Sources: M = src/drive/IMG_6792.MOV (iPhone 16 Pro Max, 4K ProRes HLG, 46.0 s, unlit frame + creator's Tamil voice)
#          L = src/drive/fa799ce5e58a49c29107dcd042ded275.mp4 (720x1280 HEVC, 29.4 s, lamps being switched on + voice)
# All times are seconds; output times are snapped to 30 fps frames.
import os
FPS = 30
f = lambda t: int(round(t * FPS))
VERSION = os.environ.get("VERSION", "v03")   # v01/v02 = reviewed versions; v03 = clean voice + cinematic finish

# (name, source, src_in, src_out, speed, voice)  voice: True = the clip's own sound, or (src, in, out) to lay other audio
SEGS = [
    ("hook",   "L", 19.00, 21.60, 0.85, ("M", 2.26, 5.32)),   # lit frame (flash-forward) under "Okay guys, quick review"
    ("story",  "M",  5.70, 23.40, 1.0, True),                 # wall frame art → just a frame → customer → key holder, 5 hooks
    ("howto",  "M", 40.10, 42.42, 1.0, True),                 # "how do you use it? see this lamp"
    ("reveal", "L",  3.22,  7.38, 1.0, True),                 # "hold the lamp, turn it here — it turns on" (lamp 1 lights)
    ("glow",   "L", 25.78, 27.14, 1.0, False),                # fully lit, no voice: music swell / breathing room
    ("cta",    "L", 21.60, 25.78, 1.0, True),                 # "want one like this for your home? follow me"
    ("bye",    "L", 27.66, 28.70, 1.0, True),                 # "okay bye, thank you"
    ("end",    "L", 28.70, 29.30, 1.0, False),                # last lit frames, then freeze under the end card
]
END_FREEZE = 2.4
if VERSION >= "v03":
    SEGS[4] = ("glow", "L", 25.78, 27.14, 0.7, False)        # slow-motion hold on the lit frame (frame-blended)

OUT = []; t = 0
for name, src, a, b, sp, vo in SEGS:
    n = f((b - a) / sp)
    OUT.append(dict(name=name, src=src, a=a, b=b, speed=sp, vo=vo, o0=t / FPS, o1=(t + n) / FPS, n=n)); t += n
NF = t + f(END_FREEZE); TOTAL = NF / FPS
S = {s["name"]: s for s in OUT}

def out_t(seg, src_t):
    s = S[seg]; return s["o0"] + (src_t - s["a"]) / s["speed"]

# Zoom keyframes per segment: (src time, Z, cx, cy, ease-to-this-key) in 1080x1920 output space of the full source frame.
# ease: "hold" = jump (hard punch cut), "lin", "io" (ease in-out)
ZOOM = {
    "hook":   [(19.00, 1.00, 540, 900, "hold"), (21.60, 1.07, 540, 880, "lin")],
    "story":  [(5.70, 1.00, 540, 960, "hold"), (11.30, 1.12, 540, 900, "lin"),           # slow push: "3D wall frame art"
               (11.34, 1.00, 540, 960, "hold"), (14.70, 1.00, 540, 960, "hold"),         # wide + still: "just a frame"
               (14.72, 1.26, 540, 960, "hold"), (18.50, 1.30, 540, 950, "lin"),          # punch: close on the faces while "a customer messaged me"
               (18.56, 1.00, 540, 960, "hold"), (19.35, 1.00, 540, 960, "hold"),         # wide while the frame is lowered
               (19.95, 1.12, 590, 1000, "io"), (20.70, 1.12, 600, 1000, "lin"),          # push in to the 5 key hooks,
               (21.40, 1.12, 580, 1010, "lin"), (22.00, 1.12, 530, 1010, "lin"),         # panning with the hand-held frame
               (22.50, 1.12, 500, 1010, "lin"), (23.40, 1.12, 500, 1010, "lin")],
    "howto":  [(40.10, 1.06, 540, 940, "hold"), (42.42, 1.12, 540, 900, "lin")],         # lamps + faces in view
    "reveal": [(3.22, 1.08, 540, 900, "hold"), (6.55, 1.08, 540, 900, "hold"), (7.05, 1.00, 540, 960, "io"), (7.38, 1.00, 540, 960, "hold")],
    "glow":   [(25.78, 1.00, 540, 960, "hold"), (27.14, 1.05, 540, 940, "lin")],
    "cta":    [(21.60, 1.12, 540, 1063, "hold"), (25.78, 1.14, 540, 1070, "lin")],     # framed low so faces clear the caption
    "bye":    [(27.66, 1.14, 540, 1070, "hold"), (28.70, 1.15, 540, 1075, "lin")],
    "end":    [(28.70, 1.15, 540, 1075, "hold"), (29.30, 1.16, 540, 1078, "lin")],
}

if VERSION >= "v03":                                          # cinematic: smooth eased moves instead of hard punch cuts
    ZOOM["story"] = [(5.70, 1.00, 540, 960, "hold"), (11.30, 1.12, 540, 900, "lin"),   # slow push: "3D wall frame art"
                     (11.85, 1.00, 540, 960, "io"), (14.70, 1.03, 540, 955, "lin"),    # ease back + drift: "just a frame"
                     (15.35, 1.26, 540, 960, "io"), (18.40, 1.30, 540, 950, "lin"),    # ease in to the faces: "a customer messaged me"
                     (19.00, 1.00, 540, 960, "io"), (19.35, 1.00, 540, 960, "hold")] + ZOOM["story"][8:]

# Hook layout: the lit frame as a rounded card (scale HOOK_CARD of the full frame, top-left at HOOK_XY) on a blurred,
# darkened copy of itself, leaving the top band for the title so no text covers the faces.
HOOK_CARD, HOOK_XY = 0.67, (178, 636)

# Grade (ffmpeg): M tone-mapped HLG → SDR needs contrast + colour; L gets a small cool-cast reduction.
CURVE = "curves=all='0/0.01 0.25/0.235 0.5/0.5 0.75/0.77 1/1'"
GRADE = {"M": f"eq=contrast=1.06:saturation=1.10,{CURVE},unsharp=5:5:0.30",
         "L": f"colorbalance=rm=0.02:bm=-0.04:rh=0.01:bh=-0.05,eq=contrast=1.05:saturation=1.04,{CURVE},unsharp=5:5:0.25"}

# v03 film look on top (RGB): warm highlights / cool shadows, lifted blacks + soft roll-off, warm halation on the
# bright parts (lamps, gold), vignette, fine moving grain.
FILM = ("eq=saturation=0.96,format=gbrp,colorbalance=rs=-0.015:bs=0.025:rh=0.035:gh=0.012:bh=-0.035,"
        "curves=all='0/0.035 0.15/0.125 0.5/0.5 0.85/0.875 1/0.965',split[a][b];[b]curves=all='0/0 0.62/0 1/1',gblur=sigma=22,"
        "colorchannelmixer=rr=1:gg=0.78:bb=0.5[g];[a][g]blend=all_mode=screen:all_opacity=0.38,vignette=angle=PI/4.6,noise=alls=6:allf=t")
if VERSION >= "v03":
    GRADE = {k: v + "," + FILM for k, v in GRADE.items()}

# Captions: English meaning of the creator's Tamil-English speech (his English words kept). (seg, src_in, src_out, text)
# *word* = gold emphasis; optional 5th field "top" puts the caption in the top band.
CAPS = [
    ("story",  5.70,  7.46, "This is our wall frame"),
    ("story",  7.46, 11.34, "we call it *3D wall frame art*"),
    ("story", 11.62, 14.70, "This was just a frame"),
    ("story", 14.98, 18.56, "A customer messaged me"),
    ("story", 18.80, 20.66, "They wanted a *key holder*"),
    ("story", 20.66, 23.40, "See — it holds *5 keys*"),
    ("howto", 40.10, 42.42, "How to use it? See this *lamp*", "top"),   # frame held low here: faces sit in the caption band
    ("reveal", 3.22,  5.96, "Hold the lamp, turn it here…"),
    ("reveal", 5.96,  7.38, "…and it *turns on*"),
    ("cta",   21.62, 25.78, "Want one for your home? You can *follow me*"),
    ("bye",   27.66, 29.30, "Okay, bye — thank you!"),
]

REVEAL_SRC = 6.90          # first frame where the lit frame is clearly visible after the hand moves away (L)
HOOKS_SRC = (20.70, 22.95) # numbered tags pop on the 5 key hooks while he says "anju key hold" (M)
