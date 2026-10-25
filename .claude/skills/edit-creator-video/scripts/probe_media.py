#!/usr/bin/env python3
"""Write FFprobe JSON using argument arrays and no shell."""
import sys, json, subprocess
from pathlib import Path
if len(sys.argv)!=3: raise SystemExit('Usage: probe_media.py INPUT OUTPUT.json')
src=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve()
if not src.is_file(): raise SystemExit('Input does not exist')
if out.exists(): raise SystemExit('Output exists; use a new filename')
r=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(src)],capture_output=True,text=True,check=True)
data=json.loads(r.stdout); data['inspected_source']=str(src)
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,indent=2),encoding='utf-8')
print(str(out))
