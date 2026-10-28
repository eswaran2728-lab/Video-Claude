# Mix -> edit/assets/mix.wav (stereo 48 kHz): dialogue (about -16 LUFS from make_dialogue.py), music bed ducked under speech
# (Digital Clouds, Mixkit #175, Mixkit Stock Music Free License), SFX from edit/cues.json with each sound's transient
# (its peak sample) placed on the cue frame. Final loudness is set by master_preview.sh / master_final.sh.
import json, subprocess, numpy as np, soundfile as sf, plan
SR = 48000; N = round(plan.TOTAL * SR)
def load(p, ss=0.0):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(ss), "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
db = lambda g: 10 ** (g / 20)
voice = load("edit/assets/dialogue.wav")[:N]; voice = np.pad(voice, ((0, N - len(voice)), (0, 0))) * db(0.0)
# speech envelope -> duck curve (bed -22 dB under speech, -15 dB in gaps >= 0.3 s and in the end hold)
h = SR // 50; e = np.sqrt(np.convolve(voice[:, 0] ** 2, np.ones(h) / h, "same"))
active = 20 * np.log10(e + 1e-9) > -38
act_s = np.array([active[i:i + h].any() for i in range(0, N, h)])
k = int(0.3 * 50); hold = np.convolve(act_s.astype(float), np.ones(2 * k + 1), "same") > 0
gain_db = np.where(hold, -22.0, -15.0); gain_db[int(plan.SPEECH_OUT_END * 50) + 4:] = -13.0
g = np.repeat(gain_db, h)[:N]; g = np.convolve(g, np.ones(int(0.15 * SR)) / int(0.15 * SR), "same")
g[:int(0.075 * SR)] = gain_db[0]
music = load("music/mixkit_175_digital_clouds.mp3")[:N] * db(g)[:, None]
fade = int(0.6 * SR); music[-fade:] *= np.linspace(1, 0, fade)[:, None]
sfx = np.zeros((N, 2))
for c in json.load(open("edit/cues.json"))["cues"]:
    a, sr = sf.read(f"edit/assets/sfx/{c['sfx']}.wav", always_2d=True)
    a = a if a.shape[1] == 2 else np.repeat(a, 2, 1)
    if sr != SR: raise SystemExit("sfx sample rate")
    pk = int(np.argmax(np.abs(a).sum(1))); i0 = int(round(c["t"] * SR)) - pk
    if c["sfx"] == "zoom-swish": i0 = int(round(13.05 * SR)) - pk          # its peak lands where the punch-in settles
    a = a[max(0, -i0):] * db(c["gain_db"]); i0 = max(0, i0); n = min(len(a), N - i0)
    sfx[i0:i0 + n] += a[:n]
mix = voice + music + sfx
pk = np.abs(mix).max(); print("peak dBFS", round(20 * np.log10(pk), 2))
if pk > 0.95: mix *= 0.95 / pk
sf.write("src/mix_prelimit.wav", mix, SR, subtype="FLOAT")
# a few consonant peaks (the first "call", 0.05 s) sit 16 dB over the speech level: a -9 dBFS bus limiter keeps the mix
# crest near 12 dB so the 2-pass loudnorm stays linear (no pumping)
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "src/mix_prelimit.wav", "-af",
                "alimiter=limit=0.355:attack=3:release=60:level=false", "-ar", str(SR), "-c:a", "pcm_s24le", "edit/assets/mix.wav"], check=True)
sf.write("edit/assets/stem_music.wav", music, SR, subtype="PCM_16"); sf.write("edit/assets/stem_sfx.wav", sfx, SR, subtype="PCM_16")
