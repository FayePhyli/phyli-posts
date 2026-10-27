"""tiktok: 12s, the leather jacket only, locked look, two on-screen lines; silent (she adds a sound in-app)"""
import sys, os, json, subprocess; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import F, IVORY
from lib import hx
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
RW, RH, FPS = 1080, 1920, 30; meta = json.load(open('broll/meta2.json'))
LOOK = "eq=contrast=1.17:saturation=1.5:gamma=0.93,colorbalance=rh=0.06:bh=-0.09:rs=-0.02:bs=0.04,split[a][b];[b]curves=all='0/0 0.55/0 1/1',gblur=sigma=22[g];[a][g]blend=all_mode=screen:all_opacity=0.5,gblur=sigma=0.8,noise=alls=7:allf=t+u[v];[v][1:v]overlay=format=auto"
SHOTS = [('00', 0.0, 4.4, .5, .4, 1.0), ('00', 0.0, 4.4, .6, .25, 1.4)]
wd = 'sys/r_tt_skel2'; os.makedirs(wd, exist_ok=True); segs = []
for i, (k, ip, d, fx, fy, z) in enumerate(SHOTS):
    out = f'{wd}/{i:02d}.mp4'; segs.append(out); src = meta[k]['p']
    pre = f"scale={int(RW*z)}:{int(RH*z)}:force_original_aspect_ratio=increase,crop={RW}:{RH}:'(iw-{RW})*{fx}':'(ih-{RH})*{fy}',fps={FPS},setsar=1,"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{ip:.2f}', '-i', src, '-i', 'sys/grad.png', '-t', f'{d:.3f}', '-filter_complex', '[0:v]' + pre + LOOK, '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], check=True)
open(f'{wd}/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{wd}/list.txt', '-c', 'copy', f'{wd}/base.mp4'], check=True)
D = sum(s[2] for s in SHOTS); N = int(D * FPS); f = F('sansb', 62); LH = 78; COL = np.array((255, 255, 255), np.float32); GLOW = np.array((0, 0, 0), np.float32); CY = 1180
LINES = [(0.0, D, ["your company has a skeleton,", "a nervous system", "and a circulation.", "", "nobody told you.", "twelve volumes, I will."])]
layers = []
for s, e, lines in LINES:
    lay = Image.new('L', (RW, RH), 0); ld = ImageDraw.Draw(lay); y0 = CY - LH * len(lines) / 2
    for i, l in enumerate(lines): ld.text((RW / 2, y0 + i * LH), l, font=f, fill=255, anchor='ma')
    A = np.asarray(lay).astype(np.float32) / 255; G = np.clip(np.asarray(lay.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32) / 255 * 1.6, 0, 1) * .75
    layers.append((s, e, A[..., None], G[..., None]))
FS = RW * RH * 3
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', f'{wd}/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-shortest', '-movflags', '+faststart', 'sys/TikTok_skeleton_v2.mp4'], stdin=subprocess.PIPE)
for fi in range(N):
    raw = dec.stdout.read(FS)
    if len(raw) < FS: break
    fr = np.frombuffer(raw, np.uint8).reshape(RH, RW, 3).astype(np.float32); t = fi / FPS
    for s, e, A, G in layers:
        if t < s or t > e + 0.25: continue
        g = min(1, (t - s) / 0.18) * (1.0 if t <= e else max(0, 1 - (t - e) / 0.25))
        fr = fr * (1 - G * g) + GLOW * G * g; fr = fr * (1 - A * g) + COL * A * g
    if t < 0.4: fr *= t / 0.4
    if t > D - 0.5: fr *= max(0, (D - t) / 0.5)
    enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); dec.stdout.close(); enc.wait(); print('done', round(D, 1))
