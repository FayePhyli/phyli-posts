"""manifesto v4: her four chosen layouts in rhythm. 2 = b&w photo + pink bold · 3 = dark plum serif with bracket aside · 4 = cream editorial left · 7 = faded portrait + pink bold. cover = her tile, 11 = the Indigo camcorder video."""
import sys, os, subprocess; sys.path.insert(0, 'sys')
from style import *
import cv2
G = {}; exec(open('g60/build.py').read(), G)
srcf = open('g60/final.py').read(); exec(srcf[srcf.index('def big'):srcf.index('T=[None]*21')].replace('def big(', 'def gbig('), G)
grade, FIT, gbig, IV = G['grade'], G['F'], G['gbig'], G['IV']
OUT = 'send/manifesto/v4'; os.makedirs(OUT, exist_ok=True)
INKC = (28, 22, 26); PERI = (58, 62, 138); AUB = (70, 40, 60); PLUM = (44, 26, 40); PLUMQ = (150, 130, 150); PLUMT = (200, 186, 200); PINK = '#F3C6E3'; PINKD = '#C96AA8'; N = 12
fairy = Image.open('sys/week1/fairy/fairy_mask.png').convert('L')
por = np.array(Image.open('fp/web/portrait.png').convert('RGB')).astype(float)
up = cv2.resize(por, None, fx=1.9, fy=1.9, interpolation=cv2.INTER_LANCZOS4); PA = FIT(up, (.58, .45)); PA = PA.mean(2, keepdims=True).repeat(3, 2)
sp = Image.open('fp/web/sprig_a.png').convert('L'); bb = sp.point(lambda v: 255 if v > 40 else 0).getbbox(); sp = sp.crop(bb); sp = sp.crop((0, 0, sp.size[0], int(sp.size[1] * .78)))
sp = sp.filter(ImageFilter.GaussianBlur(1.6)).point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.GaussianBlur(0.8)).rotate(-90, expand=True, resample=Image.BICUBIC)

def paper(seed=7, tone=IVORY):
    a = np.ones((H, W, 3), np.float32) * np.array(tone, np.float32); rs = np.random.RandomState(seed); a += rs.randn(H, W, 1) * 2.4; return pil(a)
def label(im, t, col, x=72, y=92, align='l'): spaced(ImageDraw.Draw(im), (x, y), t.upper(), F('mono', 16), col, .36, align)
def numb(im, i, col): spaced(ImageDraw.Draw(im), (W - 72, H - 84), f'{i:02d} / {N:02d}', F('mono', 15), col, .18, 'r')
def arrow(im, col, y=None):
    y = H - 150 if y is None else y; d = ImageDraw.Draw(im); d.line([(72, y), (190, y)], fill=col, width=3); d.line([(170, y - 14), (190, y), (170, y + 14)], fill=col, width=3)
def bw(path, focus=(.5, .5), zoom=1.0, seed=4):
    a = FIT(np.array(Image.open(path).convert('RGB')).astype(float), focus, zoom); g = a.mean(2); g = np.clip((g - 110) * 1.25 + 118, 0, 255); rs = np.random.RandomState(seed); g = g + rs.randn(*g.shape) * 7
    return np.stack([g, g, g], 2) * np.array([1.0, .98, 1.0])
def line_into_flower(im, x0, x1, y, col=INKC, seed=3, width=4, fw=300):
    d = ImageDraw.Draw(im); rs = np.random.RandomState(seed); pts = []; n = int((x1 - x0) / 5)
    for i in range(n + 1):
        t = i / n; pts.append((x0 + (x1 - x0) * t, y + math.sin(t * 7 + seed) * 2.0 + rs.randn() * 0.6))
    d.line(pts, fill=col, width=width, joint='curve')
    s = fw / sp.size[0]; a = sp.resize((int(sp.size[0] * s), int(sp.size[1] * s)), Image.LANCZOS)
    arr = np.asarray(a); cols = np.where(arr.max(0) > 60)[0]; x_first = cols[0]; rows = np.where(arr[:, x_first:x_first + 12].max(1) > 60)[0]; stem_y = int(rows.mean())
    im.paste(Image.new('RGB', a.size, col), (int(x1 - x_first - 6), int(y - stem_y)), a)

# ---- the four layouts ----
def L2(photo, focus, zoom, big_lines, big_size, big_y, small=None, small_y=None, lead=None, lead_y=None, seed=4):
    a = bw(photo, focus, zoom, seed)
    if small:   # darken the foot so the small text reads over the photo
        yy = np.arange(H)[:, None, None]; g = np.clip((yy - (small_y - 140)) / 220.0, 0, 1) * .5; a = a * (1 - g)
    if lead: a = gbig(a, [lead], PINK, 40, y=lead_y, lh=1.0, glow='#B48CF0', ga=.4, shadow=.4)
    a = gbig(a, big_lines, PINK, big_size, y=big_y, lh=1.0, glow='#B48CF0', ga=.55, shadow=.45)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if small: text(im, small, 'serif', 30, 72, small_y, col=IVORY, maxw=820, align='c', lh=1.36)
    return im
def L3(chap, lead, head, aside, body=None, head_size=92, y0=330):
    im = paper(3, PLUM); label(im, chap, PLUMQ)
    y = text(im, lead, 'serif', 32, 72, y0, col=PLUMT, maxw=900, align='l', lh=1.3) if lead else y0
    y = text(im, head, 'display', head_size, 72, y + 24, col=IVORY, maxw=936, align='l', lh=1.02)
    if aside: y = text(im, "(" + aside + ")", 'italic', 32, 72, y + 40, col=PLUMT, maxw=840, align='l', lh=1.3)
    if body: y = text(im, body, 'serif', 30, 72, y + 50, col=IVORY, maxw=820, align='l', lh=1.4)
    arrow(im, IVORY); return im
def L4(chap, lead, head, body, aside, head_size=92, y0=330, head_col=INKC):
    im = paper(4); label(im, chap, PERI)
    y = text(im, lead, 'serif', 32, 72, y0, col=QUIET, maxw=900, align='l', lh=1.3) if lead else y0
    y = text(im, head, 'display', head_size, 72, y + 24, col=head_col, maxw=936, align='l', lh=1.02)
    if body: y = text(im, body, 'serif', 31, 72, y + 50, col=INKC, maxw=820, align='l', lh=1.4)
    if aside: y = text(im, aside, 'italic', 30, 72, y + 30, col=PERI, maxw=820, align='l', lh=1.3)
    arrow(im, INKC); return im
def L7(lead, big_lines, big_size, big_y, body, aside, body_y, lead_y=340, seed=7):
    im = paper(seed); a = np.asarray(im).astype(float) * .80 + PA * .20
    a = gbig(a, big_lines, PINKD, big_size, y=big_y, lh=1.0, glow='#F6E2EC', ga=.6, shadow=0)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if lead: text(im, lead, 'serif', 32, 72, lead_y, col=AUB, maxw=900, align='c', lh=1.3)
    y = text(im, body, 'serif', 31, 72, body_y, col=AUB, maxw=820, align='c', lh=1.4) if body else body_y
    if aside: text(im, aside, 'italic', 29, 72, y + 28, col=QUIET, maxw=820, align='c', lh=1.3)
    return im
pages = {}
# 01 cover
a = grade(FIT(up, (.58, .45)), warm=.02, sat=1.08, bloom=.3, grain=8)
A = gbig(a, ['a note,', 'before this', 'page changes'], IV, 112, y=975, lh=1.0, glow='#B48CF0', ga=.5, shadow=.4)
pages[1] = Image.fromarray(np.clip(A, 0, 255).astype(np.uint8))
# 02 who · L2 (the stairs, b&w, pink)
pages[2] = L2('g30/src/faye33.jpg', (.5, .55), 1.0, ['twenty years', 'as the woman', 'behind the founder', 'now the founder'], 92, 120, small="I ran other people's companies for twenty years and I was really good at it, and in all that time nobody ever asked me who the company was, only what it was making", small_y=1080)
numb(pages[2], 2, IVORY)
# 03 ugly · L3 (dark)
pages[3] = L3('i  ·  who', "I don't know about you, but my experience of learning about business has been", "pretty\nfucking ugly", "the greys, the oranges, the fonts, the tone, one more list of things to implement before Monday", "every business book I was ever given looked like a tax return", 108); numb(pages[3], 3, PLUMQ)
# 04 claim · L7 (faded portrait, pink)
pages[4] = L7("I wanted a theory of the organisation with", ['a womb,', 'a nervous system', 'and a backbone'], 112, 420, "a business is not a machine to be extracted from, she is a living thing, she has seasons, she has moods, she heals", "nature solved all of this a long time ago, nobody wrote it down beautifully", 800); numb(pages[4], 4, QUIET)
# 05 Phyli · L4 (cream)
pages[5] = L4('ii  ·  the claim', None, "now,\nI'm making\nPhyli", "the business book I wish someone had handed me at twenty-five\n\ntwelve volumes, a different part of your company in each one, and every one of them turns to nature for the answer, because that's where I've always found it", None, 108, 300, PERI); numb(pages[5], 5, QUIET)
# 06 the book · L2 (headscarf, b&w, pink)
pages[6] = L2('g30/src/faye20.jpg', (.72, .4), 1.15, ['the most', 'beautiful', 'business book', 'in the world'], 100, 110, small="pages that open out, lift and unfold the way the books we loved as children did, made from couture fabric by masters of paper, leather and binding\n\nadult books stopped being beautiful a long time ago, this is the opposite of that, a book you keep and hand down", small_y=900, seed=6)
numb(pages[6], 6, IVORY)
# 07 the dream · L7
pages[7] = L7("my dream is to launch it in an art gallery, the collectors' volumes numbered and bound by hand, MoMA's bookshop, Vogue", ['what if the most', 'beautiful object', 'on your shelf', 'was also the one', 'that fixed', 'your Monday'], 84, 460, None, None, 0, lead_y=270, seed=8); numb(pages[7], 7, QUIET)
# 08 why · L4
pages[8] = L4('iii  ·  why', "because the women building thoughtful companies deserve", "wisdom that\ndoesn't shout", "because I needed it and couldn't find it\n\nbecause this has felt channelled for a long time, and I'd rather be the hands than argue with it", None, 96); numb(pages[8], 8, QUIET)
# 09 daughter · L3 (dark)
pages[9] = L3('iii  ·  why', "and because one day my daughter will ask", "what I made\nwith my life", None, "I want the answer to be beautiful", 108, 330); numb(pages[9], 9, PLUMQ)
# 10 truth care craft · L7
pages[10] = L7("I care about", ['truth, care, craft'], 104, 420, "and work that outlives the week it was posted in\n\nI'm not trying to be fast, I'm trying to be aligned, and connected", "not hacks, not hustle, not being everywhere", 620, lead_y=350, seed=10); numb(pages[10], 10, QUIET)
# 11 Indigo · the camcorder video (made in v3) + its first frame
import shutil; shutil.copy('send/manifesto/v3/Manifesto_11_video.mp4', f'{OUT}/Manifesto_11_video.mp4'); pages[11] = Image.open('send/manifesto/v3/Manifesto_11.jpg')
# 12 for you · L4 with the one flourish, one stay, the fairy
im = paper(12); d = ImageDraw.Draw(im); t = 'IV  ·  FOR YOU'; f = F('mono', 16); tw = sum(d.textlength(ch, font=f) for ch in t) + 16 * .36 * (len(t) - 1)
spaced(d, (72, 92), t, f, PERI, .36); line_into_flower(im, 66, 72 + tw + 10, 92 + 36, INKC, seed=5, width=4, fw=280)
y = text(im, "if you're the one who remembers, decides, follows up and fixes everything\n\nif you built something out of taste and now spend your days defending it with numbers\n\nif your supply chain runs like clockwork and you still can't take a week off", 'serif', 31, 72, 300, col=INKC, maxw=820, align='l', lh=1.4)
y = text(im, "stay", 'display', 120, 72, y + 30, col=PERI, maxw=900, align='l', lh=1.0)
y = text(im, "and if you're here because you love me, being here is support, and I feel it", 'italic', 30, 72, y + 30, col=QUIET, maxw=700, align='l', lh=1.3)
y = text(im, "thank you for watching\nme do the thing", 'display', 50, 72, y + 30, col=INKC, maxw=700, align='l', lh=1.04); dot(im, 86, y + 44)
a_f = fairy.copy(); s = 320 / a_f.size[1]; a_f = a_f.resize((int(a_f.size[0] * s), 320), Image.LANCZOS)
fl = FIT(np.array(Image.open('g30/src/p10.jpg').convert('RGB')).astype(float), (.5, .5), 1.0); fl = cv2.resize(fl, a_f.size); mn = fl.mean(); fl = np.clip((fl - mn) * 1.3 + mn * .5, 0, 255)
im.paste(pil(fl), (W - 72 - a_f.size[0], H - 110 - 320), a_f); numb(im, 12, QUIET); pages[12] = im

for i in range(1, 13): pages[i].save(f'{OUT}/Manifesto_{i:02d}.jpg', quality=93)
tiles = [pages[i].resize((270, 338)) for i in range(1, 13)]
Sh = Image.new('RGB', (4 * 270, 3 * 338), (30, 30, 30))
for i, t in enumerate(tiles): Sh.paste(t, ((i % 4) * 270, (i // 4) * 338))
Sh.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
