import sys; sys.argv=['x']
H=open('g30/build8.py').read(); exec(H[:H.index('# 1\n')])
exec(open('g60/house.py').read())
sys.path.insert(0,'g60'); from snips import SN, snip
import json, os
INKA={'horse':ink_alpha_img('art62'),'eye':ink_alpha_img('art57'),'roots':ink_alpha_img('art54'),'tiger':ink_alpha_img('art76'),
 'thick':ink_alpha_img('art79'),'thicktiger':ink_alpha_img('art81'),'frame':ink_alpha_img('art66')}
for n in ['bloomtree','rootflower','sprig','marks','signature']: INKA[n]=inkfile(n)
sf=L('mum4'); A_=np.clip((sf.mean(2)-80)/110,0,1); yy,xx=np.mgrid[0:A_.shape[0],0:A_.shape[1]]; r=np.sqrt(((xx/A_.shape[1]-.5)/.5)**2+((yy/A_.shape[0]-.55)/.5)**2); INKA['seafan']=A_*np.clip((1-r)/.35,0,1)
def fit_place(p,A,maxw,maxh,cx,cy,col=INK,op=1.0):
    s=min(maxw/A.shape[1],maxh/A.shape[0]); return place(p,A,s,cx,cy,col,op)
# ---------- shared collab tiles ----------
VOLS=[('IX','Volume IX · Operations · the skeleton'),('VIII','Volume VIII · Leadership · the nervous system'),('X','Volume X · Relationships · symbiosis'),('XII','Volume XII · Rest · winter')]
def marker2(v,label,seed):
    rs=np.random.RandomState(seed); p=paper_bg('#F3EFE8'); M=np.zeros((TH,TW),np.float32)
    s=340; cx,cy=540,600; o=lambda: rs.randn()*7
    pts=[(cx-s+o(),cy-s+o()),(cx+s+o(),cy-s+o()),(cx+s+o(),cy+s+o()),(cx-s+o(),cy+s+o())]
    ext=lambda p_,q,k:(p_[0]+(p_[0]-q[0])*k,p_[1]+(p_[1]-q[1])*k)
    for i in range(4):
        a,b=pts[i],pts[(i+1)%4]; stroke(M,ext(a,b,.03+rs.rand()*.04),ext(b,a,.04-rs.rand()*.06),11+rs.rand()*5,rs)
    M=drybrush(M,rs); p=p*(1-M[...,None])+hx(INK)*M[...,None]
    A=snip(v); cols=A.max(0)>.2; w=len(cols); gaps=[];run=0
    for x in range(w):
        if not cols[x]: run+=1
        else:
            if run>25: gaps.append((x-run,x))
            run=0
    num=A[:, :gaps[0][0]] if gaps else A; big=max(gaps,key=lambda g:g[1]-g[0]) if len(gaps)>=2 else None; title=A[:, big[1]:] if big else None
    p=fit_place(p,num,300,230,540,520)
    if title is not None: p=fit_place(p,title,480,140,540,760)
    return mono(p,label.upper(),1060,size=20)
RA={'IX':[('the skeleton','roots',.0),('posture','tiger',.0)],'VIII':[('the herd at the river','horse',0),('the second dome','eye',0)],
    'X':[('the relationship that changed its kind','sprig',0),('parasitism','thicktiger',0)],'XII':[('what winter actually does','bloomtree',0),('planting in the dark','rootflower',0)]}
def ra(v,i):
    t,k,_=RA[v][i]; p=paper_bg('#F3EFE8'); p=fit_place(p,INKA[k],720,760,540,560)
    p=mono(p,'READ ALOUD · VOLUME '+v,1120,size=18,op=.6); return mono(p,t.upper(),1160,size=22)
def correction(seed=0,dark=False,scale=.82,cy=640):
    d=np.load('hw/corr.npz'); A=np.maximum.reduce([d['top'],d['bot']*.55,d['strike']*.55])
    if dark:
        bg=grade(grad('#3A2838','#1F141E'),bloom=0,soft=0,grain=6); return place(bg,A,scale,TW/2,cy,'#EDE4D6')
    return place(paper_bg(),A,scale,TW/2,cy,'#2A1B2A')
COLLAB={}
for j,(v,l) in enumerate(VOLS): COLLAB[v]={'M':marker2(v,l,j+3),'RA1':ra(v,0),'RA2':ra(v,1)}
# ---------- house grid ----------
HT=[];HL=[]
def h(a,lab): HT.append(np.clip(a,0,255)); HL.append(lab)
LINES={'IX':['Most founders have built one skeleton and are being broken by the other.','The tool is a prosthetic. Operations is the posture.','Work flows. It does not pool.','A good crutch makes itself unnecessary.'],
 'VIII':['Culture is the ground everyone stands on. Leadership is the signal you are sending across it right now.','Regulated. Congruent. Going somewhere worth following.','The dome holds pressure off the life beneath it…','Hold your own state. Make your signal congruent.'],
 'X':['The organisation is relationships, all the way down.','Who is being fed, and at whose cost?','What was once mutual quietly became something else.','The bee is not helping the flower. The bee is being fed.'],
 'XII':['Rest is not a recharge. It is a revelation.','Freeze looks like rest and restores nothing.','A plant denied winter does not flower.','Do not rush the spring.']}
CORR={'IX':['we need a better system → we need to stop bracing','an organisation is a machine → already alive'],'VIII':['founder mode → regulated mode','be the strongest in the room → be the steadiest'],
 'X':["we're a family → a mutual arrangement, on purpose",'keep everyone happy → keep it mutual'],'XII':["I'll plan January → I'll plant January",'recharge → reveal']}
def line_tile(v,i,seed):
    rs=np.random.RandomState(seed); p=paper_bg('#F3EFE8')
    keys=['larger','growth','build','intercourse','watch','pack']; k=keys[(seed)%len(keys)]
    lay=(seed+i)%4
    if lay==0:
        p=fit_place(p,snip(k),920,300,540,560); p=fit_place(p,INKA['sprig'],140,200,930,1170,op=.9)
    elif lay==1:
        m=INKA['marks']; hh,ww=m.shape; p=fit_place(p,m[int(hh*.68):int(hh*.98),0:int(ww*.62)],1100,600,420,1040); p=fit_place(p,snip(k),900,260,540,300)
    elif lay==2:
        p=fit_place(p,snip(k),920,300,540,700); p=dots(p,860,250,9,26,seed)
    else:
        p=fit_place(p,snip(k),860,260,520,1050); p=fit_place(p,INKA['frame'],520,420,700,460,op=.95)
    if seed%5==2: p=gdot(p,540,1230)
    return p
for j,(v,l) in enumerate(VOLS):
    C=COLLAB[v]; L4=LINES[v]; C2=CORR[v]
    h(C['M'],f'{v} marker · collab'); h(line_tile(v,0,j*7+1),'line: '+L4[0]); h(C['RA1'],'read aloud · collab')
    h(correction(),'correction: '+C2[0]); h(line_tile(v,1,j*7+2),'line: '+L4[1]); h(line_tile(v,2,j*7+3),'line: '+L4[2])
    h(C['RA2'],'read aloud · collab'); h(dots(correction(scale=.62,cy=820),300,330,7,22,j+11),'correction: '+C2[1]); h(line_tile(v,3,j*7+4),'line: '+L4[3])
os.makedirs('g60/house',exist_ok=True)
for i,t in enumerate(HT): Image.fromarray(t.astype(np.uint8)).save(f'g60/house/{i+1:02d}.jpg',quality=90)
json.dump(HL,open('g60/house_labels.json','w'))
np.save('g60/collab_keys.npy',np.array([0]))
import pickle; pickle.dump({v:{k:np.clip(a,0,255).astype(np.uint8) for k,a in d.items()} for v,d in COLLAB.items()},open('g60/collab.pkl','wb'))
