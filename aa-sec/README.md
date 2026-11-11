# AA-SEC Signing Forms – training video

Narrated motion-graphics version of the *AA-SEC Signing Forms – Staff Guide* deck (50 slides + a closing "Let's practise" scene), built with HyperFrames.

- `deck.pptx` – source slides
- `narration.md` – the script; `vo/spoken/` – the text actually sent to the voice (spelled for pronunciation, e.g. "A. A. Seck", "Noh-tock")
- `words/` – word timings of each voice clip, used to reveal each item as it is spoken
- `build.py` – rebuilds `video/` (one scene per slide) from the deck, voice clips and timings
- `video/` – the HyperFrames project (`index.html`, `compositions/s01…s51.html`, `assets/`)

Voice: Kokoro `bf_emma` (free, local). Rebuild and render:

```bash
python3 build.py
cd video && npx hyperframes check && npx hyperframes render --quality delivery -o renders/AA-SEC_Signing_Forms_Training.mp4
```
