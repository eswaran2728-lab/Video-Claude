# QUALITY / CHEAP / FAST — explainer reel (Eshan Creations)

Vertical 1080x1920, 30 fps, 48.6 s. HyperFrames 0.8.193 project in `edit/` (built by `build.py`).
Preview only — the final high-quality export waits for the creator's approval. Nothing is published.

## Versions
- **v01** (`python3 build.py`, `PREVIEW_quality_cheap_fast_v01.mp4`): notebook photo -> traced -> clean diagram; b-roll from
  the earlier AVSEC shoot.
- **v02** (`VERSION=v02 python3 make_assets.py && python3 build_v02.py`, `PREVIEW_quality_cheap_fast_v02.mp4`), on the
  creator's notes "no need to add my drawing" and "don't use the previous video": no notebook photo and no footage from
  earlier shoots. The clean diagram builds itself in the hook (labels pop on "of these three", the three pair loops draw
  on "two"); "you're going to buy a product" (9.66–12.2) and "every product / spending money with me" (21.19–25.4) stay
  on him full frame with punch-ins. Everything else (cut, captions, pair highlights, sound) is unchanged. He offered
  product videos: those two beats are where they would go.
- **v03** (`VERSION=v03 python3 make_assets.py && python3 build_v03.py`, `PREVIEW_quality_cheap_fast_v03.mp4`), after he
  allowed b-roll from the public web: v02 plus licensed stock on the two beats v01 had b-roll on —
  9.66–12.2 "you're going to buy a product" and 23.1–25.4 "if you're spending money with me". He is back on camera for
  "use this for every product" (21.19–23.1).
- Each builder writes `edit/index.html` (the render entry). Run `make_assets.py` with the same `VERSION` first: the
  versions share clip names (`full1` differs in length between v02 and v01/v03).

## Stock footage (v03) — source and licence
Downloaded to `stock/` (not committed). Both items checked on their own Mixkit page on 2026-10-25: "Download this free
stock video clip for commercial or personal use, under the Mixkit Stock Video Free License." That licence allows social
media posts, online marketing ads and commercial projects; attribution not required (credit appreciated).
| id | title | page | used | treatment |
|---|---|---|---|---|
| sk1 | Checking an item on a sales site on a cell phone (#42123) | https://mixkit.co/free-stock-video/checking-an-item-on-a-sales-site-on-a-cell-phone-42123/ | src 2.5–5.2 → 9.66–12.2 | 1920x1080 → 608x1080 crop on the phone, scaled to 1080x1920, slow push |
| sk2 | Hands of two people sealing a package with tape (#42137) | https://mixkit.co/free-stock-video/hands-of-two-people-sealing-a-package-with-tape-42137/ | src 0.3–2.7 → 23.1–25.4 | vertical, slow pull-out |
Rejected: "Woman pays cashier with credit card in shop" (#15914, Mixkit Restricted License = personal use only, no
company social media); "Woman exploring an online sales page" (#42136, shows Amazon branding and dollar prices);
"Man counting a wad of bills" (#18296, US dollars). Pexels/Pixabay were not reachable from this environment.

## Rebuild
```
./make_proxies.sh            # stream the 4 Drive originals -> proxy/*.mp4 (1080x1920, 30 fps CFR)
python3 transcribe.py        # Whisper large-v3: auto (Tamil), English, Tamil->English  -> transcript.json
python3 denoise.py           # spectral noise reduction -> edit/assets/clean_*.wav
python3 geometry.py          # sketch traces + clean pair ellipses -> edit/geometry.json
python3 make_assets.py       # EDL -> video spans (edit/assets/v), dialogue.wav, edit/timing_map.json
python3 verify_cuts.py       # re-transcribe every cut piece (verify_cuts.json/.log)
python3 gen_bgm.py && python3 mix_music.py   # local MusicGen placeholder bed, ducked -> music_bed.wav
python3 build.py             # -> edit/index.html, edit/cues.json
cd edit && npx hyperframes@0.8.193 check && npx hyperframes@0.8.193 render --quality draft -o ../renders/draft_v01.mp4
```

## Asset inventory (Drive folder 1_GhbNTw56Y0ljytsH3Z7dQ7Hiv_QFTqP, no subfolders)
| proxy | Drive file | recorded (UTC) | length | content |
|---|---|---|---|---|
| d67f | d67fce98…1850.mp4 | 08:18:08 | 16.9 s | "Okay guys, here's a diagram…" + a garbled "business luxury / pricing" line |
| e5dd | e5dd03d4…cb2e.mp4 | 08:20:37 | 14.8 s | introduces Quality, Cheap, Fast ("a psychology"), "remember these three", "only two" |
| b5ae | b5aeb0ce…5740.mp4 | 08:22:19 | 59.9 s | main explanation: choose 2 of 3, pair examples, "with me", fun fact, opinion |
| a336 | a336a791…5b4e.mp4 | 08:24:42 | 18.4 s | outro: "my ideology", comment below, an unclear cheap+quality DM line, bye |

All four are 720x1280 HEVC talking-head takes at the same desk; no b-roll in this set (filenames are hashes, so the
order comes from creation time). Sketch: `src/IMG_6372.jpeg` (the attached photo; the top drawing is used, cropped
to `edit/assets/sketch_top.jpg`; the lower drawing is the same diagram drawn smaller and is not used).
B-roll: the creator's own footage from the AVSEC keychain shoot (`../work7`, relit there): `vc4/V7.mp4` (a packed
keychain) and `vc4/V1.mp4` (build plate of printed keychains slides out of the printer).

## What he actually says (Tamil, English keywords) — verified on the cut pieces
| out | source | Tamil (as heard by Whisper, checked across passes) | caption (English) |
|---|---|---|---|
| 0.00 | b5ae 4.82–7.72 | இந்த மூனில இரண்டுதான் நீங்க choose செய்ய முடியும் | Of these 3, you can only choose 2 |
| 2.90 | d67f 0.00–2.38 | Okay guys, மேல வந்து ஒரு diagram | Okay guys, here's a diagram |
| 5.28 | e5dd 0.00–4.38 | இதுதான் வந்து Quality, Cheap and then Fast, அப்படிங்கது ஒரு Psychology | This is QUALITY, CHEAP and FAST / It's a psychology |
| 9.66 | e5dd 5.15–10.68 | (நீங்க) ஒரு பொருள் வாங்கப் போறீங்க. அந்த பொருள் வாங்கணும்னா இந்த மூன்று விஷயத்தை ஞாபகம் வச்சுக்கோங்க | You're going to buy a product / If you want to buy it, / remember these 3 things |
| 15.19 | b5ae 7.72–13.72 | எப்படின்னா, உங்களுக்கு quality and cheap-ஆ கிடைக்கிற பொருள் fast-ஆ கிடைக்காது | How? QUALITY and CHEAP / won't come FAST |
| 21.19 | b5ae 25.85–34.28 | (this works for everything) … spending money with me … choose 2 of 3 … drop one | You can use this for every product / If you're spending money with me, / you have to choose 2 of 3 / and drop 1 |
| 29.62 | b5ae 39.82–51.15 | quality and fast product → pricing cheap-ஆ expect பண்ணாதீங்க; அதே மாதிரி fast and cheap → quality expect பண்ணாதீங்க | If you want QUALITY and FAST, / don't expect the price to be CHEAP / Same way, if you want FAST and CHEAP, / don't expect QUALITY |
| 40.95 | a336 2.25–7.72 | இது என்னுடைய ஒரு ideology. உங்களுக்கு இது பிடிச்சிருந்தா கீழே comment பண்ணுங்க | This is my ideology / If you like it, comment below |

He explicitly states the choose-two rule (b5ae 4.8 s, again at 30.6 s with "drop one", and e5dd 10.7 s), so the
pair highlights follow his words. The three pairs he gives map one-to-one onto the three pen loops of the sketch.
Negations: the two full-take passes agree on "won't / should NOT"; one windowed English pass dropped the "not" in
the last line, the Tamil -காது endings and the full passes were trusted.

Cut and why: b5ae 0–4.8 (greeting), b5ae 13.7–25.8 (the "similarly" / "another option" lines repeat the
QUALITY+CHEAP case), the 4 s pause b5ae 34.3–39.8, b5ae 51–60 ("fun fact", "my opinion" – said again in a336),
d67f 2.4–16.9 (garbled), e5dd 10.7–14.8 (the rule, already the hook), a336 0–2.2 (false start), a336 7.7–18.4
(an unclear "cheap and quality … DM me" line that, as transcribed, contradicts the rule, and a second "comment below").

## Visual plan / cue sheet (`edit/cues.json` has every time)
| out | spoken | layout | graphic |
|---|---|---|---|
| 0–2.9 | "of these three … only two" | notebook board over speaker pane | words underlined in their accent colour on "three" (0.60); the pen rings the "2" by the brace on "two" (1.04) |
| 2.9–5.3 | "here's a diagram" | board opens full screen, face cam | pane slides away; charcoal pen traces draw over the three sketch loops |
| 5.3–9.7 | "Quality, Cheap and then Fast" | board | photo lifts away; ring becomes the pen dot; each label lands on its handwritten word (5.76 / 6.50 / 7.76), previous label steps back; 8.3 labels glide into the clean triangle and the loops morph into clean pair ellipses |
| 9.7–12.2 | "going to buy a product" | b-roll 1 | packed AVSEC keychain (V7) |
| 12.2–15.2 | "remember these three things" | board | the dot taps QUALITY, CHEAP, FAST (13.58 +0.27 s each) |
| 15.2–21.2 | "quality and cheap … won't come fast" | board | QUALITY 17.23 / CHEAP 18.31 fill, QUALITY+CHEAP loop draws and tints, other loops dim; FAST drops, struck through, "× NOT FAST" (20.17) |
| 21.2–23.1 | "use this for every product" | speaker full, punch-in | – |
| 23.1–25.4 | "spending money with me" | b-roll 2 | his printer: build plate of keychains (V1) |
| 25.4–29.6 | "choose 2 of 3 … drop 1" | board | all three pulse (26.01); each pair in turn lights while the third steps out (26.63 / 27.25 / 27.87) |
| 29.6–36.3 | "quality and fast … don't expect cheap" | board | QUALITY 30.80 / FAST 31.66, QUALITY+FAST loop; CHEAP drops "× NOT CHEAP" (35.22) |
| 36.3–41.0 | "same way, fast and cheap … don't expect quality" | board | FAST 37.90 / CHEAP 38.50, CHEAP+FAST loop; QUALITY drops "× NOT QUALITY" (39.46) |
| 41.0–43.3 | "this is my ideology" | board | resolves: all three labels and all three pair loops, stable |
| 43.3–46.4 | "if you like it, comment below" | speaker full, punch-in on "comment" | – |
| 46.4–48.6 | – | end card | logo, QUALITY · CHEAP · FAST, "Choose 2. Drop 1." (his rule), "Comment below" |

Diagram palette: paper #f1ece3, ink #1c1b1a, QUALITY #e4572e, CHEAP #12936a, FAST #2c5ddb. State is never colour
alone: selected = filled chip inside a drawn loop; dropped = grey, struck through, tilted, with a "× NOT …" tag.
Motion reference (prompt-motion.com/ultimaxbt-bbebf5) used only for its system: warm off-white + near-black + bold
type, one dot that carries through every scene, spring overshoots, no gradients/glows/random transitions. None of
its text, numbers, scenes or branding are used. No numbers, percentages or prices appear anywhere.

## Sound
Dialogue: spectral denoise (noise floor ≈ −40 → −70 dB), 20/30 ms fades per cut, loudnorm −16 LUFS (−14 at master).
SFX (edit-video skill pack, synthesized, Apache-2.0): pop on label/bubble arrivals, tick per dot tap, latch when a
pair loop closes, thock when a label drops, one swish when the board opens, ding on the end card.
Music: `gen_bgm.py`, local MusicGen-small (no third-party recording) — AI placeholder, not auditioned by ear; only
its first 30 s are used (the generated tail turns loud and clips), looped with a crossfade and ducked ~19 dB under speech.

## Open issues
- Captions are English translations (his English words kept). A Tamil/Thanglish caption track needs his exact text.
- The a336 DM line was left out (unclear words); if he wants a DM call to action, the exact wording is needed.
- Music is a generated placeholder; replace with a licensed track if preferred.
- v01 b-roll is from the earlier AVSEC shoot; v03 uses licensed Mixkit stock (generic, not his products). His own
  product clips would be a better fit for both beats when he sends them.
