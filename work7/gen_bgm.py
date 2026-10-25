# Local MusicGen bed (no third-party recordings): upbeat maker/product reel, sits under Tamil speech.
import torch,numpy as np,soundfile as sf
from transformers import AutoProcessor, MusicgenForConditionalGeneration
torch.set_num_threads(4);torch.manual_seed(21)
proc=AutoProcessor.from_pretrained("facebook/musicgen-small")
model=MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
p="upbeat modern lo-fi pop instrumental, punchy light drums, plucky synth and soft bass, positive maker workshop vibe, clean mix, no vocals, 105 bpm"
inp=proc(text=[p],padding=True,return_tensors="pt")
with torch.no_grad(): a=model.generate(**inp,do_sample=True,guidance_scale=3.5,max_new_tokens=1850)
sf.write("bgm/bed_raw.wav",a[0,0].numpy().astype(np.float32),model.config.audio_encoder.sampling_rate);print("done")
