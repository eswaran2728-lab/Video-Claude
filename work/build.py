import json,re,html
tr=json.load(open("transcript.json"))
words=[w for s in tr for w in s["words"]]
edl=[l.split() for l in open("edl.json.tmp")]
edl=[(float(a),float(b),float(c),n) for a,b,c,n in edl]
nw=[]
for s,e,ns,n in edl:
    for w in words:
        if w["s"]>=s-0.05 and w["e"]<=e+0.1:
            nw.append({"w":w["w"].strip(),"s":round(w["s"]-s+ns,2),"e":round(min(w["e"],e)-s+ns,2),"seg":n})
def find(word,after=0):
    for w in nw:
        if w["s"]>=after and word.lower() in w["w"].lower(): return w["s"]
    raise Exception(word)
# phrases
BAKED=(111.0,131.0)
ph=[];cur=[]
for i,w in enumerate(nw):
    cur.append(w)
    nxt=nw[i+1] if i+1<len(nw) else None
    if len(cur)>=5 or re.search(r"[.,?!]$",w["w"]) or not nxt or nxt["seg"]!=w["seg"] or nxt["s"]-w["e"]>0.6:
        ph.append(cur);cur=[]
ph=[p for p in ph if not (BAKED[0]<=p[0]["s"]<BAKED[1])]
KEY={"tailgating.","visible","high.","lock","report","immediately.","escort","failure.","alert,","security","you."}
cap_html=[];cap_js=[]
for i,p in enumerate(ph):
    st=p[0]["s"];en=max(p[-1]["e"]+0.15,st+0.6)
    if i+1<len(ph): en=min(en,ph[i+1][0]["s"]-0.02)
    spans="".join(f'<span class="w{" k" if w["w"].lower() in KEY else ""}" id="c{i}w{j}">{html.escape(w["w"])}</span> ' for j,w in enumerate(p))
    rz=" raise" if st<29.5 else ""
    cap_html.append(f'<div id="cap{i}" class="clip cap{rz}" data-start="{st:.2f}" data-duration="{en-st:.2f}" data-track-index="2"><div class="capbox">{spans}</div></div>')
    cap_js.append(f'tl.from("#cap{i} .capbox",{{y:24,opacity:0,duration:0.18,ease:"power2.out"}},{st:.2f});')
    for j,w in enumerate(p):
        cap_js.append(f'tl.to("#c{i}w{j}",{{color:"var(--hl)",duration:0.05}},{w["s"]:.2f});')
T={"tail":find("tailgating"),"lock":find("Lock",60),"report":find("report",70),"fail":find("failure",90),
   "escort":find("escort",99),"visible":find("visible",42),"high":find("high",58),"see":find("See",126),"secu":find("Security",128)}
mods=[(5.4,"01","ANTI-TAILGATING"),(29.5,"02","BADGE VISIBILITY"),(63.6,"03","ASSET & PACKAGE"),(81.1,"04","VISITOR MANAGEMENT"),(109.7,"05","INCIDENT REPORTING")]
sfx=[]
def S(name,t,vol=1):sfx.append((name,round(t,2),vol))
S("impact",T["tail"]-0.05)
for t,_,_ in mods: S("whoosh",t-0.15)
S("pop",11.25); S("ding",14.1); S("pop",T["visible"]); S("impact",T["high"]-0.05,0.6)
S("pop",T["lock"]); S("buzz",75.6); S("pop",T["report"]); S("buzz",T["fail"]-0.05); S("ding",T["escort"])
S("buzz",111.4); S("impact",T["see"]-0.05); S("whoosh",130.4)
out=open("index.tpl.html").read()
modhtml="".join(f'<div id="mod{n}" class="clip modchip" style="inset:auto;left:72px;top:72px;width:300px;height:auto" data-start="{t:.2f}" data-duration="2.6" data-track-index="3"><div class="mnum">MODULE {n}<span>/05</span></div><div class="mbar"></div></div>' for t,n,_ in mods)
modjs="".join(f'tl.from("#mod{n}",{{x:-60,opacity:0,duration:0.35,ease:"back.out(1.6)"}},{t:.2f});tl.from("#mod{n} .mbar",{{scaleX:0,duration:0.6,ease:"power3.out"}},{t+0.15:.2f});tl.to("#mod{n}",{{opacity:0,duration:0.3}},{t+2.25:.2f});' for t,n,_ in mods)
prog="".join(f'tl.to("#pseg{i}",{{scaleX:1,duration:{(mods[i+1][0] if i<4 else 130.5)-t:.2f},ease:"none"}},{t:.2f});' for i,(t,_,_) in enumerate(mods))
sfxhtml="".join(f'<audio id="sfx{i}" class="clip" src="sfx/{n}.wav" data-start="{t:.2f}" data-duration="0.8" data-track-index="{10+i%4}" data-volume="{v}"></audio>' for i,(n,t,v) in enumerate(sfx))
rep={"CAPS":"\n".join(cap_html),"CAPJS":"\n".join(cap_js),"MODS":modhtml,"MODJS":modjs,"PROGJS":prog,"SFX":sfxhtml}
for k,v in T.items(): rep["T_"+k]=f"{v:.2f}"
for k,v in rep.items(): out=out.replace("%%"+k+"%%",v)
open("avsec-edit/index.html","w").write(out)
print(T); print(len(ph),"captions",len(sfx),"sfx")
