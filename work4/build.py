import json
edl=json.load(open("edl_final.json"));B=json.load(open("beats_ext.json"))["beats"]
TOTAL=54.72
cuts=[round(e["t0"],3) for e in edl]
phr=[0.0]+[round(B[i],3) for i in (16,32,48,64,80,96) if i<len(B)]
words=["SILAMBAM","SPEED","POWER","FOCUS","DISCIPLINE","TRADITION","UNITY"]
fast=[e["t0"] for e in edl if e["t1"]-e["t0"]<1.2]
FINAL=53.655
wordsH="\n".join(f'      <div id="kw{i}" class="clip kw" data-start="{t+0.05:.3f}" data-duration="{(1.7 if i else 1.85):.3f}" data-track-index="4"><span>{w}</span></div>' for i,(t,w) in enumerate(zip(phr,words)) if t+0.05<FINAL-0.5)
js=[]
for t in cuts[1:]:
    js.append(f'tl.fromTo("#bw", {{ scale: 1.07 }}, {{ scale: 1.0, duration: 0.32, ease: "power3.out", immediateRender: false }}, {t:.3f});')
for t in phr[1:]:
    js.append(f'tl.fromTo("#flash", {{ opacity: 0.55 }}, {{ opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false }}, {t:.3f});')
    js.append(f'tl.fromTo("#hdr .shine", {{ xPercent: -160, skewX: -20 }}, {{ xPercent: 640, skewX: -20, duration: 0.9, ease: "power2.inOut", immediateRender: false }}, {t:.3f});')
    js.append(f'tl.fromTo("#logo", {{ scale: 1.08 }}, {{ scale: 1.0, duration: 0.45, ease: "back.out(2)", immediateRender: false }}, {t:.3f});')
for t in fast:
    js.append(f'tl.fromTo("#streak", {{ xPercent: -120, skewX: -20, opacity: 0.9 }}, {{ xPercent: 420, skewX: -20, opacity: 0, duration: 0.35, ease: "power1.in", immediateRender: false }}, {t:.3f});')
for i,(t,w) in enumerate(zip(phr,words)):
    if t+0.05>=FINAL-0.5: continue
    d=1.7 if i else 1.85
    js.append(f'tl.from("#kw{i} span", {{ x: -140, skewX: -18, opacity: 0, duration: 0.28, ease: "power4.out" }}, {t+0.05:.3f});')
    js.append(f'tl.to("#kw{i} span", {{ x: 120, opacity: 0, duration: 0.22, ease: "power2.in" }}, {t+0.05+d-0.24:.3f});')
tpl=open("index.tpl.html").read()
for k,v in dict(TOTAL=f"{TOTAL}",WORDS=wordsH,JS="\n      ".join(js),FINAL=f"{FINAL}",FINALD=f"{TOTAL-FINAL:.3f}").items(): tpl=tpl.replace("%%"+k+"%%",v)
open("edit/index.html","w").write(tpl);print("cuts",len(cuts),"phrases",phr,"fast",len(fast))
