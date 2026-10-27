"""the samhain cut with NO grade, smoke or captions: her clips in order, voice attached. for her to style herself."""
import sys, os, subprocess
src = open('sys/reel_veil3.py').read(); head = src[:src.index('# ---- smoke')]
sys.argv = ['x', 'samhain3', 'the night', 'x']; G = {}; exec(head, G)
SHOTS, meta, RW, RH, FPS, LEAD = G['SHOTS'], G['meta'], G['RW'], G['RH'], G['FPS'], G['LEAD']
wd = 'sys/r_samhain3_og'; os.makedirs(wd, exist_ok=True); segs = [f'{wd}/black.mp4']
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', f'color=c=black:s={RW}x{RH}:r={FPS}', '-t', f'{LEAD:.2f}', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', segs[0]], check=True)
for i, s in enumerate(SHOTS):
    k, ip, d, fx, fy = s[:5]; m = meta[k]; out = f'{wd}/{i:02d}.mp4'; segs.append(out)
    if ip + d > m['d'] - 0.1: ip = max(0, m['d'] - d - 0.1)
    vf = f"scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}:'(iw-{RW})*{fx}':'(ih-{RH})*{fy}',fps={FPS},setsar=1,format=yuv420p"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{ip:.2f}', '-i', m['p'], '-t', f'{d:.3f}', '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', out], check=True); print('seg', i, k, flush=True)
open(f'{wd}/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{wd}/list.txt', '-i', 'vo/samhain3_cut.m4a', '-filter_complex', f'[1:a]adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', 'sam/Samhain_clips_OG.mp4'], check=True)
print('done')
