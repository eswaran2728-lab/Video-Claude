# v02 Video 3 - Acknowledgement of Receipt AA/SEC/F/007 (staff handing over, CBTO staff, witnesses): every slide, in order.
import common20 as C
HOLDS_S = {(11, 0): 0.9, (18, 0): 0.9, (21, 1): 0.6, (5, 1): 0.8, (5, 2): 0.8, (8, 0): 1.2, (8, 2): 1.2, (13, 3): 1.0,
           (14, 0): 1.2, (14, 1): 1.2, (16, 0): 1.2, (19, 1): 1.0}
END_HOLD = 4.2
SEC, STAFF, WIT, CBTO = "SECURITY", "STAFF HANDING OVER", "WITNESS", "CBTO STAFF"
o = lambda *r: C.orc("v3_aor", 1, *r)
NAME_O, ITEMS_O, RECIP_O, HAND_O, WIT_O = o(150, 440, 1540, 565), o(150, 598, 1540, 1278), o(150, 1310, 900, 1600), o(150, 1645, 765, 1970), o(848, 1645, 1465, 1970)
ORIG = "ORIGINAL PAPER FORM"
REC = (167, 330, 443, 106); SIG = (181, 455, 416, 235); CONF = (167, 777, 443, 65); CLEAR = (181, 702, 416, 56); ITEMS = (133, 289, 704, 422)
ROW = lambda y: (964.8, y, 878.4, 93.6)                                   # signing-order rows on slides 7 / 13
COLA = lambda y: (165.6, y, 748.8, 86.4); COLB = lambda y: (1065.6, y, 748.8, 86.4)


def build(P, K):
    Shot, B, O, A, Card, ICON, chip, SL = K["Shot"], K["BLUE"], K["ORANGE"], K["AMBER"], K["Card"], K["ICON"], K["role_chip"], K["stage_label"]
    sp = C.spans(P, K); K["role"](0.0, SEC, B)
    C.title(P, K, 1, sp); C.changed(P, K, 2, sp, "orig-1.png"); C.steps(P, K, 3, sp, "SIGNER"); C.need(P, K, 4, sp)
    # ---- slide 5: one form, two situations (slide -> animation -> slide) ----
    t0, t1 = sp[5]; s = C.lines(P, 5)
    Shot(5, t0, P.L(s[1], -0.2)).hl(P.A(5, 0.2), P.txt(5, "One form, two situations"), P.L(s[1], -0.2)).done()
    c = Card(P.L(s[1], -0.2), P.L(s[3], -0.2), "One form, two situations")
    for r, (lab, a, b_, ca, cb, tmv) in enumerate((("Situation A", "STAFF", "SECURITY", O, B, P.W(s[1], "hand")), ("Situation B", "SECURITY", "CBTO", B, O, P.W(s[2], "hands")))):
        y = 230 + r * 250; tr = P.L(s[1 + r], -0.1)
        c.el(f'<div class="mgs" style="font-size:34px;font-weight:800">{lab}</div>', 70, y + 30, tr)
        c.el(chip(a, ca, 30), 330, y + 26, tr + 0.1); c.el(chip(b_, cb, 30), 1090, y + 26, tr + 0.3)
        bx = c.el(ICON["box"], 560, y, tr + 0.2, enter="pop"); c.move(bx, tmv, 1.2, 400)
        c.el('<div class="mgs" style="font-size:28px;color:#b8550d">▲ Recipient</div>', 1100, y + 100, tmv + 1.2)
    c.done()
    sh = Shot(5, P.L(s[3], -0.2), t1)
    sh.hl(P.W(s[3], "fills") - 0.2, COLA(511.2), t1, B).hl(P.W(s[3], "fills") - 0.2, COLB(511.2), t1, B)
    sh.hl(P.W(s[3], "recipient") - 0.2, COLA(614.9), t1, O).hl(P.W(s[3], "recipient") - 0.2, COLB(614.9), t1, O)
    sh.hl(P.W(s[3], "witness") - 0.2, COLA(822.2), t1, O).hl(P.W(s[3], "witness") - 0.2, COLB(822.2), t1, O).done()
    # ================= Situation A (slides 6-11) =================
    C.part(P, K, 6, sp)
    t0, t1 = sp[7]; s = C.lines(P, 7); sh = Shot(7, t0, P.L(s[3], -0.2))
    sh.hl(P.W(s[0], "recipient") - 0.2, ROW(396), t1, B).hl(P.W(s[0], "recipient") - 0.2, (132.6, 723.4, 386.1, 147.2), t1, B)
    sh.hl(P.L(s[1], 0.1), ROW(525.6), t1, O).hl(P.L(s[1], 0.1), (132.6, 893.3, 318, 163.5), t1, O)
    sh.hl(P.L(s[2], 0.1), ROW(655.2), t1, O).hl(P.L(s[2], 0.1), (482.4, 893.3, 318, 163.5), t1, O)
    sh.done()
    sh = Shot("o-1", P.L(s[3], -0.2), t1).camfit(P.L(s[3], 0.4), o(150, 440, 1540, 1278), pad=1.06).hl(P.W(s[3], "names") - 0.2, NAME_O, t1, B).hl(P.W(s[3], "items") - 0.2, ITEMS_O, t1, B)
    sh.camfit(P.L(s[4], -0.2), o(150, 1300, 1540, 1975), pad=1.08).hl(P.L(s[4], 0.1), HAND_O, t1, O).done(); K["stage_label"](P.L(s[3], -0.2), t1, ORIG)
    t0, t1 = sp[8]; s = C.lines(P, 8); tp = P.W(s[0], "passes") - 0.2; ti = P.W(s[2], "role") - 0.2
    Shot(8, t0, tp).done()
    K["handover"](tp, P.L(s[1], -0.2), (SEC, B), (STAFF, O), "Security has signed as Recipient", t_move=tp + 0.3); K["role"](tp + 1.3, STAFF, O)
    Shot(8, P.L(s[1], -0.2), ti).camfit(P.L(s[1], 0.3), REC, pad=1.25, wmin=560).hl(P.L(s[1], 0.3), REC, ti, O).done()
    Shot("o-1", ti, t1).camfit(ti + 0.3, o(150, 440, 1540, 1278), pad=1.08).hl(P.W(s[2], "items") - 0.2, ITEMS_O, t1).done(); K["stage_label"](ti, t1, ORIG)
    K["callout"](ti + 0.2, t1, "On the phone, scroll up to check your role and items", "note")
    t0, t1 = sp[9]; s = C.lines(P, 9); sh = Shot(9, t0, t1)
    sh.camfit(P.L(s[0], 0.5), (167, 455, 443, 390), pad=1.12, wmin=620)
    sh.hl(P.W(s[0], "sign"), SIG, t1, O).ring(P.W(s[0], "tap"), CONF, t1, A).ring(P.W(s[1], "tap"), CLEAR, t1, A).done()
    t0, t1 = sp[10]; s = C.lines(P, 10); tw = P.W(s[0], "check") - 0.2
    K["handover"](t0, tw, (STAFF, O), (WIT, O), "Next, the witness", t_move=t0 + 0.5); K["role"](t0 + 1.4, WIT, O)
    sh = Shot(10, tw, t1)
    sh.cam(tw + 0.7, 389, 400, 580).cam(P.W(s[0], "tap") - 0.7, 389, 790, 580)
    sh.hl(tw + 0.3, REC, t1, O).ring(P.W(s[0], "tap"), CONF, t1, A).done()
    C.last(P, K, 11, sp, WIT)
    # ================= Situation B (slides 12-18) =================
    C.part(P, K, 12, sp)
    t0, t1 = sp[13]; s = C.lines(P, 13); sh = Shot(13, t0, P.W(s[3], "listed"))
    sh.hl(P.W(s[0], "recipient") - 0.2, ROW(396), t1, O).hl(P.W(s[0], "recipient") - 0.2, (132.6, 723.4, 386.1, 147.2), t1, O)
    sh.hl(P.L(s[1], 0.1), ROW(525.6), t1, B).hl(P.L(s[1], 0.1), (132.6, 893.3, 318, 163.5), t1, B)
    sh.hl(P.L(s[2], 0.1), ROW(655.2), t1, O).hl(P.L(s[2], 0.1), (482.4, 893.3, 318, 163.5), t1, O)
    sh.hl(P.L(s[3], 0.1), (964.8, 792, 864, 115.2), P.W(s[3], "listed")).done()
    Shot("o-1", P.W(s[3], "listed"), t1).camfit(P.W(s[3], "listed") + 0.3, o(150, 598, 1540, 1600), pad=1.06).hl(P.W(s[3], "listed") + 0.2, ITEMS_O, t1, O).hl(P.W(s[3], "received") - 0.2, RECIP_O, t1, O).done(); K["stage_label"](P.W(s[3], "listed"), t1, ORIG)
    t0, t1 = sp[14]; s = C.lines(P, 14); tc = P.L(s[0], 0.3)
    K["handover"](t0, P.L(s[1], -0.2), (SEC, B), (CBTO, O), "CBTO staff sign first, as Recipient", t_move=t0 + 0.6); K["role"](t0 + 1.5, CBTO, O)
    Shot(14, P.L(s[1], -0.2), P.W(s[1], "check") - 0.2).camfit(P.L(s[1], 0.2), REC, pad=1.25, wmin=560).hl(P.L(s[1], 0.2), REC, t1, O).done()
    Shot("o-1", P.W(s[1], "check") - 0.2, t1).camfit(P.W(s[1], "check"), o(150, 440, 1540, 1278), pad=1.08).hl(P.W(s[1], "item"), ITEMS_O, t1).done(); K["stage_label"](P.W(s[1], "check") - 0.2, t1, ORIG)
    K["callout"](P.L(s[1]), t1, "On the phone, scroll up to see the items list", "note")
    t0, t1 = sp[15]; s = C.lines(P, 15); sh = Shot(15, t0, t1)
    sh.camfit(P.L(s[0], 0.4), (167, 455, 443, 390), pad=1.12, wmin=620).hl(P.W(s[0], "sign"), SIG, t1, O).ring(P.W(s[0], "tap"), CONF, t1, A).ring(P.W(s[1], "tap"), CLEAR, t1, A).done()
    t0, t1 = sp[16]; s = C.lines(P, 16); tb = P.W(s[0], "back") - 0.1
    Shot(16, t0, tb).hl(P.A(16, 0.1), P.txt(16, "Pass the phone back"), tb).done()
    K["handover"](tb, P.L(s[1], -0.2), (CBTO, O), (SEC, B), "Pass the phone back to Security", t_move=tb + 0.3); K["role"](tb + 1.3, SEC, B)
    sh = Shot(16, P.L(s[1], -0.2), t1).hl(P.L(s[1], 0.1), C.rowrect(P, K, 16, "Security signs as"), t1, B).hl(P.L(s[2], 0.1), C.rowrect(P, K, 16, "Then the witness"), t1, O).done()
    K["role"](P.L(s[2], 0.3), WIT, O)
    t0, t1 = sp[17]; s = C.lines(P, 17); sh = Shot(17, t0, t1)
    sh.cam(P.W(s[0], "checks") + 0.3, 389, 400, 580).cam(P.W(s[0], "taps") - 0.7, 389, 790, 580)
    sh.hl(P.W(s[0], "checks"), REC, t1, O).ring(P.W(s[0], "taps"), CONF, t1, A).done()
    C.last(P, K, 18, sp, WIT)
    # ---- slides 19-21 ----
    C.after_saved(P, K, 19, sp, (154, 561, 498, 174), (172, 686, 465, 42)); C.remember(P, K, 20, sp)
    C.where(P, K, 21, sp, sub="The Recipient signs first in both situations.")
    if C.WARN: print("WARN", *C.WARN, sep="\n  ")
