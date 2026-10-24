import torch,numpy as np,soundfile as sf,time
from transformers import AutoProcessor, MusicgenForConditionalGeneration
torch.set_num_threads(4)
proc=AutoProcessor.from_pretrained("facebook/musicgen-small")
model=MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
prompts=[
 "soft emotional South Indian Tamil devotional instrumental, gentle bansuri flute melody, veena, tanpura drone, light mridangam, calm reverent sincere mood, 80 bpm, warm cinematic",
 "peaceful Carnatic instrumental background music, veena and bamboo flute over tanpura drone, soft temple bells, slow tabla, heartfelt and respectful, 76 bpm",
]
sr=model.config.audio_encoder.sampling_rate
for k,p in enumerate(prompts):
    t=time.time()
    inp=proc(text=[p],padding=True,return_tensors="pt")
    with torch.no_grad(): a=model.generate(**inp,do_sample=True,guidance_scale=3.5,max_new_tokens=1500)  # ~30 s
    x=a[0,0].numpy().astype(np.float32)
    sf.write(f"bgm/cand{k}.wav",x,sr);print(k,len(x)/sr,"s",round(time.time()-t),"s",flush=True)
