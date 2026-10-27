"""the manifesto carousel as a sketchbook: five page types in rhythm (statement / photo / wash / object-ink / moving). cover = her chosen portrait tile."""
exec(open('g60/build.py').read())
src = open('g60/final.py').read(); exec(src[src.index('def big'):src.index('T=[None]*21')])
import sys, subprocess; sys.path.insert(0, 'sys'); import style as S
from style import spaced, text, dot, underline, fit, pil
SF = S.F
OUT = 'send/manifesto/v2'; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350; PERI = (58, 62, 138); AUB = (70, 40, 60); IVO = S.IVORY; N = 12
fairy = Image.open('sys/week1/fairy/fairy_mask.png').convert('L')

# ---------- grounds ----------
def paper(seed=7, tone=IVO):
    a = np.ones((H, W, 3), np.float32) * np.array(tone, np.float32); rs = np.random.RandomState(seed); a += rs.randn(H, W, 1) * 2.4; return pil(a)
def wash(name, lift=.2, crop=(0.10, 0.10, 0.90, 0.90), lilac=1.0):
    im = Image.open(f'art/new/{name}.jpg'); W0, H0 = im.size
    im = im.crop((int(crop[0]*W0), int(crop[1]*H0), int(crop[2]*W0), int(crop[3]*H0)))
    a = fit(np.asarray(im).astype(np.float32), W, H)
    m = a.reshape(-1, 3).mean(0); a = np.clip(a * (np.array([226, 196, 206], np.float32) / m), 0, 255)
    b = a.copy(); b[..., 2] = np.clip(b[..., 2] * (1 + .144 * lilac), 0, 255); b[..., 0] = np.clip(b[..., 0] * (1 - .04 * lilac), 0, 255)
    return pil(b * (1 - lift) + np.array(IVO, np.float32) * lift)
def scribble(name='IMG_7465', lift=.55):
    im = Image.open(f'art/new/{name}.jpg'); W0, H0 = im.size; im = im.crop((int(.12*W0), int(.10*H0), int(.88*W0), int(.80*H0)))
    a = fit(np.asarray(im).astype(np.float32), W, H); a = cv2.GaussianBlur(a, (0, 0), 1.2)
    return pil(a * (1 - lift) + np.array(IVO, np.float32) * lift)
def photo(path, focus=(.5, .4), zoom=1.0, **kw):
    a = np.array(Image.open(path).convert('RGB')).astype(float); return grade(F(a, focus, zoom), **kw)
def inkmark(im, name, w, cx, cy, col=S.INK, op=.92, crop=(0, 0, 1, 1)):
    a = Image.open(f'ink/masks/{name}.png').convert('L'); W0, H0 = a.size; a = a.crop((int(crop[0]*W0), int(crop[1]*H0), int(crop[2]*W0), int(crop[3]*H0)))
    s = w / a.size[0]; a = a.resize((int(a.size[0]*s), int(a.size[1]*s)), Image.LANCZOS).point(lambda v: int(v*op))
    im.paste(Image.new('RGB', a.size, col), (int(cx - a.size[0]/2), int(cy - a.size[1]/2)), a); return im
def put_fairy(im, h, x, y, col=AUB):
    a = fairy.copy(); s = h / a.size[1]; a = a.resize((int(a.size[0]*s), int(a.size[1]*s)), Image.LANCZOS); im.paste(Image.new('RGB', a.size, col), (x, y), a); return im

# ---------- furniture ----------
def label(im, col=AUB): spaced(ImageDraw.Draw(im), (72, 92), 'faye pressly  ·  a note, before this page changes', SF('mono', 15), col, .28)
def numb(im, i, col=AUB, side='r'):
    d = ImageDraw.Draw(im)
    if side == 'r': spaced(d, (W - 72, H - 84), f'{i:02d} / {N:02d}', SF('mono', 15), col, .18, 'r')
    else: spaced(d, (72, H - 84), f'{i:02d} / {N:02d}', SF('mono', 15), col, .18)
def margin(im, t, col=AUB, side='l', y=None):
    """the italic aside as a margin note, off-centre"""
    y = H - 300 if y is None else y
    if side == 'l': text(im, t, 'italic', 30, 72, y, col=col, maxw=520, align='l', lh=1.3)
    else: text(im, t, 'italic', 30, W - 72 - 520, y, col=col, maxw=520, align='r', lh=1.3)
def statement(im, t, size, col=PERI, y=None):
    """one line, enormous, centred vertically"""
    tmp = Image.new('RGB', (W, H)); h = text(tmp, t, 'display', size, 72, 0, col=col, maxw=936, align='c', lh=1.0)
    return text(im, t, 'display', size, 72, (H - h) / 2 - 40 if y is None else y, col=col, maxw=936, align='c', lh=1.0)
def bodyc(im, t, y, size=34, col=AUB): return text(im, t, 'serif', size, 72, y, col=col, maxw=880, align='c', lh=1.38)
def headc(im, t, y, size=62, col=PERI): return text(im, t, 'display', size, 72, y, col=col, maxw=930, align='c', lh=1.06)
def block(im, fn, dy=-30):
    h = fn(Image.new('RGB', (W, H)), 0); fn(im, (H - h) / 2 + dy); return im
out = {}

# 01 cover: her chosen portrait tile
por = np.array(Image.open('fp/web/portrait.png').convert('RGB')).astype(float)
up = cv2.resize(por, None, fx=1.9, fy=1.9, interpolation=cv2.INTER_LANCZOS4)
a = grade(F(up, (.58, .45)), warm=.02, sat=1.08, bloom=.3, grain=8)
A = big(a, ['a note,', 'before this', 'page changes'], IV, 112, y=975, glow='#B48CF0', ga=.5, shadow=.4)
out[1] = Image.fromarray(np.clip(A, 0, 255).astype(np.uint8))

# 02 statement
im = paper(2); y = statement(im, "for almost twenty years\nI've run and grown\nthe inside of companies,\nfor other people", 78)
label(im); numb(im, 2); out[2] = im

# 03 photo: the mirror selfie, grid sans
a = photo('broll/new_stills/IMG_7390.jpg', (.5, .35), 1.0, warm=.03, sat=1.08, bloom=.3)
a = big(a, ["I've spent the", 'last two years', "watching everyone", "else's stories", 'from today', "I'm making mine"], IV, 92, lh=1.0, glow='#B48CF0', ga=.5, shadow=.4)
im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); numb(im, 3, IVO, 'l'); out[3] = im

# 04 wash: I'm making Phyli
im = wash('IMG_7450')
def f4(im, y):
    y = headc(im, "I'm making Phyli", y, 92)
    return bodyc(im, "a place for what I know to come to life,\nfor women running and growing their own\ncompanies as if they are alive", y + 44)
block(im, f4, -80); margin(im, "because they are", side='r'); label(im); numb(im, 4); out[4] = im

# 05 object / ink: the root flower, the book
im = paper(5); im = inkmark(im, 'IMG_1628', 520, W/2, 420, crop=(0, 0, 1, .93))
y = headc(im, "the most beautiful\nbusiness book in the world", 760, 60)
y = bodyc(im, "twelve volumes, pages that open, lift and unfold,\nthe way the books we loved as children did,\nmade by hand, from the materials of couture", y + 30, 31)
margin(im, "a business book you'd leave on the table\nbecause it's stunning, and then actually read", side='l', y=H - 250); label(im); numb(im, 5); out[5] = im

# 06 scribble ground: adult books
im = scribble()
def f6(im, y):
    y = headc(im, "adult books stopped being\nbeautiful a long time ago", y, 64, col=PERI)
    return bodyc(im, "made as cheap as possible,\nshipped to as many as possible\n\nthis is the opposite of that,\na book you keep, and hand down", y + 40, 34)
block(im, f6); label(im); numb(im, 6, side='l'); out[6] = im

# 07 statement: wisdom that doesn't shout
im = paper(7); statement(im, "wisdom that\ndoesn't shout", 120, PERI, 380)
bodyc(im, "because the women building thoughtful companies deserve it\nbecause I needed it and couldn't find it\nbecause this has felt channelled for a long time,\nand I'd rather be the hands than argue with it", 820, 30)
label(im); numb(im, 7); out[7] = im

# 08 photo: Indigo
a = photo('sys/mstills/indigo2.jpg', (.55, .45), 1.05, warm=.04, sat=1.05, bloom=.3)
a = big(a, ['one day', 'my daughter', 'will ask what', 'I made with', 'my life'], IV, 104, y=120, lh=1.0, glow='#F2B3A8', ga=.5, shadow=.4)
a = big(a, ['I want the answer', 'to be beautiful'], IV, 56, y=1120, lh=1.05, glow='#B48CF0', ga=.5, shadow=.4)
im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); numb(im, 8, IVO); out[8] = im

# 09 wash lilac: truth beauty craft
im = wash('IMG_7452', lift=.15, lilac=1.4)
def f9(im, y):
    y = headc(im, "I care about truth,\nbeauty, craft", y, 76)
    return bodyc(im, "and work that outlives\nthe week it was posted in", y + 40, 36)
block(im, f9, -60); margin(im, "hacks, hustle, being everywhere,\ngoing viral... no", side='l'); label(im); numb(im, 9); out[9] = im

# 10 moving: the mirror dance (video) + a still fallback
SRC = 'broll/px/IMG_7386.mp4'; wd = 'sys/r_man10'; os.makedirs(wd, exist_ok=True)
LOOK = "eq=contrast=1.12:saturation=1.3:gamma=0.95,colorbalance=rh=0.05:bh=-0.06:rs=-0.02:bs=0.04,split[a][b];[b]curves=all='0/0 0.55/0 1/1',gblur=sigma=22[g];[a][g]blend=all_mode=screen:all_opacity=0.45,noise=alls=6:allf=t+u[v];[v][1:v]overlay=format=auto"
vf = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}:'(iw-{W})*0.5':'(ih-{H})*0.3',fps=30,setsar=1,{LOOK}"
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '18', '-i', SRC, '-i', 'sys/grad.png', '-t', '7', '-filter_complex', vf, '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', f'{wd}/base.mp4'], check=True)
tmp = Image.new('RGB', (W, H), (0, 0, 0)); T1 = big(np.zeros((H, W, 3)), ['it will not', 'take over', 'my life'], '#FFFFFF', 112, y=120, lh=1.0, shadow=0)
T2 = big(np.zeros((H, W, 3)), ['the most important work', "I'll ever do is being", "Indigo's mother", 'so not everything here', 'will be perfect,', "beautifully imperfect,", 'occasionally cringe'], '#FFFFFF', 46, y=880, lh=1.12, shadow=0)
A1 = (T1.mean(2) / 255)[..., None]; A2 = (T2.mean(2) / 255)[..., None]
G1 = np.clip(cv2.GaussianBlur(A1[..., 0], (0, 0), 16) * 1.8, 0, 1)[..., None] * .5; G2 = np.clip(cv2.GaussianBlur(A2[..., 0], (0, 0), 18) * 2.2, 0, 1)[..., None] * .7
IVa = np.array(IVO, float); GL = np.array([110, 70, 150.])
FS = W * H * 3; dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', f'{wd}/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-shortest', '-movflags', '+faststart', f'{OUT}/Manifesto_10_video.mp4'], stdin=subprocess.PIPE)
first = None
for fi in range(7 * 30):
    raw = dec.stdout.read(FS)
    if len(raw) < FS: break
    fr = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32); g = min(1, fi / 10)
    fr = fr * (1 - G1 * g) + GL * G1 * g; fr = fr * (1 - A1 * g) + IVa * A1 * g
    fr = fr * (1 - G2 * g) + GL * G2 * g; fr = fr * (1 - A2 * g) + IVa * A2 * g
    if fi == 45: first = fr.copy()
    enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); dec.stdout.close(); enc.wait()
im = Image.fromarray(np.clip(first, 0, 255).astype(np.uint8)); numb(im, 10, IVO, 'l'); out[10] = im

# 11 statement: being seen never felt safe + the five percent in the corner
im = paper(11)
bodyc(im, "I've spent most of my life\nhelping other people shine\nit was real, it was also a hiding place", 300, 32)
statement(im, "being seen\nnever felt safe", 104, PERI, 560)
text(im, "I give no fucks now", 'display', 44, W - 72 - 600, 1040, col=AUB, maxw=600, align='r', lh=1.0)
text(im, "well, maybe five percent", 'italic', 28, W - 72 - 600, 1100, col=AUB, maxw=600, align='r')
label(im); numb(im, 11, side='l'); out[11] = im

# 12 the fairy, the stay
im = wash('IMG_7453', lift=.25)
def f12(im, y):
    y = headc(im, "this page is for women building\ncompanies with taste and ambition,\nand for anyone who loves one", y, 52)
    y = bodyc(im, "if that's you, stay", y + 36, 40)
    y = text(im, "and if you're here because you love me,\nbeing here is support, and I feel it", 'italic', 30, 72, y + 26, col=AUB, maxw=860, align='c', lh=1.3)
    y = bodyc(im, "thank you for watching me do the thing", y + 30, 34); dot(im, W/2, y + 48); return y + 64
block(im, f12, -120); im = put_fairy(im, 330, W - 72 - 175, H - 150 - 330); label(im); numb(im, 12); out[12] = im

for i in range(1, 13): out[i].save(f'{OUT}/Manifesto_{i:02d}.jpg', quality=93)
tiles = [out[i].resize((270, 338)) for i in range(1, 13)]
Sh = Image.new('RGB', (4 * 270, 3 * 338), (30, 30, 30))
for i, t in enumerate(tiles): Sh.paste(t, ((i % 4) * 270, (i // 4) * 338))
Sh.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
