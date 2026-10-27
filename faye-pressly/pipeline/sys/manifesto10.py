"""the manifesto v5: the website's system (Rozha, tracked mono with a hand-drawn underline, Newsreader italic, her ink) on a pearl ombré that shifts slide to slide. text centred. no photographs. cover = the landing card."""
import sys, os, math; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import *
import cv2
OUT = 'sys/week1/manifesto10'; os.makedirs(OUT, exist_ok=True); N = 13
ROSE = (196, 86, 122)
def ground(i):
    """pearl, lifted towards ivory, a different drift of colour each slide"""
    seed = 500 + i * 7; tone = i * 0.9
    return pil(pearl(seed=seed, tone=tone) * 0.70 + np.array(IVORY, float) * 0.30)
def inkmask(name, w, crop=(0, 0, 1, 1)):
    p = f'ink/masks/{name}.png' if os.path.exists(f'ink/masks/{name}.png') else f'fp/web/{name}_a.png'
    a = Image.open(p).convert('L'); W0, H0 = a.size; a = a.crop((int(crop[0] * W0), int(crop[1] * H0), int(crop[2] * W0), int(crop[3] * H0)))
    s = w / a.size[0]; return a.resize((int(a.size[0] * s), int(a.size[1] * s)), Image.LANCZOS)
def ink(im, name, w, cx, cy, op=.92, crop=(0, 0, 1, 1), col=INK):
    a = inkmask(name, w, crop).point(lambda v: int(v * op)); layer = Image.new('RGB', a.size, col)
    im.paste(layer, (int(cx - a.size[0] / 2), int(cy - a.size[1] / 2)), a); return im
def mono(im, t, y, size=18, col=QUIET, ul=True, seed=0):
    d = ImageDraw.Draw(im); f = F('mono', size); t = t.upper(); ws = [d.textlength(ch, font=f) for ch in t]; tr = size * .36; total = sum(ws) + tr * (len(t) - 1)
    spaced(d, (W / 2, y), t, f, col, .36, 'c')
    if ul: underline(im, W / 2 - total / 2 - 10, W / 2 + total / 2 + 10, y + size + 16, INK, seed=seed, width=3)
    return y + size + 40
def head(im, t, y, size=50): return text(im, t, 'display', size, 72, y, col=INK, maxw=920, align='c', lh=1.1, acc=ROSE)
def body(im, t, y, size=30): return text(im, t, 'serif', size, 72, y, col=INK, maxw=860, align='c', lh=1.38, acc=ROSE, acc_scale=1.02)
def ital(im, t, y, size=30, col=QUIET): return text(im, t, 'italic', size, 72, y, col=col, maxw=900, align='c', lh=1.3)
def measure(fn):
    tmp = Image.new('RGB', (W, H)); return fn(tmp, 0)
def centred(im, fn):
    h = measure(fn); fn(im, (H - h) / 2 - 20); return im

out = []
# 01 · cover: the landing card
im = ground(0); y = mono(im, 'arrival card  ·  faye pressly', 120, 18, QUIET, True, 1)
y = head(im, "Purpose of visit?", 300, 92); d = ImageDraw.Draw(im)
rows = [('business', False), ('pleasure', False)]; yy = y + 90
for lab, tick in rows:
    d.rectangle((W / 2 - 250, yy, W / 2 - 198, yy + 52), outline=INK, width=3); spaced(d, (W / 2 - 150, yy + 10), lab.upper(), F('mono', 30), INK, .3); yy += 116
# the third box, drawn by hand, ticked
rs = np.random.RandomState(4); bx = [(W / 2 - 252 + rs.randn() * 2, yy - 2 + rs.randn() * 2), (W / 2 - 196 + rs.randn() * 2, yy - 3 + rs.randn() * 2), (W / 2 - 194 + rs.randn() * 2, yy + 54 + rs.randn() * 2), (W / 2 - 254 + rs.randn() * 2, yy + 52 + rs.randn() * 2)]
d.line(bx + [bx[0]], fill=INK, width=4, joint='curve'); d.line([(W / 2 - 242, yy + 26), (W / 2 - 222, yy + 48), (W / 2 - 186, yy - 10)], fill=ROSE, width=7, joint='curve')
d.text((W / 2 - 150, yy - 4), "both. obviously.", font=F('italic', 50), fill=INK); yy += 150
spaced(d, (W / 2, yy + 30), 'LENGTH OF STAY', F('mono', 16), QUIET, .3, 'c'); ital(im, "indefinite.", yy + 60, 30, INK)
spaced(d, (W / 2, yy + 150), 'ITEMS TO DECLARE', F('mono', 16), QUIET, .3, 'c'); ital(im, "twelve volumes. unfinished.", yy + 180, 30, INK)
im = ink(im, 'rootflower', 170, 150, H - 230, .9, crop=(0, 0, 1, .93)); out.append(im)

def slide(i, fn, inkspec=None):
    im = ground(i)
    if inkspec: im = ink(im, *inkspec)
    im = centred(im, fn); num(im, i, N, QUIET); return im
# 02 · twenty years
def s2(im, y):
    y = mono(im, 'who i am', y, seed=2)
    y = body(im, "For almost twenty years I've run and grown the inside of companies, for other people.\n\nI've spent the last two years watching everyone else's stories. From today I'm making mine.\n\nNow I'm building *Phyli*: a place for my thoughts, wisdom and ideas to come to life, for other women running and growing their own companies as if they are alive.", y + 20)
    return ital(im, "Because they are.", y + 24)
out.append(slide(2, s2))
# 03 · the mission
def s3(im, y):
    y = head(im, "I want to curate the most beautiful business book in the *world*.", y + 400)
    return body(im, "Twelve volumes. Pages that open out, lift and unfold, the way the books we loved as children did. Made by hand, from the materials of couture. Carrying the content of a business book that feels timeless.", y + 30)
out.append(slide(3, s3, ('IMG_1628', 300, W / 2, 330, .9, (0, 0, 1, .93))))
# 04 · why
def s4(im, y):
    y = head(im, "Adult books stopped being *beautiful* a long time ago.", y, 46)
    return body(im, "Made as cheap as possible, shipped to as many as possible. This is the opposite of that. A book you keep, and hand down.\n\nBecause the women building thoughtful companies deserve wisdom that doesn't shout. Because I needed it, and couldn't find it. Because this has felt channelled for a long time, and I'd rather be the hands than argue with it.\n\nAnd because one day my daughter will ask what I made with my life. I want the answer to be beautiful.", y + 30, 29)
out.append(slide(4, s4, ('sprig', 260, W / 2, 1120, .8)))
# 05 · what I care about
def s5(im, y):
    y = head(im, "I care about *truth*,\n*beauty*, craft,", y + 380, 60)
    return body(im, "and work that outlives the week it was posted in.", y + 24)
out.append(slide(5, s5, ('IMG_1631', 420, W / 2, 330, .9)))
# 06 · what I don't
def s6(im, y):
    y = head(im, "What I don't care for:\nhacks, hustle, being everywhere, going viral.", y, 46)
    return body(im, "I'm not trying to be fast.\nI'm trying to be *aligned*, and connected, for a very long time.", y + 30)
out.append(slide(6, s6, ('IMG_4688', 360, W / 2, 1060, .85, (0, 0, 1, .95))))
# 07 · the dream
def s7(im, y):
    y = mono(im, 'the dream', y, seed=7)
    return body(im, "My dream is to launch in an art gallery. The Collectors' Volumes, numbered and bound by hand, by masters of their trade. MoMA's bookshop. *Vogue*.\n\nA business book you'd leave on the table because it's beautiful, and then actually read.", y + 20)
out.append(slide(7, s7, ('IMG_4685', 340, W / 2, 1040, .9)))
# 08 · pause
def s8(im, y):
    y = head(im, "If you read it,\nI want you to *pause*.", y, 60)
    return body(im, "To recognise something you already knew. To find pleasure in it. Not another fast thing to consume, and extract from you.", y + 30)
out.append(slide(8, s8, ('IMG_1634', 240, W / 2, 1040, .85, (0, 0, 1, .9))))
# 09 · not my whole life
def s9(im, y):
    y = head(im, "And it will not\ntake over my life.", y, 54)
    return body(im, "I'll share what I know without draining myself to the bone, because the most important work I'll ever do is being Indigo's *mother*.", y + 30)
out.append(slide(9, s9, ('rose54', 150, W / 2, 1060, .85)))
# 10 · imperfect
def s10(im, y):
    y = head(im, "So not everything\nhere will be perfect.", y, 54)
    return body(im, "It'll be beautifully *imperfect*. Occasionally cringe.\n\nI'm playing with a bigger picture, which mostly terrifies me. And I've decided to stay optimistic, and to keep moving towards something better for her, and for her children.", y + 30)
out.append(slide(10, s10, ('IMG_4686', 380, W / 2, 1070, .8, (0, .05, 1, .55))))
# 11 · shine
def s11(im, y):
    y = body(im, "I've spent most of my life helping other people *shine*. It was real. It was also a hiding place.\n\nThroughout my career, being seen never felt safe.", y)
    y = head(im, "I give no fucks now.", y + 50, 66); d = ImageDraw.Draw(im)
    d.text((W / 2 + 150, y + 4), "well. maybe five percent.", font=F('italic', 28), fill=QUIET, anchor='ma'); return y + 60
out.append(slide(11, s11, ('IMG_1636', 440, W / 2, 300, .9)))
# 12 · who for
def s12(im, y):
    y = body(im, "This page is for women building companies with taste and ambition, and for anyone who loves one.", y + 330)
    return head(im, "If that's you, *stay*.", y + 36, 60)
out.append(slide(12, s12, ('bloomtree', 330, W / 2, 330, .9)))
# 13 · loved ones
def s13(im, y):
    y = body(im, "And if you're here because you love me: being here is support, and I feel it.", y + 330)
    y = head(im, "Thank you for watching\nme do the thing.", y + 36, 50); dot(im, W / 2, y + 40)
    return ital(im, "Growth guided by inherent intelligence, rather than force.", y + 70, 26)
out.append(slide(13, s13, ('mumeye', 520, W / 2, 330, .9)))

for i, im in enumerate(out): im.save(f'{OUT}/Manifesto_{i+1:02d}.jpg', quality=92)
tiles = [cv2.resize(cv2.imread(f'{OUT}/Manifesto_{i+1:02d}.jpg'), (300, 375)) for i in range(N)] + [np.full((375, 300, 3), 30, np.uint8)] * 3
cv2.imwrite(f'{OUT}/sheet.jpg', np.vstack([np.hstack(tiles[i:i+4]) for i in (0, 4, 8, 12)])); print('ok')
