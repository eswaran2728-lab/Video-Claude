# Video 4 - Search List AA/SEC/F/008: the person searched and the witness (if present).
HOLDS = {3: 1.0, 4: 0.6, 5: 1.0, 6: 1.0, 7: 1.8, 8: 0.4, 11: 0.8, 12: 3.4, 13: 0.8, 15: 1.8, 18: 0.4}
PRE = {1: 1.3, 2: 1.3, 3: 1.2}
END_HOLD = 4.4
SEC, PER, WIT = "SECURITY", "PERSON SEARCHED", "WITNESS (IF PRESENT)"


def build(P, K):
    Shot, B, O, A, Card, chip = K["Shot"], K["BLUE"], K["ORANGE"], K["AMBER"], K["Card"], K["role_chip"]
    K["role"](0.0, SEC, B)
    # ---- Scene 1 (slides 1, 6) ----
    Shot(1, 0.0, P.L(1) - 0.3).done()
    K["role"](P.W(0, "hands") + 0.4, PER, O)
    sh = Shot(6, P.L(1) - 0.3, P.S(1))                                          # the deck's own signing-order list + the form's signer areas
    sh.hl(P.W(1, "first") - 0.3, (565, 816, 250, 96), P.S(1), O).hl(P.W(1, "first") - 0.3, (960, 392, 880, 102), P.S(1), O)
    sh.hl(P.W(2, "witness"), (145, 816, 223, 96), P.S(1), O).hl(P.W(2, "witness"), (960, 522, 880, 102), P.S(1), O)
    sh.hl(P.L(3) + 0.2, (145, 941, 351, 94), P.S(1), B).hl(P.L(3) + 0.2, (960, 651, 880, 102), P.S(1), B).done()
    # ---- Scene 2 (slides 7, 6, 12) ----
    sh = Shot(7, P.S(1), P.L(5) - 0.3)
    sh.camfit(P.S(1) + 1.0, (167, 330, 443, 134), pad=1.25, wmin=560).hl(P.W(4, "orange") - 0.1, (167, 330, 443, 134), P.L(5) - 0.3, O).done()
    sh = Shot(6, P.L(5) - 0.3, P.L(8) - 0.3)
    sh.camfit(P.L(5) + 0.4, (145, 320, 670, 250), pad=1.1, wmin=760).hl(P.W(5, "search"), (148, 330, 664, 236), P.L(6))
    sh.camfit(P.L(6) - 0.1, (145, 590, 670, 190), pad=1.1, wmin=760).hl(P.L(6) + 0.3, (148, 595, 664, 185), P.L(8) - 0.3).done()
    K["stage_label"](P.L(5) - 0.3, P.L(8) - 0.3, "PAPER FORM", "#ffffff")
    K["callout"](P.L(5), P.L(7) - 0.2, "On the phone, scroll up to see these details", "note")
    K["callout"](P.L(7), P.L(8) - 0.3, "‘Nil’ means nothing was found", "info")
    sh = Shot(12, P.L(8) - 0.3, P.S(2))
    sh.hl(P.L(8) + 0.3, P.txt(12, "Read the details before signing"), P.S(2), "#ffffff").done()
    # ---- Scene 3 (slides 8, 9, outcomes, 10) ----
    sh = Shot(8, P.S(2), P.L(12) - 0.3)
    sh.camfit(P.S(2) + 0.9, (167, 482, 443, 386), pad=1.12, wmin=620)
    sh.hl(P.W(9, "sign"), (181, 482, 416, 235), P.L(12) - 0.3, O).ring(P.W(10, "tap"), (181, 727, 416, 56), P.L(11), A).ring(P.W(11, "tap"), (167, 804, 443, 64), P.L(12) - 0.3, A).done()
    K["role"](P.L(12), WIT, O)
    sh = Shot(9, P.L(12) - 0.3, P.E(12) + 0.3)
    sh.cam(P.L(12) + 0.3, 389, 400, 580).cam(P.W(12, "tap") - 0.7, 389, 790, 580)
    sh.hl(P.W(12, "check"), (167, 330, 443, 106), P.E(12) + 0.3, O).ring(P.W(12, "tap"), (167, 777, 443, 65), P.E(12) + 0.3, A).done()
    c = Card(P.E(12) + 0.3, P.L(13) - 0.2, "After you confirm")
    t1, t2 = P.E(12) + 0.6, P.E(12) + 1.9
    c.el(chip("WITNESS PRESENT", O, 32), 170, 260, t1, enter="pop", sfx="curated/ui-pop.wav"); c.el('<div class="arrowx" style="width:200px"></div>', 590, 285, t1 + 0.2, enter="draw")
    c.el('<div class="mgs" style="font-size:40px;font-weight:800">Witness signs, then back to Security</div>', 840, 262, t1 + 0.4)
    c.el(chip("NO WITNESS", O, 32), 170, 460, t2, enter="pop", sfx="curated/ui-pop.wav"); c.el('<div class="arrowx" style="width:200px"></div>', 590, 485, t2 + 0.2, enter="draw")
    c.el('<div class="mgs" style="font-size:40px;font-weight:800">Straight back to Security</div>', 840, 462, t2 + 0.4)
    c.done()
    sh = Shot(10, P.L(13) - 0.2, P.S(3))
    sh.hl(P.L(13) + 0.3, P.txt(10, "Screen says"), P.S(3)).done()
    K["role"](P.W(13, "back"), SEC, B)
    # ---- Scene 4 (slides 11, 13) ----
    sh = Shot(11, P.S(3), P.L(16) - 0.3)
    sh.camfit(P.S(3) + 0.9, (154, 561, 498, 174), pad=1.3, wmin=640)
    sh.ring(P.W(15, "record"), (160, 686, 470, 42), P.E(15) + 0.6, A, sfx=False)
    sh.camfit(P.E(15) + 0.5, (778, 720, 1051, 194), pad=1.1).hl(P.E(15) + 0.8, (778, 720, 1051, 194), P.L(16) - 0.3).done()
    K["stage_label"](P.S(3), P.E(15) + 0.5, "SAVED SCREEN · TEST RECORD"); K["stage_label"](P.E(15) + 0.5, P.L(16) - 0.3, "PDF FILENAME EXAMPLE")
    sh = Shot(13, P.L(16) - 0.3, P.L(17) - 0.3)
    sh.hl(P.L(16) + 0.4, P.txt(13, "restricted AirAsia folder"), P.L(17) - 0.3, "#ffffff").done()
    K["flow"](P.L(17) - 0.3, P.E(18) + 0.4, "Where your signed copy goes", [("pdf", "Signed Search List<br>with Record ID", P.L(17) - 0.1), ("folder", "Restricted<br>AirAsia folder", P.L(17) + 0.3),
                                                                              ("log", "Record<br>log", P.L(17) + 0.7), ("mail", "Email copy<br>to you", P.W(17, "emails"))])
    K["summary"](P.E(18) + 0.4, P.total, ["Check the list", "Sign", "Confirm", "Hand back"])
