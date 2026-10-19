import numpy as np, math
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import distance_transform_edt as edt
import icons, glyphs2
from icons import S, superellipse, gradient

# ---- paleta (estilo iOS/CarPlay escuro) ----
C={'blue':((64,156,255),(0,98,230)),'orange':((255,184,64),(255,120,10)),'teal':((84,220,232),(14,140,170)),
   'pink':((255,112,140),(222,28,84)),'green':((92,226,120),(30,168,70)),'red':((255,110,100),(228,40,50)),
   'gray':((176,176,186),(84,84,94)),'purple':((200,140,255),(124,70,226)),'cyan':((90,200,255),(10,110,225))}
C.update({'orange':((255,176,70),(236,92,18)),'pink':((255,98,206),(214,26,138)),'green':((104,236,136),(26,166,88)),'blue':((86,150,255),(24,72,226)),'red':((255,112,104),(226,40,56)),'gray':((124,124,132),(50,50,58)),'purple':((196,88,236),(112,30,188)),'teal':((78,226,214),(10,140,160)),'cyan':((96,206,255),(14,112,230))})
ACCENT={k:v[0] for k,v in C.items()}

def squircle(top,bot,glyph,size):
    """icone arredondado refinado, retorna RGBA size x size (supersampled internamente)"""
    n=5.0; W=112*S
    y,x=np.mgrid[0:W,0:W].astype(float)
    base=gradient(W,W,top,bot,diag=0.08)
    mask=superellipse(W,W,n); m=mask>0
    dist=edt(np.pad(m,1))[1:-1,1:-1]
    # luz superior suave + sombra interna inferior
    gl=np.clip(1-(y/(W*0.55)),0,1)**1.8*0.20
    rgb=base+(255-base)*gl[...,None]
    sh=np.clip((y/W-0.62)/0.38,0,1)**1.4*0.20
    rgb=rgb*(1-sh[...,None])
    # filete interno claro (1px) mais forte no topo
    rim=((dist<1.4*S)&m).astype(float)*np.clip(0.50-0.42*(y/W),0.05,0.50)
    rgb=rgb+(255-rgb)*rim[...,None]
    g=glyph(W); ga=np.array(g).astype(float)/255
    gsh=np.array(g.filter(ImageFilter.GaussianBlur(2.2*S))).astype(float)/255*0.28
    gsh=np.roll(gsh,int(2*S),axis=0)
    rgb=rgb*(1-gsh[...,None])
    # glifo branco com leve degrade (topo 100%, base 93%)
    gv=255-(y/W)*14
    rgb=rgb*(1-ga[...,None])+gv[...,None]*ga[...,None]
    im=Image.fromarray(np.dstack([np.clip(rgb,0,255),mask]).astype('uint8'),'RGBA')
    return im.resize((size,size),Image.LANCZOS)

def shadow_under(im,canvas_size,pos,blur,dy,alpha):
    sh=Image.new('L',canvas_size,0); sh.paste(im.split()[3],(pos[0],pos[1]+dy))
    sh=sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v:int(v*alpha))
    k=Image.new('RGBA',canvas_size,(0,0,0,255)); k.putalpha(sh); return k

def small_icon(key,glyph,selected=False,W=170,H=120,size=100):
    top,bot=C[key]; ic=squircle(top,bot,glyph,size*S//S) 
    ic=squircle(top,bot,glyph,size)
    cv=Image.new('RGBA',(W,H),(0,0,0,0)); pos=((W-size)//2,3)
    cv=Image.alpha_composite(cv,shadow_under(ic,(W,H),pos,5,4,0.55))
    if selected:
        # anel + brilho na cor do icone
        ring=Image.new('L',(W*S,H*S),0); d=ImageDraw.Draw(ring)
        x0,y0=pos[0]*S,pos[1]*S; pad=6*S
        d.rounded_rectangle([x0-pad,y0-pad,x0+size*S+pad,y0+size*S+pad],radius=int(26*S),outline=255,width=int(2.6*S))
        glow=ring.filter(ImageFilter.GaussianBlur(5*S)).point(lambda v:min(255,int(v*1.4)))
        ring=ring.resize((W,H),Image.LANCZOS); glow=glow.resize((W,H),Image.LANCZOS)
        gcol=Image.new('RGBA',(W,H),ACCENT[key]+(255,)); gcol.putalpha(glow.point(lambda v:int(v*0.8)))
        rcol=Image.new('RGBA',(W,H),(255,255,255,255)); rcol.putalpha(ring)
        cv=Image.alpha_composite(cv,gcol); cv=Image.alpha_composite(cv,rcol)
    cv.alpha_composite(ic,pos)
    return cv

def tile(key,glyph,w=204,h=300,radius=30,isize=116,cy=0.40,selected=False):
    top,bot=C[key]; W,H=w*S,h*S
    y,x=np.mgrid[0:H,0:W].astype(float)
    c0=np.array([32,32,40],float); c1=np.array([32,32,40],float)
    t=np.clip(y/(H-1),0,1)[...,None]; rgb=c0*(1-t)+c1*t
    cx,cyp=W/2,H*cy
    dd=np.sqrt(((x-cx)/(W*0.62))**2+((y-cyp)/(H*0.36))**2)
    glow=np.clip(1-dd,0,1)**2*(0.0 if not selected else 0.0)
    rgb=rgb*(1-glow[...,None])+np.array(top,float)*glow[...,None]*0.9
    mk=Image.new('L',(W,H),0); ImageDraw.Draw(mk).rounded_rectangle([0,0,W-1,H-1],radius=radius*S,fill=255)
    mask=np.array(mk); dist=edt(np.pad(mask>0,1))[1:-1,1:-1]
    rim=((dist<1.5*S)&(mask>0)).astype(float)
    rgb=rgb*(1-rim[...,None])+np.array([72,72,86],float)*rim[...,None]
    if selected:
        ring=((dist<3.0*S)&(mask>0)).astype(float)
        rgb=rgb*(1-ring[...,None])+np.array(top,float)*ring[...,None]
    base=Image.fromarray(np.dstack([np.clip(rgb,0,255),mask]).astype('uint8'),'RGBA')
    ic=squircle(top,bot,glyph,isize*S)
    pos=(int((W-isize*S)/2),int(H*cy-isize*S/2))
    base=Image.alpha_composite(base,shadow_under(ic,(W,H),pos,9*S,6*S,0.55))
    base.alpha_composite(ic,pos)
    return base.resize((w,h),Image.LANCZOS)

# ---------- glifos extras ----------
_w=glyphs2.wrap
GL=dict(globe=icons.g_globe,fm=glyphs2.g_radio,link=glyphs2.g_link2,btm=_w(icons.g_headset),phone=glyphs2.g_phone2)
SMALL={ # indice normal -> (cor, glifo)
 4:('red',glyphs2.g_usb2),6:('blue',_w(icons.g_sd)),8:('gray',glyphs2.g_camera2),10:('orange',_w(icons.g_clock)),
 12:('purple',_w(icons.g_eq)),14:('teal',_w(icons.g_photo)),18:('green',glyphs2.g_link2),20:('cyan',_w(icons.g_dashcam)),
 22:('pink',_w(icons.g_btmusic)),24:('gray',_w(icons.g_gear))}
TILES={0:('blue','globe',dict(isize=72,cy=0.19)),2:('orange','fm',dict(w=205,h=301)),26:('teal','link',{}),28:('pink','btm',{}),30:('green','phone',{})}

def build_file14():
    out={}
    for i,(c,g,kw) in TILES.items():
        for s in (0,1):
            im=tile(c,GL[g],selected=bool(s),**kw)
            out[i+s]=im
    for i,(c,g) in SMALL.items():
        for s in (0,1): out[i+s]=small_icon(c,g,bool(s))
    # calendario (16/17)
    for s in (0,1):
        cal=icons.calendar_icon(100)
        cv=Image.new('RGBA',(170,120),(0,0,0,0)); pos=(35,3)
        cv=Image.alpha_composite(cv,shadow_under(cal,(170,120),pos,5,4,0.55)); cv.alpha_composite(cal,pos)
        if s:
            ring=Image.new('L',(170*S,120*S),0); d=ImageDraw.Draw(ring)
            d.rounded_rectangle([(35-6)*S,(3-6)*S,(35+100+6)*S,(3+100+6)*S],radius=26*S,outline=255,width=int(2.6*S))
            gl=ring.filter(ImageFilter.GaussianBlur(5*S)).point(lambda v:min(255,int(v*1.4))).resize((170,120),Image.LANCZOS)
            r=ring.resize((170,120),Image.LANCZOS)
            g1=Image.new('RGBA',(170,120),(255,90,90,255)); g1.putalpha(gl.point(lambda v:int(v*.8)))
            w1=Image.new('RGBA',(170,120),(255,255,255,255)); w1.putalpha(r)
            base=Image.alpha_composite(Image.new('RGBA',(170,120),(0,0,0,0)),g1); base=Image.alpha_composite(base,w1)
            base=Image.alpha_composite(base,shadow_under(cal,(170,120),pos,5,4,0.55)); base.alpha_composite(cal,pos); cv=base
        out[16+s]=cv
    return out
if __name__=='__main__':
    o=build_file14()
    sh=Image.new('RGB',(1300,640),(10,10,14)); x=10
    for i in (0,1,2,3,26,27,28,29,30,31):
        im=o[i]; sh.paste(im,(10+(x//1 if False else 0)+ [0,1,2,3,26,27,28,29,30,31].index(i)*125,10),im) if False else None
    xs=10
    for i in (0,2,26,28,30,1,3,27,29,31):
        im=o[i].resize((o[i].width*5//8,o[i].height*5//8)); sh.paste(im,(xs,10+(0 if i in (0,2,26,28,30) else 200)),im); xs+=130 if i!=1 else 130
        if i==30: xs=10
    xs=10
    for k,i in enumerate((4,6,8,10,12,14,16,18,20,22,24)):
        sh.paste(o[i],(10+(k%7)*185,420+(k//7)*110-0),o[i])
    sh.save('ex/dark_sheet.png'); print('ok')
