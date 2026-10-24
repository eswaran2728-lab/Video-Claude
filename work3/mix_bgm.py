"""Build a ducked BGM bed for the edit: loop the chosen candidate to the film length, duck it under the voice."""
import subprocess,sys,json
cand=sys.argv[1];out="edit/assets/bgm_bed.wav";TOTAL=62.233
# voice timeline as laid out in index.html: hook snippets + body
subprocess.run(["ffmpeg","-v","error","-y",
  "-i","edit/assets/main_audio.wav","-i","edit/assets/body.wav",
  "-filter_complex",
  "[0:a]atrim=55.55:56.87,asetpts=PTS-STARTPTS,adelay=120|120[h1];"
  "[0:a]atrim=39.13:41.35,asetpts=PTS-STARTPTS,adelay=1300|1300[h2];"
  "[1:a]adelay=3500|3500[b];"
  f"[h1][h2][b]amix=inputs=3:normalize=0,apad,atrim=0:{TOTAL}[v]",
  "-map","[v]","-ac","2","-ar","48000","bgm/voice_timeline.wav"],check=True)
# loop the 30 s candidate with crossfades, normalise, fade, then duck with the voice as sidechain
subprocess.run(["ffmpeg","-v","error","-y","-i",cand,"-i",cand,"-i",cand,
  "-filter_complex",
  "[0:a][1:a]acrossfade=d=3:c1=tri:c2=tri[ab];[ab][2:a]acrossfade=d=3:c1=tri:c2=tri,"
  f"aresample=48000,aformat=channel_layouts=stereo,atrim=0:{TOTAL},loudnorm=I=-20:TP=-2:LRA=7,"
  f"afade=t=in:d=1.2,afade=t=out:st={TOTAL-2.5}:d=2.5[m]",
  "-map","[m]","bgm/bed_raw.wav"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","bgm/bed_raw.wav","-i","bgm/voice_timeline.wav",
  "-filter_complex","[1:a]asplit=1[sc];[0:a][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=450:makeup=1[d]",
  "-map","[d]",out],check=True)
print("wrote",out)
