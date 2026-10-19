import math
from PIL import Image, ImageDraw, ImageFont
import icons
from icons import S, layer, rr, ci, poly, thick
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def fit(im,W,target=70,cx=56,cy=56):
    """recorta a mascara, ajusta ao tamanho alvo (grade 112) e centraliza"""
    bb=im.getbbox(); c=im.crop(bb); w,h=c.size
    k=target*S/max(w,h); c=c.resize((max(1,int(w*k)),max(1,int(h*k))),Image.LANCZOS)
    out=Image.new('L',(W,W),0); out.paste(c,(int(cx*S-c.width/2),int(cy*S-c.height/2)))
    return out
def arc_pts(c,R,a0,a1,step=3):
    return [(c[0]+R*math.cos(math.radians(a)),c[1]+R*math.sin(math.radians(a))) for a in range(a0,a1+1,step)]
def g_phone2(W):
    """fone de telefone: mascara extraida da imagem de referencia enviada pelo usuario (ref_phone_mask.png)"""
    import os
    from PIL import ImageFilter
    m=Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ref_phone_mask.png')).convert('L')
    m=m.filter(ImageFilter.GaussianBlur(1.5))
    bb=m.getbbox(); m=m.crop(bb)
    return fit(m.resize((W,int(W*m.height/m.width)),Image.LANCZOS) if False else _pad(m,W),W,72)
def _pad(m,W):
    out=Image.new('L',(W,W),0); k=W*0.9/max(m.size); mm=m.resize((int(m.width*k),int(m.height*k)),Image.LANCZOS)
    out.paste(mm,((W-mm.width)//2,(W-mm.height)//2)); return out
def g_fm2(W):
    im,d=layer(W)
    cx,cy=56,34
    ci(d,(cx,cy),8,255)
    for R,wd in ((22,7),(37,7)):
        for a0,a1 in ((-52,52),(128,232)):
            thick(d,arc_pts((cx,cy),R,a0,a1,2),wd)
    f=ImageFont.truetype(FB,int(46*S))
    bb=d.textbbox((0,0),'FM',font=f)
    d.text((cx*S-(bb[0]+bb[2])/2,78*S-bb[1]),'FM',font=f,fill=255)
    return fit(im,W,76)
def g_camera2(W):
    im,d=layer(W)
    rr(d,(14,32,98,88),14,255); rr(d,(36,20,76,40),8,255)
    ci(d,(56,60),21,0); ci(d,(56,60),15,255); ci(d,(56,60),8,0)
    ci(d,(84,44),4,0)
    return fit(im,W,74)

def g_radio(W):
    """radio retro: corpo, alto-falante, mostrador e antena"""
    im,d=layer(W)
    rr(d,(12,38,100,92),12,255)
    thick(d,[(30,38),(78,16)],5)
    ci(d,(36,65),15,0); ci(d,(36,65),9,255); ci(d,(36,65),4,0)
    for y in (52,62,72):
        rr(d,(60,y-2,90,y+2),2,0)
    ci(d,(80,80),4,0)
    return fit(im,W,78)
def wrap(g,t=74):
    return lambda W: fit(g(W),W,t)

def g_usb2(W):
    """simbolo USB (tridente): haste, circulo na base, ponta de seta, ramo com circulo e ramo com quadrado"""
    im,d=layer(W)
    thick(d,[(30,64),(78,64)],0.01) if False else None
    # haste principal
    thick(d,[(30,58),(82,58)],6)
    ci(d,(22,58),9,255)                       # circulo na base
    poly(d,[(82,46),(82,70),(100,58)],255)    # ponta de seta
    thick(d,[(46,58),(58,36),(70,36)],5); rr(d,(68,29,82,43),2,255)    # ramo superior com quadrado
    thick(d,[(58,58),(68,80),(76,80)],5); ci(d,(80,80),7,255)          # ramo inferior com circulo
    return fit(im,W,76)
def g_link2(W):
    """espelhamento: tela larga ao fundo e celular na frente"""
    im,d=layer(W)
    rr(d,(8,22,104,84),10,255); rr(d,(14,28,98,78),5,0)          # tela
    rr(d,(34,88,78,94),3,255); rr(d,(50,82,62,90),0,255)         # base da tela
    rr(d,(52,40,98,104),11,0); rr(d,(56,44,94,100),9,255)        # celular (recorte + corpo)
    rr(d,(68,48,82,51),1,0)                                      # alto-falante
    return fit(im,W,74)
