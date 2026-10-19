import struct, zlib, sys
src, out, vmode = sys.argv[1], sys.argv[2], sys.argv[3]   # vmode: bin | ascii
d = open(src,'rb').read()
assert len(d)==16*1024*1024
SEC=512
def addsum(b):
    b = b + b'\0'*((-len(b))%4)
    return sum(struct.unpack('<%dI'%(len(b)//4), b)) & 0xffffffff

# --- sunxi_mbr (0x4000 bytes, 4 copies) ---
parts=[('bootA',0x20,0xc80,1,0),('ROOTFS',0xca0,0x6f80,1,0),('UDISK',0x7c20,0x380,0,0x8000)]
def mkmbr(copy):
    m=bytearray(0x4000)
    struct.pack_into('<I',m,4,0x200)
    m[8:16]=b'softw411'
    struct.pack_into('<III',m,0x10,4,copy,len(parts))   # copy count, index, PartCount
    for i,(n,s,l,ro,key) in enumerate(parts):
        o=0x20+i*0x80
        struct.pack_into('<IIII',m,o,0,s,0,l)
        m[o+0x10:o+0x10+4]=b'DISK'
        m[o+0x20:o+0x20+len(n)]=n.encode()
        struct.pack_into('<III',m,o+0x30,0,key,ro)
    struct.pack_into('<I',m,0,zlib.crc32(bytes(m[4:]))&0xffffffff)
    return bytes(m)
mbr=b''.join(mkmbr(i) for i in range(4))

# --- DLINFO (0x4000) ---
dl_name=b'ROOTFS_FEX00000'.ljust(16,b'\0')
vf_name=b'VROOTFS_FEX0000'.ljust(16,b'\0')
dli=bytearray(0x4000)
struct.pack_into('<I',dli,4,0x200); dli[8:16]=b'softw411'; struct.pack_into('<I',dli,16,1)
o=32
dli[o:o+6]=b'ROOTFS'
struct.pack_into('<IIII',dli,o+16,0,0xca0,0,0x6f80)
dli[o+32:o+48]=dl_name; dli[o+48:o+64]=vf_name
struct.pack_into('<II',dli,o+64,0,1)
struct.pack_into('<I',dli,0,zlib.crc32(bytes(dli[4:]))&0xffffffff)

rootfs=d[0x1a0000:0xf90000]
assert len(rootfs)==0x6f80*SEC
s=addsum(rootfs)
if vmode=='bin':
    vf=struct.pack('<I',s).ljust(64,b'\0')
else:
    vf=(b'%08x'%s).ljust(64,b'\0')
boot0=d[0:0xC000]

items=[('12345678','1234567890BNOR_0',boot0),
       ('12345678','1234567890___MBR',mbr),
       ('12345678','1234567890DLINFO',bytes(dli)),
       ('RFSFAT16','ROOTFS_FEX00000',rootfs),
       ('RFSFAT16','VROOTFS_FEX0000',vf)]
n=len(items)
tab=1024+n*1024
off=tab
offs=[]
for it in items:
    offs.append(off); off+=(len(it[2])+1023)//1024*1024
total=off
hdr=bytearray(1024)
hdr[0:8]=b'IMAGEWTY'
struct.pack_into('<IIIII',hdr,8,0x300,96,0x4d00000,0x100234,total)
struct.pack_into('<I',hdr,28,1024)
struct.pack_into('<IIIIII',hdr,32,0x1234,0x8743,0x100,0x100,1,1024)
struct.pack_into('<I',hdr,60,n)
struct.pack_into('<I',hdr,64,1024)
out_b=bytearray(hdr)
FN=256
for (m,sb,data),o in zip(items,offs):
    e=bytearray(1024)
    struct.pack_into('<II',e,0,FN,1024)
    e[8:16]=m.encode().ljust(8,b'\0'); e[16:32]=sb.encode().ljust(16,b'\0')
    e[36:36+len(sb)]=sb.encode()
    p=32+FN
    struct.pack_into('<I',e,p+12,len(data))
    struct.pack_into('<I',e,p+20,o)
    struct.pack_into('<I',e,p+4,len(data))
    out_b+=e
for (m,sb,data),o in zip(items,offs):
    assert len(out_b)==o
    out_b+=data+b'\0'*((-len(data))%1024)
open(out,'wb').write(out_b)
print(out,len(out_b),hex(s))
