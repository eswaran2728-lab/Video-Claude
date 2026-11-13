"""Generate instrumental cues with MusicGen-small (CPU). usage: musicgen.py"""
import os, sys, torch, numpy as np, soundfile as sf
from transformers import AutoProcessor, MusicgenForConditionalGeneration
os.environ.setdefault('REQUESTS_CA_BUNDLE', '/root/.ccr/ca-bundle.crt')
torch.manual_seed(7)
CUES = {
 'flute_alap': 'solo Indian bamboo flute bansuri, slow meditative alap, soft tanpura drone, warm intimate small room, no drums, no synth, gentle and sparse, 72 bpm',
 'veena_refrain': 'gentle South Indian Carnatic veena melody with soft bamboo flute answer and low tanpura drone, very light mridangam hand drum, tender folk dedication, acoustic, warm, 76 bpm',
 'drone_bed': 'low tanpura drone only, soft sustained Indian drone, calm, acoustic, no melody, no drums',
}
only = sys.argv[1:]
proc = AutoProcessor.from_pretrained('facebook/musicgen-small')
model = MusicgenForConditionalGeneration.from_pretrained('facebook/musicgen-small')
sr = model.config.audio_encoder.sampling_rate
for k, prompt in CUES.items():
    if only and k not in only: continue
    inp = proc(text=[prompt], padding=True, return_tensors='pt')
    with torch.no_grad():
        out = model.generate(**inp, do_sample=True, guidance_scale=3.5, max_new_tokens=1450)  # ~29 s
    a = out[0, 0].cpu().numpy().astype(np.float32)
    a = a / max(1e-6, np.abs(a).max()) * 0.89
    sf.write(f'audio/music/{k}.wav', a, sr)
    print(k, round(len(a) / sr, 1), 's', flush=True)
