"""the manifesto, seven slides: approved cover from the grid, then pearl + image-filled ink interiors. one job: let people into what she's making."""
import sys, os; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import *
import cv2
G = 'g30/src/'; S = 'sys/src/'; OUT = 'sys/week1/manifesto7'; os.makedirs(OUT, exist_ok=True)
ROSE = (196, 110, 128); LILAC = (150, 122, 170); AUB = (92, 48, 78); PINKPALE = (232, 184, 194)
N = 7
def plab(im, lab, dark=False): label(im, lab, IVORY if dark else INK); fp(im, IVORY if dark else INK)

out = [Image.open('fp/site/m/01.jpg').convert('RGB').resize((W, H))]            # 01 · the approved cover

# 02 · a photograph of her, one ordinary sentence
im = pil(img(G + 'faye104.jpg', W, H, (.5, .35), 1.0)); im = vignette(darken(im, .15, .6), .25); plab(im, 'ii', True)
im, y = shadowed(im, "a little update,", 'display', 60, 72, 1100, maxw=940, lh=1.05)
text(im, "because you're about to see more of\nwhat I'm working on here.", 'sans', 31, 72, y + 18, col=IVORY, maxw=900, lh=1.3); num(im, 2, N); out.append(im)

# 03 · twenty years inside other people's companies (light pearl, ink filled with the stairs photo)
im = pil(pearl(seed=301)); plab(im, 'iii')
im = inkfill(im, 'ink_tree_spiral', img(G + 'faye33.jpg', 900, 900, (.5, .4), 1.3), 560, 760, 330, op=.96, tone=.68, bold=1)
y = text(im, "for almost twenty years\nI've worked on the inside\nof other people's companies.", 'display', 50, 72, 700, col=INK, maxw=920, lh=1.1)
y = text(im, "how people work together. who's responsible for what. why everything somehow ends up back with the *founder*.", 'sans', 30, 72, y + 28, col=INK, maxw=880, lh=1.34, acc=ROSE, acc_scale=1.1)
num(im, 3, N, INK); out.append(im)

# 04 · now something of my own (dark pearl, the name)
im = pil(pearl(seed=304, dark=True)); plab(im, 'iv', True)
im = inkfill(im, 'rootflower', img(G + 'faye98.jpg', 900, 900, (.5, .45), 1.2), 560, 540, 1200, op=.96, tone=1.05, bold=2)
y = text(im, "now I'm bringing what I know\ninto something of my own.", 'display', 50, 72, 380, col=IVORY, maxw=920, lh=1.1)
text(im, "it's called *Phyli*.", 'sans', 34, 72, y + 28, col=IVORY, maxw=880, acc=PINKPALE, acc_kind='display', acc_scale=1.15)
num(im, 4, N); out.append(im)

# 05 · the book dream, on the actual making (cards on the rug)
im = pil(img(S + 'studio_floor.jpg', W, H, (.5, .5), 1.0)); im = vignette(darken(im, .25, .62), .3); plab(im, 'v', True)
im, y = shadowed(im, "I want to make the most\nbeautiful business book\nin the world.", 'display', 54, 72, 880, maxw=940, lh=1.08)
text(im, "twelve volumes. pages that open out, lift and unfold, the way the books we loved as children did. books you want to touch, keep and actually read.", 'sans', 29, 72, y + 22, col=IVORY, maxw=900, lh=1.34)
num(im, 5, N); out.append(im)

# 06 · the honest bit (light pearl, small splat filled with her own ink)
im = pil(pearl(seed=306)); plab(im, 'vi')
im = inkfill(im, 'splat', img(G + 'art22.jpg', 700, 700, (.5, .5), 1.2), 460, 800, 1380, op=.92, tone=.7)
y = text(im, "writing that down in public\nmakes me feel slightly sick.", 'display', 50, 72, 420, col=INK, maxw=920, lh=1.1)
y = text(im, "I give no fucks now. well, about ninety-five percent. the other five is still there, and I'm doing it anyway.\n\nalongside being Indigo's mother, which is the most important work I'll ever do.", 'sans', 30, 72, y + 28, col=INK, maxw=860, lh=1.34)
ImageDraw.Draw(im).text((72, y + 34), "you'll probably watch me change my mind.", font=F('italic', 32), fill=QUIET)
num(im, 6, N, INK); out.append(im)

# 07 · warm ending, seal
im = pil(pearl(seed=307)); im = inkfill(im, 'sprig', img(S + 'pink_dance.jpg', 900, 900, (.5, .4), 1.2), 520, 540, 400, op=.96, tone=.7, bold=2)
d = ImageDraw.Draw(im); dot(im, W / 2, 740)
spaced(d, (W / 2, 780), 'faye pressly  ·  founder, phyli', F('mono', 16), QUIET, .2, 'c')
text(im, "if you're here because you know me\nand want to watch this happen,\nI'm really glad you're here.", 'display', 44, 72, 850, col=INK, maxw=940, align='c', lh=1.12)
text(im, "the work lives at @phyli.studio.\nthis is where it's made.", 'italic', 30, 72, 1090, col=QUIET, maxw=940, align='c', lh=1.3)
num(im, 7, N, INK); out.append(im)

for i, im in enumerate(out): im.save(f'{OUT}/Manifesto_{i+1:02d}.jpg', quality=92)
tiles = [cv2.resize(cv2.imread(f'{OUT}/Manifesto_{i+1:02d}.jpg'), (300, 375)) for i in range(N)] + [np.full((375, 300, 3), 30, np.uint8)]
cv2.imwrite(f'{OUT}/sheet.jpg', np.vstack([np.hstack(tiles[i:i+4]) for i in (0, 4)])); print('ok')
