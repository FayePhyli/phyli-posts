"""fast reel builder: grade in ffmpeg at cut time, captions in python.
usage: python3 sys/reel2.py <name> <label> <out.mp4>   (needs vo/<name>_cut.m4a + vo/<name>_timeline.json + sys/shots_<name>.json)"""
import sys, os, re, json, subprocess
sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import F, IVORY, spaced
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import pillow_heif; pillow_heif.register_heif_opener()
name, LABEL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
RW, RH, FPS = 1080, 1920, 30
SRC = "/mnt/user-data/uploads/Desktop/Phyli/Phyli Content CLAUDE/06 Studio & Life B-roll/"
meta = json.load(open('broll/meta.json'))
T = json.load(open(f'vo/{name}_timeline.json')); words = [w['w'] for w in T['words']]; times = [(w['s'], w['e']) for w in T['words']]; D = T['D']
SHOTS = json.load(open(f'sys/shots_{name}.json'))          # [[key, in, dur, fx, fy], ...]
tot = sum(s[2] for s in SHOTS); sc = D / tot
GRADE = "eq=contrast=1.22:saturation=1.45:gamma=0.9,colorbalance=rh=0.06:bh=-0.10:rs=-0.03:bs=0.05:rm=0.02:bm=-0.03,vignette=PI/5.5,noise=alls=6:allf=t+u"
wd = f'sys/r_{name}'; os.makedirs(wd, exist_ok=True); segs = []
for i, (k, ip, d, fx, fy) in enumerate(SHOTS):
    d *= sc; m = meta[k]; src = SRC + m['f']; out = f'{wd}/{i:02d}.mp4'; segs.append(out)
    if os.path.exists(out): continue
    if m['t'] == 'v':
        if ip + d > m['d'] - 0.1: ip = max(0, m['d'] - d - 0.1)
        loop = ['-stream_loop', '-1'] if m['d'] < d + 0.2 else []
        vf = f"scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}:'(iw-{RW})*{fx}':'(ih-{RH})*{fy}',fps={FPS},setsar=1,{GRADE}"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + loop + ['-ss', f'{ip:.2f}', '-i', src, '-t', f'{d:.3f}', '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], check=True)
    else:
        tmp = f'{wd}/{i:02d}_still.jpg'; Image.open(src).convert('RGB').save(tmp, quality=95); N = int(d * FPS) + 1
        vf = f"scale={2*RW}:{2*RH}:force_original_aspect_ratio=increase,crop={2*RW}:{2*RH},zoompan=z='1+0.08*on/{N}':d={N}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={RW}x{RH}:fps={FPS},setsar=1,{GRADE}"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', tmp, '-t', f'{d:.3f}', '-vf', vf, '-frames:v', str(int(round(d * FPS))), '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], check=True)
    print('seg', i, k, round(d, 1), flush=True)
open(f'{wd}/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{wd}/list.txt', '-c', 'copy', f'{wd}/base.mp4'], check=True)

def ends(w): return bool(re.search(r'[.!?]$', w))
chunks = []; cur = []
for i, w in enumerate(words):
    cur.append(i)
    if ends(w) or len(cur) >= 10: chunks.append(cur); cur = []
if cur: chunks.append(cur)
f = F('sansm', 50); LH = 66; MAXW = 930; CY = 1480
dd = ImageDraw.Draw(Image.new('L', (1, 1))); sp = dd.textlength(' ', font=f)
layers = []
for ch in chunks:
    lines = [[]]; cw = 0
    for i in ch:
        tw = dd.textlength(words[i], font=f)
        if lines[-1] and cw + sp + tw > MAXW: lines.append([]); cw = 0
        lines[-1].append((i, tw)); cw += (sp if len(lines[-1]) > 1 else 0) + tw
    hgt = len(lines) * LH; ytop = CY - hgt / 2; boxes = {}; lay = Image.new('L', (RW, RH), 0); ld = ImageDraw.Draw(lay)
    for li, ln in enumerate(lines):
        x = 72; y = ytop + li * LH
        for i, tw in ln: ld.text((x, y), words[i], font=f, fill=255); boxes[i] = (int(x) - 3, int(y) - 2, int(x + tw) + 4, int(y + LH) - 2); x += tw + sp
    halo = np.asarray(lay.filter(ImageFilter.GaussianBlur(20))).astype(np.float32) / 255 * 0.85
    y0 = max(0, int(ytop) - 50); y1 = min(RH, int(ytop + hgt) + 50)
    layers.append((np.asarray(lay).astype(np.float32)[y0:y1] / 255, halo[y0:y1], {i: (a, b - y0, c, d - y0) for i, (a, b, c, d) in boxes.items()}, y0, y1))
spans = []
for k, ch in enumerate(chunks):
    s = times[ch[0]][0] - 0.05; nxt = times[chunks[k + 1][0]][0] if k + 1 < len(chunks) else D
    e = min(nxt - 0.06, times[ch[-1]][1] + 1.2) if k + 1 < len(chunks) else D - 0.4; spans.append((s, e))
FADE_W, FADE_OUT, RECEDE, REST = 0.12, 0.3, 0.5, 0.45
furn = Image.new('RGBA', (RW, RH), (0, 0, 0, 0)); fd = ImageDraw.Draw(furn)
spaced(fd, (72, 110), LABEL.lower(), F('mono', 17), IVORY + (255,), .18); fd.text((RW - 72, 94), 'fp', font=F('italic', 44), fill=IVORY + (255,), anchor='ra')
fa = np.asarray(furn).astype(np.float32); FA = fa[..., 3:4] / 255; FRGB = fa[..., :3]
grad = (1 - np.linspace(0, .42, RH))[:, None, None].astype(np.float32)
N = int(D * FPS); ink = np.array(IVORY, np.float32); FS = RW * RH * 3
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', f'{wd}/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-i', f'vo/{name}_cut.m4a', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for fi in range(N):
    raw = dec.stdout.read(FS)
    if len(raw) < FS: break
    fr = np.frombuffer(raw, np.uint8).reshape(RH, RW, 3).astype(np.float32) * grad
    t = fi / FPS
    for k, (s, e) in enumerate(spans):
        if t < s or t > e + FADE_OUT: continue
        lay, halo, boxes, y0, y1 = layers[k]; ch = chunks[k]; gg = 1.0 if t <= e else max(0.0, 1 - (t - e) / FADE_OUT)
        vis = np.zeros(lay.shape, np.float32); any_ = False
        for j, i in enumerate(ch):
            ws_ = times[i][0]
            if t < ws_: break
            a_ = min(1.0, (t - ws_) / FADE_W)
            if j + 1 < len(ch) and t > times[ch[j + 1]][0]: a_ = max(REST, 1 - (1 - REST) * (t - times[ch[j + 1]][0]) / RECEDE)
            bx0, by0, bx1, by1 = boxes[i]; vis[by0:by1, bx0:bx1] = np.maximum(vis[by0:by1, bx0:bx1], lay[by0:by1, bx0:bx1] * a_ * gg); any_ = True
        if not any_: continue
        band = fr[y0:y1]; band = band * (1 - halo[..., None] * gg * 0.7); fr[y0:y1] = band * (1 - vis[..., None]) + ink * vis[..., None]
    fr = fr * (1 - FA) + FRGB * FA
    p = int(72 + 936 * min(t / D, 1)); fr[1846:1848, 72:p] = ink; fr[1846:1847, p:1008] = fr[1846:1847, p:1008] * .5 + 128
    if t < 0.8: fr *= t / 0.8
    if t > D - 1.2: fr *= max(0, (D - t) / 1.2)
    enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    if fi % 900 == 0: print('frame', fi, '/', N, flush=True)
enc.stdin.close(); dec.stdout.close(); enc.wait(); print('done', OUT, round(D, 1))
