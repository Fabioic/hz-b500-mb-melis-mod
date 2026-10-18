# Gerador dos icones estilo iOS (vidro) usados nos testes. Requer numpy + Pillow. Arte original deste projeto (MIT).
import numpy as np, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
S=4; B=112   # lado do icone base
FONT='/usr/share/fonts/opentype/inter/Inter-Bold.otf'
import os
if not os.path.exists(FONT): FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def superellipse(w,h,n=5.0,inset=0):
    y,x=np.mgrid[0:h,0:w].astype(float)
    a=(w-1)/2-inset*S; b=(h-1)/2-inset*S
    v=(np.abs((x-(w-1)/2)/a)**n+np.abs((y-(h-1)/2)/b)**n)
    return (v<=1).astype(np.uint8)*255

def gradient(w,h,top,bot,diag=0.15):
    y,x=np.mgrid[0:h,0:w].astype(float)
    t=np.clip(y/(h-1)*(1-diag)+x/(w-1)*diag,0,1)[...,None]
    c=np.array(top,float)*(1-t)+np.array(bot,float)*t
    return c

def glass_icon(top,bot,glyph,size=B,n=5.0):
    W=size*S
    base=gradient(W,W,top,bot)
    mask=superellipse(W,W,n)
    # brilho de vidro: elipse clara no topo
    y,x=np.mgrid[0:W,0:W].astype(float)
    gl=np.clip(1-(y/(W*0.58)),0,1)**1.6*0.34
    gl*= (superellipse(W,W,n,inset=3)>0)
    # luz de borda (rim): diferenca entre mascara e mascara menor
    inner=superellipse(W,W,n,inset=2.2)
    rim=((mask>0)&(inner==0)).astype(float)
    rimv=rim*np.clip(0.75-0.55*(y/W),0.15,0.75)
    # sombra interna inferior
    sh=np.clip((y/W-0.62)/0.38,0,1)**1.5*0.16
    rgb=base*(1-sh[...,None])
    rgb=rgb+(255-rgb)*gl[...,None]
    rgb=rgb+(255-rgb)*rimv[...,None]
    # glifo
    g=glyph(W) if callable(glyph) else glyph
    ga=np.array(g).astype(float)/255
    # sombra do glifo
    sa=np.array(Image.fromarray((ga*255).astype('uint8')).filter(ImageFilter.GaussianBlur(3*S)))/255*0.28
    sa=np.roll(sa,int(2.5*S),axis=0)
    rgb=rgb*(1-sa[...,None])
    rgb=rgb*(1-ga[...,None])+255*ga[...,None]
    out=np.dstack([np.clip(rgb,0,255),mask]).astype('uint8')
    im=Image.fromarray(out,'RGBA').resize((size,size),Image.LANCZOS)
    return im

# ---------- glifos (mascaras L, 255=branco) em grade 112*S ----------
def layer(W): 
    im=Image.new('L',(W,W),0); return im,ImageDraw.Draw(im)
def rr(d,box,r,fill):  # retangulo arredondado, coordenadas na grade 112
    s=lambda v:v*S
    d.rounded_rectangle([s(box[0]),s(box[1]),s(box[2]),s(box[3])],radius=r*S,fill=fill)
def ci(d,c,r,fill):
    d.ellipse([(c[0]-r)*S,(c[1]-r)*S,(c[0]+r)*S,(c[1]+r)*S],fill=fill)
def poly(d,pts,fill): d.polygon([(x*S,y*S) for x,y in pts],fill=fill)
def thick(d,pts,w,fill=255):
    for a,b in zip(pts,pts[1:]):
        d.line([(a[0]*S,a[1]*S),(b[0]*S,b[1]*S)],fill=fill,width=int(w*S))
    for p in pts: ci(d,p,w/2,fill)

def g_usb(W):
    im,d=layer(W)
    rr(d,(36,18,76,42),5,255); rr(d,(30,38,82,92),12,255)
    rr(d,(44,24,51,36),2,0); rr(d,(61,24,68,36),2,0)
    return im
def g_sd(W):
    im,d=layer(W)
    poly(d,[(32,30),(64,30),(80,46),(80,86),(32,86)],255)
    rr(d,(32,24,80,40),0,0)  # remove cantos de cima
    poly(d,[(34,26),(62,26),(78,42),(78,84),(34,84)],255)
    d.rectangle([32*S,24*S,80*S,26*S],fill=0)
    for x in (42,51,60): rr(d,(x,32,x+5,48),2,0)
    return im
def g_camera(W):
    im,d=layer(W)
    rr(d,(22,34,90,86),12,255); rr(d,(40,26,72,40),6,255)
    ci(d,(56,60),19,0); ci(d,(56,60),13,255); ci(d,(56,60),6,0)
    ci(d,(80,44),3,0)
    return im
def g_plug(W):
    im,d=layer(W)
    rr(d,(34,22,78,58),8,255)
    rr(d,(42,10,50,28),3,255); rr(d,(62,10,70,28),3,255)
    rr(d,(50,56,62,76),3,255)
    thick(d,[(56,74),(56,84),(70,92),(86,92)],8)
    return im
def g_clock(W):
    im,d=layer(W)
    ci(d,(56,56),37,255); ci(d,(56,56),29,0)
    thick(d,[(56,56),(56,38)],6); thick(d,[(56,56),(69,63)],6)
    return im
def g_eq(W):
    im,d=layer(W)
    for x,y in ((30,42),(56,70),(82,52)):
        rr(d,(x-4,22,x+4,90),4,120); rr(d,(x-4,y-9,x+4,90),4,120)
        ci(d,(x,y),11,255)
    return im
def g_photo(W):
    im,d=layer(W)
    rr(d,(22,26,90,86),11,255); rr(d,(28,32,84,80),6,0)
    ci(d,(66,46),6,255)
    poly(d,[(30,80),(46,56),(58,72),(66,62),(82,80)],255)
    return im
def g_multi(W):
    im,d=layer(W)
    rr(d,(22,22,70,70),9,255); rr(d,(28,28,64,64),5,0)
    rr(d,(36,36,96,96),12,0); rr(d,(42,42,90,90),9,255)
    return im
def g_dashcam(W):
    im,d=layer(W)
    ci(d,(56,46),28,255); poly(d,[(34,60),(78,60),(56,96)],255)
    rr(d,(42,38,60,54),3,0); poly(d,[(60,44),(70,38),(70,54)],0)
    return im
def g_btmusic(W):
    im,d=layer(W)
    d.ellipse([20*S,64*S,42*S,82*S],fill=255)
    rr(d,(37,26,43,74),2,255)
    poly(d,[(39,26),(60,34),(60,46),(39,40)],255)
    thick(d,[(70,38),(92,60),(81,71),(81,27),(92,38),(70,60)],5)
    return im
def g_gear(W):
    im,d=layer(W)
    ci(d,(56,56),28,255)
    for k in range(8):
        a=k*math.pi/4
        c,s=math.cos(a),math.sin(a)
        pts=[(56+c*20-s*8,56+s*20+c*8),(56+c*39-s*7,56+s*39+c*7),(56+c*39+s*7,56+s*39-c*7),(56+c*20+s*8,56+s*20-c*8)]
        poly(d,pts,255)
    ci(d,(56,56),12,0)
    return im
def g_globe(W):
    im,d=layer(W)
    ci(d,(56,56),38,255); ci(d,(56,56),32,0)
    d.ellipse([(56-15)*S,(56-32)*S,(56+15)*S,(56+32)*S],outline=255,width=5*S)
    d.line([(24*S,56*S),(88*S,56*S)],fill=255,width=5*S)
    d.line([(56*S,24*S),(56*S,88*S)],fill=255,width=4*S)
    return im
def g_tower(W):
    im,d=layer(W)
    ci(d,(56,40),7,255)
    thick(d,[(56,50),(40,92)],6); thick(d,[(56,50),(72,92)],6); thick(d,[(46,76),(66,76)],5)
    for r,wd in ((20,5),(32,5)):
        d.arc([(56-r)*S,(40-r)*S,(56+r)*S,(40+r)*S],200,340,fill=255,width=wd*S)
        d.arc([(56-r)*S,(40-r)*S,(56+r)*S,(40+r)*S],20,160,fill=0,width=0)
    # ondas laterais
    im2,d2=layer(W)
    for r in (20,33):
        for a0,a1 in ((200,250),(290,340)):
            d2.arc([(56-r)*S,(40-r)*S,(56+r)*S,(40+r)*S],a0-60,a1-60,fill=255,width=5*S)
    return im
def g_tower2(W):
    im,d=layer(W)
    ci(d,(56,38),7,255)
    thick(d,[(56,48),(41,90)],6); thick(d,[(56,48),(71,90)],6); thick(d,[(46,74),(66,74)],5)
    for r in (21,34):
        d.arc([(56-r)*S,(38-r)*S,(56+r)*S,(38+r)*S],140,220,fill=255,width=5*S)
        d.arc([(56-r)*S,(38-r)*S,(56+r)*S,(38+r)*S],320,400,fill=255,width=5*S)
    return im
def g_headset(W):
    im,d=layer(W)
    d.arc([22*S,22*S,90*S,90*S],180,360,fill=255,width=7*S)
    thick(d,[(25,58),(25,66)],7); thick(d,[(87,58),(87,66)],7)
    rr(d,(18,56,36,84),8,255); rr(d,(76,56,94,84),8,255)
    thick(d,[(52,50),(66,64),(59,71),(59,41),(66,48),(52,62)],0.01) if False else None
    thick(d,[(50,58),(64,72),(57,79),(57,45),(64,52),(50,66)],4.5,255)
    return im
def g_phone(W):
    im,d=layer(W)
    cx,cy,r=56,40,34
    arc=[(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a))) for a in range(40,141,4)]
    thick(d,arc,12)
    # bocais apontando para cima nas pontas
    for (ex,ey) in (arc[0],arc[-1]):
        rr(d,(ex-11,ey-24,ex+11,ey+6),6,255)
    im=im.rotate(-45,resample=Image.BICUBIC,center=(W/2,W/2*1.0+0))
    return im
def g_calendar_num(W):
    im,d=layer(W)
    return im

def calendar_icon(size=B):
    W=size*S
    mask=superellipse(W,W,5.0)
    y,x=np.mgrid[0:W,0:W].astype(float)
    base=gradient(W,W,(255,255,255),(228,230,236))
    # faixa vermelha no topo
    band=(y<W*0.30)[...,None]
    red=gradient(W,W,(255,92,84),(235,48,56))
    rgb=np.where(band,red,base)
    gl=np.clip(1-(y/(W*0.5)),0,1)**1.6*0.30*(superellipse(W,W,5.0,inset=3)>0)
    rgb=rgb+(255-rgb)*gl[...,None]
    inner=superellipse(W,W,5.0,inset=2.2)
    rim=((mask>0)&(inner==0)).astype(float)*0.5
    rgb=rgb+(255-rgb)*rim[...,None]
    img=Image.fromarray(np.clip(rgb,0,255).astype('uint8'),'RGB')
    dd=ImageDraw.Draw(img)
    f=ImageFont.truetype(FONT,int(W*0.50))
    t='20'; bb=dd.textbbox((0,0),t,font=f)
    dd.text(((W-(bb[2]-bb[0]))/2-bb[0],W*0.30+(W*0.70-(bb[3]-bb[1]))/2-bb[1]-W*0.02),t,font=f,fill=(28,28,32))
    # pequeno texto no topo
    f2=ImageFont.truetype(FONT,int(W*0.15)); t2='CAL'; b2=dd.textbbox((0,0),t2,font=f2)
    dd.text(((W-(b2[2]-b2[0]))/2-b2[0],W*0.15-(b2[3]-b2[1])/2-b2[1]),t2,font=f2,fill=(255,255,255))
    out=np.dstack([np.array(img),mask]).astype('uint8')
    return Image.fromarray(out,'RGBA').resize((size,size),Image.LANCZOS)

def glass_tile(w,h,top,bot,glyph,gscale=1.55,gy=0.44,radius=34):
    W,H=w*S,h*S
    base=gradient(W,H,top,bot,diag=0.12)
    y,x=np.mgrid[0:H,0:W].astype(float)
    # mascara retangulo arredondado
    mk=Image.new('L',(W,H),0); ImageDraw.Draw(mk).rounded_rectangle([0,0,W-1,H-1],radius=radius*S,fill=255)
    mask=np.array(mk)
    gl=np.clip(1-(y/(H*0.42)),0,1)**1.7*0.30
    rgb=base+(255-base)*gl[...,None]
    # rim
    er=np.array(Image.fromarray(mask).filter(ImageFilter.MinFilter(2*int(2.2*S)+1)))
    rim=((mask>0)&(er==0)).astype(float)*np.clip(0.8-0.6*(y/H),0.15,0.8)
    rgb=rgb+(255-rgb)*rim[...,None]
    sh=np.clip((y/H-0.7)/0.3,0,1)**1.4*0.18
    rgb=rgb*(1-sh[...,None])
    g=glyph(B*S)
    gw=int(B*S*gscale); g=g.resize((gw,gw),Image.LANCZOS)
    canvas=Image.new('L',(W,H),0)
    canvas.paste(g,(int((W-gw)/2),int(H*gy-gw/2)))
    ga=np.array(canvas).astype(float)/255
    sa=np.array(canvas.filter(ImageFilter.GaussianBlur(5*S)))/255*0.30
    sa=np.roll(sa,4*S,axis=0)
    rgb=rgb*(1-sa[...,None])
    rgb=rgb*(1-ga[...,None])+255*ga[...,None]
    out=np.dstack([np.clip(rgb,0,255),mask]).astype('uint8')
    return Image.fromarray(out,'RGBA').resize((w,h),Image.LANCZOS)

ICONS={ # indice do item (normal) -> (cima,baixo,glifo)
 4:((255,110,100),(236,48,72),g_usb),
 6:((96,176,255),(24,104,236),g_sd),
 8:((150,156,172),(72,78,96),g_plug),
 10:((255,176,56),(255,116,24),g_clock),
 12:((186,132,255),(112,70,232),g_eq),
 14:((84,226,206),(22,150,196),g_photo),
 18:((84,226,150),(20,170,104),g_multi),
 20:((70,200,255),(24,112,226),g_dashcam),
 22:((255,92,150),(222,30,100),g_btmusic),
 24:((176,182,198),(104,110,128),g_gear),
}
TILES={
 0:((92,168,255),(34,76,232),g_globe),
 2:((255,150,84),(255,76,70),g_tower2),
 26:((90,200,255),(40,90,240),g_multi),
 28:((190,118,255),(96,60,224),g_headset),
 30:((74,222,112),(22,170,76),g_phone),
}
def build_all():
    new={}
    for i,(t,b,g) in ICONS.items():
        ic=glass_icon(t,b,g)
        cv=Image.new('RGBA',(170,120),(0,0,0,0)); cv.paste(ic,(29,4),ic); new[i]=cv
    cv=Image.new('RGBA',(170,120),(0,0,0,0)); ic=calendar_icon(); cv.paste(ic,(29,4),ic); new[16]=cv
    for i,(t,b,g) in TILES.items(): new[i]=glass_tile(204,300,t,b,g)
    return new
def dim(im,f):
    a=np.array(im).copy(); a[...,3]=(a[...,3]*f).astype('uint8'); return Image.fromarray(a,'RGBA')
if __name__=='__main__':
    new=build_all()
    for i,im in new.items(): im.save(f'ex/new_{i:02d}.png')
    # folha comparativa
    import glob
    sheet=Image.new('RGB',(1500,720),(48,48,56)); x=y=0
    order=[4,6,8,10,12,14,16,18,20,22,24]
    for k,i in enumerate(order):
        o=Image.open(glob.glob(f'ex/ui/img{i:02d}_*.png')[0]).convert('RGBA')
        sheet.paste(o,(10+(k%8)*185,10+(k//8)*260),o)
        sheet.paste(new[i],(10+(k%8)*185,130+(k//8)*260),new[i])
    sheet.save('ex/cmp_icons.png')
    sheet=Image.new('RGB',(1300,330),(48,48,56))
    for k,i in enumerate([0,2,26,28,30]):
        o=Image.open(glob.glob(f'ex/ui/img{i:02d}_*.png')[0]).convert('RGBA')
        sheet.paste(o,(10+k*210,10),o)
    sheet.save('ex/cmp_tiles_old.png')
    sheet=Image.new('RGB',(1100,330),(48,48,56))
    for k,i in enumerate([0,2,26,28,30]): sheet.paste(new[i],(10+k*210,10),new[i])
    sheet.save('ex/cmp_tiles_new.png')
