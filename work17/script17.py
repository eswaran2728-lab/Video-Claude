# AA/SEC/F/042 High-Lift Escort eForm - the creator's slide-by-slide narration (script17_raw.md, verbatim), parsed into scenes.
# Captions show the script text; `spoken()` only changes how the AI voice reads codes, sample IDs and times.
import re
RAW = open("script17_raw.md").read()
SAY = [
    (r"AA/SEC/F/042", "A. A. S. E. C. F. zero four two"), (r" – ", ", "),
    (r"TEST-AK01", "test, A K zero one"), (r"KUL-TEST", "K U L, test"), (r"TEST-HL01", "test, H L zero one"),
    (r"TEST-0001", "test, zero zero zero one"), (r"TEST001", "test, zero zero one"), (r"TEST002", "test, zero zero two"),
    (r"TEST USER 2", "test user two"), (r"\b10:00 AM\b", "ten a.m."), (r"\b10:00 PM\b", "ten p.m."), (r"\b10:00\b", "ten"),
    (r"\b11:30 AM\b", "eleven thirty a.m."), (r"\b10:30 AM\b", "ten thirty a.m."), (r"\b10:45\b", "ten forty-five"),
    (r"\bAM or PM selection\b", "AM-or-PM selection"), (r"\bAM or PM\b", "a.m. or p.m."), (r"\bAM\b", "a.m."), (r"\bPM\b", "p.m."), (r"\bETD\b", "E T D"), (r"\bQR\b", "Q R"),
    (r"Staff ID", "Staff I D"), (r"staff ID", "staff I D"), (r"Staff No\.", "Staff Number"), (r"\bAVSEC\b", "Av-Sec"),
    (r"eForm", "e-Form"), (r'"', ""),
]


def spoken(t):
    for a, b in SAY: t = re.sub(a, b, t)
    return t


SCENES = []
for blk in re.split(r"^### ", RAW, flags=re.M)[1:]:
    head, *lines = [l.strip() for l in blk.strip().split("\n") if l.strip()]
    n, title = re.match(r"Slide (\d+) – (.*)", head).groups()
    SCENES.append(dict(id=f"s{int(n):02d}", n=int(n), title=title, lines=[(l, None, spoken(l)) for l in lines]))
