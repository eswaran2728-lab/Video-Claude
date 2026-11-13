# Shared v02 treatments for the slides every Partner Briefing deck has (same layout in all four decks):
# title, What changed, How it works, What you need, This part is for, Last step, After signing, Remember, Where your signature goes.
# Every slide is shown in full first; highlights / rings land on the spoken word (whisper word times).
B, O, A, G, RD, W = "#0b57d0", "#b8550d", "#ffb000", "#188038", "#c8102e", "#ffffff"
WARN = []
import json as _j
ORIG = _j.load(open("orig20.json"))


def orc(v, page, x0, y0, x1, y1):
    """a rectangle on the original paper form (PDF pixels at 200 dpi) -> slide coordinates of the stage image o-<page>.jpg"""
    o = ORIG[v][str(page)]; s = o["s"]; return (o["x0"] + x0 * s, o["y0"] + y0 * s, (x1 - x0) * s, (y1 - y0) * s)


def spans(P, K):
    """slide -> (t0, t1): a slide is on screen from just before its first sentence until the next slide starts"""
    L = K["LINES"]; order = []
    for l in L:
        if l["slide"] not in order: order.append(l["slide"])
    t0 = {}
    for n in order:
        l = L[P.sl(n)]; first = l["i"] == 0 or L[l["i"] - 1]["scene"] != l["scene"]
        t0[n] = P.S(l["scene"]) if first else P.A(n, -0.4)
    return {n: (t0[n], t0[order[j + 1]] if j + 1 < len(order) else P.total) for j, n in enumerate(order)}


def lines(P, n): return [P.sl(n, j) for j in range(P.nsl(n))]


def has(K, i, word): return any(w["w"] == word for w in K["LINES"][i]["words"])


def line_with(P, K, n, word, k=0):
    hits = [i for i in lines(P, n) if has(K, i, word)]
    return hits[k] if len(hits) > k else None


def line_start(P, K, n, word):
    return next(i for i in lines(P, n) if K["LINES"][i]["words"] and K["LINES"][i]["words"][0]["w"] == word)


def wt(P, K, n, word, k=0, d=0.0, default=None):
    """time of the k-th spoken `word` on slide n"""
    ts = [w["t"] for i in lines(P, n) for w in K["LINES"][i]["words"] if w["w"] == word]
    if len(ts) > k: return round(ts[k] + d, 3)
    WARN.append(f"slide {n}: word '{word}' #{k} not heard"); return default if default is not None else P.A(n, 0.3)


def rowrect(P, K, n, sub):
    """a list row on the slide: its text box plus the numbered circle on the same row"""
    x, y, w, h = P.txt(n, sub); cy = y + h / 2; x1 = x + w
    for d in K["SHAPES"][n]:
        if d["kind"] != "pic" and d.get("fill") and abs(d["y"] + d["h"] / 2 - cy) < 45 and d["x"] < x and d["w"] < 200: x = min(x, d["x"])
    return (x, y, x1 - x, h)


def title(P, K, n, sp):
    t0, t1 = sp[n]; sh = K["Shot"](n, t0, t1)
    sh.hl(P.A(n, 0.2), P.txt(n, "now signed on a phone"), t1)
    sh.hl(wt(P, K, n, "guide", d=-0.1) if heard(P, K, n, "guide") else P.L(lines(P, n)[-1], 0.2), P.txt(n, "For "), t1).done()


def changed(P, K, n, sp, paper):
    t0, t1 = sp[n]; ib, inow = line_with(P, K, n, "before"), line_with(P, K, n, "now")
    sh = K["Shot"](n, t0, P.L(inow, -0.2))
    if ib != P.sl(n): sh.hl(P.A(n, 0.1), P.txt(n, "From paper to one phone"), P.L(inow, -0.2))
    sh.hl(P.L(ib, 0.1), (100.8, 288, 820.8, 619.2), P.L(inow, -0.2), "#5f6368").done()
    rest = [i for i in lines(P, n) if i > inow]; c_end = P.L(rest[0], -0.2) if rest else t1
    K["before_now"](P.L(inow, -0.2), c_end, paper, P.W(inow, "now") + 0.1, (P.W(inow, "saved") - 0.3) if has(K, inow, "saved") else None)
    if rest:
        sh = K["Shot"](n, c_end, t1).hl(c_end, (1000.8, 288, 820.8, 619.2), t1, RD)
        sh.hl(P.L(rest[0], 0.1), P.txt(n, "You sign there and then"), t1)
        sh.hl(wt(P, K, n, "saved", d=-0.2), P.txt(n, "Signed PDF is saved"), t1)
        sh.hl(wt(P, K, n, "restricted", d=-0.2), P.txt(n, "Kept in a restricted"), t1).done()


def steps(P, K, n, sp, signer):
    t0, t1 = sp[n]; sh = K["Shot"](n, t0, t1)
    PN = [(100.8, 331.2, 396, 432), (554.4, 331.2, 396, 432), (1008, 331.2, 396, 432), (1461.6, 331.2, 396, 432)]
    ty, tb, to = P.L(line_start(P, K, n, "you"), 0.1), wt(P, K, n, "blue", d=-0.1), wt(P, K, n, "orange", d=-0.1)
    for j, (t, c) in enumerate(((wt(P, K, n, "fills", d=-0.3), B), (wt(P, K, n, "hands", d=-0.2), B), (ty, O), (wt(P, K, n, "back", d=-0.3), B))): sh.hl(t, PN[j], tb, c)
    for j in (0, 1, 3): sh.ring(tb, PN[j], to, B, sfx=j == 0)
    sh.ring(to, PN[2], t1, O).hl(to, P.txt(n, "YOUR PART"), t1, O).done()
    K["role"](wt(P, K, n, "hands", d=0.5), signer, O); K["role"](wt(P, K, n, "back"), "SECURITY", B)


def keyed(P, K, n, sh, keys, t_end, keep=True):
    """keys: [(word, k, rect, color)] -> highlight each rect when its word is spoken"""
    ev = sorted((wt(P, K, n, w, k, -0.2), r, c) for w, k, r, c in keys)
    for j, (t, r, c) in enumerate(ev): sh.hl(t, r, t_end if keep or j + 1 == len(ev) else ev[j + 1][0] + 0.25, c)
    return sh


def heard(P, K, n, w): return any(has(K, i, w) for i in lines(P, n))


def need(P, K, n, sp):
    t0, t1 = sp[n]; sh = K["Shot"](n, t0, t1)
    keys = [("install", 0, P.txt(n, "Nothing to install"), A), ("brings" if heard(P, K, n, "brings") else "account", 0, rowrect(P, K, n, "No app, no login"), A),
            ("read", 0, rowrect(P, K, n, "Read the form"), A), ("only", 0, rowrect(P, K, n, "Sign only for yourself"), A)]
    if heard(P, K, n, "ready"): keys.append(("ready", 0, rowrect(P, K, n, "Have your own name"), A))
    keyed(P, K, n, sh, keys, t1).done()


def part(P, K, n, sp):
    """'This part is for' slide: the audience rows, then the footnote line"""
    t0, t1 = sp[n]; sh = K["Shot"](n, t0, t1); ls = lines(P, n)
    rows = [d for d in K["SHAPES"][n] if d["kind"] != "pic" and d.get("t", "").strip() and 520 < d["y"] < 760 and d["x"] > 200]
    for j, d in enumerate(rows): sh.hl(P.L(ls[0], 0.3 + 0.6 * j), (d["x"] - 130, d["y"], d["w"] + 130, d["h"]), t1, O)
    foot = [d for d in K["SHAPES"][n] if d["kind"] != "pic" and d.get("t", "").strip() and d["y"] > 900]
    if foot and len(ls) > 1: sh.hl(P.L(ls[1], 0.1), (foot[0]["x"], foot[0]["y"], foot[0]["w"], foot[0]["h"]), t1)
    sh.done()


def last(P, K, n, sp, signer):
    """Last step: give the phone back to Security (slide -> handover animation -> slide)"""
    t0, t1 = sp[n]; s0, s1 = lines(P, n)[0], lines(P, n)[-1]; tb = P.W(s0, "back")
    K["Shot"](n, t0, tb - 0.3).hl(P.A(n, 0.2), rowrect(P, K, n, "Screen says"), tb - 0.3).done()
    K["handover"](tb - 0.3, P.L(s1, -0.2), (signer, O), ("SECURITY", B), "Give the phone back to Security", t_move=tb + 0.1)
    K["role"](tb + 1.0, "SECURITY", B)
    sh = K["Shot"](n, P.L(s1, -0.2), t1).hl(P.L(s1, -0.2), rowrect(P, K, n, "Screen says"), t1)
    sh.hl(P.L(s1, 0.2), rowrect(P, K, n, "Security signs and saves"), t1, B).done()


def after_pdf(P, K, n, sp):
    """FOCA: the deck's real signed TEST PDF"""
    t0, t1 = sp[n]; ls = lines(P, n); ir, ie = line_with(P, K, n, "real"), line_with(P, K, n, "email")
    sh = K["Shot"](n, t0, t1)
    sh.hl(P.A(n, 0.1), rowrect(P, K, n, "Security saves. The app"), P.L(ir, -0.1))
    sh.cam(P.L(ir, -0.2), 619, 540, 990).hl(P.L(ir, 0.3), (712, 432, 112, 30), P.L(ie, -0.1))
    sh.ring(P.L(ir, 0.6), (152.0, 290.4, 414.4, 29.6), P.L(ie, -0.1), A, sfx=False)
    sh.cam(P.L(ie, -0.3), 960, 540, 1920).hl(P.L(ie, 0.1), rowrect(P, K, n, "Security staff email"), t1).hl(P.L(ie, 0.5), (1209.6, 720, 619.2, 194.4), t1)
    sh.hl(wt(P, K, n, "keep", d=-0.2), rowrect(P, K, n, "Keep it for your records"), t1).done()
    K["stage_label"](P.L(ir, -0.2), P.L(ie, -0.3), "REAL SIGNED PDF · TEST RECORD")


def after_saved(P, K, n, sp, saved, rid):
    """NOTOC / AOR / Search List: the deck's real Saved screen + PDF filename example"""
    t0, t1 = sp[n]; ie = line_with(P, K, n, "email"); tr, tf = wt(P, K, n, "id", d=-0.4), wt(P, K, n, "file" if heard(P, K, n, "file") else "filename", d=-0.2)
    sh = K["Shot"](n, t0, t1)
    sh.camfit(P.A(n, 0.3), saved, pad=1.3, wmin=640).hl(P.A(n, 0.6), saved, tr)
    sh.ring(tr, rid, tf + 0.3, A, sfx=False)
    sh.camfit(tf, (778, 720, 1051, 194), pad=1.1).hl(tf + 0.3, (778, 720, 1051, 194), P.L(ie, -0.1))
    sh.cam(P.L(ie, -0.3), 960, 540, 1920).hl(P.L(ie, -0.2), rowrect(P, K, n, "Security saves. The app"), t1)
    sh.hl(P.L(ie, 0.1), rowrect(P, K, n, "Security staff email"), t1).hl(wt(P, K, n, "keep", d=-0.2), rowrect(P, K, n, "Keep it for your records"), t1).done()
    K["stage_label"](t0, tf, "SAVED SCREEN · TEST RECORD"); K["stage_label"](tf, P.L(ie, -0.3), "PDF FILENAME EXAMPLE")


def remember(P, K, n, sp):
    t0, t1 = sp[n]; sh = K["Shot"](n, t0, t1)
    do = [("check", 0, "Check your name and role"), ("read", 0, "Read the details before"), ("type", 0, "Type your own name"), ("finger", 0, "Sign with your finger"), ("hand", 0, "Hand the phone back")]
    dont = [("someone", 0, "Sign for someone else"), ("wrong", 0, "Sign if the details are wrong"), ("close", 0, "Close the app"), ("photos", 0, "Take photos")]
    kd = [(w, k, P.txt(n, s), G) for w, k, s in do if heard(P, K, n, w)]; kx = [(w, k, P.txt(n, s), RD) for w, k, s in dont if heard(P, K, n, w)]
    t_do, t_dont = min(wt(P, K, n, w, k) for w, k, _, _ in kd), min(wt(P, K, n, w, k) for w, k, _, _ in kx)
    sh.cam(t_do - 0.5, 525, 640, 1080).cam(t_dont - 0.6, 1430, 620, 980)
    keyed(P, K, n, sh, kd + kx, t1).done()


def where(P, K, n, sp, pdf_label="Signed PDF<br>with Record ID", summary_steps=("Check", "Sign", "Confirm", "Hand back"), sub=None):
    """Where your signature goes: slide -> flow (PDF -> restricted folder -> record log -> email) -> slide (questions) -> summary"""
    t0, t1 = sp[n]; ls = lines(P, n); i1 = line_with(P, K, n, "restricted"); iq = line_with(P, K, n, "question")
    sh = K["Shot"](n, t0, P.L(i1, -0.2)).hl(P.A(n, 0.2), P.txt(n, "Into a signed PDF"), P.L(i1, -0.2))
    sh.hl(wt(P, K, n, "one", d=-0.1), P.txt(n, "One PDF per form"), P.L(i1, -0.2)).done()
    mail = "emailed" if line_with(P, K, n, "emailed") is not None else "email"
    f_end = P.L(iq, -0.2) if iq is not None else P.E(ls[-1], 0.6)
    K["flow"](P.L(i1, -0.2), f_end, "Where your signature goes", [("pdf", pdf_label, P.L(i1, -0.1)), ("folder", "Restricted<br>AirAsia folder", wt(P, K, n, "restricted", d=-0.2)),
                                                                  ("log", "Record<br>log", wt(P, K, n, "log", d=-0.2)), ("mail", "PDF copy<br>by email", wt(P, K, n, mail, d=-0.2))])
    if iq is not None:
        s_end = P.E(ls[-1], 0.6)
        K["Shot"](n, f_end, s_end).hl(P.L(iq, 0.1), P.txt(n, "Have a question"), s_end).done()
    else: s_end = f_end
    K["summary"](s_end, P.total, list(summary_steps), sub=sub)
