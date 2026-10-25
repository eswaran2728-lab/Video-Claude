# Edit decision list for the AVSEC keychain reel. All "out" times are on the output timeline (s, 30 fps).
# Speech (Tamil) segments, cut on the quietest point between sentences:
SPEECH = [  # (src clip, src_in, src_out)
    ("IMG_6358", 0.13, 7.80),    # "In the company I work at, I needed 50 keychains as a giveaway."
    ("IMG_6358", 8.45, 14.80),   # "So I designed all of these, multi-colour keychains for them."
    ("IMG_6358", 14.88, 19.94),  # "As you can see, every keychain here comes in 3 colours: red, black and white."
    ("3437BABC", 6.10, 12.86),   # "I've done the design and packaging. As soon as possible, I'll deliver them to you."
    ("IMG_6358", 35.05, 41.40),  # "If you want bulk orders like this, contact me or DM me."
]
# cut: 6358 20.0-34.8 (where he works - transcription uncertain; repeats the giveaway point), 6358 42-44.8
# ("Claude, later cut this one"), 3437 0-6.1 (repeats "50 pieces") and 3437 12.9-21.5 (second CTA; the 4K one is used)
OUT = []; t = 0.0
for clip, a, b in SPEECH:
    OUT.append((t, t + (b - a), clip, a, b)); t += b - a
SPEECH_END = round(t, 3)
TOTAL = round(SPEECH_END + 3.3, 3)
def out_of(seg, src):  # output time of a source time inside speech segment `seg`
    o, _, _, a, _ = OUT[seg]; return round(o + (src - a), 3)

# Visual track: (id, layout, clip, src_in, out_start, out_end, note)
V = [
    ("V1",  "proof", "IMG_6351", 0.00, 0.0,  2.30, "hook: build plate slides out, full of red AVSEC planes"),
    ("V2",  "face",  "IMG_6358", 2.43, 2.30, OUT[0][1], "speaker: 50 keychains for a company giveaway"),
    ("V3",  "proof", "IMG_6352", 0.40, OUT[1][0], OUT[1][0] + 3.03, "flexing the plate: prints pop off"),
    ("V4",  "split", "IMG_6352", 3.43, OUT[1][0] + 3.03, OUT[1][1], "split: pieces drop onto the mat / speaker"),
    ("V5",  "proof", "IMG_6353", 0.30, OUT[2][0], OUT[2][0] + 2.98, "box of keychains poured out (red + black)"),
    ("V6",  "proof", "IMG_6351", 3.40, OUT[2][0] + 2.98, OUT[2][1], "macro: red body, black outline, white AVSEC print"),
    ("V7",  "proof", "IMG_6356", 0.00, OUT[3][0], OUT[3][0] + 2.75, "a packed keychain held to camera"),
    ("V8",  "proof", "IMG_6357", 0.60, OUT[3][0] + 2.75, OUT[3][1], "rows of packed keychains"),
    ("V9",  "proof", "IMG_6354", 0.00, OUT[4][0], OUT[4][0] + 2.36, "the whole batch on the table: bulk"),
    ("V10", "face",  "IMG_6358", 35.05 + 2.36, OUT[4][0] + 2.36, OUT[4][1], "speaker CTA: contact / DM"),
    ("V11", "proof", "IMG_6359", 0.00, SPEECH_END, SPEECH_END + 0.83, "whip blur into the end card"),
    ("V12", "end",   "3437BABC", 0.30, SPEECH_END + 0.83, TOTAL, "end card over the keychain shake"),
]
