"""Split each clip's speech into phrase chunks at pauses (for reliable chunk-wise transcription)."""
import numpy as np, soundfile as sf, json, sys
from scipy.signal import stft
out = {}
for c in ('C005', 'C006', 'C007'):
    a, sr = sf.read(f'analysis/{c}_c.wav')
    f, t, Z = stft(a, sr, nperseg=1024, noverlap=768); P = np.abs(Z) ** 2
    db = 10 * np.log10(P[(f > 350) & (f < 3000)].sum(0) + 1e-12)
    k = max(1, int(0.12 / (t[1] - t[0]))); sm = np.convolve(db, np.ones(k) / k, 'same')
    on = sm > np.percentile(sm, 25) + 9
    segs, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = t[i]
        if not v and s is not None: segs.append([s, t[i]]); s = None
    if s is not None: segs.append([s, t[-1]])
    segs = [x for x in segs if x[1] - x[0] > 0.15]
    # phrases: merge gaps < 0.45 s
    ph = []
    for x in segs:
        if ph and x[0] - ph[-1][1] < 0.45: ph[-1][1] = x[1]
        else: ph.append(list(x))
    # chunks for ASR: group phrases up to ~7 s
    ch = []
    for x in ph:
        if ch and x[1] - ch[-1][0] < 7.0 and x[0] - ch[-1][1] < 1.2: ch[-1][1] = x[1]
        else: ch.append(list(x))
    out[c] = {'phrases': [[round(float(a_), 2), round(float(b_), 2)] for a_, b_ in ph], 'chunks': [[round(float(max(0, a_ - 0.2)), 2), round(float(b_ + 0.25), 2)] for a_, b_ in ch]}
    print(c, 'phrases', len(ph), 'chunks', out[c]['chunks'])
json.dump(out, open('analysis/speech_segments.json', 'w'), indent=1)
