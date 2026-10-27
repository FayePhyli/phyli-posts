"""the manifesto carousel, Wednesday: her copy (the long version she preferred), on the wash, treatment 5, Night Court system. cover = portrait on ivory (made in manifesto_cov.py)."""
import sys, os; sys.path.insert(0, 'sys')
from style import *
import cv2
OUT = 'send/manifesto/carousel'; os.makedirs(OUT, exist_ok=True)
PERI = (58, 62, 138); AUB = (70, 40, 60)
fairy = Image.open('sys/week1/fairy/fairy_mask.png').convert('L')
WASHES = ['IMG_7450', 'IMG_7452', 'IMG_7453', 'IMG_7454', 'IMG_7451', 'IMG_7457', 'IMG_7458', 'IMG_7459', 'IMG_7460', 'IMG_7461', 'IMG_7462']
def wash(name, crop=(0.10, 0.10, 0.90, 0.90)):
    im = Image.open(f'art/new/{name}.jpg'); W0, H0 = im.size
    im = im.crop((int(crop[0]*W0), int(crop[1]*H0), int(crop[2]*W0), int(crop[3]*H0)))
    a = fit(np.asarray(im).astype(np.float32), W, H)
    m = a.reshape(-1, 3).mean(0); a = np.clip(a * (np.array([226, 196, 206], np.float32) / m), 0, 255)
    b = a.copy(); b[..., 2] = np.clip(b[..., 2] * 1.144, 0, 255); b[..., 0] = np.clip(b[..., 0] * 0.96, 0, 255)
    return pil(b * 0.8 + np.array(IVORY, np.float32) * 0.2)
def label(im): spaced(ImageDraw.Draw(im), (W/2, 96), 'faye pressly  ·  a note, before this page changes', F('mono', 16), AUB, .3, 'c')
def numb(im, i, n): spaced(ImageDraw.Draw(im), (W - 72, H - 84), f'{i:02d} / {n:02d}', F('mono', 15), AUB, .18, 'r')
def head(im, t, y, size=62): return text(im, t, 'display', size, 72, y, col=PERI, maxw=930, align='c', lh=1.06)
def body(im, t, y, size=34): return text(im, t, 'serif', size, 72, y, col=AUB, maxw=880, align='c', lh=1.38)
def aside(im, t, y, size=31): return text(im, t, 'italic', size, 72, y, col=AUB, maxw=860, align='c', lh=1.3)
def measure(fn): return fn(Image.new('RGB', (W, H)), 0)
def centred(im, fn, dy=-30): h = measure(fn); fn(im, (H - h) / 2 + dy); return im
N = 12
def slide(i, fn, with_fairy=False):
    im = wash(WASHES[(i - 2) % len(WASHES)])
    if with_fairy:
        a = fairy.copy(); s = 300 / a.size[1]; a = a.resize((int(a.size[0]*s), int(a.size[1]*s)), Image.LANCZOS)
        im.paste(Image.new('RGB', a.size, AUB), (W - 72 - a.size[0], H - 150 - a.size[1]), a)
    im = centred(im, fn); label(im); numb(im, i, N); return im

def s2(im, y):
    y = head(im, "for almost twenty years\nI've run and grown the inside\nof companies, for other people", y)
    return body(im, "I've spent the last two years watching\neveryone else's stories\nfrom today I'm making mine", y + 40)
def s3(im, y):
    y = head(im, "I'm making Phyli", y, 84)
    y = body(im, "a place for what I know to come to life,\nfor women running and growing their own\ncompanies as if they are alive", y + 40)
    return aside(im, "because they are", y + 28)
def s4(im, y):
    y = head(im, "the most beautiful\nbusiness book in the world", y)
    y = body(im, "twelve volumes. pages that open, lift and unfold,\nthe way the books we loved as children did,\nmade by hand, from the materials of couture", y + 40)
    return aside(im, "a business book you'd leave on the table\nbecause it's stunning, and then actually read", y + 28)
def s5(im, y):
    y = head(im, "adult books stopped being\nbeautiful a long time ago", y)
    return body(im, "made as cheap as possible,\nshipped to as many as possible\nthis is the opposite of that,\na book you keep, and hand down", y + 40)
def s6(im, y):
    y = head(im, "because the women building\nthoughtful companies deserve\nwisdom that doesn't shout", y, 56)
    return body(im, "because I needed it and couldn't find it\nbecause this has felt channelled for a long time,\nand I'd rather be the hands than argue with it", y + 40)
def s7(im, y):
    y = head(im, "and because one day\nmy daughter will ask\nwhat I made with my life", y)
    return body(im, "I want the answer to be beautiful", y + 40)
def s8(im, y):
    y = head(im, "I care about truth,\nbeauty, craft", y, 72)
    y = body(im, "and work that outlives\nthe week it was posted in", y + 40)
    return aside(im, "hacks, hustle, being everywhere, going viral... no", y + 28)
def s9(im, y):
    y = head(im, "it will not take over my life", y, 60)
    y = body(im, "the most important work I'll ever do\nis being Indigo's mother", y + 40)
    return aside(im, "so not everything here will be perfect,\nit'll be beautifully imperfect, occasionally cringe", y + 28)
def s10(im, y):
    y = head(im, "I've spent most of my life\nhelping other people shine", y)
    return body(im, "it was real\nit was also a hiding place\nbeing seen never felt safe", y + 40)
def s11(im, y):
    y = head(im, "I give no fucks now", y, 84)
    return aside(im, "well, maybe five percent", y + 36)
def s12(im, y):
    y = head(im, "this page is for women building\ncompanies with taste and ambition,\nand for anyone who loves one", y, 54)
    y = body(im, "if that's you, stay", y + 40)
    y = aside(im, "and if you're here because you love me,\nbeing here is support, and I feel it", y + 28)
    y = body(im, "thank you for watching me do the thing", y + 30); dot(im, W/2, y + 50); return y + 70
out = [Image.open('send/manifesto/Manifesto_carousel_cover_WED.jpg')]
for i, fn in zip(range(2, 13), (s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12)): out.append(slide(i, fn, with_fairy=(i == 12)))
for i, im in enumerate(out): im.save(f'{OUT}/Manifesto_{i+1:02d}.jpg', quality=93)
tiles = [im.resize((270, 338)) for im in out]
S = Image.new('RGB', (4 * 270, 3 * 338), (30, 30, 30))
for i, t in enumerate(tiles): S.paste(t, ((i % 4) * 270, (i // 4) * 338))
S.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
