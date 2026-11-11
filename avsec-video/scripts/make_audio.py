"""Generate per-slide voiceover (one TTS call per sentence) + caption timeline."""
import asyncio, json, re, subprocess, wave, sys
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent.parent
VOICE = "en-GB-SoniaNeural"
RATE = "-4%"
PROXY = "http://127.0.0.1:44637"   # sandbox egress proxy; harmless to drop locally
GAP, LEAD, TAIL = 0.28, 0.7, 1.0
TMP = ROOT / "data" / "tts_tmp"; TMP.mkdir(exist_ok=True)

SPOKEN = [  # caption text -> better spoken text
    (r"AA/SEC/F/042", "A A, S E C, F, zero four two"),
    (r"eForm", "e-Form"), (r"\bETD\b", "E T D"), (r"AVSEC", "A V sec"),
    (r"\bAM\b", "A M"), (r"\bPM\b", "P M"), (r"TEST-AK01", "TEST, A K, zero one"),
    (r"TEST-HL01", "TEST, H L, zero one"), (r"TEST-0001", "TEST, zero zero zero one"),
    (r"TEST001", "TEST, zero zero one"), (r"TEST002", "TEST, zero zero two"),
    (r"KUL-TEST", "K U L, TEST"), (r"\bID\b", "I D"), (r"\bQR\b", "Q R"),
    (r"Hi-lift", "High-lift"), (r"hi-lift", "high-lift"), (r"Hi-Lift", "High-Lift"),
    (r"Staff No\.", "Staff Number"), (r"–", ","),
]
def spoken(t):
    for a, b in SPOKEN: t = re.sub(a, b, t)
    return t

def parse():
    slides, cur = [], None
    for line in (ROOT / "data" / "narration.txt").read_text().splitlines():
        if line.startswith("## "):
            n, title = line[3:].split("|", 1)
            cur = {"n": int(n), "title": title.strip(), "sentences": []}; slides.append(cur)
        elif line.strip(): cur["sentences"].append(line.strip())
    return slides

sem = asyncio.Semaphore(6)
async def tts(text, out):
    if out.exists() and out.stat().st_size > 1000: return
    async with sem:
        for attempt in range(5):
            try:
                await edge_tts.Communicate(spoken(text), VOICE, rate=RATE, proxy=PROXY).save(str(out)); return
            except Exception as e:
                print("retry", out.name, e, file=sys.stderr); await asyncio.sleep(2 * (attempt + 1))
        raise SystemExit(f"TTS failed {out}")

def to_wav(mp3, wav):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ar", "24000", "-ac", "1", "-sample_fmt", "s16", wav], check=True)

def silence(f, s): f.writeframes(b"\x00\x00" * int(24000 * s))

async def main():
    slides = parse()
    await asyncio.gather(*[tts(s, TMP / f"s{sl['n']:02d}_{i:02d}.mp3") for sl in slides for i, s in enumerate(sl["sentences"])])
    timeline = []
    for sl in slides:
        n = sl["n"]; wavp = TMP / f"s{n:02d}.wav"; t = LEAD; items = []
        with wave.open(str(wavp), "wb") as out:
            out.setnchannels(1); out.setsampwidth(2); out.setframerate(24000)
            silence(out, LEAD)
            for i, s in enumerate(sl["sentences"]):
                w = TMP / f"s{n:02d}_{i:02d}.wav"; to_wav(str(TMP / f"s{n:02d}_{i:02d}.mp3"), str(w))
                with wave.open(str(w)) as r: frames = r.readframes(r.getnframes()); dur = r.getnframes() / 24000
                out.writeframes(frames); items.append({"text": s, "start": round(t, 3), "end": round(t + dur, 3)})
                t += dur; gap = GAP if i < len(sl["sentences"]) - 1 else TAIL
                silence(out, gap); t += gap
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wavp), "-codec:a", "libmp3lame", "-b:a", "128k",
                        str(ROOT / "public" / "audio" / f"s{n:02d}.mp3")], check=True)
        timeline.append({"n": n, "title": sl["title"], "duration": round(t, 3), "sentences": items})
    (ROOT / "data" / "timeline.json").write_text(json.dumps(timeline, indent=1))
    print("total seconds:", round(sum(x["duration"] for x in timeline), 1))
asyncio.run(main())
