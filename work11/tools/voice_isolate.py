# Voice isolation with DeepFilterNet3 (github.com/Rikorose/DeepFilterNet, MIT/Apache-2.0; model zip from
# raw.githubusercontent.com/Rikorose/DeepFilterNet/main/models/DeepFilterNet3.zip). Run with a venv that holds only
# deepfilternet + deepfilterlib (+ loguru, appdirs) on top of the system torch. torchaudio is used only by DF's file I/O,
# which this script replaces, so a stub stands in for it.
# The network is built from config.ini and its weights are loaded HERE with torch.load(weights_only=True): tensors only,
# no pickled code runs (DF's own checkpoint loader is not used).
# Usage: <venv>/bin/python -I tools/voice_isolate.py MODEL_DIR IN.wav OUT.wav [atten_lim_db]
import os, sys, types
for name in ["torchaudio", "torchaudio.backend", "torchaudio.backend.common", "torchaudio.functional", "torchaudio.transforms",
             "torchaudio.compliance", "torchaudio.compliance.kaldi"]:
    m = types.ModuleType(name); m.__path__ = []; sys.modules[name] = m
sys.modules["torchaudio"].__version__ = "0.0-stub"
sys.modules["torchaudio.backend.common"].AudioMetaData = object
def _no_resample(*a, **k): raise RuntimeError("input must already be at the model rate (48 kHz)")
sys.modules["torchaudio.compliance.kaldi"].resample_waveform = _no_resample
sys.modules["torchaudio.functional"].resample = _no_resample
import numpy as np, soundfile as sf, torch
from df.enhance import enhance, init_df

base, inp, out = sys.argv[1:4]; lim = float(sys.argv[4]) if len(sys.argv) > 4 else None
model, state, _ = init_df(base, log_level="ERROR", epoch=None)          # architecture only, no checkpoint read
sd = torch.load(os.path.join(base, "checkpoints", "model_120.ckpt.best"), map_location="cpu", weights_only=True)
sd = {k.replace("clc", "df"): v for k, v in sd.items()}                # same key rename as DF's read_cp
missing, unexpected = model.load_state_dict(sd, strict=False)
bad = [k for k in missing if not (k.endswith(".h0") or "erb_comp" in k)]
if bad or unexpected: raise SystemExit(f"checkpoint mismatch: missing {bad[:5]} unexpected {list(unexpected)[:5]}")
model.eval()
a, sr = sf.read(inp, always_2d=True)
if sr != state.sr(): raise SystemExit(f"need {state.sr()} Hz input, got {sr}")
x = torch.from_numpy(a.mean(1).astype(np.float32))[None]
with torch.no_grad():
    y = enhance(model, state, x, atten_lim_db=lim)
sf.write(out, y[0].numpy(), sr, subtype="FLOAT")
print("isolated", inp, "->", out, "sr", sr, "atten_lim_db", lim)
