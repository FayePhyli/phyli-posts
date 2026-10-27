"""one carousel slide, three ways, on Faye's own pastel wash. A: wash as shot. B: lifted towards ivory, grain kept. C: lifted + her ink fairy small."""
import sys, os; sys.path.insert(0, 'sys')
from style import *
import cv2
OUT = 'sys/week1/fairy'; os.makedirs(OUT, exist_ok=True)

fairy = Image.open(f'{OUT}/fairy_mask.png').convert('L')

# ---- the wash ----
def wash(name, lift=0.0, crop=(0.02, 0.02, 0.98, 0.98)):
    im = Image.open(f'art/new/{name}.jpg'); W0, H0 = im.size
    im = im.crop((int(crop[0]*W0), int(crop[1]*H0), int(crop[2]*W0), int(crop[3]*H0)))
    a = np.asarray(fit(np.asarray(im).astype(np.float32), W, H)).astype(np.float32)
    # gentle: keep the paper grain, lift towards ivory by `lift`
    a = a * (1 - lift) + np.array(IVORY, np.float32) * lift
    if lift: a = a * np.array([0.985, 0.995, 1.03], np.float32)   # take the warm lamp cast off
    return pil(a)

def put_fairy(im, w, cx, cy, op=.9):
    a = fairy.copy(); s = w / a.size[0]; a = a.resize((int(a.size[0]*s), int(a.size[1]*s)), Image.LANCZOS).point(lambda v: int(v*op))
    im = im.copy(); im.paste(Image.new('RGB', a.size, INK), (int(cx - a.size[0]/2), int(cy - a.size[1]/2)), a); return im

def words(im, tag):
    d = ImageDraw.Draw(im)
    spaced(d, (W/2, 110), 'faye pressly  ·  volume I', F('mono', 17), INK, .3, 'c')
    y = text(im, "my name means\nlittle fairy", 'display', 96, 72, 430, col=INK, maxw=940, align='c', lh=1.0)
    y = text(im, "I spent twenty years running\nother people's operations", 'serif', 34, 72, y + 60, col=INK, maxw=900, align='c', lh=1.3)
    text(im, "someone had to", 'italic', 34, 72, y + 48, col=INK, maxw=900, align='c')
    spaced(d, (W - 72, H - 84), '01 / 06', F('mono', 15), INK, .18, 'r')
    return im

A = words(wash('IMG_7457', 0.0), 'A')
B = words(wash('IMG_7457', 0.35), 'B')
C = words(put_fairy(wash('IMG_7452', 0.35), 200, W - 210, H - 300), 'C')
for k, im in zip('ABC', (A, B, C)): im.save(f'{OUT}/slide_{k}.jpg', quality=93)
sheet = Image.new('RGB', (3 * 540 + 40, 675), (30, 30, 30))
for i, im in enumerate((A, B, C)): sheet.paste(im.resize((540, 675)), (i * 560, 0))
sheet.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
