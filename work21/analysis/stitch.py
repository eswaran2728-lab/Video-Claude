import numpy as np, soundfile as sf
from scipy.signal import fftconvolve
SR=48000
L={c:sf.read(f'analysis/a48/{c}.wav')[0] for c in ('c02','c06','c09')}
def refine(a,b,guess):   # a time t <-> b time t-guess ; refine within +-0.1s
    m=lambda x:x.mean(1)
    best=None
    g=int(guess*SR); n=SR*8
    A=m(a)[g:g+n]
    for d in range(-4800,4801,1):
        pass
    B=m(b)[:n+9600]
    A2=m(a)[g-4800:g-4800+n+9600]
    c=fftconvolve(A2,B[4800:4800+n][::-1],mode='valid')
    i=np.argmax(c); return (g-4800+i)/SR, c[i]/ (np.linalg.norm(B[4800:4800+n])**2)
l1,q1=refine(L['c02'],L['c06'],10.46); l2,q2=refine(L['c06'],L['c09'],16.79)
print('lags',l1,q1,l2,q2)
# b[4800:] aligned with a[g-4800+i:] -> b time 0.1 <-> a time lag+0.1 ; so a t = b t + lag
x=int(0.05*SR)
def join(a,b,lag):
    k=int(lag*SR)+SR*2     # crossfade 2 s after overlap begins
    r=np.linspace(0,1,x)[:,None]
    bb=b[k-int(lag*SR):]
    out=np.concatenate([a[:k], a[k:k+x]*(1-r)+bb[:x]*r, bb[x:]])
    return out
ab=join(L['c02'],L['c06'],l1); abc=join(ab,L['c09'],l1+l2)
sf.write('analysis/track_A.wav',abc,SR); print('len',len(abc)/SR)
# onset envelope / tempo
m=abc.mean(1); hop=480; fr=np.array([np.sqrt((m[i:i+960]**2).mean()) for i in range(0,len(m)-960,hop)])
on=np.maximum(0,np.diff(np.log(fr+1e-4))); on=on-on.mean()
ac=np.correlate(on,on,'full')[len(on)-1:]
lags=np.arange(len(ac))*hop/SR
sel=(lags>0.3)&(lags<1.2); top=np.argsort(ac[sel])[-5:][::-1]
print('tempo cands (s, bpm, strength):',[(round(lags[sel][i],3),round(60/lags[sel][i],1),round(ac[sel][i]/ac[0],3)) for i in top])
sec=[round(float(20*np.log10(fr[i:i+100].mean()+1e-6)),1) for i in range(0,len(fr),100)]
print('dB per s:',sec)
np.save('analysis/onset.npy',on)
