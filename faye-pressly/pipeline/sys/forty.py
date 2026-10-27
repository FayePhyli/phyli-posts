"""post 3 · silent reel · forty messages before 9am · ~12s · the graffiti door, then the studio; four lines"""
import sys, os, subprocess, json; sys.path.insert(0, 'sys'); sys.path.insert(0, 'look')
from style import *
RW, RH, FPS = 1080, 1920, 30
SRC = "/mnt/user-data/uploads/Desktop/Phyli/Phyli Content CLAUDE/06 Studio & Life B-roll/"
meta = json.load(open('broll/meta.json')); os.makedirs('sys/r_forty', exist_ok=True)
GRADE = "eq=contrast=1.22:saturation=1.45:gamma=0.9,colorbalance=rh=0.06:bh=-0.10:rs=-0.03:bs=0.05,vignette=PI/5.5,noise=alls=6:allf=t+u"
N = int(5.5 * FPS) + 1
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'g30/src/mum12.jpg', '-t', '5.5', '-vf', f"scale={2*RW}:{2*RH}:force_original_aspect_ratio=increase,crop={2*RW}:{2*RH},zoompan=z='1+0.08*on/{N}':d={N}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={RW}x{RH},fps={FPS},setsar=1,{GRADE}", '-frames:v', str(int(5.5 * FPS)), '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', 'sys/r_forty/00.mp4'], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '12', '-i', SRC + meta['04']['f'], '-t', '6.5', '-an', '-vf', f"scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH},fps={FPS},setsar=1,{GRADE}", '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', 'sys/r_forty/01.mp4'], check=True)
open('sys/r_forty/list.txt', 'w').write(f"file '{os.path.abspath('sys/r_forty/00.mp4')}'\nfile '{os.path.abspath('sys/r_forty/01.mp4')}'\n")
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'sys/r_forty/list.txt', '-c', 'copy', 'sys/r_forty/base.mp4'], check=True)
LINES = [("forty messages before 9am.", 0.6, 5.3, 0), ("all of them need you.", 2.4, 5.3, 1), ("that isn't a logistics problem.", 6.2, 11.6, 0), ("that's a seized spine.", 8.2, 11.6, 1)]
f = F('sansm', 58); D = 12.0; Nf = int(D * FPS)
furn = Image.new('RGBA', (RW, RH), (0, 0, 0, 0)); fd = ImageDraw.Draw(furn); spaced(fd, (72, 110), 'no. 03  ·  palma', F('mono', 17), IVORY + (255,), .18); fd.text((RW - 72, 94), 'fp', font=F('italic', 44), fill=IVORY + (255,), anchor='ra')
fa = np.asarray(furn).astype(np.float32); FA = fa[..., 3:4] / 255; FRGB = fa[..., :3]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'sys/r_forty/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', 'sys/Reel_03_forty.mp4'], stdin=subprocess.PIPE)
grad = (1 - np.linspace(0, .45, RH))[:, None, None].astype(np.float32); FS = RW * RH * 3
for fi in range(Nf):
    raw = dec.stdout.read(FS)
    if len(raw) < FS: break
    fr = np.frombuffer(raw, np.uint8).reshape(RH, RW, 3).astype(np.float32) * grad; t = fi / FPS
    im = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im, 'RGBA')
    for ln, s, e, row in LINES:
        if s <= t <= e:
            a = min(1, (t - s) / 0.25) * min(1, (e - t) / 0.3); yy = 1380 + row * 80
            d.text((74, yy + 3), ln, font=f, fill=(10, 6, 10, int(160 * a))); d.text((72, yy), ln, font=f, fill=IVORY + (int(255 * a),))
    fr = np.asarray(im).astype(np.float32); fr = fr * (1 - FA) + FRGB * FA
    if t < 0.5: fr *= t / 0.5
    if t > D - 0.8: fr *= max(0, (D - t) / 0.8)
    enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('forty done')
