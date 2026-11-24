scenes = []; MASCOT = []                     # (abs t, action)
def M(S, t, act): MASCOT.append((R(S.start + t), act))
TIP = f"left:250px;top:1580px;width:580px;padding:22px 30px;border-radius:30px 30px 30px 6px;background:{CARD};color:{PLUM};font-size:38px;font-weight:700;line-height:1.25;box-shadow:0 18px 40px rgba(0,0,0,.4)"
WABUB = lambda title, body: (f'<div style="padding:24px 30px;border-radius:28px 28px 28px 6px;background:#dcf8c6;color:#0b3d2e;box-shadow:0 18px 40px rgba(0,0,0,.4);width:560px">'
                             f'<div style="font-size:28px;font-weight:800;color:#128c7e">{title}</div><div style="font-size:34px;font-weight:700;margin-top:6px;line-height:1.25">{body}</div></div>')
def fly_in(S, eid, t, x0, y0, sc=0.3):
    S.gs(f"#{eid}", {"opacity": 0, "scale": sc, "x": x0, "y": y0, "transformOrigin": "0% 100%"})
    S.tw(f"#{eid}", t, 0.8, {"opacity": 1, "scale": 1, "x": 0, "y": 0}, "back.out(1.5)"); S.sfx(t, "curated/ui-pop.wav", -14)
def counter_chip(S, eid, t, frm, to, total, x=640, y=200, cls="chip am"):
    S.add(eid, f'<span id="{eid}n">{frm}</span>/{total}', f"left:{x}px;top:{y}px;font-size:72px", cls, t, S.dur, "pop")
    S.count(f"{eid}n", t + 0.3, 1.2, to, start=frm)

# ---------------- 01 INTRO ----------------
S = Scene("s01"); scenes.append(S)
S.add("stk", stick_svg(620, 40), "left:230px;top:520px;width:620px;height:40px", "a")
S.gs("#stk", {"rotation": -360}); S.tw("#stk", 0.0, 1.4, {"rotation": 0}, "power3.out")
S.js.append('tl.to("#stk",{rotation:-8,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:2},1.5);'); S.sfx(0.1, "curated/metallic-riser.wav", -22)
S.add("tw0", "BeltFlow", f"left:0;top:620px;width:1080px;text-align:center;font-size:96px;font-weight:800;color:{AMBER}", "a")
S.add("tbf", "Master's Guide", "left:0;top:740px;width:1080px;text-align:center;font-size:132px;font-weight:800;letter-spacing:-3px;line-height:1", "a")
S.ft("#tw0", 0.0, 0.7, {"y": 30}, {"y": 0}, "power3.out"); S.ft("#tbf", 0.0, 0.9, {"scale": 0.9}, {"scale": 1}, "back.out(2)")
S.add("crown", '<svg width="150" height="110" viewBox="0 0 30 22"><path d="M2 20 L4 6 L10 12 L15 2 L20 12 L26 6 L28 20 Z" fill="#ff9e1b" stroke="#fff" stroke-width="1.2" stroke-linejoin="round"/></svg>',
      "left:465px;top:900px", "a", 0.9, None, "pop", ("clean-ding.wav", -20))
S.add("you", "You are the Master!", f"left:0;top:1060px;width:1080px;text-align:center;font-size:58px;font-weight:800", "a", 1.3, None, "up")
for i, col in enumerate(BELTS):
    S.add(f"ib{i}", belt_svg(col, 130), f"left:{75 + i * 160}px;top:1160px", "a", 1.6 + 0.15 * i, None, "pop", ("tick.wav", -26))
M(S, 0.6, "wave"); M(S, S.c("learn"), "cheer")

# ---------------- 02 SIGN IN ----------------
S = Scene("s02"); scenes.append(S); S.step_card(1, "Sign in")
S.phone_on([("a", "01-login-staff-google.png", 1688)], t_in=1.1)
G = ('<div style="width:100%;height:100%;border-radius:40px;border:2px solid #dadce0;background:#fff;display:flex;align-items:center;justify-content:center;gap:12px;font-weight:700;font-size:20px;color:#3c4043">'
     '<svg width="24" height="24" viewBox="0 0 24 24"><path d="M21.6 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3z" fill="#4285F4"/><path d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22z" fill="#34A853"/><path d="M6.4 14a6 6 0 0 1 0-3.9V7.5H3.1a10 10 0 0 0 0 9z" fill="#FBBC05"/><path d="M12 6c1.5 0 2.8.5 3.8 1.5l2.9-2.9A10 10 0 0 0 3.1 7.5l3.3 2.6C7.2 7.8 9.4 6 12 6z" fill="#EA4335"/></svg>'
     'Sign in with Google</div>')
S.ov("a", f'<div id="gbtn" class="a" style="left:{R(110 * K)}px;top:{R(880 * K)}px;width:{R(560 * K)}px;height:{R(86 * K)}px">{G}</div>')
S.push(S.c("staff", -0.2), 551, 749, 1.9); S.hl("a", "h1", (400, 720, 740, 780), S.c("staff"), S.c("google"), r=20)
S.tap("a", "t1", 551, 749, S.w("staff", 1, 0.1))
S.push(S.c("google", -0.2), 390, 923, 1.9, 0.6); S.hl("a", "h2", (100, 872, 680, 974), S.c("google"), S.dur, r=40)
S.tap("a", "t2", 390, 923, S.w("google", 2, 0.1))
S.add("tip", f'<b style="color:{AMBER}">Tip:</b> Use the Gmail<br>you gave the Admin.', TIP, "a", S.c("google", 0.4), S.dur, "pop", ("curated/ui-pop.wav", -20))
M(S, S.c("open"), "point"); M(S, S.w("google", 2, 0.3), "cheer")

# ---------------- 03 HOME ----------------
S = Scene("s03"); scenes.append(S)
S.phone_on([("a", "02b-master-home-full.png", 2216)])
S.hl("a", "h0", (40, 200, 740, 480), S.c("home", 0.2), S.c("classes"))
S.add("hi", 'Vanakkam, Master!', "left:540px;top:200px;font-size:40px", "chip am", S.c("home", 0.4), S.c("classes"), "pop")
S.scroll("a", S.c("classes", -0.5), 1.0, 640); S.hl("a", "h1", (30, 1290, 760, 1530), S.c("classes", 0.3), S.c("pay"))
S.scroll("a", S.c("pay", -0.5), 0.9, 300)
S.hl("a", "h2", (40, 665, 390, 880), S.c("pay", 0.2), S.c("rem"))
S.add("p1", '<span id="p1n">0</span> to check', "left:600px;top:200px;font-size:48px", "chip am", S.c("pay", 0.4), S.c("rem"), "pop"); S.count("p1n", S.c("pay", 0.6), 0.8, 1)
S.hl("a", "h3", (410, 665, 745, 880), S.c("rem", 0.2), S.dur)
S.add("bell", '<svg width="110" height="110" viewBox="0 0 24 24"><path d="M12 3a6 6 0 0 0-6 6v4l-2 3h16l-2-3V9a6 6 0 0 0-6-6z" fill="#ff9e1b" stroke="#1f1435" stroke-width="1.4"/><circle cx="12" cy="19.5" r="2" fill="#ff9e1b" stroke="#1f1435" stroke-width="1.4"/></svg>',
      "left:880px;top:220px", "a", S.c("rem", 0.3), S.dur, "pop")
S.js.append(f'tl.to("#bell",{{rotation:18,duration:0.18,ease:"sine.inOut",yoyo:true,repeat:5,transformOrigin:"50% 10%"}},{R(S.c("rem", 0.8))});')
M(S, S.c("home"), "wave"); M(S, S.c("pay"), "point")

# ---------------- 04 ATTENDANCE ----------------
S = Scene("s04"); scenes.append(S); S.step_card(2, "Attendance")
S.phone_on([("a", "02-master-home.png", 1688), ("b", "03-attendance-today.png", 1688)], t_in=1.1)
S.push(S.c("att", -0.2), 240, 1630, 1.8); S.ring("a", "rg", 240, 1625, S.c("att"), 2, 90); S.tap("a", "t1", 240, 1625, S.w("att", 1, 0.1))
S.swap("a", "b", S.w("att", 1, 0.5), "fade"); S.pull(S.w("att", 1, 0.5))
S.push(S.c("pick", -0.1), 390, 366, 1.8); S.hl("b", "h1", (35, 305, 750, 430), S.c("pick"), S.dur, r=20)
S.tap("b", "t2", 300, 366, S.w("pick", 2, 0.2))
S.add("clk", '19:00 · Kids Class', "left:520px;top:200px;font-size:42px", "chip", S.c("pick", 0.3), S.dur, "pop", ("curated/ui-pop.wav", -20))
M(S, S.c("att"), "point")

# ---------------- 05 STUDENTS ----------------
S = Scene("s05"); scenes.append(S)
S.phone_on([("a", "06b-attendance-full.png", 2766)])
S.ov("a", f'<div id="cover" class="a" style="left:0;top:0;width:500px;height:{R(2766 * K)}px"><img src="assets/screens/04-attendance-class-list.png" style="display:block;width:500px" alt=""></div>')
S.hl("a", "h0", (30, 700, 750, 960), S.c("kids", 0.2), S.c("one"))
S.add("kc", '<span id="kcn">0</span> students', "left:620px;top:200px;font-size:48px", "chip am", S.c("kids", 0.4), S.dur, "pop"); S.count("kcn", S.c("kids", 0.6), 1.0, 5)
S.push(S.c("one", -0.2), 390, 895, 1.9); S.hl("a", "h1", (75, 860, 715, 930), S.c("one"), S.dur, r=18)
S.ring("a", "r1", 154, 895, S.c("one", 0.4), 2, 70); S.ring("a", "r2", 301, 895, S.c("one", 0.8), 2, 70); S.ring("a", "r3", 472, 895, S.c("one", 1.2), 2, 70); S.ring("a", "r4", 635, 895, S.c("one", 1.6), 2, 70)
S.add("ptg", f'<span style="color:{GREEN}">Present</span> · <span style="color:{RED}">Absent</span> · <span style="color:{ORANGE}">Late</span> · Excused', "left:130px;top:1180px;font-size:40px", "chip", S.c("one", 0.6), S.dur, "pop")
M(S, S.c("kids"), "point")

# ---------------- 06 ALL PRESENT ----------------
S = Scene("s06"); scenes.append(S)
S.phone_on([("a", "04-attendance-class-list.png", 1688), ("b", "05-attendance-all-present.png", 1688)])
S.hl("a", "h0", (40, 360, 750, 450), S.c("came", 0.1), S.c("mark", 0.4), r=20)
S.push(S.c("mark", -0.2), 270, 404, 1.9); S.tap("a", "t1", 272, 404, S.w("mark", 1, 0.1))
S.swap("a", "b", S.w("mark", 1, 0.45), "fade")
counter_chip(S, "cc", S.w("mark", 1, 0.4), 0, 5, 5, 620, 200)
S.pull(S.w("mark", 3, 0.3)); S.hl("b", "h1", (60, 700, 740, 1560), S.c("fast"), S.dur)
S.add("fast", f'<span style="font-size:60px">⚡</span> 1 tap!', "left:640px;top:330px;font-size:56px", "chip gr", S.c("fast"), S.dur, "pop", ("clean-ding.wav", -16))
M(S, S.c("came"), "talk"); M(S, S.c("fast"), "cheer")

# ---------------- 07 ABSENT ----------------
S = Scene("s07"); scenes.append(S)
S.phone_on([("a", "05-attendance-all-present.png", 1688), ("b", "06-attendance-absent-reason.png", 1688)])
S.hl("a", "h0", (60, 1010, 740, 1250), S.c("abs", 0.1), S.c("tapabs", 0.4))
S.push(S.c("tapabs", -0.2), 317, 1205, 1.9); S.tap("a", "t1", 317, 1205, S.w("tapabs", 1, 0.1))
S.swap("a", "b", S.w("tapabs", 1, 0.45), "fade")
S.add("ab", "Absent", "left:640px;top:200px;font-size:56px", "chip rd", S.w("tapabs", 1, 0.4), S.dur, "pop")
S.push(S.c("why", -0.2), 390, 1334, 1.9, 0.6); S.hl("b", "h1", (80, 1290, 715, 1380), S.c("why"), S.dur, r=18)
S.ov("b", f'<div id="fv" class="a" style="left:{R(104 * K)}px;top:{R(1310 * K)}px;width:{R(300 * K)}px;height:{R(50 * K)}px;background:#fff8f2;font-size:22px;font-weight:600;color:#1f1435;line-height:{R(50 * K)}px;padding-left:4px">{"".join(f"<span id=fk{i}>{ch}</span>" for i, ch in enumerate("Fever"))}</div>')
for i in range(5):
    S.gs(f"#fk{i}", {"opacity": 0}); S.st(f"#fk{i}", S.w("why", 3, 0.1 * i), {"opacity": 1}); S.sfx(S.w("why", 3, 0.1 * i), "typing-tick.wav", -22)
S.add("thm", '<svg width="80" height="140" viewBox="0 0 16 28"><rect x="5" y="1" width="6" height="20" rx="3" fill="#fff" stroke="#1f1435" stroke-width="1.4"/><circle cx="8" cy="22" r="5" fill="#ef4444" stroke="#1f1435" stroke-width="1.4"/><rect x="6.6" y="8" width="2.8" height="13" fill="#ef4444"/></svg>',
      "left:900px;top:330px", "a", S.w("why", 3, 0.2), S.dur, "pop")
M(S, S.c("abs"), "talk")

# ---------------- 08 SUBMIT ----------------
S = Scene("s08"); scenes.append(S)
S.phone_on([("a", "06-attendance-absent-reason.png", 1688), ("b", "06c-attendance-saved.png", 1688)])
S.push(S.c("submit", -0.2), 416, 1612, 1.7); S.tap("a", "t1", 416, 1612, S.w("submit", 1, 0.1))
S.swap("a", "b", S.w("submit", 1, 0.45), "fade"); S.hl("b", "h1", (35, 1575, 745, 1650), S.w("submit", 1, 0.5), S.c("msg"), r=24)
S.pull(S.c("done", -0.1)); S.burst("ok", 540, 760, S.c("done"))
S.add("msg", WABUB("BeltFlow · to parent", "Bala Kumar was absent today (Fever)."), "left:250px;top:1560px", "a", None, S.dur); fly_in(S, "msg", S.c("msg", 0.2), -150, -550)
M(S, S.c("done"), "cheer")

# ---------------- 09 PAYMENTS ----------------
S = Scene("s09"); scenes.append(S); S.step_card(3, "Check payments")
S.phone_on([("a", "07-payments-to-check.png", 1688)], t_in=1.1)
for i in range(4):
    it = (f'<div style="width:80px;height:100px;border-radius:8px;background:#fff;border:3px solid {PLUM};padding:10px"><div style="height:7px;background:#ccc;margin:7px 0"></div><div style="height:7px;background:#ccc;margin:7px 0"></div><div style="height:7px;background:{AMBER};margin:7px 0"></div></div>'
          if i == 0 else f'<div style="width:64px;height:64px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffe08a,{AMBER});border:3px solid #b86a00;color:#7a3e00;font-size:22px;font-weight:800;display:flex;align-items:center;justify-content:center">RM</div>')
    S.add(f"fly{i}", it, "left:60px;top:260px", "a"); S.gs(f"#fly{i}", {"opacity": 0, "scale": 0.5})
    t0 = S.c("here", 0.3) + 0.2 * i
    S.tw(f"#fly{i}", t0, 0.25, {"opacity": 1, "scale": 1}, "back.out(2)"); S.tw(f"#fly{i}", t0, 1.0, {"x": 380 + 20 * i}, "power1.inOut")
    S.js.append(f'tl.to("#fly{i}",{{y:300,duration:1.0,ease:"back.in(1.1)"}},{R(t0)});'); S.tw(f"#fly{i}", t0 + 0.9, 0.2, {"opacity": 0, "scale": 0.3}, "power2.in"); S.sfx(t0 + 0.95, "tick.wav", -20)
S.hl("a", "h0", (20, 360, 760, 640), S.c("here", 1.2), S.c("view"))
S.push(S.c("view", -0.2), 181, 491, 2.0); S.tap("a", "t1", 181, 491, S.w("view", 1, 0.2))
S.add("rcp", f'''<div style="width:440px;padding:30px 34px;border-radius:18px;background:#fff;color:{PLUM};box-shadow:0 30px 60px rgba(0,0,0,.5)">
  <div style="font-size:26px;font-weight:800;color:#f5b301">Maybank2u</div><div style="font-size:30px;font-weight:800;margin-top:10px">Transfer successful</div>
  <div style="font-size:64px;font-weight:800;margin-top:10px">RM 50.00</div><div style="font-size:24px;opacity:.7;margin-top:8px">To: Ravi a/l Muthu</div><div style="font-size:24px;opacity:.7">Ref: Fee 2026-11 · Arjun</div></div>''',
      "left:320px;top:560px", "a", S.w("view", 1, 0.6), S.c("ack", 0.2), "pop", ("curated/ui-pop.wav", -16))
S.push(S.c("ack", -0.2), 432, 491, 2.0, 0.6); S.tap("a", "t2", 432, 491, S.w("ack", 3, 0.1))
S.ov("a", f'<div id="ackd" class="a" style="left:{R(30 * K)}px;top:{R(370 * K)}px;width:{R(720 * K)}px;height:{R(270 * K)}px;border-radius:14px;background:rgba(236,253,245,.96);border:4px solid {GREEN};display:flex;align-items:center;justify-content:center;gap:14px;color:#065f46;font-weight:800;font-size:30px">'
          f'<span style="width:44px;height:44px;border-radius:50%;background:{GREEN};padding:8px;display:block">{tick_svg()}</span>Paid · RM 50</div>')
S.gs("#ackd", {"opacity": 0, "scale": 0.7}); S.tw("#ackd", S.w("ack", 3, 0.4), 0.5, {"opacity": 1, "scale": 1}, "back.out(2)"); S.tw("#ackd", S.c("rej", -0.3), 0.3, {"opacity": 0}, "power2.in")
S.pull(S.w("ack", 3, 0.6)); S.burst("ok", 540, 1180, S.w("ack", 3, 0.6), 26, tick=False); S.sfx(S.w("ack", 3, 0.6), "clean-ding.wav", -14)
S.push(S.c("rej", -0.2), 141, 592, 2.0, 0.6); S.hl("a", "h2", (80, 560, 200, 625), S.c("rej"), S.dur, r=14)
S.add("rj", "Reject = send back", "left:520px;top:200px;font-size:44px", "chip rd", S.w("rej", 2), S.dur, "pop")
S.add("tip", f'<b style="color:{AMBER}">Cash too!</b><br>Acknowledge cash when you get it.', TIP, "a", S.c("rej", 0.6), S.dur, "pop", ("curated/ui-pop.wav", -20))
M(S, S.c("here"), "point"); M(S, S.w("ack", 3, 0.6), "cheer")

# ---------------- 10 REMINDERS ----------------
S = Scene("s10"); scenes.append(S); S.step_card(4, "Send reminders")
S.phone_on([("a", "08-reminders.png", 1688)], t_in=1.1)
S.hl("a", "h0", (20, 360, 760, 790), S.c("ready", 0.2), S.c("send"))
S.push(S.c("send", -0.2), 152, 737, 2.0); S.tap("a", "t1", 152, 737, S.w("send", 1, 0.1)); S.pull(S.w("send", 1, 0.5))
S.add("wa", WABUB("WhatsApp · Bala's parent", "Bala Kumar was marked absent today."), "left:250px;top:1560px", "a", None, S.dur); fly_in(S, "wa", S.c("wa"), -150, -550)
S.add("snd", f'<div style="width:130px;height:130px;border-radius:50%;background:#25d366;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px rgba(0,0,0,.4)"><svg width="64" height="64" viewBox="0 0 24 24"><path d="M3 20l18-8L3 4l2 7 9 1-9 1z" fill="#fff"/></svg></div>',
      "left:860px;top:1500px", "a", S.c("press", -0.2), S.dur, "pop")
S.add("tf", FINGER, "left:900px;top:1560px;width:120px;height:150px", "a"); S.gs("#tf", {"opacity": 0, "x": 120, "y": 160})
S.tw("#tf", S.c("press", 0.1), 0.5, {"opacity": 1, "x": 0, "y": 0}, "power3.out"); S.tw("#tf", S.w("press", 1, 0.2), 0.12, {"scale": 0.86}, "power2.in"); S.tw("#tf", S.w("press", 1, 0.32), 0.2, {"scale": 1}, "back.out(3)")
S.sfx(S.w("press", 1, 0.32), "curated/ui-click.wav", -12); S.tw("#wa", S.w("press", 1, 0.5), 0.7, {"x": 400, "y": -900, "opacity": 0, "scale": 0.4}, "power2.in"); S.sfx(S.w("press", 1, 0.5), "curated/zoom-swish.wav", -18)
S.add("tip", f'<b style="color:{AMBER}">Emails</b> go out by themselves<br>every evening.', "left:250px;top:200px;width:580px;padding:22px 30px;border-radius:30px 30px 30px 6px;background:#f7f5fa;color:#1f1435;font-size:38px;font-weight:700;line-height:1.25;box-shadow:0 18px 40px rgba(0,0,0,.4)",
      "a", S.c("press", 0.8), S.dur, "pop", ("curated/ui-pop.wav", -20))
M(S, S.c("ready"), "talk"); M(S, S.w("press", 1, 0.5), "cheer")

# ---------------- 11 MORE ----------------
S = Scene("s11"); scenes.append(S); S.step_card(5, "More tools")
S.phone_on([("a", "07-payments-to-check.png", 1688), ("b", "09-more-menu.png", 1688)], t_in=1.1)
S.push(S.c("more", -0.3), 692, 1640, 1.8); S.tap("a", "t1", 692, 1640, S.w("more", 1, 0.1)); S.swap("a", "b", S.w("more", 1, 0.45), "fade"); S.pull(S.w("more", 1, 0.5))
for i, (y0, y1) in enumerate(((365, 600), (705, 920), (1030, 1130))):
    S.hl("b", f"h{i}", (30, y0, 750, y1), S.w("more", 1, 0.9 + 0.5 * i), S.dur)
S.add("tl", "Gradings · Belts · Notices · Profile", "left:120px;top:1180px;font-size:38px", "chip", S.w("more", 1, 1.0), S.dur, "pop")
M(S, S.c("more"), "point")

# ---------------- 12 GRADINGS ----------------
S = Scene("s12"); scenes.append(S)
S.phone_on([("a", "10-gradings.png", 1688)])
S.hl("a", "h0", (40, 250, 740, 1190), S.c("test", 0.1), S.c("tick"))
S.push(S.c("tick", -0.2), 390, 760, 1.45)
for i, (y, t) in enumerate(((604, S.w("tick", 0, 0.3)), (929, S.w("tick", 2, 0.2)))):
    S.ov("a", f'<div id="cb{i}" class="a" style="left:{R(68 * K)}px;top:{R((y - 22) * K)}px;width:{R(44 * K)}px;height:{R(44 * K)}px;border-radius:6px;background:{AMBER};padding:3px">{tick_svg()}</div>')
    S.gs(f"#cb{i}", {"opacity": 0, "scale": 0.3}); S.tw(f"#cb{i}", t, 0.35, {"opacity": 1, "scale": 1}, "back.out(3)"); S.sfx(t, "curated/ui-click.wav", -14)
S.add("blt", f'<div style="display:flex;align-items:center;gap:14px">{belt_svg(BELTS[1], 90)}<span style="font-size:50px">→</span>{belt_svg(BELTS[2], 90)}</div>', "left:560px;top:200px", "chip", S.c("tick", 0.6), S.dur, "pop")
S.push(S.c("nom", -0.3), 388, 1154, 1.8, 0.6); S.tap("a", "t1", 388, 1154, S.w("nom", 1, 0.1)); S.pull(S.w("nom", 1, 0.5))
S.hl("a", "h1", (40, 1240, 740, 1530), S.w("nom", 1, 0.6), S.dur); S.burst("ok", 540, 760, S.w("nom", 1, 0.6))
M(S, S.c("test"), "talk"); M(S, S.w("nom", 1, 0.6), "cheer")

# ---------------- 13 BELTS ----------------
S = Scene("s13"); scenes.append(S)
S.phone_on([("a", "11-belts.png", 1688)])
S.hl("a", "h0", (20, 245, 760, 480), S.c("belts", 0.2), S.c("belts", 1.6))
S.push(S.c("belts", 1.5), 390, 1000, 1.25, 1.2)
for i, col in enumerate(BELTS):
    S.add(f"lb{i}", belt_svg(col, 150), f"left:880px;top:{1180 - i * 170}px", "a", S.c("belts", 0.3 + 0.35 * i), None, "up", ("tick.wav", -22))
S.add("star", f'<svg width="110" height="110" viewBox="0 0 24 24"><path d="M12 2l2.9 6.2 6.8.7-5.1 4.6 1.5 6.7L12 16.8 5.9 20.2l1.5-6.7L2.3 8.9l6.8-.7z" fill="{AMBER}" stroke="#fff" stroke-width="1"/></svg>',
      "left:900px;top:150px", "a", S.c("belts", 2.5), None, "pop", ("clean-ding.wav", -16))
S.js.append(f'tl.to("#star",{{rotation:360,duration:2,ease:"power1.inOut"}},{R(S.c("belts", 2.8))});')
M(S, S.c("belts"), "point")

# ---------------- 14 NOTICES ----------------
S = Scene("s14"); scenes.append(S)
S.phone_on([("a", "12-notices-post.png", 1688)])
S.hl("a", "h0", (40, 250, 740, 1000), S.c("news", 0.1), S.c("write"))
S.push(S.c("write", -0.2), 390, 640, 1.6)
def typ(eid, x, y, w, h, text, t, size=22, rate=0.07):
    S.ov("a", f'<div id="{eid}" class="a" style="left:{R(x * K)}px;top:{R(y * K)}px;width:{R(w * K)}px;height:{R(h * K)}px;font-size:{size}px;font-weight:600;color:#1f1435;line-height:1.3">{"".join(f"<span id={eid}k{i}>{c}</span>" for i, c in enumerate(text))}</div>')
    for i in range(len(text)):
        S.gs(f"#{eid}k{i}", {"opacity": 0}); S.st(f"#{eid}k{i}", t + rate * i, {"opacity": 1})
        if i % 2 == 0: S.sfx(t + rate * i, "typing-tick.wav", -24)
typ("tt", 92, 575, 580, 40, "Belt test on Sunday!", S.c("write", 0.2))
typ("tm", 92, 738, 580, 120, "Come at 8am in uniform.", S.c("write", 1.7), 20, 0.05)
S.push(S.c("post", -0.2), 390, 957, 1.8, 0.6); S.tap("a", "t1", 390, 957, S.w("post", 1, 0.1)); S.pull(S.w("post", 1, 0.5)); S.burst("ok", 540, 760, S.w("post", 1, 0.55))
S.add("ntc", WABUB("New notice", "Belt test on Sunday!"), "left:250px;top:1560px", "a", None, S.dur); fly_in(S, "ntc", S.w("post", 1, 0.8), -150, -550)
M(S, S.c("news"), "talk"); M(S, S.w("post", 1, 0.55), "cheer")

# ---------------- 15 PROFILE ----------------
S = Scene("s15"); scenes.append(S)
S.phone_on([("a", "13b-profile-full.png", 1786)])
S.hl("a", "h0", (30, 300, 750, 560), S.c("classes", 0.2), S.c("bank"))
S.push(S.c("bank", -0.2), 390, 1000, 1.3); S.hl("a", "h1", (40, 590, 740, 1240), S.c("bank", 0.1), S.c("save"))
for i, (y, t) in enumerate(((885, S.w("bank", 2, 0)), (1210, S.w("bank", 5, 0)))):
    S.ring("a", f"bk{i}", 380, y, t, 2, 110)
S.push(S.c("save", -0.3), 391, 1494, 1.8, 0.6); S.tap("a", "t1", 391, 1494, S.w("save", 1, 0.1)); S.pull(S.w("save", 1, 0.5)); S.burst("ok", 540, 760, S.w("save", 1, 0.55))
S.add("pp", f'''<div style="padding:22px 28px;border-radius:22px;background:{PLUM};border:3px solid {AMBER};box-shadow:0 18px 40px rgba(0,0,0,.45);width:520px">
   <div style="font-size:26px;font-weight:800;color:{AMBER}">Parents see · Pay to</div><div style="font-size:32px;font-weight:800;margin-top:6px">Maybank · Ravi a/l Muthu</div>
   <div style="font-size:40px;font-weight:800;margin-top:4px;letter-spacing:2px">1621 2345 6789</div></div>''', "left:270px;top:1560px", "a", None, S.dur)
fly_in(S, "pp", S.c("see", 0.1), -150, -550)
M(S, S.c("classes"), "point"); M(S, S.c("see", 0.3), "cheer")

# ---------------- 16 OUTRO ----------------
S = Scene("s16"); scenes.append(S)
S.add("lg", f'''<svg width="300" height="300" viewBox="0 0 100 100"><g transform="rotate(-35 50 50)"><rect x="8" y="46" width="84" height="8" rx="4" fill="#c98a4b"/></g><g transform="rotate(35 50 50)"><rect x="8" y="46" width="84" height="8" rx="4" fill="#c98a4b"/></g>
   <rect x="22" y="34" width="56" height="12" rx="4" fill="#fff"/><path d="M45 44 L36 66 L43 66 L50 52 L57 66 L64 66 L55 44 Z" fill="#fff"/><rect x="43" y="31" width="14" height="17" rx="3" fill="#fff"/></svg>''', "left:390px;top:260px", "a")
S.gs("#lg", {"opacity": 0, "scale": 0.2, "rotation": -200}); S.tw("#lg", 0.1, 1.1, {"opacity": 1, "scale": 1, "rotation": 0}, "back.out(1.5)")
S.add("ot", "BeltFlow Lite", f"left:0;top:600px;width:1080px;text-align:center;font-size:110px;font-weight:800;color:{AMBER}", "a", 0.4, None, "pop", ("thock.wav", -18))
S.add("os", "PERSATUAN SILAMBAM DAERAH SEPANG", "left:0;top:740px;width:1080px;text-align:center;font-size:36px;font-weight:800;letter-spacing:3px;opacity:.9", "a", 0.7, None, "up")
S.add("url", "beltflow-lite.vercel.app", "left:220px;top:850px;width:640px;text-align:center;font-size:48px", "chip", 1.0, None, "pop", ("curated/ui-pop.wav", -18))
S.add("tm", "Thank you, Master!", f"left:0;top:1010px;width:1080px;text-align:center;font-size:56px;font-weight:800", "a", 1.4, None, "up")
for i, col in enumerate(BELTS):
    S.add(f"eb{i}", belt_svg(col, 120), f"left:{110 + i * 150}px;top:1130px", "a", 1.6 + 0.12 * i, None, "pop", ("tick.wav", -26))
S.burst("cf", 540, 520, S.c("great", 0.1), 34, tick=False); S.burst("cf2", 540, 520, S.c("bye", 0.1), 34, tick=False)
M(S, S.c("great"), "cheer"); M(S, S.c("bye"), "wave")
