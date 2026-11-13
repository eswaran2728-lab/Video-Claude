# v02 Video 2 - NOTOC (Firearm) AA-SEC-F-063, Captain: every slide of the deck, in order.
import common20 as C
HOLDS_S = {(11, 0): 0.9, (14, 2): 0.6, (6, 1): 0.8, (6, 2): 1.0, (7, 0): 1.1, (7, 1): 0.8, (8, 0): 0.6, (8, 1): 1.2, (9, 0): 0.6, (9, 2): 0.8, (10, 1): 1.4, (10, 2): 0.8, (12, 1): 1.0}
END_HOLD = 4.2
SEC, CAP = "SECURITY", "CAPTAIN"


def build(P, K):
    Shot, B, O, A = K["Shot"], K["BLUE"], K["ORANGE"], K["AMBER"]
    sp = C.spans(P, K); K["role"](0.0, SEC, B)
    C.title(P, K, 1, sp); C.changed(P, K, 2, sp, "orig-1.png"); C.steps(P, K, 3, sp, CAP); C.need(P, K, 4, sp); C.part(P, K, 5, sp)
    # ---- slide 6: the paper form we used (deck slide -> the ORIGINAL form) ----
    t0, t1 = sp[6]; s = C.lines(P, 6); o = lambda *r: C.orc("v2_notoc", 1, *r)
    sh = Shot(6, t0, P.L(s[1], -0.2)).hl(P.A(6, 0.3), (190, 733, 447, 233), P.L(s[1], -0.2), B).hl(P.A(6, 0.3), (637, 733, 444, 233), P.L(s[1], -0.2), O).done()
    sh = Shot("o-1", P.L(s[1], -0.2), t1)
    sh.hl(P.W(s[1], "fills") - 0.2, o(195, 420, 2136, 939), P.L(s[2], -0.2), B).hl(P.W(s[1], "loaded") - 0.2, o(195, 992, 1178, 1395), P.L(s[2], -0.2), B)
    sh.hl(P.W(s[2], "checks"), o(195, 420, 2136, 939), P.W(s[2], "types") - 0.2, O)
    sh.camfit(P.W(s[2], "types") - 0.4, o(1170, 992, 2155, 1395), pad=1.3).hl(P.W(s[2], "types") - 0.2, o(1172, 992, 2153, 1395), t1, O).done()
    K["stage_label"](P.L(s[1], -0.2), t1, "ORIGINAL PAPER FORM")
    # ---- slide 7: Security hands you the phone -> tap 'Captain has the phone' ----
    t0, t1 = sp[7]; s = C.lines(P, 7); th = P.W(s[0], "hands") - 0.2
    Shot(7, t0, th).done()
    K["handover"](th, P.L(s[1], -0.2), (SEC, B), (CAP, O), "Security hands the phone to the Captain", t_move=th + 0.4); K["role"](th + 1.4, CAP, O)
    sh = Shot(7, P.L(s[1], -0.2), t1)
    sh.cam(P.L(s[1], -0.2), 389, 600, 640).ring(P.W(s[1], "tap"), (155, 575, 468, 73), t1, A).done()
    # ---- slide 8: check the details ----
    t0, t1 = sp[8]; s = C.lines(P, 8); sh = Shot(8, t0, t1)
    sh.camfit(P.L(s[0], 0.5), (167, 262, 443, 384), pad=1.15, wmin=620).hl(P.L(s[0], 0.5), (176, 279, 426, 136), P.L(s[1]))
    sh.hl(P.W(s[1], "review"), (176, 455, 426, 92), t1).hl(P.W(s[1], "loaded") - 0.2, (180, 572, 230, 38), t1, O).done()
    # ---- slide 9: Acknowledged by + ID number, then sign ----
    t0, t1 = sp[9]; s = C.lines(P, 9); sh = Shot(9, t0, t1)
    sh.camfit(P.L(s[0], 0.6), (181, 571, 416, 174), pad=1.25, wmin=560)
    sh.hl(P.W(s[0], "acknowledged") - 0.2, (181, 571, 416, 85), P.L(s[2]), O).hl(P.L(s[1], 0.1), (181, 656, 416, 89), P.L(s[2]), O)
    sh.camfit(P.L(s[2], -0.1), (181, 770, 416, 222), pad=1.15, wmin=560).hl(P.L(s[2], 0.2), (181, 770, 416, 222), t1, O).done()
    # ---- slide 10: Clear / Something is wrong / Confirm my signature ----
    t0, t1 = sp[10]; s = C.lines(P, 10); tg = P.W(s[1], "give") - 0.1
    sh = Shot(10, t0, tg)
    sh.cam(P.L(s[0], 0.4), 389, 790, 620).ring(P.W(s[0], "tap"), (180, 703, 418, 56), P.L(s[1], -0.1), A)
    sh.cam(P.L(s[1], 0.1), 389, 815, 600).ring(P.W(s[1], "tap"), (167, 849, 443, 91), tg, A).done()
    K["handover"](tg, P.L(s[2], -0.2), (CAP, O), (SEC, B), "Something wrong? Phone back to Security for correction", t_move=tg + 0.4)
    sh = Shot(10, P.L(s[2], -0.2), t1)
    sh.cam(P.L(s[2], -0.2), 389, 790, 620).ring(P.W(s[2], "tap"), (167, 782, 443, 65), t1, A).done()
    # ---- slides 11-14 ----
    C.last(P, K, 11, sp, CAP); C.after_saved(P, K, 12, sp, (154, 410, 498, 165), (180, 536, 420, 40)); C.remember(P, K, 13, sp); C.where(P, K, 14, sp)
    if C.WARN: print("WARN", *C.WARN, sep="\n  ")
