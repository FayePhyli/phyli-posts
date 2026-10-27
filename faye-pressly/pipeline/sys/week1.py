"""week one of @faye.pressly: covers in the approved feed style, interiors in pearl + image-filled ink"""
import sys, os; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import *
import cv2
S = 'sys/src/'; OUT = 'sys/week1'; os.makedirs(OUT, exist_ok=True)
FB = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
LIL, CORAL, PLUM = (230, 212, 248), (242, 174, 158), (58, 34, 56)

def glowtext(im, lines, size, y, col, glow, ga=.55, caps=False):
    """the approved cover type: bold sans, centred, soft glow"""
    f = ImageFont.truetype(FB, size); d0 = ImageDraw.Draw(Image.new('L', (1, 1)))
    g = Image.new('L', im.size, 0); gd = ImageDraw.Draw(g); t = Image.new('RGB', im.size, (0, 0, 0)); td = ImageDraw.Draw(t); m = Image.new('L', im.size, 0); md = ImageDraw.Draw(m)
    yy = y
    for ln in lines:
        s = ln.upper() if caps else ln; gd.text((W / 2, yy), s, font=f, fill=255, anchor='ma'); md.text((W / 2, yy), s, font=f, fill=255, anchor='ma'); yy += size * 1.12
    g = g.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(min(255, v * ga * 1.6)))
    out = im.convert('RGBA'); gl = Image.new('RGBA', im.size, glow + (0,)); gl.putalpha(g); out.alpha_composite(gl)
    solid = Image.new('RGBA', im.size, col + (255,)); solid.putalpha(m); out.alpha_composite(solid); return out.convert('RGB')
def cover(path, lines, focus=(.5, .4), zoom=1.0, col=LIL, glow=(156, 123, 224), size=66, y=940, g=1.0, caps=False):
    im = pil(img(S + path, W, H, focus, zoom, g)); im = darken(im, 0.0, 0.42); return glowtext(im, lines, size, y, col, glow, ga=.9, caps=caps)
def plate_label(im, lab, dark=False):
    label(im, lab, INK if not dark else IVORY); fp(im, INK if not dark else IVORY)
def seal(seed, mark, fill, w, line1, line2, tone=.7, bold=0, dark=False):
    im = pil(pearl(seed=seed, dark=dark)); im = inkfill(im, mark, fill, w, 540, 440, op=.97, tone=tone, bold=bold)
    d = ImageDraw.Draw(im); dot(im, W / 2, 1000); c = IVORY if dark else INK
    spaced(d, (W / 2, 1040), 'faye pressly  ·  founder, phyli', F('mono', 16), QUIET if not dark else (190, 182, 190), .2, 'c')
    d.text((W / 2, 1120), line1, font=F('italic', 30), fill=c, anchor='ma'); d.text((W / 2, 1168), line2, font=F('italic', 30), fill=c, anchor='ma'); return im

# ================= TUE 27 OCT · carousel · every business is unique =================
A = []
im = cover('headscarf.jpg', ['every single business', 'is completely unique.'], (.5, .35), 1.0, LIL, PLUM, 64, 980); A.append(im)
im = pil(pearl(seed=41)); plate_label(im, 'ii'); im = inkfill(im, 'horse62', img(S + 'kimono_balcony.jpg', 900, 900, (.5, .55), 1.6), 560, 740, 330, op=.96, tone=.55, bold=2)
y = text(im, "a business is not a machine\nto be extracted from.", 'display', 54, 72, 640, col=INK, lh=1.08)
ImageDraw.Draw(im).text((72, y + 24), "she is a living thing.", font=F('italic', 40), fill=INK); num(im, 2, 7, INK); A.append(im)
im = pil(pearl(seed=42, dark=True)); plate_label(im, 'iii', True)
y = text(im, "a different *rhythm*.\na different *soul*.", 'display', 66, 72, 360, col=IVORY, lh=1.1, acc=(232, 184, 194), acc_scale=1.0)
text(im, "even if you sell the same thing as the company next door. even if you have the same product, the same service, the same supplier.", 'sans', 29, 72, 640, col=IVORY, maxw=860, lh=1.34); num(im, 3, 7); A.append(im)
im = pil(pearl(seed=43)); plate_label(im, 'iv'); im = inkfill(im, 'splat', img(S + 'pink_dance.jpg', 900, 900, (.5, .4), 1.3), 620, 760, 880, op=.97, tone=.8, bold=1)
text(im, "a different *shape*.\na different *energy*.\na different *personality*.", 'display', 58, 72, 220, col=INK, lh=1.1, acc=POPS['magenta'], acc_scale=1.0); num(im, 4, 7, INK); A.append(im)
im = pil(pearl(seed=44)); plate_label(im, 'v')
y = text(im, "this is how i read\na business.", 'display', 60, 72, 200, col=INK, lh=1.08)
d = ImageDraw.Draw(im); y += 50
for q in ["who is she?", "how does she operate?", "how does she want to move?", "where is she blocked?", "where is she healing badly?", "where does she need attending to?"]:
    d.text((72, y), q, font=F('italic', 40), fill=INK); y += 64
underline(im, 72, 420, y + 10, POPS['olive'], 3); num(im, 5, 7, INK); A.append(im)
im = pil(img(S + 'studio_floor.jpg', W, H, (.5, .5), 1.0)); im = darken(im, .1, .55); label(im, 'vi'); fp(im)
im, y = shadowed(im, "none of that language existed\nanywhere i worked.", 'display', 50, 72, 980, maxw=940, lh=1.1)
text(im, "it's the language i speak. so i wrote it down.", 'sans', 30, 72, y + 16, col=IVORY, maxw=900); num(im, 6, 7); A.append(im)
A.append(seal(45, 'rootflower', img(S + 'studio_cards.jpg', 900, 900, (.5, .6), 1.1), 540, "the thinking lives at @phyli.studio.", "this is where it's made."))
for i, im in enumerate(A): im.save(f'{OUT}/tue_unique_{i+1:02d}.jpg', quality=92)

# ================= THU 29 OCT · carousel · what is your company compensating for =================
B = []
B.append(Image.open('fp/site/t/05.jpg').convert('RGB').resize((W, H)))
im = pil(pearl(seed=51)); plate_label(im, 'ii'); im = inkfill(im, 'ink_tree_spiral', img(S + 'kimono_court.jpg', 900, 900, (.5, .4), 1.3), 620, 740, 300, op=.96, tone=.6, bold=1)
y = text(im, "every company\nhas a posture.", 'display', 62, 72, 620, col=INK, lh=1.08)
text(im, "and most bad posture is *compensation* for an injury that has already healed.", 'sans', 31, 72, y + 28, col=INK, maxw=860, lh=1.34, acc=POPS['orange'], acc_scale=1.1); num(im, 2, 8, INK); B.append(im)
for k, (lab, line, sub) in enumerate([
    ('iii', "the approval that exists because of one *expensive* mistake in year two.", None),
    ('iv', "the reporting line that bends around a conflict nobody even *remembers*.", None),
    ('v', "everything routing through you, because in year one it genuinely *had* to.", None),
    ('vi', "the weekly meeting that was built to catch a problem you solved last *spring*.", None)]):
    dark = k % 2 == 1; im = pil(pearl(seed=60 + k, dark=dark)); plate_label(im, lab, dark)
    text(im, line, 'display', 46, 72, 420, col=IVORY if dark else INK, lh=1.12, maxw=920, acc=(232, 184, 194) if dark else POPS['orange'], acc_scale=1.0)
    if k % 2 == 0: im = inkfill(im, ['ink_dandelion_seedhead', 'sprig'][k // 2], img(S + ['sunset_road.jpg', 'kimono_balcony.jpg'][k // 2], 600, 600, (.5, .4), 1.2), 300, 820, 760, op=.95, tone=.7 if k else 1.1, bold=1)
    ImageDraw.Draw(im).text((72, 980), "still here. still bracing.", font=F('italic', 32), fill=(190, 182, 190) if dark else QUIET); num(im, 3 + k, 8, IVORY if dark else INK); B.append(im)
im = pil(img(S + 'mirror_dance.jpg', W, H, (.5, .4), 1.05)); im = vignette(darken(im, .3, .55), .3); label(im, 'vii'); fp(im)
im, y = shadowed(im, "ask of each one:\nwhat old injury is this\nshape built around?", 'display', 50, 72, 760, maxw=920, lh=1.08)
text(im, "is it still there?", 'italic', 40, 72, y + 20, col=IVORY); num(im, 7, 8); B.append(im)
im = seal(70, 'splat', img(S + 'sunset_road.jpg', 800, 800, (.5, .3), 1.0), 560, "if the reason has gone,", "you're allowed to let the bracing go too.", tone=1.15, bold=1, dark=True); B.append(im)
for i, im in enumerate(B): im.save(f'{OUT}/thu_posture_{i+1:02d}.jpg', quality=92)

# ================= covers for the reels that don't have one =================
# tonight · why i made phyli (the riff)
im = cover('kimono_court.jpg', ['learning about business', 'is pretty f*cking ugly.'], (.5, .35), 1.0, CORAL, PLUM, 64, 960); im.save(f'{OUT}/sun_riff_cover.jpg', quality=92)
# wed · done with that
im = cover('hairflip.jpg', ["i spent years making myself", "sound like them.", "i'm done with that now."], (.5, .3), 1.0, LIL, PLUM, 56, 920); im.save(f'{OUT}/wed_done_cover.jpg', quality=92)
# sat · the greys, the oranges, the blacks
im = cover('mirror_dance.jpg', ['the greys. the oranges.', 'the blacks.', "it's not even sexy masculine."], (.5, .4), 1.05, CORAL, PLUM, 56, 920); im.save(f'{OUT}/sat_greys_cover.jpg', quality=92)

# sheets
def sheet(prefix, n, name):
    tiles = [cv2.resize(cv2.imread(f'{OUT}/{prefix}_{i+1:02d}.jpg'), (300, 375)) for i in range(n)]
    while len(tiles) % 4: tiles.append(np.full((375, 300, 3), 30, np.uint8))
    cv2.imwrite(f'{OUT}/{name}', np.vstack([np.hstack(tiles[i:i+4]) for i in range(0, len(tiles), 4)]))
sheet('tue_unique', 7, 'sheet_tue.jpg'); sheet('thu_posture', 8, 'sheet_thu.jpg')
cv2.imwrite(f'{OUT}/sheet_covers.jpg', np.hstack([cv2.resize(cv2.imread(f'{OUT}/{n}'), (360, 450)) for n in ('sun_riff_cover.jpg', 'wed_done_cover.jpg', 'sat_greys_cover.jpg')]))
print('ok')

# ---- covers rebuilt in the approved feed language: her art and posterised portraits, big glowing type ----
def artcover(path, lines, col, glow, size, y, focus=(.5, .5), zoom=1.0, g=.6, caps=False, dk=.3):
    im = pil(img(path, W, H, focus, zoom, g)); im = darken(im, 0.0, dk); return glowtext(im, lines, size, y, col, glow, ga=1.0, caps=caps)
im = artcover('g30/src/art91.jpg', ['learning about', 'business is pretty', 'f*cking ugly.'], LIL, PLUM, 86, 420, (.5, .5), 1.1, caps=False); im.save(f'{OUT}/sun_riff_cover.jpg', quality=92)
im = artcover('g30/src/art5.jpg', ['every single', 'business is', 'completely unique.'], IVORY, (120, 60, 140), 84, 440, (.5, .5), 1.05); im.save(f'{OUT}/tue_unique_01.jpg', quality=92)
im = artcover('g30/src/faye98.jpg', ["i'm done", "sounding", "like them."], LIL, PLUM, 96, 900, (.5, .3), 1.0, g=.9, dk=.45); im.save(f'{OUT}/wed_done_cover.jpg', quality=92)
im = artcover('g30/src/art1.jpg', ['the greys.', 'the oranges.', 'the blacks.'], CORAL, (120, 40, 60), 100, 420, (.5, .5), 1.0, caps=True); im.save(f'{OUT}/sat_greys_cover.jpg', quality=92)
tiles=[('sat',f'{OUT}/sat_greys_cover.jpg'),('fri','fp/site/t/06.jpg'),('thu','fp/site/t/05.jpg'),('wed',f'{OUT}/wed_done_cover.jpg'),('tue',f'{OUT}/tue_unique_01.jpg'),('mon','fp/site/t/02.jpg'),('sun reel',f'{OUT}/sun_riff_cover.jpg'),('sun manifesto','fp/site/m/01.jpg'),('current top','g30/src/faye1.jpg')]
ims=[]
for n,p in tiles:
    a=cv2.imread(p); h,w=a.shape[:2]; s=max(360/w,450/h); a=cv2.resize(a,(int(w*s),int(h*s))); yy=(a.shape[0]-450)//2; xx=(a.shape[1]-360)//2; ims.append(a[yy:yy+450,xx:xx+360].copy())
cv2.imwrite(f'{OUT}/grid_week1.jpg',np.vstack([np.hstack(ims[i:i+3]) for i in (0,3,6)])); print('covers ok')
