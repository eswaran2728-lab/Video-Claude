# Scenes for build27.py (exec'd inside it). Boxes/points are in the screenshots' own 800x465 pixels.
CX = W / 2
def grid_rects(n=8):
    if O == "h": return [(250 + (i % 4) * 400, LAY["CY"] + (i // 4) * 150, 370, 120) for i in range(n)]
    return [(80 + (i % 2) * 470, 470 + (i // 2) * 150, 440, 120) for i in range(n)]
def tab_grid(S, pre, t0, step, t_out=None, label_nums=True):
    for i, (t, (x, y, w, h)) in enumerate(zip(TABS, grid_rects())):
        S.add(f"{pre}{i}", f'<div style="display:flex;align-items:center;gap:18px;height:100%;padding:0 26px"><span style="width:62px;height:62px;border-radius:50%;background:{AMBER};color:{PLUM2};font-size:34px;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none">{i + 1}</span>'
              f'<span style="font-size:{38 if O == "h" else 40}px;font-weight:800;color:{PLUM};white-space:nowrap">{t}</span><span id="{pre}{i}t" style="margin-left:auto;width:48px;height:48px;border-radius:50%;background:#047857;padding:8px;opacity:0;flex:none">{tick_svg()}</span></div>',
              f"left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:24px;background:{CARD};box-shadow:0 16px 36px rgba(0,0,0,.4)", "a", t0 + step * i, t_out, "pop", ("curated/ui-pop.wav", -20))
def HDR(eid, txt, t_in, t_out=None, top_h=None, col="#fff", fs=60):
    if O == "h": st = f"left:0;top:{top_h if top_h is not None else LAY['CY'] - 150}px;width:{W}px;text-align:center;font-size:{fs}px"
    else: st = f"left:40px;top:300px;width:800px;text-align:center;font-size:{fs - 4}px;line-height:1.15"
    S.add(eid, txt, st + f";font-weight:800;color:{col}", "a", t_in, t_out, "down")
PHONE_ICON = '<svg width="44" height="56" viewBox="0 0 24 32" style="vertical-align:middle;margin-right:10px"><rect x="3" y="1" width="18" height="30" rx="4" fill="none" stroke="#1f1435" stroke-width="2.6"/><circle cx="12" cy="26" r="1.8" fill="#1f1435"/></svg>'

# ---------------- 01 INTRO ----------------
S = Scene("s01"); scenes.append(S); cy = LAY["CY"] - (60 if O == "h" else 0)
S.add("stk", stick_svg(620, 40), f"left:{R(CX - 310)}px;top:{cy - 160}px;width:620px;height:40px", "a")
S.gs("#stk", {"rotation": -360}); S.tw("#stk", 0.0, 1.4, {"rotation": 0}, "power3.out"); S.js.append('tl.to("#stk",{rotation:-8,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:2},1.5);')
S.sfx(0.1, "curated/metallic-riser.wav", -22)
S.add("t1", "Filling the", f"left:0;top:{cy - 70}px;width:{W}px;text-align:center;font-size:{80 if O == 'h' else 84}px;font-weight:800", "a")
S.add("t2", "BeltFlow Sheet", f"left:0;top:{cy + 30}px;width:{W}px;text-align:center;font-size:{150 if O == 'h' else 128}px;font-weight:800;color:{AMBER};letter-spacing:-3px;line-height:1", "a")
S.ft("#t1", 0, 0.7, {"y": 30}, {"y": 0}); S.ft("#t2", 0, 0.9, {"scale": 0.9}, {"scale": 1}, "back.out(2)")
S.add("ic", SHEET_ICON, f"left:{R(CX - 60)}px;top:{cy + 210}px;width:120px;height:120px", "a", 0.6, None, "pop", ("clean-ding.wav", -20))
S.add("sub", "For the Admin &amp; Committee", f"left:0;top:{cy + 350}px;width:{W}px;text-align:center;font-size:48px;font-weight:700;opacity:.9", "a", 1.0, None, "up")
M(S, 0.6, "wave"); M(S, S.c("fill"), "cheer")

# ---------------- 02 TAB MAP ----------------
S = Scene("s02"); scenes.append(S)
HDR("h", "We fill the tabs in this order", 0.3)
tab_grid(S, "g", S.c("order", 0.3), 0.4)
for i, t in enumerate(TABS): TAB(S, S.c("order", 0.3) + 0.4 * i, t, "flash")
S.sfx(S.c("one"), "clean-ding.wav", -18)
M(S, S.c("order"), "point")

# ---------------- 03 CONFIG ----------------
S = Scene("s03"); scenes.append(S); S.tab_card(1, "Config"); TAB(S, 1.1, "Config")
S.laptop([("a", SH("01-config"))], t_in=1.1)
S.push(S.c("name", -0.3), 200, 146, 2.1); S.hl("a", "h1", (30, 138, 332, 154), S.c("name"), S.dur)
PN = "PERSATUAN SILAMBAM DAERAH SEPANG"
S.magcard("mg", "PERSATUAN_NAME", PN, S.c("name", 0.1), S.dur, typed=(S.c("name", 0.4), 0.05))
for i, ch in enumerate(PN):
    if ch != " ": S.sfx(S.c("name", 0.4) + 0.05 * i, "typing-tick.wav", -24)
S.chip("app", f'{PHONE_ICON}On the app header', S.c("shows", 0.1), S.dur, size=34)
M(S, S.c("first"), "point"); M(S, S.c("shows", 0.4), "thumb"); TAB(S, S.dur - 0.2, "Config", "done")

# ---------------- 04 BELTS ----------------
S = Scene("s04"); scenes.append(S); S.tab_card(2, "Belts"); TAB(S, 1.1, "Belts")
S.laptop([("a", SH("02-belts"))], t_in=1.1)
S.hl("a", "h0", (30, 158, 560, 318), S.c("row"), S.c("order"))
S.push(S.c("order", -0.2), 140, 230, 1.7); S.hl("a", "h1", (30, 140, 96, 318), S.c("order"), S.c("code"))
for i in range(3): S.chip(f"n{i}", str(i + 1), S.w("order", 4 + i), S.c("code"), slot=(LAY["chip"][0] + i * 100, LAY["chip"][1]), size=48)
S.push(S.c("code", -0.2), 340, 230, 2.0, 0.7); S.hl("a", "h2", (306, 140, 374, 318), S.c("code"), S.dur)
S.magcard("mg", "Colour", "#FACC15", S.c("code", 0.2), S.c("paints", 0.3))
bl = "".join(f'<span id="pb{i}" style="display:inline-block;margin:0 6px">{belt_svg(c, 110 if O == "h" else 100)}</span>' for i, c in enumerate(BELTS))
S.add("paint", bl, f"left:{LAY['mag'][0]}px;top:{LAY['mag'][1]}px;width:{LAY['mag'][2]}px;padding:24px;border-radius:22px;background:{PLUM};border:4px solid {AMBER};text-align:center", "a", S.c("paints"), None, "pop")
for i in range(6): S.ft(f"#pb{i}", S.c("paints", 0.2 + 0.12 * i), 0.4, {"scale": 0, "rotation": -40}, {"scale": 1, "rotation": 0}, "back.out(2.5)"); S.sfx(S.c("paints", 0.2 + 0.12 * i), "tick.wav", -24)
M(S, S.c("row"), "point"); M(S, S.c("paints", 0.6), "thumb")

# ---------------- 05 NEW BELT ----------------
S = Scene("s05"); scenes.append(S)
S.laptop([("a", GN("02b_base.jpg")), ("b", SH("02b-belts-adding-new-belt"))])
S.push(S.c("new", -0.1), 290, 320, 1.9); S.hl("a", "h0", (28, 310, 540, 332), S.c("new", 0.2), S.c("easy"))
t = S.c("type", 0.2)
for (box, txt, tid) in (((31, 313, 96, 330), "7", "ta"), ((98, 313, 166, 330), "Red", "tb"), ((168, 313, 238, 330), "Merah", "tc"), ((308, 313, 374, 330), "#DC2626", "td"), ((376, 313, 462, 330), "Master level form", "te"), ((465, 313, 536, 330), "36", "tf")):
    t = S.typing("a", tid, box, txt, t, 0.055) + 0.18
S.magcard("mg", "New belt · row 8", "7 · Red · Merah · #DC2626", S.c("type", 0.3), S.c("easy", 0.2))
S.show("b", S.c("easy", -0.1), 0.3); S.pull(S.c("easy")); S.burst("ok", R(CX), R(LY + LH * 0.45), S.c("easy", 0.1))
S.chip("rb", f'<span style="display:inline-block;vertical-align:middle;margin-right:12px">{belt_svg("#DC2626", 90)}</span>Red belt', S.c("easy", 0.3), S.dur, cls="chip", size=36)
M(S, S.c("new"), "talk"); M(S, S.c("easy", 0.2), "thumb"); TAB(S, S.dur - 0.2, "Belts", "done")

# ---------------- 06 MASTERS ----------------
S = Scene("s06"); scenes.append(S); S.tab_card(3, "Masters"); TAB(S, 1.1, "Masters")
S.laptop([("a", SH("03-masters"))], t_in=1.1)
S.push(S.c("write", -0.2), 150, 156, 2.2); S.hl("a", "h1", (30, 137, 266, 171), S.c("write"), S.c("bank"))
S.magcard("mg", "Gmail · Name · Phone", "guru.ravi@gmail.com · Master Ravi · 60121112222", S.c("write", 0.4), S.c("bank"))
S.push(S.c("bank", -0.2), 376, 156, 2.2, 0.7); S.hl("a", "h2", (266, 137, 486, 171), S.c("bank"), S.dur)
S.chip("bk", f'{PHONE_ICON}Bank: Masters add it in the app', S.c("bank", 0.4), S.dur, cls="chip", size=32)
M(S, S.c("write"), "point"); M(S, S.c("bank", 1.0), "thumb"); TAB(S, S.dur - 0.2, "Masters", "done")

# ---------------- 07 CLASSES ----------------
S = Scene("s07"); scenes.append(S); S.tab_card(4, "Classes"); TAB(S, 1.1, "Classes")
S.laptop([("a", SH("04-classes"))], t_in=1.1)
S.hl("a", "h0", (30, 137, 600, 171), S.c("row"), S.c("id"))
S.push(S.c("id", -0.2), 96, 154, 2.4); S.hl("a", "h1", (30, 137, 162, 171), S.c("id"), S.c("place"))
S.magcard("mg", "Class ID · Name", "KIDS · Kids Class", S.c("id", 0.3), S.c("place"))
S.push(S.c("place", -0.2), 410, 154, 1.9, 0.7); S.hl("a", "h2", (282, 137, 560, 171), S.c("place"), S.dur)
S.magcard("mg2", "Place · Time", "Dewan Sungai Pelek · 19:00", S.c("place", 0.3), S.dur)
M(S, S.c("row"), "point")

# ---------------- 08 PICK MASTER ----------------
S = Scene("s08"); scenes.append(S)
S.laptop([("a", GN("04b_base.jpg"))])
S.push(S.c("who", -0.2), 226, 205, 2.3); Zc = S.cam_state
S.hl("a", "h0", (166, 170, 290, 186), S.c("who", 0.1), S.c("arrow", 0.3))
S.tap("a", "t1", 281, 178, S.w("arrow", 2, 0.1)); S.popup("a", "pl", "04b_list.png", (158, 187, 292, 260), S.w("arrow", 2, 0.25))
S.glow("a", "g1", (163, 187, 287, 203), S.c("pick", 0.1)); S.tap("a", "t2", 222, 195, S.w("pick", 2, 0.1))
ex, ey = S.stage_at(222, 195, *Zc); tx, ty = tab_center("Masters")
S.arrow("ar", (tx, ty - 8), (R(ex + 40), R(ey + 18)), S.c("pick", 0.5), S.dur, bend=0.25 if O == "h" else -0.3)
S.chip("fm", "From the Masters tab!", S.c("pick", 0.9), S.dur, cls="chip", size=34)
M(S, S.c("arrow"), "point"); M(S, S.c("pick", 1.2), "thumb"); TAB(S, S.dur - 0.2, "Classes", "done")

# ---------------- 09 STUDENTS ----------------
S = Scene("s09"); scenes.append(S); S.tab_card(5, "Students"); TAB(S, 1.1, "Students")
S.laptop([("a", SH("05-students"))], t_in=1.1)
S.hl("a", "h0", (30, 137, 520, 263), S.c("row"), S.c("ic"))
S.push(S.c("ic", -0.2), 68, 200, 2.0); S.hl("a", "h1", (30, 137, 103, 263), S.c("ic"), S.dur)
S.magcard("mg", "IC number = the student's key", "150312101234", S.c("ic", 0.3), S.dur)
S.chip("tw", "✓ ✓ Check twice!", S.c("twice", 0.1), S.dur, cls="chip gr", size=40)
M(S, S.c("ic"), "talk")

# ---------------- 10 NEW STUDENT ----------------
S = Scene("s10"); scenes.append(S)
S.laptop([("a", GN("05b_base.jpg"))])
S.push(S.c("type", -0.3), 132, 270, 2.2)
t = S.c("type", 0.2)
for box, txt, tid in (((32, 262, 102, 279), "190101101010", "ta"), ((104, 262, 172, 279), "Tharun Kumar", "tb"), ((174, 262, 238, 279), "2019-01-01", "tc")):
    t = S.typing("a", tid, box, txt, t, 0.055) + 0.15
S.magcard("mg", "New student · row 10", "190101101010 · Tharun Kumar", S.c("type", 0.2), S.c("belt", 0.3))
S.push(S.c("belt", -0.3), 276, 340, 1.8, 0.7); Zc = S.cam_state
S.tap("a", "t1", 307, 270, S.w("belt", 1, 0.1)); S.popup("a", "pl", "05b_list.png", (234, 280, 317, 446), S.w("belt", 1, 0.3))
S.glow("a", "g1", (239, 401, 312, 419), S.c("here", 0.2))
ex, ey = S.stage_at(276, 410, *Zc); tx, ty = tab_center("Belts")
S.arrow("ar", (tx, ty - 8), (R(ex + 30), R(ey + 20)), S.c("here", 0.5), S.dur, bend=0.3 if O == "h" else -0.3)
S.chip("nb", f'<span style="display:inline-block;vertical-align:middle;margin-right:12px">{belt_svg("#DC2626", 80)}</span>From the Belts tab!', S.c("here", 0.8), S.dur, cls="chip", size=32)
M(S, S.c("type"), "talk"); M(S, S.c("here", 0.6), "point")

# ---------------- 11 ACTIVE YES ----------------
S = Scene("s11"); scenes.append(S)
S.laptop([("a", GN("05c_base.jpg")), ("b", GN("05c_base2.jpg"))])
S.push(S.c("fee", -0.2), 420, 280, 2.0)
te = S.typing("a", "tf", (308, 262, 384, 279), "40", S.c("fee", 0.4), 0.12); S.show("b", te + 0.4, 0.4)
S.magcard("mg", "Monthly fee (RM)", "40", S.c("fee", 0.2), S.c("yes"))
S.tap("b", "t1", 512, 270, S.w("yes", 0, 0.1)); S.popup("b", "pl", "05c_list.png", (446, 280, 529, 353), S.w("yes", 0, 0.3))
S.glow("b", "g1", (450, 279, 525, 296), S.w("yes", 1, 0.0)); S.chip("ys", "Active: Yes", S.w("yes", 1, 0.1), S.dur, cls="chip gr", size=40)
S.pull(S.c("done", -0.1)); S.burst("ok", R(CX), R(LY + LH * 0.45), S.c("done", 0.1))
M(S, S.c("done", 0.2), "thumb"); TAB(S, S.dur - 0.2, "Students", "done")

# ---------------- 12 ENROLMENTS ----------------
S = Scene("s12"); scenes.append(S); S.tab_card(6, "Enrolments"); TAB(S, 1.1, "Enrolments")
S.laptop([("a", SH("06-enrolments"))], t_in=1.1)
S.hl("a", "h0", (30, 137, 292, 280), S.c("puts", 0.2), S.c("row"))
S.push(S.c("row", -0.2), 110, 145, 2.4); S.hl("a", "h1", (30, 138, 292, 154), S.c("row"), S.dur)
S.magcard("mg", "One row = one class", "150312101234 → Kids Class", S.c("row", 0.3), S.dur)
M(S, S.c("puts"), "point")

# ---------------- 13 FIND STUDENT ----------------
S = Scene("s13"); scenes.append(S)
S.laptop([("a", GN("06b_base.jpg"))])
S.push(S.c("arrow", -0.2), 80, 298, 2.5); Zc = S.cam_state
S.tap("a", "t1", 109, 286, S.w("arrow", 2, 0.1))
te = S.typing("a", "ty", (31, 279, 104, 294), "1901", S.c("type", 0.4), 0.16)
S.magcard("mg", "Type a few numbers", "1901 …", S.c("type", 0.3), S.dur)
S.popup("a", "sg", "06b_sug.png", (27, 295, 126, 323), te + 0.1); S.glow("a", "g1", (33, 295, 120, 312), S.c("finds", 0.1))
ex, ey = S.stage_at(76, 304, *Zc); tx, ty = tab_center("Students")
S.arrow("ar", (tx, ty - 8), (R(ex), R(ey + 22)), S.c("finds", 0.4), S.dur, bend=-0.3)
M(S, S.c("type"), "talk"); M(S, S.c("finds", 0.4), "thumb")

# ---------------- 14 PICK CLASS ----------------
S = Scene("s14"); scenes.append(S)
S.laptop([("a", GN("06c_base.jpg"))])
S.push(S.c("pick", -0.4), 160, 330, 2.2); Zc = S.cam_state
S.tap("a", "t1", 193, 286, S.w("pick", 2, 0.0)); S.popup("a", "pl", "06c_list.png", (109, 295, 200, 389), S.w("pick", 2, 0.2))
S.glow("a", "g1", (114, 335, 196, 353), S.c("new", 0.1))
ex, ey = S.stage_at(154, 344, *Zc); tx, ty = tab_center("Classes")
S.arrow("ar", (tx, ty - 8), (R(ex + 30), R(ey + 20)), S.c("new", 0.4), S.dur, bend=0.3 if O == "h" else -0.3)
S.tip("tp", f'<b style="color:{AMBER}">Two classes?</b><br>Make two rows.', S.c("new", 0.8), S.dur)
M(S, S.c("new"), "point"); TAB(S, S.dur - 0.2, "Enrolments", "done")

# ---------------- 15 PARENTS ----------------
S = Scene("s15"); scenes.append(S); S.tab_card(7, "Parents"); TAB(S, 1.1, "Parents")
S.laptop([("a", SH("07-parents-children-ic-with-comma"))], t_in=1.1)
S.push(S.c("phone", -0.2), 100, 162, 2.4); S.hl("a", "h1", (30, 154, 166, 170), S.c("phone"), S.c("kids"))
S.magcard("mg", "Phone · Name", "60165557777 · Mr Ganesh", S.c("phone", 0.3), S.c("kids"))
S.push(S.c("kids", -0.2), 348, 162, 2.4, 0.7)
S.o("a", f'<div id="cl" class="ty" style="left:{R(279 * K)}px;top:{R(155 * K)}px;width:{R(137 * K)}px;height:{R(15 * K)}px;border:{R(1.2 * K)}px solid #1a73e8"></div>'); S.gs("#cl", {"opacity": 0}); S.st("#cl", S.c("kids", 0.1), {"opacity": 1})
te = S.typing("a", "tk", (280, 156, 415, 169), "190101101010, 180606109900", S.c("kids", 0.4), 0.07)
S.add("mg2", f'<div class="k">Children · IC numbers</div><div class="v"><span style="white-space:nowrap">190101101010<b id="cm" style="color:{AMBER};font-weight:900">,</b></span> <span style="white-space:nowrap">180606109900</span></div>',
      f"left:{LAY['mag'][0]}px;top:{LAY['mag'][1]}px;width:{LAY['mag'][2]}px", "mag", S.c("kids", 0.6), S.dur, "pop", ("curated/ui-pop.wav", -20))
cx_ = 340
S.push(S.c("comma", -0.2), cx_, 162, 4.2, 0.8); S.o("a", f'<div id="cr" class="pulse" style="left:{R((cx_ - 6) * K)}px;top:{R(155 * K)}px;width:{R(12 * K)}px;height:{R(14 * K)}px;border-width:{R(1.3 * K)}px"></div>')
S.gs("#cr", {"opacity": 0}); S.js.append(f'tl.fromTo("#cr",{{opacity:1,scale:0.6}},{{opacity:0,scale:2.4,duration:0.9,ease:"power2.out",repeat:2,immediateRender:false}},{R(S.c("comma", 0.5))});')
S.js.append(f'tl.fromTo("#cm",{{textShadow:"0 0 0px rgba(255,158,27,0)"}},{{textShadow:"0 0 18px rgba(255,158,27,1)",duration:0.3,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false}},{R(S.c("comma", 0.5))});')
S.chip("cmc", 'Comma <span style="font-size:60px;line-height:0">,</span> between', S.c("comma", 0.4), S.dur, size=38)
M(S, S.c("kids"), "talk"); M(S, S.c("comma", 0.6), "thumb"); TAB(S, S.dur - 0.2, "Parents", "done")

# ---------------- 16 ACCESS ----------------
S = Scene("s16"); scenes.append(S); S.tab_card(8, "Access"); TAB(S, 1.1, "Access")
S.laptop([("a", SH("08-access"))], t_in=1.1)
S.push(S.c("who", -0.1), 200, 186, 1.6); S.hl("a", "h0", (30, 137, 474, 232), S.c("who", 0.2), S.dur)
S.chip("ky", "🔑 Who can sign in", S.c("who", 0.4), S.dur, size=38)
M(S, S.c("who"), "point")

# ---------------- 17 PICK ROLE ----------------
S = Scene("s17"); scenes.append(S)
S.laptop([("a", GN("08b_base.jpg"))])
S.push(S.c("pick", -0.3), 236, 266, 2.2)
S.tap("a", "t1", 262, 224, S.w("pick", 1, 0.1)); S.popup("a", "pl", "08b_list.png", (193, 233, 277, 347), S.w("pick", 1, 0.3))
for i, ((y0, y1), wi) in enumerate(zip(((235, 251), (254, 270), (273, 290), (292, 309)), (0, 1, 2, 4))):
    S.glow("a", f"g{i}", (197, y0, 273, y1), S.w("roles", wi), None if i == 2 else S.w("roles", wi, 0.75))
S.chip("pr", "Parent", S.w("roles", 4, 0.9), S.dur, size=40)
S.tip("tp", f'<b style="color:{AMBER}">Masters:</b> their Gmail.<br><b style="color:{AMBER}">Parents &amp; students:</b> phone number.', S.c("roles", 0.6), S.dur)
M(S, S.c("pick"), "point")

# ---------------- 18 ACTIVE YES / PIN ----------------
S = Scene("s18"); scenes.append(S)
S.laptop([("a", GN("08c_base.jpg")), ("b", SH("08c-access-parent-added"))])
S.push(S.c("yes", -0.3), 434, 224, 2.4); S.tap("a", "t1", 436, 224, S.w("yes", 1, 0.0)); S.show("b", S.w("yes", 1, 0.3), 0.3)
S.chip("ys", "Active: Yes", S.w("yes", 1, 0.4), S.dur, cls="chip gr", size=40)
S.pull(S.c("pin", -0.2)); S.burst("ok", R(CX), R(LY + LH * 0.45), S.c("pin", 0.1))
S.tip("pn", f'{PHONE_ICON}<b>PIN</b> → given in the app', S.c("pin", 0.5), S.dur)
M(S, S.c("pin", 0.2), "thumb"); TAB(S, S.dur - 0.2, "Access", "done")

# ---------------- 19 FEES (app tabs) ----------------
S = Scene("s19"); scenes.append(S); S.tab_card(0, "The app fills these")
for i, t in enumerate(APP_TABS): TAB(S, 1.2 + 0.15 * i, t, "app")
S.laptop([("a", SH("09-fees"))], t_in=1.1)
S.push(S.c("colours", -0.3), 430, 260, 1.8); S.hl("a", "h0", (412, 137, 478, 388), S.c("colours"), S.dur)
S.chip("pd", "Paid", S.w("colours", 1), S.dur, cls="chip gr", slot=LAY["chip"], size=44)
S.chip("du", "Due", S.w("colours", 3), S.dur, cls="chip rd", slot=(LAY["chip"][0] + 160, LAY["chip"][1]), size=44)
S.tip("tp", f'{PHONE_ICON}Masters update this in the app.', S.c("fills", 0.6), S.dur)
M(S, S.c("fills"), "point")

# ---------------- 20 GRADINGS ----------------
S = Scene("s20"); scenes.append(S)
S.laptop([("a", SH("10-gradings"))])
S.push(S.c("tests", -0.1), 300, 162, 1.7); S.hl("a", "h0", (30, 137, 700, 186), S.c("tests", 0.2), S.dur)
S.chip("gb", f'<span style="display:inline-block;vertical-align:middle;margin-right:10px">{belt_svg(BELTS[1], 80)}</span>→<span style="display:inline-block;vertical-align:middle;margin-left:10px">{belt_svg(BELTS[2], 80)}</span>', S.c("tests", 0.4), S.dur, cls="chip")
S.tip("tp", f'{PHONE_ICON}Masters fill this in the app.', S.c("app", 0.2), S.dur)
M(S, S.c("app"), "talk")

# ---------------- 21 ATTENDANCE ----------------
S = Scene("s21"); scenes.append(S)
S.laptop([("a", SH("11-attendance-auto-filled-by-app"))])
S.js.append(f'tl.fromTo("#La",{{scale:1}},{{scale:1.1,transformOrigin:"30% 35%",duration:{R(S.dur)},ease:"none",immediateRender:false}},0);')
S.chip("au", "Fills by itself ✨", S.c("fills", 0.3), S.dur, cls="chip", size=38)
hand = f'''<svg width="100%" height="100%" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#fff" stroke="{RED}" stroke-width="8"/>
 <path d="M38 70V40c0-3 4-3 4 0v14V30c0-3 4-3 4 0v24V28c0-3 4-3 4 0v26V32c0-3 4-3 4 0v26l4-7c2-3 6-1 5 2l-7 14c-3 6-7 9-13 9h-1c-6 0-10-4-10-9z" fill="#ffd9b0" stroke="#1f1435" stroke-width="2"/>
 <path d="M20 20L80 80" stroke="{RED}" stroke-width="8" stroke-linecap="round"/></svg>'''
hs = 260 if O == "h" else 240; hx, hy = (R(CX - hs / 2), R(LY + LH * 0.25)) if O == "h" else (R(CX - hs / 2), 220)
S.add("hand", hand, f"left:{hx}px;top:{hy}px;width:{hs}px;height:{hs}px;filter:drop-shadow(0 20px 30px rgba(0,0,0,.5))", "a", S.c("dont"), S.dur, "pop", ("thock.wav", -16))
S.js.append(f'tl.to("#hand",{{rotation:-10,duration:0.25,yoyo:true,repeat:5,ease:"sine.inOut"}},{R(S.c("dont", 0.6))});')
M(S, S.c("dont"), "talk")

# ---------------- 22 NOTICES ----------------
S = Scene("s22"); scenes.append(S)
S.laptop([("a", SH("12-notices"))])
S.push(S.c("posted", -0.1), 300, 155, 1.8); S.hl("a", "h0", (30, 137, 580, 170), S.c("posted", 0.2), S.dur)
S.chip("np", f'{PHONE_ICON}Posted from the app', S.c("posted", 0.4), S.dur, cls="chip", size=36)
M(S, S.c("posted"), "point")

# ---------------- 23 RECAP + GOLDEN RULES ----------------
S = Scene("s23"); scenes.append(S)
HDR("h", "You type these 8 tabs", 0.2, S.c("rules"))
tab_grid(S, "g", 0.3, 0.08, S.c("rules"))
seq = [S.w("you", 2 + i) for i in range(4)] + [S.w("you2", i) for i in range(4)]
for i, t in enumerate(seq):
    S.tw(f"#g{i}t", t, 0.4, {"opacity": 1}, "back.out(3)"); S.ft(f"#g{i}t", t, 0.4, {"scale": 0.2}, {"scale": 1}, "back.out(3)"); S.sfx(t, "tick.wav", -18); TAB(S, t, TABS[i], "done")
S.add("rest", PHONE_ICON.replace("#1f1435", AMBER).replace('width="44" height="56"', 'width="88" height="112"'), f"left:{R(CX - 44)}px;top:{grid_rects()[-1][1] + 140}px", "a", S.c("rest"), S.c("rules"), "pop", ("clean-ding.wav", -16))
HDR("gr", "4 golden rules", S.c("rules"), None, LAY["CY"] - 190, AMBER, 66); S.sfx(S.c("rules"), "curated/metallic-riser.wav", -22)
RULES = ["Never change the top row (the titles).", "Check every IC number twice.", "Use the ▼ lists when you see them.", "Don't delete rows — set Active to “No”."]
for i, r in enumerate(RULES):
    x, y, w = (340, LAY["CY"] - 60 + i * 118, 1300) if O == "h" else (60, 520 + i * 160, 960)
    S.add(f"r{i}", f'<div style="display:flex;align-items:center;gap:22px;height:100%;padding:0 28px"><span style="width:62px;height:62px;border-radius:14px;background:{GREEN};padding:10px;flex:none">{tick_svg()}</span>'
          f'<span style="font-size:{44 if O == "h" else 42}px;font-weight:800;color:{PLUM};line-height:1.15">{esc(r)}</span></div>',
          f"left:{x}px;top:{y}px;width:{w}px;height:{100 if O == 'h' else 136}px;border-radius:22px;background:{CARD};box-shadow:0 16px 36px rgba(0,0,0,.4)", "a", S.c(f"r{i + 1}"), None, "left", ("clean-ding.wav", -18))
M(S, S.c("rest"), "cheer"); M(S, S.c("r4", 0.6), "thumb")

# ---------------- 24 OUTRO ----------------
S = Scene("s24"); scenes.append(S); oy = LAY["CY"] - (280 if O == "h" else 80)
S.add("lg", '''<svg width="260" height="260" viewBox="0 0 100 100"><g transform="rotate(-35 50 50)"><rect x="8" y="46" width="84" height="8" rx="4" fill="#c98a4b"/></g><g transform="rotate(35 50 50)"><rect x="8" y="46" width="84" height="8" rx="4" fill="#c98a4b"/></g>
   <rect x="22" y="34" width="56" height="12" rx="4" fill="#fff"/><path d="M45 44 L36 66 L43 66 L50 52 L57 66 L64 66 L55 44 Z" fill="#fff"/><rect x="43" y="31" width="14" height="17" rx="3" fill="#fff"/></svg>''', f"left:{R(CX - 130)}px;top:{oy}px", "a")
S.gs("#lg", {"opacity": 0, "scale": 0.2, "rotation": -200}); S.tw("#lg", 0.1, 1.1, {"opacity": 1, "scale": 1, "rotation": 0}, "back.out(1.5)")
S.add("ot", "BeltFlow Lite", f"left:0;top:{oy + 280}px;width:{W}px;text-align:center;font-size:110px;font-weight:800;color:{AMBER}", "a", 0.4, None, "pop", ("thock.wav", -18))
S.add("os", "PERSATUAN SILAMBAM DAERAH SEPANG", f"left:0;top:{oy + 420}px;width:{W}px;text-align:center;font-size:36px;font-weight:800;letter-spacing:3px;opacity:.9", "a", 0.7, None, "up")
S.add("url", "beltflow-lite.vercel.app", f"left:{R(CX - 320)}px;top:{oy + 500}px;width:640px;text-align:center;font-size:48px", "chip", 1.0, None, "pop", ("curated/ui-pop.wav", -18))
S.add("ta", "Thank you, Admin!", f"left:0;top:{oy + (600 if O == "h" else 630)}px;width:{W}px;text-align:center;font-size:56px;font-weight:800", "a", 1.4, None, "up")
S.burst("cf", R(CX), oy + 130, S.c("great", 0.1), 34, tick=False); S.burst("cf2", R(CX), oy + 130, S.c("bye", 0.1), 34, tick=False)
M(S, S.c("great"), "cheer"); M(S, S.c("bye"), "wave")
