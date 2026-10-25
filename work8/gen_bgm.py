# Local MusicGen bed (no third-party recordings): calm, minimal explainer groove under Tamil speech. AI placeholder.
import torch, numpy as np, soundfile as sf
from transformers import AutoProcessor, MusicgenForConditionalGeneration
torch.set_num_threads(4); torch.manual_seed(7)
proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
p = "minimal warm lo-fi instrumental, soft muted piano chords, gentle brushed drums, round soft bass, calm curious explainer mood, clean sparse mix, no vocals, 90 bpm"
inp = proc(text=[p], padding=True, return_tensors="pt")
with torch.no_grad(): a = model.generate(**inp, do_sample=True, guidance_scale=3.5, max_new_tokens=1900)
sf.write("bgm/bed_raw.wav", a[0, 0].numpy().astype(np.float32), model.config.audio_encoder.sampling_rate); print("done")
