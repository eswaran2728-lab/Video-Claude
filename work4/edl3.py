import json,numpy as np
M=json.load(open("motion.json"));B=np.array(json.load(open("beats_ext.json"))["beats"])
END=54.72
OK={"v185":[(1.5,19.4),(20.8,37.0)],"v186":[(6.0,31.5),(36.0,43.0)],"v201":[(0.3,1.8),(11.5,24.5)],
    "v203":[(0.5,24.8)],"v205":[(0.5,55.5)],"v193":[(0.5,12.5)]}
BAN={"v185":[(28.5,31.5)],"v186":[(18.0,20.8)]}   # clips the user called slow
PH1=["p152","p153","p156","p158","p160","p162","p164","p165"]
PH2=["p166","p167","p168","p169","p170","p171","p173","p180"]
PHOTO_PHRASES={2:PH1,5:PH2}
def mot(v,a,b):
    t=np.array(M[v]["t"]);m=np.array(M[v]["m"]);s=(t>=a)&(t<b);return float(m[s].mean()) if s.any() else 0
used={v:[] for v in OK};edl=[];order=["v205","v186","v185","v203","v201","v193"];k=0
nb=len(B)
def tb(i): return END if i>=nb else float(B[i])
i=0
while i<nb-1:
    ph=i//16
    if ph in PHOTO_PHRASES and i%16==0:
        for j,p in enumerate(PHOTO_PHRASES[ph]):
            a,b=tb(i+2*j),tb(i+2*j+2)
            edl.append({"kind":"photo","src":p,"t0":round(a,3),"t1":round(b,3)})
        i+=16;continue
    n=4;t0,t1=tb(i),tb(i+n)
    if i+n>=nb-1: t1=END
    d=t1-t0;best=None
    for vi in range(len(order)):
        v=order[(k+vi)%len(order)]
        if edl and edl[-1].get("src")==v: continue
        for lo,hi in OK[v]:
            for st in np.arange(lo,hi-d,0.1):
                a,b=st,st+d
                if any(not(b<=x or a>=y) for x,y in BAN.get(v,[])+used[v]): continue
                m=mot(v,a,b)
                sp=1.0 if m>=3.0 else 1.15
                b=st+d*sp
                if b>hi or any(not(b<=x or a>=y) for x,y in BAN.get(v,[])+used[v]): continue
                sc=mot(v,a,b)-(sp-1)*4-(1.5 if v=="v193" else 0)+(0.3 if vi==0 else 0)+(1.5 if not used[v] else 0)
                if best is None or sc>best[0]: best=(sc,v,round(float(st),2),sp,d*sp)
    sc,v,st,sp,ln=best;used[v].append((st,st+ln));k+=1
    edl.append({"kind":"video","src":v,"ss":st,"speed":sp,"src_len":round(ln,3),"t0":round(t0,3),"t1":round(t1,3),"motion":round(float(sc),2)})
    i+=n
edl[0]["t0"]=0.0;edl[-1]["t1"]=END
json.dump(edl,open("edl3.json","w"),indent=0)
for e in edl: print(e["t0"],e["t1"],e["kind"],e["src"],e.get("ss",""),e.get("speed",""))
vids=[e for e in edl if e["kind"]=="video"]
print(len(vids),"videos,",len(edl)-len(vids),"photos; per video",{v:sum(1 for e in vids if e['src']==v) for v in OK})
# verify no overlap
for v in OK:
    r=sorted((e["ss"],e["ss"]+e["src_len"]) for e in vids if e["src"]==v)
    assert all(r[j][1]<=r[j+1][0]+1e-6 for j in range(len(r)-1)),v
print("no repeated footage: OK")
