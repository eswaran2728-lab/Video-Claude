# RevLog explainer -> HyperFrames project (project/index.html), captions (video/captions.srt), cue list for the mix.
# 1920x1080, 30 fps. Screenshots are only scaled, masked (rounded screen corners), panned and zoomed; nothing is drawn into them.
import json, os, re, shutil, html
import plan22 as P
OCR = json.load(open("ocr.json")); T = json.load(open("timing.json")); SRC = "src/unz/revlog screenshot"; OUT = "project"
os.makedirs(f"{OUT}/assets/shots", exist_ok=True); os.makedirs(f"{OUT}/assets/fonts", exist_ok=True); os.makedirs("video", exist_ok=True)
for f in os.listdir("fonts"):
    if f.endswith(".ttf"): shutil.copy(f"fonts/{f}", f"{OUT}/assets/fonts/{f}")
for f in ("Inter-SemiBold.otf", "Inter-Medium.otf", "Inter-Bold.otf"): shutil.copy(f"/usr/share/fonts/opentype/inter/{f}", f"{OUT}/assets/fonts/{f}")
MANIFEST = {e["file"] for e in json.load(open(f"{SRC}/manifest.json")) if e.get("file")}
BANNED = {"rider-03-verify-photos-ready.png", "owner-06-team-before-remove.png", "owner-07-remove-staff-confirm.png", "staff-09-bike-opens-without-code.png"}
R3 = lambda x: round(float(x), 3); esc = html.escape
BG, SURF, RAISED, TXT, MUTED, TEAL, CHOP = "#0D0E10", "#17181B", "#222428", "#ECEDEF", "#9EA3AB", "#03DAC6", "#8D9AE9"
AIR, LEAD, CH_GAP, SILENT = 0.4, 0.12, 0.3, 1.8
NW, NH = 585, 1266

# ---------------- timeline: line start/end from measured speech ----------------
tl, t, prev_ch = [], 0.6, 0
rec = {(r["scene"], r["n"]): r for r in T}
for sc in P.S:
    t += LEAD + (CH_GAP if sc["chapter"] != prev_ch else 0); prev_ch = sc["chapter"]
    for n, ln in enumerate(sc["lines"]):
        r = rec[(sc["id"], n)]; d = r.get("dur", 0.0)
        end = t + (d + AIR if ln["text"] else SILENT); end = max(end, t + ln.get("hold", 0))
        tl.append(dict(scene=sc["id"], ch=sc["chapter"], role=sc["role"], n=n, t0=R3(t), sp=R3(t + d), t1=R3(end), text=ln["text"], shot=ln["shot"], words=r.get("words", []), file=r.get("file"), i0=r.get("i0"), sr=r.get("sr")))
        t = end
TOTAL = R3(t + 1.5)

def word_t(L, word, k=0):
    """time of a spoken word in line L (closest heard word; copes with US/UK spelling); None -> line start"""
    if word is None: return L["t0"]
    import difflib
    w = word.lower().replace("'", ""); hw = [x["w"].replace("'", "") for x in L["words"]]
    sc = [max(difflib.SequenceMatcher(None, w, h).ratio(), 1.0 if h.startswith(w[:5]) else 0) for h in hw]
    cand = [i for i, v in enumerate(sc) if v >= 0.7]
    if not cand: raise SystemExit(f"word '{word}' not heard in {L['scene']}: {L['text']} | {hw}")
    return R3(L["t0"] + L["words"][cand[min(k, len(cand) - 1)]]["t"])

def target(file, tg):
    if isinstance(tg, tuple): return tg
    toks = tg.lower().split(); ws = OCR[file]
    for i in range(len(ws)):
        if all(i + j < len(ws) and ws[i + j]["t"].lower().strip(".,:?") .startswith(toks[j].strip(".,:?")) for j in range(len(toks))):
            g = ws[i:i + len(toks)]; x0 = min(a["x"] for a in g); y0 = min(a["y"] for a in g); x1 = max(a["x"] + a["w"] for a in g); y1 = max(a["y"] + a["h"] for a in g)
            return (x0, y0, x1 - x0, y1 - y0)
    raise SystemExit(f"target '{tg}' not found by OCR in {file}")

# ---------------- beats: a line split into shots ----------------
beats = []
for L in tl:
    sh = L["shot"]
    if sh[0] == "seq":
        pts = [(word_t(L, w) if w else L["t0"], s_) for w, s_ in sh[1]]
        for j, (a, s_) in enumerate(pts): beats.append(dict(L=L, t0=a, t1=pts[j + 1][0] if j + 1 < len(pts) else L["t1"], shot=s_))
    elif sh[0] == "duo" and isinstance(sh[1], tuple) and sh[1] and sh[1][0] == "seq": raise SystemExit("seq inside duo not supported")
    else: beats.append(dict(L=L, t0=L["t0"], t1=L["t1"], shot=sh))
def layout(s): return {"phone": "single", "mock": "single"}.get(s[0], s[0])

# ---------------- elements / GSAP ----------------
els, init, js = [], [], []; UID = [0]; CUES = []
def uid(p): UID[0] += 1; return f"{p}{UID[0]}"
fmt = lambda d: ",".join(f"{k}:{json.dumps(v)}" for k, v in d.items())
def J(sel, t, d, props, ease="power2.out"): js.append(f'tl.to("{sel}",{{{fmt(props)},duration:{R3(d)},ease:"{ease}"}},{R3(t)});')
def SET(sel, t, props): js.append(f'tl.set("{sel}",{{{fmt(props)}}},{R3(t)});')
def INIT(sel, props): init.append(f'gsap.set("{sel}",{{{fmt(props)}}});')
used = set()

def accent(role): return P.ROLE.get(role, TEAL)

FRAME_ORIGIN = {}                                        # screen top-left on the stage for single-phone frames (for callouts)
def callout(file, box, sc, ta, te, role):
    """magnifier: an enlarged crop of the screenshot beside the phone (<= 1.8x native), an outline on the source area and a joining line"""
    x, y, w, h = box; sx0, sy0 = FRAME_ORIGIN["single"]; s_c = min(1.8, 600 / w, 560 / h); cw, ch = w * s_c, h * s_c
    cy = min(max(sy0 + (y + h / 2) * sc - ch / 2, 60), 900 - ch); cx = 1250
    cid = uid("co"); col = accent(role)
    PENDING.append(f'<div id="{cid}" class="callout" style="left:{R3(cx)}px;top:{R3(cy)}px;width:{R3(cw + 16)}px;height:{R3(ch + 16)}px;border-color:{col}">'
               f'<div class="cwin" style="width:{R3(cw)}px;height:{R3(ch)}px"><img src="assets/shots/{file}" alt="" style="left:{R3(-x * s_c)}px;top:{R3(-y * s_c)}px;width:{R3(NW * s_c)}px;height:{R3(NH * s_c)}px"></div></div>')
    ox, oy, ow, oh = sx0 + x * sc, sy0 + y * sc, w * sc, h * sc
    lid2 = uid("cl"); PENDING.append(f'<svg id="{lid2}" class="cline" width="1920" height="930"><rect x="{R3(ox - 3)}" y="{R3(oy - 3)}" width="{R3(ow + 6)}" height="{R3(oh + 6)}" rx="8" fill="none" stroke="{col}" stroke-width="2.5"/>'
               f'<line x1="{R3(ox + ow + 3)}" y1="{R3(oy + oh / 2)}" x2="{R3(cx)}" y2="{R3(cy + ch / 2 + 8)}" stroke="{col}" stroke-width="2"/></svg>')
    INIT(f"#{cid}", {"opacity": 0, "x": -24}); J(f"#{cid}", ta, 0.35, {"opacity": 1, "x": 0}, "power2.out"); J(f"#{cid}", te - 0.25, 0.22, {"opacity": 0}, "power1.in")
    INIT(f"#{lid2}", {"opacity": 0}); J(f"#{lid2}", ta - 0.05, 0.3, {"opacity": 1}); J(f"#{lid2}", te - 0.25, 0.22, {"opacity": 0}, "power1.in"); CUES.append((ta, "zoom"))

def layer_html(lid, file, ops, L, sc, t0, t1, role, mode="single"):
    """one screenshot inside a screen viewport of scale sc; rings/zooms in screenshot pixels"""
    assert file in MANIFEST and file not in BANNED, file
    used.add(file); shutil.copy(f"{SRC}/{file}", f"{OUT}/assets/shots/{file}")
    inner = []; col = accent(role)
    INIT(f"#{lid}", {"scale": sc, "x": 0, "y": 0, "transformOrigin": "0px 0px"})
    for op in ops:
        if op[0] == "zoom" and mode == "single":
            _, w, tg, z = op; ta = max(t0 + 0.3, word_t(L, w) - 0.1) if w else t0 + 0.4
            nxt = [o for o in ops if o[0] in ("zoom", "unzoom") and o is not op and ops.index(o) > ops.index(op)]
            te = (word_t(L, nxt[0][1]) if nxt[0][1] else t1) if nxt else t1
            callout(file, target(file, tg), sc, ta, te, role)
        elif op[0] == "unzoom" and mode == "single": pass
        elif op[0] == "zoom":
            _, w, tg, z = op; x, y, w_, h = target(file, tg); ta = max(t0, word_t(L, w)) if w else t0
            z = min(z, NW / (w_ + 40), NH / (h + 40))        # never crop the target: it always fits the screen width
            s2 = sc * z; assert s2 <= 1.8 + 1e-6, (file, s2); vw, vh = NW * sc, NH * sc
            tx = min(0, max(vw - NW * s2, vw / 2 - (x + w_ / 2) * s2)); ty = min(0, max(vh - NH * s2, vh / 2 - (y + h / 2) * s2))
            if ta <= t0 + 0.05: SET(f"#{lid}", t0, {"scale": R3(s2), "x": R3(tx), "y": R3(ty)})
            else: J(f"#{lid}", ta - 0.15, 0.7, {"scale": R3(s2), "x": R3(tx), "y": R3(ty)}, "power2.inOut"); CUES.append((ta - 0.15, "zoom"))
        elif op[0] == "unzoom":
            ta = word_t(L, op[1]) if op[1] else t0; J(f"#{lid}", ta, 0.6, {"scale": sc, "x": 0, "y": 0}, "power2.inOut")
        elif op[0] == "ring":
            _, w, tg = op; x, y, w_, h = target(file, tg); ta = max(t0 + 0.15, (word_t(L, w) if w else t0 + 0.6) - 0.1); rid = uid("rg"); pad = 10
            inner.append(f'<div id="{rid}" class="ring" style="left:{x - pad}px;top:{y - pad}px;width:{w_ + 2 * pad}px;height:{h + 2 * pad}px;border-color:{col}"></div>')
            INIT(f"#{rid}", {"opacity": 0, "scale": 1.06, "transformOrigin": "50% 50%"}); J(f"#{rid}", ta, 0.3, {"opacity": 1, "scale": 1}, "power2.out")
            J(f"#{rid}", t1 - 0.25, 0.2, {"opacity": 0}, "power1.in")
            pid = uid("tp"); cx, cy = x + w_ / 2, y + h / 2
            inner.append(f'<div id="{pid}" class="tap" style="left:{cx - 40}px;top:{cy - 40}px;border-color:{col}"></div>')
            INIT(f"#{pid}", {"opacity": 0, "scale": 0.3, "transformOrigin": "50% 50%"}); SET(f"#{pid}", ta, {"opacity": 0.9}); J(f"#{pid}", ta, 0.55, {"scale": 1.6, "opacity": 0}, "power2.out")
            CUES.append((ta, "tap"))
    clip = next((op[1] for op in ops if op[0] == "clip"), None)          # crop: show only the top `clip` rows of the screenshot
    img = f'<img src="assets/shots/{file}" alt="" width="{NW}" height="{NH}">'
    if clip: img = f'<div class="crop" style="height:{clip}px">{img}</div>'
    return f'<div id="{lid}" class="shotl">{img}{"".join(inner)}</div>'

# --- mock-ups (drawn in HTML; generic, made-up details, each with a Sample tag) ---
import segno
segno.make("REVLOG-SAMPLE", error="m").save(f"{OUT}/assets/qr_sample.svg", scale=10, border=2, dark="#0D0E10", light="#FFFFFF")
def card_licence():
    return ('<div class="doc lic"><div class="doc-h">DRIVING LICENCE</div><div class="doc-b"><div class="doc-ph"></div><div class="doc-f">'
            '<div><span>NAME</span>AHMAD BIN TEST</div><div><span>CLASS</span>B2</div><div><span>NO.</span>0000 0000</div></div></div><div class="doc-wm">SAMPLE</div></div>')
def card_geran(plate, model):
    return (f'<div class="doc ger"><div class="doc-h">VEHICLE REGISTRATION (GERAN)</div><div class="doc-f2"><div><span>PLATE</span>{plate}</div>'
            f'<div><span>OWNER</span>AHMAD BIN TEST</div><div><span>MAKE / MODEL</span>{model}</div></div><div class="doc-wm">SAMPLE</div></div>')
def mock_html(mid, name, t0, t1):
    """screen content of a camera mock-up; returns html; schedules its own animation"""
    a = []
    if name in ("licence", "geran", "geran2"):
        title = {"licence": "Your driving licence", "geran": "The bike's geran", "geran2": "The bike's geran"}[name]
        doc = card_licence() if name == "licence" else card_geran("TEST1234" if name == "geran" else "TEST5678", "Yamaha Y15ZR" if name == "geran" else "Honda RS150R")
        a.append(f'<div class="cam"><div class="cam-t">{title}</div><div class="cam-s">Fit the card inside the frame</div><div id="{mid}d" class="cam-doc">{doc}</div>'
                 f'<div class="brk"><i class="b1"></i><i class="b2"></i><i class="b3"></i><i class="b4"></i></div><div id="{mid}sh" class="shutter"></div><div id="{mid}fl" class="flash"></div></div>')
        INIT(f"#{mid}d", {"scale": 0.92, "rotation": -3, "opacity": 0}); J(f"#{mid}d", t0 + 0.15, 0.6, {"scale": 1, "rotation": 0, "opacity": 1}, "power2.out")
        tp = min(t1 - 0.7, t0 + 2.0); J(f"#{mid}sh", tp, 0.12, {"scale": 0.86}, "power1.in"); J(f"#{mid}sh", tp + 0.12, 0.2, {"scale": 1}, "power1.out")
        INIT(f"#{mid}fl", {"opacity": 0}); SET(f"#{mid}fl", tp + 0.05, {"opacity": 0.5}); J(f"#{mid}fl", tp + 0.08, 0.3, {"opacity": 0}, "power1.out"); CUES.append((tp, "shutter"))
    elif name in ("geran_checking", "geran2_checking"):
        doc = card_geran("TEST1234" if name == "geran_checking" else "TEST5678", "Yamaha Y15ZR" if name == "geran_checking" else "Honda RS150R")
        a.append(f'<div class="cam chk"><div class="cam-t">Checking</div><div class="cam-s">Reading the name and plate</div><div id="{mid}d" class="cam-doc">{doc}</div>'
                 f'<div class="prog"><i id="{mid}p"></i></div></div>')
        INIT(f"#{mid}d", {"scale": 1}); J(f"#{mid}d", t0, 0.6, {"scale": 0.78, "y": -40}, "power2.inOut")
        INIT(f"#{mid}p", {"x": -160});
        k = 0
        while t0 + 0.5 + k * 1.3 < t1 - 0.2: SET(f"#{mid}p", t0 + 0.5 + k * 1.3, {"x": -160}); J(f"#{mid}p", t0 + 0.5 + k * 1.3, 1.2, {"x": 380}, "power1.inOut"); k += 1
    elif name in ("claim", "scan_mycode"):
        title, sub = ("Scan the workshop's QR", "Claim QR · TEST5678") if name == "claim" else ("Scan My code", "Rider's My code")
        a.append(f'<div class="cam"><div class="cam-t">{title}</div><div id="{mid}d" class="cam-phone"><div class="cp-t">{sub}</div><img src="assets/qr_sample.svg" alt=""></div>'
                 f'<div class="brk sq"><i class="b1"></i><i class="b2"></i><i class="b3"></i><i class="b4"></i></div><div id="{mid}ln" class="scanln"></div>'
                 f'<div id="{mid}ok" class="readok">QR read</div>' + ('<div class="typeopt">or type the 6-digit code</div>' if name == "scan_mycode" else "") + '</div>')
        INIT(f"#{mid}d", {"rotation": 4, "scale": 0.94, "opacity": 0}); J(f"#{mid}d", t0 + 0.1, 0.7, {"rotation": 0, "scale": 1, "opacity": 1}, "power2.out")
        INIT(f"#{mid}ln", {"y": 0, "opacity": 0}); SET(f"#{mid}ln", t0 + 0.6, {"opacity": 0.9}); J(f"#{mid}ln", t0 + 0.6, 1.1, {"y": 300}, "power1.inOut"); SET(f"#{mid}ln", t0 + 1.75, {"opacity": 0})
        INIT(f"#{mid}ok", {"opacity": 0, "y": 8}); J(f"#{mid}ok", t0 + 1.8, 0.3, {"opacity": 1, "y": 0}); CUES.append((t0 + 1.8, "tap"))
    a.append('<div class="sample">Sample</div>')
    return "".join(a)

# --- phone frames ---
FRAME_PAD = 12
def frame_open(fid, cx, top, sc, label=None, lcol=None):
    w, h = NW * sc, NH * sc
    lab = f'<div class="flabel" style="color:{lcol};border-color:{lcol}">{esc(label)}</div>' if label else ""
    els.append(f'<div id="{fid}" class="frame" style="left:{R3(cx - w / 2 - FRAME_PAD)}px;top:{R3(top)}px;width:{R3(w + 2 * FRAME_PAD)}px;height:{R3(h + 2 * FRAME_PAD)}px;'
               f'border-radius:{R3(46 * sc / 0.64)}px">{lab}<div id="{fid}s" class="screen" style="width:{R3(w)}px;height:{R3(h)}px;border-radius:{R3(36 * sc / 0.64)}px">')
PENDING = []
def frame_close():
    els.append('</div></div>')
    while PENDING: els.append(PENDING.pop(0))
def frame_anim(fid, t_in, t_out, dx=0, tilt=-4):
    INIT(f"#{fid}", {"opacity": 0, "x": 60 + dx, "y": 24, "rotation": tilt})
    J(f"#{fid}", t_in, 0.5, {"opacity": 1, "x": 0, "y": 0, "rotation": 0}, "power2.out"); CUES.append((t_in, "whoosh"))
    if t_out < TOTAL - 0.01: J(f"#{fid}", t_out - 0.3, 0.28, {"opacity": 0, "x": -50}, "power1.in")

def fill_screen(beats_, sc, role, mode="single"):
    """screen layers for consecutive beats; crossfade between different contents"""
    prev = None
    for k, B_ in enumerate(beats_):
        s_ = B_["shot"]; t0, t1 = B_["t0"], B_["t1"]
        key = (s_[0], s_[1]) if s_[0] in ("phone", "mock") else s_
        lid = uid("ly")
        if s_[0] == "phone": els.append(layer_html(lid, s_[1], s_[2], B_["L"], sc, t0, t1, role, mode))
        else:
            els.append(f'<div id="{lid}" class="mockl" style="width:{NW}px;height:{NH}px">{mock_html(lid + "m", s_[1], t0, t1)}</div>')
            INIT(f"#{lid}", {"scale": sc, "transformOrigin": "0px 0px"})
        INIT(f"#{lid}", {"opacity": 0}); (SET(f"#{lid}", t0 - 0.45, {"opacity": 1}) if k == 0 else J(f"#{lid}", t0 - 0.05, 0.25, {"opacity": 1}, "power1.out"))   # first content is in place before its frame slides in
        nxt = beats_[k + 1]["t0"] if k + 1 < len(beats_) else None
        if nxt is not None: SET(f"#{lid}", nxt + 0.25, {"opacity": 0})

# ---------------- build per scene-run ----------------
runs = []                                                # consecutive beats with the same layout (and same chapter for single)
for B_ in beats:
    lay = layout(B_["shot"])
    if runs and runs[-1]["lay"] == lay and (lay != "single" or runs[-1]["ch"] == B_["L"]["ch"]) and lay not in ("row4", "ways", "close", "card", "strip"): runs[-1]["beats"].append(B_)
    elif runs and runs[-1]["lay"] == lay and lay in ("row4", "ways", "close", "strip") and runs[-1]["scene"] == B_["L"]["scene"]: runs[-1]["beats"].append(B_)
    else: runs.append(dict(lay=lay, ch=B_["L"]["ch"], scene=B_["L"]["scene"], beats=[B_]))
for j, run in enumerate(runs):
    same_ch = j and runs[j - 1]["beats"][0]["L"]["ch"] == run["beats"][0]["L"]["ch"]
    # a new chapter enters only after the old phones are gone
    run["t_in"] = run["beats"][0]["t0"] - (0.3 if same_ch else 0.0)
    run["t_out"] = runs[j + 1]["beats"][0]["t0"] if j + 1 < len(runs) else TOTAL

SC1, SC2, SC4 = 0.64, 0.58, 0.44
FRAME_ORIGIN["single"] = (960 - NW * SC1 / 2, 46 + FRAME_PAD)
for run in runs:
    lay, bs = run["lay"], run["beats"]; t_in, t_out = run["t_in"], run["t_out"]; role = bs[0]["L"]["role"]
    if lay == "single":
        fid = uid("fr"); frame_open(fid, 960, 46, SC1); fill_screen(bs, SC1, role); frame_close(); frame_anim(fid, t_in, t_out)
    elif lay == "duo":
        # Staff (left) and Rider (right): each side keeps its own sequence of contents
        for side, cx, lab in (("L", 640, "Staff"), ("R", 1280, "Rider")):
            seq = []
            for B_ in bs:
                c = B_["shot"][1] if side == "L" else B_["shot"][2]
                if c is None: continue
                shot = ("mock", c[1], []) if c[0] == "mock" else ("phone", c[0], c[1])
                if seq and seq[-1]["shot"][:2] == shot[:2] and not shot[2]: seq[-1]["t1"] = B_["t1"]; continue
                seq.append(dict(L=B_["L"], t0=B_["t0"], t1=B_["t1"], shot=shot))
            if not seq: continue
            fid = uid("fr"); frame_open(fid, cx, 92, SC2, lab.upper(), P.ROLE[lab]); fill_screen(seq, SC2, lab, "duo"); frame_close()
            frame_anim(fid, seq[0]["t0"] - (0.3 if seq[0]["t0"] > t_in + 0.1 else 0) if seq[0]["t0"] > t_in + 0.1 else t_in, t_out, dx=(0 if side == "L" else 80))
            # active side: the other phone dims slightly
            for B_ in bs:
                act = B_["shot"][3]
                if seq[0]["t0"] + 0.6 < B_["t0"] < t_out - 0.7: J(f"#{fid}", B_["t0"], 0.3, {"opacity": 1 if act == side else 0.55}, "power1.inOut")
        # connector between the phones while My code is in play
        cn = uid("cn"); els.append(f'<div id="{cn}" class="conn"><i></i></div>'); INIT(f"#{cn}", {"opacity": 0, "scaleX": 0, "transformOrigin": "100% 50%"})
        tc = next(B_["t0"] for B_ in bs if B_["shot"][2] is not None) + 0.4
        J(f"#{cn}", tc, 0.6, {"opacity": 1, "scaleX": 1}, "power2.out"); J(f"#{cn}", t_out - 0.3, 0.25, {"opacity": 0}, "power1.in")
    elif lay == "row4":
        files = [("Rider", "rider-07-garage-top.png"), ("Workshop owner", "owner-01-workshop-home.png"), ("Staff", "staff-05-saved-record-bike-history.png"), ("Admin", "admin-01-workshops-pending.png")]
        fids = []
        for k, (rl, f) in enumerate(files):
            fid = uid("fr"); frame_open(fid, 330 + 420 * k, 70, SC4, rl.upper(), P.ROLE[rl]); lid = uid("ly")
            els.append(layer_html(lid, f, [], bs[0]["L"], SC4, t_in, t_out, rl)); frame_close(); frame_anim(fid, t_in + 0.12 * k, t_out); fids.append(fid)
        for B_ in bs:
            act = B_["shot"][1] if len(B_["shot"]) > 1 else None
            if t_in + 1.0 < B_["t0"] < t_out - 0.7:
                for k, fid in enumerate(fids): J(f"#{fid}", B_["t0"], 0.3, {"opacity": 1 if act in (None, k) else 0.35}, "power1.inOut")
    elif lay == "strip":
        files = bs[0]["shot"][1]
        for k, f in enumerate(files):
            fid = uid("fr"); frame_open(fid, 330 + 420 * k, 70, SC4); lid = uid("ly"); els.append(layer_html(lid, f, [], bs[0]["L"], SC4, t_in, t_out, role)); frame_close()
            frame_anim(fid, t_in + 0.18 * k, t_out)
    elif lay == "ways":
        groups = [("A", "Sell to a RevLog rider", [("rider-25-receive-code.png", "BUYER: RECEIVE CODE", 400), ("transfer-02-sell-to-revlog-rider.png", "SELLER", 820)]),
                  ("B", "Transfer to a buyer", [("transfer-03-transfer-to-buyer-verified.png", "SELLER: LOCKED FILE", 1460)])]
        els.append('<div id="wdiv" class="wdiv"></div>'); INIT("#wdiv", {"opacity": 0}); J("#wdiv", t_in + 0.2, 0.4, {"opacity": 1}); J("#wdiv", t_out - 0.3, 0.25, {"opacity": 0})
        for g, title, ph in groups:
            hid = uid("wh"); hx = 610 if g == "A" else 1460
            els.append(f'<div id="{hid}" class="whead" style="left:{hx - 300}px">{"1" if g == "A" else "2"} · {esc(title)}</div>'); INIT(f"#{hid}", {"opacity": 0, "y": 10}); J(f"#{hid}", t_in + 0.2, 0.4, {"opacity": 1, "y": 0}); J(f"#{hid}", t_out - 0.3, 0.25, {"opacity": 0})
            gids = [hid]
            for f, lab, cx in ph:
                fid = uid("fr"); frame_open(fid, cx, 128, 0.52, lab, P.ROLE["Rider"]); lid = uid("ly"); els.append(layer_html(lid, f, [], bs[0]["L"], 0.52, t_in, t_out, "Rider")); frame_close()
                frame_anim(fid, t_in + (0 if g == "A" else 0.2), t_out); gids.append(fid)
            for B_ in bs:
                act = B_["shot"][1]
                if t_in + 1.0 < B_["t0"] < t_out - 0.7:
                    for gid in gids: J(f"#{gid}", B_["t0"], 0.3, {"opacity": 1 if act in (None, g) else 0.35}, "power1.inOut")
    elif lay == "card":
        title, sub = bs[0]["shot"][1], bs[0]["shot"][2]; cid = uid("cd")
        els.append(f'<div id="{cid}" class="tcard"><div class="tc1">{esc(title)}</div><div class="tc2">{esc(sub)}</div></div>')
        INIT(f"#{cid}", {"opacity": 0, "y": 16}); J(f"#{cid}", t_in + 0.4, 0.35, {"opacity": 1, "y": 0}); J(f"#{cid}", t_out - 0.6, 0.25, {"opacity": 0})   # never overlaps the phones either side
    elif lay == "close":
        fid = uid("fr"); frame_open(fid, 960, 150, 0.5); lid = uid("ly"); els.append(layer_html(lid, "visit-03-rider-history-workshop-badge.png", [], bs[0]["L"], 0.5, t_in, t_out, None)); frame_close(); frame_anim(fid, t_in, TOTAL)
        pos = [("Rider", 420, 260), ("Workshop owner", 1500, 260), ("Staff", 420, 640), ("Admin", 1500, 640)]
        for k, (rl, x, y) in enumerate(pos):
            rid = uid("cr"); lid2 = uid("cl"); x2 = 960 - 160 if x < 960 else 960 + 160
            els.append(f'<svg id="{lid2}" class="cline" width="1920" height="1080"><line x1="{x + (150 if x < 960 else -150)}" y1="{y + 26}" x2="{x2}" y2="{y + 26 + (60 if y < 500 else -60)}" stroke="{P.ROLE[rl]}" stroke-width="2"/></svg>')
            els.append(f'<div id="{rid}" class="crole" style="left:{x - 150}px;top:{y}px;color:{P.ROLE[rl]};border-color:{P.ROLE[rl]}">{esc(rl.upper())}</div>')
            ta = bs[0]["t0"] + 0.5 + 0.35 * k
            INIT(f"#{rid}", {"opacity": 0, "y": 10}); J(f"#{rid}", ta, 0.4, {"opacity": 1, "y": 0}); INIT(f"#{lid2}", {"opacity": 0}); J(f"#{lid2}", ta + 0.2, 0.4, {"opacity": 1})
            J(f"#{rid}", bs[-1]["t0"] - 0.2, 0.4, {"opacity": 0}); J(f"#{lid2}", bs[-1]["t0"] - 0.2, 0.4, {"opacity": 0})
        J(f"#{fid}", bs[-1]["t0"] - 0.2, 0.5, {"opacity": 0, "scale": 0.96})
        wm = uid("wm"); els.append(f'<div id="{wm}" class="wordmark">RevLog</div><div id="{wm}s" class="wmsub">One service record for every bike</div>')
        INIT(f"#{wm}", {"opacity": 0, "y": 14}); J(f"#{wm}", bs[-1]["t0"] + 0.1, 0.6, {"opacity": 1, "y": 0}); INIT(f"#{wm}s", {"opacity": 0}); J(f"#{wm}s", bs[-1]["t0"] + 0.6, 0.5, {"opacity": 1})

# ---------------- chrome: chapter eyebrow, role chip, progress bar ----------------
ch_t = {}
for L in tl: ch_t.setdefault(L["ch"], [L["t0"], L["t1"]]); ch_t[L["ch"]][1] = L["t1"]
for c, (a, b_) in ch_t.items():
    eid = f"ey{c}"; els.append(f'<div id="{eid}" class="eyebrow"><b>{c + 1:02d}</b>{esc(P.CHAPTERS[c].upper())}</div>')
    INIT(f"#{eid}", {"opacity": 0}); J(f"#{eid}", a - 0.3, 0.3, {"opacity": 1}); J(f"#{eid}", b_ - 0.25, 0.25, {"opacity": 0})
roles = []                                               # role chip per run of the same scene role
for L in tl:
    if roles and roles[-1][0] == L["role"]: roles[-1][2] = L["t1"]
    else: roles.append([L["role"], L["t0"], L["t1"]])
for rl, a, b_ in roles:
    if not rl: continue
    rid = uid("rc"); els.append(f'<div id="{rid}" class="rolechip" style="color:{P.ROLE[rl]};border-color:{P.ROLE[rl]}"><i style="background:{P.ROLE[rl]}"></i>{esc(rl)}</div>')
    INIT(f"#{rid}", {"opacity": 0, "x": -12}); J(f"#{rid}", a - 0.2, 0.3, {"opacity": 1, "x": 0}); J(f"#{rid}", b_ - 0.25, 0.25, {"opacity": 0})
seg_w = 1800 / 10
els.append('<div class="pbar">' + "".join(f'<div class="pseg" style="left:{60 + seg_w * c}px;width:{seg_w - 8}px"><div class="plab" id="pl{c}">{esc(P.CHAPTERS[c])}</div><div class="ptrack"><i id="pf{c}"></i></div></div>' for c in range(10)) + '</div>')
for c, (a, b_) in ch_t.items():
    INIT(f"#pf{c}", {"scaleX": 0, "transformOrigin": "0% 50%"}); SET(f"#pf{c}", a, {"scaleX": 0}); J(f"#pf{c}", a, b_ - a, {"scaleX": 1}, "none")
    INIT(f"#pl{c}", {"opacity": 0.45}); J(f"#pl{c}", a - 0.2, 0.25, {"opacity": 1}); J(f"#pl{c}", b_, 0.25, {"opacity": 0.45})

# ---------------- captions: a phrase at a time, words exactly as narrated ----------------
def phrases(text, maxc=58):
    """phrases of up to ~58 characters; break after punctuation when the phrase is already long enough"""
    out, cur = [], []
    for w in text.split():
        if cur and (len(" ".join(cur + [w])) > maxc or (re.search(r"[,:;.?]$", cur[-1]) and len(" ".join(cur)) >= 34)): out.append(" ".join(cur)); cur = []
        cur.append(w)
    if cur:
        if out and len(" ".join(cur)) < 16 and len(out[-1]) + len(" ".join(cur)) < 72: out[-1] += " " + " ".join(cur)
        else: out.append(" ".join(cur))
    return out
srt, cn = [], 0
for L in tl:
    if not L["text"]: continue
    ph = phrases(L["text"]); sw = L["text"].split(); hw = L["words"]
    def tw(k):                                           # time of the k-th script word (mapped proportionally onto the heard words)
        if not hw: return L["t0"] + (L["sp"] - L["t0"]) * k / len(sw)
        j = min(len(hw) - 1, round(k * len(hw) / len(sw))); return L["t0"] + hw[j]["t"]
    k = 0
    for j, p in enumerate(ph):
        a = L["t0"] if j == 0 else tw(k); k += len(p.split()); b_ = (tw(k) if j + 1 < len(ph) else min(L["t1"] - 0.04, L["sp"] + 0.4))
        cid = f"cap{cn}"; cn += 1; els.append(f'<div id="{cid}" class="cap"><span>{esc(p)}</span></div>')
        INIT(f"#{cid}", {"opacity": 0}); J(f"#{cid}", a, 0.12, {"opacity": 1}, "none"); SET(f"#{cid}", b_ - 0.02, {"opacity": 0}); srt.append((a, b_, p))
fmt_t = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round((x % 1) * 1000)) % 1000:03d}"
open("video/captions.srt", "w").write("".join(f"{i + 1}\n{fmt_t(a)} --> {fmt_t(b_)}\n{p}\n\n" for i, (a, b_, p) in enumerate(srt)))

CSS = open("build22.css").read()
doc = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-start="0" data-duration="{TOTAL}">
      <div id="gfx" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="1">
        <div id="stage">
        {(chr(10) + "        ").join(e for e in els if not e.startswith(('<div id="cap', '<div class="pbar', '<div id="ey', '<div id="rc')))}
        </div>
        {(chr(10) + "        ").join(e for e in els if e.startswith(('<div id="cap', '<div class="pbar', '<div id="ey', '<div id="rc')))}
      </div>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      {(chr(10) + "      ").join(init)}
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(js)}
      tl.set({{}}, {{}}, {TOTAL});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(f"{OUT}/index.html", "w").write(doc)
json.dump(dict(total=TOTAL, lines=[{k: L[k] for k in ("scene", "n", "t0", "sp", "t1", "text", "file", "i0", "sr")} for L in tl], cues=sorted(CUES), used=sorted(used),
               chapters={P.CHAPTERS[c]: v for c, v in ch_t.items()}), open("layout.json", "w"), indent=1)
print("built", TOTAL, "s;", len(tl), "lines;", len(beats), "beats;", len(used), "screenshots;", cn, "caption phrases;", len(js), "tweens")
