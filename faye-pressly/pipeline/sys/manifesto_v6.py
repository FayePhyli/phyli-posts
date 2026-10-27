"""manifesto v6: depth on every page. surfaces from her art and photos, light, grain, one highlighted line, inks only where wanted, the 3D cut-out on 04."""
import sys, os, subprocess, shutil; sys.path.insert(0, 'sys')
from style import *
import cv2
G = {}; exec(open('g60/build.py').read(), G)
srcf = open('g60/final.py').read(); exec(srcf[srcf.index('def big'):srcf.index('T=[None]*21')].replace('def big(', 'def gbig('), G)
grade, FIT, gbig, IV = G['grade'], G['F'], G['gbig'], G['IV']
OUT = 'send/manifesto/v6'; os.makedirs(OUT, exist_ok=True)
INKC = (28, 22, 26); PERI = (58, 62, 138); AUB = (70, 40, 60); PINK = '#F3C6E3'; PINKD = (201, 106, 168); BAR = (236, 190, 214); PLUMQ = (150, 130, 150); PLUMT = (200, 186, 200); N = 12
fairy = Image.open('sys/week1/fairy/fairy_mask.png').convert('L')
por = np.array(Image.open('fp/web/portrait.png').convert('RGB')).astype(float)
up = cv2.resize(por, None, fx=1.9, fy=1.9, interpolation=cv2.INTER_LANCZOS4); PA = FIT(up, (.58, .45)); PA = PA.mean(2, keepdims=True).repeat(3, 2)
sp = Image.open('fp/web/sprig_a.png').convert('L'); bb = sp.point(lambda v: 255 if v > 40 else 0).getbbox(); sp = sp.crop(bb); sp = sp.crop((0, 0, sp.size[0], int(sp.size[1] * .78)))
sp = sp.filter(ImageFilter.GaussianBlur(1.6)).point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.GaussianBlur(0.8)).rotate(-90, expand=True, resample=Image.BICUBIC)

def inkmask(name): return Image.open(f'ink/masks/{name}.png').convert('L') if os.path.exists(f'ink/masks/{name}.png') else Image.open(f'fp/web/{name}_a.png').convert('L')
def load(p, focus=(.5, .5), zoom=1.0): return FIT(np.array(Image.open(p).convert('RGB')).astype(float), focus, zoom)
def finish(a, grain=9, vig=.28, seed=1):
    rs = np.random.RandomState(seed); a = a + rs.randn(H, W, 1) * grain
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2); v = 1 - vig * np.clip(r - .55, 0, 1) / .9
    return np.clip(a * v[..., None], 0, 255)
def light(a, cx, cy, rad, strength, col=(255, 240, 248)):
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2); g = np.clip(1 - d / rad, 0, 1) ** 2 * strength
    return a * (1 - g[..., None]) + np.array(col, float) * g[..., None]
def highlight(im, t, kind, size, x, y, col, bar=BAR, maxw=900, align='l'):
    d = ImageDraw.Draw(im); f = F(kind, size); tw = d.textlength(t, font=f); x0 = x if align == 'l' else W / 2 - tw / 2
    bar_im = Image.new('RGBA', (int(tw + 28), int(size * 1.05)), bar + (210,)); im.paste(bar_im, (int(x0 - 14), int(y + size * .08)), bar_im)
    d.text((x0, y), t, font=f, fill=col); return y + size * 1.3
def mask_fill(im, m, w, x, y, photo, tone=.6, op=.95):
    s_ = w / m.size[0]; a = m.resize((int(m.size[0]*s_), int(m.size[1]*s_)), Image.LANCZOS).point(lambda v: int(v*op))
    f = load(photo, (.5, .4)); f = cv2.resize(f, a.size); mn = f.mean(); f = np.clip((f - mn) * 1.3 + mn * tone, 0, 255); im.paste(pil(f), (int(x), int(y)), a)
def mask_on(im, m, w, x, y, col, op=1.0):
    s_ = w / m.size[0]; a = m.resize((int(m.size[0]*s_), int(m.size[1]*s_)), Image.LANCZOS).point(lambda v: int(v*op)); im.paste(Image.new('RGB', a.size, col), (int(x), int(y)), a)
def numb(im, i, col): spaced(ImageDraw.Draw(im), (W - 72, H - 84), f'{i:02d} / {N:02d}', F('mono', 15), col, .18, 'r')
def chap(im, t, col): spaced(ImageDraw.Draw(im), (72, 92), t.upper(), F('mono', 16), col, .36)
def cream_surface(sheet, photo, zoom=1.7, lift=.45, faint=.14, lx=760, ly=380, seed=5):
    a = load(f'g30/src/{sheet}.jpg', (.5, .45), zoom); a = a * (1 - lift) + np.array(IVORY, float) * lift
    ph = load(photo, (.5, .4), 1.0) if photo else PA; ph = ph.mean(2, keepdims=True).repeat(3, 2); a = a * (1 - faint) + ph * faint
    a = light(a, lx, ly, 700, .35); return finish(a, 7, .22, seed)
def dark_surface(painting, zoom=1.2, seed=2, lx=300, ly=300):
    a = load(f'g30/src/{painting}.jpg', (.5, .5), zoom); a = a * .32 + np.array([44, 26, 40.]) * .55
    a = light(a, lx, ly, 900, .18, (120, 80, 120)); return finish(a, 8, .3, seed)
def bwgrade(a):
    g = a.mean(2); g = np.clip((g - 110) * 1.2 + 118, 0, 255); a = np.stack([g, g, g], 2)
    a = a * np.array([1.0, .97, 1.03]) + np.array([14, 6, 22.]) * (1 - g[..., None] / 255)
    bl = cv2.GaussianBlur(a, (0, 0), 22); return a * .82 + np.clip(bl - 110, 0, 255) * .35
def foot(a, y0, depth=.6, span=240):
    yy = np.arange(H)[:, None, None]; g = np.clip((yy - y0) / span, 0, 1) * depth; return a * (1 - g)
pages = {}

# 01 cover
a = grade(FIT(up, (.58, .45)), warm=.02, sat=1.08, bloom=.3, grain=8)
A = gbig(a, ['a note,', 'before this', 'page changes'], IV, 112, y=975, lh=1.0, glow='#B48CF0', ga=.5, shadow=.4); pages[1] = pil(A)

# 02 ugly · dark painting, no ink
im = pil(dark_surface('art5')); chap(im, 'i  ·  who', PLUMQ)
y = text(im, "I don't know about you, but my experience of learning about business has been", 'serif', 32, 72, 300, col=PLUMT, maxw=880, align='l', lh=1.3)
y = text(im, "pretty\nf*king ugly", 'serif', 112, 72, y + 24, col=IVORY, maxw=936, align='l', lh=1.0)
y = text(im, "the greys, the oranges, the fonts, the tone, one more list of things to implement before Monday", 'italic', 31, 72, y + 40, col=PLUMT, maxw=760, align='l', lh=1.3)
highlight(im, "every business book I was ever given looked like a tax return", 'serif', 30, 72, y + 36, INKC); numb(im, 2, PLUMQ); pages[2] = im

# 03 the womb · faint portrait on her pastel, pink bold
a = cream_surface('p05', None, 1.4, .4, .2, 540, 700, 3)
a = gbig(a, ['a womb,', 'a nervous system', 'and a backbone'], '#C96AA8', 112, y=420, lh=1.0, glow='#F6E2EC', ga=.6, shadow=0); im = pil(a)
text(im, "I wanted a theory of the organisation with", 'serif', 32, 72, 340, col=AUB, maxw=900, align='c', lh=1.3)
y = text(im, "a business is not a machine to be extracted from, she is a living thing, she has seasons, she has moods, she heals", 'serif', 31, 72, 800, col=AUB, maxw=820, align='c', lh=1.4)
highlight(im, "nature solved all of this a long time ago, nobody wrote it down beautifully", 'italic', 29, 0, y + 28, AUB, align='c'); numb(im, 3, QUIET); pages[3] = im

# 04 behind the founder · the 3D cut-out, her smaller in frame so the type reads
src = np.array(Image.open('g30/src/faye0.jpg').convert('RGB')).astype(float); cut = Image.open('sys/cut/faye0.png').convert('RGBA'); alpha = np.asarray(cut)[..., 3].astype(float) / 255
focus, zoom = (.5, .5), 1.0; base = bwgrade(FIT(src, focus, zoom)); am = FIT(np.stack([alpha * 255] * 3, 2), focus, zoom)[..., 0] / 255; am = cv2.GaussianBlur(am, (0, 0), 1.2)[..., None]
T = gbig(base.copy(), ['twenty years', 'as the woman', 'behind the founder'], PINK, 104, y=90, lh=1.0, glow='#B48CF0', ga=.6, shadow=.45)
T4 = gbig(base.copy(), ['now the founder'], PINK, 104, y=90 + 3 * 104, lh=1.0, glow='#B48CF0', ga=.6, shadow=.45)
a4 = np.clip(np.abs(T4 - base).max(2) / 40.0, 0, 1)                                                              # where the last line was drawn
core = (np.abs(T4 - base).max(2) > 110).astype(float); rows = np.where(core.max(1) > 0)[0]; y0_, y1_ = rows.min(), rows.max(); prof = core[y0_:y1_].max(0)
cols = np.where(prof > 0)[0]; gaps = [(cols[i + 1] - cols[i], cols[i]) for i in range(len(cols) - 1) if cols[i + 1] - cols[i] > 12]
split = sorted(gaps)[-1][1] + 6                                                                                     # the space between 'the' and 'founder'
M = np.float32([[1, 0, 80], [0, 1, 0]]); T4s = cv2.warpAffine(T4, M, (W, H), borderMode=cv2.BORDER_REPLICATE); a4s = cv2.warpAffine(a4, M, (W, H), borderMode=cv2.BORDER_CONSTANT, borderValue=0)
keepL = a4.copy(); keepL[:, split:] = 0; moveR = a4s.copy(); moveR[:, :split + 80] = 0
T = T * (1 - keepL[..., None]) + T4 * keepL[..., None]; T = T * (1 - moveR[..., None]) + T4s * moveR[..., None]     # 'now the' stays, only 'founder' moves right
out = T * (1 - am) + base * am; out = finish(out, 9, .25, 3); out = foot(out, 1000, .55, 220); im = pil(out)
text(im, "I ran other people's companies for twenty years and I was really good at it, and in all that time nobody ever asked me who the company was, only what it was making", 'serif', 27, 72, 1180, col=IVORY, maxw=860, align='c', lh=1.3); numb(im, 4, IVORY); pages[4] = im

# 05 Phyli · her screenshot, as it is. the page takes the screenshot's own white; the words sit above and below it
shot = Image.open('brand/phyli_lily_screenshot.jpg').convert('RGB'); bgc = tuple(int(v) for v in np.asarray(shot)[5:40, 5:40].reshape(-1, 3).mean(0))
im = Image.new('RGB', (W, H), bgc); sw = 1080; shot = shot.resize((sw, int(shot.size[1] * sw / shot.size[0])), Image.LANCZOS)
sy = int((H - shot.size[1]) / 2) + 20; im.paste(shot, (0, sy))
chap(im, 'ii  ·  the claim', PERI)
PX = 170   # the left edge of the P in the screenshot
HEADCOL = globals().get('HEADCOL', GREEN)
yh = text(im, "now,", 'display', 124, PX, 160, col=HEADCOL, maxw=900, align='l', lh=1.0)
text(im, "I'm making", 'display', 124, PX, yh + 6, col=HEADCOL, maxw=900, align='l', lh=1.0)
y = text(im, "the business book I wish someone had handed me at twenty-five", 'serif', 32, 72, sy + 590, col=INKC, maxw=820, align='c', lh=1.36)
text(im, "twelve volumes, a different part of your company in each one, and every one of them turns to nature for the answer, because that's where I've always found it", 'serif', 28, 72, y + 30, col=AUB, maxw=760, align='c', lh=1.4); numb(im, 5, QUIET); pages[5] = im

# 06 the book · the couture fabric itself, deep and soft, ivory serif, nothing else
a = load('g30/src/mum0.jpg', (.5, .5), 1.25); a = a * .55 + np.array([44, 26, 40.]) * .25; a = light(a, 540, 500, 800, .22, (255, 230, 240)); a = finish(a, 7, .32, 6)
im = pil(a); chap(im, 'ii  ·  the claim', PLUMT)
y = text(im, "the most beautiful\nbusiness book\nin the world", 'display', 88, 72, 330, col=IVORY, maxw=936, align='c', lh=1.04)
y = text(im, "pages that open out, lift and unfold the way the books we loved as children did, made from couture fabric by masters of paper, leather and binding", 'serif', 31, 72, y + 50, col=(240, 232, 236), maxw=820, align='c', lh=1.4)
text(im, "a book you keep, and hand down", 'italic', 34, 72, y + 34, col=(240, 232, 236), maxw=820, align='c', lh=1.3); numb(im, 6, PLUMT); pages[6] = im

# 07 the dream · the rose under the faint portrait, pink bold
a = load('g30/src/art3.jpg', (.5, .5), 1.0) * .55 + np.array(IVORY, float) * .45; a = a * .84 + PA * .16; a = light(a, 540, 300, 700, .3); a = finish(a, 7, .22, 8)
a = gbig(a, ['for the founder', 'who consults', 'the Universe,', 'and still has to', 'explain the numbers', 'to her CFO'], '#C96AA8', 84, y=460, lh=1.0, glow='#F6E2EC', ga=.6, shadow=0); im = pil(a)
text(im, "my dream is to launch her in an art gallery, the collectors' volumes numbered and bound by hand, MoMA's bookshop, Vogue", 'serif', 31, 72, 270, col=AUB, maxw=860, align='c', lh=1.3); numb(im, 7, QUIET); pages[7] = im

# 08 wisdom · the b&w headscarf with the grade; bold pink lead, quiet line small
a = bwgrade(load('g30/src/faye20.jpg', (.72, .4), 1.15)); a = foot(a, 600, .62, 280); a = finish(a, 10, .2, 8)
a = gbig(a, ['because the women', 'building thoughtful', 'companies deserve'], PINK, 78, y=680, lh=1.0, glow='#B48CF0', ga=.6, shadow=.45); im = pil(a)
text(im, "wisdom that doesn't shout", 'italic', 44, 72, 950, col=IVORY, maxw=900, align='c', lh=1.1)
text(im, "because I needed it and couldn't find it, because this has felt channelled for a long time, and I'd rather be the hands than argue with it", 'serif', 27, 72, 1050, col=(226, 216, 222), maxw=820, align='c', lh=1.34); numb(im, 8, IVORY); pages[8] = im

# 09 daughter · dark painting (the pink one sunk into plum), the root flower in white
im = pil(dark_surface('art91', 1.1, 9, 760, 400)); mask_on(im, inkmask('IMG_1631'), 460, W - 72 - 460, H - 600, (236, 226, 232), .85)
chap(im, 'iii  ·  why', PLUMQ)
y = text(im, "and because one day my daughter will ask", 'serif', 32, 72, 330, col=PLUMT, maxw=900, align='l', lh=1.3)
y = text(im, "what I made\nwith my life", 'display', 108, 72, y + 24, col=IVORY, maxw=936, align='l', lh=1.02)
highlight(im, "I want the answer to be beautiful", 'serif', 32, 72, y + 44, INKC); numb(im, 9, PLUMQ); pages[9] = im

# 10 truth care craft · the watercolour under the faint portrait
a = load('g30/src/art87.jpg', (.5, .5), 1.1) * .45 + np.array(IVORY, float) * .55; a = a * .84 + PA * .16; a = light(a, 540, 420, 700, .3); a = finish(a, 7, .22, 10)
a = gbig(a, ['truth, care, craft'], '#C96AA8', 104, y=420, lh=1.0, glow='#F6E2EC', ga=.6, shadow=0); im = pil(a)
text(im, "I care about", 'serif', 32, 72, 350, col=AUB, maxw=900, align='c', lh=1.3)
y = text(im, "and work that outlives the week it was posted in\n\nI'm not trying to be fast, I'm trying to be aligned, and connected", 'serif', 31, 72, 620, col=AUB, maxw=820, align='c', lh=1.4)
highlight(im, "not hacks, not hustle, not being everywhere", 'italic', 29, 0, y + 28, AUB, align='c'); numb(im, 10, QUIET); pages[10] = im

# 11 Indigo video (from v5)
shutil.copy('send/manifesto/v5/Manifesto_11_video.mp4', f'{OUT}/Manifesto_11_video.mp4'); pages[11] = Image.open('send/manifesto/v5/Manifesto_11.jpg')

# 12 for you · her pastel paper, the one flourish, one stay, the fairy filled
im = pil(cream_surface('p10', None, 1.7, .5, .0, 300, 300, 12))
d = ImageDraw.Draw(im); t = 'IV  ·  FOR YOU'; f = F('mono', 16); tw = sum(d.textlength(ch, font=f) for ch in t) + 16 * .36 * (len(t) - 1); spaced(d, (72, 92), t, f, PERI, .36)
rs = np.random.RandomState(5); pts = [(66 + i * 5, 128 + math.sin(i / 7) * 2 + rs.randn() * .6) for i in range(int((tw + 16) / 5))]; d.line(pts, fill=INKC, width=4, joint='curve')
s_ = 280 / sp.size[0]; a_s = sp.resize((int(sp.size[0] * s_), int(sp.size[1] * s_)), Image.LANCZOS); arr = np.asarray(a_s); cols = np.where(arr.max(0) > 60)[0]; xf = cols[0]; rows = np.where(arr[:, xf:xf + 12].max(1) > 60)[0]; im.paste(Image.new('RGB', a_s.size, INKC), (int(pts[-1][0] - xf - 6), int(128 - rows.mean())), a_s)
y = text(im, "if you're the one who remembers, decides, follows up and fixes everything\n\nif you built something out of taste and now spend your days defending it with numbers", 'serif', 31, 72, 300, col=INKC, maxw=820, align='l', lh=1.4)
y = text(im, "if your supply chain runs like clockwork", 'serif', 31, 72, y + 26, col=INKC, maxw=820, align='l', lh=1.4)
y = highlight(im, "and you still can't take a week off", 'serif', 31, 72, y + 4, INKC)
y = text(im, "stay", 'display', 120, 72, y + 20, col=PERI, maxw=900, align='l', lh=1.0)
y = text(im, "and if you're here because you love me, being here is support, and I feel it", 'italic', 30, 72, y + 30, col=QUIET, maxw=700, align='l', lh=1.3)
y = text(im, "thank you for watching\nme do the thing", 'display', 50, 72, y + 30, col=INKC, maxw=700, align='l', lh=1.04); dot(im, 86, y + 44)
a_f = fairy.copy(); sf = 320 / a_f.size[1]; a_f = a_f.resize((int(a_f.size[0] * sf), 320), Image.LANCZOS)
fl = load('g30/src/art84.jpg', (.5, .5), 1.0); fl = cv2.resize(fl, a_f.size); mn = fl.mean(); fl = np.clip((fl - mn) * 1.3 + mn * .5, 0, 255); im.paste(pil(fl), (W - 72 - a_f.size[0], H - 110 - 320), a_f)
numb(im, 12, QUIET); pages[12] = im

for i in range(1, 13): pages[i].save(f'{OUT}/Manifesto_{i:02d}.jpg', quality=93)
tiles = [pages[i].resize((270, 338)) for i in range(1, 13)]
Sh = Image.new('RGB', (4 * 270, 3 * 338), (30, 30, 30))
for i, t in enumerate(tiles): Sh.paste(t, ((i % 4) * 270, (i // 4) * 338))
Sh.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
