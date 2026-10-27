"""the samhain reel: firelight grade (aubergine and silver, only the flame in colour), a drifting veil of smoke, cream Rozha with an ember glow, a black opening card, one full-colour shot at the end.
usage: python3 sys/reel_veil.py samhain2 "the night  ·  samhain" sam/Reel_samhain.mp4"""
import sys, os, re, json, subprocess
sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import F, spaced
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
name, LABEL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
RW, RH, FPS = 1080, 1920, 30; LEAD = 2.4
CREAM = np.array([244, 236, 214], np.float32); EMBER = np.array([190, 96, 60], np.float32)
meta = json.load(open('broll/meta2.json'))
for p in os.listdir('sam/vid'):
    if p.endswith('.mp4'):
        k = 'S_' + p[:-4]; d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'sam/vid/{p}'], capture_output=True, text=True).stdout or 0)
        meta[k] = {'p': f'sam/vid/{p}', 'd': d}
T = json.load(open(f'vo/{name}_timeline.json')); words = [w['w'] for w in T['words']]; times = [(w['s'] + LEAD, w['e'] + LEAD) for w in T['words']]; D = T['D'] + LEAD
# (key, in, dur, fx, fy[, colour])
SHOTS = [('S_39A7BF25', 0.5, 2.5, .5, .4), ('S_IMG_1878', 0.3, 3.0, .5, .5), ('S_094C3052', 2.0, 2.5, .5, .3), ('S_4E0D5044', 4.0, 2.5, .5, .4), ('S_6A432BDD', 1.0, 2.5, .5, .4),
         ('N043', 2.0, 3.0, .6, .6), ('S_IMG_1783', 1.0, 3.0, .5, .5), ('N021', 0.0, 2.8, .5, .5), ('N016', 1.0, 2.5, .5, .5), ('N044', 3.0, 2.5, .6, .6),
         ('N022', 2.0, 3.0, .5, .5), ('N041', 1.0, 2.5, .5, .5), ('N004', 2.0, 3.0, .5, .5), ('N026', 1.0, 2.5, .5, .5), ('S_75461B2D', 3.0, 2.5, .5, .4),
         ('N045', 0.0, 2.0, .6, .6), ('S_15B7DEAF', 2.0, 2.5, .5, .4), ('S_D0812069', 5.0, 3.0, .5, .4), ('N027', 1.0, 2.5, .5, .5), ('S_CF43661C', 1.0, 2.5, .5, .5),
         ('S_BB0C1EE1', 0.3, 2.5, .5, .4), ('S_7A6CAA6C', 0.0, 1.8, .5, .4), ('S_IMG_1733', 1.0, 2.5, .5, .5), ('S_E02BAA6D', 1.0, 3.0, .5, .4), ('S_4A96AA39', 1.0, 2.5, .5, .4),
         ('S_6EDF4B63', 3.0, 3.0, .5, .4), ('N106', 20.0, 3.0, .5, .3), ('N017', 0.5, 2.5, .5, .5), ('S_IMG_1734', 0.5, 2.0, .5, .5), ('N008', 2.0, 2.5, .5, .5),
         ('00', 0.0, 2.5, .5, .4), ('N030', 4.0, 3.0, .5, .5), ('S_4E0D5044', 20.0, 2.5, .5, .4), ('N026', 7.0, 3.0, .5, .5),
         ('N022', 12.0, 3.0, .5, .5), ('S_D0812069', 22.0, 3.0, .5, .4), ('S_6EDF4B63', 16.0, 2.5, .5, .4), ('S_15B7DEAF', 12.0, 2.5, .5, .4), ('N043', 12.0, 3.0, .6, .6),
         ('S_IMG_1878', 1.8, 2.5, .5, .5), ('N004', 8.0, 2.5, .5, .5), ('N041', 7.0, 2.5, .5, .5), ('N016', 5.0, 2.5, .5, .5), ('S_75461B2D', 9.0, 2.5, .5, .4),
         ('N027', 2.5, 2.5, .5, .5), ('N008', 7.0, 2.5, .5, .5), ('N104', 30.0, 3.0, .5, .4, 1), ('N106', 40.0, 3.0, .5, .3, 1)]
tot = sum(s[2] for s in SHOTS); sc = T['D'] / tot
# ---- smoke: a 12s drifting veil, looped ----
wd = f'sys/r_{name}_veil'; os.makedirs(wd, exist_ok=True)
if not os.path.exists(f'{wd}/smoke.mp4'):
    rs = np.random.RandomState(3); layers = [rs.rand(RH // sc_ + 4, RW // sc_ + 4).astype(np.float32) for sc_ in (48, 96, 192)]
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', f'{RW}x{RH}', '-r', '15', '-i', '-', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', f'{wd}/smoke.mp4'], stdin=subprocess.PIPE)
    for fi in range(12 * 15):
        t = fi / (12 * 15) * 2 * np.pi; n = np.zeros((RH, RW), np.float32)
        for k, (L, sc_) in enumerate(zip(layers, (48, 96, 192))):
            dx = int((np.sin(t + k) * 1.5 + fi * 0.08 * (k + 1)) % L.shape[1]); dy = int((np.cos(t * .7 + k) * 1.0 + fi * 0.03) % L.shape[0])
            Lr = np.roll(np.roll(L, dy, 0), dx, 1); n += cv2.resize(Lr, (RW, RH), interpolation=cv2.INTER_CUBIC) / (k + 1)
        n = cv2.GaussianBlur(n, (0, 0), 20); n = (n - n.min()) / (n.max() - n.min() + 1e-6); n = (n ** 2.4) * 255 * .55
        enc.stdin.write(np.clip(n, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); print('smoke', flush=True)
# ---- grades ----
FIRE = ("split[a][b];[a]hue=s=0,colorlevels=rimin=0.02:gimin=0.02:bimin=0.02:rimax=0.95:gimax=0.95:bimax=0.95,colorbalance=rs=0.10:gs=-0.04:bs=0.14:rm=0.04:gm=-0.02:bm=0.06:rh=0.02:bh=0.03,eq=contrast=1.08:gamma=0.95[m];"
        "[b]colorhold=color=#ff7a28:similarity=0.42:blend=0.25,eq=saturation=1.35[w];[m][w]blend=all_mode=lighten:all_opacity=0.9,"
        "vignette=angle=PI/3.6,noise=alls=9:allf=t+u[v];[v][1:v]blend=all_mode=screen:all_opacity=0.5,format=yuv420p")
Y2K = "eq=contrast=1.17:saturation=1.5:gamma=0.93,colorbalance=rh=0.06:bh=-0.09:rs=-0.02:bs=0.04,split[a][b];[b]curves=all='0/0 0.55/0 1/1',gblur=sigma=22[g];[a][g]blend=all_mode=screen:all_opacity=0.5,gblur=sigma=0.8,noise=alls=7:allf=t+u[v];[v][2:v]overlay=format=auto"
segs = [f'{wd}/black.mp4']
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', f'color=c=black:s={RW}x{RH}:r={FPS}', '-t', f'{LEAD:.2f}', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', segs[0]], check=True)
for i, s in enumerate(SHOTS):
    k, ip, d, fx, fy = s[:5]; colour = len(s) > 5; d *= sc; m = meta[k]; src = m['p']; out = f'{wd}/{i:02d}.mp4'; segs.append(out)
    if os.path.exists(out): continue
    segs.pop(); break
    if ip + d > m['d'] - 0.1: ip = max(0, m['d'] - d - 0.1)
    pre = f"[0:v]scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}:'(iw-{RW})*{fx}':'(ih-{RH})*{fy}',fps={FPS},setsar=1,"
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{ip:.2f}', '-i', src, '-stream_loop', '-1', '-i', f'{wd}/smoke.mp4', '-i', 'sys/grad.png', '-t', f'{d:.3f}', '-filter_complex', pre + (Y2K if colour else FIRE), '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out]
    subprocess.run(cmd, check=True); print('seg', i, k, round(d, 1), flush=True)
open(f'{wd}/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
segs = segs[:17]; open(f'{wd}/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{wd}/list.txt', '-c', 'copy', f'{wd}/base_prev.mp4'], check=True)
# ---- captions ----
CY = 1150; f = F('display', 80); LH = 92; MAXW = 920
def ends(w): return bool(re.search(r'[.!?]$', w))
chunks = []; cur = []
for i, w in enumerate(words):
    cur.append(i)
    if ends(w) or len(cur) >= 7: chunks.append(cur); cur = []
if cur: chunks.append(cur)
disp = [re.sub(r'\.+$', '', w) for w in words]
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
# the opening card and the closing card
card = Image.new('L', (RW, RH), 0); ImageDraw.Draw(card).text((RW / 2, 960), 'a year ago, almost', font=F('display', 76), fill=255, anchor='mm'); CARD = np.asarray(card).astype(np.float32)[..., None] / 255
card2 = Image.new('L', (RW, RH), 0); cd = ImageDraw.Draw(card2); cd.text((RW / 2, 1100), 'volume I  ·  vision', font=F('display', 60), fill=255, anchor='mm'); cd.text((RW / 2, 1180), 'begins next week', font=F('italic', 40), fill=255, anchor='mm'); CARD2 = np.asarray(card2).astype(np.float32)[..., None] / 255
furn = Image.new('RGBA', (RW, RH), (0, 0, 0, 0)); spaced(ImageDraw.Draw(furn), (72, 110), LABEL.lower(), F('mono', 17), tuple(int(v) for v in CREAM) + (255,), .18)
fa = np.asarray(furn).astype(np.float32); FA = fa[..., 3:4] / 255; FRGB = fa[..., :3]
D = LEAD + sum(SHOTS[i][2] for i in range(16)) * sc; N = int(D * FPS); FS = RW * RH * 3
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', f'{wd}/base_prev.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-i', f'vo/{name}_cut.m4a', '-filter_complex', f'[1:a]adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for fi in range(N):
    raw = dec.stdout.read(FS)
    if len(raw) < FS: break
    fr = np.frombuffer(raw, np.uint8).reshape(RH, RW, 3).astype(np.float32); t = fi / FPS
    if t < LEAD + 0.6:
        g = min(1, t / 0.8) * (1 if t < LEAD else max(0, 1 - (t - LEAD) / 0.6)); fr = fr * (1 - CARD * g) + CREAM * CARD * g
    for k, (s, e) in enumerate(spans):
        if t < s or t > e + 0.3: continue
        A, boxes, ya, yb = layers[k]; ch = chunks[k]; g = 1.0 if t <= e else max(0, 1 - (t - e) / 0.3)
        vis = np.zeros(A.shape, np.float32)
        for i in ch:
            if t < times[i][0]: break
            a_ = min(1, (t - times[i][0]) / 0.14); x0, y0, x1, y1 = boxes[i]; vis[y0:y1, x0:x1] = A[y0:y1, x0:x1] * a_ * g
        if not vis.any(): continue
        glow = np.clip(np.asarray(Image.fromarray((vis * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))).astype(np.float32) / 255 * 2.0, 0, 1) * .6
        band = fr[ya:yb]; band = band * (1 - glow[..., None]) + EMBER * glow[..., None]; fr[ya:yb] = band * (1 - vis[..., None]) + CREAM * vis[..., None]
    if False:
        g = min(1, (t - (D - 3.2)) / 0.6); fr = fr * (1 - CARD2 * g) + CREAM * CARD2 * g
    if t >= LEAD: fr = fr * (1 - FA) + FRGB * FA
    enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    if fi % 300 == 0: print('frame', fi, '/', N, flush=True)
enc.stdin.close(); dec.stdout.close(); enc.wait(); print('done', OUT)
