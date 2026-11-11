"""Build the AA-SEC training video (HyperFrames project) from the PPTX deck,
the per-slide voice clips and their word timings."""
import json, os, re, subprocess, html
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, MSO_SHAPE

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'video')
IMG = os.path.join(OUT, 'assets', 'img')
VOICE = os.path.join(OUT, 'assets', 'voice')
COMP = os.path.join(OUT, 'compositions')
for d in (IMG, VOICE, COMP):
    os.makedirs(d, exist_ok=True)

A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
VO_LEAD = 0.45   # voice starts this long after the scene starts
TAIL = 0.85      # hold after the voice ends
FONT = "'Roboto', 'Inter', sans-serif"

prs = Presentation(os.path.join(ROOT, 'deck.pptx'))
SW, SH = prs.slide_width, prs.slide_height
px = lambda v, total, size: (v or 0) * size / total
X = lambda v: round(px(v, SW, 1920), 1)
Y = lambda v: round(px(v, SH, 1080), 1)
PT = 1920 / (SW / 12700)  # px per point (=2)


def rgb(c):
    try:
        return '#' + str(c.rgb)
    except Exception:
        return None


def paras_of(tf):
    out = []
    for p in tf.paragraphs:
        runs = []
        for child in p._p:
            tag = child.tag.replace(A, '')
            if tag == 'r':
                from pptx.text.text import _Run
                r = _Run(child, p)
                f = r.font
                runs.append(dict(text=r.text, size=(f.size.pt if f.size else 18) * PT,
                                 bold=bool(f.bold), italic=bool(f.italic),
                                 underline=bool(f.underline), color=rgb(f.color) or '#1A1A1A'))
            elif tag == 'br':
                runs.append(dict(br=True))
        al = str(p.alignment) if p.alignment is not None else 'LEFT'
        al = 'center' if 'CENTER' in al else 'right' if 'RIGHT' in al else 'left'
        sz = next((r['size'] for r in runs if 'size' in r), None)
        if sz is None:
            ep = p._p.find(A + 'endParaRPr')
            sz = (int(ep.get('sz')) / 100 * PT) if ep is not None and ep.get('sz') else 36
        out.append(dict(align=al, runs=runs, size=sz))
    return out


def shapes_of(slide):
    res = []
    for sh in slide.shapes:
        d = dict(x=X(sh.left), y=Y(sh.top), w=X(sh.width), h=Y(sh.height), name=sh.name)
        st = sh.shape_type
        if st == MSO_SHAPE_TYPE.PICTURE:
            d['kind'] = 'pic'
            d['blob'] = sh.image.blob
            d['ext'] = sh.image.ext
        elif st == MSO_SHAPE_TYPE.LINE or sh.__class__.__name__ == 'Connector':
            d['kind'] = 'line'
            d['bx'], d['by'], d['ex'], d['ey'] = X(sh.begin_x), Y(sh.begin_y), X(sh.end_x), Y(sh.end_y)
            d['color'] = rgb(sh.line.color) or '#E31837'
            d['lw'] = (sh.line.width.pt if sh.line.width else 1) * PT
        elif st == MSO_SHAPE_TYPE.TABLE:
            d['kind'] = 'table'
            rows = []
            for ri, row in enumerate(sh.table.rows):
                cells = []
                for ci, cell in enumerate(row.cells):
                    fill = None
                    try:
                        if cell.fill.type == 1:
                            fill = rgb(cell.fill.fore_color)
                    except Exception:
                        pass
                    cells.append(dict(paras=paras_of(cell.text_frame), fill=fill,
                                      w=X(sh.table.columns[ci].width)))
                rows.append(dict(cells=cells, h=Y(row.height)))
            d['rows'] = rows
        else:
            d['kind'] = 'text' if st == MSO_SHAPE_TYPE.TEXT_BOX else 'shape'
            if d['kind'] == 'shape':
                try:
                    ast = sh.auto_shape_type
                except Exception:
                    ast = None
                d['geom'] = 'oval' if ast == MSO_SHAPE.OVAL else 'round' if ast == MSO_SHAPE.ROUNDED_RECTANGLE else 'rect'
                if d['geom'] == 'round':
                    try:
                        adj = sh.adjustments[0]
                    except Exception:
                        adj = 0.16667
                    d['radius'] = round(adj * min(d['w'], d['h']), 1)
                d['fill'] = None
                try:
                    if sh.fill.type == 1:
                        d['fill'] = rgb(sh.fill.fore_color)
                except Exception:
                    pass
                d['line'] = None
                try:
                    if sh.line.fill.type == 1:
                        d['line'] = rgb(sh.line.color)
                        d['lw'] = (sh.line.width.pt if sh.line.width else 1) * PT
                except Exception:
                    pass
            if sh.has_text_frame and sh.text_frame.text.strip():
                bp = sh.text_frame._txBody.find(A + 'bodyPr')
                d['anchor'] = bp.get('anchor') or 't'
                ins = [bp.get(k) for k in ('lIns', 'tIns', 'rIns', 'bIns')]
                dflt = [91440, 45720, 91440, 45720]
                d['ins'] = [X(int(v)) if v is not None else X(dflt[i]) for i, v in enumerate(ins)]
                d['paras'] = paras_of(sh.text_frame)
        res.append(d)
    return res


def text_of(d):
    if 'paras' in d:
        return ' '.join(''.join(r.get('text', ' ') for r in p['runs']) for p in d['paras']).strip()
    if d['kind'] == 'table':
        return ' '.join(text_of(c) for r in d['rows'] for c in r['cells'])
    return ''


# ---------------------------------------------------------------- slide 51
def closing_slide():
    W = '#FFFFFF'
    def T(x, y, w, h, text, size, bold=True, color=W, anchor='ctr', align='left'):
        return dict(kind='text', x=x, y=y, w=w, h=h, anchor=anchor, ins=[0, 0, 0, 0],
                    paras=[dict(align=align, size=size, runs=[dict(text=text, size=size, bold=bold, italic=False, underline=False, color=color)])])
    s = [T(115, 70, 1600, 60, "LET'S PRACTISE", 36, color='#FFD9DE'),
         T(115, 135, 1700, 110, 'Which form would you use?', 96)]
    qs = [('A flight security checklist?', 'FOCA'), ('A firearm record?', 'NOTOC'),
          ('An item handover?', 'Ack'), ('A search?', 'Search')]
    for i, (q, _) in enumerate(qs):
        x = 115 + (i % 2) * 860
        y = 285 + (i // 2) * 125
        s.append(dict(kind='shape', geom='round', radius=18, x=x, y=y, w=830, h=100, fill='#FFFFFF', line=None))
        s.append(dict(kind='shape', geom='oval', x=x + 24, y=y + 22, w=56, h=56, fill='#C8102E', line=None,
                      anchor='ctr', ins=[0, 0, 0, 0],
                      paras=[dict(align='center', size=34, runs=[dict(text='?', size=34, bold=True, italic=False, underline=False, color=W)])]))
        s.append(T(x + 104, y, 700, 100, q, 44, color='#1A1A1A'))
    s.append(T(115, 560, 1600, 60, 'REMEMBER THE PATTERN', 32, color='#FFD9DE'))
    steps = ['Choose the correct form', 'Enter accurate details', 'Each person signs', 'Wait for Saved', 'Check the PDF']
    for i, t in enumerate(steps):
        x = 115 + i * 342
        s.append(dict(kind='shape', geom='oval', x=x, y=640, w=72, h=72, fill='#FFFFFF', line=None,
                      anchor='ctr', ins=[0, 0, 0, 0],
                      paras=[dict(align='center', size=40, runs=[dict(text=str(i + 1), size=40, bold=True, italic=False, underline=False, color='#C8102E')])]))
        s.append(T(x, 728, 320, 110, t, 38, anchor='t'))
    s.append(dict(kind='shape', geom='round', radius=20, x=115, y=870, w=1690, h=120, fill='#1F1F24', line=None,
                  anchor='ctr', ins=[40, 0, 40, 0],
                  paras=[dict(align='left', size=40, runs=[
                      dict(text='Something wrong, or no Saved screen? ', size=40, bold=True, italic=False, underline=False, color=W),
                      dict(text='Keep the page open and ask your supervisor.', size=40, bold=False, italic=False, underline=False, color='#FFD9DE')])]))
    return s, '#C8102E'


# ---------------------------------------------------------------- units
def contains(a, b, tol=6):
    return (b['x'] >= a['x'] - tol and b['y'] >= a['y'] - tol and
            b['x'] + b['w'] <= a['x'] + a['w'] + tol and b['y'] + b['h'] <= a['y'] + a['h'] + tol)


def is_highlight(d):
    if d['kind'] == 'line':
        return (d.get('color') or '').upper() in ('#E31837', '#C8102E')
    return d['kind'] == 'shape' and not d.get('fill') and (d.get('line') or '').upper() in ('#E31837', '#C8102E') and not d.get('paras')


def build_units(shapes):
    """Group shapes into units that animate together."""
    owner = {}
    for i, b in enumerate(shapes):
        if is_highlight(b):
            continue
        best = None
        for j, a in enumerate(shapes):
            if i == j or is_highlight(a) or a['kind'] not in ('shape', 'pic'):
                continue
            if a['kind'] == 'pic' and b['kind'] != 'shape':
                continue
            if a['kind'] == 'shape' and not a.get('fill') and not a.get('line'):
                continue
            if contains(a, b) and (a['w'] * a['h'] > b['w'] * b['h'] or (a['w'] * a['h'] == b['w'] * b['h'] and j < i)):
                if best is None or shapes[best]['w'] * shapes[best]['h'] > a['w'] * a['h']:
                    best = j
        if best is not None:
            owner[i] = best

    def top(i):
        while i in owner:
            i = owner[i]
        return i
    groups = {}
    for i, d in enumerate(shapes):
        if is_highlight(d):
            continue
        groups.setdefault(top(i), []).append(i)
    # "CLOSE-UP" label joins the box below it
    for k in list(groups):
        d = shapes[k]
        if d['kind'] == 'text' and text_of(d).upper() == 'CLOSE-UP':
            below = [g for g in groups if g != k and abs(shapes[g]['y'] - (d['y'] + d['h'])) < 30 and abs(shapes[g]['x'] - d['x']) < 30]
            if below:
                groups[below[0]] = sorted(groups[below[0]] + groups.pop(k))
    units = []
    for k, members in groups.items():
        main = shapes[k]
        txt = ' '.join(text_of(shapes[m]) for m in members).strip()
        has_pic = any(shapes[m]['kind'] == 'pic' for m in members)
        role = 'body'
        if has_pic and main['h'] > 500:
            role = 'phone'
        elif has_pic and main['kind'] == 'shape' and any(text_of(shapes[m]).upper() == 'CLOSE-UP' for m in members):
            role = 'closeup'
        elif has_pic:
            role = 'image'
        units.append(dict(members=sorted(members), main=k, text=txt, role=role,
                          x=main['x'], y=min(shapes[m]['y'] for m in members)))
    for i, d in enumerate(shapes):
        if is_highlight(d):
            units.append(dict(members=[i], main=i, text='', role='highlight', x=d['x'], y=d['y']))
    return units


STOP = set('the a an and or of to in on for with your you is are it its this that be by at as from then each one own their they them once only new any all if not do does did was what who how when where can will must should use tap'.split())


def norm(w):
    return re.sub(r'[^a-z0-9]', '', w.lower())


def content_tokens(t):
    toks = [norm(w) for w in re.split(r'[\s/·•\-–—]+', t)]
    return [w for w in toks if len(w) >= 3 and w not in STOP]


def load_words(n):
    p = os.path.join(ROOT, 'words', f's{n:02d}.json')
    if not os.path.exists(p):
        return []
    d = json.load(open(p))
    w = d if isinstance(d, list) else d.get('words', [])
    return [dict(t=norm(x['text']), s=x['start'], e=x['end']) for x in w if 'start' in x]


def find_anchor(tokens, words, cursor):
    for j in range(cursor, len(words)):
        for t in tokens[:4]:
            wt = words[j]['t']
            if wt and (wt == t or (len(t) >= 5 and len(wt) >= 5 and wt[:5] == t[:5])):
                return j
    return None


# ---------------------------------------------------------------- html
def runs_html(paras, split_words=False):
    out = []
    for p in paras:
        parts = []
        for r in p['runs']:
            if r.get('br'):
                parts.append('<br>')
                continue
            st = f"font-size:{max(r['size'], 28):.0f}px;font-weight:{700 if r['bold'] else 400};color:{r['color']};"
            if r['italic']:
                st += 'font-style:italic;'
            if r['underline']:
                st += 'text-decoration:underline;'
            txt = r['text']
            if split_words:
                txt = ''.join(f'<span class="w">{html.escape(w)}</span>' if w.strip() else w
                              for w in re.split(r'(\s+)', txt))
            else:
                txt = html.escape(txt)
            parts.append(f'<span style="{st}">{txt}</span>')
        body = ''.join(parts) if any(r.get('text') for r in p['runs']) else '&nbsp;'
        out.append(f'<p style="text-align:{p["align"]};font-size:{p["size"]:.0f}px">{body}</p>')
    return ''.join(out)


def shape_html(d, sid, idx, split=False):
    eid = f'{sid}-e{idx}'
    base = f'left:{d["x"]}px;top:{d["y"]}px;width:{d["w"]}px;height:{d["h"]}px;'
    if d['kind'] == 'pic':
        fn = f'{sid}-{idx}.{d["ext"]}'
        with open(os.path.join(IMG, fn), 'wb') as f:
            f.write(d['blob'])
        return f'<img id="{eid}" class="el" src="assets/img/{fn}" style="{base}object-fit:fill;" alt="">'
    if d['kind'] == 'line':
        lw = max(d['lw'], 2)
        x0, y0, x1, y1 = d['bx'], d['by'], d['ex'], d['ey']
        if abs(y1 - y0) < 1:  # horizontal
            left, width = min(x0, x1), abs(x1 - x0)
            org = 'left' if x0 <= x1 else 'right'
            st = f'left:{left}px;top:{y0 - lw / 2}px;width:{width}px;height:{lw}px;transform-origin:{org} center;'
            axis = 'x'
        else:
            top_, height = min(y0, y1), abs(y1 - y0)
            org = 'top' if y0 <= y1 else 'bottom'
            st = f'left:{x0 - lw / 2}px;top:{top_}px;width:{lw}px;height:{height}px;transform-origin:center {org};'
            axis = 'y'
        return f'<div id="{eid}" class="el line" data-axis="{axis}" style="{st}background:{d["color"]};border-radius:{lw / 2}px;"></div>'
    if d['kind'] == 'table':
        rows = []
        for r in d['rows']:
            cells = ''.join(
                f'<td style="width:{c["w"]}px;background:{c["fill"] or "transparent"};">{runs_html(c["paras"])}</td>'
                for c in r['cells'])
            rows.append(f'<tr style="height:{r["h"]}px">{cells}</tr>')
        return (f'<table id="{eid}" class="el tbl" style="left:{d["x"]}px;top:{d["y"]}px;">'
                + ''.join(rows) + '</table>')
    st = base
    if d['kind'] == 'shape':
        if d.get('fill'):
            st += f'background:{d["fill"]};'
        if d.get('line'):
            st += f'border:{d["lw"]:.1f}px solid {d["line"]};'
        if d['geom'] == 'oval':
            st += 'border-radius:50%;'
        elif d['geom'] == 'round':
            st += f'border-radius:{d["radius"]}px;'
    inner = ''
    if d.get('paras'):
        jc = {'t': 'flex-start', 'ctr': 'center', 'b': 'flex-end'}.get(d.get('anchor', 't'), 'flex-start')
        l, t, r, b = d['ins']
        st += f'display:flex;flex-direction:column;justify-content:{jc};padding:{t}px {r}px {b}px {l}px;'
        inner = runs_html(d['paras'], split)
    return f'<div id="{eid}" class="el" style="{st}">{inner}</div>'


def scene_html(n, shapes, bg, prev_bg, dur, vo_dur, words):
    sid = f's{n:02d}'
    units = build_units(shapes)
    phones = [u for u in units if u['role'] == 'phone']
    texts = [u for u in units if u['role'] not in ('phone', 'highlight')]
    texts.sort(key=lambda u: (round(u['y'] / 40), u['x']))
    hls = [u for u in units if u['role'] == 'highlight']

    first = prev_bg is None
    flood = (not first) and bg.upper() != (prev_bg or '').upper()
    t0 = 0.45 if flood else (0.0 if first else 0.1)

    # title = largest-font text unit
    def maxfont(u):
        return max((r.get('size', 0) for m in u['members'] for p in shapes[m].get('paras', []) for r in p['runs']), default=0)
    title = max(texts, key=maxfont) if texts else None
    header = [u for u in texts if u is title or (u['y'] < (title['y'] if title else 0) and u['role'] == 'body')]
    body = [u for u in texts if u not in header]

    times = {}
    t = t0 + (0.15 if phones else 0)
    for u in header:
        times[id(u)] = t
        t += 0.16
    hdr_end = t + 0.25
    cursor, prev = 0, hdr_end - 0.3
    limit = max(hdr_end + 0.5, VO_LEAD + vo_dur * 0.85)
    pending = []
    for u in body:
        j = find_anchor(content_tokens(u['text']), words, cursor) if u['text'] else None
        if j is not None:
            at = max(VO_LEAD + words[j]['s'] - 0.2, prev + 0.12, hdr_end)
            cursor = j + 1
            for k, pu in enumerate(pending):  # spread unanchored units before this one
                times[id(pu)] = prev + (at - prev) * (k + 1) / (len(pending) + 1)
            pending = []
            times[id(u)] = min(at, limit)
            prev = times[id(u)]
        else:
            pending.append(u)
    for k, pu in enumerate(pending):
        times[id(pu)] = min(prev + 0.35 * (k + 1), limit)
    # highlights: with the close-up, or a beat after the title
    closeups = [times[id(u)] for u in body if u['role'] == 'closeup']
    hl_t = closeups[0] if closeups else (min([times[id(u)] for u in body], default=hdr_end) + 0.3)
    hl_t = max(hl_t, t0 + 0.9)

    els, js = [], []
    idx = 0
    def emit(u, split=False):
        nonlocal idx
        ids = []
        for m in u['members']:
            els.append(shape_html(shapes[m], sid, idx, split))
            ids.append(f'#{sid}-e{idx}')
            idx += 1
        return ids

    for u in phones:
        ids = emit(u)
        sel = ', '.join(ids)
        if first:
            continue
        js.append(f'tl.fromTo("{sel}", {{opacity:0, y:70, scale:0.97}}, {{opacity:1, y:0, scale:1, duration:0.9, ease:"expo.out"}}, {t0:.2f});')
    for u in texts:
        nw = len(u['text'].split())
        read = min(0.5 + 0.3 * nw, 4.3)
        times[id(u)] = max(0.0, min(times[id(u)], dur - 0.4 - read))
        at = times[id(u)]
        is_title = u is title
        ids = emit(u, split=is_title)
        sel = ', '.join(ids)
        main = shapes[u['main']]
        if is_title:
            js.append(f'tl.fromTo("{ids[0]} .w", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.22, ease:"power2.out", stagger:0.067}}, {at:.2f});')
        elif u['role'] == 'closeup':
            js.append(f'tl.fromTo("{sel}", {{opacity:0, y:34, scale:0.96}}, {{opacity:1, y:0, scale:1, duration:0.7, ease:"expo.out"}}, {at:.2f});')
        elif u['role'] == 'image':
            js.append(f'tl.fromTo("{sel}", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.8, ease:"expo.out"}}, {at:.2f});')
        elif main['kind'] == 'shape' and main.get('geom') == 'oval' and main['w'] < 160:
            # numbered step: the circle pops, its line of text blurs in just after
            js.append(f'tl.fromTo("{sel}", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {at:.2f});')
        elif main['kind'] == 'line':
            axis = 'scaleX' if abs(main['ey'] - main['by']) < 1 else 'scaleY'
            js.append(f'tl.fromTo("{sel}", {{{axis}:0}}, {{{axis}:1, duration:0.45, ease:"power3.out"}}, {at:.2f});')
        elif main['kind'] == 'shape' and main.get('fill') and main['h'] < 160 and main['w'] < 500:
            # badge / chip
            js.append(f'tl.fromTo("{sel}", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.6)"}}, {at:.2f});')
        elif main['kind'] in ('shape', 'table'):
            js.append(f'tl.fromTo("{sel}", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.6, ease:"expo.out"}}, {at:.2f});')
        else:
            js.append(f'tl.fromTo("{sel}", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.3, ease:"power2.out"}}, {at:.2f});')
    hl_boxes = [u for u in hls if shapes[u['main']]['kind'] != 'line']
    hl_lines = [u for u in hls if shapes[u['main']]['kind'] == 'line']
    for k, u in enumerate(hl_boxes):
        ids = emit(u)
        at = hl_t + 0.12 * k
        js.append(f'tl.fromTo("{ids[0]}", {{opacity:0, scale:1.18}}, {{opacity:1, scale:1, duration:0.5, ease:"expo.out"}}, {at:.2f});')
        js.append(f'tl.fromTo("{ids[0]}", {{boxShadow:"0 0 0 0px rgba(227,24,55,0.55)"}}, {{boxShadow:"0 0 0 18px rgba(227,24,55,0)", duration:0.9, ease:"power2.out"}}, {at + 0.35:.2f});')
    for k, u in enumerate(hl_lines):
        ids = emit(u)
        m = shapes[u['main']]
        axis = 'scaleX' if abs(m['ey'] - m['by']) < 1 else 'scaleY'
        at = hl_t + 0.25 + 0.12 * k
        js.append(f'tl.fromTo("{ids[0]}", {{{axis}:0}}, {{{axis}:1, duration:0.4, ease:"power3.out"}}, {at:.2f});')

    # exit: content blurs out together just before the cut
    out_at = dur - 0.32
    js.append(f'tl.to("#{sid}-content", {{opacity:0, filter:"blur(6px)", duration:0.25, ease:"power2.in"}}, {out_at:.2f});')
    bgjs = ''
    if flood:
        bgjs = (f'tl.fromTo("#{sid}-bg", {{clipPath:"circle(0% at 0% 50%)"}}, '
                f'{{clipPath:"circle(150% at 0% 50%)", duration:0.6, ease:"power2.inOut"}}, 0);')
    return f'''<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; font-family:{FONT}; }}
    #{sid}-bg {{ position:absolute; inset:0; background:{bg}; }}
    #{sid}-content {{ position:absolute; inset:0; }}
    #{sid}-content .el {{ position:absolute; box-sizing:border-box; }}
    #{sid}-content p {{ margin:0; line-height:1.18; }}
    #{sid}-content .w {{ display:inline-block; white-space:pre; }}
    #{sid}-content .tbl {{ border-collapse:collapse; }}
    #{sid}-content .tbl td {{ border:1.5px solid #C9CDD2; padding:4px 10px; vertical-align:middle; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
    <div id="{sid}-bg"></div>
    <div id="{sid}-content" data-hold>
      {chr(10).join('      ' + e for e in els).strip()}
    </div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      {bgjs}
      {chr(10).join('      ' + j for j in js).strip()}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
'''


def dur_of(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode())


SECTIONS = [(1, 'Start'), (7, 'FOCA'), (29, 'NOTOC'), (35, 'Acknowledgement'), (41, 'Search List'), (47, 'Records & wrap-up')]


def main():
    slides = []
    for i, s in enumerate(prs.slides, 1):
        try:
            bg = rgb(s.background.fill.fore_color) or '#FFFFFF'
        except Exception:
            bg = '#FFFFFF'
        slides.append((shapes_of(s), bg))
    slides.append(closing_slide())

    hosts, audios, starts = [], [], []
    t, prev_bg = 0.0, None
    for n, (shapes, bg) in enumerate(slides, 1):
        wav = os.path.join(ROOT, 'vo', f's{n:02d}.wav')
        dst = os.path.join(VOICE, f's{n:02d}.wav')
        subprocess.run(['cp', wav, dst], check=True)
        vd = round(dur_of(dst), 3)
        dur = round(VO_LEAD + vd + TAIL, 2)
        html_ = scene_html(n, shapes, bg, prev_bg, dur, vd, load_words(n))
        open(os.path.join(COMP, f's{n:02d}.html'), 'w').write(html_)
        sid = f's{n:02d}'
        hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{t:.2f}" data-duration="{dur:.2f}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1920" data-height="1080"></div>')
        audios.append(f'      <audio id="vo-{sid}" class="clip" src="assets/voice/{sid}.wav" data-start="{t + VO_LEAD:.2f}" '
                      f'data-duration="{vd:.2f}" data-track-index="2" data-volume="1"></audio>')
        starts.append(t)
        t = round(t + dur, 2)
        prev_bg = bg
    total = t
    # progress bar, one segment per section
    segs = []
    for k, (sn, label) in enumerate(SECTIONS):
        a = starts[sn - 1]
        b = starts[SECTIONS[k + 1][0] - 1] if k + 1 < len(SECTIONS) else total
        segs.append((a, b, label))
    seg_html, seg_js = [], []
    for k, (a, b, label) in enumerate(segs):
        left = a / total * 1920
        w = (b - a) / total * 1920 - 4
        seg_html.append(f'<div class="seg" style="left:{left:.1f}px;width:{w:.1f}px"><div id="seg{k}" class="fill"></div></div>')
        seg_js.append(f'tl.fromTo("#seg{k}", {{scaleX:0}}, {{scaleX:1, duration:{b - a:.2f}, ease:"none"}}, {a:.2f});')
    prog = f"""<template>
  <style>
    #root {{ position:absolute; inset:0; pointer-events:none; }}
    #progress-bar {{ position:absolute; left:0; right:0; bottom:0; height:8px; }}
    #progress-bar .seg {{ position:absolute; top:0; height:8px; background:rgba(0,0,0,0.12); overflow:hidden; }}
    #progress-bar .fill {{ position:absolute; inset:0; background:#1A1A1A; transform-origin:left center; }}
  </style>
  <div id="root" data-composition-id="progress" data-width="1920" data-height="1080">
    <div id="progress-bar" data-layout-ignore>{''.join(seg_html)}</div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join('      ' + j for j in seg_js).strip()}
      window.__timelines["progress"] = tl;
    }})();
  </script>
</template>
"""
    open(os.path.join(COMP, 'progress.html'), 'w').write(prog)
    index = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1920px; height:1080px; overflow:hidden; background:#FFFFFF; }}
      #root {{ position:relative; width:100%; height:100%; font-family:{FONT}; }}
      #progress {{ z-index:50; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
{chr(10).join(audios)}
      <div id="progress" data-composition-id="progress" data-composition-src="compositions/progress.html" data-start="0" data-duration="{total:.2f}" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open(os.path.join(OUT, 'index.html'), 'w').write(index)
    print('scenes', len(slides), 'total', round(total, 2), 's')


if __name__ == '__main__':
    main()
