"""cut a voice note by word timings: drop word ranges, cap pauses, clean gently, keep it crisp. writes <name>_cut.m4a + <name>_timeline.json
usage: python3 vo/cutvoice.py <name> [cap=1.1] [lead=0.4] [tail=1.0]"""
import sys, json, subprocess
name = sys.argv[1]; CAP = float(sys.argv[2]) if len(sys.argv) > 2 else 1.1; LEAD = float(sys.argv[3]) if len(sys.argv) > 3 else 0.4; TAIL = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
ws = json.load(open(f'mm/{name}_words.json'))
try: cuts = json.load(open(f'vo/{name}_cuts.json'))
except FileNotFoundError: cuts = []
drop = set()
for a, b in cuts: drop.update(range(a, b))
keep = [w for i, w in enumerate(ws) if i not in drop]
# removal intervals: dropped word spans (padded to neighbours), then long pauses
pieces = []; cur = max(0, ws[0]['s'] - LEAD); shift = -cur; times = []
i = 0
while i < len(ws):
    w = ws[i]
    if i in drop:
        # find end of dropped run
        j = i
        while j < len(ws) and j in drop: j += 1
        prev_e = ws[i - 1]['e'] if i > 0 else w['s']; next_s = ws[j]['s'] if j < len(ws) else ws[-1]['e']
        c0 = prev_e + 0.05; c1 = next_s - 0.05
        pieces.append((cur, c0)); cur = c1; shift -= (c1 - c0); i = j; continue
    times.append([w['s'] + shift, w['e'] + shift])
    if i + 1 < len(ws) and (i + 1) not in drop:
        gap = ws[i + 1]['s'] - w['e']
        if gap > CAP + 0.3:
            c0 = w['e'] + CAP * 0.45; c1 = ws[i + 1]['s'] - CAP * 0.55; pieces.append((cur, c0)); cur = c1; shift -= (c1 - c0)
    i += 1
pieces.append((cur, ws[-1]['e'] + TAIL)); D = sum(b - a for a, b in pieces)
fc = ''.join(f'[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[p{i}];' for i, (a, b) in enumerate(pieces)) + ''.join(f'[p{i}]' for i in range(len(pieces))) + f'concat=n={len(pieces)}:v=0:a=1,highpass=f=60,afftdn=nr=6:nf=-34,equalizer=f=3000:t=q:w=1.2:g=1.5,loudnorm=I=-16:TP=-1.5:LRA=9,afade=t=out:st={D-0.8:.2f}:d=0.8[a]'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'vo/{name}.m4a', '-filter_complex', fc, '-map', '[a]', '-ac', '1', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', f'vo/{name}_cut.m4a'], check=True)
json.dump({'D': D, 'words': [{'w': w['w'], 's': t[0], 'e': t[1]} for w, t in zip(keep, times)]}, open(f'vo/{name}_timeline.json', 'w'))
print(name, 'pieces', len(pieces), 'duration', round(D, 1), 'words', len(keep))
