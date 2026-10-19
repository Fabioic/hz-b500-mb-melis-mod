import struct, zlib, re
R=0x1a0000
SIG='DATAV1.0'.encode('utf-16le')
def dir_records(d):
    """acha registros de diretorio (nome,.data etc) na area 0..0x5000 do ROOTFS: retorna lista de dict"""
    area=d[R:R+0x5000]; out=[]
    for o in range(0,len(area)-20,4):
        off,sz,sz2,attr=struct.unpack_from('<4I',area,o)
        nl=struct.unpack_from('<I',area,o+16)[0]&0xffff
        if 0<nl<64 and 0x1000<off<0xe00000 and 0<sz<0x1000000 and (sz2==sz or (attr&0xe0 and sz2>sz)):
            nm=area[o+20:o+20+nl]
            if all(32<=c<127 for c in nm.rstrip(b'\0')):
                out.append(dict(rec=R+o,off=off,size=sz,size2=sz2,attr=attr,name=nm.rstrip(b'\0').decode()))
    return out
def parse(md):
    """md = bytes de um arquivo DATAV1.0. retorna (tabpos, itens[(off,clen)], hdr24s[list])"""
    tab=struct.unpack_from('<I',md,0x14)[0]
    n=struct.unpack_from('<I',md,tab)[0]
    items=[struct.unpack_from('<II',md,tab+4+8*i) for i in range(n)]
    return tab,n,items
def check(md):
    tab,n,items=parse(md)
    for i,(o,c) in enumerate(items):
        hs=struct.unpack_from('<I',md,o)[0]
        if hs!=24: return False
        try:
            z=zlib.decompressobj(); z.decompress(md[o+24:o+24+c])
            if not z.eof: return False
        except Exception: return False
    return True
def item_info(md,i):
    tab,n,items=parse(md); o,c=items[i]
    hs,w,h,fmt,comp,x=struct.unpack_from('<6I',md,o)
    return dict(off=o,clen=c,w=w,h=h,fmt=fmt,comp=comp,x=x)
def rebuild(md,repl):
    """repl: {idx: (fmt, rawbytes)} -> novo md com itens substituidos (tabela atualizada, itens re-empacotados em ordem)"""
    tab,n,items=parse(md)
    if n==0: return md
    ordered=sorted(range(n),key=lambda i:items[i][0])
    first=items[ordered[0]][0]
    # verifica que os itens sao contiguos e o que vem apos o ultimo
    last=items[ordered[-1]]; end=last[0]+24+last[1]
    out=bytearray(md[:first]); newitems=[None]*n
    pos=first
    for i in ordered:
        o,c=items[i]
        hdr=bytearray(md[o:o+24]); body=md[o+24:o+24+c]
        if i in repl:
            fmt,raw=repl[i]
            struct.pack_into('<I',hdr,12,fmt)
            body=zlib.compress(raw,9)
        newitems[i]=(pos,len(body)); out+=hdr+body; pos+=24+len(body)
    out+=md[end:]
    for i,(o,c) in enumerate(newitems): struct.pack_into('<II',out,tab+4+8*i,o,c)
    return bytes(out)
