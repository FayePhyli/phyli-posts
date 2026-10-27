exec(open('g60/personal.py').read())
N={}
a=grade(F(L('mum12'),(.5,.5),1.2),sat=1.25,bloom=.3); N['door']=txt(a,['forty messages','before 9am.'],'#F4EFE6',72,y=1060)
N['stairs']=txt(grade(F(L('faye33'),(.5,.55)),warm=.04),['posture.'],IV,84,y=170)
a=grade(F(L('art30'),(.5,.45),1.05),sat=.85,lift=14); lum=a.mean(2,keepdims=True)/255; N['silver']=grade(a*.5+(hx('#5E5A66')*(1-lum)+hx('#F1EEEA')*lum)*.5,bloom=.35,soft=.3,grain=5)
o,m=rgba('abalone'); N['dome2']=txt(obj_on(tex('mum0',MAU,.8),o,m,780,540,560,shadow=.6,sheen=.45),['the second dome.'],IV,66,y=1090,shadow=.4,spark=3,seed=2)
N['wolf']=grade(F(L('art73'),(.5,.35),1.05),warm=.03,tint='#E9DCC8',ta=.05)
a=grade(F(L('art84'),(.08,.5),1.0),sat=1.0,bloom=.25); N['tiger']=txt(place(a,ink_alpha_img('art76'),.62,560,640,IV,.95),['parasitism.'],IV,70,y=1120)
am=L('mum36',(39,615,786,1176)); m=cutout(am); N['amethyst']=txt(obj_on(tex('mum0',CHO,.78),am,m,780,540,600,shadow=.6,sheen=.3),['how to','keep winter.'],LI,66,y=1060,shadow=.4,spark=3,seed=9)
P=PT
src_=load(S+'art22.jpg'); M=np.clip((src_.mean(2)/255-.25)/.5,0,1); hh,ww=M.shape; sc=min(820/ww,820/hh); M=cv2.resize(M,(int(ww*sc),int(hh*sc)))
bg=tex('mum0',CHO,.85,(.3,.6),1.4); Pi=iri_map(TH,TW,t=.7,seed=9,scale=1.5)*0.8+255*0.2; MM=np.zeros((TH,TW)); y0=110; x0=(TW-M.shape[1])//2; MM[y0:y0+M.shape[0],x0:x0+M.shape[1]]=M
sh=cv2.GaussianBlur(np.roll(MM,(30,12),(0,1)),(0,0),25)*.45; bg=bg*(1-sh[...,None]); a=grade(bg*(1-MM[...,None])+Pi*MM[...,None],bloom=.35,soft=.4,grain=4)
N['poppy']=txt(a,['planting','in the dark.'],IV,70,y=1080,shadow=.4,spark=3,seed=1)
seq=[(1,'IX · carrying'),(3,'IX · read aloud: the skeleton (collab)'),('door','IX · forty messages'),(4,'IX · compensating'),(5,'IX · work flows'),(6,'IX · correction'),(7,'IX · black friday'),(8,'IX · crutch test'),('stairs','IX · read aloud: posture'),(10,'IX · one skeleton'),(11,'IX · rhythm'),('silver','IX · studio: silver, bone, ink'),
 (14,'VIII · hold your face'),(16,'VIII · read aloud: the herd (collab)'),(15,'VIII · 82%'),(17,'VIII · two signals'),(18,'VIII · the dome'),(20,'VIII · reading you'),(19,'VIII · correction'),(21,'VIII · keystone'),('dome2','VIII · read aloud: second dome'),(23,'VIII · the hive'),(24,'VIII · good luck today'),(25,'VIII · week after'),
 (27,'X · flowing one way'),(29,'X · read aloud: changed its kind (collab)'),(28,'X · who is fed'),(30,'X · not a priority'),(31,'X · all the way down'),(32,'X · correction'),(33,'X · repair'),('wolf','X · relationship audit'),('tiger','X · read aloud: parasitism'),(36,'X · hiring your friend'),(37,'X · the bee'),(38,'X · studio: green and umber'),
 (40,'XII · freezing'),(42,'XII · read aloud: what winter does (collab)'),(41,'XII · still (handwrite)'),('amethyst','XII · how to keep winter'),(44,'XII · revelation'),(46,'XII · longest night'),(45,'XII · correction'),(47,'XII · still (handwrite)'),('poppy','XII · read aloud: planting in the dark'),(49,'XII · closed for winter'),(50,'XII · boxing day'),(51,"XII · don't rush the spring")]
os.makedirs('g60/p2',exist_ok=True); labs=[]
for i,(k,l) in enumerate(seq):
    t=N[k] if isinstance(k,str) else P[k]
    Image.fromarray(np.clip(np.nan_to_num(t),0,255).astype(np.uint8)).save(f'g60/p2/{i+1:02d}.jpg',quality=90); labs.append(l)
json.dump(labs,open('g60/p2_labels.json','w'))
