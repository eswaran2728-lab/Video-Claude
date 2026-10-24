import json,os
GRADE=open("grade_attr.txt").read()
INTRO=6.5;TOTAL=48.5;XF=0.6
SEQ=[("6343",5.0),("6312",3.6),("6317",3.6),("6319",3.0),("6322",3.0),("6326",3.0),("6327",3.0),("6330",3.4),("6335",3.0),("6333",3.0),("6334",3.0),("6340",5.4)]
LAND={"6312","6317","6340"}
# snap boundaries to musical beats (every 4th beat preferred) when a beat grid exists
bounds=[INTRO];t=INTRO
for _,d in SEQ: t+=d;bounds.append(round(t,3))
bf="edit/beats/assets/music_TEMP.wav.json"
if os.path.exists(bf):
    B=[x["time"] for x in json.load(open(bf))["beats"]]
    for i in range(1,len(bounds)-1):
        bounds[i]=round(min(B,key=lambda b:abs(b-bounds[i])),3)
bounds[-1]=TOTAL
slides=[];js=[]
for i,(s,_) in enumerate(SEQ):
    t0,t1=bounds[i],bounds[i+1];dur=(t1-t0)+(XF if i<len(SEQ)-1 else 0)
    if s in LAND:
        inner=f'<img class="bgimg" src="assets/photos/{s}_bg.jpg" alt="" /><div class="pz"><div class="frame"><img {GRADE} id="im{s}" src="assets/photos/{s}.jpg" alt="" /></div></div>'
    else:
        inner=f'<div class="pz"><img {GRADE} id="im{s}" class="full" src="assets/photos/{s}.jpg" alt="" /></div>'
    slides.append(f'      <div id="s{i}" class="clip slide" data-start="{t0:.3f}" data-duration="{dur:.3f}" data-track-index="{1+i%2}" style="z-index:{2+i}">{inner}</div>')
    js.append(f'tl.fromTo("#s{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: {XF}, ease: "sine.inOut", immediateRender: false }}, {t0:.3f});')
    zin=i%2==0;d=dur
    a,b=(1.0,1.06) if zin else (1.06,1.0);dx=(-14 if i%3==0 else 14)
    js.append(f'tl.fromTo("#s{i} .pz", {{ scale: {a}, x: 0 }}, {{ scale: {b}, x: {dx}, duration: {d:.3f}, ease: "none", immediateRender: "false" }}, {t0:.3f});')
# titles
def words(cls,txt): return f'<div class="{cls}">'+"".join(f"<span>{w}</span>" for w in txt.split())+"</div>"
T=[("t_open",INTRO+0.35,bounds[1]-0.25,[("l1","Persatuan Silambam Daerah Sepang"),("l2","A Special Gathering with Karate R. Tiagarajan")]),
   ("t_mid",bounds[1]+0.5,bounds[3]-bounds[1]-0.8,[("l2","Sharing a Meal. Strengthening Bonds.")]),
   ("t_close",bounds[11]+0.6,TOTAL-bounds[11]-0.6,[("l3","Respect • Friendship • Unity"),("l1","Persatuan Silambam Daerah Sepang")])]
tit=[]
for n,st,du,lines in T:
    if n=="t_open": du=bounds[1]-0.25-st
    cls="clip ttl top" if n=="t_open" else "clip ttl"
    tit.append(f'      <div id="{n}" class="{cls}" data-start="{st:.3f}" data-duration="{du:.3f}" data-track-index="7">'+"".join(words(c,t) for c,t in lines)+'<div class="rule"></div></div>')
    js.append(f'tl.fromTo("#{n} span", {{ opacity: 0, y: 22, filter: "blur(5px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.45, stagger: 0.07, ease: "power3.out", immediateRender: false }}, {st+0.05:.3f});')
    js.append(f'tl.fromTo("#{n} .rule", {{ width: 0 }}, {{ width: 420, duration: 0.8, ease: "power2.out", immediateRender: false }}, {st+0.4:.3f});')
    if n!="t_close": js.append(f'tl.to("#{n}", {{ opacity: 0, duration: 0.35, ease: "sine.in" }}, {st+du-0.4:.3f});')
# two soft light leaks: lunch -> presentation, and into the closing group photo
leaks=[];sfx=[]
for k,tb in enumerate((bounds[3],bounds[11])):
    st=tb-0.9;leaks.append(f'      <div id="lk{k}" class="clip leak" data-start="{st:.3f}" data-duration="1.8" data-track-index="5"><i class="a"></i><i class="g"></i></div>')
    js.append(f'tl.fromTo("#lk{k}", {{ opacity: 0 }}, {{ opacity: 0.55, duration: 0.7, ease: "sine.out", immediateRender: false }}, {st:.3f});')
    js.append(f'tl.to("#lk{k}", {{ opacity: 0, duration: 0.8, ease: "sine.in" }}, {st+0.95:.3f});')
    js.append(f'tl.fromTo("#lk{k} .a", {{ xPercent: -18 }}, {{ xPercent: 16, duration: 1.8, ease: "sine.inOut", immediateRender: false }}, {st:.3f});')
    js.append(f'tl.fromTo("#lk{k} .g", {{ xPercent: -26 }}, {{ xPercent: 22, duration: 1.8, ease: "sine.inOut", immediateRender: false }}, {st:.3f});')
    sfx.append(f'      <audio id="sx{k}" class="clip" src="assets/sfx/whoosh-short.mp3" data-start="{st+0.2:.3f}" data-duration="1.2" data-volume="0.22"></audio>')
sfx.append(f'      <audio id="sx2" class="clip" src="assets/sfx/sparkle.mp3" data-start="{bounds[11]+0.6:.3f}" data-duration="1.5" data-volume="0.25"></audio>')
DECOS=bounds[11]+0.3
intro=(f'      <video id="intro" class="clip" src="assets/intro.mp4" muted playsinline data-start="0" data-duration="{INTRO+XF:.3f}" data-track-index="0" style="z-index:1"></video>\n'
       f'      <div id="topscrim" class="clip" data-start="{INTRO:.3f}" data-duration="{TOTAL-INTRO:.3f}" data-track-index="4"></div>\n'
       f'      <div id="botscrim" class="clip" data-start="{INTRO:.3f}" data-duration="{TOTAL-INTRO:.3f}" data-track-index="4"></div>')
js.append(f'tl.fromTo(["#topscrim","#botscrim"], {{ opacity: 0 }}, {{ opacity: 1, duration: {XF}, ease: "sine.inOut", immediateRender: false }}, {INTRO:.3f});')
sfx.append('      <audio id="sxi0" class="clip" src="assets/sfx/pop.mp3" data-start="0.30" data-duration="0.8" data-volume="0.35"></audio>')
sfx.append('      <audio id="sxi1" class="clip" src="assets/sfx/whoosh-short.mp3" data-start="0.90" data-duration="1.0" data-volume="0.3"></audio>')
tpl=open("index.tpl.html").read()
for k,v in dict(TOTAL=f"{TOTAL}",SLIDES=intro+"\n"+"\n".join(slides),TITLES="\n".join(tit),LEAKS="\n".join(leaks),SFX="\n".join(sfx),
                JS="      "+"\n      ".join(js),DECOS=f"{DECOS:.3f}",DECOD=f"{TOTAL-DECOS:.3f}").items(): tpl=tpl.replace("%%"+k+"%%",v)
open("edit/index.html","w").write(tpl)
json.dump({"bounds":bounds,"seq":[s for s,_ in SEQ]},open("storyboard.json","w"))
print("bounds",bounds)
