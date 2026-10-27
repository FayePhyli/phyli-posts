"""ten caption/grade versions on two reel frames, for her to pick from"""
import sys, os, subprocess; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import *
from lib import y2k, hx
RW, RH = 1080, 1920; OUT = 'sys/capvers'; os.makedirs(OUT, exist_ok=True)
SRC = "/mnt/user-data/uploads/Desktop/Phyli/Phyli Content CLAUDE/06 Studio & Life B-roll/"
meta = json.load(open('broll/meta.json')) if 'json' in dir() else __import__('json').load(open('broll/meta.json'))
def frame(key, t):
    p = f'{OUT}/src_{key}.jpg'
    if not os.path.exists(p): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', SRC + meta[key]['f'], '-frames:v', '1', '-vf', f'scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}', p], check=True)
    return load(p)
ROSE = '#C46E80'; LILAC = '#B8A3C9'; MAG = '#B2346E'; PINK = '#D8A9B3'; OLIVE = '#A8A77C'
def gradient_overlay(a, c0='#B8A3C9', c1='#E8B8C2', amt=0.22):
    yy = np.linspace(0, 1, RH)[:, None, None]; g = hx(c0) * (1 - yy) + hx(c1) * yy
    return a * (1 - amt) + g * amt
def vintage(a):
    x = a / 255; x = x * 0.86 + 0.08                                   # lifted blacks, softened whites
    x = x * np.array([1.04, 1.0, 0.92]); x = np.clip(x, 0, 1) ** 0.95
    m = x.mean(2, keepdims=True); x = m + (x - m) * 0.9
    rs = np.random.RandomState(3); x = x + rs.randn(RH, RW, 1) * 0.035
    yy, xx = np.mgrid[0:RH, 0:RW]; v = 1 - 0.28 * (((xx / RW - .5) ** 2 + (yy / RH - .5) ** 2)) * 2
    return np.clip(x * v[..., None] * 255, 0, 255)
GR = {'colour': lambda a: grade(a, 1.0), 'y2k': lambda a: y2k(grade(a, .6), sat=1.3, bloom=.45, soft=1.0, grain=8, warm=.03), 'y2k+grad': lambda a: gradient_overlay(y2k(grade(a, .6), sat=1.3, bloom=.45, soft=1.0, grain=8), amt=.2), 'vintage': lambda a: vintage(grade(a, .5)), 'vintage+grad': lambda a: gradient_overlay(vintage(grade(a, .5)), '#9FB0C9', '#D8A9B3', .18)}
LINES = ["it's just the worst", "of masculine energy."]; LIVE = (1, 2)   # line idx, word idx of the 'live' word
def draw(a, kind, size, col, live=None, halo=.7, box=None, strip=None, glow=None, upper=False, track=0, y=None):
    im = pil(a); d = ImageDraw.Draw(im, 'RGBA'); f = F(kind, size); LH = size * 1.15
    lines = [l.upper() if upper else l for l in LINES]; y0 = (RH - LH * len(lines)) / 2 if y is None else y
    if strip:
        d.rectangle((0, y0 - 40, RW, y0 + LH * len(lines) + 30), fill=strip)
    if halo:
        lay = Image.new('L', (RW, RH), 0); ld = ImageDraw.Draw(lay)
        for i, l in enumerate(lines): ld.text((RW / 2, y0 + i * LH), l, font=f, fill=255, anchor='ma')
        h = np.asarray(lay.filter(ImageFilter.GaussianBlur(24))).astype(np.float32) / 255 * halo
        arr = np.asarray(im).astype(np.float32) * (1 - h[..., None] * .8); im = pil(arr); d = ImageDraw.Draw(im, 'RGBA')
    if glow:
        lay = Image.new('L', (RW, RH), 0); ld = ImageDraw.Draw(lay)
        for i, l in enumerate(lines): ld.text((RW / 2, y0 + i * LH), l, font=f, fill=255, anchor='ma')
        g = np.clip(np.asarray(lay.filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255 * 2.2, 0, 1) * .8
        arr = np.asarray(im).astype(np.float32) * (1 - g[..., None]) + hx(glow) * g[..., None]; im = pil(arr); d = ImageDraw.Draw(im, 'RGBA')
    for i, l in enumerate(lines):
        words = l.split(' '); ws = [d.textlength(w, font=f) for w in words]; sp = d.textlength(' ', font=f) + track
        x = (RW - (sum(ws) + sp * (len(words) - 1))) / 2; yy = y0 + i * LH
        if box:
            d.rounded_rectangle((x - 26, yy - 10, x + sum(ws) + sp * (len(words) - 1) + 26, yy + size * 1.08 + 6), radius=12, fill=box)
        for w, ww in zip(words, ws):
            c = col
            if live and (i, words.index(w)) == LIVE: c = live
            d.text((x, yy), w, font=f, fill=c); x += ww + sp
    label(im, 'version', IVORY); fp(im, IVORY); return im
V = [
 ('01_colour_inter54_halo',      'colour',       lambda a: draw(a, 'sansm', 54, IVORY, live=(196,110,128), halo=.7)),
 ('02_y2k_inter72_halo',         'y2k',          lambda a: draw(a, 'sansb', 72, IVORY, halo=.9)),
 ('03_y2kgrad_inter66_rose',     'y2k+grad',     lambda a: draw(a, 'sansm', 66, IVORY, live=(232,184,194), halo=.9)),
 ('04_y2kgrad_rozha72_shadow',   'y2k+grad',     lambda a: draw(a, 'display', 72, IVORY, halo=.8)),
 ('05_y2k_rozha84_pink_glow',    'y2k',          lambda a: draw(a, 'display', 84, (248, 226, 232), live=(216,169,179), halo=.5, glow='#5A2A44')),
 ('06_vintage_newsreader76',     'vintage',      lambda a: draw(a, 'italic', 76, IVORY, halo=.85)),
 ('07_y2k_inter60_caps_sticker', 'y2k',          lambda a: draw(a, 'sansb', 56, (60, 30, 50), halo=0, box=(232, 184, 194, 235), upper=True, track=3)),
 ('08_y2kgrad_inter64_magenta',  'y2k+grad',     lambda a: draw(a, 'sansb', 64, (178, 52, 110), halo=0, glow='#F6E6EE')),
 ('09_colour_inter64_rosebox',   'colour',       lambda a: draw(a, 'sansm', 64, IVORY, halo=0, box=(150, 60, 95, 215))),
 ('10_vintagegrad_rozha70_strip','vintage+grad', lambda a: draw(a, 'display', 70, INK, halo=0, strip=(244, 239, 230, 205))),
]
import json
for key, t in (('45', 2.0), ('31', 9.0)):
    a0 = frame(key, t)
    for name, g, fn in V:
        im = fn(GR[g](a0)); im.save(f'{OUT}/{key}_{name}.jpg', quality=90)
# contact sheets: one per frame, 5x2
for key in ('45', '31'):
    fs = sorted([f for f in os.listdir(OUT) if f.startswith(key + '_')]); tiles = []
    for f_ in fs:
        im = Image.open(f'{OUT}/{f_}').resize((432, 768)); d = ImageDraw.Draw(im); d.rectangle((0, 0, 432, 44), fill=(20, 14, 20)); d.text((12, 10), f_[3:-4], font=F('mono', 20), fill=IVORY); tiles.append(im)
    S = Image.new('RGB', (5 * 432, 2 * 768)); [S.paste(t_, ((i % 5) * 432, (i // 5) * 768)) for i, t_ in enumerate(tiles)]; S.save(f'{OUT}/sheet_{key}.jpg', quality=88)
print('ok')

# ---- round two ----
def paper_strip(im, y0, y1, seed=5):
    """a torn ivory paper piece across the frame, not a flat rectangle"""
    rs = np.random.RandomState(seed); m = Image.new('L', (RW, RH), 0); d = ImageDraw.Draw(m)
    top = [(x, y0 + rs.randint(-14, 14)) for x in range(-20, RW + 40, 40)]; bot = [(x, y1 + rs.randint(-14, 14)) for x in range(RW + 20, -40, -40)]
    d.polygon(top + bot, fill=255); m = m.filter(ImageFilter.GaussianBlur(1.2))
    paper = pearl(RW, RH, seed=seed) * 0.35 + np.array(IVORY, float) * 0.65; paper = paper + rs.randn(RH, RW, 1) * 4
    sh = np.asarray(m.filter(ImageFilter.GaussianBlur(18))).astype(np.float32) / 255 * .45
    arr = np.asarray(im).astype(np.float32) * (1 - sh[..., None]); mm = np.asarray(m).astype(np.float32)[..., None] / 255
    return pil(arr * (1 - mm) + paper * mm)
def draw2(a, kind, size, col, lines=None, y=None, halo=.7, glow=None, pill=None, strip=False, track=0, lh=1.12, align='c', x=72):
    im = pil(a); lines = lines or LINES; f = F(kind, size); LH = size * lh; y0 = (RH - LH * len(lines)) / 2 if y is None else y
    if strip: im = paper_strip(im, y0 - 46, y0 + LH * len(lines) + 26)
    d = ImageDraw.Draw(im, 'RGBA')
    if halo:
        lay = Image.new('L', (RW, RH), 0); ld = ImageDraw.Draw(lay)
        for i, l in enumerate(lines): ld.text((RW / 2 if align == 'c' else x, y0 + i * LH), l, font=f, fill=255, anchor='ma' if align == 'c' else 'la')
        h = np.asarray(lay.filter(ImageFilter.GaussianBlur(26))).astype(np.float32) / 255 * halo
        im = pil(np.asarray(im).astype(np.float32) * (1 - h[..., None] * .8)); d = ImageDraw.Draw(im, 'RGBA')
    if glow:
        lay = Image.new('L', (RW, RH), 0); ld = ImageDraw.Draw(lay)
        for i, l in enumerate(lines): ld.text((RW / 2 if align == 'c' else x, y0 + i * LH), l, font=f, fill=255, anchor='ma' if align == 'c' else 'la')
        g = np.clip(np.asarray(lay.filter(ImageFilter.GaussianBlur(16))).astype(np.float32) / 255 * 2.2, 0, 1) * .85
        im = pil(np.asarray(im).astype(np.float32) * (1 - g[..., None]) + hx(glow) * g[..., None]); d = ImageDraw.Draw(im, 'RGBA')
    for i, l in enumerate(lines):
        w = d.textlength(l, font=f) + track * len(l); xx = (RW - w) / 2 if align == 'c' else x; yy = y0 + i * LH
        if pill: d.rounded_rectangle((xx - 30, yy - 8, xx + w + 30, yy + size * 1.1 + 4), radius=size * .6, fill=pill)
        if track:
            for ch in l: d.text((xx, yy), ch, font=f, fill=col); xx += d.textlength(ch, font=f) + track
        else: d.text((xx, yy), l, font=f, fill=col)
    label(im, 'version', IVORY); return im
V2 = [
 ('11_nocaptions_y2kgrad',          'y2k+grad', lambda a: draw2(a, 'sansm', 10, IVORY, lines=[''], halo=0)),
 ('12_pullquote_rozha96',           'y2k+grad', lambda a: draw2(a, 'display', 96, IVORY, lines=['the worst of', 'masculine energy.'], halo=.6)),
 ('13_filmsub_mono40_tracked',      'y2k+grad', lambda a: draw2(a, 'mono', 40, IVORY, y=1500, halo=.75, track=3)),
 ('14_newsreader_italic88',         'y2k+grad', lambda a: draw2(a, 'italic', 88, IVORY, halo=.7)),
 ('15_rozha72_ink_on_torn_paper',   'y2k+grad', lambda a: draw2(a, 'display', 72, INK, strip=True, halo=0)),
 ('16_inter66_aubergine_pill',      'y2k+grad', lambda a: draw2(a, 'sansm', 66, IVORY, halo=0, pill=(42, 22, 48, 200))),
 ('17_rozha80_aubergine_pinkglow',  'y2k+grad', lambda a: draw2(a, 'display', 80, (58, 28, 52), halo=0, glow='#F2D3DD')),
 ('18_oneword_rozha150',            'y2k+grad', lambda a: draw2(a, 'display', 150, IVORY, lines=['worst.'], halo=.5)),
 ('19_lowerthird_left_rozha64',     'y2k+grad', lambda a: draw2(a, 'display', 64, IVORY, y=1420, halo=.75, align='l', x=72)),
 ('20_sans_light_90_wide',          'y2k+grad', lambda a: draw2(a, 'sansl', 90, IVORY, halo=.8, track=-2)),
]
for key, t in (('45', 2.0), ('31', 9.0)):
    a0 = frame(key, t)
    for name, g, fn in V2: fn(GR[g](a0)).save(f'{OUT}/{key}_{name}.jpg', quality=90)
for key in ('45', '31'):
    fs = sorted([f for f in os.listdir(OUT) if f.startswith(key + '_') and int(f[3:5]) > 10]); tiles = []
    for f_ in fs:
        im = Image.open(f'{OUT}/{f_}').resize((432, 768)); d = ImageDraw.Draw(im); d.rectangle((0, 0, 432, 44), fill=(20, 14, 20)); d.text((12, 10), f_[3:-4], font=F('mono', 20), fill=IVORY); tiles.append(im)
    S = Image.new('RGB', (5 * 432, 2 * 768)); [S.paste(t_, ((i % 5) * 432, (i // 5) * 768)) for i, t_ in enumerate(tiles)]; S.save(f'{OUT}/sheet2_{key}.jpg', quality=88)
print('ok2')

# ---- round three: highlight colours ----
PERI = (157, 168, 224); PALE = (243, 217, 223); AUB = (58, 28, 52)
V3 = [
 ('21_periwinkle_text_ivory_glow',   lambda a: draw2(a, 'display', 80, PERI, y=1105, halo=0, glow='#F4EFE6')),
 ('22_palepink_text_aubergine_glow', lambda a: draw2(a, 'display', 80, PALE, y=1105, halo=0, glow='#3A1C34')),
 ('23_ivory_text_periwinkle_glow',   lambda a: draw2(a, 'display', 80, IVORY, y=1105, halo=0, glow='#8F9FD9')),
 ('24_ivory_text_palepink_glow',     lambda a: draw2(a, 'display', 80, IVORY, y=1105, halo=0, glow='#E8B8C2')),
 ('25_aubergine_text_periwinkle_glow', lambda a: draw2(a, 'display', 80, AUB, y=1105, halo=0, glow='#C9D2F0')),
 ('26_periwinkle_text_palepink_glow', lambda a: draw2(a, 'display', 80, (120, 134, 210), y=1105, halo=0, glow='#F6E2E7')),
]
for key, t in (('45', 2.0), ('31', 9.0)):
    a0 = GR['y2k+grad'](frame(key, t))
    for name, fn in V3: fn(a0).save(f'{OUT}/{key}_{name}.jpg', quality=90)
tiles = []
for name, _ in V3:
    for key in ('31', '45'):
        im = Image.open(f'{OUT}/{key}_{name}.jpg').resize((360, 640)); d = ImageDraw.Draw(im); d.rectangle((0, 0, 360, 40), fill=(20, 14, 20)); d.text((10, 9), name[3:], font=F('mono', 18), fill=IVORY); tiles.append(im)
S = Image.new('RGB', (6 * 360, 2 * 640)); [S.paste(t_, ((i // 2) * 360, (i % 2) * 640)) for i, t_ in enumerate(tiles)]; S.save(f'{OUT}/sheet3.jpg', quality=88); print('ok3')
