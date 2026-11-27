# RevLog explainer: scene plan. One narration line = one visual beat. Every screenshot file must be listed in manifest.json.
# Shot kinds:
#   ("phone", file, ops)            single phone, centred
#   ("duo", L, R, active)           Staff phone left, Rider phone right (chapter 5); L/R = (file, ops) or ("mock", name)
#   ("row4",)                       four role phones in a row (chapter 2)
#   ("ways", ops)                   two ways to sell (chapter 7)
#   ("mock", name, ops)             camera mock-up inside a phone frame
#   ("card", title, sub)            title card, no screenshot
#   ("close",)                      closing: role labels around one shared record
#   ("seq", [(word, shot), ...])    several shots inside one line, switching at the spoken word (None = line start)
#   ("strip", [files])              a quick strip of several phones (guide cards)
# ops: list of ("zoom", word, target, z) | ("ring", word, target) | ("unzoom", word) ; word = a spoken word that triggers it (or None = line start)
# target: OCR phrase (searched in that screenshot) or an explicit native-pixel box (x, y, w, h) on the 585x1266 screenshot.
VOICE, SPEED = "af_heart", 0.87
CHAPTERS = ["Opening", "Four roles", "Rider", "Workshop setup", "Workshop visit", "New bike", "Rider controls", "Admin", "Privacy", "Closing"]
ROLE = {"Rider": "#03DAC6", "Workshop owner": "#BB86FC", "Staff": "#6CB4F0", "Admin": "#D3D6DC"}

S = []
def scene(sid, chapter, role, *lines): S.append(dict(id=sid, chapter=chapter, role=role, lines=list(lines)))
L = lambda text, shot, hold=0: dict(text=text, shot=shot, hold=hold)   # hold = minimum seconds on screen for the line

# ---------------- Chapter 1: Opening ----------------
scene("1.1", 0, None,
      L("Service history is usually scattered across workshops and paper receipts.", ("phone", "start-01-welcome.png", [])),
      L("RevLog keeps one record for every bike.", ("phone", "start-01-welcome.png", [("zoom", "record", (30, 850, 525, 120), 1.8)])),
      L("The Rider owns it, and workshops add to it with the Rider's approval.", ("phone", "start-01-welcome.png", [("unzoom", None)])),
      L("A bike with no owner yet can be served too.", ("phone", "start-01-welcome.png", [])))
# ---------------- Chapter 2: The four roles ----------------
scene("2.1", 1, None,
      L("First, pick one: I ride, or I run a workshop.", ("phone", "start-02-register.png", [("ring", "ride", (38, 288, 509, 223)), ("ring", "run", (38, 536, 509, 324))])),
      L("Then sign in with Google or email.", ("phone", "start-03-signin.png", [("ring", "google", (36, 890, 513, 85))])))
scene("2.2", 1, None,
      L("There are four roles.", ("row4",)),
      L("The Rider owns the record.", ("row4", 0)),
      L("The Workshop owner runs the workshop.", ("row4", 1)),
      L("Staff save each service.", ("row4", 2)),
      L("And the Admin approves workshops and checks ownership.", ("row4", 3)))
# ---------------- Chapter 3: Rider workflow (Set A) ----------------
scene("3.1", 2, "Rider",
      L("A Rider finds their bike, then adds the odometer and plate.", ("seq", [(None, ("phone", "rider-01-find-bike.png", [])), ("adds", ("phone", "rider-02-bike-details.png", [("zoom", "odometer", (20, 480, 545, 290), 1.7)]))])))
scene("3.2", 2, "Rider",
      L("Two quick questions help RevLog tell you what's due.", ("phone", "rider-04-quick-start.png", [])),
      L("A short guide follows.", ("strip", ["rider-05-guide-1.png", "rider-05-guide-2.png", "rider-05-guide-3.png", "rider-05-guide-4.png"])),
      L("Then the Rider agrees to how their data is used.", ("phone", "rider-06-consent.png", [("ring", "agrees", (24, 1010, 537, 70))])))
scene("3.3", 2, "Rider",
      L("The bike is now in the Garage.", ("phone", "rider-07-garage-top.png", [])),
      L("Below it: Log service, Verify this bike, and What's due.", ("phone", "rider-07-garage-bottom.png", [("ring", "log", (24, 395, 537, 71)), ("ring", "verify", (24, 481, 537, 71)), ("ring", "due", "What's due")])))
scene("3.4", 2, "Rider",
      L("Verify this bike asks for photos of your driving licence and geran.", ("phone", "rider-03-verify-bike.png", [("clip", 585), ("ring", "licence", (40, 350, 505, 90)), ("ring", "and", (40, 478, 505, 92))])),
      L("They prove the bike is yours.", ("mock", "licence", []), 3.6),
      L("Document photos are deleted after the check, or kept up to 14 days if checked by hand.", ("mock", "geran", [])),
      L("Once the bike is verified, My code becomes available. We'll see the Admin's check later.", ("mock", "geran_checking", [])))
scene("3.5", 2, "Rider",
      L("What's due lists every item. Tap one to see how far it has left.", ("seq", [(None, ("phone", "rider-08-whats-due-top.png", [])), ("tap", ("phone", "rider-08-item-detail.png", [("zoom", "far", (24, 170, 537, 290), 1.6)]))])))
scene("3.6", 2, "Rider",
      L("Log service records your own work.", ("phone", "rider-09-log-service.png", [("ring", "work", (24, 226, 182, 71))])),
      L("It appears in History as a Rider entry, with its details.", ("seq", [(None, ("phone", "rider-10-history.png", [("ring", "rider", "Rider entry")])), ("details", ("phone", "rider-11-record-detail.png", []))])))
scene("3.7", 2, "Rider",
      L("Fuel tracks fill-ups and kilometres per litre.", ("seq", [(None, ("phone", "rider-13-fuel-add.png", [])), ("kilometres", ("phone", "rider-13-fuel.png", [("zoom", "litre", (150, 190, 285, 210), 1.6)]))])))
scene("3.8", 2, "Rider",
      L("Plus a service schedule, renewal reminders, and spending.", ("seq", [(None, ("phone", "rider-12-schedule.png", [])), ("renewal", ("phone", "rider-12-renewals.png", [])), ("spending", ("phone", "rider-12-spending.png", []))])))
# ---------------- Chapter 4: Workshop setup ----------------
scene("4.1", 3, "Workshop owner",
      L("A Workshop owner registers the workshop.", ("phone", "owner-00-register-workshop.png", [("ring", "registers", "Workshop name")])),
      L("RevLog checks every workshop before it can search bikes.", ("phone", "pending-01-waiting-for-approval.png", [("ring", "checks", "Waiting for approval")])))
scene("4.2", 3, "Admin",
      L("The Admin approves it,", ("seq", [(None, ("phone", "admin-01-workshops-pending.png", [("ring", "approves", (176, 264, 364, 72))])), ("it", ("phone", "admin-03-workshop-approved.png", []))])),
      L("and now the workshop can search by plate.", ("phone", "admin-04-pending-owner-now-approved.png", [("ring", "search", (24, 212, 537, 71))])))
scene("4.3", 3, "Workshop owner",
      L("Workshop mode has Search, Customers, Packages and Team.", ("phone", "owner-01-workshop-home.png", [("ring", "search", (0, 1190, 585, 76))])),
      L("Packages save the usual items and costs, ready in one tap.", ("seq", [(None, ("phone", "owner-03-new-package.png", [])), ("ready", ("phone", "owner-03-packages.png", [("ring", "tap", "Minor service")]))])))
scene("4.4", 3, "Workshop owner",
      L("Under Team, the owner adds Branches.", ("seq", [(None, ("phone", "owner-04-team.png", [("ring", "team", (24, 665, 537, 83))])), ("adds", ("phone", "owner-04-add-branch.png", []))])),
      L("The Free plan allows one Branch.", ("phone", "owner-05-limit-reached-branch.png", [("zoom", "free", (40, 500, 505, 310), 1.7)])))
scene("4.5", 3, "Workshop owner",
      L("The owner creates an invite code, and a Staff member joins with it.", ("seq", [(None, ("phone", "owner-08-invite-code.png", [("zoom", "invite", (40, 500, 505, 310), 1.7)])), ("staff", ("phone", "staff-10-join-workshop.png", [("ring", "joins", "Join a workshop")]))])),
      L("The Free plan limits how many staff you can add.", ("phone", "staff-11-joined-workshop-home.png", [])))
# ---------------- Chapter 5: The workshop visit (Set B) ----------------
scene("5.1", 4, "Staff",
      L("Now, a workshop visit. Staff search the plate.", ("duo", ("staff-01-search-plate.png", [("ring", "plate", (24, 116, 537, 77))]), None, "L")),
      L("The bike belongs to a Rider: Approval needed.", ("duo", ("staff-09-approval-needed.png", [("ring", "approval", "Approval needed")]), None, "L")))
scene("5.2", 4, "Rider",
      L("The Rider opens My code: a QR and a 6-digit code, valid for ten minutes, used once.", ("duo", ("staff-09-approval-needed.png", []), ("visit-01-rider-my-code.png", [("ring", "qr", (104, 266, 377, 377)), ("zoom", "valid", (100, 670, 385, 130), 1.6)]), "R")))
scene("5.3", 4, "Staff",
      L("Staff scan it,", ("duo", ("mock", "scan_mycode"), ("visit-01-rider-my-code.png", []), "L"), 3.2),
      L("or type the code and tap Done.", ("duo", ("staff-12-enter-code.png", [("zoom", None, (100, 455, 385, 90), 1.6), ("ring", "type", "Enter rider's code"), ("zoom", "done", (100, 690, 385, 130), 1.6), ("ring", "done", (119, 720, 347, 72))]), ("visit-01-rider-my-code.png", []), "L")))
scene("5.4", 4, "Staff",
      L("The bike opens, with the Rider's first name and the workshop's record.", ("duo", ("staff-13-bike-opens-after-code.png", [("ring", "name", "Rider: Test"), ("ring", "record", (20, 255, 545, 270))]), ("visit-01-rider-my-code.png", []), "L")))
scene("5.5", 4, "Rider",
      L("In the Rider's History, the workshop's record appears with the Workshop badge.", ("duo", ("staff-13-bike-opens-after-code.png", []), ("visit-03-rider-history-workshop-badge.png", [("ring", "badge", (64, 702, 124, 38))]), "R")),
      L("The Rider typed nothing.", ("duo", ("staff-13-bike-opens-after-code.png", []), ("visit-03-rider-history-workshop-badge.png", [("ring", None, (24, 545, 537, 195))]), "R")))
# ---------------- Chapter 6: A bike not in the system ----------------
scene("6.1", 5, "Staff",
      L("A plate not in the system? Staff tap Add this bike, with its brand and model.", ("seq", [(None, ("phone", "staff-02-not-in-system.png", [("ring", "add", (45, 425, 495, 83))])), ("brand", ("phone", "staff-03-new-bike.png", []))])))
scene("6.2", 5, "Staff",
      L("Then a package, the odometer and costs, and Save record.", ("seq", [(None, ("phone", "staff-04-add-service-top.png", [("ring", "package", "Minor service")])), ("odometer", ("phone", "staff-04-add-service-bottom.png", [("ring", "save", (24, 1176, 537, 71))]))])))
scene("6.3", 5, "Staff",
      L("The record carries the workshop's stamp, and Staff show the Claim QR.", ("seq", [(None, ("phone", "staff-05-saved-record-bike-history.png", [("ring", "stamp", (450, 412, 95, 95))])), ("staff", ("phone", "staff-06-claim-qr.png", [("ring", "claim", "Give this QR")]))])))
scene("6.4", 5, "Rider",
      L("The Rider scans the Claim QR,", ("seq", [(None, ("phone", "rider-19-claim-scan.png", [])), ("claim", ("mock", "claim", []))]), 3.8),
      L("and photographs the geran.", ("mock", "geran2", []), 3.2),
      L("Once ownership is confirmed, the bike and the workshop's records are theirs.", ("mock", "geran2_checking", [])))
# ---------------- Chapter 7: Rider controls (Set B) ----------------
scene("7.1", 6, "Rider",
      L("The Rider sees which workshops have access, and can remove one at any time.", ("seq", [(None, ("phone", "rider-24-workshop-access-with-workshop.png", [("ring", "access", "Test Workshop")])), ("remove", ("phone", "rider-26-remove-access-confirm.png", [("ring", "remove", "Remove access?")])), ("time", ("phone", "rider-27-access-removed.png", []))])))
scene("7.2", 6, "Rider",
      L("There are two ways to sell.", ("ways", None)),
      L("Sell to a RevLog rider: the seller types the buyer's Receive code.", ("ways", "A")),
      L("Or Transfer to a buyer: a locked file, opened with a 6-digit code.", ("ways", "B")))
# ---------------- Chapter 8: Admin workflow (Set A rider screens) ----------------
scene("8.1", 7, "Rider",
      L("A bike checked by hand waits as not yet verified.", ("phone", "rider-20-garage-waiting-check.png", [("ring", "verified", "Not yet verified")])))
scene("8.2", 7, "Admin",
      L("The Admin opens the case, compares the names, and approves it.", ("seq", [(None, ("phone", "admin-07-ownership-case-list.png", [("ring", "case", "TEST1234")])), ("compares", ("phone", "admin-08-ownership-case.png", [("zoom", "names", (20, 150, 545, 80), 1.6)])), ("approves", ("phone", "admin-09-approve-confirm.png", [("ring", "approves", (300, 702, 216, 62))]))])))
scene("8.3", 7, "Rider",
      L("After approval, My code appears where Verify this bike was.", ("seq", [(None, ("phone", "rider-21-garage-verified.png", [("ring", "my", (24, 902, 537, 73))])), ("was", ("phone", "rider-22-my-code.png", []))]), 5.2))
scene("8.4", 7, "Admin",
      L("The Admin also sets plans and limits: on the Free plan, 30 bikes and one Branch.", ("phone", "admin-06-settings.png", [("zoom", "free", (170, 110, 400, 250), 1.7)])))
# ---------------- Chapter 9: Privacy ----------------
scene("9.1", 8, None,
      L("A workshop sees your bike only after you approve it.", ("phone", "rider-06-consent.png", [("zoom", None, (24, 222, 537, 200), 1.6), ("zoom", "approve", (24, 425, 537, 172), 1.6)])))
scene("9.2", 8, None,
      L("", ("card", "Your documents", "Licence and geran photos")))
scene("9.3", 8, None,
      L("Document photos are deleted after the check, or kept up to 14 days if checked by hand.", ("phone", "staff-09-approval-needed.png", [])))
# ---------------- Chapter 10: Closing ----------------
scene("10.1", 9, None,
      L("One record for every bike: owned by the Rider, added to by workshops, checked by the Admin.", ("close",)),
      L("RevLog.", ("close", "word")))
