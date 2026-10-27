src=open('g60/final.py').read(); exec(src[:src.index("# 1 marker IX")])
exec(src[src.index("BPK="):].split(";")[0]) if False else None
BPK=['#9A5A72','#D395A6','#F0C2CD','#F9DEE5','#FEF2F5']; PL='#7A3A58'
T=[None]*21; LB=[None]*21
def put(k,a,lab): T[42-k]=np.clip(np.nan_to_num(a),0,255); LB[42-k]=f'{k}. {lab}'
def marker(v,sub):
    p=paper_bg('#F3EFE8'); p=fit_place(p,snip(v),980,420,540,620); return caps(p,sub,1180,'#3A2A36')
# 22 keystone: sunglasses
a=grade(F(L('faye39'),(.5,.35)),sat=1.1,bloom=.25); put(22,big(a,['SPOT THE','KEYSTONE.'],'#E6D4F8',150,y=900,glow='#9C7BE0',ga=.6,spark=4,seed=22),'carousel · spot the keystone')
# 23 RA second dome: pastel swirl
a=grade(F(L('p03',(150,520,1800,1800)),(.5,.5),1.0),sat=1.25,lift=8,bloom=.15); a=caps(a,'read aloud · volume viii',1040,PL); put(23,big(a,['the second dome.'],PL,84,y=1090,shadow=0,glow='#FFF4F6',ga=.6,spark=3,seed=23),'read aloud · the second dome · your pastel')
# 24 hive: pink dot flower on black
a=grade(F(L('art22'),(.5,.45),1.15),sat=1.1,bloom=.3); put(24,big(a,["the hive doesn't","have a thermostat.","it has everyone."],'#3A1630',84,y=990,shadow=0,glow='#FFF6F8',ga=.9,spark=4,seed=24),'silent · the hive')
# 25 good luck: halter on blue sky
a=grade(F(L('faye77',(0,110,923,1900)),(.5,.4)),sat=1.1,bloom=.25); put(25,big(a,['GOOD LUCK','TODAY.'],'#FF7A66',150,y=150,glow='#FFB3A3',ga=.55,shadow=.35),'studio · black friday · good luck today')
# 26 week after: iridescent rose
a=grade(F(L('art3'),(.5,.5),1.05),sat=1.05,lift=10,bloom=.25); put(26,big(a,['the week after','the launch needs','a plan too.'],PL,84,y=980,shadow=0,glow='#FFF4F6',ga=.65,spark=3,seed=26),'VO · the week after')
# 27 X marker
put(27,marker('X','volume x · relationships · symbiosis'),'X marker · collab · ink (your design)')
# 28 feed you both: pink shirt selfie
a=grade(F(L('faye1'),(.5,.3)),warm=.02,bloom=.25); put(28,big(a,['it used to feed you both.','when did it start','flowing one way?'],IV,70,y=1020,glow='#C2607E',ga=.45),'VO · it used to feed you both')
# 29 who is being fed: flower
a=grade(F(L('art2'),(.55,.5),1.1),sat=1.05,bloom=.2,lift=6); put(29,big(a,['WHO IS','BEING FED,','AND AT','WHOSE COST?'],'#5A2550',140,shadow=0,glow='#FFFFFF',ga=1.0,spark=3,seed=29),'carousel · who is being fed')
# 30 RA changed its kind: pink scratch painting
a=grade(F(L('art91'),(.5,.5),1.0),sat=1.1,lift=10,bloom=.2); a=caps(a,'read aloud · volume x',1040,IV); put(30,big(a,['the relationship','that changed its kind.'],IV,76,y=1090,glow='#7A3A58',ga=.55),'read aloud · the relationship that changed its kind')
# 31 not a priority: 82%-style ink
p=fit_place(paper_bg('#F3EFE8'),ink_alpha_img('art66'),620,420,540,330)
p=big(p,['“YOU’RE NOT','A PRIORITY AS','A SMALL BRAND.”'],AUB,96,y=620,shadow=0); put(31,big(p,['said a manufacturer, to a founder, in 2026.'],AUB,40,y=1010,shadow=0),'silent · not a priority · ink')
# 32 relationships all the way down: coral blossom tree
a=grade(F(L('art24'),(.5,.5),1.0),sat=1.05,bloom=.35); put(32,big(a,['THE ORGANISATION','IS RELATIONSHIPS,','ALL THE WAY DOWN.'],'#FBE3E8',92,y=1010,glow='#1E0E18',ga=.85,shadow=.7,spark=4,seed=32),'VO · all the way down')
# 33 correction ink
put(33,dots(hand(paper_bg('#F2EEE8'),.8,600),250,1060,7,24,33),"correction · we're a family → a mutual arrangement, on purpose · ink (handwrite)")
# 34 repair: pastel crack close-up
a=grade(F(L('p05'),(.45,.5),1.0),sat=1.2,lift=6,bloom=.15); put(34,big(a,['AFTER PEAK,','THE TEAM','DOESN’T NEED','A PARTY.','IT NEEDS','REPAIR.'],PL,130,lh=1.12,shadow=0,glow='#FFF4F6',ga=.6,spark=4,seed=34),'VO · it needs repair · your pastel')
# 35 audit: cream-pink flower close-up
a=grade(F(L('art30'),(.5,.45),1.0),sat=1.05,bloom=.25); put(35,big(a,['THE RELATIONSHIP','AUDIT BEFORE','CHRISTMAS.'],IV,96,y=990,glow='#2A0E1E',ga=.85,shadow=.7),'carousel · the relationship audit')
# 36 RA parasitism: coral painting
a=grade(F(L('art84'),(.35,.5),1.05),sat=1.0,bloom=.25,lift=4); a=caps(a,'read aloud · volume x',1040,IV); put(36,big(a,['parasitism.'],IV,96,y=1090,glow='#7A3A58',ga=.5),'read aloud · parasitism')
# 37 hiring your friend: beads selfie
a=grade(F(L('faye104'),(.5,.25)),warm=.02,bloom=.2); put(37,big(a,['hiring your friend','changed the biology.'],'#F7D9E6',76,y=1070,glow='#B48CF0',ga=.5,spark=3,seed=37),'talking (optional) · hiring your friend')
# 38 bee: deep pink flower
a=grade(F(L('art11'),(.5,.5),1.1),sat=1.05,bloom=.3); put(38,big(a,['THE BEE IS NOT','HELPING THE FLOWER.','THE BEE IS','BEING FED.'],'#FBF3F0',100,glow='#5A2550',ga=.6,shadow=.5),'silent · the bee is being fed')
# 39 from the studio: room with paintings (no title)
put(39,grade(F(L('mum3'),(.5,.6)),sat=1.05,bloom=.3,lift=4),'from the studio (no title)')
# 40 XII marker
put(40,marker('XII','volume xii · rest · winter'),'XII marker · collab · ink (your design)')
# 41 freezing: pastel bands
a=grade(F(L('p10'),(.5,.6),1.45),sat=1.2,lift=6); put(41,big(a,['if you stop and feel','no better, you may','not be resting.','you may be freezing.'],PL,72,y=1000,shadow=0,glow='#FFF4F6',ga=.65,spark=3,seed=41),'VO · you may be freezing · your pastel')
# 42 freeze: light ink on dark paper
p=paper_bg('#F3EFE8')*(hx('#2E1F2C')/hx('#F3EFE8')); p=fit_place(p,ink_alpha_img('art54'),520,620,540,470,'#E9DDEB',.9)
put(42,big(p,['freeze looks like rest','and restores nothing.'],'#F3E9F2',66,y=1020,shadow=0,glow='#B996F0',ga=.35),'still · freeze · light ink on dark paper (handwrite)')
os.makedirs('g60/next',exist_ok=True)
for i,t in enumerate(T): Image.fromarray(t.astype(np.uint8)).save(f'g60/next/{i+1:02d}.jpg',quality=92)
json.dump(LB,open('g60/next_labels.json','w'))
