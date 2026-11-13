# Video 1 - FOCA Checklist (AA/SEC/F/070), Airline Representative. Slide coordinates are 1920x1080 slide pixels (shapes.json).
HOLDS = {3: 1.4, 5: 0.8, 6: 1.2, 7: 1.2, 9: 0.6, 11: 1.2, 13: 0.4, 14: 0.8, 17: 0.4}
PRE = {1: 1.4, 2: 1.3, 3: 1.2}
END_HOLD = 4.2
SEC, REP = "SECURITY", "AIRLINE REPRESENTATIVE"


def build(P, K):
    Shot, B, O = K["Shot"], K["BLUE"], K["ORANGE"]
    K["role"](0.0, SEC, B)
    # ---- Scene 1: Security hands you the phone (slides 1, 6) ----
    Shot(1, 0.0, P.L(1) - 0.2).done()
    sh = Shot(6, P.L(1) - 0.2, P.L(2) - 0.3)
    sh.camfit(P.L(1) + 0.9, (995, 347, 840, 597), pad=1.08)                       # page 2 of the paper form
    sh.hl(P.W(1, "sign") - 0.2, (1590, 716, 216, 104), P.L(2) - 0.3, O)            # where the Airline Representative signs
    sh.chip(P.W(1, "sign") - 1.0, 1590, 830, "Airline Rep signs here", O, P.L(2) - 0.3, 34).done()
    c = K["handover"](P.L(2) - 0.3, P.S(1), (SEC, B), (REP, O), "You use Security’s phone", t_move=P.L(2) + 0.3)
    K["role"](P.L(2) + 1.6, REP, O)
    K["callout"](P.L(3), P.S(1), "No app to install · No account to sign in to", "info")
    # ---- Scene 2: Check the details (slides 7, 8) ----
    sh = Shot(7, P.S(1), P.L(5) - 0.4)
    sh.cam(P.S(1) + 1.0, 389, 600, 640)                                              # the real orange handover button (phone panel only)
    sh.ring(P.W(4, "tap"), (149.7, 587.2, 478.1, 78.0), P.L(5) - 0.4, K["AMBER"]).done()
    sh = Shot(8, P.L(5) - 0.4, P.L(7) - 0.2)
    sh.camfit(P.L(5) + 0.5, (175, 265, 430, 165), pad=1.25, wmin=520)            # flight details
    sh.hl(P.L(5) + 0.3, (180.8, 272.7, 416.1, 148.8), P.L(6) + 0.2)
    sh.cam(P.L(6) + 0.2, 390, 700, 760, 1.0).hl(P.L(6) + 0.5, (168, 430, 445, 555), P.L(7) - 0.2).done()   # the checklist lines
    K["handover"](P.L(7) - 0.2, P.S(2), (REP, O), (SEC, B), "Something wrong? Give the phone back to Security", t_move=P.W(7, "give"))
    K["callout"](P.L(7), P.S(2), "Tap ‘Something is wrong’ (not shown in the deck screenshot)", "note")
    # ---- Scene 3: Sign and confirm (slides 9, 10) ----
    sh = Shot(9, P.S(2), P.L(10) - 0.3)
    sh.camfit(P.S(2) + 1.0, (150, 378, 478, 80), pad=1.15, wmin=560)
    sh.hl(P.W(8, "name") - 0.1, (157, 386, 230, 63), P.L(9), O).hl(P.W(8, "id") - 0.1, (390, 386, 232, 63), P.L(9), O)
    sh.camfit(P.L(9) - 0.1, (150, 440, 478, 272), pad=1.15, wmin=560).hl(P.L(9) + 0.3, (154.8, 443.7, 468.1, 264.2), P.L(10) - 0.3, O).done()
    sh = Shot(10, P.L(10) - 0.3, P.S(3))
    sh.camfit(P.L(10) + 0.6, (135, 705, 508, 178), pad=1.2, wmin=600)
    sh.ring(P.W(10, "tap"), (154.8, 710.5, 468.1, 75.5), P.L(11), K["AMBER"])
    sh.ring(P.W(11, "tap"), (139.7, 803.6, 498.3, 74.2), P.S(3), K["AMBER"]).done()
    # ---- Scene 4: Give the phone back and receive the PDF (slides 11, 12, 14) ----
    sh = Shot(11, P.S(3), P.L(14) - 0.3)
    sh.hl(P.L(12) + 0.2, P.txt(11, "Screen says"), P.L(14) - 0.3).hl(P.L(13) + 0.2, P.txt(11, "Security signs and saves"), P.L(14) - 0.3, B).done()
    K["role"](P.W(12, "back"), SEC, B)
    sh = Shot(12, P.L(14) - 0.3, P.L(15) - 0.3)
    sh.cam(P.L(14) + 0.5, 619, 540, 990)                                              # the PDF panel
    sh.hl(P.L(14) + 0.7, (712, 432, 112, 30), P.L(15) - 0.3)                       # form name in the PDF header
    sh.ring(P.W(14, "record") - 0.1, (152.0, 290.4, 414.4, 29.6), P.L(15) - 0.3, K["AMBER"], sfx=False).done()   # filename with the Record ID
    K["stage_label"](P.L(14) - 0.3, P.L(15) - 0.3, "REAL SIGNED PDF · TEST RECORD")
    sh = Shot(14, P.L(15) - 0.3, P.L(16) - 0.3)
    sh.hl(P.L(15) + 0.4, P.txt(14, "restricted AirAsia folder"), P.L(16) - 0.3, "#ffffff").done()
    K["flow"](P.L(16) - 0.3, P.E(17) + 0.4, "Where your signed copy goes", [("pdf", "Signed PDF<br>with Record ID", P.L(16) - 0.1), ("folder", "Restricted<br>AirAsia folder", P.L(16) + 0.4),
                                                                              ("log", "Record<br>log", P.L(16) + 0.9), ("mail", "Email copy<br>to you", P.W(16, "emails"))])
    K["summary"](P.E(17) + 0.4, P.total, ["Check", "Sign", "Confirm", "Hand back"])
