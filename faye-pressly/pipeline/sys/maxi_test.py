"""two pages with the simonarose / lillyalbaab devices applied to her own material: scattered justified serif across a dark painting with silver ink; a split-image page with the words in the band between."""
import sys, os; sys.path.insert(0, 'sys')
from style import *
import cv2
G = {}; exec(open('g60/build.py').read(), G)
srcf = open('g60/final.py').read(); exec(srcf[srcf.index('def big'):srcf.index('T=[None]*21')].replace('def big(', 'def gbig('), G)
grade, FIT, gbig, IV = G['grade'], G['F'], G['gbig'], G['IV']
OUT = 'send/manifesto/maxi'; os.makedirs(OUT, exist_ok=True)
INKC = (28, 22, 26); CREAM = (244, 236, 214); SILVER = (206, 200, 212); PLUMQ = (150, 130, 150)
def inkmask(name): return Image.open(f'ink/masks/{name}.png').convert('L') if os.path.exists(f'ink/masks/{name}.png') else Image.open(f'fp/web/{name}_a.png').convert('L')
def load(p, focus=(.5, .5), zoom=1.0): return FIT(np.array(Image.open(p).convert('RGB')).astype(float), focus, zoom)
def finish(a, grain=9, vig=.28, seed=1):
    rs = np.random.RandomState(seed); a = a + rs.randn(H, W, 1) * grain
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2); v = 1 - vig * np.clip(r - .55, 0, 1) / .9
    return np.clip(a * v[..., None], 0, 255)
def mask_fill(im, m, w, x, y, photo, tone=.6, op=.95, focus=(.5, .4)):
    s_ = w / m.size[0]; a = m.resize((int(m.size[0]*s_), int(m.size[1]*s_)), Image.LANCZOS).point(lambda v: int(v*op))
    f = load(photo, focus); f = cv2.resize(f, a.size); mn = f.mean(); f = np.clip((f - mn) * 1.3 + mn * tone, 0, 255); im.paste(pil(f), (int(x), int(y)), a)
def mask_on(im, m, w, x, y, col, op=1.0):
    s_ = w / m.size[0]; a = m.resize((int(m.size[0]*s_), int(m.size[1]*s_)), Image.LANCZOS).point(lambda v: int(v*op)); im.paste(Image.new('RGB', a.size, col), (int(x), int(y)), a)
def scattered(im, lines, size, y0, col, x0=60, x1=W - 60, lh=1.15, kind='serif'):
    """each line justified edge to edge, the words pushed apart: the device from the references"""
    d = ImageDraw.Draw(im); f = F(kind, size); y = y0
    for ln in lines:
        ws = ln.split(); tw = [d.textlength(w, font=f) for w in ws]
        if len(ws) == 1: d.text((x0, y), ws[0], font=f, fill=col)
        else:
            gap = (x1 - x0 - sum(tw)) / (len(ws) - 1); x = x0
            for w, t in zip(ws, tw): d.text((x, y), w, font=f, fill=col); x += t + gap
        y += size * lh
    return y
def numb(im, i, col): spaced(ImageDraw.Draw(im), (W - 72, H - 84), f'{i:02d} / 12', F('mono', 15), col, .18, 'r')

# A · the womb, maximal: her dark painting sunk to plum, the tiger in silver behind, the words scattered edge to edge in cream serif
a = load('g30/src/art5.jpg', (.5, .5), 1.3); a = a * .45 + np.array([40, 22, 38.]) * .5; a = finish(a, 9, .3, 4); im = pil(a)
mask_on(im, inkmask('IMG_4685'), 900, W / 2 - 450, H / 2 - 420, SILVER, .55)                       # the tiger, silver, behind the words
y = scattered(im, ["I wanted a theory", "of the organisation", "with a womb,", "a nervous system", "and a backbone"], 96, 300, CREAM, lh=1.12)
text(im, "a business is not a machine to be extracted from, she is a living thing, she has seasons, she has moods, she heals", 'italic', 30, 72, y + 60, col=SILVER, maxw=760, align='l', lh=1.3)
numb(im, 3, PLUMQ); im.save(f'{OUT}/M03.jpg', quality=93)

# B · truth, care, craft as a split page: her photo top, a crop of her painting bottom, the words in the band between, the horse crossing the seam
top = load('g30/src/faye51.jpg', (.5, .3), 1.1); g = top.mean(2); g = np.clip((g - 110) * 1.2 + 118, 0, 255); top = np.stack([g, g, g], 2) * np.array([1.0, .97, 1.03]) + np.array([14, 6, 22.]) * (1 - g[..., None] / 255)
bot = load('g30/src/art87.jpg', (.5, .6), 1.2) * .8
a = np.zeros((H, W, 3)); a[:560] = top[:560]; a[560:900] = np.array([40, 22, 38.]); a[900:] = bot[900:]; a = finish(a, 8, .22, 7); im = pil(a)
y = scattered(im, ["I care about", "truth, care, craft,", "and work that outlives", "the week it was posted in"], 58, 590, CREAM, lh=1.22)
mask_fill(im, inkmask('IMG_1636'), 420, W - 72 - 420, 760, 'g30/src/faye20.jpg', .5, focus=(.7, .4))        # the horse across the seam, filled with her
text(im, "not hacks, not hustle, not being everywhere", 'italic', 30, 72, 1180, col=CREAM, maxw=600, align='l', lh=1.3)
numb(im, 10, CREAM); im.save(f'{OUT}/M10.jpg', quality=93)
S = Image.new('RGB', (2 * 540 + 20, 675), (30, 30, 30)); S.paste(Image.open(f'{OUT}/M03.jpg').resize((540, 675)), (0, 0)); S.paste(Image.open(f'{OUT}/M10.jpg').resize((540, 675)), (560, 0)); S.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
