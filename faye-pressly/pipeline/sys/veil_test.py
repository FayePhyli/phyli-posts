"""the firelight grade, on three frames: near-monochrome aubergine and silver, only the flame keeps its colour, a drifting veil of smoke, grain, vignette, cream Rozha."""
import sys, os, subprocess; sys.path.insert(0, 'sys')
from style import *
import cv2
OUT = 'sam/test'; os.makedirs(OUT, exist_ok=True); RW, RH = 1080, 1920
def frame(path, t):
    out = f'{OUT}/_f.png'; subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', path, '-frames:v', '1', out], check=True)
    a = np.array(Image.open(out).convert('RGB')).astype(np.float32); h, w = a.shape[:2]
    s = max(RW / w, RH / h); a = cv2.resize(a, (int(w * s) + 1, int(h * s) + 1)); y0 = (a.shape[0] - RH) // 2; x0 = (a.shape[1] - RW) // 2; return a[y0:y0 + RH, x0:x0 + RW]
def veil(seed, strength=.22):
    """a slow smoke: layered low-frequency noise, lifted to silver"""
    rs = np.random.RandomState(seed); n = np.zeros((RH, RW), np.float32)
    for k, sc in enumerate([6, 12, 24, 48]):
        m = cv2.resize(rs.rand(RH // sc + 2, RW // sc + 2).astype(np.float32), (RW, RH), interpolation=cv2.INTER_CUBIC); n += m / (k + 1)
    n = cv2.GaussianBlur(n, (0, 0), 18); n = (n - n.min()) / (n.max() - n.min()); return (n ** 2.2) * strength
def firelight(a, seed=1, warm_keep=.85, vig=.42):
    # luminance to aubergine/silver: shadows plum, mids mauve-grey, highlights silver
    g = a.mean(2) / 255; g = np.clip((g - .08) * 1.25, 0, 1) ** 0.95
    shadow = np.array([26, 14, 30.]); mid = np.array([120, 96, 122.]); high = np.array([214, 206, 216.])
    mono = np.where(g[..., None] < .5, shadow + (mid - shadow) * (g[..., None] / .5), mid + (high - mid) * ((g[..., None] - .5) / .5))
    # keep the flame: warm, saturated, bright pixels stay in colour
    r, gg, b = a[..., 0], a[..., 1], a[..., 2]; warmth = np.clip((r - b) / 90, 0, 1) * np.clip((r + gg) / 2 / 150, 0, 1); keep = cv2.GaussianBlur(warmth, (0, 0), 3)[..., None] * warm_keep
    col = a * np.array([1.05, .9, .75]); out = mono * (1 - keep) + col * keep
    # the veil, grain, vignette
    v = veil(seed)[..., None]; out = out * (1 - v) + np.array([200, 190, 205.]) * v
    rs = np.random.RandomState(seed + 7); out = out + rs.randn(RH, RW, 1) * 10
    yy, xx = np.mgrid[0:RH, 0:RW]; rr = np.sqrt(((xx - RW / 2) / (RW / 2)) ** 2 + ((yy - RH / 2) / (RH / 2)) ** 2); out = out * (1 - vig * np.clip(rr - .45, 0, 1) / 1.0)[..., None]
    return np.clip(out, 0, 255)
def caption(im, t, size=80, cy=1180, col=(244, 236, 214)):
    tmp = Image.new('RGB', (RW, RH)); d = ImageDraw.Draw(tmp); f = F('display', size); d.text((RW / 2, cy), t, font=f, fill=(255, 255, 255), anchor='mm')
    A = np.asarray(tmp.convert('L')).astype(np.float32) / 255; G = np.clip(cv2.GaussianBlur(A, (0, 0), 18) * 1.6, 0, 1) * .55
    a = np.asarray(im).astype(np.float32); a = a * (1 - G[..., None]) + np.array([180, 90, 60.]) * G[..., None]; a = a * (1 - A[..., None]) + np.array(col, float) * A[..., None]; return pil(a)
tests = [('sam/vid/39A7BF25.mp4', 1.5, 'one year ago tonight', 1), ('broll/px/IMG_1816.mp4', 3.0, 'the night the veil is thinnest', 2), ('sam/vid/IMG_1783.mp4', 4.0, "Lara's beautiful yurt", 3)]
tiles = []
for p, t, cap, sd in tests:
    im = caption(pil(firelight(frame(p, t), sd)), cap); im.save(f'{OUT}/veil_{sd}.jpg', quality=92); tiles.append(im.resize((405, 720)))
S = Image.new('RGB', (3 * 405 + 20, 720), (20, 20, 20))
for i, t in enumerate(tiles): S.paste(t, (i * 415, 0))
S.save(f'{OUT}/sheet.jpg', quality=88); print('ok')
