"""the manifesto on the website spine: ivory paper, tracked mono chapter labels with the hand-drawn underline and her sprig as the flourish, Rozha for the one big line per page, Newsreader for the rest, the root flower climbing in from the bottom-left, the portrait cover, the cuddle on 09, the fairy on 12."""
import sys, os, subprocess; sys.path.insert(0, 'sys')
from style import *
import cv2
OUT = 'send/manifesto/site'; os.makedirs(OUT, exist_ok=True)
INKC = (28, 22, 26); PERI = (58, 62, 138); N = 12
fairy = Image.open('sys/week1/fairy/fairy_mask.png').convert('L')
sprig = Image.open('fp/web/sprig_a.png').convert('L'); rootf = Image.open('fp/web/rootflower_a.png').convert('L')
# crop the sprig to its ink and rotate so the stem runs along a line, flower at the end
bb = sprig.point(lambda v: 255 if v > 40 else 0).getbbox(); sprig = sprig.crop(bb); sprig = sprig.rotate(-90, expand=True, resample=Image.BICUBIC)

def paper(seed=7):
    a = np.ones((H, W, 3), np.float32) * np.array(IVORY, np.float32); rs = np.random.RandomState(seed); a += rs.randn(H, W, 1) * 2.4; return pil(a)
def mask_on(im, m, w, x, y, col=INKC, op=1.0):
    s = w / m.size[0]; a = m.resize((int(m.size[0]*s), int(m.size[1]*s)), Image.LANCZOS).point(lambda v: int(v*op)); im.paste(Image.new('RGB', a.size, col), (int(x), int(y)), a); return a.size
def chapter(im, t, y=96, x=None, seed=1):
    """tracked mono label, hand-drawn underline, the sprig flourish coming off the end (the website's link style)"""
    d = ImageDraw.Draw(im); f = F('mono', 17); t = t.upper(); ws = [d.textlength(ch, font=f) for ch in t]; tr = 17 * .36; total = sum(ws) + tr * (len(t) - 1)
    x0 = (W - total) / 2 if x is None else x
    spaced(d, (x0, y), t, f, INKC, .36); x1 = x0 + total
    underline(im, x0 - 6, x1 + 6, y + 36, INKC, seed=seed, width=3)
    mask_on(im, sprig, 120, x1 + 4, y + 36 - 46, INKC, .95)
def root(im, h=520, x=-30, y=None, op=.95):
    y = H - h - 40 if y is None else y; mask_on(im, rootf, int(h * rootf.size[0] / rootf.size[1]), x, y, INKC, op)
def numb(im, i): spaced(ImageDraw.Draw(im), (W - 72, H - 84), f'{i:02d} / {N:02d}', F('mono', 15), QUIET, .18, 'r')
def name(im): spaced(ImageDraw.Draw(im), (72, 60), 'faye pressly', F('mono', 15), QUIET, .36)
def big(im, t, y, size=66, col=INKC, align='c'): return text(im, t, 'display', size, 72, y, col=col, maxw=936, align=align, lh=1.04)
def body(im, t, y, size=31, col=INKC, align='c', maxw=860): return text(im, t, 'serif', size, 72 if align != 'r' else W - 72 - maxw, y, col=col, maxw=maxw, align=align, lh=1.38)
def ital(im, t, y, size=30, col=QUIET, align='c', maxw=860): return text(im, t, 'italic', size, 72, y, col=col, maxw=maxw, align=align, lh=1.32)
def measure(fn): return fn(Image.new('RGB', (W, H)), 0)
def centred(im, fn, dy=-20): h = measure(fn); fn(im, (H - h) / 2 + dy); return im
pages = {}

# 01 cover (her chosen tile, re-made with the line unclipped)
G = {}; exec(open('g60/build.py').read(), G)
srcf = open('g60/final.py').read(); exec(srcf[srcf.index('def big'):srcf.index('T=[None]*21')].replace('def big(', 'def gbig('), G)
grade, FIT, gbig, IV = G['grade'], G['F'], G['gbig'], G['IV']
por = np.array(Image.open('fp/web/portrait.png').convert('RGB')).astype(float)
up = cv2.resize(por, None, fx=1.9, fy=1.9, interpolation=cv2.INTER_LANCZOS4)
a = grade(FIT(up, (.58, .45)), warm=.02, sat=1.08, bloom=.3, grain=8)
A = gbig(a, ['a note,', 'before this', 'page changes'], IV, 112, y=975, glow='#B48CF0', ga=.5, shadow=.4)
pages[1] = Image.fromarray(np.clip(A, 0, 255).astype(np.uint8))

# 02 who
im = paper(2); chapter(im, 'i  ·  who', 150, seed=2)
y = big(im, "twenty years as the woman\nbehind the founder", 330, 70)
y = big(im, "now the founder", y + 36, 70, PERI)
body(im, "I ran other people's companies for twenty years and I was really good at it, and in all that time nobody ever asked me who the company was, only what it was making", y + 70, 31)
root(im, 480); numb(im, 2); pages[2] = im

# 03 ugly
im = paper(3); chapter(im, 'i  ·  who', 150, seed=3)
def f3(im, y):
    y = body(im, "I don't know about you, but my experience of learning about business has been", y, 34)
    y = big(im, "pretty fucking ugly", y + 24, 96)
    return body(im, "the greys, the oranges, the fonts, the tone, one more list of things to implement before Monday\n\nevery business book I was ever given looked like a tax return", y + 50, 31)
centred(im, f3, 10); numb(im, 3); pages[3] = im

# 04 the theory
im = paper(4); chapter(im, 'ii  ·  the claim', 150, seed=4)
def f4(im, y):
    y = body(im, "I wanted a theory of the organisation with", y, 34)
    y = big(im, "a womb, a nervous system\nand a backbone", y + 24, 72)
    return body(im, "a business is not a machine to be extracted from, she is a living thing, she has seasons, she has moods, she heals\n\nnature solved all of this a long time ago, nobody wrote it down beautifully", y + 50, 31)
centred(im, f4, 10); root(im, 420, op=.9); numb(im, 4); pages[4] = im

# 05 Phyli
im = paper(5); chapter(im, 'ii  ·  the claim', 150, seed=5)
def f5(im, y):
    y = big(im, "now, I'm making Phyli", y, 92, PERI)
    y = body(im, "the business book I wish someone had handed me at twenty-five", y + 40, 34)
    return body(im, "twelve volumes, a different part of your company in each one, and every one of them turns to nature for the answer, because that's where I've always found it", y + 30, 31)
centred(im, f5); numb(im, 5); pages[5] = im

# 06 the book
im = paper(6); chapter(im, 'ii  ·  the claim', 150, seed=6)
def f6(im, y):
    y = big(im, "the most beautiful\nbusiness book\nin the world", y, 84)
    y = body(im, "pages that open out, lift and unfold the way the books we loved as children did, made from couture fabric by masters of paper, leather and binding", y + 40, 31)
    return ital(im, "adult books stopped being beautiful a long time ago, this is the opposite of that, a book you keep and hand down", y + 30, 29)
centred(im, f6, 10); numb(im, 6); pages[6] = im

# 07 the dream (the question alone)
im = paper(7); chapter(im, 'iii  ·  the dream', 150, seed=7)
def f7(im, y):
    y = body(im, "my dream is to launch it in an art gallery\nthe collectors' volumes, numbered and bound by hand, MoMA's bookshop, Vogue", y, 31)
    return text(im, "what if the most beautiful object on your shelf was also the one that fixed your Monday", 'italic', 62, 72, y + 70, col=PERI, maxw=900, align='c', lh=1.1)
centred(im, f7, 0); root(im, 380, op=.85); numb(im, 7); pages[7] = im

# 08 why
im = paper(8); chapter(im, 'iv  ·  why', 150, seed=8)
def f8(im, y):
    y = body(im, "because the women building thoughtful companies deserve", y, 34)
    y = big(im, "wisdom that doesn't shout", y + 20, 64)
    return body(im, "because I needed it and couldn't find it\n\nbecause this has felt channelled for a long time, and I'd rather be the hands than argue with it", y + 50, 31)
centred(im, f8, 10); numb(im, 8); pages[8] = im

# 09 Indigo (photo page, one line)
a = np.array(Image.open('sys/mstills/indigo2.jpg').convert('RGB')).astype(float)
a = grade(FIT(a, (.55, .45), 1.05), warm=.04, sat=1.05, bloom=.3)
A = gbig(a, ['and because one day', 'my daughter will ask', 'what I made', 'with my life'], IV, 92, y=110, lh=1.0, glow='#F2B3A8', ga=.5, shadow=.4)
A = gbig(A, ['I want the answer', 'to be beautiful'], IV, 60, y=1120, lh=1.05, glow='#B48CF0', ga=.5, shadow=.4)
im = Image.fromarray(np.clip(A, 0, 255).astype(np.uint8)); spaced(ImageDraw.Draw(im), (W - 72, H - 84), '09 / 12', F('mono', 15), IVORY, .18, 'r'); pages[9] = im

# 10 what I care about
im = paper(10); chapter(im, 'v  ·  how', 150, seed=10)
def f10(im, y):
    y = body(im, "I care about", y, 34)
    y = big(im, "truth, care, craft", y + 20, 84)
    y = body(im, "and work that outlives the week it was posted in", y + 36, 34)
    y = ital(im, "not hacks, not hustle, not being everywhere", y + 40, 30)
    return body(im, "I'm not trying to be fast, I'm trying to be aligned, and connected", y + 30, 31)
centred(im, f10, 10); numb(im, 10); pages[10] = im

# 11 limits
im = paper(11); chapter(im, 'v  ·  how', 150, seed=11)
def f11(im, y):
    y = big(im, "it will not take over my life", y, 64)
    y = body(im, "the most important work I'll ever do is being Indigo's mother\n\nso not everything here will be perfect, it'll be beautifully imperfect, occasionally cringe", y + 40, 31)
    return ital(im, "I left a perfectly good career to make a business book out of silk, no regrets, some fear", y + 36, 30)
centred(im, f11, 0); root(im, 440, op=.9); numb(im, 11); pages[11] = im

# 12 stay (the list, each stay underlined with the sprig)
im = paper(12); chapter(im, 'vi  ·  for you', 150, seed=12)
lines = ["if you're the one who remembers, decides,\nfollows up and fixes everything", "if you built something out of taste and now\nspend your days defending it with numbers", "if your supply chain runs like clockwork\nand you still can't take a week off"]
y = 300
for k, l in enumerate(lines):
    y = body(im, l, y, 31); d = ImageDraw.Draw(im)
    f = F('display', 46); tw = d.textlength('stay', font=f); d.text((W/2, y + 8), 'stay', font=f, fill=PERI, anchor='ma')
    underline(im, W/2 - tw/2 - 8, W/2 + tw/2 + 8, y + 8 + 54, INKC, seed=20 + k, width=3); mask_on(im, sprig, 90, W/2 + tw/2 + 10, y + 8 + 54 - 34, INKC, .9)
    y += 120
y = ital(im, "and if you're here because you love me,\nbeing here is support, and I feel it", y + 10, 29)
y = big(im, "thank you for watching\nme do the thing", y + 30, 50); dot(im, W/2, y + 40)
a_f = fairy.copy(); s = 300 / a_f.size[1]; a_f = a_f.resize((int(a_f.size[0]*s), 300), Image.LANCZOS); im.paste(Image.new('RGB', a_f.size, INKC), (W - 72 - a_f.size[0], H - 110 - 300), a_f)
numb(im, 12); pages[12] = im

for i in range(1, 13): pages[i].save(f'{OUT}/Manifesto_{i:02d}.jpg', quality=93)
tiles = [pages[i].resize((270, 338)) for i in range(1, 13)]
Sh = Image.new('RGB', (4 * 270, 3 * 338), (30, 30, 30))
for i, t in enumerate(tiles): Sh.paste(t, ((i % 4) * 270, (i // 4) * 338))
Sh.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
