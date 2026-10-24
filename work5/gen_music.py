import torch,numpy as np,soundfile as sf
from transformers import AutoProcessor, MusicgenForConditionalGeneration
torch.set_num_threads(4);torch.manual_seed(11)
p=AutoProcessor.from_pretrained("facebook/musicgen-small");m=MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
prompt="warm uplifting Tamil film style instrumental, nadaswaram-like flute melody, acoustic guitar, soft strings, gentle tabla and claps, joyful friendship and respect, major key, 84 bpm, clean mix"
inp=p(text=[prompt],return_tensors="pt")
with torch.no_grad(): a=m.generate(**inp,do_sample=True,guidance_scale=3.5,max_new_tokens=1500)
sf.write("music/temp_raw.wav",a[0,0].numpy().astype(np.float32),m.config.audio_encoder.sampling_rate);print("ok")
