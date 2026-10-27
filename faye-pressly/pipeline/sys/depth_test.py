"""three pages with depth: real surface, layers, light, grain. 02 ugly (dark), 05 Phyli (cream), 08 wisdom (b&w)."""
import sys, os; sys.path.insert(0, 'sys')
from style import *
import cv2
G = {}; exec(open('g60/build.py').read(), G)
srcf = open('g60/final.py').read(); exec(srcf[srcf.index('def big'):srcf.index('T=[None]*21')].replace('def big(', 'def gbig('), G)
grade, FIT, gbig, IV = G['grade'], G['F'], G['gbig'], G['IV']
OUT = 'send/manifesto/depth'; os.makedirs(OUT, exist_ok=True)
INKC = (28, 22, 26); PERI = (58, 62, 138); AUB = (70, 40, 60); PINK = '#F3C6E3'; PINKD = (201, 106, 168); BAR = (236, 190, 214)
def inkmask(name): return Image.open(f'ink/masks/{name}.png').convert('L') if os.path.exists(f'ink/masks/{name}.png') else Image.open(f'fp/web/{name}_a.png').convert('L')
def load(p, focus=(.5, .5), zoom=1.0): return FIT(np.array(Image.open(p).convert('RGB')).astype(float), focus, zoom)
def finish(a, grain=9, vig=.28, seed=1):
    """film grain + soft vignette over the whole page"""
    rs = np.random.RandomState(seed); a = a + rs.randn(H, W, 1) * grain
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2); v = 1 - vig * np.clip(r - .55, 0, 1) / .9
    return np.clip(a * v[..., None], 0, 255)
def light(a, cx, cy, rad, strength, col=(255, 240, 248)):
    """a soft pool of light"""
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2); g = np.clip(1 - d / rad, 0, 1) ** 2 * strength
    return a * (1 - g[..., None]) + np.array(col, float) * g[..., None]
def highlight(im, t, kind, size, x, y, col, bar, maxw=900, align='l'):
    """one line with a highlighter bar behind it"""
    d = ImageDraw.Draw(im); f = F(kind, size); tw = d.textlength(t, font=f); x0 = x if align == 'l' else W / 2 - tw / 2
    bar_im = Image.new('RGBA', (int(tw + 28), int(size * 1.05)), bar + (210,)); im.paste(bar_im, (int(x0 - 14), int(y + size * .08)), bar_im)
    d.text((x0, y), t, font=f, fill=col); return y + size * 1.3
def mask_fill(im, m, w, x, y, photo, tone=.6, op=.95):
    s_ = w / m.size[0]; a = m.resize((int(m.size[0]*s_), int(m.size[1]*s_)), Image.LANCZOS).point(lambda v: int(v*op))
    f = load(photo, (.5, .4)); f = cv2.resize(f, a.size); mn = f.mean(); f = np.clip((f - mn) * 1.3 + mn * tone, 0, 255); im.paste(pil(f), (int(x), int(y)), a)
def mask_on(im, m, w, x, y, col, op=1.0):
    s_ = w / m.size[0]; a = m.resize((int(m.size[0]*s_), int(m.size[1]*s_)), Image.LANCZOS).point(lambda v: int(v*op)); im.paste(Image.new('RGB', a.size, col), (int(x), int(y)), a)
def numb(im, i, col): spaced(ImageDraw.Draw(im), (W - 72, H - 84), f'{i:02d} / 12', F('mono', 15), col, .18, 'r')

# ---- 02 · ugly: the dark page with a surface. her dark painting (art5) crushed to plum, a pool of light, white ink, pink highlighter
a = load('g30/src/art5.jpg', (.5, .5), 1.2); a = a * .32 + np.array([44, 26, 40.]) * .55          # the painting sunk into plum
a = light(a, 300, 300, 900, .18, (120, 80, 120)); a = finish(a, 8, .3, 2)
im = pil(a); mask_on(im, inkmask('IMG_1631'), 520, W - 72 - 520, H - 620, (236, 226, 232), .85)   # the eye, white, bottom right
spaced(ImageDraw.Draw(im), (72, 92), 'I  ·  WHO', F('mono', 16), (150, 130, 150), .36)
y = text(im, "I don't know about you, but my experience of learning about business has been", 'serif', 32, 72, 300, col=(200, 186, 200), maxw=880, align='l', lh=1.3)
y = text(im, "pretty\nf*king ugly", 'serif', 112, 72, y + 24, col=IVORY, maxw=936, align='l', lh=1.0)
y = text(im, "the greys, the oranges, the fonts, the tone, one more list of things to implement before Monday", 'italic', 31, 72, y + 40, col=(200, 186, 200), maxw=760, align='l', lh=1.3)
highlight(im, "every business book I was ever given looked like a tax return", 'serif', 30, 72, y + 36, INKC, BAR, 800)
numb(im, 2, (150, 130, 150)); im.save(f'{OUT}/D02.jpg', quality=93)

# ---- 05 · Phyli: the cream page with a surface. her pastel sheet as paper, the stairs photo faint behind, the horse filled with the photo, light, a highlight
a = load('g30/src/p10.jpg', (.5, .45), 1.7); a = a * .55 + np.array(IVORY, float) * .45                 # her pastel as the paper
ph = load('g30/src/faye33.jpg', (.5, .4), 1.0); ph = ph.mean(2, keepdims=True).repeat(3, 2); a = a * .86 + ph * .14   # her, faint, underneath
a = light(a, 760, 380, 700, .35); a = finish(a, 7, .22, 5)
im = pil(a); mask_fill(im, inkmask('IMG_1636'), 480, W - 72 - 480, H - 560, 'g30/src/faye20.jpg', .55)
spaced(ImageDraw.Draw(im), (72, 92), 'II  ·  THE CLAIM', F('mono', 16), PERI, .36)
y = text(im, "now,\nI'm making\nPhyli", 'display', 116, 72, 300, col=PERI, maxw=936, align='l', lh=1.0)
y = highlight(im, "the business book I wish someone had handed me at twenty-five", 'serif', 30, 72, y + 40, INKC, BAR, 820)
text(im, "twelve volumes, a different part of your company in each one, and every one of them turns to nature for the answer, because that's where I've always found it", 'serif', 30, 72, y + 16, col=AUB, maxw=700, align='l', lh=1.4)
numb(im, 5, QUIET); im.save(f'{OUT}/D05.jpg', quality=93)

# ---- 08 · wisdom: the b&w with the cover's grade on it. bloom, grain, lilac in the shadows, the lead line bold pink, the quiet line small
a = load('g30/src/faye20.jpg', (.72, .4), 1.15); g = a.mean(2); g = np.clip((g - 110) * 1.2 + 118, 0, 255); a = np.stack([g, g, g], 2)
a = a * np.array([1.0, .97, 1.03]) + np.array([14, 6, 22.]) * (1 - g[..., None] / 255)                      # lilac in the shadows
bl = cv2.GaussianBlur(a, (0, 0), 22); a = a * .82 + np.clip(bl - 110, 0, 255) * .35                           # bloom
yy = np.arange(H)[:, None, None]; gg = np.clip((yy - 600) / 280.0, 0, 1) * .62; a = a * (1 - gg); a = finish(a, 10, .2, 8)
a = gbig(a, ['because the women', 'building thoughtful', 'companies deserve'], PINK, 78, y=680, lh=1.0, glow='#B48CF0', ga=.6, shadow=.45)
im = pil(a)
text(im, "wisdom that doesn't shout", 'italic', 44, 72, 950, col=IVORY, maxw=900, align='c', lh=1.1)
text(im, "because I needed it and couldn't find it, because this has felt channelled for a long time, and I'd rather be the hands than argue with it", 'serif', 27, 72, 1050, col=(226, 216, 222), maxw=820, align='c', lh=1.34)
numb(im, 8, IVORY); im.save(f'{OUT}/D08.jpg', quality=93)

S = Image.new('RGB', (3 * 540 + 40, 675), (30, 30, 30))
for k, n in enumerate(['D02', 'D05', 'D08']): S.paste(Image.open(f'{OUT}/{n}.jpg').resize((540, 675)), (k * 560, 0))
S.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
