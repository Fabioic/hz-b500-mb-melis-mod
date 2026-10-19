import numpy as np, math
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import distance_transform_edt as edt
S=8
BLUE=(10,132,255)
def canvas(w,h): return Image.new('RGBA',(w*S,h*S),(0,0,0,0))
def fin(im,w,h): return im.resize((w,h),Image.LANCZOS)
def circle(d,cx,cy,r,fill=None,wd=0,outline=None):
    d.ellipse([(cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r)*S],fill=fill,outline=outline,width=int(wd*S))
def ball(active):
    w=h=60; W=w*S
    y,x=np.mgrid[0:W,0:W].astype(float)
    r=np.sqrt((x-W/2)**2+(y-W/2)**2)/S
    m=r<=27.5
    col=np.zeros((W,W,3)); col[:]=(32,32,40)
    rim=(r>25.9)&m
    col[rim]=BLUE if active else (192,192,204)
    a=np.where(m,236,0).astype(float)
    im=Image.fromarray(np.dstack([col,a]).astype('uint8'),'RGBA')
    cc=Image.new('RGBA',(W,W),(0,0,0,0)); dd=ImageDraw.Draw(cc)
    dd.ellipse([(30-12.5)*S,(30-12.5)*S,(30+12.5)*S,(30+12.5)*S],fill=(255,255,255,255) if active else (240,240,248,255))
    im=Image.alpha_composite(im,cc)
    return fin(im,w,h)
def panel():
    w,h=400,240; W,H=w*S,h*S
    mk=Image.new('L',(W,H),0); ImageDraw.Draw(mk).rounded_rectangle([0,0,W-1,H-1],radius=38*S,fill=255)
    m=np.array(mk)>0; dist=edt(np.pad(m,1))[1:-1,1:-1]
    col=np.zeros((H,W,3)); col[:]=(24,24,32)
    col[(dist<1.6*S)&m]=(88,88,104)
    a=np.where(m,226,0).astype(float)
    return fin(Image.fromarray(np.dstack([col,a]).astype('uint8'),'RGBA'),w,h)
def disc(d,on):
    if on: circle(d,27,27,26,BLUE+(110,))
def stroke(d,pts,wd,col=(255,255,255,255),closed=False):
    P=[(x*S,y*S) for x,y in pts]
    d.line(P+([P[0]] if closed else []),fill=col,width=int(wd*S),joint='curve')
    for x,y in P: circle(d,x/S,y/S,wd/2,col)
def icon_vol(muted,on):
    im=canvas(54,54); d=ImageDraw.Draw(im); disc(d,on); W=(255,255,255,255)
    d.polygon([(13*S,22*S),(20*S,22*S),(29*S,14*S),(29*S,40*S),(20*S,32*S),(13*S,32*S)],fill=W)
    d.rounded_rectangle([13*S,22*S,20*S,32*S],radius=2*S,fill=W)
    if not muted:
        for r in (7,12): d.arc([(30-r+1)*S,(27-r)*S,(30+r+1)*S,(27+r)*S],-50,50,fill=W,width=int(2.6*S))
    else:
        stroke(d,[(34,21),(44,33)],2.8); stroke(d,[(44,21),(34,33)],2.8)
    return fin(im,54,54)
def icon_home(on):
    im=canvas(54,54); d=ImageDraw.Draw(im); disc(d,on)
    stroke(d,[(14,25),(27,13),(40,25),(40,40),(14,40)],3.0,closed=True); stroke(d,[(23,34),(31,34)],3.0)
    return fin(im,54,54)
def icon_pow(on):
    im=canvas(54,54); d=ImageDraw.Draw(im); disc(d,on); W=(255,255,255,255)
    d.arc([14*S,14*S,40*S,40*S],-50,230,fill=W,width=int(3.0*S))
    for a in (-50,230):
        t=math.radians(a); circle(d,27+13*math.cos(t),27+13*math.sin(t),1.5,W)
    stroke(d,[(27,11),(27,26)],3.0)
    return fin(im,54,54)
def track(fill):
    w,h=320,26; im=canvas(w,h); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,w*S-1,h*S-1],radius=13*S,fill=(255,255,255,235) if fill else (130,130,142,95))
    return fin(im,w,h)
def thumb():
    im=canvas(26,26); d=ImageDraw.Draw(im); circle(d,13,13,12.5,(255,255,255,255)); return fin(im,26,26)
def roles(): return {-2:ball(True),-1:ball(False),0:panel(),1:icon_vol(False,False),2:icon_vol(True,True),3:icon_home(False),4:icon_home(True),5:icon_pow(False),6:icon_pow(True),7:track(False),8:track(True),9:thumb()}
if __name__=='__main__':
    R=roles(); sh=Image.new('RGB',(900,320),(20,70,110))
    sh.paste(R[0],(20,20),R[0]); x=440
    for k in (-2,-1,1,2,3,4,5,6): sh.paste(R[k],(x,20+ (60 if k in(-2,-1) else 0)) if False else (x,20),R[k]); x+=60
    sh.paste(R[7],(20,270),R[7]); sh.save('ex/dark_ball.png')
