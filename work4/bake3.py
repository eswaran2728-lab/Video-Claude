import json,subprocess,os
edl=json.load(open("edl3.json"));END=54.72;F=30
os.makedirs("seg",exist_ok=True);L1=open("seg/band.txt","w");L2=open("seg/bg.txt","w");out_f=0
ENC=["-an","-c:v","libx264","-preset","fast","-pix_fmt","yuv420p"]
for i,e in enumerate(edl):
    n=round(e["t1"]*F)-round(e["t0"]*F)
    if e["kind"]=="video":
        sp=e["speed"];src_len=n/F*sp+0.2
        inp=["-i",f"src/{e['src']}.mp4"]
        head=f"[0:v]trim=start={e['ss']}:duration={src_len:.3f},setpts=(PTS-STARTPTS)/{sp},fps={F},split[a][b];"
        band="[a]crop=ih*4/3:ih,scale=1080:810:flags=lanczos,unsharp=5:5:0.6:5:5:0,setsar=1[band];"
    else:
        inp=["-loop","1","-framerate",str(F),"-i",f"photos/{e['src']}.jpg"]
        z=f"zoompan=z='1+0.0016*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x810:fps={F}"
        head="[0:v]split[a][b];"
        # landscape: fill 4:3; portrait: fit over a blurred copy of itself
        band=(f"[a]split[p][q];[p]scale=1080:810:force_original_aspect_ratio=increase,crop=1080:810,gblur=sigma=24,eq=brightness=-0.15[pb];"
              f"[q]scale=1080:810:force_original_aspect_ratio=decrease,scale=2160:-2:flags=lanczos,{z}[pz];"
              f"[pb]scale=1080:810[pb2];[pb2][pz]overlay=(W-w)/2:(H-h)/2,setsar=1,unsharp=5:5:0.5:5:5:0[band];") if e["src"] in ("p173","p180") else \
             (f"[a]scale=-2:810:flags=lanczos,crop=1080:810,scale=2160:-2:flags=lanczos,{z},unsharp=5:5:0.5:5:5:0,setsar=1[band];")
    bg="[b]scale=-2:1920,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.12:saturation=1.2,setsar=1,fps=30[bg]"
    subprocess.run(["ffmpeg","-v","error","-y",*inp,"-filter_complex",head+band+bg,
        "-map","[band]","-frames:v",str(n),*ENC,"-crf","14",f"seg/band_{i:02d}.mp4",
        "-map","[bg]","-frames:v",str(n),*ENC,"-crf","22",f"seg/bg_{i:02d}.mp4"],check=True)
    L1.write(f"file 'band_{i:02d}.mp4'\n");L2.write(f"file 'bg_{i:02d}.mp4'\n");e["frames"]=n;e["out_f"]=out_f;out_f+=n
L1.close();L2.close()
for kind in ("band","bg"):
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"seg/{kind}.txt","-c","copy",f"edit/assets/{kind}.mp4"],check=True)
json.dump(edl,open("edl_final.json","w"),indent=0);print("frames",out_f)
