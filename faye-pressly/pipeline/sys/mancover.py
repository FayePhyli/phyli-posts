"""manifesto cover: the website portrait on ivory, 'a note, before this page changes.' two versions: 4:5 grid tile and 9:16 reel cover."""
import sys, os; sys.path.insert(0, 'sys')
from style import *
OUT = 'sys/week1'; os.makedirs(OUT, exist_ok=True)
por = Image.open('fp/web/portrait.png').convert('RGB')

def build(W_, H_, name, pw, py, ty, size, sub_y):
    im = Image.new('RGB', (W_, H_), IVORY)
    # faint paper grain
    a = np.asarray(im).astype(np.float32); rs = np.random.RandomState(2); a += rs.randn(H_, W_, 1) * 2.2; im = pil(a)
    p = por.resize((pw, int(pw * por.size[1] / por.size[0])), Image.LANCZOS)
    # lift the portrait very slightly towards the ivory so it sits in the paper
    pa = np.asarray(p).astype(np.float32) * 0.96 + np.array(IVORY, np.float32) * 0.04; p = pil(pa)
    im.paste(p, ((W_ - pw) // 2, py))
    d = ImageDraw.Draw(im)
    spaced(d, (W_ / 2, 92), 'faye pressly  ·  founder, phyli', F('mono', 17), QUIET, .3, 'c')
    y = text(im, "a note, before\nthis page changes.", 'display', size, 72, ty, col=INK, maxw=W_ - 144, align='c', lh=1.04)
    underline(im, W_ / 2 - 150, W_ / 2 + 150, y + 22, INK, seed=4, width=3)
    spaced(d, (W_ / 2, sub_y), 'palma  ·  26 . x . 2026', F('mono', 15), QUIET, .3, 'c')
    im.save(f'{OUT}/{name}', quality=94); print(name, im.size)

build(1080, 1350, 'Manifesto_cover_4x5.jpg', 760, 230, 1000, 64, 1350 - 90)
build(1080, 1920, 'Manifesto_cover_9x16.jpg', 800, 440, 1330, 66, 1920 - 120)
