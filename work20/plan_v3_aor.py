# Video 3 - Acknowledgement of Receipt AA/SEC/F/007: staff handing over, CBTO staff, witnesses.
HOLDS = {3: 0.6, 4: 1.0, 6: 1.0, 7: 2.4, 12: 1.2, 8: 0.4, 10: 0.6, 11: 1.0, 13: 0.6, 14: 1.6, 15: 0.4, 17: 0.6, 18: 1.0, 20: 0.4, 22: 1.8, 24: 0.4}
PRE = {1: 1.4, 2: 1.4, 3: 1.2}
END_HOLD = 4.8
SEC, STAFF, WIT, CBTO = "SECURITY", "STAFF HANDING OVER", "WITNESS", "CBTO STAFF"
REC = (167, 330, 443, 106); SIG = (181, 455, 416, 235); CONF = (167, 777, 443, 65); CLEAR = (181, 702, 416, 56)


def build(P, K):
    Shot, B, O, A, Card, ICON, chip = K["Shot"], K["BLUE"], K["ORANGE"], K["AMBER"], K["Card"], K["ICON"], K["role_chip"]
    K["role"](0.0, SEC, B)
    # ---- Scene 1: two situations (slide 5 + animation) ----
    sh = Shot(5, 0.0, P.L(3) - 0.3)
    sh.hl(P.L(1) + 0.2, (100.8, 288, 842.4, 676.8), P.L(3) - 0.3, O).hl(P.L(2) + 0.2, (1000.8, 288, 842.4, 676.8), P.L(3) - 0.3, O).done()
    c = Card(P.L(3) - 0.3, P.S(1), "Security fills in the form and brings the phone")
    for r, (lab, a, b, ca, cb, tmv) in enumerate((("Situation A", "STAFF", "SECURITY", O, B, P.L(3) + 0.5), ("Situation B", "SECURITY", "CBTO", B, O, P.L(3) + 2.0))):
        y = 230 + r * 250
        c.el(f'<div class="mgs" style="font-size:34px;font-weight:800">{lab}</div>', 70, y + 30, P.L(3) - 0.1 + 0.4 * r)
        c.el(chip(a, ca, 30), 330, y + 26, P.L(3) + 0.4 * r); c.el(chip(b, cb, 30), 1090, y + 26, P.L(3) + 0.2 + 0.4 * r)
        bx = c.el(ICON["box"], 560, y, P.L(3) + 0.2 + 0.4 * r, enter="pop"); c.move(bx, tmv, 1.2, 400)
        c.el(f'<div class="mgs" style="font-size:28px;color:#b8550d">▲ Recipient</div>', 1100, y + 100, P.W(4, "receiving") + 0.3 * r)
    c.done()
    # ---- Scene 2: Situation A (slides 7-11) ----
    sh = Shot(7, P.S(1), P.L(7) - 0.3)
    sh.camfit(P.S(1) + 1.0, (101, 700, 763, 370), pad=1.08, wmin=820)
    sh.chip(P.W(5, "first"), 530, 760, "1  Security — Recipient", B, P.L(7) - 0.3, 32)
    sh.chip(P.L(6), 140, 1015, "2  Staff — Handed over by", O, P.L(7) - 0.3, 30)
    sh.chip(P.L(6) + 0.8, 560, 845, "3  Witness", O, P.L(7) - 0.3, 30).done()
    K["role"](P.W(6, "turn"), STAFF, O)
    sh = Shot(8, P.L(7) - 0.3, P.W(7, "role") - 0.2)
    sh.camfit(P.L(7) + 0.3, REC, pad=1.25, wmin=560).hl(P.W(7, "name") - 0.1, REC, P.W(7, "role") - 0.2, O).done()
    sh = Shot(7, P.W(7, "role") - 0.2, P.L(8) - 0.3)
    sh.cam(P.W(7, "role") + 0.3, 470, 500, 760).hl(P.W(7, "items"), (133, 289, 704, 422), P.L(8) - 0.3).done()
    K["stage_label"](P.S(1), P.W(7, "role") - 0.2, "SITUATION A", "#ffcf99"); K["stage_label"](P.W(7, "role") - 0.2, P.L(8) - 0.3, "SITUATION A · PAPER FORM", "#ffcf99"); K["stage_label"](P.L(8) - 0.3, P.S(2), "SITUATION A", "#ffcf99")
    K["callout"](P.W(7, "role"), P.L(8) - 0.3, "On the phone, scroll up to check your role and items", "note")
    sh = Shot(9, P.L(8) - 0.3, P.L(10) - 0.3)
    sh.camfit(P.L(8) + 0.4, (167, 455, 443, 390), pad=1.12, wmin=620)
    sh.hl(P.W(8, "sign"), SIG, P.L(10) - 0.3, O).ring(P.W(8, "tap"), CONF, P.L(10) - 0.3, A).ring(P.W(9, "tap"), CLEAR, P.L(10) - 0.3, A).done()
    K["role"](P.L(10), WIT, O)
    sh = Shot(10, P.L(10) - 0.3, P.L(11) - 0.3)
    sh.cam(P.L(10) + 0.4, 389, 400, 580).cam(P.W(10, "taps") - 0.7, 389, 790, 580)
    sh.hl(P.W(10, "checks"), REC, P.L(11) - 0.3, O).ring(P.W(10, "taps"), CONF, P.L(11) - 0.3, A).done()
    sh = Shot(11, P.L(11) - 0.3, P.S(2))
    sh.hl(P.L(11) + 0.2, P.txt(11, "Screen says"), P.S(2)).done()
    K["role"](P.W(11, "security"), SEC, B)
    # ---- Scene 3: Situation B (slides 12-18) ----
    sh = Shot(13, P.S(2), P.L(13) - 0.3)
    sh.camfit(P.S(2) + 1.0, (101, 700, 763, 370), pad=1.08, wmin=820)
    sh.chip(P.W(12, "cbto", 1) - 0.2, 530, 760, "1  CBTO — Recipient", O, P.L(13) - 0.3, 32)
    sh.chip(P.W(12, "recipient") - 0.2, 140, 1015, "2  Security — Handed over by", B, P.L(13) - 0.3, 30)
    sh.chip(P.W(12, "recipient") + 0.5, 560, 845, "3  Witness", O, P.L(13) - 0.3, 30).done()
    K["role"](P.L(13), CBTO, O)
    sh = Shot(14, P.L(13) - 0.3, P.L(14) - 0.3)
    sh.camfit(P.L(13) + 0.3, REC, pad=1.25, wmin=560).hl(P.W(13, "name") - 0.1, REC, P.L(14) - 0.3, O).done()
    sh = Shot(13, P.L(14) - 0.3, P.L(15) - 0.3)
    sh.cam(P.L(14) + 0.2, 470, 500, 760).hl(P.W(14, "item"), (133, 289, 704, 422), P.L(15) - 0.3).done()
    K["stage_label"](P.S(2), P.L(14) - 0.3, "SITUATION B", "#ffcf99"); K["stage_label"](P.L(14) - 0.3, P.L(15) - 0.3, "SITUATION B · PAPER FORM", "#ffcf99"); K["stage_label"](P.L(15) - 0.3, P.S(3), "SITUATION B", "#ffcf99")
    K["callout"](P.L(14), P.L(15) - 0.3, "On the phone, scroll up to see the items list", "note")
    sh = Shot(15, P.L(15) - 0.3, P.L(16) - 0.3)
    sh.camfit(P.L(15) + 0.3, (167, 455, 443, 390), pad=1.12, wmin=620).hl(P.W(15, "sign"), SIG, P.L(16) - 0.3, O).ring(P.W(15, "tap"), CONF, P.L(16) - 0.3, A).done()
    sh = Shot(16, P.L(16) - 0.3, P.L(18) - 0.3)
    sh.hl(P.L(17) + 0.2, P.txt(16, "Security signs as"), P.L(18) - 0.3, B).done()
    K["role"](P.W(16, "security"), SEC, B)
    K["role"](P.L(18), WIT, O)
    sh = Shot(17, P.L(18) - 0.3, P.W(18, "gives") - 0.2)
    sh.cam(P.L(18) + 0.4, 389, 400, 580).cam(P.W(18, "taps") - 0.7, 389, 790, 580)
    sh.hl(P.W(18, "checks"), REC, P.W(18, "gives") - 0.2, O).ring(P.W(18, "taps"), CONF, P.W(18, "gives") - 0.2, A).done()
    sh = Shot(18, P.W(18, "gives") - 0.2, P.S(3))
    sh.hl(P.W(18, "gives") + 0.2, P.txt(18, "Screen says"), P.S(3)).done()
    K["role"](P.W(18, "back") + 0.2, SEC, B)
    # ---- Scene 4: wrong details and the signed copy (slides 20, 19, 21) ----
    sh = Shot(20, P.S(3), P.L(21) - 0.3)
    sh.hl(P.L(19) + 0.3, P.txt(20, "Read the details before signing"), P.L(21) - 0.3, "#ffffff").hl(P.L(20) + 0.2, P.txt(20, "Sign for someone else"), P.L(21) - 0.3, "#ff8a8a").done()
    K["callout"](P.L(19), P.L(21) - 0.3, "Wrong name, role or item? Tell Security before signing", "warn")
    sh = Shot(19, P.L(21) - 0.3, P.L(23) - 0.3)
    sh.camfit(P.L(21) + 0.5, (154, 561, 498, 174), pad=1.3, wmin=640)
    sh.ring(P.W(22, "record"), (172, 686, 465, 42), P.E(22) + 0.5, A, sfx=False)
    sh.camfit(P.E(22) + 0.4, (778, 720, 1051, 194), pad=1.1).hl(P.E(22) + 0.7, (778, 720, 1051, 194), P.L(23) - 0.3).done()
    K["stage_label"](P.L(21) - 0.3, P.E(22) + 0.4, "SAVED SCREEN · TEST RECORD"); K["stage_label"](P.E(22) + 0.4, P.L(23) - 0.3, "PDF FILENAME EXAMPLE")
    sh = Shot(21, P.L(23) - 0.3, P.L(24) - 0.3)
    sh.hl(P.L(23) + 0.4, P.txt(21, "restricted AirAsia folder"), P.L(24) - 0.3, "#ffffff").done()
    K["flow"](P.L(24) - 0.3, P.E(24) + 0.4, "Where your signed copy goes", [("pdf", "Signed PDF<br>with Record ID", P.L(24) - 0.1), ("folder", "Restricted<br>AirAsia folder", P.L(24) + 0.3),
                                                                              ("log", "Record<br>log", P.L(24) + 0.7), ("mail", "Email copy<br>to you", P.W(24, "emails"))])
    K["summary"](P.E(24) + 0.4, P.total, ["Check", "Sign", "Confirm", "Hand back"], sub="The recipient signs first in both situations.")
