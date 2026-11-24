# BeltFlow Lite – Masters guide. One entry per caption line: (caption, cue, spoken form or omitted).
SCENES = [
 dict(id="s01", title="Intro", step=None, lines=[("Vanakkam, Master!", "hello"), ("Let's learn the app!", "learn")]),
 dict(id="s02", title="Sign in", step=(1, "Sign in"), lines=[("Open the app.", "open"), ("Tap Staff.", "staff"), ("Tap Sign in with Google.", "google")]),
 dict(id="s03", title="Home", step=None, lines=[("This is your home.", "home"), ("See today's classes.", "classes"), ("See payments to check.", "pay"), ("See reminders to send.", "rem")]),
 dict(id="s04", title="Attendance", step=(2, "Attendance"), lines=[("Tap Attendance.", "att"), ("Pick today's class.", "pick")]),
 dict(id="s05", title="Students", step=None, lines=[("Here are your students.", "kids"), ("One tap for each child.", "one")]),
 dict(id="s06", title="All present", step=None, lines=[("Everyone came?", "came"), ("Tap Mark all present.", "mark"), ("So fast!", "fast")]),
 dict(id="s07", title="Absent", step=None, lines=[("Someone absent?", "abs"), ("Tap Absent.", "tapabs"), ("Type why, like Fever.", "why")]),
 dict(id="s08", title="Submit", step=None, lines=[("Tap Submit.", "submit"), ("Done!", "done"), ("The parent gets a message.", "msg")]),
 dict(id="s09", title="Payments", step=(3, "Check payments"), lines=[("Parents send fee receipts here.", "here"), ("Tap View receipt.", "view"), ("Money came? Tap Acknowledge.", "ack"), ("Wrong? Tap Reject.", "rej")]),
 dict(id="s10", title="Reminders", step=(4, "Send reminders"), lines=[("Reminders are ready messages.", "ready"), ("Tap Send.", "send"), ("WhatsApp opens.", "wa"), ("Press send!", "press")]),
 dict(id="s11", title="More", step=(5, "More tools"), lines=[("Tap More for extra tools.", "more")]),
 dict(id="s12", title="Gradings", step=None, lines=[("Belt test coming?", "test"), ("Tick the students.", "tick"), ("Tap Nominate.", "nom")]),
 dict(id="s13", title="Belts", step=None, lines=[("Belts shows what each belt must learn.", "belts")]),
 dict(id="s14", title="Notices", step=None, lines=[("Want to tell parents news?", "news"), ("Write a notice.", "write"), ("Tap Post.", "post")]),
 dict(id="s15", title="Profile", step=None, lines=[("In Profile, see all your classes.", "classes"), ("Type your bank name and account number.", "bank"), ("Tap Save.", "save"), ("Parents will see it when they pay!", "see")]),
 dict(id="s16", title="Outro", step=None, lines=[("Great job, Master!", "great"), ("Your students are lucky.", "lucky"), ("Vanakkam!", "bye")]),
]
EXTRA = {"s01": {"learn": 1.2}, "s02": {"staff": 0.6, "google": 2.2}, "s03": {"home": 0.6, "classes": 0.6, "pay": 0.6, "rem": 1.2},
         "s04": {"att": 0.6, "pick": 1.4}, "s05": {"kids": 0.6, "one": 1.6}, "s06": {"mark": 1.6, "fast": 1.0}, "s07": {"tapabs": 0.8, "why": 1.6},
         "s08": {"submit": 0.8, "done": 0.8, "msg": 1.8}, "s09": {"here": 1.4, "view": 1.8, "ack": 1.8, "rej": 2.4}, "s10": {"ready": 0.8, "send": 1.2, "wa": 0.6, "press": 2.4},
         "s11": {"more": 2.2}, "s12": {"test": 0.4, "tick": 1.6, "nom": 1.6}, "s13": {"belts": 3.0}, "s14": {"news": 0.4, "write": 2.0, "post": 1.6},
         "s15": {"classes": 1.0, "bank": 1.6, "save": 1.4, "see": 1.6}, "s16": {"bye": 2.2}}
