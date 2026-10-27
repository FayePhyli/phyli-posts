"""the two manifesto covers from the website portrait.
A (reel, Tue): the portrait full-bleed in the grid's colour-tile style, bold sans 'a note, before this page changes.' with glow.
B (carousel, Wed): the portrait on ivory, Rozha, the grid's ivory-break family (made earlier as Manifesto_cover_4x5.jpg; re-made here with the green dot)."""
exec(open('g60/build.py').read())
src = open('g60/final.py').read(); exec(src[src.index('def big'):src.index('T=[None]*21')])
import sys; sys.path.insert(0, 'sys'); import style as S
os.makedirs('send/manifesto', exist_ok=True)
por = np.array(Image.open('fp/web/portrait.png').convert('RGB')).astype(float)      # 941 x 878
# upscale with a little softness + grain so the enlargement reads as film, not pixels
up = cv2.resize(por, None, fx=1.9, fy=1.9, interpolation=cv2.INTER_LANCZOS4)
a = grade(F(up, (.58, .45)), warm=.02, sat=1.08, bloom=.3, grain=8)
A = big(a, ['a note,', 'before this', 'page changes.'], IV, 118, y=1000, glow='#B48CF0', ga=.5, shadow=.4)
Image.fromarray(np.clip(A, 0, 255).astype(np.uint8)).save('send/manifesto/Manifesto_reel_cover_TUE.jpg', quality=93)
# 9:16 version of the same for the reel's cover frame
up2 = cv2.resize(por, None, fx=2.3, fy=2.3, interpolation=cv2.INTER_LANCZOS4)
a2 = grade(F(up2, (.58, .45), 1.0) if False else cv2.resize(up2, (1080, 1920)) if False else F(up2, (.58, .45)), warm=.02, sat=1.08, bloom=.3, grain=8)
# F() fits to TW x TH (1080x1350); build the 9:16 by padding the 4:5 tile top and bottom with the tile's own edge colour
pad = np.zeros((1920, 1080, 3)) + np.median(A[:40].reshape(-1, 3), 0); pad[285:285 + 1350] = A
Image.fromarray(np.clip(pad, 0, 255).astype(np.uint8)).save('send/manifesto/Manifesto_reel_cover_9x16.jpg', quality=93)

# B: portrait on ivory (carousel cover)
W, H = 1080, 1350
im = Image.new('RGB', (W, H), S.IVORY); arr = np.asarray(im).astype(np.float32); rs = np.random.RandomState(2); arr += rs.randn(H, W, 1) * 2.2; im = S.pil(arr)
p = Image.open('fp/web/portrait.png').convert('RGB'); pw = 760; p = p.resize((pw, int(pw * p.size[1] / p.size[0])), Image.LANCZOS)
pa = np.asarray(p).astype(np.float32) * 0.96 + np.array(S.IVORY, np.float32) * 0.04; p = S.pil(pa); im.paste(p, ((W - pw) // 2, 200))
d = ImageDraw.Draw(im)
S.spaced(d, (W / 2, 96), 'faye pressly  ·  founder, phyli', S.F('mono', 17), S.QUIET, .3, 'c')
y = S.text(im, "a note, before\nthis page changes.", 'display', 66, 72, 960, col=(58, 62, 138), maxw=W - 144, align='c', lh=1.04)
S.dot(im, W / 2, y + 46)
S.spaced(d, (W - 72, H - 84), '01 / 12', S.F('mono', 15), S.QUIET, .18, 'r')
im.save('send/manifesto/Manifesto_carousel_cover_WED.jpg', quality=93)
sheet = Image.new('RGB', (2 * 540 + 20, 675), (30, 30, 30)); sheet.paste(Image.open('send/manifesto/Manifesto_reel_cover_TUE.jpg').resize((540, 675)), (0, 0)); sheet.paste(im.resize((540, 675)), (560, 0)); sheet.save('send/manifesto/covers_sheet.jpg', quality=88)
print('ok')
