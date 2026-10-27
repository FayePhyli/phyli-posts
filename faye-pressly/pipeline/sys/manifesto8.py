"""the manifesto, seven slides, v3: approved cover; lighter ombré; HER ink drawings lifted straight off the paper (no digital masks); humour carried by the type."""
import sys, os; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import *
import cv2
G = 'g30/src/'; S = 'sys/src/'; OUT = 'sys/week1/manifesto8'; os.makedirs(OUT, exist_ok=True)
ROSE = (196, 110, 128); N = 7
def light(seed): return pil(pearl(seed=seed) * 0.72 + np.array(IVORY, float) * 0.28)        # lighter ombré
def realink(base, name, fill, w, cx, cy, op=1.0, tone=0.8, crop=(0, 0, 1, 1), rot=0):
    """fill = RGB tuple (plain ink) or np image (photo behind the ink). crop = fractional box of the mask to keep"""
    a = Image.open(f'ink/masks/{name}.png'); W0, H0 = a.size; a = a.crop((int(crop[0] * W0), int(crop[1] * H0), int(crop[2] * W0), int(crop[3] * H0)))
    s = w / a.size[0]; a = a.resize((int(a.size[0] * s), int(a.size[1] * s)), Image.LANCZOS)
    if rot: a = a.rotate(rot, expand=True, resample=Image.BICUBIC)
    a = a.point(lambda v: int(v * op))
    if isinstance(fill, tuple): layer = Image.new('RGB', a.size, fill)
    else:
        f_ = fit(fill, a.size[0], a.size[1]); m_ = f_.mean(); layer = pil((f_ - m_) * 1.2 + m_ * tone)
    out = base.copy(); out.paste(layer, (int(cx - a.size[0] / 2), int(cy - a.size[1] / 2)), a); return out
def plab(im, lab, dark=False): label(im, lab, IVORY if dark else INK)

out = [Image.open('fp/site/m/01.jpg').convert('RGB').resize((W, H))]                              # 01 · approved cover

# 02 · a beautiful photograph (the stairs), one ordinary line
im = pil(img(G + 'faye33.jpg', W, H, (.5, .3), 1.0)); im = vignette(darken(im, .05, .5), .2); plab(im, 'ii', True)
im, y = shadowed(im, "a little update,", 'display', 56, 72, 1110, maxw=940)
text(im, "because you're about to see more of\nwhat I'm working on here.", 'sans', 30, 72, y + 14, col=IVORY, maxw=900, lh=1.3); num(im, 2, N); out.append(im)

# 03 · twenty years (the eye, her ink, plain)
im = light(303); plab(im, 'iii'); im = realink(im, 'IMG_1631', INK, 620, 700, 330, op=.92)
y = text(im, "for almost twenty years\nI've worked on the inside\nof other people's companies.", 'display', 50, 72, 690, col=INK, maxw=920, lh=1.1)
text(im, "how people work together. who's responsible for what. why everything somehow ends up back with the *founder*.", 'sans', 30, 72, y + 28, col=INK, maxw=880, lh=1.34, acc=ROSE, acc_scale=1.1)
num(im, 3, N, INK); out.append(im)

# 04 · something of my own (the horse, her ink, with a photograph behind it)
im = light(304); plab(im, 'iv'); im = realink(im, 'IMG_1636', img(S + 'kimono_balcony.jpg', 1000, 1000, (.5, .4), 1.3), 760, 600, 960, op=.97, tone=.7, crop=(0, 0, 1, .92))
y = text(im, "now I'm bringing what I know\ninto something of my own.", 'display', 50, 72, 300, col=INK, maxw=920, lh=1.1)
text(im, "it's called *Phyli*.", 'sans', 34, 72, y + 26, col=INK, maxw=880, acc=ROSE, acc_kind='display', acc_scale=1.15)
num(im, 4, N, INK); out.append(im)

# 05 · the book dream, on the making
im = pil(img(S + 'studio_floor.jpg', W, H, (.5, .5), 1.0)); im = vignette(darken(im, .25, .62), .3); plab(im, 'v', True)
im, y = shadowed(im, "I want to make the most\nbeautiful business book\nin the world.", 'display', 54, 72, 880, maxw=940, lh=1.08)
text(im, "twelve volumes. pages that open out, lift and unfold, the way the books we loved as children did. books you want to touch, keep and actually read.", 'sans', 29, 72, y + 22, col=IVORY, maxw=900, lh=1.34)
num(im, 5, N); out.append(im)

# 06 · the honest page: the joke is in the type
im = light(306); plab(im, 'vi'); im = realink(im, 'IMG_1634', INK, 260, 820, 1010, op=.9, crop=(0, 0, 1, .9))
y = text(im, "writing that down in public\nmakes me feel slightly sick.", 'display', 46, 72, 300, col=INK, maxw=920, lh=1.1)
y = text(im, "I give no fucks now.", 'display', 68, 72, y + 60, col=INK, maxw=920)
d = ImageDraw.Draw(im); d.text((W - 72, y + 4), "(well. about ninety-five percent.)", font=F('italic', 30), fill=QUIET, anchor='ra'); y += 70
y = text(im, "the other five is still there,\nand I'm doing it anyway.", 'sans', 30, 72, y + 30, col=INK, maxw=860, lh=1.34)
y = text(im, "alongside being Indigo's mother, which is\nthe most important work I'll ever do.", 'sans', 30, 72, y + 30, col=INK, maxw=860, lh=1.34)
d.text((72, y + 40), "you'll probably watch me change my mind.", font=F('italic', 28), fill=QUIET)
num(im, 6, N, INK); out.append(im)

# 07 · seal: the root flower, her ink, the pink dance behind it
im = light(307); im = realink(im, 'IMG_1628', img(S + 'pink_dance.jpg', 1000, 1000, (.5, .4), 1.2), 440, 540, 400, op=.97, tone=.8, crop=(0, 0, 1, .93))
d = ImageDraw.Draw(im); dot(im, W / 2, 740); spaced(d, (W / 2, 780), 'faye pressly  ·  founder, phyli', F('mono', 16), QUIET, .2, 'c')
text(im, "if you're here because you know me\nand want to watch this happen,\nI'm really glad you're here.", 'display', 44, 72, 850, col=INK, maxw=940, align='c', lh=1.12)
text(im, "the work lives at @phyli.studio.\nthis is where it's made.", 'italic', 30, 72, 1090, col=QUIET, maxw=940, align='c', lh=1.3)
num(im, 7, N, INK); out.append(im)

for i, im in enumerate(out): im.save(f'{OUT}/Manifesto_{i+1:02d}.jpg', quality=92)
tiles = [cv2.resize(cv2.imread(f'{OUT}/Manifesto_{i+1:02d}.jpg'), (300, 375)) for i in range(N)] + [np.full((375, 300, 3), 30, np.uint8)]
cv2.imwrite(f'{OUT}/sheet.jpg', np.vstack([np.hstack(tiles[i:i+4]) for i in (0, 4)])); print('ok')
