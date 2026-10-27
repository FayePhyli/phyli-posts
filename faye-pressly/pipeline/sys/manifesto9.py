"""the manifesto v4: the original copy (minus the door slide and 'go gently'), the website portrait on the cover, photo-led inside: full-bleed, darkened, no boxes, no pearl, no ink."""
import sys, os; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import *
import cv2
G = 'g30/src/'; S = 'sys/src/'; C = 'fp/web2/'; OUT = 'sys/week1/manifesto9'; os.makedirs(OUT, exist_ok=True)
PALE = (232, 184, 194); N = 13
def measure(parts):
    tmp = Image.new('RGB', (W, H)); y = 0
    for kind, size, t, lh, gap in parts: y = text(tmp, t, kind, size, 72, y, maxw=936, lh=lh) + gap
    return y
def page(photo, parts, focus=(.5, .5), zoom=1.0, g=1.0, top=.12, bottom=.62, i=0, pad=120):
    im = pil(img(photo, W, H, focus, zoom, g)); im = vignette(darken(im, top, bottom), .22)
    h = measure(parts); y = H - pad - h
    for kind, size, t, lh, gap in parts:
        col = (190, 182, 190) if kind == 'italic' else IVORY
        im, y = shadowed(im, t, kind, size, 72, y, col=col, maxw=936, lh=lh, acc=PALE); y += gap
    num(im, i, N); return im
HEAD = lambda t: ('display', 46, t, 1.1, 22); BODY = lambda t: ('sans', 29, t, 1.36, 18); SMALL = lambda t: ('italic', 30, t, 1.3, 0)

out = []
# 01 · cover: the website portrait on ivory, title in the grid's bold sans
im = Image.new('RGB', (W, H), IVORY); p = Image.open('fp/web/portrait.png').convert('RGB'); p = p.resize((W, int(p.size[1] * W / p.size[0])), Image.LANCZOS); im.paste(p, (0, 0))
text(im, "a note, before\nthis page changes.", 'sansb', 58, 72, p.size[1] + 70, col=INK, maxw=936, align='c', lh=1.08); out.append(im)
# 02 · twenty years (the bomber jacket, walking away down the old street)
out.append(page(S + 'bomber.jpg', [BODY("For almost twenty years I've run and grown the inside of companies, for other people.\n\nNow I'm building *Phyli*: a place for my thoughts, wisdom and ideas to come to life, for other women running and growing their own companies as if they are alive."), SMALL("Because they are.")], (.5, .5), 1.0, i=2))
# 03 · the mission (her mother's PHYLI stack)
out.append(page(C + 'phyli_stack.png', [HEAD("I want to curate the most beautiful business book in the *world*."), BODY("Twelve volumes. Pages that open out, lift and unfold, the way the books we loved as children did. Made by hand, from the materials of couture. Carrying the content of a business book that feels timeless.")], (.5, .3), 1.0, g=.4, i=3))
# 04 · why
out.append(page(S + 'headscarf.jpg', [HEAD("Adult books stopped being *beautiful* a long time ago."), BODY("Made as cheap as possible, shipped to as many as possible. This is the opposite of that. A book you keep, and hand down.\n\nBecause the women building thoughtful companies deserve wisdom that doesn't shout. Because I needed it, and couldn't find it. Because this has felt channelled for a long time, and I'd rather be the hands than argue with it.\n\nAnd because one day my daughter will ask what I made with my life. I want the answer to be beautiful.")], (.5, .25), 1.0, top=.2, bottom=.7, i=4, pad=90))
# 05 · what I care about (the magenta butterflies)
out.append(page(C + 'magenta.png', [HEAD("I care about *truth*, *beauty*, craft,"), BODY("and work that outlives the week it was posted in.")], (.5, .4), 1.0, g=.4, i=5))
# 06 · what I don't (the mirror dance)
out.append(page(S + 'mirror_dance.jpg', [HEAD("What I don't care for: hacks, hustle, being everywhere, going viral."), BODY("I'm not trying to be fast.\nI'm trying to be *aligned*, and connected, for a very long time.")], (.5, .4), 1.0, i=6))
# 07 · the dream (the Collectors' volume)
out.append(page(C + 'womb_book.png', [BODY("My dream is to launch in an art gallery. The Collectors' Volumes, numbered and bound by hand, by masters of their trade. MoMA's bookshop. *Vogue*.\n\nA business book you'd leave on the table because it's beautiful, and then actually read.")], (.5, .4), 1.0, g=.4, i=7))
# 08 · pause (the horse)
out.append(page(S + 'horse.jpg', [HEAD("If you read it,\nI want you to *pause*."), BODY("To recognise something you already knew. To find pleasure in it. Not another fast thing to consume, and extract from you.")], (.5, .5), 1.0, i=8))
# 09 · not my whole life (the sunset road)
out.append(page(S + 'sunset_road.jpg', [HEAD("And it will not\ntake over my life."), BODY("I'll share what I know without draining myself to the bone, because the most important work I'll ever do is being Indigo's *mother*.")], (.5, .4), 1.0, i=9))
# 10 · imperfect (the hair flip)
out.append(page(S + 'hairflip.jpg', [HEAD("So not everything\nhere will be perfect."), BODY("It'll be beautifully *imperfect*. Occasionally cringe.\n\nI'm playing with a bigger picture, which mostly terrifies me. And I've decided to stay optimistic, and to keep moving towards something better for her, and for her children.")], (.5, .3), 1.0, i=10))
# 11 · shine (the stairs)
out.append(page(G + 'faye33.jpg', [BODY("I've spent most of my life helping other people *shine*. It was real. It was also a hiding place.\n\nThroughout my career, being seen never felt safe."), ('display', 54, "I give no fucks now.", 1.1, 6), SMALL("Well. Maybe five percent.")], (.5, .3), 1.0, i=11))
# 12 · who for (the white village doorway)
out.append(page(S + 'village.jpg', [BODY("This page is for women building companies with taste and ambition, and for anyone who loves one."), ('display', 54, "If that's you, *stay*.", 1.1, 0)], (.5, .5), 1.0, i=12))
# 13 · loved ones
im = page(G + 'faye104.jpg', [BODY("And if you're here because you love me: being here is support, and I feel it."), HEAD("Thank you for watching\nme do the thing."), SMALL("Growth guided by inherent intelligence, rather than force.")], (.5, .35), 1.0, i=13)
out.append(im)

for i, im in enumerate(out): im.save(f'{OUT}/Manifesto_{i+1:02d}.jpg', quality=92)
tiles = [cv2.resize(cv2.imread(f'{OUT}/Manifesto_{i+1:02d}.jpg'), (300, 375)) for i in range(N)] + [np.full((375, 300, 3), 30, np.uint8)] * 3
cv2.imwrite(f'{OUT}/sheet.jpg', np.vstack([np.hstack(tiles[i:i+4]) for i in (0, 4, 8, 12)])); print('ok')
