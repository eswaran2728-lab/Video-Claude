import torch,numpy as np,soundfile as sf,time
from transformers import AutoProcessor, MusicgenForConditionalGeneration
torch.set_num_threads(4);torch.manual_seed(7)
proc=AutoProcessor.from_pretrained("facebook/musicgen-medium")
model=MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")
prompts=[
 "emotional Tamil devotional instrumental, solo Carnatic veena melody with soft tanpura drone and gentle mridangam, slow, heartfelt, reverent, clean studio recording, 72 bpm",
 "calm South Indian temple background music, bansuri flute lead, soft strings pad, tanpura drone, light tabla, sincere and hopeful, clean mix, 80 bpm",
]
sr=model.config.audio_encoder.sampling_rate
for k,p in enumerate(prompts):
    t=time.time()
    inp=proc(text=[p],padding=True,return_tensors="pt")
    with torch.no_grad(): a=model.generate(**inp,do_sample=True,guidance_scale=3.5,max_new_tokens=1500)
    sf.write(f"bgm/cand{k+2}.wav",a[0,0].numpy().astype(np.float32),sr);print(k+2,round(time.time()-t),"s",flush=True)
