# TEMPORARY music bed for timing (the reference video's own audio; replace when the creator supplies a track).
# Reference music ~105.5 BPM, bar = 2.276 s, downbeats at ref 2.32 / 4.60 / 6.87 / 9.15 / 11.42 s.
#  out 0.00-10.10 = ref 1.32-11.42  (ref downbeat 2.32 lands on intro 1 at out 1.00)
#  out 10.10-15.0 = ref 6.87-11.77  (jump back two bars, downbeat to downbeat, 40 ms crossfade)
#  fade out 14.35-15.0 so the ending is not abrupt. Exactly 15.000 s, 48 kHz stereo -> edit/assets/music.wav
import subprocess, numpy as np, soundfile as sf
SR, TOTAL = 48000, 15.0
a = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", "src/reference.mov", "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
S = lambda t: int(round(t * SR))
OFF, JUMP_SRC, JUMP_DST, XF = 1.32, 11.42, 6.87, 0.04
p1 = a[S(OFF):S(JUMP_SRC) + S(XF)]
p2 = a[S(JUMP_DST):S(JUMP_DST) + S(TOTAL - (JUMP_SRC - OFF))]
x = S(XF); r = np.linspace(0, 1, x)[:, None]
out = np.concatenate([p1[:-x], p1[-x:] * (1 - r) + p2[:x] * r, p2[x:]])[:S(TOTAL)]
t = np.arange(len(out)) / SR
out *= (np.clip(t / 0.03, 0, 1) * np.clip((TOTAL - t) / 0.65, 0, 1))[:, None]
sf.write("edit/assets/music.wav", out.astype(np.float32), SR, subtype="PCM_16")
print("music", len(out) / SR, "s, peak", round(float(np.abs(out).max()), 3))
