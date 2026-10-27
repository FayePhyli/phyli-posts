exec(open('g60/build.py').read())

def big(a,lines,col,size,y=None,glow=None,ga=.5,shadow=.45,lh=.98,spark=0,seed=1,iri=False):
    from PIL import ImageFont as _F, ImageDraw as _D
    while True:
        f=_F.truetype(FB,size); w=max(_D.Draw(Image.new('L',(1,1))).textlength(l,font=f) for l in lines)
        if w<=960 or size<40: break
        size-=4
    h=len(lines)*size*lh; y=(TH-h)/2 if y is None else y
    A=cv2.GaussianBlur(text_layer(TW,TH,lines,size,y,lh=lh,track=-0.035),(0,0),1.0)
    if shadow:
        sh=cv2.GaussianBlur(np.roll(A,(6,4),(0,1)),(0,0),5)*shadow; a=a*(1-sh[...,None])+np.array([40,25,40.])*sh[...,None]
    if glow:
        g=np.clip(cv2.GaussianBlur(A,(0,0),16)*1.8,0,1)*ga; a=a*(1-g[...,None])+hx(glow)*g[...,None]
    C=iri_map(TH,TW,t=.3,seed=seed) if iri else hx(col)
    a=np.clip(a*(1-A[...,None])+C*A[...,None],0,255)
    return stars(a,A,spark,seed) if spark else a
T=[None]*21; LB=[None]*21
def put(k,a,lab): T[21-k]=np.clip(np.nan_to_num(a),0,255); LB[21-k]=f'{k}. {lab}'
# 1 marker IX (ink, collab)
put(1,COLLAB['IX']['M'],'IX marker · collab · ink')
# 2 carrying
a=grade(F(L('faye0'),(.5,.4)),warm=.03,lift=4); put(2,big(a,['SO WHY DOES','RUNNING IT FEEL','LIKE CARRYING IT?'],IV,104,y=150,glow='#E8C9A8',ga=.35),'VO · carrying')
# 3 forty messages
a=grade(F(L('mum12'),(.5,.5),1.2),sat=1.2,bloom=.3); put(3,big(a,['FORTY','MESSAGES','BEFORE 9AM.'],'#F4EFE6',150,glow='#B48CF0',ga=.6),'silent · forty messages')
# 4 RA skeleton: sea fan ivory on olive
sf=L('mum4'); A_=np.clip((sf.mean(2)-115)/80,0,1)**1.2; _h,_w=A_.shape; _f=np.minimum(1,np.minimum(np.arange(_h)/(_h*.12),(_h-1-np.arange(_h))/(_h*.22)))[:,None]*np.minimum(1,np.minimum(np.arange(_w)/(_w*.08),(_w-1-np.arange(_w))/(_w*.08)))[None]; A_=A_*_f; BPK=['#9A5A72','#D395A6','#F0C2CD','#F9DEE5','#FEF2F5']; bg=tex('art95',BPK,.85,(.4,.6),1.3)
a=fit_place(bg,A_,1080,1000,540,520,'#7A3A58',.92); a=caps(a,'read aloud · volume ix',1040,'#7A3A58'); put(4,big(a,['the skeleton.'],'#7A3A58',84,y=1090,shadow=0,glow='#FFF4F6',ga=.6,spark=3,seed=4),'read aloud · the skeleton')
# 5 compensating: messy ink page
p=paper_bg('#F3EFE8'); mk=inkfile('marks'); h_,w_=mk.shape; m1=mk[int(h_*.68):int(h_*.98),0:int(w_*.62)]; m2=mk[int(h_*.30):int(h_*.52),int(w_*.28):int(w_*.75)]
p=place(p,m1,1000/m1.shape[1],560,1020,'#1E161E'); p=place(p,m2,380/m2.shape[1],900,130,'#1E161E',.85)
A=text_layer(TW,TH,['WHAT IS YOUR COMPANY','COMPENSATING FOR?'],62,330,lh=1.05,track=-0.01); put(5,put_text(p,A,AUB,shadow=0),'carousel · compensating · ink')
# 6 work flows: leaf + hot pink
a=grade(F(L('art9'),(.5,.5),1.1),sat=1.1,lift=22); a=hotline(a,560,0,TH); put(6,big(a,['WORK FLOWS.','IT DOES','NOT POOL.'],IV,120,glow='#5A2E1E',ga=.45),'VO · work flows')
# 7 correction ink
put(7,hand(paper_bg(),.82,640),'correction · better system → stop bracing · ink (handwrite)')
# 8 black friday: beetle iridescent
jb=np.array(Image.open('g30/src/jewel_beetle.png').convert('RGB')).astype(float)
cr=jb[430:1590,110:1050]; bgc=np.median(np.concatenate([cr[:40].reshape(-1,3),cr[:, :40].reshape(-1,3),cr[:, -40:].reshape(-1,3)]),0)
cv=np.zeros((TH,TW,3))+bgc; yy,xx=np.mgrid[0:TH,0:TW]; cv=cv  # soft fall-off
sc=.86; cr=cv2.resize(cr,None,fx=sc,fy=sc,interpolation=cv2.INTER_LANCZOS4); h,w=cr.shape[:2]
x0=(TW-w)//2; y0=40; m=np.ones((h,w)); fe=110
for i in range(fe): v=i/fe; m[i,:]*=v; m[-1-i,:]*=v; m[:,i]*=v; m[:,-1-i]*=v
y1=min(TH,y0+h); h2=y1-y0; reg=cv[y0:y1,x0:x0+w]; mm=m[:h2,:,None]
cv[y0:y1,x0:x0+w]=reg*(1-mm)+cr[:h2]*mm
a=grade(cv,sat=1.12,bloom=.25,tint='#E6DCEE',ta=.05)
put(8,big(a,['black friday will','find out which','skeleton you built.'],'#4A2C46',78,y=1075,shadow=0,glow='#F7EEF6',ga=.6,spark=4,seed=3),'VO · black friday · jewel beetle placeholder (license or paint)')
# 9 crutch: amethyst on chocolate (no title)
am=L('mum36',(39,615,786,1176)); m=cutout(am); put(9,obj_on(tex('mum0',BPK,.8),am,m,780,540,640,shadow=.6,sheen=.3),'carousel · crutch test (no title)')
# 10 RA posture: stairs
a=grade(F(L('faye33'),(.5,.55)),warm=.04); a=caps(a,'read aloud · volume ix',110,IV); put(10,big(a,['POSTURE.'],IV,150,y=150,glow='#F2B3A8',ga=.5),'read aloud · posture')
# 11 talking: selfie
sc_=np.array(Image.open('g30/src/scales.png').convert('RGB')).astype(float)[421:1437,19:1162]
a=grade(F(sc_,(.5,.5),1.0),sat=1.15,bloom=.3,lift=-6)
put(11,big(a,['MOST FOUNDERS','HAVE BUILT','ONE SKELETON','AND ARE BEING','BROKEN BY','THE OTHER.'],'#FBF3F0',150,lh=1.78,glow='#6E3352',ga=.55,shadow=.5,spark=5,seed=11),'VO · one skeleton · scales placeholder')
# 12 rhythm
pa=np.array(Image.open('g30/src/pastel1.jpg').convert('RGB')).astype(float); pa=pa*(250/np.percentile(pa,97,axis=(0,1))); a=grade(F(np.clip(pa,0,255),(.5,.45),1.0),sat=1.3,bloom=.15,lift=6); put(12,big(a,['rhythm,','not rigidity.'],'#6E3F66',84,y=1110,shadow=0,glow='#FFF6F2',ga=.6,spark=3,seed=7),'silent · rhythm')
# 13 studio: prints (no title)
put(13,grade(F(L('faye98'),(.5,.4)),sat=1.15,bloom=.3),'studio · silver, bone, ink (no title)')
# 14 marker VIII ink
put(14,COLLAB['VIII']['M'],'VIII marker · collab · ink')
# 15 hold your face: headscarf
a=grade(F(L('faye20'),(.75,.4),1.15),warm=.04,bloom=.35); put(15,big(a,['you can hold','your face for','about an hour.'],'#F7D9CF',96,y=130,glow='#C2603A',ga=.4),'VO · hold your face')
# 16 82%: eye ink on paper
p=fit_place(paper_bg('#F3EFE8'),ink_alpha_img('art57'),600,560,540,430)
p=big(p,['82%'],AUB,200,y=760,shadow=0); put(16,big(p,['of bosses have had','no management training.'],AUB,56,y=980,shadow=0),'silent · 82% · ink')
# 17 RA herd: wolf
a=grade(F(L('art73'),(.5,.35),1.05),warm=.02,tint='#E2D2E8',ta=.06); a=caps(a,'read aloud · volume viii',1040,'#5A2E3E'); put(17,big(a,['the herd','at the river.'],'#5A2E3E',80,y=1080,shadow=0,glow='#F4EFE6',ga=.7),'read aloud · the herd at the river')
# 18 two signals: leopard eye
a=grade(F(L('leopard'),(.5,.5),1.0),sat=1.05,soft=1.2,bloom=.2,grain=7); put(18,big(a,['THE TWO','SIGNALS.'],'#E6D4F8',150,glow='#9C7BE0',ga=.6),'carousel · two signals · leopard placeholder')
# 19 dome: carnelian on olive watercolour
st=L('mum35',(33,333,767,933)); m=cutout(st); bg=grade(earth('art95',OLV,.75,(.5,.5),1.25),sat=1.05,bloom=.15,soft=.4,grain=6)
put(19,big(obj_on(bg,st,m,700,540,560,shadow=.55,sheen=.12),['the dome holds','pressure off the','life beneath it.'],'#F1E9D6',80,y=960,shadow=.45),'VO · the dome')
# 20 correction ink
put(20,dots(hand(paper_bg('#F2EEE8'),.8,600),830,1060,7,24,5),'correction · founder mode → regulated mode · ink (handwrite)')
# 21 BF week: lilac street, big coral
a=grade(F(L('faye51'),(.5,.35)),sat=1.1); put(21,big(a,['BLACK FRIDAY','WEEK.','YOUR TEAM IS','ALREADY','READING YOU.'],'#FF7A66',128,glow='#FFB3A3',ga=.55,shadow=.35),'VO · black friday week')
os.makedirs('g60/final',exist_ok=True)
for i,t in enumerate(T): Image.fromarray(t.astype(np.uint8)).save(f'g60/final/{i+1:02d}.jpg',quality=92)
json.dump(LB,open('g60/final_labels.json','w'))
