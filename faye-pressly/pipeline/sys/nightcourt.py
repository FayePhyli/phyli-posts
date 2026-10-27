"""the Night Court carousel. cover: ivory paper, her ink fairy with the pastel showing through. inside: her pastel wash, periwinkle headline, aubergine body, fairy once on the last slide."""
import sys, os; sys.path.insert(0, 'sys')
from style import *
import cv2
OUT = 'sys/week1/nightcourt'; os.makedirs(OUT, exist_ok=True)
PERI = (58, 62, 138); AUB = (70, 40, 60); AUBQ = (118, 92, 108)
fairy = Image.open('sys/week1/fairy/fairy_mask.png').convert('L')
WASHES = ['IMG_7457', 'IMG_7450', 'IMG_7461', 'IMG_7452', 'IMG_7453', 'IMG_7454', 'IMG_7451']

def wash(name, crop=(0.10, 0.10, 0.90, 0.90)):
    im = Image.open(f'art/new/{name}.jpg'); W0, H0 = im.size
    im = im.crop((int(crop[0]*W0), int(crop[1]*H0), int(crop[2]*W0), int(crop[3]*H0)))
    a = fit(np.asarray(im).astype(np.float32), W, H)
    m = a.reshape(-1, 3).mean(0); target = np.array([226, 196, 206], np.float32); a = np.clip(a * (target / m), 0, 255)   # lamp off
    b = a.copy(); b[..., 2] = np.clip(b[..., 2] * 1.144, 0, 255); b[..., 0] = np.clip(b[..., 0] * 0.96, 0, 255)         # pushed lilac
    return pil(b * 0.8 + np.array(IVORY, np.float32) * 0.2)                                                             # lifted 20%

def fairy_layer(h, fill):
    """fill: RGB tuple or a PIL image to show through the ink"""
    a = fairy.copy(); s = h / a.size[1]; a = a.resize((int(a.size[0]*s), int(a.size[1]*s)), Image.LANCZOS)
    if isinstance(fill, tuple): layer = Image.new('RGB', a.size, fill)
    else:
        f = fit(np.asarray(fill).astype(np.float32), a.size[0], a.size[1]); m = f.mean()
        f = (f - m) * 1.35 + m * 0.62                       # darker, more contrast, so the ink still reads as ink
        layer = pil(f)
    return layer, a

def paper():
    a = np.ones((H, W, 3), np.float32) * np.array(IVORY, np.float32); rs = np.random.RandomState(7); a += rs.randn(H, W, 1) * 2.4; return pil(a)

def label(im, t): spaced(ImageDraw.Draw(im), (W/2, 96), t, F('mono', 16), AUBQ, .3, 'c')
def numb(im, i, n): spaced(ImageDraw.Draw(im), (W - 72, H - 84), f'{i:02d} / {n:02d}', F('mono', 15), AUBQ, .18, 'r')
def head(im, t, y, size=68): return text(im, t, 'display', size, 72, y, col=PERI, maxw=930, align='c', lh=1.04)
def body(im, t, y, size=36): return text(im, t, 'serif', size, 72, y, col=AUB, maxw=860, align='c', lh=1.36)
def aside(im, t, y, size=32): return text(im, t, 'italic', size, 72, y, col=AUB, maxw=860, align='c', lh=1.3)
def measure(fn): return fn(Image.new('RGB', (W, H)), 0)
def centred(im, fn, dy=-30): h = measure(fn); fn(im, (H - h) / 2 + dy); return im

N = 7; out = []
# ---------- 01 cover, two fills ----------
def cover(fill, name):
    im = paper(); layer, a = fairy_layer(600, fill)
    im.paste(layer, (int(W/2 - a.size[0]/2), 150), a)
    label(im, 'faye pressly  ·  a note on book six')
    y = head(im, "the Night Court is\nbetter run than\nyour company", 800, 74)
    y = aside(im, "a founder's reading of books one to five,\nbefore six arrives tomorrow", y + 34, 28)
    dot(im, W/2, y + 54); numb(im, 1, N); im.save(f'{OUT}/{name}', quality=93); return im
c1 = cover(Image.open('art/new/IMG_7465.jpg'), 'Cover_scribble.jpg'); c2 = c1
out.append(c1)

# ---------- 02–06 ----------
def slide(i, fn, with_fairy=False):
    im = wash(WASHES[i - 1])
    if with_fairy:
        layer, a = fairy_layer(300, AUB); im.paste(layer, (W - 72 - a.size[0], H - 150 - a.size[1]), a)
    im = centred(im, fn); label(im, 'faye pressly  ·  a note on book six'); numb(im, i, N); return im
def s2(im, y):
    y = head(im, "Tamlin ran the Spring Court\nthe way most founders\nrun year three", y)
    return body(im, "everything through him\nnobody allowed out\nshe left", y + 40)
def s2b(im, y):
    y = head(im, "if the whole kingdom\nruns on your memory", y)
    y = body(im, "you're not the chosen one", y + 40)
    return head(im, "you're the operating system", y + 24, 56)
def s3(im, y):
    y = head(im, "Rhysand ran the Night Court\nlike a living thing", y)
    y = body(im, "a general, a spymaster, an emissary, a second\npeople who argue with him in his own house", y + 40)
    return aside(im, "the inner circle isn't a found family...\nit's a leadership team that happens\nto love each other", y + 30)
def s4(im, y):
    y = head(im, "Velaris stayed hidden\nfor five thousand years", y)
    y = body(im, "and thrived", y + 40)
    y = body(im, "the inside of your company is your Velaris", y + 30)
    return aside(im, "the part nobody sees, the part that keeps her alive\nI've spent twenty years in there", y + 26)
def s5(im, y):
    y = head(im, "Feyre paints", y, 96)
    return body(im, "she also runs a court\nnobody made her choose", y + 44)
def s6(im, y):
    y = head(im, "my name means fairy", y, 72)
    y = body(im, "I was always going to end up here", y + 40)
    y = aside(im, "twenty years inside companies, learning what keeps her alive\nnow I'm writing it down... twelve volumes", y + 30)
    y = body(im, "book six is out tomorrow\nvolume one of mine is on its way", y + 34)
    dot(im, W/2, y + 54); return y + 70
for i, fn in zip(range(2, 8), (s2, s2b, s3, s4, s5, s6)): out.append(slide(i, fn, with_fairy=(i == 7)))
for i, im in enumerate(out): im.save(f'{OUT}/NightCourt_{i+1:02d}.jpg', quality=93)
tiles = [im.resize((360, 450)) for im in out]
S = Image.new('RGB', (4 * 360, 2 * 450), (30, 30, 30))
for i, t in enumerate(tiles): S.paste(t, ((i % 4) * 360, (i // 4) * 450))
S.save(f'{OUT}/sheet.jpg', quality=88)
cs = Image.new('RGB', (2 * 540, 675), (30, 30, 30)); cs.paste(c1.resize((540, 675)), (0, 0)); cs.paste(c2.resize((540, 675)), (540, 0)); cs.save(f'{OUT}/covers.jpg', quality=88)
print('ok')
