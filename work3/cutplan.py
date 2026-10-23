import json
sil=[(1.85,3.45),(6.10,6.65),(9.05,9.60),(10.10,10.65),(11.70,13.70),(17.10,17.65),(20.45,20.90),(26.70,27.30),(41.35,42.00),(42.45,42.95),(44.85,45.35),(66.85,67.45),(72.35,73.25)]
remove=[(31.10,37.45),(53.95,55.50)]
cuts=sorted([(a+0.08,b-0.08) for a,b in sil]+remove)
keep=[];cur=1.05;END=75.75
for a,b in cuts:
    if a>cur: keep.append((cur,a))
    cur=max(cur,b)
keep.append((cur,END))
F=30;edl=[];o=0
for a,b in keep:
    fa,fb=round(a*F),round(b*F)
    if fb-fa<6: continue
    edl.append([fa,fb,o]);o+=fb-fa
json.dump(edl,open("edl.json","w"))
print(len(edl),"segments; body",o,"frames =",round(o/F,2),"s")
for fa,fb,oo in edl: print(f"src {fa/F:6.2f}-{fb/F:6.2f}  -> out {oo/F:6.2f}")
