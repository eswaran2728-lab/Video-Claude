# Music bed: first 30 s only (the generated tail turns loud and clips), normalise, loop with a 3 s crossfade to cover the cut, duck under the dialogue (envelope from the
# dialogue's own level, so pauses breathe a little), lift for the end card, fade out.
import subprocess, numpy as np, soundfile as sf
exec(open("edl.py").read())
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "bgm/bed_raw.wav", "-t", "30", "-af", "loudnorm=I=-16:TP=-2:LRA=9", "-ar", "48000", "-ac", "2", "bgm/bed_norm.wav"], check=True)
a, sr = sf.read("bgm/bed_norm.wav"); n = int(TOTAL * sr); xf = int(3.0 * sr)
while len(a) < n:                                       # loop: crossfade the tail into a later bar of the start
    b = a[int(2.0 * sr):int(2.0 * sr) + len(a)]; r = np.linspace(0, 1, xf)[:, None]
    a = np.concatenate([a[:-xf], a[-xf:] * (1 - r) + b[:xf] * r, b[xf:]])
a = a[:n]
d, _ = sf.read("edit/assets/dialogue.wav"); d = d.mean(1) if d.ndim > 1 else d
w = int(0.05 * sr); rms = np.sqrt(np.convolve(d ** 2, np.ones(w) / w, mode="same")); rms = np.pad(rms, (0, max(0, n - len(rms))))[:n]
talk = np.clip((20 * np.log10(rms + 1e-9) + 45) / 15, 0, 1)                  # 0 = silence, 1 = speech
k = int(0.35 * sr); talk = np.convolve(talk, np.ones(k) / k, mode="same")
env = 0.22 - 0.1 * talk                                  # about -13 dB in pauses, -19 dB under speech
t = np.arange(n) / sr
lift = np.clip((t - SPEECH_END) / 0.4, 0, 1); env = env + (0.7 - env) * lift
env *= np.clip((TOTAL - t) / 0.8, 0, 1) * np.clip(t / 0.15, 0, 1)
sf.write("edit/assets/music_bed.wav", (a * env[:, None]).astype(np.float32), sr, subtype="PCM_16"); print("music bed", TOTAL)
