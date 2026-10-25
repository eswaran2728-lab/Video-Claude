#!/usr/bin/env python3
"""Validate the extracted distribution without requiring a Git checkout."""
from pathlib import Path
import ast,hashlib,json,re
r=Path(__file__).resolve().parents[1]
for p in r.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
for p in r.rglob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
for p in r.rglob('*.md'):
 for href in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',p.read_text(encoding='utf-8')):
  if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',href) or href.startswith('#'):continue
  target=p.parent/href.split('#')[0]
  if not target.exists():raise SystemExit(f'Broken link: {p.relative_to(r)} -> {href}')
assert len(list((r/'references/effects').glob('*.md')))==46
assert len(list((r/'references/reel-blueprints').glob('*.md')))==7
assert len(list((r/'vendor/favstash/skills').rglob('SKILL.md')))==10
sfx=r/'vendor/favstash/skills/3-editing/edit-video/assets/sfx'
m=json.loads((sfx/'manifest.json').read_text())
assert m['count']==len(m['sounds'])
for item in m['sounds']:
 assert hashlib.sha256((sfx/item['file']).read_bytes()).hexdigest()==item['sha256'],item['file']
assert (r/'vendor/favstash/LICENSE').exists()
assert (r/'vendor/favstash/skills/3-editing-styles/breakout-card/assets/fonts/OFL.txt').exists()
print('PASS: JSON, Python syntax, relative links, 46 recipes, 7 blueprints, 10 upstream skills, SFX checksums and licences')
