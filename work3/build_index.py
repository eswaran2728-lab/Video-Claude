import json,html
HO=3.50
edl=json.load(open("edl.json"));F=30
BODY=edl[-1][2]/F+(edl[-1][1]-edl[-1][0])/F;TOTAL=round(HO+BODY,3)
def M(src):
    for fa,fb,o in edl:
        if fa/F-1e-6<=src<=fb/F+1e-6: return round(HO+o/F+(src-fa/F),3)
    best=min(edl,key=lambda e:min(abs(src-e[0]/F),abs(src-e[1]/F)))
    return round(HO+best[2]/F+(min(max(src,best[0]/F),best[1]/F)-best[0]/F),3)
CAPS=[(1.07,1.93,"Vanakkam nanbargale!",[]),
(3.37,4.95,"Naan ellaar kittayum",[]),(5.0,6.15,"romba mannippu kekkuren.",["mannippu"]),
(6.6,9.1,"Yenna-na, naan last-a potta oru video,",["video,"]),
(10.6,11.75,"naan edit pannirundhen.",[]),
(13.7,14.7,"Antha video-la naan",[]),(14.74,17.15,"Mayana Kaali-nu sollirundhen.",["Mayana","Kaali-nu"]),
(17.6,19.85,"Atharkaaga niraiya peru ennkitta",[]),(22.3,23.65,"sonneenga.",[]),
(27.25,28.25,"Romba mannichikonga.",["mannichikonga."]),
(28.3,29.3,"Yenna-na naan",[]),(29.36,31.08,"unmaiyaana Mayana Kaali pottirukken.",["unmaiyaana"]),
(39.18,41.4,"Ivanga thaan nammoda Mayana Kaali!",["Mayana","Kaali!"]),
(41.95,43.3,"So after that,",[]),(43.36,44.9,"customer request panni",["customer","request"]),
(46.72,47.9,"request pannathukkaaga,",[]),
(48.0,50.6,"Intha video neenga paartheenga,",[]),(50.7,53.9,"muzhukka customize panni senjathu.",["customize"]),
(55.55,56.85,"En thappu thaan.",["thappu"]),(58.9,60.45,"Mayana Kaali-nu sollirundhen.",["Mayana","Kaali-nu"]),
(61.5,63.9,"Niraiya peru advice panneenga,",["advice"]),
(67.4,69.3,"Still, ellathaiyum eduthukkuren.",[]),
(69.32,70.9,"Adutha thadavai video podurathukku munnadi,",[]),(70.9,72.4,"kandippa research pannuven.",["research"]),
(73.2,74.75,"Correct-aana information poduren.",["Correct-aana"]),(74.78,75.7,"Nandri, vanakkam!",["Nandri,"])]
caps=[]
for i,(a,b,t,k) in enumerate(CAPS):
    s,e=M(a),M(b)
    if i+1<len(CAPS): e=min(e,M(CAPS[i+1][0])-0.03)
    if e-s<0.3: e=s+0.3
    caps.append((s,e,t,k))
capH="\n".join(f'      <div id="cap{i}" class="clip cap" data-start="{s:.3f}" data-duration="{e-s:.3f}"><div class="cb glass">'+" ".join(f'<span class="{"k" if w in k else ""}">{html.escape(w)}</span>' for w in t.split())+'</div></div>' for i,(s,e,t,k) in enumerate(caps))
capJ="\n".join(f'      tl.from("#cap{i} .cb", {{ y: 22, opacity: 0, scale: 0.94, duration: 0.16, ease: "back.out(2)" }}, {s:.3f});' for i,(s,e,t,k) in enumerate(caps))
# B-roll placements (body-relative seconds -> absolute)
B1=(HO+3.95,2.4);B2=(HO+21.6,6.75);B3=(HO+33.75,4.85)
TITLES=[("t1",HO+0.87,2.8,["MANNIPPU","SORRY"]),("t2",HO+8.07,3.5,["MAYANA KAALI?","NOT QUITE"]),
        ("t3",HO+39.67,3.3,["EN THAPPU","MY MISTAKE"]),("t4",HO+51.1,5.0,["NEXT TIME","RESEARCH FIRST"])]
titH="\n".join(f'      <div id="{n}" class="clip mt" data-start="{s:.3f}" data-duration="{d:.3f}" data-words="{"|".join(w)}"><div class="mtd"><span class="ma"></span><span class="mb"></span></div></div>' for n,s,d,w in TITLES)
SFX=[("impact-bass-1",0.02,0.7),("error",0.35,0.5),("whoosh-cinematic",1.2,0.6),("sparkle",1.35,0.45),("chime",1.9,0.5),("whoosh-cinematic",3.3,0.5),
     ("pop",HO+0.9,0.5),("whoosh-short",B1[0]-0.05,0.6),("sparkle",B1[0]+0.05,0.4),("pop",HO+8.1,0.5),
     ("whoosh-cinematic",B2[0]-0.05,0.6),("sparkle",B2[0]+0.05,0.45),("chime",B2[0]+0.6,0.45),
     ("whoosh-short",B3[0]-0.05,0.6),("sparkle",B3[0]+0.05,0.4),("pop",HO+39.7,0.5),("pop",HO+51.12,0.5),("chime",HO+56.25,0.5)]
sfxH="\n".join(f'      <audio id="sx{i}" class="clip" src="assets/sfx/{n}.mp3" data-start="{s:.3f}" data-duration="1.2" data-volume="{v}"></audio>' for i,(n,s,v) in enumerate(SFX))
cut_js=[]
for k,(fa,fb,o) in enumerate(edl):
    st=HO+o/F
    cut_js.append(f'tl.set("#tw", {{ scale: {1.08 if k%2==0 else 1.14} }}, {st:.3f});')
for src in (27.25,55.55):
    st=M(src);cut_js.append(f'tl.fromTo("#tw", {{ scale: 1.08 }}, {{ scale: 1.2, duration: 1.2, ease: "power2.out", immediateRender: false }}, {st:.3f});')
CTAS=HO+56.2
tpl=open("index.tpl.html").read()
rep=dict(TOTAL=f"{TOTAL}",HO=f"{HO}",BODYDUR=f"{BODY:.3f}",CAPS=capH,CAPJS=capJ,TITLES=titH,SFX=sfxH,
 B1S=f"{B1[0]:.3f}",B1D=f"{B1[1]}",B2S=f"{B2[0]:.3f}",B2D=f"{B2[1]}",B3S=f"{B3[0]:.3f}",B3D=f"{B3[1]}",
 CUTJS="\n      ".join(cut_js),CTAS=f"{CTAS:.3f}",CTAD=f"{TOTAL-CTAS:.3f}")
for k,v in rep.items(): tpl=tpl.replace("%%"+k+"%%",v)
open("edit/index.html","w").write(tpl);print("TOTAL",TOTAL,"captions",len(caps))
