"""@faye.pressly visual system — 'the garden, not the herbarium'
Ground: the photograph (graded) or PEARL (mother-of-pearl wash from her palette). Never flat colour.
Mark: her own ink drawings, image-filled (the PHYLI wordmark device) — same hand as the house, different light.
Type: Rozha One (the one line), Newsreader italic (the aside / accent word), Inter (body), IBM Plex Mono (specimen label).
Thread: the green dot. Pop: one colour per post, taken from the photograph.
"""
import sys, os, re, math
sys.path.insert(0, 'look')
from lib import hx, load, fit
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1350
FD = 'fonts/'; FI = '/usr/share/fonts/opentype/inter/'
def F(kind, size):
    p = {'display': FD + 'RozhaOne-Regular.ttf', 'italic': FD + 'Newsreader-Italic.ttf', 'serif': FD + 'Newsreader.ttf', 'mono': FD + 'IBMPlexMono-Regular.ttf',
         'sans': FI + 'Inter-Regular.otf', 'sansm': FI + 'Inter-Medium.otf', 'sansb': FI + 'Inter-Bold.otf', 'sansl': FI + 'Inter-Light.otf'}[kind]
    f = ImageFont.truetype(p, size)
    if kind in ('italic', 'serif'):
        try: f.set_variation_by_axes([420, 14])
        except Exception: pass
    return f
IVORY = (244, 239, 230); INK = (28, 22, 26); QUIET = (122, 114, 121); GREEN = (152, 168, 90)
POPS = {'olive': (118, 122, 60), 'magenta': (178, 52, 110), 'orange': (214, 110, 54), 'turquoise': (58, 150, 150), 'slate': (84, 104, 150), 'rose': (196, 110, 128)}
PALETTE = ['#9FB0C9', '#B8A3C9', '#D8A9B3', '#A8A77C', '#E6D4BE', '#C9D6CC']   # slate · mauve · dusty rose · olive · champagne · sage

# ---------- photographic grade (her Esti recipe) ----------
def grade(a, strength=1.0):
    x = np.clip(a, 0, 255) / 255.0
    s = strength
    x = np.clip((x - 0.5) * (1 + 0.28 * s) + 0.5, 0, 1)              # contrast
    x = x ** (1 + 0.14 * s)                                            # darker mids
    m = x.mean(2, keepdims=True); x = np.clip(m + (x - m) * (1 + 0.55 * s), 0, 1)   # saturation
    L = x.mean(2, keepdims=True)
    warm = np.array([1 + .06 * s, 1.0, 1 - .10 * s]); cool = np.array([1 - .03 * s, 1 - .01 * s, 1 + .05 * s])
    x = np.clip(x * (L * warm + (1 - L) * cool), 0, 1)                 # split tone
    u8 = (x * 255).astype(np.uint8); hsv = cv2.cvtColor(u8, cv2.COLOR_RGB2HSV).astype(np.float32)
    hh, ss, vv = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    g = ((hh > 35) & (hh < 85)).astype(np.float32)                     # greens → olive
    g = cv2.GaussianBlur(g, (0, 0), 3)
    hsv[..., 0] = hh - 10 * g * s; hsv[..., 1] = ss * (1 - 0.3 * g * s)
    x = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32) / 255
    hi = np.clip(x - 0.6, 0, 1); bl = cv2.GaussianBlur(hi, (0, 0), 22)
    x = 1 - (1 - x) * (1 - bl * 0.18 * s)                              # bloom
    rs = np.random.RandomState(7); x = x + (rs.randn(*x.shape[:2])[..., None]) * 0.018 * s   # grain
    return np.clip(x * 255, 0, 255)

# ---------- pearl ground ----------
def pearl(w=W, h=H, seed=1, tone=0.0, dark=False):
    """mother-of-pearl: high-key champagne ground, soft pastel clouds from her palette, an oil-film sheen"""
    rs = np.random.RandomState(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    base = hx('#2B2333') if dark else hx('#F3EEE9')
    cols = ['#A9BAD6', '#C7B2DA', '#E8B8C2', '#B9B88C', '#F0DCC6', '#CFE0D6']
    rs.shuffle(cols); g = np.ones((h, w, 3)) * base
    for c in cols:
        cx, cy = rs.uniform(-.1, 1.1) * w, rs.uniform(-.1, 1.1) * h; sg = rs.uniform(.25, .45) * w
        wgt = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * sg * sg))[..., None] * (0.55 if dark else 0.42)
        g = g * (1 - wgt) + (hx(c) * (0.55 if dark else 1.0)) * wgt
    n = cv2.GaussianBlur(rs.rand(h // 8 + 1, w // 8 + 1).astype(np.float32), (0, 0), 7); n = cv2.resize(n, (w, h))
    ph = xx * 0.0040 + yy * 0.0026 + n * 5.0 + tone
    sheen = (np.sin(ph) * .5 + .5)[..., None]
    film = np.stack([np.sin(ph), np.sin(ph + 2.1), np.sin(ph + 4.2)], -1) * (9 if dark else 7)
    hi = hx('#6A5A7A') if dark else hx('#FFFDF8')
    g = g * (1 - 0.16 * sheen) + hi * 0.16 * sheen + film
    g = g + rs.randn(h, w, 1) * 1.3
    v = 1 - (0.10 if dark else 0.06) * (((xx / w - .5) ** 2 + (yy / h - .5) ** 2))[..., None] * 2
    return np.clip(g * v, 0, 255)

def img(path, w, h, focus=(.5, .5), zoom=1.0, g=1.0): return np.clip(grade(fit(load(path), w, h, focus, zoom), g), 0, 255)
def pil(a): return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGB')

# ---------- image-filled ink (the wordmark device) ----------
def ink_mask(name):
    for p in (f'fp/web/{name}_a.png', f'lib/ink_a/{name}.png', f'mock/ink/{name}.png'):
        if os.path.exists(p):
            im = Image.open(p); return im.split()[-1] if im.mode in ('RGBA', 'LA') else im.convert('L')
    raise FileNotFoundError(name)
def inkfill(base, name, fill, w, cx, cy, rot=0, op=1.0, soft=0, tone=0.72, bold=0):
    """fill = np array image (any size, resized to the mark) or an RGB tuple; bold = dilate px"""
    a = ink_mask(name); s = w / a.size[0]; a = a.resize((int(a.size[0] * s), int(a.size[1] * s)), Image.LANCZOS)
    if bold: a = a.filter(ImageFilter.MaxFilter(bold * 2 + 1))
    if rot: a = a.rotate(rot, expand=True, resample=Image.BICUBIC)
    if soft: a = a.filter(ImageFilter.GaussianBlur(soft))
    a = a.point(lambda v: int(v * op))
    if isinstance(fill, tuple): layer = Image.new('RGB', a.size, fill)
    else:
        f_ = fit(fill, a.size[0], a.size[1]); m_ = f_.mean()
        f_ = (f_ - m_) * 1.25 + m_ * tone                 # contrast up, darkened so the mark reads on pearl
        layer = pil(f_)
    out = base.copy(); out.paste(layer, (int(cx - a.size[0] / 2), int(cy - a.size[1] / 2)), a); return out

# ---------- type ----------
def wrap(d, text, f, maxw):
    out = []
    for para in text.split('\n'):
        line = ''
        for w_ in para.split():
            t = (line + ' ' + w_).strip()
            if d.textlength(t, font=f) > maxw and line: out.append(line); line = w_
            else: line = t
        out.append(line)
    return out
def text(im, t, kind, size, x, y, col=IVORY, maxw=900, align='l', lh=1.18, shadow=0, acc=None, acc_kind='italic', acc_scale=1.0):
    """*word* → accent face in acc colour; returns bottom y"""
    d = ImageDraw.Draw(im); fb = F(kind, size); fa = F(acc_kind, int(size * acc_scale))
    toks = []
    for para in t.split('\n'):
        for w_ in re.findall(r'\*[^*]+\*\S*|\S+', para):
            if w_.startswith('*') and '*' in w_[1:]:
                k = w_.index('*', 1); toks.append((w_[1:k], True, False))
                if w_[k + 1:]: toks.append((w_[k + 1:], False, True))
            else: toks.append((w_, False, False))
        toks.append(('\n', None, False))
    toks = toks[:-1]
    sp = d.textlength(' ', font=fb); wl = lambda s_, a_: d.textlength(s_, font=fa if a_ else fb)
    lines = [[]]; cur = 0
    for s_, a_, glue in toks:
        if a_ is None: lines.append([]); cur = 0; continue
        ww = wl(s_, a_)
        if cur and not glue and cur + sp + ww > maxw: lines.append([]); cur = 0
        lines[-1].append((s_, a_, glue)); cur += (0 if glue or not cur else sp) + ww
    step = size * lh; yy = y
    asc_b = fb.getmetrics()[0]; asc_a = fa.getmetrics()[0]
    for ln in lines:
        total = sum(wl(s_, a_) for s_, a_, g in ln) + sp * sum(1 for k, (s_, a_, g) in enumerate(ln) if k and not g)
        xx = x if align == 'l' else (W - total) / 2 if align == 'c' else x - total
        for k, (s_, a_, g) in enumerate(ln):
            f = fa if a_ else fb; c = (acc or col) if a_ else col; dy = (asc_b - asc_a) if a_ else 0
            if shadow:
                d.text((xx + 2, yy + dy + 3), s_, font=f, fill=(0, 0, 0, 0));
            d.text((xx, yy + dy), s_, font=f, fill=c)
            xx += wl(s_, a_) + (0 if (k + 1 < len(ln) and ln[k + 1][2]) else sp)
        yy += step
    return yy
def shadowed(im, t, kind, size, x, y, col=IVORY, **kw):
    """soft dark halo under type for photographs"""
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); tmp = Image.new('RGB', im.size, (0, 0, 0))
    text(tmp, t, kind, size, x, y, col=(255, 255, 255), **{k: v for k, v in kw.items() if k != 'acc'}, acc=(255, 255, 255))
    m = tmp.convert('L').filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(min(255, v * 0.9)))
    layer.paste((20, 14, 20, 255), (0, 0), m); out = im.convert('RGBA'); out.alpha_composite(layer); out = out.convert('RGB')
    return out, text(out, t, kind, size, x, y, col=col, **kw)
def spaced(d, xy, t, f, fill, track=.22, anchor='l'):
    x, y = xy; ws = [d.textlength(ch, font=f) for ch in t]; tr = f.size * track; total = sum(ws) + tr * (len(t) - 1)
    if anchor == 'r': x -= total
    if anchor == 'c': x -= total / 2
    for ch, w_ in zip(t, ws): d.text((x, y), ch, font=f, fill=fill); x += w_ + tr
def label(im, t, col=IVORY, y=78): spaced(ImageDraw.Draw(im), (72, y), t.lower(), F('mono', 17), col, .18)
def fp(im, col=IVORY): ImageDraw.Draw(im).text((W - 72, 62), 'fp', font=F('italic', 44), fill=col, anchor='ra')
def num(im, i, n, col=IVORY): spaced(ImageDraw.Draw(im), (W - 72, H - 84), f'{i:02d} / {n:02d}', F('mono', 15), col, .18, 'r')
def dot(im, cx, cy, r=8): ImageDraw.Draw(im).ellipse((cx - r, cy - r, cx + r, cy + r), fill=GREEN)
def underline(im, x0, x1, y, col, seed=0, width=4):
    d = ImageDraw.Draw(im); rs = np.random.RandomState(seed); pts = []
    n = int((x1 - x0) / 6)
    for i in range(n + 1):
        t = i / n; pts.append((x0 + (x1 - x0) * t, y + math.sin(t * 9 + seed) * 2.2 + rs.randn() * 0.7))
    d.line(pts, fill=col, width=width, joint='curve')
def hairline(im, x0, x1, y, col=(255, 255, 255), op=120):
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).line((x0, y, x1, y), fill=col + (op,), width=1)
    out = im.convert('RGBA'); out.alpha_composite(ov); return out.convert('RGB')
def darken(im, top=0.0, bottom=0.45):
    a = np.asarray(im).astype(float); h = a.shape[0]; g = np.linspace(top, bottom, h)[:, None, None]; return pil(a * (1 - g))
def vignette(im, amt=.25):
    a = np.asarray(im).astype(float); yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    v = 1 - amt * (((xx / a.shape[1] - .5) ** 2 + (yy / a.shape[0] - .5) ** 2) * 2); return pil(a * v[..., None])
