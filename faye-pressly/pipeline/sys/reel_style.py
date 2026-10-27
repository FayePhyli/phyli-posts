"""colour trial reels: y2k + gradient grade per frame, Rozha captions just below centre.
usage: python3 sys/reel_style.py <name> <style: 12|17> <label> <out.mp4>"""
import sys, os, re, json, subprocess
sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import F, IVORY, spaced, grade
from lib import y2k, hx
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import pillow_heif; pillow_heif.register_heif_opener()
name, STYLE, LABEL, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
RW, RH, FPS = 1080, 1920, 30
SRC = "/mnt/user-data/uploads/Desktop/Phyli/Phyli Content CLAUDE/06 Studio & Life B-roll/"
meta = json.load(open('broll/meta.json'))
T = json.load(open(f'vo/{name}_timeline.json')); words = [w['w'] for w in T['words']]; times = [(w['s'], w['e']) for w in T['words']]; D = T['D']
SHOTS = json.load(open(f'sys/shots_{name}.json')); tot = sum(s[2] for s in SHOTS); sc = D / tot
wd = f'sys/r_{name}_col'; os.makedirs(wd, exist_ok=True); segs = []
for i, (k, ip, d, fx, fy) in enumerate(SHOTS):
    d *= sc; m = meta[k]; src = SRC + m['f']; out = f'{wd}/{i:02d}.mp4'; segs.append(out)
    if os.path.exists(out): continue
    if ip + d > m['d'] - 0.1: ip = max(0, m['d'] - d - 0.1)
    vf = f"scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}:'(iw-{RW})*{fx}':'(ih-{RH})*{fy}',fps={FPS},setsar=1"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{ip:.2f}', '-i', src, '-t', f'{d:.3f}', '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], check=True)
open(f'{wd}/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{wd}/list.txt', '-c', 'copy', f'{wd}/base.mp4'], check=True)

yy_ = np.linspace(0, 1, RH)[:, None, None]; GRAD = hx('#B8A3C9') * (1 - yy_) + hx('#E8B8C2') * yy_
import cv2
RS = np.random.RandomState(11); GRAIN = [RS.normal(0, 7, (RH // 2, RW // 2, 1)).astype(np.float32) for _ in range(6)]
def look(a):
    x = a / 255.0; s = .6
    x = np.clip((x - 0.5) * (1 + 0.28 * s) + 0.5, 0, 1); x = x ** (1 + 0.14 * s)
    m = x.mean(2, keepdims=True); x = np.clip(m + (x - m) * (1 + 0.55 * s), 0, 1)
    L = x.mean(2, keepdims=True); warm = np.array([1 + .06 * s, 1.0, 1 - .10 * s]); cool = np.array([1 - .03 * s, 1 - .01 * s, 1 + .05 * s])
    x = np.clip(x * (L * warm + (1 - L) * cool), 0, 1) * 255
    # y2k: sat, contrast, bloom (quarter res), soft, warm
    m = x.mean(2, keepdims=True); x = m + (x - m) * 1.3; x = (x - 128) * 1.08 + 128; x = x * np.array([1.03, 1, 0.97]); x = np.clip(x, 0, 255)
    sm = cv2.resize(x, (RW // 4, RH // 4), interpolation=cv2.INTER_AREA); bl = cv2.GaussianBlur(np.clip(sm - 150, 0, 255), (0, 0), 6); bl = cv2.resize(bl, (RW, RH))
    x = 255 - (255 - x) * (255 - bl * .45) / 255; x = cv2.GaussianBlur(x, (0, 0), 1.0)
    g = cv2.resize(GRAIN[look.i % 6], (RW, RH), interpolation=cv2.INTER_LINEAR); look.i += 1
    return np.clip(x + g[..., None] if g.ndim == 2 else x + g, 0, 255) * .8 + GRAD * .2
look.i = 0

CY = 1150
if STYLE == '12':   # pull-quotes only, Rozha 96 ivory, soft halo
    f = F('display', 96); LH = 108; COL = np.array(IVORY, np.float32)
    PHR = [(["the greys,", "the oranges,", "the blacks."], 0), (["the worst of", "masculine energy."], 0)]
    # time each phrase from its first word; find by matching word sequences
    def find(seq):
        toks = [re.sub(r'[^a-z]', '', w.lower()) for w in words]; s_ = [re.sub(r'[^a-z]', '', w.lower()) for w in ' '.join(seq).split()]
        for i in range(len(toks) - len(s_) + 1):
            if toks[i:i + len(s_)] == s_: return i, i + len(s_) - 1
        raise ValueError(seq)
    spans = []
    for lines, _ in PHR:
        a, b = find(lines); spans.append((times[a][0] - 0.05, times[b][1] + 1.4, lines))
    for k in range(len(spans) - 1): spans[k] = (spans[k][0], min(spans[k][1], spans[k + 1][0] - 0.1), spans[k][2])
    spans[-1] = (spans[-1][0], D - 0.3, spans[-1][2])
    layers = []
    for s, e, lines in spans:
        lay = Image.new('L', (RW, RH), 0); ld = ImageDraw.Draw(lay); y0 = CY - LH * len(lines) / 2
        for i, l in enumerate(lines): ld.text((RW / 2, y0 + i * LH), l, font=f, fill=255, anchor='ma')
        A = np.asarray(lay).astype(np.float32) / 255; H = np.asarray(lay.filter(ImageFilter.GaussianBlur(26))).astype(np.float32) / 255 * .6
        layers.append((s, e, A[..., None], H[..., None]))
    def caption(fr, t):
        for s, e, A, H in layers:
            if t < s or t > e + 0.3: continue
            g = min(1, (t - s) / 0.18) * (1.0 if t <= e else max(0, 1 - (t - e) / 0.3))
            fr = fr * (1 - H * g * .8); fr = fr * (1 - A * g) + COL * A * g
        return fr
else:               # 17: running captions in Rozha 80, aubergine with a pink glow, words arriving as spoken
    f = F('display', 80); LH = 92; MAXW = 920; PAL = {'17': ((58, 28, 52), '#F2D3DD'), '36': ((184, 196, 140), '#1E2A14'), '25': ((58, 28, 52), '#C9D2F0'), '23': (IVORY, '#8F9FD9')}
    COL = np.array(PAL[STYLE][0], np.float32); GLOW = hx(PAL[STYLE][1])
    def ends(w): return bool(re.search(r'[.!?]$', w))
    chunks = []; cur = []
    for i, w in enumerate(words):
        cur.append(i)
        if ends(w) or len(cur) >= 7: chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    dd = ImageDraw.Draw(Image.new('L', (1, 1))); sp = dd.textlength(' ', font=f)
    layers = []
    for ch in chunks:
        lines = [[]]; cw = 0
        for i in ch:
            tw = dd.textlength(words[i], font=f)
            if lines[-1] and cw + sp + tw > MAXW: lines.append([]); cw = 0
            lines[-1].append((i, tw)); cw += (sp if len(lines[-1]) > 1 else 0) + tw
        y0 = CY - LH * len(lines) / 2; lay = Image.new('L', (RW, RH), 0); ld = ImageDraw.Draw(lay); boxes = {}
        for li, ln in enumerate(lines):
            total = sum(tw for _, tw in ln) + sp * (len(ln) - 1); x = (RW - total) / 2; y = y0 + li * LH
            for i, tw in ln: ld.text((x, y), words[i], font=f, fill=255); boxes[i] = (int(x) - 4, int(y) - 4, int(x + tw) + 6, int(y + LH)); x += tw + sp
        A = np.asarray(lay).astype(np.float32) / 255; layers.append((A, boxes))
    spans = []
    for k, ch in enumerate(chunks):
        s = times[ch[0]][0] - 0.05; nxt = times[chunks[k + 1][0]][0] if k + 1 < len(chunks) else D
        e = min(nxt - 0.06, times[ch[-1]][1] + 1.2) if k + 1 < len(chunks) else D - 0.3; spans.append((s, e))
    def caption(fr, t):
        for k, (s, e) in enumerate(spans):
            if t < s or t > e + 0.3: continue
            A, boxes = layers[k]; ch = chunks[k]; g = 1.0 if t <= e else max(0, 1 - (t - e) / 0.3)
            vis = np.zeros(A.shape, np.float32)
            for i in ch:
                if t < times[i][0]: break
                a_ = min(1, (t - times[i][0]) / 0.14); x0, y0, x1, y1 = boxes[i]; vis[y0:y1, x0:x1] = A[y0:y1, x0:x1] * a_ * g
            if not vis.any(): continue
            glow = np.clip(np.asarray(Image.fromarray((vis * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(16))).astype(np.float32) / 255 * 2.2, 0, 1) * .85
            fr = fr * (1 - glow[..., None]) + GLOW * glow[..., None]; fr = fr * (1 - vis[..., None]) + COL * vis[..., None]
        return fr

furn = Image.new('RGBA', (RW, RH), (0, 0, 0, 0)); fd = ImageDraw.Draw(furn)
spaced(fd, (72, 110), LABEL.lower(), F('mono', 17), IVORY + (255,), .18)
fa = np.asarray(furn).astype(np.float32); FA = fa[..., 3:4] / 255; FRGB = fa[..., :3]
N = int(D * FPS); FS = RW * RH * 3
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', f'{wd}/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-i', f'vo/{name}_cut.m4a', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for fi in range(N):
    raw = dec.stdout.read(FS)
    if len(raw) < FS: break
    fr = look(np.frombuffer(raw, np.uint8).reshape(RH, RW, 3).astype(np.float32)); t = fi / FPS
    fr = caption(fr, t); fr = fr * (1 - FA) + FRGB * FA
    if t < 0.5: fr *= t / 0.5
    if t > D - 0.8: fr *= max(0, (D - t) / 0.8)
    enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    if fi % 150 == 0: print('frame', fi, '/', N, flush=True)
enc.stdin.close(); dec.stdout.close(); enc.wait(); print('done', OUT)
