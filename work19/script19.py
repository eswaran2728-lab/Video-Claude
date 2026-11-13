# FOCA Checklist (AA/SEC/F/070) - the creator's narration (script19_raw.md, verbatim) split into scenes and sentences.
# Lines starting "@" are the creator's trainer directions ("Point to...", "Show...", "Ask trainees..."): not spoken, kept as
# `notes` so the motion graphics do the pointing. `spoken()` only helps the AI voice with codes and abbreviations.
import re
RAW = open("script19_raw.md").read()
SAY = [(r"AA/SEC/F/070", "A. A. S. E. C. F. zero seven zero"), (r"AA-SEC", "A. A. S. E. C."), (r"\(RESTRICTED\)", ", restricted,"),
       (r"airasia\.com", "Air Asia dot com"), (r"\bSTA\b", "S. T. A."), (r"\bATA\b", "A. T. A."), (r"\bSTD\b", "S. T. D."), (r"\bATD\b", "A. T. D."),
       (r"\(PDF to Drive \+ Sheet\)", ", P D F to Drive plus Sheet,"), (r"\bID\b", "I D"), (r"\bPDF\b", "P D F"), (r"Wi-Fi", "wifi"),
       (r"Saving\.\.\.,", "Saving,"), (r"Keep it on Restricted\.", "Keep it on, Restricted."), (r"Required/Completed", "Required, Completed,"), (r"SECURITY STAFF", "Security Staff"), (r"[“”]", "")]


def spoken(t):
    for a, b in SAY: t = re.sub(a, b, t)
    return t


def sentences(p):
    out = []
    for s in [s.strip() for s in re.split(r"(?<=[.?!])\s+(?=[A-Z“\"])", p) if s.strip()]:
        if out and re.fullmatch(r"(One|Two|Three|Four|Five)\.", out[-1]): out[-1] += " " + s     # "One. Are the flight details..."
        else: out.append(s)
    return out


SCENES = []
for blk in re.split(r"^### ", RAW, flags=re.M)[1:]:
    head, *paras = [l.strip() for l in blk.strip().split("\n") if l.strip()]
    n, title = re.match(r"Slide (\d+) — (.*)", head).groups()
    lines, notes = [], []
    for p in paras:
        if p.startswith("@"): notes.append(p[1:].strip()); continue
        for s in sentences(p): lines.append((s, None, spoken(s)))
    SCENES.append(dict(id=f"s{int(n):02d}", n=int(n), title=title, lines=lines, notes=notes))
