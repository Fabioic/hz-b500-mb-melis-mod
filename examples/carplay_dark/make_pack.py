import sys, struct, zlib, json, re
import numpy as np
from PIL import Image
sys.path.insert(0,'.')
import dataf, darkset, ballmenu
base,out,mode=sys.argv[1],sys.argv[2],sys.argv[3]   # mode: bgra | d565
fw=bytearray(open(base,'rb').read())
R=dataf.R; LIMIT=0xdf0000
A4=lambda n:(n+3)//4*4
recs=dataf.dir_records(bytes(fw))
hits=[m.start() for m in re.finditer(re.escape(dataf.SIG),bytes(fw))]
byabs={R+r['off']:r for r in recs}
# fim dos dados e buracos
tail=max(r['off']+r['size'] for r in recs); tail=A4(tail); holes=[]
used_added=0
def alloc(n):
    global tail
    for h in holes:
        if h[1]-h[0]>=n:
            p=h[0]; h[0]+=A4(n); return p
    p=tail; tail+=A4(n)
    assert tail<=LIMIT,('sem espaco',hex(tail))
    return p
def put(rec,new):
    """grava arquivo novo (relocando se maior) e atualiza registro"""
    global used_added
    old_off,old_sz=rec['off'],rec['size']
    if len(new)<=old_sz:
        p=old_off
        fw[R+p:R+p+len(new)]=new
        if len(new)<old_sz: fw[R+p+len(new):R+p+old_sz]=b'\0'*(old_sz-len(new))
    else:
        p=alloc(len(new)); fw[R+p:R+p+len(new)]=new
        holes.append([A4(old_off),A4(old_off)+(old_sz//4)*4]) if False else holes.append([old_off,old_off+old_sz])
    struct.pack_into('<III',fw,rec['rec'],p,len(new),len(new))
    rec['off'],rec['size'],rec['size2']=p,len(new),len(new)
# ---------- codificadores ----------
def enc1(im): return np.array(im.convert('RGBA'))[...,[2,1,0,3]].tobytes()
def enc3d(im):
    a=np.array(im.convert('RGBA')).astype(np.float64); h,w=a.shape[:2]
    rgb=a[...,:3].copy(); al=a[...,3]
    # Floyd-Steinberg em 565
    out=np.zeros((h,w),np.uint32)
    for y in range(h):
        for x in range(w):
            r,g,b=rgb[y,x]
            r5=int(min(31,max(0,round(r*31/255)))); g6=int(min(63,max(0,round(g*63/255)))); b5=int(min(31,max(0,round(b*31/255))))
            q=np.array([r5*255/31,g6*255/63,b5*255/31]); e=rgb[y,x]-q
            if al[y,x]>0:
                if x+1<w: rgb[y,x+1]+=e*7/16
                if y+1<h:
                    if x>0: rgb[y+1,x-1]+=e*3/16
                    rgb[y+1,x]+=e*5/16
                    if x+1<w: rgb[y+1,x+1]+=e*1/16
            out[y,x]=(r5<<11)|(g6<<5)|b5 if al[y,x]>0 else 0
    st=A4(w*3); buf=np.zeros((h,st),np.uint8)
    buf[:,0:w*3:3]=out&255; buf[:,1:w*3:3]=out>>8; buf[:,2:w*3:3]=al.astype(np.uint8)
    return buf.tobytes()
def enc3(im):
    a=np.array(im.convert('RGBA')).astype(np.int32); h,w=a.shape[:2]
    rgb,al=a[...,:3],np.round(a[...,3]*31/255).astype(np.int32)
    r5=np.round(rgb[...,0]*31/255).astype(np.int32); g6=np.round(rgb[...,1]*63/255).astype(np.int32); b5=np.round(rgb[...,2]*31/255).astype(np.int32)
    v=np.where(al==0,65535 if (h,w)==(60,60) else 0,(r5<<11)|(g6<<5)|b5)
    st=A4(w*3); buf=np.zeros((h,st),np.uint8)
    buf[:,0:w*3:3]=v&255; buf[:,1:w*3:3]=v>>8; buf[:,2:w*3:3]=al
    return buf.tobytes()
FMT=1 if mode=='bgra' else 3
ENC=enc1 if mode=='bgra' else (enc3 if mode=='r565' else enc3d)
def repack(rec,images,expect=None):
    md=bytes(fw[R+rec['off']:R+rec['off']+rec['size']])
    tab,n,items=dataf.parse(md); repl={}
    for idx,im in images.items():
        ii=dataf.item_info(md,idx); assert im.size==(ii['w'],ii['h']),(rec['name'],idx,im.size,(ii['w'],ii['h']))
        repl[idx]=(FMT,ENC(im))
    nb=dataf.rebuild(md,repl)
    assert dataf.check(nb)
    put(rec,nb); return len(nb)
# ---------- 1) Main.data (arquivo 14) ----------
rec14=byabs[hits[14]]
n14=repack(rec14,darkset.build_file14()); print('Main.data',n14)
# ---------- 2) bolinha/painel nos 8 arquivos ----------
roles=ballmenu.roles()
for f in (1,13,26,44,49,52,56,67):
    rec=byabs[hits[f]]
    md=bytes(fw[R+rec['off']:R+rec['off']+rec['size']]); tab,n,items=dataf.parse(md)
    infos=[dataf.item_info(md,i) for i in range(n)]
    p=[k for k,i in enumerate(infos) if (i['w'],i['h'])==(400,240)][0]
    imgs={p+rel:im for rel,im in roles.items()}
    print(rec['name'],repack(rec,imgs))

# ---------- 2b) nome do idioma (imagem 200x30 no SetupLanguage.data, item 11) ----------
from PIL import Image,ImageDraw,ImageFont
recL=[r for r in recs if r['name']=='SetupLanguage.data'][0]
big=Image.new('L',(800,120),0); dd=ImageDraw.Draw(big)
fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf',4*26)
bb=dd.textbbox((0,0),'Português BR',font=fnt)
dd.text(((800-(bb[2]-bb[0]))//2-bb[0],(120-(bb[3]-bb[1]))//2-bb[1]-4),'Português BR',font=fnt,fill=255)
cov=np.array(big.resize((200,30),Image.LANCZOS)).astype(float)/255
al=np.round(cov*31).astype(np.int32)
v=np.full((30,200),59229,np.int32)
buf=np.zeros((30,600),np.uint8); buf[:,0::3]=v&255; buf[:,1::3]=v>>8; buf[:,2::3]=al
mdL=bytes(fw[R+recL['off']:R+recL['off']+recL['size']])
nbL=dataf.rebuild(mdL,{7:(3,buf.tobytes())}); assert dataf.check(nbL); put(recL,nbL); print('SetupLanguage',len(nbL))
# ---------- 3) idioma ----------
rs=[r for r in recs if r['name']=='Setup.txt'][0]
txt=bytes(fw[R+rs['off']:R+rs['off']+rs['size']]).decode('utf-16le')
cnt=0
def sub(m):
    global cnt; cnt+=1; return '\tPortuguês BR\t'
# tokens inteiros 'Portugal' entre tabs/aspas (nao Portugalski/Portugalština)
lines=txt.split('\r\n'); cnt=0
for k,ln in enumerate(lines):
    c=ln.split('\t')
    if len(c)>20 and c[0]=='{' and c[1]=='葡萄牙语':
        for j in range(2,len(c)-1):
            if c[j] and all(ord(ch)<0x250 for ch in c[j]):
                c[j]='Português BR'; cnt+=1
        lines[k]='\t'.join(c)
new='\r\n'.join(lines)
print('Portugal ->',cnt)
put(rs,new.encode('utf-16le'))
# ---------- 3b) FM Transmit(ter) -> Transmissor FM ----------
for nm in ('Main.txt','SystemBar.txt','Setup.txt'):
    rr_=[r for r in recs if r['name']==nm][0]
    tx=bytes(fw[R+rr_['off']:R+rr_['off']+rr_['size']]).decode('utf-16le'); ls=tx.split('\r\n'); n=0
    for k,ln in enumerate(ls):
        c=ln.split('\t')
        if len(c)>20 and c[0]=='{' and c[1] in ('收音机','FM发射') and c[2].startswith('FM Transmit'):
            for j in (10,16):
                if c[j].startswith('FM Transmit'): c[j]='Transmissor FM'; n+=1
            ls[k]='\t'.join(c)
    put(rr_,'\r\n'.join(ls).encode('utf-16le')); print(nm,'FM ->',n)
# ---------- superbloco ----------
used=struct.unpack_from('<I',fw,R+0x18)[0]
newused=used+(tail-A4(max(r['off']+r['size'] for r in recs if True) if False else 0)) if False else None
open(out,'wb').write(fw)
print('fim dos dados',hex(tail),'holes',[(hex(a),hex(b)) for a,b in holes])
# atualiza campo "usado" = tail - 0x4a00
struct.pack_into('<I',fw,R+0x18,tail-0x4a00); open(out,'wb').write(fw)
print(out,'%08X'%zlib.crc32(bytes(fw)))
