# BeltFlow Lite parents & students guide. One entry per caption line: (caption, cue, spoken form or omitted).
# Short, simple sentences for children. Scenes follow the creator's list; "step" scenes open with a Step N title card.
SCENES = [
 dict(id="s01", title="Intro", step=None, lines=[("Hello! Vanakkam!", "hello"), ("Let's learn our Silambam app together!", "learn")]),
 dict(id="s02", title="Open the app", step=(1, "Sign in"), lines=[("Open the app.", "open"), ("Tap Parent or Student.", "tap")]),
 dict(id="s03", title="Sign in", step=None, lines=[("Type your phone number.", "phone"), ("Then your secret 6-number PIN.", "pin", "Then your secret six number pin."), ("Tap Sign in!", "signin")]),
 dict(id="s04", title="Language", step=None, lines=[("You can pick English, Malay or Tamil!", "lang")]),
 dict(id="s05", title="My children", step=(2, "See your child"), lines=[("Here are your children.", "kids"), ("See their belt colour.", "belt"), ("See how many classes they came.", "count")]),
 dict(id="s06", title="Child details", step=None, lines=[("Tap a name to see more.", "tapname"), ("Green means came.", "green"), ("Red means absent.", "red"), ("Orange means late.", "orange"), ("See belt tests here too!", "grading")]),
 dict(id="s07", title="Pay the fee", step=(3, "Pay the fee"), lines=[("Time to pay the fee?", "fee"), ("Tap Pay.", "pay"), ("You can see the Master's bank account.", "bank"), ("Tap Copy!", "copy")]),
 dict(id="s08", title="Send receipt", step=None, lines=[("Paid by bank?", "paid"), ("Take a photo of your receipt.", "photo"), ("Tap Send to Master.", "send")]),
 dict(id="s09", title="Wait", step=None, lines=[("Now we wait.", "wait"), ("The Master checks it.", "check"), ("Then it turns green!", "turns")]),
 dict(id="s10", title="Notices", step=(4, "News and belts"), lines=[("Notices tell you news.", "news"), ("Like belt test day!", "testday")]),
 dict(id="s11", title="Belts", step=None, lines=[("Belts shows what to learn.", "learn"), ("Learn these, then get your next belt!", "next")]),
 dict(id="s12", title="Students", step=(5, "Students and sign out"), lines=[("Students can sign in too,", "students"), ("with their own phone.", "own")]),
 dict(id="s13", title="Sign out", step=None, lines=[("All done?", "done"), ("Tap Sign out.", "out")]),
 dict(id="s14", title="Home screen", step=None, lines=[("Tip! Put the app on your home screen.", "tip"), ("Open the menu in your browser.", "menu"), ("Tap Add to Home screen.", "add"), ("Now it is just one tap away!", "icon")]),
 dict(id="s15", title="Outro", step=None, lines=[("Great job!", "great"), ("See you at class!", "see"), ("Vanakkam!", "bye")]),
]
# extra seconds after a line, for the motion to play out
EXTRA = {"s01": {"learn": 1.2}, "s02": {"tap": 1.0}, "s03": {"pin": 0.6, "signin": 1.4}, "s04": {"lang": 2.4}, "s05": {"count": 1.6},
         "s06": {"tapname": 0.8, "orange": 0.6, "grading": 1.4}, "s07": {"pay": 0.6, "bank": 0.8, "copy": 1.0}, "s08": {"photo": 0.6, "send": 1.6},
         "s09": {"check": 0.6, "turns": 1.6}, "s10": {"testday": 1.4}, "s11": {"learn": 0.6, "next": 2.2}, "s12": {"own": 1.4}, "s13": {"out": 1.2}, "s14": {"tip": 0.6, "menu": 1.6, "add": 2.0, "icon": 2.0}, "s15": {"bye": 2.2}}
