import json,numpy as np
M=json.load(open("motion.json"));B=json.load(open("beats_ext.json"))["beats"]
B=np.array(B);ib=0.4762
VIDS={"v185":(0.5,37.0),"v186":(0.5,42.5),"v201":(0.3,24.5),"v203":(0.8,25.5)}
# slot plan in beats per phrase (16 beats each) -> list of (start_beat, n_beats)
plan=[4,4,4,4]+[2]*8+[4,4,4,4]+[2]*8+[4,4,4,4]+[2]*8+[4,4,4,4]
slots=[];bi=0
for n in plan:
    if bi>=len(B): break
    slots.append((bi,n));bi+=n
slots=[(s,n) for s,n in slots if s+n<=len(B)]
END=54.72
def mot(v,a,b):
    t=np.array(M[v]["t"]);m=np.array(M[v]["m"]);sel=(t>=a)&(t<b)
    return float(m[sel].mean()) if sel.any() else 0
used={v:[] for v in VIDS};edl=[];order=["v201","v186","v185","v203"];k=0
for si,(s,n) in enumerate(slots):
    t0=float(B[s]);t1=float(B[s+n]) if s+n<len(B) else END
    d=t1-t0;best=None
    for vi in range(4):
        v=order[(k+vi)%4];lo,hi=VIDS[v]
        for st in np.arange(lo,hi,0.1):
            m=mot(v,st,st+d*1.3)
            sp=float(np.clip(4.6/max(m,0.1),1.0,2.0))
            ln=d*sp
            if st+ln>hi: continue
            ov=sum(max(0,min(st+ln,b)-max(st,a)) for a,b in used[v])
            score=mot(v,st,st+ln)*(1.15 if vi==0 else 1.0)-ov*6
            if best is None or score>best[0]: best=(score,v,round(float(st),2),round(sp,2),ln)
        if best and vi==0 and best[0]>3.2: break
    sc,v,st,sp,ln=best;used[v].append((st,st+ln));k+=1
    edl.append({"slot":si,"t0":round(t0,3),"t1":round(t1,3),"src":v,"ss":st,"speed":sp,"src_len":round(ln,3),"motion":round(sc,2)})
json.dump(edl,open("edl.json","w"),indent=0)
for e in edl: print(e)
print(len(edl),"clips; per video",{v:sum(1 for e in edl if e['src']==v) for v in VIDS})
