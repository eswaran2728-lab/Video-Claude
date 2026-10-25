# Spectral noise reduction for the two speech clips (workshop fan/printer hum, room tone).
# Noise profile = the quietest 15% of STFT frames of the whole clip; Wiener-style gain with over-subtraction,
# a gain floor (no "underwater" artefacts) and time/frequency smoothing (no musical noise); extra attenuation in
# the pauses between phrases. Writes edit/assets/clean_<clip>.wav (48 kHz mono), used by make_assets.py.
import subprocess, numpy as np, soundfile as sf, sys
from scipy.signal import stft, istft
from scipy.ndimage import uniform_filter
SR = 48000
def load(clip):
    a = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f"proxy/{clip}.mp4", "-vn", "-af", "highpass=f=80", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True).stdout
    return np.frombuffer(a, np.float32).copy()

def denoise(x, over=2.2, floor=0.06):
    f, t, Z = stft(x, SR, nperseg=2048, noverlap=1536)
    mag = np.abs(Z); en = mag.sum(0)
    quiet = en <= np.percentile(en, 15)
    N = mag[:, quiet].mean(1, keepdims=True) + 1e-9
    snr = np.maximum(mag ** 2 / (over * N) ** 2, 0)
    G = np.maximum(1 - 1 / np.maximum(snr, 1e-9) ** 0.5, 0)
    G = uniform_filter(G, size=(5, 5))                      # smooth across bins and frames
    speech = uniform_filter((en > np.percentile(en, 15) * 2.2).astype(float), size=9) > 0.2
    G = np.maximum(G, floor) * np.where(speech, 1.0, 0.35)[None, :]   # pauses sit lower still
    _, y = istft(Z * G, SR, nperseg=2048, noverlap=1536)
    return y[:len(x)].astype(np.float32), 20 * np.log10(N.mean())

def floor_db(x, sel):
    w = 2048; e = np.array([np.sqrt((x[i:i + w] ** 2).mean()) for i in range(0, len(x) - w, w)])
    return 20 * np.log10(np.percentile(e, sel) + 1e-9)

for clip in sys.argv[1:] or ["b5ae", "e5dd", "d67f", "a336"]:
    x = load(clip)
    y, n = denoise(x)
    sf.write(f"edit/assets/clean_{clip}.wav", y, SR, subtype="FLOAT")
    print(f"{clip}: noise floor {floor_db(x, 10):.1f} dB -> {floor_db(y, 10):.1f} dB, speech {floor_db(x, 90):.1f} -> {floor_db(y, 90):.1f} dB")
