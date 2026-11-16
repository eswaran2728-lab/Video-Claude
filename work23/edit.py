"""work23 edit: picks speech phrases from the plan, tightens pauses, writes the timing map, cuts graded 1080x1920
video proxies per segment and assembles one cleaned voice track. usage: python3 edit.py v01
Source times are in each clip's own seconds; output times start at 0 of the reel."""
import json, os, sys, subprocess
import numpy as np, soundfile as sf
ROOT = os.path.dirname(os.path.abspath(__file__)); V = sys.argv[1]
P = json.load(open(os.path.join(ROOT, V, 'edit-plan.json')))
PH = json.load(open(os.path.join(ROOT, 'analysis', 'speech_segments.json')))
SR = 48000; PAD0, PAD1, GAP = P['cut']['pad_in'], P['cut']['pad_out'], P['cut']['max_gap']

segs = []          # {clip, src:[a,b], at, dur, kind}
t = 0.0
for blk in P['blocks']:
    if blk['kind'] == 'broll':          # visual-only insert (no source audio)
        segs.append({'id': blk['id'], 'clip': blk['clip'], 'src': blk['src'], 'at': round(t, 3), 'dur': round(blk['src'][1] - blk['src'][0], 3), 'kind': 'broll', 'role': blk.get('role', '')})
        t += blk['src'][1] - blk['src'][0]; continue
    a, b = blk['src']
    phr = [p for p in PH[blk['clip']]['phrases'] if p[1] > a and p[0] < b and [round(p[0], 2), round(p[1], 2)] not in [[round(x, 2) for x in d] for d in blk.get('drop', [])]]
    # merge phrases into runs where the gap is already short; long gaps are cut down to GAP
    runs = []
    for p in phr:
        s0, s1 = max(a, p[0] - PAD0), min(b, p[1] + PAD1)
        if runs and s0 - runs[-1][1] <= GAP: runs[-1][1] = s1
        else: runs.append([s0, s1])
    for k, (s0, s1) in enumerate(runs):
        if k == 0 and blk.get('lead'): s0 = max(a, s0 - blk['lead'])
        if k == len(runs) - 1 and blk.get('tail'): s1 = min(b, s1 + blk['tail'])
        segs.append({'id': f"{blk['id']}_{k}", 'clip': blk['clip'], 'src': [round(s0, 3), round(s1, 3)], 'at': round(t, 3), 'dur': round(s1 - s0, 3), 'kind': 'talk', 'block': blk['id']})
        t += s1 - s0
TOTAL_CUT = round(t, 3)
json.dump({'segments': segs, 'cut_end': TOTAL_CUT}, open(os.path.join(ROOT, V, 'timing-map.json'), 'w'), indent=1)
print('segments', len(segs), 'cut length', TOTAL_CUT)

if '--map-only' in sys.argv: sys.exit()
vd = os.path.join(ROOT, V, 'assets', 'video'); os.makedirs(vd, exist_ok=True)
lut = os.path.join(ROOT, V, 'grade.cube')
for s in segs:
    out = os.path.join(vd, s['id'] + '.mp4')
    if os.path.exists(out) and '--force' not in sys.argv: continue
    a, b = s['src']
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-v', 'error', '-ss', str(a), '-t', str(b - a + 0.1), '-i', os.path.join(ROOT, 'source', s['clip'] + '.mov'), '-an',
                    '-vf', f'scale=1080:1920:flags=lanczos,fps=30,lut3d={lut}', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-g', '15', '-pix_fmt', 'yuv420p', out], check=True)
# voice: clean each clip once, then lay segments on the output clock with 15 ms fades
ad = os.path.join(ROOT, V, 'assets', 'audio'); os.makedirs(ad, exist_ok=True)
clean = {}
for c in {s['clip'] for s in segs if s['kind'] == 'talk'}:
    p = os.path.join(ROOT, 'analysis', c + '_voice48.wav')
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-v', 'error', '-i', os.path.join(ROOT, 'source', c + '.mov'), '-vn', '-ac', '1', '-ar', str(SR), '-af',
                    'highpass=f=90,bandreject=f=100:width_type=h:w=8,bandreject=f=60:width_type=h:w=6,afftdn=nr=16:nf=-44,'
                    'equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3,acompressor=threshold=-26dB:ratio=3:attack=6:release=120:makeup=5', p], check=True)
    clean[c], _ = sf.read(p)
N = int((TOTAL_CUT + P['tail_card']) * SR) + SR
buf = np.zeros(N); fd = int(0.015 * SR)
for s in segs:
    if s['kind'] != 'talk': continue
    a, b = s['src']; x = clean[s['clip']][int(a * SR):int(b * SR)].copy()
    x[:fd] *= np.linspace(0, 1, fd); x[-fd:] *= np.linspace(1, 0, fd)
    i = int(s['at'] * SR); buf[i:i + len(x)] += x
raw = os.path.join(ad, 'voice_raw.wav'); sf.write(raw, buf, SR, subtype='PCM_24')
subprocess.run(['ffmpeg', '-nostdin', '-y', '-v', 'error', '-i', raw, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=7', '-ar', str(SR), '-ac', '2', os.path.join(ad, 'voice.wav')], check=True)
print('voice + proxies done')
