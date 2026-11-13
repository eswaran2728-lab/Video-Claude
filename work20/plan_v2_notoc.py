# Video 2 - NOTOC (Firearm) AA-SEC-F-063, Captain. Slide coordinates in 1920x1080 slide pixels.
HOLDS = {1: 1.2, 3: 0.8, 4: 1.4, 5: 1.4, 8: 0.6, 10: 1.2, 12: 0.4, 13: 1.8, 15: 0.4}
PRE = {1: 1.3, 2: 1.3, 3: 1.2}
END_HOLD = 4.2
SEC, CAP = "SECURITY", "CAPTAIN"


def build(P, K):
    Shot, B, O, A = K["Shot"], K["BLUE"], K["ORANGE"], K["AMBER"]
    K["role"](0.0, SEC, B)
    # ---- Scene 1 (slides 1, 6, 7) ----
    Shot(1, 0.0, P.L(0) + 2.2).done()
    sh = Shot(6, P.L(0) + 2.2, P.L(1) - 0.2)
    sh.camfit(P.L(0) + 3.0, (101, 281, 1066, 754), pad=1.02)
    sh.hl(P.L(0) + 3.3, (637, 734, 444, 181), P.L(1) - 0.2, O).chip(P.L(0) + 3.3, 700, 930, "Captain signs here", O, P.L(1) - 0.2, 34).done()
    K["handover"](P.L(1) - 0.2, P.E(1) + 0.9, (SEC, B), (CAP, O), "You check and sign on that same phone", t_move=P.L(1) + 0.3)
    K["role"](P.L(1) + 1.6, CAP, O)
    sh = Shot(7, P.E(1) + 0.9, P.S(1))
    sh.cam(P.L(2) - 0.2, 389, 600, 640).ring(P.W(2, "tap"), (155, 575, 468, 73), P.S(1), A).done()
    # ---- Scene 2 (slides 8, 10) ----
    sh = Shot(8, P.S(1), P.L(5) - 0.3)
    sh.camfit(P.S(1) + 1.0, (167, 262, 443, 384), pad=1.15, wmin=620)
    sh.hl(P.L(3) + 0.2, (176, 279, 426, 136), P.L(4))                               # flight details
    sh.hl(P.W(4, "review"), (176, 455, 426, 92), P.L(5) - 0.3)                       # each firearm entry
    sh.hl(P.W(4, "loaded"), (180, 572, 230, 38), P.L(5) - 0.3, O).done()             # Loaded by
    sh = Shot(10, P.L(5) - 0.3, P.W(5, "give") - 0.1)
    sh.cam(P.L(5) + 0.5, 389, 815, 600).ring(P.W(5, "tap"), (167, 849, 443, 91), P.W(5, "give") - 0.1, A).done()
    K["handover"](P.W(5, "give") - 0.1, P.S(2), (CAP, O), (SEC, B), "Something wrong? Phone back to Security for correction", t_move=P.W(5, "give") + 0.4)
    # ---- Scene 3 (slides 9, 10) ----
    sh = Shot(9, P.S(2), P.L(9) - 0.3)
    sh.camfit(P.S(2) + 0.9, (181, 571, 416, 174), pad=1.25, wmin=560)
    sh.hl(P.W(6, "acknowledged") - 0.2, (181, 571, 416, 85), P.L(8), O).hl(P.L(7) + 0.2, (181, 656, 416, 89), P.L(8), O)
    sh.camfit(P.L(8) - 0.1, (181, 770, 416, 222), pad=1.15, wmin=560).hl(P.L(8) + 0.2, (181, 770, 416, 222), P.L(9) - 0.3, O).done()
    sh = Shot(10, P.L(9) - 0.3, P.S(3))
    sh.cam(P.L(9) + 0.2, 389, 790, 620)
    sh.ring(P.W(9, "tap"), (180, 703, 418, 56), P.L(10), A).ring(P.W(10, "tap"), (167, 782, 443, 65), P.S(3), A).done()
    # ---- Scene 4 (slides 11, 12, 14) ----
    sh = Shot(11, P.S(3), P.L(13) - 0.3)
    sh.hl(P.L(11) + 0.2, P.txt(11, "Screen says"), P.L(13) - 0.3).hl(P.L(12) + 0.2, P.txt(11, "Security signs and saves"), P.L(13) - 0.3, B).done()
    K["role"](P.W(11, "back"), SEC, B)
    sh = Shot(12, P.L(13) - 0.3, P.L(14) - 0.3)
    sh.camfit(P.L(13) + 0.4, (154, 410, 498, 165), pad=1.3, wmin=640)
    sh.ring(P.W(13, "record"), (180, 536, 420, 40), P.E(13) + 0.6, A, sfx=False)
    sh.camfit(P.E(13) + 0.5, (778, 720, 1051, 194), pad=1.1).hl(P.E(13) + 0.8, (778, 720, 1051, 194), P.L(14) - 0.3).done()
    K["stage_label"](P.L(13) - 0.3, P.E(13) + 0.5, "SAVED SCREEN · TEST RECORD"); K["stage_label"](P.E(13) + 0.5, P.L(14) - 0.3, "PDF FILENAME EXAMPLE")
    sh = Shot(14, P.L(14) - 0.3, P.L(15) - 0.3)
    sh.hl(P.L(14) + 0.4, P.txt(14, "restricted AirAsia folder"), P.L(15) - 0.3, "#ffffff").done()
    K["flow"](P.L(15) - 0.3, P.E(15) + 0.4, "Where your signed copy goes", [("pdf", "Signed PDF<br>with Record ID", P.L(15) - 0.1), ("folder", "Restricted<br>AirAsia folder", P.L(15) + 0.3),
                                                                              ("log", "Record<br>log", P.L(15) + 0.7), ("mail", "Email copy<br>to you", P.W(15, "emails"))])
    K["summary"](P.E(15) + 0.4, P.total, ["Check", "Sign", "Confirm", "Hand back"])
