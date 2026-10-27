"""examples of the system on post 8 (black friday / which skeleton) using her own footage"""
import sys, os; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import *
os.makedirs('sys/out', exist_ok=True)
S = 'sys/src/'
POP = POPS['olive']            # this post's colour (from the kimono + the lane)
POPL = (168, 172, 96)          # lighter olive for on-photo use
out = []

# 01 · COVER · plate · kimono on the balcony
im = pil(img(S + 'kimono_balcony.jpg', W, H, (.5, .35), 1.0)); im = darken(im, 0, .55)
label(im, 'no. 08  ·  palma  ·  november'); fp(im)
im, y = shadowed(im, "black friday will find out\nwhich *skeleton* you built.", 'sansb', 60, 72, 980, col=IVORY, maxw=940, lh=1.12, acc=POPL, acc_kind='italic', acc_scale=1.08)
out.append(im)

# 02 · PLATE · the horse · one line
im = pil(img(S + 'horse.jpg', W, H, (.5, .5), 1.0)); im = darken(im, .05, .5); label(im, 'ii'); fp(im)
im, y = shadowed(im, "black friday is a stress test.", 'display', 58, 72, 960, maxw=940, lh=1.1)
text(im, "it doesn't find out how hard you can work.\nit finds out what you built.", 'sans', 28, 72, y + 18, col=IVORY, maxw=900, lh=1.3)
num(im, 2, 8); out.append(im)

# 03 · NOTE · pearl · two skeletons · image-filled horse
im = pil(pearl(seed=3)); fp(im, INK); label(im, 'iii', INK)
im = inkfill(im, 'horse62', img(S + 'kimono_balcony.jpg', 900, 900, (.5, .55), 1.6), 560, 740, 330, op=.96, tone=.55, bold=2)
y = text(im, "two skeletons.", 'display', 72, 72, 640, col=INK, lh=1.05)
y = text(im, "the one you *designed*: roles, handovers, the way a decision moves without you.\n\nand the one that *grew* while you weren't looking.", 'sans', 30, 72, y + 28, col=INK, maxw=820, lh=1.34, acc=POP, acc_scale=1.1)
underline(im, 72, 300, y + 10, POP, 2);
ImageDraw.Draw(im).text((72, y + 26), "the second one is made of you.", font=F('italic', 30), fill=QUIET)
num(im, 3, 8, INK); out.append(im)

# 04 · PLATE · text-heavy · the mirror dance, darkened · list
im = pil(img(S + 'mirror_dance.jpg', W, H, (.5, .4), 1.05)); im = vignette(darken(im, .35, .55), .3); label(im, 'iv'); fp(im)
im, y = shadowed(im, "what the second\nskeleton is made of", 'display', 54, 72, 300, maxw=900, lh=1.08)
d = ImageDraw.Draw(im); y += 30
for i, line in enumerate(["every gap in the structure, filled with your body", "the thing you remember so the system doesn't have to", "the decision that waits outside your door", "the late night that is really compensation"]):
    d.text((72, y), '→', font=F('mono', 24), fill=POPL); d.text((122, y - 2), line, font=F('sans', 29), fill=IVORY); y += 56
y += 30; d.text((72, y), "none of it is on the org chart.", font=F('italic', 34), fill=IVORY)
underline(im, 72, 300, y + 48, POPL, 4); num(im, 4, 8); out.append(im)

# 05 · NOTE · pearl, dark · the big quote · image-filled splat
im = pil(pearl(seed=11, dark=True)); fp(im); label(im, 'v')
im = inkfill(im, 'splat', img(S + 'sunset_road.jpg', 800, 800, (.5, .3), 1.0), 560, 760, 1040, op=.95, tone=1.15)
text(im, "the stress test\ndoesn't test\nyour effort.", 'display', 80, 72, 220, col=IVORY, lh=1.04)
text(im, "it tests what moves *without* you.", 'sans', 32, 72, 560, col=IVORY, maxw=700, lh=1.3, acc=POPL, acc_scale=1.1)
num(im, 5, 8); out.append(im)

# 06 · PLATE · studio floor · the practical note (tipped-in plate on pearl, bleeding off the right)
im = pil(pearl(seed=5)); ph = pil(img(S + 'studio_cards.jpg', 760, 900, (.5, .5), 1.0)); im.paste(ph, (W - 760 + 60, 0)); label(im, 'vi', INK); fp(im, INK)
y = text(im, "try this\nbefore\nfriday.", 'display', 64, 72, 120, col=INK, lh=1.05)
y = text(im, "write down the five things that break if you're ill on the day.\n\nthat list *is* your skeleton. nothing else is.", 'sans', 29, 72, 960, col=INK, maxw=900, lh=1.34, acc=POP, acc_scale=1.1)
num(im, 6, 8, INK); out.append(im)

# 07 · SEAL · pearl · the mark, large · the house thread
im = pil(pearl(seed=21));
im = inkfill(im, 'rootflower', img(S + 'studio_cards.jpg', 900, 900, (.5, .6), 1.1), 540, 540, 440, op=.97, tone=.7)
d = ImageDraw.Draw(im); dot(im, W / 2, 1000)
spaced(d, (W / 2, 1040), 'faye pressly  ·  founder, phyli', F('mono', 16), QUIET, .2, 'c')
d.text((W / 2, 1120), "the thinking lives at @phyli.studio.", font=F('italic', 30), fill=INK, anchor='ma')
d.text((W / 2, 1168), "this is where it's made.", font=F('italic', 30), fill=INK, anchor='ma')
out.append(im)

# 08 · REEL FRAME (1080x1920) · text over b-roll
RW, RH = 1080, 1920
fr = pil(img(S + 'sunset_road.jpg', RW, RH, (.5, .4), 1.0)); fr = darken(fr, .0, .5)
d = ImageDraw.Draw(fr); spaced(d, (72, 110), 'no. 01  ·  the reintroduction', F('mono', 17), IVORY, .18); d.text((RW - 72, 94), 'fp', font=F('italic', 44), fill=IVORY, anchor='ra')
tmp = Image.new('RGB', (RW, RH), (0, 0, 0));
# word focus: spoken word full ivory, the rest receded
words = "most people don't realise I spent the last year writing a business book".split(); live = 7
f = F('sansm', 54); x, y = 72, 1480; sp = d.textlength(' ', font=f); maxw = 940; lines = [[]]; cur = 0
for i, w_ in enumerate(words):
    ww = d.textlength(w_, font=f)
    if cur and cur + sp + ww > maxw: lines.append([]); cur = 0
    lines[-1].append((w_, i)); cur += (sp if cur else 0) + ww
halo = Image.new('L', (RW, RH), 0); hd = ImageDraw.Draw(halo)
for li, ln in enumerate(lines):
    xx = x
    for w_, i in ln: hd.text((xx, y + li * 70), w_, font=f, fill=255); xx += d.textlength(w_, font=f) + sp
halo = halo.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(min(255, v * .8)))
lay = Image.new('RGBA', (RW, RH), (0, 0, 0, 0)); lay.paste((16, 10, 16, 255), (0, 0), halo); fr = fr.convert('RGBA'); fr.alpha_composite(lay); fr = fr.convert('RGB'); d = ImageDraw.Draw(fr)
for li, ln in enumerate(lines):
    xx = x
    for w_, i in ln:
        c = IVORY if i == live else (255, 255, 255) if i > live else (190, 182, 178)
        if i > live: c = None
        if c: d.text((xx, y + li * 70), w_, font=f, fill=c)
        xx += d.textlength(w_, font=f) + sp
d.line((72, 1850, 72 + 936 * 0.32, 1850), fill=IVORY, width=2); d.line((72 + 936 * 0.32, 1850, 1008, 1850), fill=(255, 255, 255, 60), width=1)
fr.save('sys/out/08_reel.jpg', quality=92)

for i, im in enumerate(out): im.save(f'sys/out/{i+1:02d}.jpg', quality=92)

# ---------- the system card: palette, pearl, type, marks ----------
card = pil(pearl(1080, 1350, seed=2)); d = ImageDraw.Draw(card)
spaced(d, (72, 80), 'faye pressly  ·  visual system  ·  nov 2026 – jan 2027', F('mono', 16), INK, .18)
d.text((72, 130), "the garden,", font=F('display', 74), fill=INK); d.text((72, 212), "not the herbarium.", font=F('italic', 60), fill=INK)
d.text((72, 300), "the house presses the specimen in ink on ivory. this page is the living thing before it is pressed:\ncolour, movement, imperfection, the hand that made it.", font=F('sans', 24), fill=INK)
# swatches
y0 = 400; x0 = 72
spaced(d, (x0, y0), 'grounds', F('mono', 14), QUIET, .2)
sw = pil(pearl(300, 120, seed=4)); card.paste(sw, (x0, y0 + 26)); d.text((x0, y0 + 152), 'pearl · light', font=F('sans', 16), fill=INK)
sw = pil(pearl(300, 120, seed=9, dark=True)); card.paste(sw, (x0 + 320, y0 + 26)); d.text((x0 + 320, y0 + 152), 'pearl · dark', font=F('sans', 16), fill=INK)
sw = pil(img(S + 'horse.jpg', 300, 120, (.5, .5), 1.6)); card.paste(sw, (x0 + 640, y0 + 26)); d.text((x0 + 640, y0 + 152), 'the photograph, graded', font=F('sans', 16), fill=INK)
y0 = 600; spaced(d, (x0, y0), 'one pop per post, taken from the photograph  ·  never butter yellow', F('mono', 14), QUIET, .2)
for i, (n, c) in enumerate(POPS.items()):
    xx = x0 + i * 158; d.rounded_rectangle((xx, y0 + 26, xx + 140, y0 + 96), 6, fill=c); d.text((xx, y0 + 104), n, font=F('sans', 15), fill=INK)
d.ellipse((x0 + 950, y0 + 50, x0 + 966, y0 + 66), fill=GREEN); d.text((x0 + 930, y0 + 104), 'thread', font=F('sans', 15), fill=INK)
y0 = 760; spaced(d, (x0, y0), 'type', F('mono', 14), QUIET, .2)
d.text((x0, y0 + 24), "Rozha One for the one line.", font=F('display', 40), fill=INK)
d.text((x0, y0 + 80), "Newsreader italic for the aside, and the accent word.", font=F('italic', 32), fill=INK)
d.text((x0, y0 + 126), "Inter for the body. Small, lowercase, never shouting.", font=F('sans', 24), fill=INK)
spaced(d, (x0, y0 + 168), 'ibm plex mono for the specimen label  ·  no. 08  ·  palma  ·  november', F('mono', 16), INK, .18)
y0 = 980; spaced(d, (x0, y0), 'the mark  ·  her ink, image-filled (the wordmark device)  ·  one per post', F('mono', 14), QUIET, .2)
card = inkfill(card, 'horse62', img(S + 'kimono_balcony.jpg', 500, 500, (.5, .55), 1.6), 300, 220, 1180, op=.97, tone=.6)
card = inkfill(card, 'splat', img(S + 'sunset_road.jpg', 500, 500, (.5, .3), 1.0), 280, 540, 1180, op=.97, tone=1.1)
card = inkfill(card, 'rootflower', img(S + 'studio_cards.jpg', 500, 500, (.5, .6), 1.1), 230, 820, 1180, op=.97, tone=.7)
card = inkfill(card, 'ink_dandelion_seedhead', pearl(400, 400, seed=5, dark=True), 180, 1000, 1180, op=.97)
card.save('sys/out/00_system.jpg', quality=92)

# contact sheet
tiles = [cv2.resize(cv2.imread(f'sys/out/{n}.jpg'), (360, 450)) for n in ['00_system','01','02','03','04','05','06','07']]
reel = cv2.resize(cv2.imread('sys/out/08_reel.jpg'), (253, 450)); reel = cv2.copyMakeBorder(reel, 0, 0, 53, 54, 0, value=(20, 20, 20))
tiles.append(reel)
rows = [np.hstack(tiles[0:3]), np.hstack(tiles[3:6]), np.hstack(tiles[6:9])]
cv2.imwrite('sys/out/sheet.jpg', np.vstack(rows)); print('ok')

# ---------- grid preview: nine covers, pop colour rotating, with breathing room ----------
G = []
def cover(path, focus, zoom, line, pop, lab, dk=.5):
    im = pil(img(S + path, W, H, focus, zoom)); im = darken(im, 0, dk); label(im, lab); fp(im)
    im, _ = shadowed(im, line, 'sansb', 58, 72, 1000, col=IVORY, maxw=940, lh=1.12, acc=pop, acc_kind='italic', acc_scale=1.08); return im
G.append(cover('kimono_balcony.jpg', (.5, .35), 1.0, "black friday will find out\nwhich *skeleton* you built.", (168, 172, 96), 'no. 08 · palma'))
im = pil(pearl(seed=31)); im = inkfill(im, 'splat', img(S + 'pink_dance.jpg', 800, 800, (.5, .4), 1.2), 700, 540, 520, op=.97, tone=.75, bold=1); label(im, 'no. 09 · a note', INK); fp(im, INK)
text(im, "the crutch test.", 'display', 70, 72, 1000, col=INK); G.append(im)
G.append(cover('horse.jpg', (.5, .5), 1.0, "most founders have built\none skeleton and are being\n*broken* by the other.", (214, 110, 54), 'no. 11 · palma'))
G.append(cover('mirror_dance.jpg', (.5, .4), 1.05, "rhythm, *not* rigidity.", (58, 150, 150), 'no. 12 · the studio', .55))
im = pil(pearl(seed=8, dark=True)); im = inkfill(im, 'rootflower', img(S + 'studio_cards.jpg', 800, 800, (.5, .6), 1.1), 520, 540, 500, op=.97, tone=.9); label(im, 'no. 13 · each volume, its own colour'); fp(im)
text(im, "each volume gets\nits own *colour*.", 'display', 58, 72, 1000, col=IVORY, acc=(216, 169, 179), acc_scale=1.0, lh=1.1); G.append(im)
G.append(cover('headscarf.jpg', (.5, .35), 1.0, "you can hold your face\nfor about an hour.", (196, 110, 128), 'no. 15 · palma', .55))
G.append(cover('studio_floor.jpg', (.5, .5), 1.0, "the two *signals*.", (118, 122, 60), 'no. 18 · the studio', .45))
G.append(cover('hairflip.jpg', (.5, .3), 1.0, "spot the *keystone*.", (178, 52, 110), 'no. 22 · palma', .5))
im = pil(pearl(seed=17)); im = inkfill(im, 'ink_dandelion_seedhead', img(S + 'sunset_road.jpg', 700, 700, (.5, .3), 1.0), 520, 540, 460, op=.97, tone=1.1, bold=1); label(im, 'no. 24 · a note', INK); fp(im, INK)
text(im, "the hive doesn't have\na thermostat. it has\n*everyone*.", 'display', 50, 72, 980, col=INK, acc=(84, 104, 150), lh=1.1); G.append(im)
for i, im in enumerate(G): im.save(f'sys/out/g{i+1}.jpg', quality=90)
tiles = [cv2.resize(np.asarray(x)[..., ::-1], (360, 450)) for x in G]
grid = np.vstack([np.hstack(tiles[i:i+3]) for i in (0, 3, 6)]); cv2.imwrite('sys/out/grid.jpg', grid); print('grid ok')
