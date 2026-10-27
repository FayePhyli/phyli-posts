"""week one, from the approved grid: approved covers (fp/site/t), pearl + image-filled ink interiors"""
import sys, os; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import *
import cv2
S = 'sys/src/'; OUT = 'sys/week1'; os.makedirs(OUT, exist_ok=True)
def approved(tile): return Image.open(f'fp/site/t/{tile}.jpg').convert('RGB').resize((W, H))
def plab(im, lab, dark=False): label(im, lab, IVORY if dark else INK); fp(im, IVORY if dark else INK)
def seal(seed, mark, fill, w, line1, line2, tone=.7, bold=0, dark=False):
    im = pil(pearl(seed=seed, dark=dark)); im = inkfill(im, mark, fill, w, 540, 440, op=.97, tone=tone, bold=bold)
    d = ImageDraw.Draw(im); dot(im, W / 2, 1000); c = IVORY if dark else INK
    spaced(d, (W / 2, 1040), 'faye pressly  ·  founder, phyli', F('mono', 16), (190, 182, 190) if dark else QUIET, .2, 'c')
    d.text((W / 2, 1120), line1, font=F('italic', 30), fill=c, anchor='ma'); d.text((W / 2, 1168), line2, font=F('italic', 30), fill=c, anchor='ma'); return im
def note(seed, lab, n, N, head, body=None, mark=None, dark=False, acc=None, markpos=(760, 300), mw=560, tone=.65, bold=1, headsize=56, heady=None, aside=None):
    im = pil(pearl(seed=seed, dark=dark)); plab(im, lab, dark); c = IVORY if dark else INK
    if mark: im = inkfill(im, mark[0], img(S + mark[1], 900, 900, (.5, .45), 1.4), mw, *markpos, op=.96, tone=tone, bold=bold)
    y = text(im, head, 'display', headsize, 72, heady or (620 if mark else 380), col=c, lh=1.1, maxw=920, acc=acc or ((232, 184, 194) if dark else POPS['orange']), acc_scale=1.0)
    if body: y = text(im, body, 'sans', 30, 72, y + 26, col=c, maxw=880, lh=1.34, acc=acc or ((232, 184, 194) if dark else POPS['orange']), acc_scale=1.1)
    if aside: ImageDraw.Draw(im).text((72, y + 30), aside, font=F('italic', 32), fill=(190, 182, 190) if dark else QUIET)
    num(im, n, N, c); return im

# ===== FRI 30 OCT · post 8 · black friday will find out which skeleton you built (cover 08, the beetle) =====
B = [approved('08')]
B.append(note(81, 'ii', 2, 8, "three and a half\nweeks out.", "your stock is ordered, your ads are built, your packaging is ready.\n\nthat's the *first* skeleton.", mark=('ink_tree_spiral', 'kimono_court.jpg')))
B.append(note(82, 'iii', 3, 8, "now the second one.", "who can approve a replacement order *without* you?", dark=True, aside="not 'who should'. who can, tonight."))
B.append(note(83, 'iv', 4, 8, "when the warehouse\nis a day behind:", "do we tell customers, or wait?\n\nwho *decides* that?", mark=('splat', 'sunset_road.jpg'), markpos=(780, 1060), tone=1.1))
B.append(note(84, 'v', 5, 8, "the one question that will\nreach your phone two\nhundred times.", "who else could answer it?", dark=True))
im = pil(img(S + 'mirror_dance.jpg', W, H, (.5, .4), 1.05)); im = vignette(darken(im, .3, .55), .3); label(im, 'vi'); fp(im)
im, y = shadowed(im, "peak doesn't create\nthese problems.", 'display', 56, 72, 900, maxw=920, lh=1.08); text(im, "it finds them.", 'italic', 44, 72, y + 16, col=IVORY); num(im, 6, 8); B.append(im)
B.append(note(86, 'vii', 7, 8, "three decisions,\nwritten down.", "with a name beside each one that *isn't* yours.", mark=('horse62', 'kimono_balcony.jpg'), tone=.55, bold=2))
B.append(seal(87, 'rootflower', img(S + 'studio_cards.jpg', 900, 900, (.5, .6), 1.1), 540, "that's the whole exercise.", "do it this week, while it's still quiet."))
for i, im in enumerate(B): im.save(f'{OUT}/fri_blackfriday_{i+1:02d}.jpg', quality=92)

# ===== SAT 31 OCT · post 9 · the crutch test (cover 09, the stone on brocade) =====
C = [approved('09')]
C.append(note(91, 'ii', 2, 8, "a good crutch makes\nitself unnecessary.", "a bad one makes itself *permanent*.", mark=('ink_dandelion_seedhead', 'sunset_road.jpg'), tone=1.1))
C.append(note(92, 'iii', 3, 8, "it does that by quietly\ntaking the capacity it\nwas meant to restore.", dark=True))
C.append(note(93, 'iv', 4, 8, "mechanical work:", "hand it to the machines, *without guilt*.", mark=('sprig', 'kimono_balcony.jpg'), markpos=(800, 1040), mw=320, tone=.7))
C.append(note(94, 'v', 5, 8, "craft:", "let the tool carry it, and stay the one who *knows how*.", dark=True))
C.append(note(95, 'vi', 6, 8, "deciding.\nrelating.\ncaring.", "*never*.", mark=('splat', 'pink_dance.jpg'), markpos=(760, 1000), tone=.8))
im = pil(img(S + 'studio_floor.jpg', W, H, (.5, .5), 1.0)); im = darken(im, .1, .55); label(im, 'vii'); fp(im)
im, y = shadowed(im, "if this tool vanished\ntomorrow, would the\ncapacity still be\nin the room?", 'display', 50, 72, 840, maxw=940, lh=1.08); num(im, 7, 8); C.append(im)
C.append(seal(97, 'splat', img(S + 'sunset_road.jpg', 800, 800, (.5, .3), 1.0), 560, "run it on the tool that feels most indispensable.", "indispensability is the symptom.", tone=1.15, bold=1, dark=True))
for i, im in enumerate(C): im.save(f'{OUT}/sat_crutch_{i+1:02d}.jpg', quality=92)

# ===== WED 28 OCT · post 5 · compensating (already built as thu_posture; cover is the approved 05) =====
# ===== sheets + the week on the grid, approved covers only =====
def sheet(prefix, n, name):
    tiles = [cv2.resize(cv2.imread(f'{OUT}/{prefix}_{i+1:02d}.jpg'), (300, 375)) for i in range(n)]
    while len(tiles) % 4: tiles.append(np.full((375, 300, 3), 30, np.uint8))
    cv2.imwrite(f'{OUT}/{name}', np.vstack([np.hstack(tiles[i:i+4]) for i in range(0, len(tiles), 4)]))
sheet('fri_blackfriday', 8, 'sheet_fri.jpg'); sheet('sat_crutch', 8, 'sheet_sat.jpg')
tiles = [('sat · crutch test', 'fp/site/t/09.jpg'), ('fri · black friday', 'fp/site/t/08.jpg'), ('thu · work flows', 'fp/site/t/06.jpg'),
         ('wed · compensating', 'fp/site/t/05.jpg'), ('tue · forty messages', 'fp/site/t/03.jpg'), ('mon · carrying it', 'fp/site/t/02.jpg'),
         ('sun · reel (the riff)', 'fp/site/t/00.jpg'), ('sun · manifesto', 'fp/site/m/01.jpg'), ('current top post', 'g30/src/faye1.jpg')]
ims = []
for n, p in tiles:
    a = cv2.imread(p); h, w = a.shape[:2]; s = max(360 / w, 450 / h); a = cv2.resize(a, (int(w * s), int(h * s))); yy = (a.shape[0] - 450) // 2; xx = (a.shape[1] - 360) // 2; ims.append(a[yy:yy+450, xx:xx+360].copy())
cv2.imwrite(f'{OUT}/grid_week1.jpg', np.vstack([np.hstack(ims[i:i+3]) for i in (0, 3, 6)])); print('ok')
