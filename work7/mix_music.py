# Music bed: normalise, then duck under the dialogue and lift for the end card.
import subprocess, numpy as np, soundfile as sf
exec(open("edl.py").read())
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "bgm/bed_raw.wav", "-af", "loudnorm=I=-16:TP=-2:LRA=9", "-ar", "48000", "-ac", "2", "bgm/bed_norm.wav"], check=True)
a, sr = sf.read("bgm/bed_norm.wav")
n = int(TOTAL * sr); a = a[:n] if len(a) >= n else np.pad(a, ((0, n - len(a)), (0, 0)))
t = np.arange(n) / sr
env = np.full(n, 0.2)                                   # ~-14 dB under speech
env[t < 0.08] = 0.6                                     # opening hit before the first word
lift = np.clip((t - SPEECH_END) / 0.45, 0, 1)           # music takes over for the end card
env = env + (0.75 - env) * lift
env *= np.clip((TOTAL - t) / 0.7, 0, 1)                 # fade out
k = int(0.05 * sr); env = np.convolve(env, np.ones(k) / k, mode="same")
sf.write("edit/assets/music_bed.wav", (a * env[:, None]).astype(np.float32), sr, subtype="PCM_16")
print("music bed", TOTAL)
