"""Fetch CC0 / CC BY sounds from Openverse. Writes audio/fx/<key>.<ext> and audio/fx/CREDITS.json"""
import json, os, subprocess, sys, urllib.parse, urllib.request, ssl, time
ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
CUES = [  # key, query, min s, max s, pick index
 ('amb_morning',   'tropical birds morning ambience', 40, 400, 0),
 ('amb_cicadas',   'cicadas forest ambience', 30, 400, 0),
 ('amb_yard',      'village birds daytime ambience', 30, 400, 0),
 ('bus_idle',      'diesel bus engine idle', 8, 120, 0),
 ('bus_ride',      'bus interior driving', 15, 300, 0),
 ('amb_estate',    'birds afternoon tropical', 30, 400, 0),
 ('amb_audience',  'audience murmur small hall', 15, 300, 0),
 ('applause',      'small audience applause', 4, 30, 0),
 ('amb_insects',   'insects afternoon ambience', 30, 400, 0),
 ('room_tone',     'room tone hall', 15, 300, 0),
 ('chair_creak',   'wooden chair creak', 1, 10, 0),
 ('paper',         'paper rustle', 1, 15, 0),
 ('book_close',    'book close', 0.5, 6, 0),
 ('amb_evening',   'evening park ambience distant traffic', 30, 400, 0),
 ('bamboo_tap',    'bamboo stick hit', 0.3, 6, 0),
 ('footsteps',     'footsteps dirt path', 3, 40, 0),
 ('swish',         'stick swish', 0.3, 4, 0),
 ('flute_a',       'Bamboo Flute Ananth Pattabi', 50, 200, 0),
 ('tanpura',       'tanpura drone', 40, 120, 0),
 ('mridangam',     'mridangam', 4, 60, 0),
]
only = sys.argv[1:]
credits = json.load(open('audio/fx/CREDITS.json')) if os.path.exists('audio/fx/CREDITS.json') else {}
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'hyperframes-media-use'})
    return urllib.request.urlopen(req, context=ctx, timeout=60).read()
for key, q, mn, mx, pick in CUES:
    if only and key not in only: continue
    d = json.loads(get('https://api.openverse.org/v1/audio/?' + urllib.parse.urlencode({'q': q, 'license': 'cc0,by', 'page_size': 20})))
    ok = [r for r in d['results'] if r['license'] in ('cc0', 'by') and mn <= (r.get('duration') or 0) / 1000 <= mx]
    if len(ok) <= pick:
        print('NO MATCH', key); continue
    r = ok[pick]
    ext = r.get('filetype') or 'mp3'
    raw = f'audio/fx/{key}.src.{ext}'
    open(raw, 'wb').write(get(r['url']))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', raw, '-ar', '48000', '-ac', '2', f'audio/fx/{key}.wav'], check=True)
    os.remove(raw)
    credits[key] = dict(title=r['title'], creator=r.get('creator'), license=r['license'], license_version=r.get('license_version'),
                        source=r.get('foreign_landing_url'), duration_s=(r.get('duration') or 0) / 1000)
    print(f"{key:13} {r['license']:3} {credits[key]['duration_s']:6.1f}s  {r['title'][:55]} | {r.get('creator')}")
    time.sleep(0.5)
json.dump(credits, open('audio/fx/CREDITS.json', 'w'), indent=1, ensure_ascii=False)
