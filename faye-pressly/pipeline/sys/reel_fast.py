"""the locked reel look, fast: y2k + lilac→pink gradient graded in ffmpeg at cut time; Rozha 80 ivory captions with a periwinkle glow, just below centre, words arriving as spoken.
usage: python3 sys/reel_fast.py <name> <label> <out.mp4> [glow_hex]   needs vo/<name>_cut.m4a, vo/<name>_timeline.json, sys/shots_<name>.json, broll/meta2.json"""
import sys, os, re, json, subprocess
sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import F, IVORY, spaced
from lib import hx
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
name, LABEL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; GLOW = hx(sys.argv[4] if len(sys.argv) > 4 else '#8F9FD9')
RW, RH, FPS = 1080, 1920, 30
meta = json.load(open('broll/meta2.json'))
T = json.load(open(f'vo/{name}_timeline.json')); words = [w['w'] for w in T['words']]; times = [(w['s'], w['e']) for w in T['words']]; D = T['D']
SHOTS = json.load(open(f'sys/shots_{name}.json')); tot = sum(s[2] for s in SHOTS); sc = D / tot
LOOK = "eq=contrast=1.17:saturation=1.5:gamma=0.93,colorbalance=rh=0.06:bh=-0.09:rs=-0.02:bs=0.04,split[a][b];[b]curves=all='0/0 0.55/0 1/1',gblur=sigma=22[g];[a][g]blend=all_mode=screen:all_opacity=0.5,gblur=sigma=0.8,noise=alls=7:allf=t+u[v];[v][1:v]overlay=format=auto"
wd = f'sys/r_{name}_fast'; os.makedirs(wd, exist_ok=True); segs = []
for i, (k, ip, d, fx, fy) in enumerate(SHOTS):
    d *= sc; m = meta[k]; src = m['p']; out = f'{wd}/{i:02d}.mp4'; segs.append(out)
    if os.path.exists(out): continue
    if ip + d > m['d'] - 0.1: ip = max(0, m['d'] - d - 0.1)
    pre = f"scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}:'(iw-{RW})*{fx}':'(ih-{RH})*{fy}',fps={FPS},setsar=1,"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{ip:.2f}', '-i', src, '-i', 'sys/grad.png', '-t', f'{d:.3f}', '-filter_complex', '[0:v]' + pre + LOOK, '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], check=True)
    print('seg', i, k, round(d, 1), flush=True)
open(f'{wd}/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{wd}/list.txt', '-c', 'copy', f'{wd}/base.mp4'], check=True)

CY = 1150; f = F('display', 80); LH = 92; MAXW = 920; COL = np.array(IVORY, np.float32)
def ends(w): return bool(re.search(r'[.!?]$', w))
chunks = []; cur = []
for i, w in enumerate(words):
    cur.append(i)
    if ends(w) or len(cur) >= 7: chunks.append(cur); cur = []
if cur: chunks.append(cur)
disp = [re.sub(r'\.+$', '', w) for w in words]   # no full stops on screen (her rule); commas stay
dd = ImageDraw.Draw(Image.new('L', (1, 1))); sp = dd.textlength(' ', font=f)
layers = []
for ch in chunks:
    lines = [[]]; cw = 0
    for i in ch:
        tw = dd.textlength(disp[i], font=f)
        if lines[-1] and cw + sp + tw > MAXW: lines.append([]); cw = 0
        lines[-1].append((i, tw)); cw += (sp if len(lines[-1]) > 1 else 0) + tw
    y0 = CY - LH * len(lines) / 2; lay = Image.new('L', (RW, RH), 0); ld = ImageDraw.Draw(lay); boxes = {}
    for li, ln in enumerate(lines):
        total = sum(tw for _, tw in ln) + sp * (len(ln) - 1); x = (RW - total) / 2; y = y0 + li * LH
        for i, tw in ln: ld.text((x, y), disp[i], font=f, fill=255); boxes[i] = (int(x) - 4, int(y) - 4, int(x + tw) + 6, int(y + LH)); x += tw + sp
    ya, yb = max(0, int(y0) - 60), min(RH, int(y0 + LH * len(lines)) + 60)
    A = np.asarray(lay).astype(np.float32)[ya:yb] / 255; layers.append((A, {i: (a, b - ya, c, d - ya) for i, (a, b, c, d) in boxes.items()}, ya, yb))
spans = []
for k, ch in enumerate(chunks):
    s = times[ch[0]][0] - 0.05; nxt = times[chunks[k + 1][0]][0] if k + 1 < len(chunks) else D
    e = min(nxt - 0.06, times[ch[-1]][1] + 1.2) if k + 1 < len(chunks) else D - 0.3; spans.append((s, e))
furn = Image.new('RGBA', (RW, RH), (0, 0, 0, 0)); fd = ImageDraw.Draw(furn); spaced(fd, (72, 110), LABEL.lower(), F('mono', 17), IVORY + (255,), .18)
fa = np.asarray(furn).astype(np.float32); FA = fa[..., 3:4] / 255; FRGB = fa[..., :3]
N = int(D * FPS); FS = RW * RH * 3
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', f'{wd}/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-i', f'vo/{name}_cut.m4a', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for fi in range(N):
    raw = dec.stdout.read(FS)
    if len(raw) < FS: break
    fr = np.frombuffer(raw, np.uint8).reshape(RH, RW, 3).astype(np.float32); t = fi / FPS
    for k, (s, e) in enumerate(spans):
        if t < s or t > e + 0.3: continue
        A, boxes, ya, yb = layers[k]; ch = chunks[k]; g = 1.0 if t <= e else max(0, 1 - (t - e) / 0.3)
        vis = np.zeros(A.shape, np.float32)
        for i in ch:
            if t < times[i][0]: break
            a_ = min(1, (t - times[i][0]) / 0.14); x0, y0, x1, y1 = boxes[i]; vis[y0:y1, x0:x1] = A[y0:y1, x0:x1] * a_ * g
        if not vis.any(): continue
        glow = np.clip(np.asarray(Image.fromarray((vis * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(16))).astype(np.float32) / 255 * 2.2, 0, 1) * .85
        band = fr[ya:yb]; band = band * (1 - glow[..., None]) + GLOW * glow[..., None]; fr[ya:yb] = band * (1 - vis[..., None]) + COL * vis[..., None]
    fr = fr * (1 - FA) + FRGB * FA
    if t < 0.5: fr *= t / 0.5
    if t > D - 0.8: fr *= max(0, (D - t) / 0.8)
    enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    if fi % 300 == 0: print('frame', fi, '/', N, flush=True)
enc.stdin.close(); dec.stdout.close(); enc.wait(); print('done', OUT)
