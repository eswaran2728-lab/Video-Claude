# Dialogue track on the output timeline: source audio (mono AAC 44.1 kHz) -> 48 kHz, the EDL pieces joined with 12 ms
# fades at the cut, then a light clean-up (80 Hz high-pass, mild FFT denoise, gentle 3:1 compression, de-harsh shelf).
# Then +9 dB, a second faster compressor and a -3 dBFS limiter so peaks sit about 13 dB over the speech level (lets the
# final loudnorm run linear). Level is finished by the 2-pass loudnorm in the master scripts. -> edit/assets/dialogue.wav (mono 48 kHz, TOTAL long)
import subprocess, numpy as np, soundfile as sf, plan
raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "src/source.mp4", "-vn", "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.float32).astype(np.float64); SR = 48000; F = int(0.012 * SR)
out = np.zeros(round(plan.TOTAL * SR))
for o0, o1, s0, s1 in plan.SEG_OUT:
    x = a[round(s0 * SR):round(s1 * SR)].copy(); x[:F] *= np.linspace(0, 1, F); x[-F:] *= np.linspace(1, 0, F)
    i = round(o0 * SR); out[i:i + len(x)] += x[:len(out) - i]
sf.write("src/dialogue_raw.wav", out, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "src/dialogue_raw.wav", "-af",
                "highpass=f=80,afftdn=nr=8:nf=-42:tn=1,acompressor=threshold=-24dB:ratio=3:attack=8:release=120:makeup=2,"
                "highshelf=f=7000:g=-2,volume=9dB,acompressor=threshold=-16dB:ratio=4:attack=3:release=90:makeup=1,"
                "alimiter=limit=0.708:attack=4:release=60:level=false", "-ar", "48000", "-c:a", "pcm_s24le", "edit/assets/dialogue.wav"], check=True)
print("dialogue", plan.TOTAL)
