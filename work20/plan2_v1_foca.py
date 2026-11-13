# v02 Video 1 - FOCA Checklist (AA/SEC/F/070), Airline Representative: every slide of the deck, in order.
import common20 as C
HOLDS_S = {(11, 0): 0.9, (14, 2): 0.6, (6, 1): 1.4, (6, 2): 0.6, (6, 3): 0.6, (7, 0): 1.1, (7, 1): 0.8, (8, 0): 0.8, (8, 1): 1.2, (8, 3): 1.4, (9, 0): 0.6, (9, 1): 0.8, (10, 2): 0.8, (12, 1): 1.0}
END_HOLD = 4.2
SEC, REP = "SECURITY", "AIRLINE REPRESENTATIVE"


def build(P, K):
    Shot, B, O, A = K["Shot"], K["BLUE"], K["ORANGE"], K["AMBER"]
    sp = C.spans(P, K); K["role"](0.0, SEC, B)
    C.title(P, K, 1, sp); C.changed(P, K, 2, sp, "orig-1.png"); C.steps(P, K, 3, sp, REP); C.need(P, K, 4, sp); C.part(P, K, 5, sp)
    # ---- slide 6: the paper form we used (deck slide -> the ORIGINAL form, page 1 and page 2 -> deck slide) ----
    t0, t1 = sp[6]; s = C.lines(P, 6); o = lambda pg, *r: C.orc("v1_foca", pg, *r); t2 = P.E(s[1], 0.6)
    Shot(6, t0, P.L(s[1], -0.2)).hl(P.A(6, 0.3), (95, 347, 839.5, 597), P.L(s[1], -0.2), "#5f6368").hl(P.A(6, 0.3), (995, 347, 839.5, 597), P.L(s[1], -0.2), "#5f6368").done()
    sh = Shot("o-1", P.L(s[1], -0.2), t2)
    sh.hl(P.W(s[1], "fills") - 0.2, o(1, 195, 445, 2145, 637), t2, B).hl(P.W(s[1], "fills") + 0.3, o(1, 195, 688, 2145, 1358), t2, B).done()
    sh = Shot("o-2", t2, P.L(s[3], -0.2))
    sh.hl(t2 + 0.3, o(2, 195, 508, 2210, 866), P.L(s[2], 0.2), B)
    sh.camfit(P.L(s[2], 0.2), o(2, 150, 880, 2210, 1240), pad=1.05)
    sh.hl(P.W(s[2], "security") - 0.1, o(2, 185, 1070, 515, 1165), P.L(s[3], -0.2), B).hl(P.W(s[2], "airline") - 0.1, o(2, 1690, 1070, 2015, 1165), P.L(s[3], -0.2), O).done()
    K["stage_label"](P.L(s[1], -0.2), P.L(s[3], -0.2), "ORIGINAL PAPER FORM")
    sh = Shot(6, P.L(s[3], -0.2), t1).hl(P.L(s[3], 0.2), (1590, 716, 216, 104), t1, O).hl(P.L(s[3], 0.2), (612, 993, 802, 63), t1, O)
    sh.chip(P.L(s[3], 0.4), 1430, 836, "Airline Rep signs here", O, t1, 38).done()
    # ---- slide 7: Security hands you the phone -> tap the orange button ----
    t0, t1 = sp[7]; s = C.lines(P, 7); th = P.W(s[0], "hands") - 0.2
    Shot(7, t0, th).done()
    K["handover"](th, P.L(s[1], -0.2), (SEC, B), (REP, O), "Security hands you the phone", t_move=th + 0.4); K["role"](th + 1.4, REP, O)
    sh = Shot(7, P.L(s[1], -0.2), t1)
    sh.cam(P.L(s[1], -0.2), 389, 600, 640).ring(P.W(s[1], "tap"), (149.7, 587.2, 478.1, 78.0), t1, A).done()
    # ---- slide 8: check the details ----
    t0, t1 = sp[8]; s = C.lines(P, 8); sh = Shot(8, t0, P.L(s[3], -0.2))
    sh.camfit(P.L(s[0], 0.4), (175, 265, 430, 165), pad=1.25, wmin=520).hl(P.L(s[0], 0.4), (180.8, 272.7, 416.1, 148.8), P.L(s[1], 0.2))
    sh.cam(P.L(s[1], 0.1), 390, 700, 760).hl(P.L(s[1], 0.4), (168, 430, 445, 555), P.L(s[2], -0.2))
    sh.cam(P.L(s[2], -0.3), 960, 540, 1920).hl(P.L(s[2], 0.1), P.txt(8, "Flight details and each line"), P.L(s[3], -0.2)).done()
    K["callout"](P.L(s[2]), t1, "‘Something is wrong’: not shown in deck screenshot", "note")
    K["handover"](P.L(s[3], -0.2), t1, (REP, O), (SEC, B), "Something wrong? The phone goes back to Security", t_move=P.L(s[3], 0.4))
    # ---- slide 9: type your name and ID, then sign ----
    t0, t1 = sp[9]; s = C.lines(P, 9); sh = Shot(9, t0, t1)
    sh.camfit(P.L(s[0], 0.6), (150, 378, 478, 80), pad=1.15, wmin=560)
    sh.hl(P.W(s[0], "name") - 0.1, (157, 386, 230, 63), P.L(s[1]), O).hl(P.W(s[0], "id") - 0.1, (390, 386, 232, 63), P.L(s[1]), O)
    sh.camfit(P.L(s[1], -0.1), (150, 440, 478, 272), pad=1.15, wmin=560).hl(P.L(s[1], 0.3), (154.8, 443.7, 468.1, 264.2), t1, O).done()
    # ---- slide 10: Clear / Confirm my signature ----
    t0, t1 = sp[10]; s = C.lines(P, 10); sh = Shot(10, t0, t1)
    sh.camfit(P.L(s[0], 0.6), (135, 705, 508, 178), pad=1.2, wmin=600)
    sh.ring(P.W(s[1], "tap"), (154.8, 710.5, 468.1, 75.5), P.L(s[2]), A).ring(P.W(s[2], "tap"), (139.7, 803.6, 498.3, 74.2), t1, A).done()
    # ---- slides 11-14 ----
    C.last(P, K, 11, sp, REP); C.after_pdf(P, K, 12, sp); C.remember(P, K, 13, sp); C.where(P, K, 14, sp)
    if C.WARN: print("WARN", *C.WARN, sep="\n  ")
