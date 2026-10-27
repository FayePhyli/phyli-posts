import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
U='/root/.claude/uploads/68bfe095-3c99-5cc0-81a9-b2085cd64223/'
FB='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
def hx(h): h=h.lstrip('#'); return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)
def load(p): return np.asarray(Image.open(p).convert('RGB'),float)
def fit(a,W,H,focus=(.5,.5),zoom=1.0):
    h,w=a.shape[:2]; s=max(W/w,H/h)*zoom
    a=cv2.resize(a,(int(w*s+1),int(h*s+1)),interpolation=cv2.INTER_CUBIC)
    h,w=a.shape[:2]; x=int((w-W)*focus[0]); y=int((h-H)*focus[1]); return a[y:y+H,x:x+W]
def iri_map(H,W,t=0.0,seed=0,scale=1.0):
    rs=np.random.RandomState(seed); yy,xx=np.mgrid[0:H,0:W]
    n=cv2.GaussianBlur(rs.rand(H//4+1,W//4+1).astype(np.float32),(0,0),6*scale); n=cv2.resize(n,(W,H)); n=(n-n.min())/(n.max()-n.min()+1e-6)
    ph=xx*0.0025+yy*0.0018+n*2.2+t
    st=np.array([hx(c) for c in ('#F6DDEC','#BFD8F2','#DCC6F6','#C4ECDA','#F7E2CF','#CFCBF6','#F6DDEC')])
    f=(np.sin(ph*2*np.pi)*.5+.5)*(len(st)-1); i=np.floor(f).astype(int); fr=(f-i)[...,None]; i2=np.minimum(i+1,len(st)-1)
    return st[i]*(1-fr)+st[i2]*fr
def y2k(a,sat=1.25,con=1.08,bloom=0.35,soft=1.2,grain=7,warm=0.0,seed=0):
    m=a.mean(2,keepdims=True); a=m+(a-m)*sat; a=(a-128)*con+128
    if warm: a=a*np.array([1+warm,1,1-warm])
    a=np.clip(a,0,255)
    hi=np.clip(a-150,0,255); bl=cv2.GaussianBlur(hi,(0,0),25)
    a=255-(255-a)*(255-bl*bloom)/255
    if soft: a=cv2.GaussianBlur(a,(0,0),soft)
    a=a+np.random.RandomState(seed).normal(0,grain,a.shape[:2])[...,None]
    return np.clip(a,0,255)
def text_layer(W,H,lines,size,y,lh=1.05,track=-0.02,align='c'):
    f=ImageFont.truetype(FB,size); m=Image.new('L',(W,H),0); d=ImageDraw.Draw(m)
    yy=y
    for ln in lines:
        w=d.textlength(ln,font=f)+track*size*len(ln); x=(W-w)/2
        for ch in ln:
            d.text((x,yy),ch,font=f,fill=255); x+=d.textlength(ch,font=f)+track*size
        yy+=size*lh
    return np.asarray(m,float)/255
def put_text(a,A,col,glow=None,glow_r=14,glow_a=0.7,shadow=0.0,iri=False,t=0.0,sparkle=0):
    H,W=A.shape
    if shadow:
        s=cv2.GaussianBlur(np.roll(A,(4,3),(0,1)),(0,0),5)*shadow; a=a*(1-s[...,None])+np.array([30,18,30.])*s[...,None]
    if glow is not None:
        g=np.clip(cv2.GaussianBlur(A,(0,0),glow_r)*2.0,0,1)*glow_a; a=a*(1-g[...,None])+hx(glow)*g[...,None]
    C=iri_map(H,W,t) if iri else hx(col)
    a=a*(1-A[...,None])+C*A[...,None]
    if sparkle:
        rs=np.random.RandomState(int(t*30)%997+11); ys,xs=np.where(A>0.9)
        if len(ys):
            idx=rs.choice(len(ys),sparkle); S=np.zeros((H,W),np.float32)
            for k in idx:
                y,x=ys[k],xs[k]; r=rs.randint(10,26)
                cv2.line(S,(x-r,y),(x+r,y),1.0,2); cv2.line(S,(x,y-r),(x,y+r),1.0,2)
                cv2.circle(S,(x,y),3,1.0,-1)
            S=cv2.GaussianBlur(S,(0,0),2.2); S=np.clip(S*1.6,0,1)
            a=a*(1-S[...,None])+255*S[...,None]
    return np.clip(a,0,255)
def save(a,p,q=92): Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save(p,quality=q)
def plum_grade(a,depth=0.5):
    L=a.mean(2,keepdims=True)/255
    sh=hx('#2A1630'); hi=hx('#F2E4EA')
    toned=sh*(1-L)+hi*L
    a=a*0.55+toned*0.45
    a=a*(0.30+0.70*L**1.1)*depth
    return np.clip(a,0,255)
def stars(a,A,n,seed,t=0.0):
    H,W=A.shape; rs=np.random.RandomState(seed); ys,xs=np.where(A>0.95)
    S=np.zeros((H,W),np.float32)
    for k in rs.choice(len(ys),n):
        y,x=ys[k],xs[k]; r=rs.randint(18,34); ph=0.5+0.5*np.sin(t*4+k)
        for dx,dy,rr in ((1,0,r),(0,1,r),(1,1,r*0.35),(1,-1,r*0.35)):
            for i in range(-int(rr),int(rr)+1):
                v=(1-abs(i)/rr)**2.2*ph; px,py=int(x+i*dx),int(y+i*dy)
                if 0<=px<W and 0<=py<H: S[py,px]=max(S[py,px],v)
    S=cv2.GaussianBlur(S,(0,0),1.1); g=cv2.GaussianBlur(S,(0,0),6)*0.8
    S=np.clip(S*2.4+g*1.5,0,1)
    return np.clip(a*(1-S[...,None])+255*S[...,None],0,255)
