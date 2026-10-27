import sys,json
from PIL import Image, ImageDraw, ImageFont
def grid(files,out,cols=3,tw=360,th=450,gap=4,labels=None,fs=15):
    rows=(len(files)+cols-1)//cols; lh=40 if labels else 0
    g=Image.new('RGB',(cols*tw+(cols-1)*gap,rows*(th+lh)+(rows-1)*gap),'white'); d=ImageDraw.Draw(g)
    fn=ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',fs)
    for i,f in enumerate(files):
        x=(i%cols)*(tw+gap); y=(i//cols)*(th+lh+gap); g.paste(Image.open(f).convert('RGB').resize((tw,th)),(x,y))
        if labels:
            import textwrap; t=textwrap.wrap(f'{i+1}. {labels[i]}',44)[:2]
            for k,ln in enumerate(t): d.text((x+4,y+th+2+k*18),ln,fill='#352535',font=fn)
    g.save(out,quality=88)
