"""week one on the approved grid: same templates, new words. IG order (newest top-left)."""
exec(open('g60/build.py').read())
src = open('g60/final.py').read(); exec(src[src.index('def big'):src.index('T=[None]*21')])
BPK = ['#9A5A72', '#D395A6', '#F0C2CD', '#F9DEE5', '#FEF2F5']
os.makedirs('g60/week1', exist_ok=True)
tiles = {}
# TUE · manifesto reel → the stairs template
a = grade(F(L('faye33'), (.5, .55)), warm=.04)
tiles['tue'] = big(a, ['a note,', 'before this', 'page changes.'], IV, 118, y=130, glow='#F2B3A8', ga=.5)
# WED · manifesto carousel → the white outfit on the street
a = grade(F(L('faye0'), (.5, .4)), warm=.03, lift=4)
tiles['wed'] = big(a, ['FOR WOMEN', 'BUILDING', 'COMPANIES', 'WITH TASTE', 'AND AMBITION.'], IV, 104, y=150, glow='#E8C9A8', ga=.35)
# THU · the vision reel → the pastel swirl
pa = np.array(Image.open('g30/src/pastel1.jpg').convert('RGB')).astype(float); pa = pa * (250 / np.percentile(pa, 97, axis=(0, 1)))
a = grade(F(np.clip(pa, 0, 255), (.5, .45), 1.0), sat=1.3, bloom=.15, lift=6)
tiles['thu'] = big(a, ['vision is a', 'receptive state.'], '#6E3F66', 84, y=1110, shadow=0, glow='#FFF6F2', ga=.6, spark=3, seed=7)
# FRI · the yurt → the graffiti door
a = grade(F(L('mum12'), (.5, .5), 1.2), sat=1.2, bloom=.3)
tiles['fri'] = big(a, ['ONE YEAR', 'AGO', 'TONIGHT.'], '#F4EFE6', 150, glow='#B48CF0', ga=.6)
# SAT · what Phyli means → ink on paper (the 82% template), struck-through old name in type
p = fit_place(paper_bg('#F3EFE8'), ink_alpha_img('art57'), 600, 560, 540, 400)
p = big(p, ['sacred scaling'], '#7A6E78', 64, y=720, shadow=0)
pp = Image.fromarray(np.clip(p, 0, 255).astype(np.uint8)); dd = ImageDraw.Draw(pp)
rs = np.random.RandomState(3); pts = [(300 + i * 24, 752 + rs.randn() * 2.2) for i in range(21)]; dd.line(pts, fill=(30, 22, 30), width=5, joint='curve')
p = np.array(pp).astype(float)
p = big(p, ['Phyli.'], AUB, 190, y=800, shadow=0)
tiles['sat'] = big(p, ['phy, to grow.  li, the intelligence', 'already in her.'], AUB, 44, y=1060, shadow=0)
# SUN · both. obviously. → the amethyst on chocolate
am = L('mum36', (39, 615, 786, 1176)); m = cutout(am); a = obj_on(tex('mum0', BPK, .8), am, m, 780, 540, 560, shadow=.6, sheen=.3)
tiles['sun'] = big(a, ['business or pleasure?', 'both. obviously.'], IV, 72, y=1060, shadow=.45, glow='#B48CF0', ga=.4)
for k, t in tiles.items(): Image.fromarray(np.clip(np.nan_to_num(t), 0, 255).astype(np.uint8)).save(f'g60/week1/{k}.jpg', quality=92)
# the grid, IG order: newest top-left
mon = 'send/nightcourt/NightCourt_01.jpg'
order = ['sun', 'sat', 'fri', 'thu', 'wed', 'tue']
files = [f'g60/week1/{k}.jpg' for k in order] + [mon]
exec(open('g60/grid.py').read())
grey = Image.new('RGB', (1080, 1350), (225, 220, 214)); grey.save('g60/week1/old.jpg')
grid(files + ['g60/week1/old.jpg'] * 2, 'g60/week1/grid_by_sunday.jpg', labels=['SUN · both. obviously.', 'SAT · what Phyli means', 'FRI · the yurt', 'THU · the vision', 'WED · manifesto carousel', 'TUE · manifesto reel', 'MON · the Night Court (posted)', 'older post', 'older post'])
print('ok')
