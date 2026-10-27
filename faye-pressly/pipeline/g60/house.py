# requires header helpers (paper_bg, place, ink_alpha_img, inkfile, hx, TW, TH, np, cv2, Image)
from PIL import ImageFont, ImageDraw
MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
INK='#1E161E'
def mono(a,t,y,col=INK,size=22,track=.32,x=None,op=.85):
    f=ImageFont.truetype(MONO,size); m=Image.new('L',(TW,TH),0); d=ImageDraw.Draw(m)
    w=sum(d.textlength(c,font=f)+size*track for c in t)-size*track; xx=(TW-w)/2 if x is None else x
    for c in t: d.text((xx,y),c,font=f,fill=255); xx+=d.textlength(c,font=f)+size*track
    A=np.asarray(m,float)/255*op; return a*(1-A[...,None])+hx(col)*A[...,None]
def stroke(M,p0,p1,w,rs):
    n=int(np.hypot(p1[0]-p0[0],p1[1]-p0[1])/2)+2
    for i in range(n):
        t=i/(n-1); x=p0[0]+(p1[0]-p0[0])*t+rs.randn()*.8; y=p0[1]+(p1[1]-p0[1])*t+rs.randn()*.8
        r=w*(0.75+0.35*np.sin(t*np.pi))*(1-0.35*t)+rs.rand()*1.2
        cv2.circle(M,(int(x),int(y)),max(1,int(r)),1.0,-1)
def drybrush(M,rs,amt=.55):
    n=cv2.GaussianBlur(rs.rand(*M.shape).astype(np.float32),(0,0),1.2); n=(n-n.min())/(n.max()-n.min())
    streak=cv2.GaussianBlur(rs.rand(*M.shape).astype(np.float32),(0,0),sigmaX=1,sigmaY=6); streak=(streak-streak.min())/(streak.max()-streak.min())
    T_=np.clip((n*.5+streak*.5)*2.6-0.35,0,1)
    return cv2.GaussianBlur(M*np.clip(T_+ (1-cv2.GaussianBlur(M,(0,0),6))*0,0,1),(0,0),.9)
GLY={'I':[((0,0),(0,1))],'V':[((-.35,0),(0,1)),((.35,0),(0,1))],'X':[((-.35,0),(.35,1)),((.35,0),(-.35,1))]}
def numeral(M,txt_,cx,cy,h,w,rs):
    widths={'I':.25,'V':.85,'X':.85}; tot=sum(widths[c] for c in txt_)*h+ (len(txt_)-1)*h*.12; x=cx-tot/2
    for c in txt_:
        ww=widths[c]*h; mx=x+ww/2
        for (a0,a1) in GLY[c]:
            stroke(M,(mx+a0[0]*h,cy-h/2+a0[1]*h),(mx+a1[0]*h,cy-h/2+a1[1]*h),w,rs)
        x+=ww+h*.12
def marker(num,label,seed=1,tone='#F3EFE8'):
    rs=np.random.RandomState(seed); p=paper_bg(tone); M=np.zeros((TH,TW),np.float32)
    s=330; cx,cy=540,600; o=lambda: rs.randn()*6
    pts=[(cx-s+o(),cy-s+o()),(cx+s+o(),cy-s+o()),(cx+s+o(),cy+s+o()),(cx-s+o(),cy+s+o())]
    for i in range(4):
        a,b=pts[i],pts[(i+1)%4]; ext=lambda p,q,k: (p[0]+(p[0]-q[0])*k,p[1]+(p[1]-q[1])*k)
        stroke(M,ext(a,b,.03+rs.rand()*.04),ext(b,a,-.03 if i==2 else .04),12+rs.rand()*5,rs)
    numeral(M,num,cx,cy,240,15,rs)
    M=drybrush(M,rs); p=p*(1-M[...,None])+hx(INK)*M[...,None]
    p=mono(p,label.upper(),1060,size=21)
    return p
def ra_tile(alpha,label,scale,cy=600,seed=2,tone='#F3EFE8'):
    p=paper_bg(tone); p=place(p,alpha,scale,540,cy,INK)
    p=mono(p,'READ ALOUD',1120,size=19,op=.6); p=mono(p,label.upper(),1160,size=22)
    return p

def dots(p,cx,cy,n,rmax,seed,col=INK):
    rs=np.random.RandomState(seed); M=np.zeros((TH,TW),np.float32)
    for i in range(n):
        r=int(rmax*(0.25+0.75*rs.rand()**2)); x=int(cx+rs.randn()*rmax*1.6); y=int(cy+rs.randn()*rmax*1.2)
        cv2.circle(M,(x,y),r,1.0,-1)
    n_=cv2.GaussianBlur(rs.rand(TH,TW).astype(np.float32),(0,0),1.5); M=np.clip(M*(0.75+n_*.6),0,1); M=cv2.GaussianBlur(M,(0,0),1.1)
    return p*(1-M[...,None])+hx(col)*M[...,None]
def gdot(p,x,y,r=13): 
    M=np.zeros((TH,TW),np.float32); cv2.circle(M,(x,y),r,1.0,-1); M=cv2.GaussianBlur(M,(0,0),1.2)
    return p*(1-M[...,None])+hx('#7E9A3A')*M[...,None]
def crop_alpha(A,box): 
    h,w=A.shape; x0,y0,x1,y1=box; return A[int(y0*h):int(y1*h),int(x0*w):int(x1*w)]
def fitw(A,w): return w/A.shape[1]
