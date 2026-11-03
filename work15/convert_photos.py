# Creator's photos (HEIC/JPG from Drive, src/drive/) -> upright sRGB JPEGs, long side 2000 px, in src/photos/ (originals untouched).
import os, sys, io, pillow_heif
from PIL import Image, ImageOps, ImageCms
pillow_heif.register_heif_opener(); os.makedirs("src/photos", exist_ok=True); SRGB = ImageCms.createProfile("sRGB")
for n in sorted(os.listdir("src/drive")):
    if not n.lower().endswith((".heic", ".jpg", ".jpeg")): continue
    out = "src/photos/" + os.path.splitext(n)[0] + ".jpg"
    if os.path.exists(out): continue
    im = Image.open("src/drive/" + n); icc = im.info.get("icc_profile")
    im = ImageOps.exif_transpose(im).convert("RGB")
    if icc:
        try: im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB, outputMode="RGB")
        except Exception: pass
    im.thumbnail((2000, 2000), Image.LANCZOS); im.save(out, quality=93); print(out, im.size, flush=True)
