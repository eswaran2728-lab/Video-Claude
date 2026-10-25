# Upscale the 368x640 WhatsApp source: FSRCNN x2 -> 736x1280, Lanczos to 1080x1920, light unsharp + mild denoise.
import cv2,subprocess,sys,numpy as np
src,dst=sys.argv[1],sys.argv[2]
sr=cv2.dnn_superres.DnnSuperResImpl_create();sr.readModel("scripts/FSRCNN_x2.pb");sr.setModel("fsrcnn",2)
W,H=1080,1920
dec=subprocess.Popen(["ffmpeg","-v","error","-i",src,"-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-",
  "-c:v","libx264","-crf","14","-preset","slow","-pix_fmt","yuv420p","-g","15",dst],stdin=subprocess.PIPE)
w,h=368,640;n=0
while True:
    b=dec.stdout.read(w*h*3)
    if len(b)<w*h*3: break
    f=np.frombuffer(b,np.uint8).reshape(h,w,3)
    f=cv2.fastNlMeansDenoisingColored(f,None,3,3,5,15)
    up=sr.upsample(f); up=cv2.resize(up,(W,H),interpolation=cv2.INTER_LANCZOS4)
    up=cv2.addWeighted(up,1.5,cv2.GaussianBlur(up,(0,0),1.4),-0.5,0)
    enc.stdin.write(up.tobytes());n+=1
enc.stdin.close();enc.wait();print("frames",n)
