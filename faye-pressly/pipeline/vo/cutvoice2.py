"""like cutvoice, but the kept words are read in an ORDER of segments (reordering allowed). spec json: {"base": "samhain", "drop": [[a,b],...], "order": [[a,b],...]} (ranges are original word indices, end exclusive)
usage: python3 vo/cutvoice2.py <name> [cap] [lead] [tail]"""
import sys, json, subprocess
name = sys.argv[1]; CAP = float(sys.argv[2]) if len(sys.argv) > 2 else 1.1; LEAD = float(sys.argv[3]) if len(sys.argv) > 3 else 0.4; TAIL = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
spec = json.load(open(f'vo/{name}_spec.json')); ws = json.load(open(f"mm/{spec['base']}_words.json"))
drop = set()
for a, b in spec['drop']: drop.update(range(a, b))
pieces = []; keep = []; times = []; T = 0.0; JOIN = 0.45  # pause inserted between reordered segments
for si, (a, b) in enumerate(spec['order']):
    idx = [i for i in range(a, b) if i not in drop]
    if not idx: continue
    cur = ws[idx[0]]['s'] - (LEAD if si == 0 else 0.12); shift = T - cur
    for n, i in enumerate(idx):
        w = ws[i]; keep.append(w); times.append([w['s'] + shift, w['e'] + shift])
        if n + 1 < len(idx):
            j = idx[n + 1]; gap = ws[j]['s'] - w['e']
            if j != i + 1:  # a dropped run sits between: cut it tight
                c0 = w['e'] + 0.05; c1 = ws[j]['s'] - 0.05; pieces.append((cur, c0)); cur = c1; shift -= (c1 - c0)
            elif gap > CAP + 0.3:
                c0 = w['e'] + CAP * 0.45; c1 = ws[j]['s'] - CAP * 0.55; pieces.append((cur, c0)); cur = c1; shift -= (c1 - c0)
    last = ws[idx[-1]]['e'] + (TAIL if si == len(spec['order']) - 1 else 0.15); pieces.append((cur, last)); T = last + shift
    if si < len(spec['order']) - 1: pieces.append(('pad', JOIN)); T += JOIN
D = T
fc = ''
for i, p in enumerate(pieces):
    fc += (f'anullsrc=r=48000:cl=mono,atrim=0:{p[1]:.3f}[p{i}];' if p[0] == 'pad' else f'[0:a]atrim={p[0]:.3f}:{p[1]:.3f},asetpts=PTS-STARTPTS[p{i}];')
fc += ''.join(f'[p{i}]' for i in range(len(pieces))) + f'concat=n={len(pieces)}:v=0:a=1,highpass=f=60,afftdn=nr=6:nf=-34,equalizer=f=3000:t=q:w=1.2:g=1.5,loudnorm=I=-16:TP=-1.5:LRA=9,afade=t=out:st={D-0.8:.2f}:d=0.8[a]'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f"vo/{spec['base']}.m4a", '-filter_complex', fc, '-map', '[a]', '-ac', '1', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', f'vo/{name}_cut.m4a'], check=True)
for w, t in zip(keep, times):
    if w['w'].startswith('Sowin'): w['w'] = 'Samhain,'
json.dump({'D': D, 'words': [{'w': w['w'], 's': t[0], 'e': t[1]} for w, t in zip(keep, times)], 'sections': spec['order']}, open(f'vo/{name}_timeline.json', 'w'))
print(name, 'pieces', len(pieces), 'duration', round(D, 1), 'words', len(keep))
