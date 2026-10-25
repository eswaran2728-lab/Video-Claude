#!/usr/bin/env python3
"""Basic photo-only hard-cut preview. No captions, logos or advanced effects."""
import json, sys, subprocess, tempfile, math
from pathlib import Path
if len(sys.argv)!=3: raise SystemExit('Usage: render_montage.py PROJECT.json OUTPUT.mp4')
config=Path(sys.argv[1]).resolve(); p=json.loads(config.read_text(encoding='utf-8')); out=Path(sys.argv[2]).resolve()
if out.exists(): raise SystemExit('Output exists; choose a new filename')
def resolve(s):
 q=Path(s).expanduser();return q.resolve() if q.is_absolute() else (config.parent/q).resolve()
w=int(p.get('preview',{}).get('width',540));h=int(p.get('preview',{}).get('height',960));fps=float(p.get('canvas',{}).get('fps',30))
if not (0<w<=3840 and 0<h<=3840 and w%2==0 and h%2==0 and math.isfinite(fps) and 1<=fps<=60):raise SystemExit('Invalid output geometry or fps')
clips=p.get('clips',[])
if not clips or len(clips)>100:raise SystemExit('Provide 1–100 photos')
cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin']; filters=[];duration=0
for i,c in enumerate(clips):
 src=resolve(c['path']);d=float(c['duration'])
 if not src.is_file() or src.suffix.lower() not in ['.jpg','.jpeg','.png','.webp']:raise SystemExit('Only existing local photo files are supported')
 if not math.isfinite(d) or not 0.1<=d<=60:raise SystemExit('Each photo duration must be 0.1–60 seconds')
 frames=round(d*fps);d=frames/fps;duration+=d
 cmd+=['-loop','1','-framerate',str(fps),'-i',str(src)]
 filters.append(f'[{i}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps={fps},trim=duration={d},setpts=PTS-STARTPTS[v{i}]')
filters.append(''.join(f'[v{i}]' for i in range(len(clips)))+f'concat=n={len(clips)}:v=1:a=0[v]')
music=p.get('music',{}); audio=music.get('path')
if audio:
 src=resolve(audio)
 if not src.is_file():raise SystemExit('Music file missing')
 gain=float(music.get('gain_db',-16))
 if not math.isfinite(gain) or not -60<=gain<=0:raise SystemExit('gain_db must be between -60 and 0')
 cmd+=['-i',str(src)]
 filters.append(f'[{len(clips)}:a]volume={gain}dB,apad,atrim=duration={duration},afade=t=out:st={max(0,duration-.5)}:d=0.5[a]')
cmd+=['-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','[v]']
if audio:cmd+=['-map','[a]','-c:a','aac','-ar','48000']
else:cmd+=['-an']
out.parent.mkdir(parents=True,exist_ok=True)
# Render atomically to a temporary file in the destination directory.
with tempfile.TemporaryDirectory(prefix='montage-',dir=out.parent) as td:
 temp=Path(td)/'preview.mp4'
 cmd+=['-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-t',str(duration),'-movflags','+faststart',str(temp)]
 subprocess.run(cmd,check=True);temp.replace(out)
print(str(out))
