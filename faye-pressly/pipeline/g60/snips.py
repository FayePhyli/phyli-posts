import numpy as np, cv2
from PIL import Image
def _A(n): return np.asarray(Image.open(f'mock/ink/{n}.png'))[...,3]/255.
def _bb(A,pad=8):
    ys,xs=np.where(A>.25); return A[max(ys.min()-pad,0):ys.max()+pad,max(xs.min()-pad,0):xs.max()+pad]
def _rows(A,gap=4,minh=8):
    r=cv2.GaussianBlur((A>.3).astype(np.float32),(0,0),2).max(1)>0.05; out=[];s=None
    for y,v in enumerate(list(r)+[False]):
        if v and s is None: s=y
        if not v and s is not None:
            if y-s>minh: out.append(A[s:y])
            s=None
    return out
LG=_A('larger'); WG=_A('watchgrow'); CR=_A('correction'); VO=_A('volumes')
SN={}
SN['build']=_bb(LG[837:1009]); SN['larger']=_bb(LG[1311:1503])
SN['intercourse']=_bb(WG[221:393]); SN['watch']=_bb(WG[840:1322])
g=CR[1638:1861]; SN['growth']=_bb(g[:, :int(g.shape[1]*.80)])
b18=VO[1182:1252]; SN['pack']=_bb(b18[:, int(b18.shape[1]*.42):])
SN['IX']=_bb(VO[1623:1679])
a=_bb(VO[1476:1613]); SN['VIII']=_bb(a[a.shape[0]//2+4:])
a=_bb(VO[1681:1884]); h=a.shape[0]; SN['X']=_bb(a[:int(h*.36)]); SN['XII']=_bb(a[int(h*.68):])
def snip(k,dark=False):
    A=SN[k]; A=np.clip((A-.15)/.6,0,1); return A
