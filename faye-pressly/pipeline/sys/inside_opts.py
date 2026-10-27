"""six treatments of the same inside slide (Tamlin), so she can pick the style for every inside slide."""
import sys, os; sys.path.insert(0, 'sys')
from style import *
import cv2
OUT = 'sys/week1/inside'; os.makedirs(OUT, exist_ok=True)
PERI = (58, 62, 138); AUB = (70, 40, 60); LILAC = (233, 222, 240); PINK = (246, 214, 224)
def load(name, crop=(0.10, 0.10, 0.90, 0.90)):
    im = Image.open(f'art/new/{name}.jpg'); W0, H0 = im.size
    im = im.crop((int(crop[0]*W0), int(crop[1]*H0), int(crop[2]*W0), int(crop[3]*H0)))
    return fit(np.asarray(im).astype(np.float32), W, H)
def wb(a, cool=1.0):
    """take the lamp off: neutralise so the paper's mean sits pink-lilac rather than salmon"""
    m = a.reshape(-1, 3).mean(0); target = np.array([226, 196, 206], np.float32)   # dusty pink, the colour the pastel is in daylight
    return np.clip(a * (target / m) ** cool, 0, 255)
def lift(a, k): return a * (1 - k) + np.array(IVORY, np.float32) * k
def sat(a, s):
    g = a.mean(2, keepdims=True); return np.clip(g + (a - g) * s, 0, 255)
def hue_lilac(a, k=.5):
    """push the wash towards lilac/periwinkle (light-summer) rather than peach"""
    b = a.copy(); b[..., 2] = np.clip(b[..., 2] * (1 + .18 * k), 0, 255); b[..., 0] = np.clip(b[..., 0] * (1 - .05 * k), 0, 255); return b
def words(im, hc, bc, ac, glow=None):
    d = ImageDraw.Draw(im)
    spaced(d, (W/2, 96), 'faye pressly  ·  a note on book six', F('mono', 16), ac, .3, 'c')
    if glow is not None:
        lay = Image.new('L', (W, H), 0); text(Image.new('RGB', (W, H)), "x", 'display', 10, 0, 0)  # warm fonts
        tmp = Image.new('RGB', (W, H), (0, 0, 0)); text(tmp, "Tamlin ran the Spring Court\nthe way most founders\nrun year three", 'display', 68, 72, 470, col=(255, 255, 255), maxw=930, align='c', lh=1.04)
        g = np.asarray(tmp.convert('L')).astype(np.float32) / 255
        g = cv2.GaussianBlur(g, (0, 0), 14) * 1.3; g = np.clip(g, 0, 1)[..., None]
        a = np.asarray(im).astype(np.float32); a = a * (1 - g * .9) + np.array(glow, np.float32) * g * .9; im = pil(a); d = ImageDraw.Draw(im)
    y = text(im, "Tamlin ran the Spring Court\nthe way most founders\nrun year three", 'display', 68, 72, 470, col=hc, maxw=930, align='c', lh=1.04)
    body = text(im, "everything through him\nnobody allowed out\nshe left", 'serif', 36, 72, y + 40, col=bc, maxw=860, align='c', lh=1.36)
    spaced(d, (W - 72, H - 84), '02 / 06', F('mono', 15), ac, .18, 'r'); return im

base = load('IMG_7450')
opts = [
    ('1  wash as shot · ivory headline',            pil(base),                          IVORY, AUB, AUB),
    ('2  lamp taken off · ivory headline',          pil(wb(base)),                      IVORY, AUB, AUB),
    ('3  lamp off, pushed lilac · ivory headline',  pil(hue_lilac(wb(base), .8)),       IVORY, AUB, AUB),
    ('4  lamp off, lifted 25% · aubergine headline', pil(lift(wb(base), .25)),          AUB, AUB, AUB),
    ('5  lamp off, lilac, lifted 20% · periwinkle', pil(lift(hue_lilac(wb(base), .8), .2)), PERI, AUB, AUB),
    ('6  lamp off, richer · ivory with pink glow',  pil(sat(wb(base), 1.25)),           IVORY, AUB, AUB, (232, 170, 196)),
]
out = []
for o in opts:
    name, im, hc, bc, ac = o[:5]; glow = o[5] if len(o) > 5 else None
    im = words(im.copy(), hc, bc, ac, glow); out.append((name, im)); im.save(f"{OUT}/opt_{name[0]}.jpg", quality=92)
S = Image.new('RGB', (3 * 400, 2 * 520), (30, 30, 30)); d = ImageDraw.Draw(S)
for i, (name, im) in enumerate(out):
    S.paste(im.resize((400, 500)), ((i % 3) * 400, (i // 3) * 520)); d.text(((i % 3) * 400 + 8, (i // 3) * 520 + 502), name, fill=(255, 255, 255), font=F('mono', 13))
S.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
