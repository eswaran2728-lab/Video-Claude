#!/usr/bin/env python3
"""Copy this pack and all ten bundled skills. Dry-run by default; never overwrite."""
import argparse, shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--destination',required=True,help='Absolute path to project .claude/skills');p.add_argument('--apply',action='store_true');a=p.parse_args()
dest=Path(a.destination).expanduser()
if not dest.is_absolute():raise SystemExit('Use an absolute destination')
root=Path(__file__).resolve().parents[1];vendor=root/'vendor/favstash/skills'
sources=[root]+sorted(x.parent for x in vendor.rglob('SKILL.md'))
assert len(sources)==11,'Expected router plus ten upstream skills'
targets=[dest/('edit-creator-video' if i==0 else x.name) for i,x in enumerate(sources)]
for target in targets:
 if target.exists():raise SystemExit(f'Refusing existing destination: {target}; back it up or choose a new destination')
for source,target in zip(sources,targets):
 if source==dest or source in dest.parents:raise SystemExit('Destination must be outside the extracted pack')
 print(('COPY' if a.apply else 'WOULD COPY'),source,'->',target)
if a.apply:
 dest.mkdir(parents=True,exist_ok=True)
 for source,target in zip(sources,targets):shutil.copytree(source,target,ignore=shutil.ignore_patterns('__pycache__','node_modules','.git'))
 print('Copied 11 skill folders. No runtimes installed, no accounts connected, no files uploaded.')
