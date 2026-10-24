import json,numpy as np
M=json.load(open("motion.json"));B=np.array(json.load(open("beats_ext.json"))["beats"])
OK={"v185":[(1.5,19.4),(20.8,37.0)],"v186":[(6.0,31.5),(36.0,43.0)],"v201":[(0.3,1.8),(11.5,24.5)],"v203":[(0.5,24.8)]}
END=54.72
def mot(v,a,b):
    t=np.array(M[v]["t"]);m=np.array(M[v]["m"]);s=(t>=a)&(t<b);return float(m[s].mean()) if s.any() else 0
def inside(v,a,b): return any(lo<=a and b<=hi for lo,hi in OK[v])
slots=[(i,4) for i in range(0,len(B)-4,4)]
used={v:[] for v in OK};edl=[];order=["v201","v186","v185","v203"]
for k,(s,n) in enumerate(slots):
    t0=float(B[s]);t1=float(B[s+n]) if s+n<len(B) else END
    if k==len(slots)-1: t1=END
    d=t1-t0;best=None
    for vi in range(4):
        v=order[(k+vi)%4]
        for lo,hi in OK[v]:
            for st in np.arange(lo,hi,0.1):
                m=mot(v,st,st+d)
                sp=1.0 if m>=3.0 else (1.15 if m>=2.6 else 1.25)
                ln=d*sp
                if not inside(v,st,st+ln): continue
                ov=sum(max(0,min(st+ln,b)-max(st,a)) for a,b in used[v])
                sc=mot(v,st,st+ln)*(1.2 if vi==0 else 1.0)-ov*8-(sp-1)*4
                if best is None or sc>best[0]: best=(sc,v,round(float(st),2),sp,ln)
        if best and vi==0 and best[0]>3.4: break
    sc,v,st,sp,ln=best;used[v].append((st,st+ln))
    edl.append({"slot":k,"t0":round(t0,3),"t1":round(t1,3),"src":v,"ss":st,"speed":sp,"src_len":round(ln,3),"motion":round(float(sc),2)})
json.dump(edl,open("edl.json","w"),indent=0)
for e in edl: print(e["slot"],e["t0"],e["t1"],e["src"],e["ss"],"x",e["speed"])
print(len(edl),"clips; speeds",{s:sum(1 for e in edl if e['speed']==s) for s in (1.0,1.15,1.25)},"per video",{v:sum(1 for e in edl if e['src']==v) for v in OK})
