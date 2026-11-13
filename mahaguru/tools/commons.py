"""Search Wikimedia Commons audio. usage: commons.py "query" [n]"""
import json, sys, ssl, urllib.parse, urllib.request
ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
UA = {'User-Agent': 'ClaudeCode-media-fetch/1.0 (+https://claude.ai/code) python-urllib'}
def api(**p):
    p.update(format='json')
    import time, urllib.error
    for i in range(10):
        try:
            req = urllib.request.Request('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(p), headers=UA)
            return json.loads(urllib.request.urlopen(req, context=ctx, timeout=60).read())
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(60)
    raise RuntimeError('rate limited')
def search(q, n=10):
    r = api(action='query', generator='search', gsrsearch=f'{q} filetype:audio', gsrnamespace=6, gsrlimit=n,
            prop='imageinfo', iiprop='url|extmetadata|size|mime', iiextmetadatafilter='LicenseShortName|Artist|ObjectName')
    out = []
    for p in (r.get('query', {}).get('pages', {}) or {}).values():
        ii = p['imageinfo'][0]; md = ii.get('extmetadata', {})
        lic = md.get('LicenseShortName', {}).get('value', '')
        out.append(dict(title=p['title'], url=ii['url'], license=lic, artist=md.get('Artist', {}).get('value', '')[:80],
                        page=ii.get('descriptionurl'), size=ii.get('size')))
    return out
if __name__ == '__main__':
    for x in search(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10):
        ok = x['license'].lower().startswith(('cc0', 'cc by ', 'cc-by-', 'public domain', 'cc by 4', 'cc by 3', 'cc by 2')) and 'sa' not in x['license'].lower()
        print('OK ' if ok else '-- ', x['license'][:16].ljust(16), x['title'][5:80])
