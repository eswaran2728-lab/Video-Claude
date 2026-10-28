# Dialogue track on the output timeline: source audio (mono AAC 44.1 kHz) -> 48 kHz, the EDL pieces joined with 12 ms
# fades at the cut, then a light clean-up (80 Hz high-pass, mild FFT denoise, gentle 3:1 compression, de-harsh shelf).
# Then +9 dB, a second faster compressor and a -3 dBFS limiter so peaks sit about 13 dB over the speech level (lets the
# final loudnorm run linear). Level is finished by the 2-pass loudnorm in the master scripts. -> edit/assets/dialogue.wav (mono 48 kHz, TOTAL long)
# v02 (VERSION=v02): the joined track is first voice-isolated with DeepFilterNet3 (tools/voice_isolate.py ->
# src/voice_df_full.wav, full strength); the FFT denoise is then dropped from the chain. -> edit/assets/dialogue_v02.wav
import os, subprocess, numpy as np, soundfile as sf, plan
VERSION = os.environ.get("VERSION", "v01"); SUF = "" if VERSION == "v01" else "_" + VERSION
raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "src/source.mp4", "-vn", "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.float32).astype(np.float64); SR = 48000; F = int(0.012 * SR)
out = np.zeros(round(plan.TOTAL * SR))
for o0, o1, s0, s1 in plan.SEG_OUT:
    x = a[round(s0 * SR):round(s1 * SR)].copy(); x[:F] *= np.linspace(0, 1, F); x[-F:] *= np.linspace(1, 0, F)
    i = round(o0 * SR); out[i:i + len(x)] += x[:len(out) - i]
sf.write("src/dialogue_raw.wav", out, SR, subtype="FLOAT")
SRC = "src/dialogue_raw.wav" if VERSION == "v01" else "src/voice_df_full.wav"
DEN = "afftdn=nr=8:nf=-42:tn=1," if VERSION == "v01" else ""
if VERSION != "v01" and not os.path.exists(SRC): raise SystemExit("run tools/voice_isolate.py on src/dialogue_raw.wav first")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", SRC, "-af",
                "highpass=f=80," + DEN + "acompressor=threshold=-24dB:ratio=3:attack=8:release=120:makeup=2,"
                "highshelf=f=7000:g=-2,volume=9dB,acompressor=threshold=-16dB:ratio=4:attack=3:release=90:makeup=1,"
                "alimiter=limit=0.708:attack=4:release=60:level=false", "-ar", "48000", "-c:a", "pcm_s24le", f"edit/assets/dialogue{SUF}.wav"], check=True)
print("dialogue", plan.TOTAL)
