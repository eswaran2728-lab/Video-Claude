# Generates candidate music beds locally with MusicGen (no third-party recordings).
import torch,numpy as np,soundfile as sf,time,sys
from transformers import AutoProcessor, MusicgenForConditionalGeneration
torch.set_num_threads(4);torch.manual_seed(11)
proc=AutoProcessor.from_pretrained("facebook/musicgen-medium")
model=MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")
prompts=[
 "powerful South Indian Tamil folk temple music, thavil and urumi drums, nadaswaram melody, fierce guardian deity, cinematic build, bold and majestic, clean mix, 100 bpm",
 "epic cinematic Tamil devotional trailer music, deep taiko and thavil percussion, low brass, nadaswaram lead, intense and majestic, 96 bpm",
]
sr=model.config.audio_encoder.sampling_rate
for k,p in enumerate(prompts):
    t=time.time()
    inp=proc(text=[p],padding=True,return_tensors="pt")
    with torch.no_grad(): a=model.generate(**inp,do_sample=True,guidance_scale=3.5,max_new_tokens=1150)
    sf.write(f"bgm/cand{k}.wav",a[0,0].numpy().astype(np.float32),sr);print(k,round(time.time()-t),"s",flush=True)
