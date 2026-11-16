# work23 — Hanuman Vahanam order story (new media set, 16 Nov 2026)
Source (Drive folder, not in git): C005 (talking head, the order), C006 (first raw print with supports -> gold finished piece),
C007 (call to action), photo.jpg (finished piece). Each clip was uploaded twice; duplicates were byte-identical and removed.
Speech: Tamil (colloquial). Transcribed in phrase chunks with Whisper large-v3 (analysis/transcript_chunks.json) - rough, many words uncertain.
- edit.py: picks phrases from the plan, shortens pauses, writes timing-map.json, cuts graded proxies, builds the cleaned voice track.
- build3.py: HyperFrames page (punch-ins, hook, cards, chips, slicer panel, end card). audio3.py: original music + SFX, ducked under voice.
- v01: first preview. Rebuild: python3 edit.py v01 && python3 audio3.py v01 && python3 build3.py v01; render draft in v01/.
