import subprocess, numpy as np, sys, json, glob, os
out={}
for p in sorted(glob.glob('source/*.mp4')):
    W,H,F=160,90,8
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-vf',f'fps={F},scale={W}:{H},format=gray','-f','rawvideo','-'],capture_output=True).stdout
    fr=np.frombuffer(raw,np.uint8).reshape(-1,H,W).astype(np.float32)
    st=fr[:, :int(H*0.6)]            # stage area
    d=np.abs(np.diff(st,axis=0))
    glob_m=np.median(d,axis=(1,2))    # camera shake proxy
    loc=(d>25).mean(axis=(1,2))       # fraction of strongly changed pixels
    # per second
    n=len(loc)//F
    sec=loc[:n*F].reshape(n,F).mean(1); sh=glob_m[:n*F].reshape(n,F).mean(1)
    b=os.path.basename(p)[:-4]; out[b]={'act':[round(float(x)*100,1) for x in sec],'shake':[round(float(x),1) for x in sh]}
    print(b,'act',' '.join('%2d'%round(x*100) for x in sec)); print('   shk',' '.join('%2d'%round(x) for x in sh))
json.dump(out,open('analysis/motion.json','w'))
