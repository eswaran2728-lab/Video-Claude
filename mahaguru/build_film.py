"""Assemble the Mahaguru short film as a HyperFrames project (film/).

Picture: 41 Higgsfield clips in bible order, 9.6 s slots (0.2 s trimmed from each
end of the 10 s clip so dissolves have handles). Sound: per-line Tamil voice clips
plus pre-mixed ambience / music / effects stems (built by mix_audio.py).
"""
import json, os, shutil, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.join(ROOT, 'film')
A = lambda *p: os.path.join(FILM, 'assets', *p)

ORDER = ['1A', 'TITLE', '1B', '1C', '1D', '2A', '2B', '2C', '2D', '3A', '3B', '3C', '3D',
         '4A', '4B', '4C', '4D', '5A', '5B', '5C', '5D', '6A', '6B', '6C', '6D',
         '7A', '7B', '7C', '7D', '8A', '8B', '8C', '8D', '9A', '9B', '9C', '9D',
         '10A', '10B', '10C', '10D']
SLOT, HEAD = 9.6, 0.2
T = {k: round(i * SLOT, 3) for i, k in enumerate(ORDER)}          # slot starts
C0 = {k: round(T[k] - HEAD, 3) for k in ORDER}                     # where clip time 0 lands
FILM_END = round(len(ORDER) * SLOT, 3)
CREDITS_LEN = 9.0
TOTAL = round(FILM_END + CREDITS_LEN, 3)

DISSOLVE_IN = {'4A', '8A', '10D'}          # crossfade from the previous shot
# black dips: (shot whose start is the dip centre, fade-out length, fade-in length)
DIPS = [('TITLE', 0.7, 2.0), ('1B', 1.0, 0.25), ('2A', 0.5, 0.8), ('9A', 0.5, 0.7)]
REENACT = ['2A', '7A']
IVORY = '#F3E9D8'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))


FONTS = '''
@font-face { font-family: "MG Serif"; src: url("assets/fonts/serif-tamil-700.woff2") format("woff2"); font-weight: 700; unicode-range: U+0B80-0BFF, U+200C-200D, U+25CC; }
@font-face { font-family: "MG Serif"; src: url("assets/fonts/serif-tamil-400.woff2") format("woff2"); font-weight: 400; unicode-range: U+0B80-0BFF, U+200C-200D, U+25CC; }
@font-face { font-family: "MG Serif"; src: url("assets/fonts/serif-latin-700.woff2") format("woff2"); font-weight: 700; unicode-range: U+0000-00FF, U+2000-206F; }
@font-face { font-family: "MG Serif"; src: url("assets/fonts/serif-latin-400.woff2") format("woff2"); font-weight: 400; unicode-range: U+0000-00FF, U+2000-206F; }
@font-face { font-family: "MG Sans"; src: url("assets/fonts/sans-tamil-700.woff2") format("woff2"); font-weight: 700; unicode-range: U+0B80-0BFF, U+200C-200D, U+25CC; }
@font-face { font-family: "MG Sans"; src: url("assets/fonts/sans-tamil-400.woff2") format("woff2"); font-weight: 400; unicode-range: U+0B80-0BFF, U+200C-200D, U+25CC; }
@font-face { font-family: "MG Sans"; src: url("assets/fonts/sans-latin-700.woff2") format("woff2"); font-weight: 700; unicode-range: U+0000-00FF, U+2000-206F; }
@font-face { font-family: "MG Sans"; src: url("assets/fonts/sans-latin-400.woff2") format("woff2"); font-weight: 400; unicode-range: U+0000-00FF, U+2000-206F; }
'''


def scene(cid, css, body, js, root_extra=''):
    return f'''<template>
  <style>
{FONTS}
    #root {{ position:absolute; inset:0; overflow:hidden; {root_extra} }}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
{body}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{js}
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
'''


def title_scene():
    css = f'''
    #title-name {{ position:absolute; left:0; right:0; top:330px; text-align:center; font-family:"MG Serif"; font-weight:700;
                  font-size:190px; line-height:1.3; color:{IVORY}; letter-spacing:0.01em; text-shadow:0 0 30px rgba(0,0,0,0.85); }}
    #title-sub {{ position:absolute; left:0; right:0; top:640px; text-align:center; font-family:"MG Serif"; font-weight:400;
                 font-size:52px; line-height:1.4; color:{IVORY}; opacity:0.85; text-shadow:0 0 18px rgba(0,0,0,0.95), 0 0 6px rgba(0,0,0,0.9); }}
    #title-rule {{ position:absolute; left:50%; top:612px; width:140px; height:2px; margin-left:-70px; background:#C9A57A; }}'''
    body = '''    <div id="title-name">மகாகுரு</div>
    <div id="title-rule"></div>
    <div id="title-sub">ஒரு சிலம்பத்தின் உயிர் வரலாறு</div>'''
    js = '''      tl.fromTo("#title-name", {opacity:0}, {opacity:1, duration:3, ease:"sine.inOut"}, 2.2);
      tl.fromTo("#title-rule", {opacity:0, scaleX:0.3}, {opacity:0.8, scaleX:1, duration:1.6, ease:"power2.out"}, 4.6);
      tl.fromTo("#title-sub", {opacity:0}, {opacity:0.85, duration:2, ease:"sine.inOut"}, 5.2);'''
    return scene('title', css, body, js)


def dedication_scene():
    css = f'''
    .ded {{ position:absolute; left:0; right:0; text-align:center; color:{IVORY}; }}
    #ded-name {{ top:330px; font-family:"MG Serif"; font-weight:700; font-size:120px; line-height:1.3; }}
    #ded-sri {{ top:520px; font-family:"MG Serif"; font-weight:400; font-size:64px; line-height:1.4; }}
    #ded-rule {{ position:absolute; left:50%; top:640px; width:120px; height:2px; margin-left:-60px; background:#C9A57A; }}
    #ded-en {{ top:672px; font-family:"MG Serif"; font-weight:400; font-size:40px; letter-spacing:0.04em; opacity:0.8; }}'''
    body = '''    <div id="ded-name" class="ded">மகாகுரு</div>
    <div id="ded-sri" class="ded">ஸ்ரீ எஸ். ஆறுமுகம்</div>
    <div id="ded-rule"></div>
    <div id="ded-en" class="ded">Dedicated to Mahaguru Sri S. Arumugam</div>'''
    js = '''      tl.fromTo("#ded-name", {opacity:0}, {opacity:1, duration:1.6, ease:"sine.inOut"}, 2.0);
      tl.fromTo("#ded-sri", {opacity:0}, {opacity:1, duration:1.4, ease:"sine.inOut"}, 2.9);
      tl.fromTo("#ded-rule", {opacity:0, scaleX:0.3}, {opacity:0.8, scaleX:1, duration:1.2, ease:"power2.out"}, 3.6);
      tl.fromTo("#ded-en", {opacity:0}, {opacity:0.8, duration:1.4, ease:"sine.inOut"}, 4.0);
      tl.to("#ded-name, #ded-sri, #ded-rule, #ded-en", {opacity:0, duration:1.2, ease:"sine.in"}, 8.4);'''
    return scene('dedication', css, body, js)


def credits_scene(credit_lines):
    css = f'''
    #cr-wrap {{ position:absolute; left:0; right:0; top:200px; text-align:center; color:{IVORY}; font-family:"MG Sans"; }}
    #cr-wrap .h {{ font-family:"MG Serif"; font-weight:700; font-size:56px; margin-bottom:34px; }}
    #cr-wrap .l {{ font-size:28px; line-height:1.55; opacity:0.85; }}
    #cr-wrap .s {{ font-size:28px; line-height:1.5; opacity:0.7; margin-top:26px; }}'''
    items = ''.join(f'<div class="l">{esc(l)}</div>' for l in credit_lines)
    body = f'''    <div id="cr-wrap" data-hold>
      <div class="h">மகாகுரு</div>
      {items}
      <div class="s">Reenacted scenes. All faces are AI-generated and do not depict the real persons.</div>
    </div>'''
    js = f'''      tl.fromTo("#cr-wrap", {{opacity:0}}, {{opacity:1, duration:1.0, ease:"sine.inOut"}}, 0.6);
      tl.to("#cr-wrap", {{opacity:0, duration:1.2, ease:"sine.in"}}, {CREDITS_LEN - 1.9:.2f});'''
    return scene('credits', css, body, js, 'background:#000;')


def subs_scene(lines, vdur):
    css = '''
    .sub { position:absolute; left:192px; right:192px; bottom:96px; text-align:center; }
    .sub span { display:inline-block; font-family:"MG Sans"; font-weight:700; font-size:44px; line-height:1.45; color:#fff;
                background:rgba(0,0,0,0.42); padding:6px 22px 8px; border-radius:6px; text-shadow:0 2px 6px rgba(0,0,0,0.6); }'''
    body, js, srt = [], [], []
    for n, L in enumerate(lines, 1):
        s = C0[L['shot']] + L['s']
        e = s + vdur[L['id']] + 0.45
        sid = 'sub-' + L['id'].replace('-', '')
        body.append(f'    <div id="{sid}" class="sub clip" data-start="{s:.2f}" data-duration="{e - s:.2f}"><span>{esc(L["t"])}</span></div>')
        js.append(f'      tl.fromTo("#{sid} span", {{opacity:0}}, {{opacity:1, duration:0.2, ease:"none"}}, {s:.2f});')
        js.append(f'      tl.to("#{sid} span", {{opacity:0, duration:0.2, ease:"none"}}, {e - 0.25:.2f});')
        f = lambda t: f'{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}'
        srt.append(f'{n}\n{f(s)} --> {f(e)}\n{L["t"]}\n')
    open(os.path.join(ROOT, 'Mahaguru_Tamil.srt'), 'w', encoding='utf-8').write('\n'.join(srt))
    return scene('subs', css, '\n'.join(body), '\n'.join(js))


def labels_scene():
    css = f'''
    .lbl {{ position:absolute; left:192px; top:118px; }}
    .lbl span {{ display:inline-block; font-family:"MG Sans"; font-weight:700; font-size:32px; color:{IVORY};
           background:rgba(0,0,0,0.45); padding:8px 20px 10px 18px; border-left:3px solid #C9A57A; border-radius:0 6px 6px 0; }}'''
    body, js = [], []
    for k in REENACT:
        s, d = C0[k] + 0.9, 5.0
        lid = f'lbl-{k}'
        body.append(f'    <div id="{lid}" class="lbl clip" data-start="{s:.2f}" data-duration="{d:.2f}"><span>மறுஉருவாக்கம்</span></div>')
        js.append(f'      tl.fromTo("#{lid} span", {{opacity:0}}, {{opacity:0.9, duration:0.6, ease:"sine.out"}}, {s:.2f});')
        js.append(f'      tl.to("#{lid} span", {{opacity:0, duration:0.6, ease:"sine.in"}}, {s + d - 0.7:.2f});')
    return scene('labels', css, '\n'.join(body), '\n'.join(js))


def main():
    lines = json.load(open(os.path.join(ROOT, 'lines.json')))
    for L in lines:
        L['shot'] = L['id'].split('-')[0]
    os.makedirs(A('audio', 'voice'), exist_ok=True)
    os.makedirs(os.path.join(FILM, 'compositions'), exist_ok=True)
    vdur = {}
    for L in lines:
        src = os.path.join(ROOT, 'audio', 'voice', L['id'] + '.wav')
        shutil.copy(src, A('audio', 'voice', L['id'] + '.wav'))
        vdur[L['id']] = round(dur(src), 3)
    json.dump(dict(T=T, C0=C0, FILM_END=FILM_END, TOTAL=TOTAL,
                   voice=[dict(id=L['id'], start=round(C0[L['shot']] + L['s'], 3), dur=vdur[L['id']]) for L in lines]),
              open(os.path.join(ROOT, 'timing.json'), 'w'), indent=1)

    comp = lambda n, s: open(os.path.join(FILM, 'compositions', n + '.html'), 'w').write(s)
    comp('title', title_scene())
    comp('dedication', dedication_scene())
    comp('subs', subs_scene(lines, vdur))
    comp('labels', labels_scene())
    credit_lines = json.load(open(os.path.join(ROOT, 'credit_lines.json'))) if os.path.exists(os.path.join(ROOT, 'credit_lines.json')) else []
    comp('credits', credits_scene(credit_lines))

    vids, tw = [], []
    nxt = {ORDER[i]: (ORDER[i + 1] if i + 1 < len(ORDER) else None) for i in range(len(ORDER))}
    for i, k in enumerate(ORDER):
        din = k in DISSOLVE_IN
        dout = nxt[k] in DISSOLVE_IN if nxt[k] else False
        start = T[k] - (HEAD if din else 0)
        mstart = 0 if din else HEAD
        end = (T[nxt[k]] if nxt[k] else FILM_END) + (HEAD if dout else 0)
        if not nxt[k]:
            end = FILM_END
        d = end - start
        assert mstart + d <= 10.04 + 1e-6, (k, mstart, d)
        vids.append(f'      <div id="w-{k}" class="vw" style="z-index:{i + 1}"><video id="v-{k}" class="clip" src="assets/video/{k}.mp4" muted playsinline '
                    f'data-start="{start:.3f}" data-duration="{d:.3f}" data-media-start="{mstart:.3f}" data-track-index="1"></video></div>')
        if din:
            tw.append(f'tl.fromTo("#w-{k}", {{opacity:0}}, {{opacity:1, duration:{2 * HEAD:.2f}, ease:"sine.inOut"}}, {start:.3f});')
    # black dips and the head / tail fades
    tw.append('tl.fromTo("#black", {opacity:1}, {opacity:0, duration:0.8, ease:"sine.out"}, 0);')
    for k, fo, fi in DIPS:
        t = T[k]
        tw.append(f'tl.to("#black", {{opacity:1, duration:{fo}, ease:"sine.in"}}, {t - fo:.3f});')
        tw.append(f'tl.to("#black", {{opacity:0, duration:{fi}, ease:"sine.out"}}, {t:.3f});')
    tw.append(f'tl.to("#black", {{opacity:1, duration:1.2, ease:"sine.in"}}, {FILM_END - 1.2:.3f});')

    host = lambda cid, s, d, z: (f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                                 f'data-start="{s:.3f}" data-duration="{d:.3f}" data-track-index="{z}" data-track-kind="graphics" '
                                 f'data-width="1920" data-height="1080" style="z-index:{100 + z}"></div>')
    hosts = [host('title', C0['TITLE'], 10.0, 2), host('dedication', C0['10D'], FILM_END - C0['10D'], 3),
             host('labels', 0, FILM_END, 4), host('subs', 0, FILM_END, 5), host('credits', FILM_END, CREDITS_LEN, 6)]

    audios = []
    for L in lines:
        s = C0[L['shot']] + L['s']
        audios.append(f'      <audio id="vo-{L["id"].replace("-", "")}" class="clip" src="assets/audio/voice/{L["id"]}.wav" '
                      f'data-start="{s:.3f}" data-duration="{vdur[L["id"]]:.3f}" data-track-index="10" data-volume="1"></audio>')
    for ti, (stem, vol) in enumerate((('ambience', 1), ('music', 1), ('effects', 1))):
        p = A('audio', stem + '.wav')
        if os.path.exists(p):
            audios.append(f'      <audio id="stem-{stem}" class="clip" src="assets/audio/{stem}.wav" data-start="0" '
                          f'data-duration="{min(dur(p), TOTAL):.3f}" data-track-index="{11 + ti}" data-volume="{vol}"></audio>')

    index = f'''<!doctype html>
<html lang="ta">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1920px; height:1080px; overflow:hidden; background:#000; }}
      #root {{ position:relative; width:100%; height:100%; background:#000; }}
      .vw {{ position:absolute; inset:0; }}
      .vw video {{ position:absolute; left:0; top:0; width:1920px; height:1080px; object-fit:cover; }}
      #black {{ position:absolute; inset:0; background:#000; z-index:90; pointer-events:none; }}
      .bar {{ position:absolute; left:0; width:1920px; height:60px; background:#000; z-index:95; pointer-events:none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1920" data-height="1080" data-fps="30">
{chr(10).join(vids)}
      <div id="black"></div>
      <div class="bar" style="top:0" data-layout-ignore></div>
      <div class="bar" style="bottom:0" data-layout-ignore></div>
{chr(10).join(hosts)}
{chr(10).join(audios)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join('      ' + t for t in tw).strip()}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
    open(os.path.join(FILM, 'index.html'), 'w').write(index)
    print('film', FILM_END, 's + credits =', TOTAL, 's; lines', len(lines))


if __name__ == '__main__':
    main()
