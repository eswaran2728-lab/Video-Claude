# Captions: Romanized Malaysian Tamil (Tanglish) as spoken, his English words kept in English (creator's own rule in the
# malaysian-affiliate-script-video-director skill: Tamil audio -> Romanized Tamil captions, not English translation).
# Reading built from 7 Whisper large-v3 passes (whole clip auto/Tamil/English/translate, phrase chunks, finer windows,
# re-transcription of the edited track: transcript*.json, verify_cut.json). Times are SOURCE seconds.
# k = the one keyword shown in the accent colour. "?" in FLAG = reading not fully resolved (listed in the report).
CAPS = [
    # (src_start, src_end, text, keyword)
    (0.40, 1.86, "call pesumbothu background-la", "call"),
    (1.86, 3.72, "noise romba irukkumna,", "noise"),
    (3.72, 4.90, "ungalukku disturbance-aa irukka?", "disturbance-aa"),
    (4.90, 6.83, "okay, namma office-la irunthaalum sari,", "office-la"),
    (6.83, 7.83, "car-la porappa,", "car-la"),
    (7.83, 8.99, "intha maathiri time-la", None),
    (8.99, 9.85, "namma vanthu", None),
    (9.85, 11.31, "romba call pesurappa,", "call"),
    (11.31, 12.20, "romba noise kidaikkum.", "noise"),
    (12.20, 13.52, "so, athukkuthaan", None),
    (13.52, 14.20, "naan intha earbuds-a", "earbuds-a"),
    (14.20, 16.30, "TikTok-la vanthu purchase pannen.", "TikTok-la"),
    (16.92, 18.15, "intha earbuds-la", "earbuds-la"),
    (18.15, 19.41, "noise cancelling", "noise cancelling"),
    (19.41, 20.65, "and then two microphones", "two microphones"),
    (20.65, 21.30, "irukkurathaala,", None),
    (21.30, 23.26, "ungaloda call vanthu", "call"),
    (23.26, 24.48, "noise cancel aayi,", "noise cancel"),
    (24.48, 25.70, "neenga pesurappa,", None),
    (25.70, 27.74, "thelivaa vilangum,", "thelivaa"),
    (27.74, 29.40, "ungalukkum avanga pesurathu", None),
    (29.40, 30.08, "clear-aa vilangum.", "clear-aa"),
    (30.08, 30.84, "so ungalukku venumna,", None),
    (30.84, 31.70, "keezha link-ku click panni", "link-ku"),
    (31.70, 99.0, "purchase pannikonga.", "purchase"),
]
FLAG = [
    ("4.95-6.83", "office-la irunthaalum sari", "two passes hear 'office vanthaalum sari'; unprompted Tamil + English passes favour 'irunthaal(um)'"),
    ("11.31-12.10", "romba noise kidaikkum", "last word heard as kidaichu / kidaikkum / kekkum"),
    ("14.12-16.18", "TikTok-la vanthu purchase pannen", "verb ending unclear (pannen / pannathu); 'vanthu' heard in 2 of 4 passes"),
    ("25.70-26.60", "(lead-in before 'thelivaa vilangum')", "heard as 'appasil oru' / 'appa sila' - left out of the caption, not guessed"),
    ("30.84-31.56", "keezha link-ku", "heard as 'keezhe-la vilakku-kku' (= link-kku); English pass: 'link below'"),
]
