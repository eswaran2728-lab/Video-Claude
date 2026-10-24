import json,subprocess,os
edl=json.load(open("edl.json"));END=54.72;F=30
edl[0]["t0"]=0.0
edl[-1]["t1"]=END
os.makedirs("seg",exist_ok=True);L1=open("seg/band.txt","w");L2=open("seg/bg.txt","w")
out_f=0
for i,e in enumerate(edl):
    n=round(e["t1"]*F)-round(e["t0"]*F)
    sp=e["speed"];src_len=n/F*sp+0.2
    fc=(f"[0:v]trim=start={e['ss']}:duration={src_len:.3f},setpts=(PTS-STARTPTS)/{sp},fps={F},split[a][b];"
        "[a]crop=ih*4/3:ih,scale=1080:810:flags=lanczos,unsharp=5:5:0.6:5:5:0,setsar=1[band];"
        "[b]scale=-2:1920,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.12:saturation=1.2,setsar=1[bg]")
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"src/{e['src']}.mp4","-filter_complex",fc,
        "-map","[band]","-frames:v",str(n),"-an","-c:v","libx264","-crf","14","-preset","fast","-pix_fmt","yuv420p",f"seg/band_{i:02d}.mp4",
        "-map","[bg]","-frames:v",str(n),"-an","-c:v","libx264","-crf","22","-preset","fast","-pix_fmt","yuv420p",f"seg/bg_{i:02d}.mp4"],check=True)
    L1.write(f"file 'band_{i:02d}.mp4'\n");L2.write(f"file 'bg_{i:02d}.mp4'\n")
    e["frames"]=n;e["out_f"]=out_f;out_f+=n
L1.close();L2.close()
for kind in ("band","bg"):
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"seg/{kind}.txt","-c","copy",f"edit/assets/{kind}.mp4"],check=True)
json.dump(edl,open("edl_final.json","w"),indent=0)
print("frames",out_f,"=",out_f/F,"s")
