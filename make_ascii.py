"""Convert your photo into ASCII art -> ascii.txt
Usage: python make_ascii.py [photo.jpg]
(Optional) pip install rembg onnxruntime  -> removes the background for a cleaner portrait.
"""
import sys
from PIL import Image, ImageOps, ImageFilter
import numpy as np

SRC   = sys.argv[1] if len(sys.argv) > 1 else "my_photo.jpg"
COLS  = 76                       # width in characters
CROP  = (215, 25, 560, 420)      # left, top, right, bottom  (head + shoulders)
RAMP  = " .'`^,:;-~=+*xX#%@"           # light -> dark ink on a dark background

src = Image.open(SRC).convert("RGB")
try:                              # background removal (optional)
    from rembg import remove, new_session
    rgba = remove(src, session=new_session("u2netp"))
    mask = np.asarray(rgba.split()[3]) > 128
except Exception:
    mask = np.ones((src.height, src.width), bool)

gray = src.convert("L")
try:                                             # local contrast (CLAHE) if OpenCV exists
    import cv2
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(6, 6))
    g = clahe.apply(np.asarray(gray)).astype(float) / 255.0
except Exception:
    gray = ImageOps.equalize(gray)
    g = np.asarray(gray, dtype=float) / 255.0
# stretch tones using only the subject's pixels, then add edge detail (DoG)
lo, hi = np.percentile(g[mask], [3, 97])
g = np.clip((g - lo) / (hi - lo + 1e-6), 0, 1)
from PIL import ImageFilter as _F
blur1 = np.asarray(Image.fromarray((g*255).astype("uint8")).filter(_F.GaussianBlur(1)), float)/255
blur2 = np.asarray(Image.fromarray((g*255).astype("uint8")).filter(_F.GaussianBlur(5)), float)/255
g = np.clip(g + 1.2*(blur1 - blur2), 0, 1)
g = (0.08 + 0.92 * g) ** 0.85
g = np.where(mask, g, 0.0)                       # background -> blank
img = Image.fromarray((g * 255).astype("uint8")).crop(CROP)

w, h = img.size
rows = int(COLS * (h / w) * 0.5)
img = img.resize((COLS, rows), Image.LANCZOS)
a = (np.asarray(img, dtype=float) / 255.0) ** 0.8
idx = (a * (len(RAMP) - 1)).round().astype(int)
lines = ["".join(RAMP[i] for i in r).rstrip() for r in idx]
open("ascii.txt", "w").write("\n".join(lines))
print("\n".join(lines))
