"""two more covers: the 'notice of change of use' pasted on the graffiti door, and the press release. plus the landing-card fix."""
import sys, os, math; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import *
import cv2
OUT = 'sys/week1/manifesto10'; ROSE = (196, 86, 122)
# ---------- the poster itself (paper, portrait halftoned, the notice) ----------
PW, PH = 900, 1330
rs = np.random.RandomState(3)
paper = np.ones((PH, PW, 3), np.float32) * np.array([236, 229, 216], np.float32)
paper += cv2.resize(rs.randn(PH // 6, PW // 6, 1).astype(np.float32), (PW, PH))[..., None] * 5 if False else rs.randn(PH, PW, 1) * 4
yy, xx = np.mgrid[0:PH, 0:PW]; paper *= (1 - 0.12 * ((xx / PW - .5) ** 2 + (yy / PH - .5) ** 2) * 2)[..., None]   # aged edges
pp = pil(paper); d = ImageDraw.Draw(pp)
# frame rule
d.rectangle((28, 28, PW - 28, PH - 28), outline=(40, 32, 36), width=3); d.rectangle((40, 40, PW - 40, PH - 40), outline=(40, 32, 36), width=1)
def mono_c(t, y, size, col=(40, 32, 36), track=.32): spaced(d, (PW / 2, y), t.upper(), F('mono', size), col, track, 'c')
mono_c('public notice', 70, 20)
y = text(pp, "Notice of\nchange of use", 'display', 74, 60, 110, col=(28, 22, 26), maxw=PW - 120, align='c', lh=1.0)
underline(pp, 200, PW - 200, y + 6, (28, 22, 26), seed=5, width=3)
# the portrait, halftoned, like a photocopied poster
por = Image.open('fp/web/portrait.png').convert('L').resize((520, 486), Image.LANCZOS)
a = np.asarray(por).astype(np.float32); a = np.clip((a - 110) * 1.9 + 128, 0, 255)
h = Image.fromarray(a.astype(np.uint8))
# halftone: threshold against a dot grid
g = np.asarray(h).astype(np.float32) / 255; Y, X = np.mgrid[0:486, 0:520]; cell = 5
dots = (np.sin(X * math.pi / cell) * np.sin(Y * math.pi / cell)) * .5 + .5
ht = (g > dots * 0.95 + 0.02).astype(np.uint8) * 255
ht = Image.fromarray(ht).convert('RGB'); ht_arr = np.asarray(ht).astype(np.float32)
inkcol = np.array([44, 30, 40], np.float32); papercol = np.array([236, 229, 216], np.float32)
blk = ht_arr[..., :1] / 255; plate = inkcol * (1 - blk) + papercol * blk
pp.paste(pil(plate), ((PW - 520) // 2, int(y) + 36)); d = ImageDraw.Draw(pp)
d.rectangle(((PW - 520) // 2 - 2, int(y) + 34, (PW + 520) // 2 + 2, int(y) + 36 + 486 + 2), outline=(40, 32, 36), width=2)
y2 = int(y) + 36 + 486 + 34
mono_c('faye pressly  ·  founder, phyli', y2, 17, (90, 80, 88)); y2 += 48
y2 = text(pp, "Notice is hereby given that an application has been made to change the use of this account.", 'serif', 25, 90, y2, col=(28, 22, 26), maxw=PW - 180, align='c', lh=1.32) + 18
mono_c('from', y2, 15, (90, 80, 88)); y2 += 26
y2 = text(pp, "a quiet personal Instagram,\nmostly watching other people's stories.", 'italic', 27, 90, y2, col=(28, 22, 26), maxw=PW - 160, align='c', lh=1.25) + 16
mono_c('to', y2, 15, (90, 80, 88)); y2 += 26
y2 = text(pp, "the professional personal brand\nof the founder of Phyli.", 'italic', 27, 90, y2, col=(28, 22, 26), maxw=PW - 160, align='c', lh=1.25) + 20
y2 = text(pp, "Objections may be lodged in the comments.\nThey will be read, and ignored.", 'serif', 23, 90, y2, col=(60, 50, 58), maxw=PW - 160, align='c', lh=1.3)
mono_c('25 . x . 2026     ·     palma', PH - 86, 15, (90, 80, 88))
pp.save('sys/notice_poster.jpg', quality=92)

# ---------- paste it on the graffiti door ----------
bg = Image.open('g30/src/mum12.jpg').convert('RGB'); BW, BH = bg.size      # 1500 x 2000
# target quad on the door's left panel, slightly skewed, as if pasted by hand
tw, th = 640, 946; x0, y0 = 300, 440
quad = np.float32([[x0 + 10, y0 + 6], [x0 + tw - 4, y0 - 4], [x0 + tw + 2, y0 + th + 2], [x0 - 2, y0 + th - 10]])
src = np.float32([[0, 0], [PW, 0], [PW, PH], [0, PH]]); M = cv2.getPerspectiveTransform(src, quad)
post = np.asarray(pp).astype(np.float32)
# wrinkles: a low-frequency displacement + shading
rs = np.random.RandomState(9); n = cv2.resize(cv2.GaussianBlur(rs.rand(12, 9).astype(np.float32), (0, 0), 1.2), (PW, PH)); n = (n - n.mean()) * 2
shade = 1 + 0.10 * n; post = np.clip(post * shade[..., None], 0, 255)
warped = cv2.warpPerspective(post, M, (BW, BH), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0))
mask = cv2.warpPerspective(np.ones((PH, PW), np.float32), M, (BW, BH))
bga = np.asarray(bg).astype(np.float32)
# the paper takes the wall's light: multiply with the door's luminance, softly
lum = cv2.GaussianBlur(bga.mean(2), (0, 0), 6) / 255; lum = np.clip(lum * 0.55 + 0.6, 0, 1.15)
comp = warped * lum[..., None]
# drop shadow under the sheet
sh = cv2.GaussianBlur(mask, (0, 0), 9); sh = np.roll(sh, (8, 6), (0, 1)) * 0.45
out = bga * (1 - sh[..., None]) ; out = out * (1 - mask[..., None]) + comp * mask[..., None]
# tape at the corners
im = pil(out); d = ImageDraw.Draw(im, 'RGBA')
for (cx, cy, ang) in [(quad[0][0] + 8, quad[0][1] + 6, 40), (quad[1][0] - 8, quad[1][1] + 8, -40), (quad[2][0] - 8, quad[2][1] - 8, 40), (quad[3][0] + 8, quad[3][1] - 8, -40)]:
    tape = Image.new('RGBA', (120, 44), (230, 222, 200, 150)); tape = tape.rotate(ang, expand=True, resample=Image.BICUBIC)
    im.paste(tape, (int(cx - tape.size[0] / 2), int(cy - tape.size[1] / 2)), tape)
# crop to 4:5 around the door, grade vintage
a = np.asarray(im).astype(np.float32); cw, ch = 1180, 1475; cx0, cy0 = 160, 230
a = a[cy0:cy0 + ch, cx0:cx0 + cw]
a = grade(a, .7); a = a * 0.9 + np.array([246, 234, 214], np.float32) * 0.1          # lifted, warm, faded
a = a + rs.randn(ch, cw, 1) * 6
cover2 = pil(a).resize((W, H), Image.LANCZOS); cover2.save(f'{OUT}/Cover_B_notice.jpg', quality=92)

# ---------- the press release ----------
im = pil(pearl(seed=611, tone=2.5) * 0.7 + np.array(IVORY, float) * 0.3); d = ImageDraw.Draw(im)
spaced(d, (72, 110), 'FOR IMMEDIATE RELEASE', F('mono', 20), INK, .36); underline(im, 62, 500, 150, INK, seed=3, width=3)
spaced(d, (W - 72, 112), 'PALMA  ·  26 . X . 2026', F('mono', 16), QUIET, .3, 'r')
y = text(im, "Faye Pressly\nto stop lurking.", 'display', 84, 72, 300, col=INK, maxw=936, lh=1.0)
y = text(im, "PALMA, Mallorca — Faye Pressly, founder of Phyli and a woman who has watched everyone else's stories for two years, announced today that she will be posting.", 'serif', 30, 72, y + 50, col=INK, maxw=900, lh=1.38)
y = text(im, "The programme is understood to include outfits, ink, a business book in twelve volumes, and the founder changing her mind in public.", 'serif', 30, 72, y + 26, col=INK, maxw=900, lh=1.38)
y = text(im, "Asked for comment, Ms Pressly said: *\"I give no fucks now. Well. Maybe five percent.\"*", 'serif', 30, 72, y + 26, col=INK, maxw=900, lh=1.38, acc=INK)
spaced(d, (W / 2, y + 60), 'ENDS', F('mono', 16), QUIET, .4, 'c')
spaced(d, (72, H - 120), 'ENQUIRIES  ·  @PHYLI.STUDIO', F('mono', 15), QUIET, .3)
im.paste(Image.new('RGB', (1, 1)), (0, 0)); im.save(f'{OUT}/Cover_C_press.jpg', quality=92)
print('ok')
