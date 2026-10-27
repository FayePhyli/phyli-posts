"""manifesto v7, maximalist: layered collage on every page from her paintings, inks, photos, her mum's stones and the beetle. scattered cream serif on the dark pages, pink bold on the photo pages. 01, 05, 11 as approved."""
import sys, os, shutil; sys.path.insert(0, 'sys')
from style import *
import cv2
G = {}; exec(open('g60/build.py').read(), G)
srcf = open('g60/final.py').read(); exec(srcf[srcf.index('def big'):srcf.index('T=[None]*21')].replace('def big(', 'def gbig('), G)
grade, FIT, gbig, IV = G['grade'], G['F'], G['gbig'], G['IV']
OUT = 'send/manifesto/v7'; os.makedirs(OUT, exist_ok=True)
INKC = (28, 22, 26); CREAM = (244, 236, 214); SILVER = (206, 200, 212); PLUM = (40, 22, 38); PLUMQ = (150, 130, 150); PINK = '#F3C6E3'; PINKD = (201, 106, 168); PERI = (58, 62, 138); AUB = (70, 40, 60); N = 12
def inkmask(name): return Image.open(f'ink/masks/{name}.png').convert('L') if os.path.exists(f'ink/masks/{name}.png') else Image.open(f'fp/web/{name}_a.png').convert('L')
def load(p, focus=(.5, .5), zoom=1.0): return FIT(np.array(Image.open(p).convert('RGB')).astype(float), focus, zoom)
def finish(a, grain=9, vig=.28, seed=1):
    rs = np.random.RandomState(seed); a = a + rs.randn(H, W, 1) * grain
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2); v = 1 - vig * np.clip(r - .55, 0, 1) / .9
    return np.clip(a * v[..., None], 0, 255)
def dark(painting, zoom=1.3, mix=.45, seed=4): a = load(f'g30/src/{painting}.jpg', (.5, .5), zoom); a = a * mix + np.array(PLUM, float) * (1 - mix + .05); return finish(a, 9, .3, seed)
def bwgrade(a):
    g = a.mean(2); g = np.clip((g - 110) * 1.2 + 118, 0, 255); a = np.stack([g, g, g], 2); a = a * np.array([1.0, .97, 1.03]) + np.array([14, 6, 22.]) * (1 - g[..., None] / 255)
    bl = cv2.GaussianBlur(a, (0, 0), 22); return a * .82 + np.clip(bl - 110, 0, 255) * .35
def mask_on(im, m, w, x, y, col, op=1.0):
    s_ = w / m.size[0]; a = m.resize((int(m.size[0]*s_), int(m.size[1]*s_)), Image.LANCZOS).point(lambda v: int(v*op)); im.paste(Image.new('RGB', a.size, col), (int(x), int(y)), a)
def mask_fill(im, m, w, x, y, photo, tone=.6, op=.95, focus=(.5, .4)):
    s_ = w / m.size[0]; a = m.resize((int(m.size[0]*s_), int(m.size[1]*s_)), Image.LANCZOS).point(lambda v: int(v*op))
    f = load(photo, focus); f = cv2.resize(f, a.size); mn = f.mean(); f = np.clip((f - mn) * 1.3 + mn * tone, 0, 255); im.paste(pil(f), (int(x), int(y)), a)
def cutout(im, name, w, x, y, rot=0, op=1.0, shadow=True):
    """a cut-out object (beetle, stone, her) pasted as a collage piece with a soft shadow"""
    c = Image.open(f'sys/cut/{name}.png').convert('RGBA'); s_ = w / c.size[0]; c = c.resize((int(c.size[0]*s_), int(c.size[1]*s_)), Image.LANCZOS)
    if rot: c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
    if shadow:
        sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); sh.paste((20, 10, 20, 150), (0, 0), c.split()[-1]); sh = sh.filter(ImageFilter.GaussianBlur(14)); im.paste(sh, (int(x) + 10, int(y) + 16), sh)
    if op < 1: c.putalpha(c.split()[-1].point(lambda v: int(v * op)))
    im.paste(c, (int(x), int(y)), c)
def strip(im, photo, y0, h, x0=0, x1=W, focus=(.5, .5), zoom=1.0, mix=1.0, crop=None):
    a = np.array(Image.open(photo).convert('RGB')).astype(float); a = a[crop[1]:crop[3], crop[0]:crop[2]] if crop else a; a = FIT(a, focus, zoom); a = cv2.resize(a, (x1 - x0, h)); a = a * mix + np.array(PLUM, float) * (1 - mix); im.paste(pil(a), (x0, y0))
def scattered(im, lines, size, y0, col, x0=60, x1=W - 60, lh=1.15, kind='serif'):
    d = ImageDraw.Draw(im); f = F(kind, size); y = y0
    for ln in lines:
        ws = ln.split(); tw = [d.textlength(w, font=f) for w in ws]
        if len(ws) == 1: d.text((x0, y), ws[0], font=f, fill=col)
        else:
            gap = (x1 - x0 - sum(tw)) / (len(ws) - 1); x = x0
            for w, t in zip(ws, tw): d.text((x, y), w, font=f, fill=col); x += t + gap
        y += size * lh
    return y
def numb(im, i, col): spaced(ImageDraw.Draw(im), (W - 72, H - 84), f'{i:02d} / {N:02d}', F('mono', 15), col, .18, 'r')
def chap(im, t, col): spaced(ImageDraw.Draw(im), (72, 92), t.upper(), F('mono', 16), col, .36)
pages = {}

# 01 cover, 05 Phyli, 11 video: as approved
pages[1] = Image.open('send/manifesto/v6/Manifesto_01.jpg'); pages[5] = Image.open('send/manifesto/v6/Manifesto_05.jpg'); pages[11] = Image.open('send/manifesto/v6/Manifesto_11.jpg'); shutil.copy('send/manifesto/v6/Manifesto_11_video.mp4', f'{OUT}/Manifesto_11_video.mp4')

# 02 ugly · dark painting, the scales as a torn strip, the beetle small, the words scattered
im = pil(dark('art5', 1.3, .45, 2)); strip(im, 'g30/src/scales.png', 1010, 340, 0, W, (.5, .5), 1.0, .55, crop=(19, 421, 1162, 1437))
cutout(im, 'beetle', 170, W - 72 - 170, 60, rot=-18); chap(im, 'i  ·  who', PLUMQ)
text(im, "I don't know about you, but my experience of learning about business has been", 'serif', 30, 72, 300, col=SILVER, maxw=880, align='l', lh=1.3)
y = text(im, "pretty\nf*king ugly", 'serif', 118, 72, 400, col=CREAM, maxw=936, align='l', lh=1.0)
y = text(im, "the greys, the oranges, the fonts, the tone, one more list of things to implement before Monday", 'italic', 30, 72, y + 40, col=SILVER, maxw=760, align='l', lh=1.3)
text(im, "every business book I was ever given looked like a tax return", 'serif', 30, 72, 1060, col=CREAM, maxw=860, align='l', lh=1.3); numb(im, 2, PLUMQ); pages[2] = im

# 03 womb · the tiger in silver on her painting, words edge to edge (the one she loved)
im = pil(dark('art5', 1.3, .45, 4)); mask_on(im, inkmask('IMG_4685'), 900, W / 2 - 450, H / 2 - 420, SILVER, .55)
y = scattered(im, ["I wanted a theory", "of the organisation", "with a womb,", "a nervous system", "and a backbone"], 96, 300, CREAM, lh=1.12)
text(im, "a business is not a machine to be extracted from, she is a living thing, she has seasons, she has moods, she heals", 'italic', 30, 72, y + 60, col=SILVER, maxw=760, align='l', lh=1.3)
cutout(im, 'amethyst', 220, 72, H - 330, rot=12); numb(im, 3, PLUMQ); pages[3] = im

# 04 behind the founder · the 3D page as approved, with the carnelian sitting on the wall
im = Image.open('send/manifesto/v6/Manifesto_04.jpg').convert('RGB'); cutout(im, 'carnelian', 190, W - 72 - 190, 640, rot=8); pages[4] = im

# 06 the book · the brocade, the beetle on the fabric like a jewel, the horse in silver, words scattered
a = load('g30/src/mum0.jpg', (.5, .5), 1.25) * .6 + np.array(PLUM, float) * .22; a = finish(a, 7, .32, 6); im = pil(a)
mask_on(im, inkmask('IMG_1636'), 520, W - 72 - 520, H - 640, SILVER, .5); cutout(im, 'beetle', 260, 72, H - 420, rot=22)
chap(im, 'ii  ·  the claim', PLUMQ)
y = scattered(im, ["the most beautiful", "business book", "in the world"], 92, 300, CREAM, lh=1.08)
y = text(im, "pages that open out, lift and unfold the way the books we loved as children did, made from couture fabric by masters of paper, leather and binding", 'serif', 30, 72, y + 50, col=CREAM, maxw=820, align='l', lh=1.4)
text(im, "a book you keep, and hand down", 'italic', 32, 72, y + 30, col=SILVER, maxw=820, align='l', lh=1.3); numb(im, 6, PLUMQ); pages[6] = im

# 07 the dream · split: the rose painting top, plum band with her headscarf photo square inside the words, the geode
a = np.zeros((H, W, 3)); top = load('g30/src/art3.jpg', (.5, .4), 1.1) * .85; a[:420] = top[:420]; a[420:] = np.array(PLUM, float); a = finish(a, 8, .25, 7); im = pil(a)
sq = bwgrade(load('g30/src/faye20.jpg', (.72, .4), 1.15)); sq = cv2.resize(sq, (340, 340)); im.paste(pil(sq), (W - 72 - 340, 560))
text(im, "my dream is to launch her in an art gallery, the collectors' volumes numbered and bound by hand, MoMA's bookshop, Vogue", 'italic', 28, 72, 460, col=SILVER, maxw=580, align='l', lh=1.3)
y = scattered(im, ["for the founder", "who consults", "the Universe,"], 74, 600, CREAM, x1=W - 72 - 360, lh=1.1)
y = scattered(im, ["and still has to explain", "the numbers to her CFO"], 74, y + 10, CREAM, lh=1.1)
cutout(im, 'carnelian', 180, 72, H - 400, rot=-10); numb(im, 7, PLUMQ); pages[7] = im

# 08 wisdom · her b&w with the grade, a strip of her pastel across the foot, the eye ink in silver, pink italic
a = bwgrade(load('g30/src/faye20.jpg', (.72, .4), 1.15)); yy = np.arange(H)[:, None, None]; a = a * (1 - np.clip((yy - 620) / 260.0, 0, 1) * .62); a = finish(a, 10, .2, 8)
a = gbig(a, ['because the women', 'building thoughtful', 'companies deserve'], PINK, 78, y=680, lh=1.0, glow='#B48CF0', ga=.6, shadow=.45); im = pil(a)
strip(im, 'g30/src/p05.jpg', H - 150, 150, 0, W, (.5, .5), 1.3, .85); mask_on(im, inkmask('IMG_1631'), 300, 60, 120, SILVER, .6)
text(im, "wisdom that doesn't shout", 'italic', 44, 72, 950, col=IVORY, maxw=900, align='c', lh=1.1)
text(im, "because I needed it and couldn't find it, because this has felt channelled for a long time, and I'd rather be the hands than argue with it", 'serif', 27, 72, 1050, col=(226, 216, 222), maxw=820, align='c', lh=1.34); numb(im, 8, IVORY); pages[8] = im

# 09 daughter · the pink painting sunk to plum, the root flower in white, the carnelian, words scattered
im = pil(dark('art91', 1.1, .5, 9)); mask_on(im, inkmask('rootflower'), 320, W - 72 - 320, H - 780, (236, 226, 232), .9)
chap(im, 'iii  ·  why', PLUMQ)
text(im, "and because one day my daughter will ask", 'serif', 32, 72, 330, col=SILVER, maxw=640, align='l', lh=1.3)
y = scattered(im, ["what I made", "with my life"], 108, 420, CREAM, x1=W - 72 - 300, lh=1.05)
text(im, "I want the answer to be beautiful", 'italic', 34, 72, y + 50, col=CREAM, maxw=640, align='l', lh=1.3)
cutout(im, 'carnelian', 230, 72, H - 360, rot=-6); numb(im, 9, PLUMQ); pages[9] = im

# 10 truth care craft · the split page (her top, watercolour below, plum band, the horse across the seam)
top = bwgrade(load('g30/src/faye51.jpg', (.5, .3), 1.1)); bot = load('g30/src/art87.jpg', (.5, .6), 1.2) * .8
a = np.zeros((H, W, 3)); a[:560] = top[:560]; a[560:900] = np.array(PLUM, float); a[900:] = bot[900:]; a = finish(a, 8, .22, 7); im = pil(a)
y = scattered(im, ["I care about", "truth, care, craft,", "and work that outlives", "the week it was posted in"], 58, 590, CREAM, lh=1.22)
mask_fill(im, inkmask('IMG_1636'), 420, W - 72 - 420, 760, 'g30/src/faye20.jpg', .5, focus=(.7, .4))
text(im, "not hacks, not hustle, not being everywhere", 'italic', 30, 72, 1180, col=CREAM, maxw=600, align='l', lh=1.3); numb(im, 10, CREAM); pages[10] = im

# 12 stay · her pastel paper with the brocade faint under it, the three lines scattered, stay, the fairy filled, the amethyst
a = load('g30/src/p10.jpg', (.5, .45), 1.7) * .55 + np.array(IVORY, float) * .45; br = load('g30/src/mum0.jpg', (.5, .5), 1.2).mean(2, keepdims=True).repeat(3, 2); a = a * .84 + br * .16; a = finish(a, 7, .22, 12); im = pil(a)
chap(im, 'iv  ·  for you', PERI)
y = text(im, "if you're the one who remembers, decides, follows up and fixes everything\n\nif you built something out of taste and now spend your days defending it with numbers\n\nif your supply chain runs like clockwork and you still can't take a week off", 'serif', 31, 72, 260, col=INKC, maxw=800, align='l', lh=1.4)
y = text(im, "stay", 'display', 130, 72, y + 30, col=PERI, maxw=900, align='l', lh=1.0)
y = text(im, "and if you're here because you love me, being here is support, and I feel it", 'italic', 30, 72, y + 24, col=QUIET, maxw=640, align='l', lh=1.3)
y = text(im, "thank you for watching\nme do the thing", 'display', 50, 72, y + 26, col=INKC, maxw=640, align='l', lh=1.04); dot(im, 86, y + 44)
fairy = Image.open('sys/week1/fairy/fairy_mask.png').convert('L'); mask_fill(im, fairy, 230, W - 72 - 230, H - 460, 'g30/src/art84.jpg', .5)
cutout(im, 'amethyst', 200, W - 72 - 420, H - 240, rot=10); numb(im, 12, QUIET); pages[12] = im

for i in range(1, 13): pages[i].save(f'{OUT}/Manifesto_{i:02d}.jpg', quality=93)
tiles = [pages[i].resize((270, 338)) for i in range(1, 13)]
Sh = Image.new('RGB', (4 * 270, 3 * 338), (30, 30, 30))
for i, t in enumerate(tiles): Sh.paste(t, ((i % 4) * 270, (i // 4) * 338))
Sh.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
