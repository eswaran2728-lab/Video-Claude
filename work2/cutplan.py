import re,subprocess,json
out=subprocess.run(["ffmpeg","-hide_banner","-i","audio.wav","-af","silencedetect=n=-38dB:d=0.4","-f","null","-"],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",out)];en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",out)]
sil=[(a,b) for a,b in zip(st,en) if b-a>=0.5]
def keep(lo,hi):
    segs=[];cur=lo
    for a,b in sil:
        if b<=lo or a>=hi: continue
        if a-cur>0.05: segs.append((cur,min(a+0.12,hi)))
        cur=max(b-0.12,lo)
    if hi-cur>0.2: segs.append((cur,hi))
    return segs
plan=[(52.1,56.07)]+keep(0.0,47.9)+keep(56.07,98.3)
plan=[(round(a,2),round(b,2)) for a,b in plan if b-a>0.25]
t=0;edl=[]
for a,b in plan: edl.append([a,b,round(t,3)]); t+=b-a
json.dump(edl,open("edl.json","w"));print(len(plan),"segs, total",round(t,2))
