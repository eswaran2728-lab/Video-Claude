import sys,os,cv2,torch,time
sys.path.insert(0,"/tmp/rvmdl/RobustVideoMatting")
from model import MattingNetwork
torch.set_num_threads(4)
m=MattingNetwork("resnet50").eval();m.load_state_dict(torch.load("/tmp/rvmdl/rvm_resnet50.pth",map_location="cpu"))
os.makedirs("rvm",exist_ok=True)
nf=[120,53,207,185,13,61,100,339,60,146,62,41,78,139,390,210,26,93,170,17]
cuts=set();c=0
for n in nf: cuts.add(c);c+=n
lim=int(sys.argv[1]) if len(sys.argv)>1 else 10**9
cap=cv2.VideoCapture("cut.mp4");i=0;rec=[None]*4;t0=time.time()
with torch.no_grad():
    while i<lim:
        ok,f=cap.read()
        if not ok: break
        if i in cuts: rec=[None]*4
        x=torch.from_numpy(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).permute(2,0,1).float().div(255).unsqueeze(0)
        fgr,pha,*rec=m(x,*rec,downsample_ratio=0.375)
        cv2.imwrite(f"rvm/{i:05d}.png",(pha[0,0].numpy()*255).astype("uint8"))
        i+=1
        if i%100==0: print(i,round(time.time()-t0,1),flush=True)
print("done",i,round(time.time()-t0,1))
