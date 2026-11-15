import numpy as np, soundfile as sf, glob, os, itertools
from scipy.signal import fftconvolve
d={}
for p in sorted(glob.glob('analysis/wav/*.wav')):
    a,sr=sf.read(p); a=a-a.mean(); d[os.path.basename(p)[:-4]]=a/ (a.std()+1e-9)
for x,y in itertools.combinations(d,2):
    a,b=d[x],d[y]
    c=fftconvolve(a,b[::-1])
    # normalise by overlap length
    n=len(c); lags=np.arange(n)-(len(b)-1)
    ov=np.minimum(len(a),lags+len(b))-np.maximum(0,lags)
    ok=ov>8000*3
    cn=np.where(ok,c/np.maximum(ov,1),0)
    i=np.argmax(cn); med=np.median(np.abs(cn[ok])); 
    print(x,y,'lag %.2fs'%(lags[i]/8000),'peak %.3f'%cn[i],'ratio %.0f'%(cn[i]/(med+1e-9)),'overlap %.1fs'%(ov[i]/8000))
