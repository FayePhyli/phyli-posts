"""slide 02 as video: 7s of her making the pastel wash (two 3.5s cuts), 4:5, lamp taken off, the Tamlin words over it. silent."""
import sys, os, subprocess; sys.path.insert(0, 'sys')
from style import *
import cv2
OUT = 'sys/week1/nightcourt'; SRC = "/mnt/user-data/uploads/Desktop/Phyli/Phyli Content CLAUDE/02 Faye's Art/IMG_7446.MOV"
RW, RH, FPS = 1080, 1350, 30
CUTS = [(2.0, 3.3, .45), (26.0, 3.3, .45), (48.0, 3.3, .5), (66.0, 3.3, .5), (100.0, 3.3, .45), (148.0, 3.3, .55)]   # the progress, in order
wd = 'sys/r_pastel'; os.makedirs(wd, exist_ok=True); segs = []
# lamp off + a touch of lilac: multiply channels, lift mids slightly
GRADE = "colorbalance=rs=-0.12:gs=-0.03:bs=0.18:rm=-0.10:gm=-0.02:bm=0.14:rh=-0.05:bh=0.06,eq=saturation=1.0:gamma=1.06:brightness=0.04,colorchannelmixer=rr=0.92:gg=0.92:bb=0.92:aa=1,lutrgb=r=val+20:g=val+19:b=val+18"
for i, (ip, d, fx) in enumerate(CUTS):
    out = f'{wd}/{i:02d}.mp4'; segs.append(out)
    vf = f"scale={RW}:-2,crop={RW}:{RH}:0:'(ih-{RH})*{fx}',fps={FPS},setsar=1,{GRADE}"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{ip:.2f}', '-i', SRC, '-t', f'{d:.2f}', '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], check=True)
open(f'{wd}/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{wd}/list.txt', '-c', 'copy', f'{wd}/base.mp4'], check=True)
# words layer (ivory headline with soft pink glow; aubergine body), composited per frame
AUB = (70, 40, 60); GLOWC = np.array((246, 226, 236), np.float32)
tmp = Image.new('RGB', (RW, RH), (0, 0, 0))
y = text(tmp, "Feyre paints", 'display', 96, 72, 520, col=(255, 255, 255), maxw=930, align='c', lh=1.04)
A_head = np.asarray(tmp.convert('L')).astype(np.float32) / 255
G = np.clip(cv2.GaussianBlur(A_head, (0, 0), 14) * 1.3, 0, 1)[..., None]; A_head = A_head[..., None]
tmp2 = Image.new('RGB', (RW, RH), (0, 0, 0)); text(tmp2, "she also runs a court\nnobody made her choose", 'serif', 36, 72, y + 44, col=(255, 255, 255), maxw=860, align='c', lh=1.36)
spaced(ImageDraw.Draw(tmp2), (RW/2, 96), 'faye pressly  ·  a note on book six', F('mono', 16), (255, 255, 255), .3, 'c')
spaced(ImageDraw.Draw(tmp2), (RW - 72, RH - 84), '06 / 07', F('mono', 15), (255, 255, 255), .18, 'r')
A_body = (np.asarray(tmp2.convert('L')).astype(np.float32) / 255)[..., None]
IV = np.array(IVORY, np.float32); AU = np.array(AUB, np.float32); PE = np.array((58, 62, 138), np.float32)
D = sum(c[1] for c in CUTS); N = int(D * FPS); FS = RW * RH * 3
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', f'{wd}/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-shortest', '-movflags', '+faststart', f'{OUT}/NightCourt_06_video.mp4'], stdin=subprocess.PIPE)
for fi in range(N):
    raw = dec.stdout.read(FS)
    if len(raw) < FS: break
    fr = np.frombuffer(raw, np.uint8).reshape(RH, RW, 3).astype(np.float32); t = fi / FPS
    g = min(1, t / 0.35)
    fr = fr * (1 - G * .8 * g) + GLOWC * G * .8 * g
    fr = fr * (1 - A_head * g) + PE * A_head * g
    fr = fr * (1 - A_body * g) + AU * A_body * g
    enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); dec.stdout.close(); enc.wait(); print('done', D)
