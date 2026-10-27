"""manifesto v3 on the website spine, her notes applied: grounds vary (her art photos), inks filled with colour, the cover-style photo page for 02,
the Indigo camcorder video on 11, one underline-into-flower on the last page only, one 'stay'."""
import sys, os, subprocess; sys.path.insert(0, 'sys')
from style import *
import cv2
G = {}; exec(open('g60/build.py').read(), G)
srcf = open('g60/final.py').read(); exec(srcf[srcf.index('def big'):srcf.index('T=[None]*21')].replace('def big(', 'def gbig('), G)
grade, FIT, gbig, IV = G['grade'], G['F'], G['gbig'], G['IV']
OUT = 'send/manifesto/v3'; os.makedirs(OUT, exist_ok=True)
INKC = (28, 22, 26); PERI = (58, 62, 138); AUB = (70, 40, 60); N = 12
fairy = Image.open('sys/week1/fairy/fairy_mask.png').convert('L'); rootf = Image.open('fp/web/rootflower_a.png').convert('L')

# ---- the flourish: her sprig, base cropped off, cleaned, stem horizontal, flower at the right ----
sp = Image.open('fp/web/sprig_a.png').convert('L'); bb = sp.point(lambda v: 255 if v > 40 else 0).getbbox(); sp = sp.crop(bb)
sp = sp.crop((0, 0, sp.size[0], int(sp.size[1] * .78)))                       # drop the ground line at the base
sp = sp.filter(ImageFilter.GaussianBlur(1.6)).point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.GaussianBlur(0.8))
sp = sp.rotate(-90, expand=True, resample=Image.BICUBIC)                      # stem on the left, flower on the right
def line_into_flower(im, x0, x1, y, col=INKC, seed=3, width=4, fw=300):
    """one hand-drawn line that runs into the sprig: the stem starts where the line ends"""
    d = ImageDraw.Draw(im); rs = np.random.RandomState(seed); pts = []; n = int((x1 - x0) / 5)
    for i in range(n + 1):
        t = i / n; pts.append((x0 + (x1 - x0) * t, y + math.sin(t * 7 + seed) * 2.0 + rs.randn() * 0.6))
    d.line(pts, fill=col, width=width, joint='curve')
    s = fw / sp.size[0]; a = sp.resize((int(sp.size[0] * s), int(sp.size[1] * s)), Image.LANCZOS)
    # the stem's y inside the sprig: find the row where the leftmost ink sits
    arr = np.asarray(a); cols = np.where(arr.max(0) > 60)[0]; x_first = cols[0]; rows = np.where(arr[:, x_first:x_first + 12].max(1) > 60)[0]; stem_y = int(rows.mean())
    im.paste(Image.new('RGB', a.size, col), (int(x1 - x_first - 6), int(y - stem_y)), a)

def paper(seed=7):
    a = np.ones((H, W, 3), np.float32) * np.array(IVORY, np.float32); rs = np.random.RandomState(seed); a += rs.randn(H, W, 1) * 2.4; return pil(a)
def ground(name, lift=.3, focus=(.5, .5), zoom=1.0, cool=True):
    a = FIT(np.array(Image.open(f'g30/src/{name}.jpg').convert('RGB')).astype(float), focus, zoom)
    if cool: a = a * np.array([0.98, 0.99, 1.03])
    return pil(a * (1 - lift) + np.array(IVORY, float) * lift)
def mask_on(im, m, w, x, y, col=INKC, op=1.0):
    s = w / m.size[0]; a = m.resize((int(m.size[0]*s), int(m.size[1]*s)), Image.LANCZOS).point(lambda v: int(v*op)); im.paste(Image.new('RGB', a.size, col), (int(x), int(y)), a); return a.size
def mask_fill(im, m, w, x, y, src, tone=.7, op=.95):
    """ink drawing filled with one of her images, darkened so it still reads as ink"""
    s = w / m.size[0]; a = m.resize((int(m.size[0]*s), int(m.size[1]*s)), Image.LANCZOS).point(lambda v: int(v*op))
    f = FIT(np.array(Image.open(f'g30/src/{src}.jpg').convert('RGB')).astype(float), (.5, .5), 1.0, )
    f = cv2.resize(f, a.size); mn = f.mean(); f = np.clip((f - mn) * 1.3 + mn * tone, 0, 255)
    im.paste(pil(f), (int(x), int(y)), a); return a.size
def inkmask(name):
    a = Image.open(f'ink/masks/{name}.png').convert('L') if os.path.exists(f'ink/masks/{name}.png') else Image.open(f'fp/web/{name}_a.png').convert('L'); return a
def chapter(im, t, y=150, col=INKC):
    d = ImageDraw.Draw(im); spaced(d, (W / 2, y), t.upper(), F('mono', 17), col, .36, 'c')
def numb(im, i, col=QUIET): spaced(ImageDraw.Draw(im), (W - 72, H - 84), f'{i:02d} / {N:02d}', F('mono', 15), col, .18, 'r')
def big(im, t, y, size=66, col=INKC): return text(im, t, 'display', size, 72, y, col=col, maxw=936, align='c', lh=1.04)
def body(im, t, y, size=31, col=INKC): return text(im, t, 'serif', size, 72, y, col=col, maxw=860, align='c', lh=1.38)
def ital(im, t, y, size=30, col=QUIET): return text(im, t, 'italic', size, 72, y, col=col, maxw=860, align='c', lh=1.32)
def measure(fn): return fn(Image.new('RGB', (W, H)), 0)
def centred(im, fn, dy=-20): h = measure(fn); fn(im, (H - h) / 2 + dy); return im
def cover_style(path, lines, size, y, focus=(.5, .4), zoom=1.0, glow='#B48CF0', small=None, up=1.0):
    a = np.array(Image.open(path).convert('RGB')).astype(float)
    if up != 1.0: a = cv2.resize(a, None, fx=up, fy=up, interpolation=cv2.INTER_LANCZOS4)
    a = grade(FIT(a, focus, zoom), warm=.02, sat=1.08, bloom=.3, grain=8)
    a = gbig(a, lines, IV, size, y=y, lh=1.0, glow=glow, ga=.5, shadow=.4)
    if small: a = gbig(a, small[0], IV, small[1], y=small[2], lh=1.08, glow=glow, ga=.45, shadow=.4)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
pages = {}

# 01 cover
pages[1] = cover_style('fp/web/portrait.png', ['a note,', 'before this', 'page changes'], 112, 975, (.58, .45), 1.0, up=1.9)
# 02 who: the stairs photo in the cover style
pages[2] = cover_style('g30/src/faye33.jpg', ['twenty years', 'as the woman', 'behind the founder', 'now the founder'], 92, 120, (.5, .55), 1.0, small=(['in all that time nobody ever asked me', 'who the company was,', 'only what it was making'], 40, 1110))
spaced(ImageDraw.Draw(pages[2]), (W - 72, H - 84), '02 / 12', F('mono', 15), IVORY, .18, 'r')
# 03 ugly: ivory
im = paper(3); chapter(im, 'i  ·  who')
def f3(im, y):
    y = body(im, "I don't know about you, but my experience of learning about business has been", y, 34)
    y = big(im, "pretty fucking ugly", y + 24, 96)
    return body(im, "the greys, the oranges, the fonts, the tone, one more list of things to implement before Monday\n\nevery business book I was ever given looked like a tax return", y + 50, 31)
centred(im, f3, 10); numb(im, 3); pages[3] = im
# 04 the claim: ivory, the root flower filled with the coral painting
im = paper(4); chapter(im, 'ii  ·  the claim')
def f4(im, y):
    y = body(im, "I wanted a theory of the organisation with", y, 34)
    y = big(im, "a womb, a nervous system\nand a backbone", y + 24, 72)
    return body(im, "a business is not a machine to be extracted from, she is a living thing, she has seasons, she has moods, she heals\n\nnature solved all of this a long time ago, nobody wrote it down beautifully", y + 50, 31)
centred(im, f4, -40); mask_fill(im, rootf, 230, 40, H - 560, 'art84', tone=.62); numb(im, 4); pages[4] = im
# 05 Phyli: pastel stripes
im = ground('p10', .3, (.5, .45), 1.7); chapter(im, 'ii  ·  the claim', col=AUB)
def f5(im, y):
    y = big(im, "now, I'm making Phyli", y, 92, PERI)
    y = body(im, "the business book I wish someone had handed me at twenty-five", y + 40, 34, AUB)
    return body(im, "twelve volumes, a different part of your company in each one, and every one of them turns to nature for the answer, because that's where I've always found it", y + 30, 31, AUB)
centred(im, f5); numb(im, 5, AUB); pages[5] = im
# 06 the book: the brocade, darkened, ivory type
a = FIT(np.array(Image.open('g30/src/mum0.jpg').convert('RGB')).astype(float), (.5, .5), 1.2); a = a * .62; im = pil(a); chapter(im, 'ii  ·  the claim', col=IVORY)
def f6(im, y):
    y = big(im, "the most beautiful\nbusiness book\nin the world", y, 84, IVORY)
    y = body(im, "pages that open out, lift and unfold the way the books we loved as children did, made from couture fabric by masters of paper, leather and binding", y + 40, 31, IVORY)
    return ital(im, "adult books stopped being beautiful a long time ago, this is the opposite of that, a book you keep and hand down", y + 30, 29, (236, 226, 232))
centred(im, f6, 10); numb(im, 6, IVORY); pages[6] = im
# 07 the dream: the rose, lifted, the question in periwinkle
im = ground('art3', .35, (.5, .5), 1.0); chapter(im, 'iii  ·  the dream', col=AUB)
def f7(im, y):
    y = body(im, "my dream is to launch it in an art gallery\nthe collectors' volumes, numbered and bound by hand, MoMA's bookshop, Vogue", y, 31, AUB)
    return text(im, "what if the most beautiful object on your shelf was also the one that fixed your Monday", 'italic', 62, 72, y + 70, col=PERI, maxw=900, align='c', lh=1.1)
centred(im, f7, 0); numb(im, 7, AUB); pages[7] = im
# 08 why: ivory, the eye ink filled with the pink painting
im = paper(8); chapter(im, 'iv  ·  why')
def f8(im, y):
    y = body(im, "because the women building thoughtful companies deserve", y, 34)
    y = big(im, "wisdom that doesn't shout", y + 20, 64)
    return body(im, "because I needed it and couldn't find it\n\nbecause this has felt channelled for a long time, and I'd rather be the hands than argue with it", y + 50, 31)
centred(im, f8, 60); mask_fill(im, inkmask('IMG_1631'), 360, W/2 - 180, 200, 'art91', tone=.6); numb(im, 8); pages[8] = im
# 09 daughter: pastel p05
im = ground('p05', .38, (.55, .5), 1.4); chapter(im, 'iv  ·  why', col=AUB)
def f9(im, y):
    y = big(im, "and because one day\nmy daughter will ask\nwhat I made with my life", y, 70, AUB)
    return big(im, "I want the answer\nto be beautiful", y + 50, 56, PERI)
centred(im, f9); numb(im, 9, AUB); pages[9] = im
# 10 truth care craft: ivory, the tiger filled with the pastel stripes
im = paper(10); chapter(im, 'v  ·  how')
def f10(im, y):
    y = body(im, "I care about", y, 34)
    y = big(im, "truth, care, craft", y + 20, 84)
    y = body(im, "and work that outlives the week it was posted in", y + 36, 34)
    y = ital(im, "not hacks, not hustle, not being everywhere", y + 40, 30)
    return body(im, "I'm not trying to be fast, I'm trying to be aligned, and connected", y + 30, 31)
centred(im, f10, -60); mask_fill(im, inkmask('IMG_4685'), 380, W/2 - 190, H - 420, 'p10', tone=.55); numb(im, 10); pages[10] = im
# 11 Indigo: camcorder video, cover grade
SRC = 'broll/px/IMG_7767.mp4'; wd = 'sys/r_man11'; os.makedirs(wd, exist_ok=True)
LOOK = "eq=contrast=1.15:saturation=1.45:gamma=0.94,colorbalance=rh=0.06:bh=-0.08:rs=-0.02:bs=0.05,split[a][b];[b]curves=all='0/0 0.55/0 1/1',gblur=sigma=20[g];[a][g]blend=all_mode=screen:all_opacity=0.5,gblur=sigma=1.1,noise=alls=10:allf=t+u[v];[v][1:v]overlay=format=auto"
vf = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}:'(iw-{W})*0.5':'(ih-{H})*0.3',fps=30,setsar=1,{LOOK}"
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '2.5', '-i', SRC, '-i', 'sys/grad.png', '-t', '7', '-filter_complex', vf, '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', f'{wd}/base.mp4'], check=True)
T1 = gbig(np.zeros((H, W, 3)), ['it will not', 'take over', 'my life'], '#FFFFFF', 104, y=110, lh=1.0, shadow=0)
T2 = gbig(np.zeros((H, W, 3)), ['the most important work', "I'll ever do is being", "Indigo's mother"], '#FFFFFF', 48, y=1100, lh=1.1, shadow=0)
A1 = (T1.mean(2) / 255)[..., None]; A2 = (T2.mean(2) / 255)[..., None]
G1 = np.clip(cv2.GaussianBlur(A1[..., 0], (0, 0), 16) * 1.8, 0, 1)[..., None] * .5; G2 = np.clip(cv2.GaussianBlur(A2[..., 0], (0, 0), 16) * 2.0, 0, 1)[..., None] * .6
IVa = np.array(IVORY, float); GL = np.array([150, 110, 210.])
FS = W * H * 3; dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', f'{wd}/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-shortest', '-movflags', '+faststart', f'{OUT}/Manifesto_11_video.mp4'], stdin=subprocess.PIPE)
first = None
for fi in range(7 * 30):
    raw = dec.stdout.read(FS)
    if len(raw) < FS: break
    fr = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32); g = min(1, fi / 10)
    fr = fr * (1 - G1 * g) + GL * G1 * g; fr = fr * (1 - A1 * g) + IVa * A1 * g
    fr = fr * (1 - G2 * g) + GL * G2 * g; fr = fr * (1 - A2 * g) + IVa * A2 * g
    if fi == 40: first = fr.copy()
    enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); dec.stdout.close(); enc.wait()
im = Image.fromarray(np.clip(first, 0, 255).astype(np.uint8)); spaced(ImageDraw.Draw(im), (W - 72, H - 84), '11 / 12', F('mono', 15), IVORY, .18, 'r'); pages[11] = im
# 12 for you: ivory, the one underline that runs into the flower, one stay, the fairy filled with pastel
im = paper(12)
d = ImageDraw.Draw(im); t = 'VI  ·  FOR YOU'; f = F('mono', 17); tw = sum(d.textlength(ch, font=f) for ch in t) + 17 * .36 * (len(t) - 1)
spaced(d, (W / 2, 150), t, f, INKC, .36, 'c'); line_into_flower(im, W / 2 - tw / 2 - 10, W / 2 + tw / 2 + 10, 150 + 38, INKC, seed=5, width=4, fw=300)
def f12(im, y):
    y = body(im, "if you're the one who remembers, decides, follows up and fixes everything", y, 32)
    y = body(im, "if you built something out of taste and now spend your days defending it with numbers", y + 26, 32)
    y = body(im, "if your supply chain runs like clockwork and you still can't take a week off", y + 26, 32)
    y = big(im, "stay", y + 40, 110, PERI)
    y = ital(im, "and if you're here because you love me,\nbeing here is support, and I feel it", y + 40, 29)
    y = big(im, "thank you for watching\nme do the thing", y + 30, 50); dot(im, W / 2, y + 40); return y + 56
centred(im, f12, 40)
mask_fill(im, fairy, 190, W - 72 - 190, H - 110 - 300, 'p10', tone=.5)
numb(im, 12); pages[12] = im

for i in range(1, 13): pages[i].save(f'{OUT}/Manifesto_{i:02d}.jpg', quality=93)
tiles = [pages[i].resize((270, 338)) for i in range(1, 13)]
Sh = Image.new('RGB', (4 * 270, 3 * 338), (30, 30, 30))
for i, t in enumerate(tiles): Sh.paste(t, ((i % 4) * 270, (i // 4) * 338))
Sh.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
