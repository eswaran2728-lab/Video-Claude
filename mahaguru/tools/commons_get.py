import json, os, ssl, subprocess, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from commons import api, ctx, UA
WANT = {
 'amb_dawn':    'File:RainforestDawnChorus Selaliparai DM.ogg',
 'amb_walk':    'File:Walk in the rainforest.ogg',
 'cicada':      'File:Cicada 20200619.wav',
 'cicada2':     'File:Cicadas in Greece.ogg',
 'amb_city':    'File:Bird sings in the morning with cars in the background.ogg',
 'amb_outdoor': 'File:20090610 0 ambience.ogg',
 'bus_engine':  'File:WWS City Bus MAN SG 220 – engine.oga',
 'bus_door':    'File:WWS CityBusMANSG220dooropeningclosing.ogg',
 'applause':    'File:Slow starting applause.ogg',
 'applause2':   'File:277021 sandermotions applause-2.wav',
 'crowd':       'File:Festival concert people crowd.ogg',
 'chair':       'File:Creaky wooden swivel chair.ogg',
 'footstep':    'File:Footstep on Gravel (Gravity Sound).mp3',
 'flute1':      'File:Indian Flute (Antti Luode).mp3',
 'flute2':      'File:Bansuri sample E bass.ogg',
 'flute3':      'File:Samuel Corwin - 15 - Flute and Drum Rishikesh.ogg',
 'veena1':      'File:Kiravani-L Ramakrishnan.ogg',
 'veena2':      'File:Shri Nilotpala Nayike, rendered on the Veena by L Ramakishnan.ogg',
 'tanpura':     'File:Ninnukori-Mohanam-ramakrishnamurthy.wav',
}
cred = json.load(open('audio/src/CREDITS.json')) if os.path.exists('audio/src/CREDITS.json') else {}
os.makedirs('audio/src', exist_ok=True)
for k, t in WANT.items():
    if k in cred: continue
    r = api(action='query', titles=t, prop='imageinfo', iiprop='url|extmetadata', iiextmetadatafilter='LicenseShortName|Artist|Credit')
    p = next(iter(r['query']['pages'].values()))
    if 'imageinfo' not in p:
        print('MISSING', k); continue
    ii = p['imageinfo'][0]; md = ii.get('extmetadata', {})
    ext = ii['url'].rsplit('.', 1)[-1]
    src = f'audio/src/{k}.{ext}'
    data = None
    for i in range(6):
        try:
            data = urllib.request.urlopen(urllib.request.Request(ii['url'], headers=UA), context=ctx, timeout=120).read(); break
        except Exception as e:
            print('  retry', k, e, flush=True); time.sleep(60)
    if data is None:
        print('FAILED', k); continue
    open(src, 'wb').write(data)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-ar', '48000', '-ac', '2', f'audio/src/{k}.wav'], check=True)
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'audio/src/{k}.wav']))
    import re
    artist = re.sub('<[^>]+>', '', md.get('Artist', {}).get('value', '')).strip()
    cred[k] = dict(title=t[5:], license=md.get('LicenseShortName', {}).get('value'), artist=artist, page=ii['descriptionurl'], duration=round(d, 1))
    print(f"{k:12} {d:7.1f}s {cred[k]['license']:14} {artist[:40]}")
    json.dump(cred, open('audio/src/CREDITS.json', 'w'), indent=1, ensure_ascii=False)
    time.sleep(20)
json.dump(cred, open('audio/src/CREDITS.json', 'w'), indent=1, ensure_ascii=False)
