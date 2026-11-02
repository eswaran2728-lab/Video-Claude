# Per-clip highlight scoring at 0.5 s resolution: motion energy (mean abs frame difference on a 160 px grey copy),
# audio loudness (RMS dB) and audio onsets (sudden jumps = impacts / cheers). -> scores.json and a printed top-3 per clip.
import json, glob, os, subprocess, numpy as np
res = {}
for f in sorted(glob.glob('src/norm/v_*.mp4')):
    n = os.path.basename(f)[:-4]
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f, "-vf", "scale=160:-2,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    w = 160; h = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", f],
                                     capture_output=True, text=True).stdout.strip().split(",")[1]) * 160 // int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip())
    h += h % 2
    fr = np.frombuffer(raw, np.uint8)
    nf = len(fr) // (w * h); fr = fr[:nf * w * h].reshape(nf, h, w).astype(np.int16)
    mot = np.r_[0, np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))]
    a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    bins = max(1, int(nf / 15))
    m_b = [float(mot[i * 15:(i + 1) * 15].mean()) for i in range(bins)]
    a_b = [float(20 * np.log10(np.sqrt(np.mean(a[i * 8000:(i + 1) * 8000] ** 2)) + 1e-9)) if len(a) > (i + 1) * 8000 else -90 for i in range(bins)]
    on = [0] + [max(0, a_b[i] - a_b[i - 1]) for i in range(1, bins)]
    mz = (np.array(m_b) - np.mean(m_b)) / (np.std(m_b) + 1e-6); az = (np.array(a_b) - np.mean(a_b)) / (np.std(a_b) + 1e-6)
    sc = mz + 0.6 * az + 0.4 * np.array(on) / 3
    top = sorted(range(bins), key=lambda i: -sc[i])[:3]
    res[n] = {"dur": round(nf / 30, 2), "motion": [round(x, 2) for x in m_b], "loud": [round(x, 1) for x in a_b], "score": [round(float(x), 2) for x in sc],
              "top": [round(i * 0.5, 1) for i in sorted(top)]}
    print(f"{n} dur {nf/30:5.1f}s  motion avg {np.mean(m_b):5.1f}  loud avg {np.mean(a_b):5.1f}  peaks at {res[n]['top']}", flush=True)
json.dump(res, open("scores.json", "w"))
