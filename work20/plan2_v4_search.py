# v02 Video 4 - Search List AA/SEC/F/008 (person searched, witness if present): every slide of the deck, in order.
import common20 as C
HOLDS_S = {(10, 0): 0.9, (13, 2): 0.6, (6, 1): 0.8, (6, 4): 0.4, (6, 5): 1.0, (7, 0): 0.8, (7, 1): 1.4, (7, 3): 0.8, (8, 0): 0.6, (8, 2): 0.6, (9, 0): 1.0, (11, 1): 1.0}
END_HOLD = 4.4
SEC, PER, WIT = "SECURITY", "PERSON SEARCHED", "WITNESS (IF PRESENT)"
o = lambda *r: C.orc("v4_search", 1, *r)
DET_O, PRES_O, ITEMS_O = o(150, 575, 1560, 810), o(150, 855, 1560, 1085), o(150, 1135, 1555, 1530)
ORIG = "ORIGINAL PAPER FORM"
REC = (167, 330, 443, 106)


def build(P, K):
    Shot, B, O, A = K["Shot"], K["BLUE"], K["ORANGE"], K["AMBER"]
    sp = C.spans(P, K); K["role"](0.0, SEC, B)
    C.title(P, K, 1, sp); C.changed(P, K, 2, sp, "orig-1.png"); C.steps(P, K, 3, sp, PER); C.need(P, K, 4, sp); C.part(P, K, 5, sp)
    # ---- slide 6: deck slide -> ORIGINAL form (Security fills) -> deck slide (signing order) -> ORIGINAL form (items) ----
    t0, t1 = sp[6]; s = C.lines(P, 6); a, b, c = P.L(s[1], -0.2), P.L(s[2], -0.2), P.L(s[5], -0.2)
    Shot(6, t0, a).hl(P.A(6, 0.3), (109.4, 253.4, 731.5, 782.9), a, "#5f6368").done()
    tf = P.W(s[1], "fills") - 0.2
    Shot("o-1", a, b).camfit(a + 0.6, o(150, 560, 1560, 1540), pad=1.04).hl(tf, DET_O, b, B).hl(tf + 0.4, PRES_O, b, B).hl(tf + 0.8, ITEMS_O, b, B).done()
    sh = Shot(6, b, c)
    sh.hl(P.W(s[2], "person") - 0.2, (960, 392, 880, 102), c, O).hl(P.W(s[2], "person") - 0.2, (565, 816, 250, 96), c, O)
    sh.hl(P.L(s[3], 0.1), (960, 522, 880, 102), c, O).hl(P.L(s[3], 0.1), (145, 816, 223, 96), c, O)
    sh.hl(P.L(s[4], 0.1), (960, 651, 880, 102), c, B).hl(P.L(s[4], 0.1), (145, 941, 351, 94), c, B).done()
    Shot("o-1", c, t1).camfit(P.L(s[5], 0.2), ITEMS_O, pad=1.15).hl(P.L(s[5], 0.3), ITEMS_O, t1, O).done()
    K["stage_label"](a, b, ORIG); K["stage_label"](c, t1, ORIG)
    # ---- slide 7: your turn -> scroll up: search details and items (original form) ----
    t0, t1 = sp[7]; s = C.lines(P, 7); to = P.W(s[0], "orange") - 0.3; ts = P.L(s[1], -0.2)
    K["handover"](t0, to, (SEC, B), (PER, O), "Security hands you the phone", t_move=t0 + 0.5); K["role"](t0 + 1.4, PER, O)
    Shot(7, to, ts).camfit(to + 0.6, (167, 330, 443, 134), pad=1.25, wmin=560).hl(to + 0.3, (167, 330, 443, 134), ts, O).done()
    sh = Shot("o-1", ts, t1)
    sh.camfit(ts + 0.4, o(150, 575, 1560, 1085), pad=1.1).hl(P.W(s[1], "search") - 0.2, DET_O, P.W(s[1], "items") - 0.2)
    sh.camfit(P.W(s[1], "items") - 0.4, ITEMS_O, pad=1.15).hl(P.W(s[1], "items") - 0.2, ITEMS_O, t1).done()
    K["stage_label"](ts, t1, ORIG)
    K["callout"](P.L(s[1]), P.L(s[2], -0.2), "On the phone, scroll up to see these details", "note")
    K["callout"](P.L(s[2]), P.L(s[3], -0.2), "‘Nil’ means nothing was found", "info")
    K["callout"](P.L(s[3]), t1, "Anything wrong? Tell Security before you sign", "warn")
    # ---- slide 8: sign, Clear, Confirm ----
    t0, t1 = sp[8]; s = C.lines(P, 8); sh = Shot(8, t0, t1)
    sh.camfit(P.L(s[0], 0.5), (167, 482, 443, 386), pad=1.12, wmin=620)
    sh.hl(P.W(s[0], "sign"), (181, 482, 416, 235), t1, O).ring(P.W(s[1], "tap"), (181, 727, 416, 56), P.L(s[2]), A).ring(P.W(s[2], "tap"), (167, 804, 443, 64), t1, A).done()
    # ---- slide 9: the witness (only if present) ----
    t0, t1 = sp[9]; s = C.lines(P, 9); tc = P.W(s[0], "check") - 0.2
    K["handover"](t0, tc, (PER, O), ("WITNESS", O), "If a witness is present", t_move=t0 + 0.5); K["role"](t0 + 1.4, WIT, O)
    sh = Shot(9, tc, t1)
    sh.cam(tc + 0.7, 389, 400, 580).cam(P.W(s[0], "tap") - 0.7, 389, 790, 580)
    sh.hl(tc + 0.3, REC, t1, O).ring(P.W(s[0], "tap"), (167, 777, 443, 65), t1, A).done()
    # ---- slides 10-13 ----
    C.last(P, K, 10, sp, PER); C.after_saved(P, K, 11, sp, (154, 561, 498, 174), (160, 686, 470, 42)); C.remember(P, K, 12, sp)
    C.where(P, K, 13, sp, pdf_label="Signed Search List<br>with Record ID", summary_steps=("Check the list", "Sign", "Confirm", "Hand back"))
    if C.WARN: print("WARN", *C.WARN, sep="\n  ")
