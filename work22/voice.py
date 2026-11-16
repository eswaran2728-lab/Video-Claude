"""Owner's voice for the reel: detect speech in the source audio, keep it in order, shorten long silences,
clean it (high-pass, hum notch, noise reduction, gentle compression, loudness) and place it on the output clock.
Writes vNN/assets/audio/voice.wav and vNN/voice-map.json (source -> output times). usage: python3 voice.py v03"""
import json, os, sys, subprocess
import numpy as np, soundfile as sf
from scipy.signal import stft
ROOT = os.path.dirname(os.path.abspath(__file__)); V = sys.argv[1]
P = json.load(open(os.path.join(ROOT, V, 'edit-plan.json'))); VC = P['voice']
SR = 48000
tmp = os.path.join(ROOT, 'analysis', 'voice_clean.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(ROOT, VC['source']), '-vn', '-ac', '1', '-ar', str(SR), '-af',
                'highpass=f=85,bandreject=f=400:width_type=h:w=60,afftdn=nr=14:nf=-42,equalizer=f=3000:t=q:w=1.2:g=3,'
                'acompressor=threshold=-24dB:ratio=3:attack=8:release=120:makeup=4', tmp], check=True)
a, _ = sf.read(tmp)
f, t, Z = stft(a, SR, nperseg=2048, noverlap=1536); Pw = np.abs(Z) ** 2
db = 10 * np.log10(Pw[(f > 500) & (f < 2800)].sum(0) + 1e-12)
k = max(1, int(0.15 / (t[1] - t[0]))); sm = np.convolve(db, np.ones(k) / k, 'same')
on = sm > np.percentile(sm, 20) + 12
segs, s = [], None
for i, v in enumerate(on):
    if v and s is None: s = t[i]
    if not v and s is not None: segs.append([s, t[i]]); s = None
lo, hi = VC['src_range']
segs = [[max(lo, x[0] - VC['pad']), min(hi, x[1] + VC['pad'])] for x in segs if x[1] > lo and x[0] < hi and x[1] - x[0] > 0.1]
merged = []
for x in segs:
    if merged and x[0] <= merged[-1][1] + 0.05: merged[-1][1] = max(merged[-1][1], x[1])
    else: merged.append(x)
out, cur, vmap = [], VC['start_at'], []
fade = int(0.02 * SR)
for i, (s0, s1) in enumerate(merged):
    if i:
        gap = s0 - merged[i - 1][1]
        cur += min(gap, VC['max_gap'])
    seg = a[int(s0 * SR):int(s1 * SR)].copy()
    seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    out.append((cur, seg)); vmap.append({'src': [round(s0, 3), round(s1, 3)], 'at': round(cur, 3), 'dur': round(s1 - s0, 3)})
    cur += s1 - s0
T = sum(s['dur'] for s in P['shots'])
buf = np.zeros(int(T * SR) + SR)
for st, seg in out: buf[int(st * SR):int(st * SR) + len(seg)] += seg
buf = buf[:int(T * SR)]
raw = os.path.join(ROOT, V, 'assets', 'audio', 'voice_raw.wav'); sf.write(raw, buf, SR, subtype='PCM_24')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', raw, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=7', '-ar', str(SR), '-ac', '2',
                os.path.join(ROOT, V, 'assets', 'audio', 'voice.wav')], check=True)
json.dump({'segments': vmap, 'voice_end': round(cur, 3)}, open(os.path.join(ROOT, V, 'voice-map.json'), 'w'), indent=1)
print('voice segments', len(vmap), 'ends at', round(cur, 2), 's of', round(T, 2))
for m in vmap: print(m)
