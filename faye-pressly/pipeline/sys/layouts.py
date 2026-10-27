"""one page of the manifesto (04), seven layouts, so she can sign off a system."""
import sys, os; sys.path.insert(0, 'sys')
from style import *
import cv2
G = {}; exec(open('g60/build.py').read(), G)
srcf = open('g60/final.py').read(); exec(srcf[srcf.index('def big'):srcf.index('T=[None]*21')].replace('def big(', 'def gbig('), G)
grade, FIT, gbig, IV = G['grade'], G['F'], G['gbig'], G['IV']
OUT = 'send/manifesto/layouts'; os.makedirs(OUT, exist_ok=True)
INKC = (28, 22, 26); PERI = (58, 62, 138); AUB = (70, 40, 60); PLUM = (44, 26, 40); PINK = (243, 198, 227); GOLD = (168, 140, 92)
HEAD1 = "I wanted a theory of the organisation with"; HEAD = "a womb, a nervous system\nand a backbone"
BODY = "a business is not a machine to be extracted from, she is a living thing, she has seasons, she has moods, she heals"
ASIDE = "nature solved all of this a long time ago, nobody wrote it down beautifully"
por = np.array(Image.open('fp/web/portrait.png').convert('RGB')).astype(float)
def paper(seed=7, tone=IVORY):
    a = np.ones((H, W, 3), np.float32) * np.array(tone, np.float32); rs = np.random.RandomState(seed); a += rs.randn(H, W, 1) * 2.4; return pil(a)
def label(im, t, col, x=72, y=92, align='l'): spaced(ImageDraw.Draw(im), (x, y), t.upper(), F('mono', 16), col, .36, align)
def numb(im, col): spaced(ImageDraw.Draw(im), (W - 72, H - 84), '04 / 12', F('mono', 15), col, .18, 'r')
out = []

# 1 · faded portrait watermark (emmajade): her face at 14% behind the type
im = paper(1); up = cv2.resize(por, None, fx=1.9, fy=1.9, interpolation=cv2.INTER_LANCZOS4); pa = FIT(up, (.58, .45)); pa = pa.mean(2, keepdims=True).repeat(3, 2)
a = np.asarray(im).astype(float) * .80 + pa * .20; im = pil(a)
label(im, 'a note, before this page changes', QUIET, W/2, 92, 'c')
y = text(im, HEAD1, 'serif', 34, 72, 400, col=INKC, maxw=900, align='c', lh=1.3)
y = text(im, "a womb, a nervous system", 'display', 74, 72, y + 20, col=INKC, maxw=936, align='c', lh=1.04)
y = text(im, "and a backbone", 'italic', 74, 72, y + 4, col=PERI, maxw=936, align='c', lh=1.04)
y = text(im, BODY, 'serif', 31, 72, y + 50, col=INKC, maxw=820, align='c', lh=1.4)
text(im, ASIDE, 'italic', 29, 72, y + 28, col=QUIET, maxw=820, align='c', lh=1.3); numb(im, QUIET); out.append(('1 faded portrait behind', im))

# 2 · black and white photo, the cover's pink bold type
a = np.array(Image.open('g30/src/faye33.jpg').convert('RGB')).astype(float); a = FIT(a, (.5, .5), 1.0); g = a.mean(2); g = np.clip((g - 110) * 1.25 + 118, 0, 255); rs = np.random.RandomState(4); g = g + rs.randn(*g.shape) * 7
a = np.stack([g, g, g], 2) * np.array([1.0, .98, 1.0])
A = gbig(a, ['a womb,', 'a nervous system', 'and a backbone'], '#F3C6E3', 112, y=620, lh=1.0, glow='#B48CF0', ga=.55, shadow=.45)
A = gbig(A, ['I wanted a theory of the organisation with'], '#F3C6E3', 40, y=540, lh=1.0, glow='#B48CF0', ga=.4, shadow=.4)
im = Image.fromarray(np.clip(A, 0, 255).astype(np.uint8)); numb(im, IVORY); out.append(('2 b&w photo, pink type', im))

# 3 · the dark tile (embodied): deep plum, ivory serif, the italic aside in brackets, the arrow
im = paper(3, PLUM); label(im, 'ii  ·  the claim', (150, 130, 150))
y = text(im, HEAD1, 'serif', 32, 72, 330, col=(200, 186, 200), maxw=900, align='l', lh=1.3)
y = text(im, HEAD, 'display', 92, 72, y + 24, col=IVORY, maxw=936, align='l', lh=1.02)
y = text(im, "(" + ASIDE + ")", 'italic', 32, 72, y + 40, col=(200, 186, 200), maxw=820, align='l', lh=1.3)
y = text(im, BODY, 'serif', 30, 72, y + 50, col=IVORY, maxw=820, align='l', lh=1.4)
d = ImageDraw.Draw(im); d.line([(72, H - 150), (190, H - 150)], fill=IVORY, width=3); d.line([(170, H - 164), (190, H - 150), (170, H - 136)], fill=IVORY, width=3); numb(im, (150, 130, 150)); out.append(('3 dark tile, serif, bracket aside', im))

# 4 · cream editorial, left-aligned, numbered mono header in periwinkle
im = paper(4); label(im, '02  ·  the claim', PERI)
y = text(im, HEAD1, 'serif', 32, 72, 330, col=QUIET, maxw=900, align='l', lh=1.3)
y = text(im, HEAD, 'display', 92, 72, y + 24, col=INKC, maxw=936, align='l', lh=1.02)
y = text(im, BODY, 'serif', 31, 72, y + 50, col=INKC, maxw=820, align='l', lh=1.4)
y = text(im, ASIDE, 'italic', 30, 72, y + 30, col=PERI, maxw=820, align='l', lh=1.3)
d = ImageDraw.Draw(im); d.line([(72, H - 150), (190, H - 150)], fill=INKC, width=3); d.line([(170, H - 164), (190, H - 150), (170, H - 136)], fill=INKC, width=3); numb(im, QUIET); out.append(('4 cream editorial, left', im))

# 5 · collage (four of her photos) with one big line across
tiles = ['g30/src/faye20.jpg', 'g30/src/faye51.jpg', 'g30/src/faye0.jpg', 'broll/new_stills/IMG_7390.jpg']
a = np.zeros((H, W, 3)); hh, ww = H // 2, W // 2
for k, p in enumerate(tiles):
    t = FIT(np.array(Image.open(p).convert('RGB')).astype(float), (.5, .4), 1.0); t = cv2.resize(t, (ww, hh)); a[(k // 2) * hh:(k // 2 + 1) * hh, (k % 2) * ww:(k % 2 + 1) * ww] = t
a = grade(a, warm=.02, sat=1.05, bloom=.25, grain=6)
A = gbig(a, ['a womb,', 'a nervous', 'system and', 'a backbone'], IV, 136, lh=1.0, glow='#B48CF0', ga=.5, shadow=.45)
im = Image.fromarray(np.clip(A, 0, 255).astype(np.uint8)); numb(im, IVORY); out.append(('5 collage, one line', im))

# 6 · colour photo in the cover style (y2k grade, bold sans) + the small text in serif at the foot
a = np.array(Image.open('g30/src/faye20.jpg').convert('RGB')).astype(float); a = grade(FIT(a, (.7, .4), 1.1), warm=.03, sat=1.1, bloom=.3, grain=8)
A = gbig(a, ['a womb,', 'a nervous system', 'and a backbone'], IV, 108, y=140, lh=1.0, glow='#B48CF0', ga=.5, shadow=.4)
im = Image.fromarray(np.clip(A, 0, 255).astype(np.uint8))
text(im, BODY, 'serif', 30, 72, 1050, col=IVORY, maxw=820, align='c', lh=1.36); numb(im, IVORY); out.append(('6 cover-style colour photo', im))

# 7 · faded portrait + pink bold (the cover's type on the watermark page)
im = paper(7); a = np.asarray(im).astype(float) * .82 + pa * .18; im = pil(a)
A = gbig(np.asarray(im).astype(float), ['a womb,', 'a nervous system', 'and a backbone'], '#C96AA8', 112, y=420, lh=1.0, glow='#F6E2EC', ga=.6, shadow=0)
im = Image.fromarray(np.clip(A, 0, 255).astype(np.uint8))
text(im, HEAD1, 'serif', 32, 72, 340, col=AUB, maxw=900, align='c', lh=1.3)
y = text(im, BODY, 'serif', 31, 72, 800, col=AUB, maxw=820, align='c', lh=1.4)
text(im, ASIDE, 'italic', 29, 72, y + 28, col=QUIET, maxw=820, align='c', lh=1.3); numb(im, QUIET); out.append(('7 faded portrait, pink bold', im))

for k, (name, im) in enumerate(out): im.save(f'{OUT}/L{k+1}.jpg', quality=92)
S = Image.new('RGB', (4 * 300, 2 * (375 + 26)), (30, 30, 30)); d = ImageDraw.Draw(S)
for k, (name, im) in enumerate(out):
    x = (k % 4) * 300; y = (k // 4) * 401; S.paste(im.resize((300, 375)), (x, y)); d.text((x + 6, y + 378), name, fill=(255, 255, 255), font=F('mono', 14))
S.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
