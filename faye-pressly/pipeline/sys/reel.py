"""trial reel · post 01 'the reintroduction' · her B-roll, the grade, words as spoken (timed to a placeholder pace until she records)"""
import sys, os, re, json, subprocess, math
sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import grade, F, pil, IVORY, spaced
import numpy as np, cv2, json
from PIL import Image, ImageDraw, ImageFilter
RW, RH, FPS = 1080, 1920, 30
SRC = "/mnt/user-data/uploads/Desktop/Phyli/Phyli Content CLAUDE/06 Studio & Life B-roll/"
meta = json.load(open('broll/meta.json'))
os.makedirs('sys/reel', exist_ok=True)
T = json.load(open('vo/reintro_timeline.json')); words = [w['w'] for w in T['words']]; times = [(w['s'], w['e']) for w in T['words']]; D = T['D']
# shots: (key, in-point, duration, focus)  — her clips, cut on sentence turns
SHOTS = [('14', 1.0, 5.5, (.5, .4)), ('26', 4.0, 5.5, (.5, .5)), ('48', 0, 5.0, (.5, .5)), ('31', 6.0, 6.0, (.5, .4)),
         ('42', 6.0, 5.5, (.5, .5)), ('15', 0, 5.0, (.5, .5)), ('68', 3.0, 6.0, (.5, .4)), ('60', 1.0, 5.5, (.5, .5)),
         ('46', 2.0, 6.0, (.5, .4)), ('34', 4.0, 6.0, (.5, .5)), ('45', 1.0, 5.5, (.5, .3)), ('24', 0, 5.0, (.5, .5)),
         ('41', 3.0, 6.0, (.5, .4)), ('16', 1.0, 5.5, (.5, .5)), ('66', 0.5, 5.0, (.5, .3)), ('26', 14.0, 6.0, (.5, .5)),
         ('31', 15.0, 6.0, (.5, .4)), ('59', 0.5, 5.5, (.5, .5)), ('47', 3.0, 6.5, (.5, .4)), ('38', 0, 5.0, (.5, .5)),
         ('30', 1.0, 6.0, (.5, .35)), ('68', 12.0, 6.0, (.5, .4)), ('40', 0.5, 6.0, (.5, .4)), ('18', 10.0, 6.0, (.5, .4)),
         ('10', 6.0, 8.0, (.5, .4))]
tot = sum(s[2] for s in SHOTS); scale = D / tot; SHOTS = [(k, ip, d * scale, f) for k, ip, d, f in SHOTS]
segs = []
for i, (k, ip, d, f) in enumerate(SHOTS):
    m = meta[k]; src = SRC + m['f']; out = f'sys/reel/{i:02d}.mp4'; segs.append(out)
    if os.path.exists(out): continue
    if m['t'] == 'v':
        vf = f"scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}:'(iw-{RW})*{f[0]}':'(ih-{RH})*{f[1]}',fps={FPS},setsar=1"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{ip:.2f}', '-i', src, '-t', f'{d:.3f}', '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], check=True)
    else:
        # HEIC still → jpg → slow push
        tmp = f'sys/reel/{i:02d}_still.jpg'
        from PIL import Image as _I; import pillow_heif; pillow_heif.register_heif_opener(); _I.open(src).convert('RGB').save(tmp, quality=95)
        N = int(d * FPS) + 1
        vf = f"scale={2*RW}:{2*RH}:force_original_aspect_ratio=increase,crop={2*RW}:{2*RH},zoompan=z='1+0.08*on/{N}':d={N}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={RW}x{RH}:fps={FPS},setsar=1"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', tmp, '-t', f'{d:.3f}', '-vf', vf, '-frames:v', str(int(round(d * FPS))), '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], check=True)
    print('seg', i, k, round(d, 1), flush=True)
open('sys/reel/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'sys/reel/list.txt', '-c', 'copy', 'sys/reel/base.mp4'], check=True)

# ---- captions: sentence chunks, word focus ----
def ends(w): return bool(re.search(r'[.!?]$', w))
chunks = []; cur = []
for i, w in enumerate(words):
    cur.append(i)
    if ends(w) or len(cur) >= 11:
        if ends(w) or (i + 1 < len(words) and not ends(words[i + 1]) and len(cur) >= 11): chunks.append(cur); cur = []
if cur: chunks.append(cur)
f = F('sansm', 52); LH = 68; MAXW = 930; CY = 1500
dd = ImageDraw.Draw(Image.new('L', (1, 1))); sp = dd.textlength(' ', font=f)
layers = []
for ch in chunks:
    lines = [[]]; cw = 0
    for i in ch:
        w = words[i]; tw = dd.textlength(w, font=f)
        if lines[-1] and cw + sp + tw > MAXW: lines.append([]); cw = 0
        lines[-1].append((i, tw)); cw += (sp if len(lines[-1]) > 1 else 0) + tw
    hgt = len(lines) * LH; ytop = CY - hgt / 2
    boxes = {}; lay = Image.new('L', (RW, RH), 0); ld = ImageDraw.Draw(lay)
    for li, ln in enumerate(lines):
        x = 72; y = ytop + li * LH
        for i, tw in ln:
            ld.text((x, y), words[i], font=f, fill=255); boxes[i] = (int(x) - 3, int(y) - 2, int(x + tw) + 4, int(y + LH) - 2); x += tw + sp
    halo = np.asarray(lay.filter(ImageFilter.GaussianBlur(20))).astype(np.float32) / 255 * 0.85
    y0 = max(0, int(ytop) - 50); y1 = min(RH, int(ytop + hgt) + 50)
    layers.append((np.asarray(lay).astype(np.float32)[y0:y1] / 255, halo[y0:y1], {i: (a, b - y0, c, d - y0) for i, (a, b, c, d) in boxes.items()}, y0, y1))
spans = []
for k, ch in enumerate(chunks):
    s = times[ch[0]][0] - 0.05; nxt = times[chunks[k + 1][0]][0] if k + 1 < len(chunks) else D
    e = min(nxt - 0.06, times[ch[-1]][1] + 1.2) if k + 1 < len(chunks) else D - 0.4; spans.append((s, e))
FADE_W, FADE_OUT, RECEDE, REST = 0.12, 0.3, 0.5, 0.45
# static furniture
furn = Image.new('RGBA', (RW, RH), (0, 0, 0, 0)); fd = ImageDraw.Draw(furn)
spaced(fd, (72, 110), 'no. 01  ·  the reintroduction  ·  palma', F('mono', 17), IVORY + (255,), .18)
fd.text((RW - 72, 94), 'fp', font=F('italic', 44), fill=IVORY + (255,), anchor='ra')
furn_a = np.asarray(furn).astype(np.float32); FA = furn_a[..., 3:4] / 255; FRGB = furn_a[..., :3]
N = int(D * FPS); ink = np.array(IVORY, np.float32)
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'sys/reel/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-i', 'vo/reintro_cut.m4a', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', 'sys/reel/Reel_01_reintroduction.mp4'], stdin=subprocess.PIPE)
FS = RW * RH * 3
for fi in range(N):
    raw = dec.stdout.read(FS)
    if len(raw) < FS: break
    fr = grade(np.frombuffer(raw, np.uint8).reshape(RH, RW, 3).astype(np.float32), 0.9)
    g = np.linspace(0, .42, RH)[:, None, None]; fr = fr * (1 - g)                       # darken toward the foot
    t = fi / FPS
    for k, (s, e) in enumerate(spans):
        if t < s or t > e + FADE_OUT: continue
        lay, halo, boxes, y0, y1 = layers[k]; ch = chunks[k]
        gg = 1.0 if t <= e else max(0.0, 1 - (t - e) / FADE_OUT)
        vis = np.zeros(lay.shape, np.float32); any_ = False
        for j, i in enumerate(ch):
            ws = times[i][0]
            if t < ws: break
            a_ = min(1.0, (t - ws) / FADE_W)
            if j + 1 < len(ch) and t > times[ch[j + 1]][0]: a_ = max(REST, 1 - (1 - REST) * (t - times[ch[j + 1]][0]) / RECEDE)
            bx0, by0, bx1, by1 = boxes[i]; vis[by0:by1, bx0:bx1] = np.maximum(vis[by0:by1, bx0:bx1], lay[by0:by1, bx0:bx1] * a_ * gg); any_ = True
        if not any_: continue
        band = fr[y0:y1]; band = band * (1 - halo[..., None] * gg * 0.7); band = band * (1 - vis[..., None]) + ink * vis[..., None]; fr[y0:y1] = band
    fr = fr * (1 - FA) + FRGB * FA
    p = int(72 + 936 * min(t / D, 1)); fr[1846:1848, 72:p] = ink; fr[1846:1847, p:1008] = fr[1846:1847, p:1008] * .5 + 128
    if t < 0.8: fr = fr * (t / 0.8)
    if t > D - 1.2: fr = fr * max(0, (D - t) / 1.2)
    enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    if fi % 300 == 0: print('frame', fi, '/', N, flush=True)
enc.stdin.close(); dec.stdout.close(); enc.wait(); print('done', round(D, 1))
