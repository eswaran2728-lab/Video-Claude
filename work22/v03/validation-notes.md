# v03 validation notes
Status: DRAFT PREVIEW, not approved; no final export. v01, v02 kept.
Change from v02: the owner's own voice from the clip (source 1.75-21.4 s) is now the main audio (voice.py -> assets/audio/voice.wav,
voice-map.json). Speech kept in original order; only silences longer than 0.45 s shortened. Cleaned: high-pass 85 Hz, 400 Hz hum notch,
FFT noise reduction, mild compression, loudness -16 LUFS. Music ducked 11 dB under speech; effects softened under speech. Scenes lengthened to 19.8 s.
Checks: lint 0 errors; draft render 19.8 s, decodes clean, -16.8 LUFS, peak -2.4 dBFS; voice stem correlates 0.84-0.97 with the final mix in its segments.
Not verified: nobody has listened (I cannot hear audio); words unknown (transcription unreliable), so no subtitles yet; speech after 21.4 s left out.
