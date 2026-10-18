#!/usr/bin/env python3
"""fwtool - utilitarios para o firmware da central multimidia HZ-B500-MB (Allwinner F133 / Melis).

Uso:  python3 fwtool.py <comando> dump.bin [opcoes]

  info        dump.bin                      tabela de particoes e visao geral
  ls          dump.bin                      lista arquivos do ROOTFS (MINFS)
  extract     dump.bin pasta                extrai arquivos nao comprimidos do ROOTFS
  ui-list     dump.bin                      lista as imagens dos arquivos DATAV1.0 (Main.data)
  ui-export   dump.bin pasta                exporta as imagens como PNG
  ui-replace  dump.bin saida.bin ARQ.ITEM img.png   troca UMA imagem mantendo o tamanho exato
  mods        dump.bin pasta                descomprime os modulos (.mod) do ROOTFS (blocos LZMA)
  udisk       dump.bin pasta                extrai os arquivos da particao UDISK (FAT12): CONFIG.INI etc.

Somente biblioteca padrao + numpy + Pillow.  NAO coloque dumps em repositorios publicos
(contem chaves de pareamento, nomes de aparelhos, etc.).
"""
import sys, os, re, struct, zlib, lzma, json

ROOTFS = 0x1A0000          # inicio da particao ROOTFS (MINFS)
UDISK  = 0xF90000          # inicio da particao UDISK (FAT12/16)
SIG    = 'DATAV1.0'.encode('utf-16le')
A4 = lambda n: (n + 3) // 4 * 4

def load(p): return open(p, 'rb').read()

# ---------------------------------------------------------------- info
def cmd_info(d):
    print('tamanho', len(d), 'bytes; boot0:', d[4:12])
    if d[0xC200:0xC208] == b'EFI PART':
        n = struct.unpack_from('<I', d, 0xC200 + 80)[0]; sz = struct.unpack_from('<I', d, 0xC200 + 84)[0]
        for i in range(min(n, 16)):
            e = d[0xC400 + i * sz: 0xC400 + (i + 1) * sz]
            if e[:16] == b'\0' * 16: continue
            first, last = struct.unpack_from('<QQ', e, 32)
            name = e[56:128].decode('utf-16le', 'ignore').strip('\0')
            print(f'{name:10s} {0xC000 + first * 512:#09x} - {0xC000 + (last + 1) * 512:#09x}')
    print('arquivos DATAV1.0:', len(re.findall(re.escape(SIG), d)))

# ---------------------------------------------------------------- MINFS
def minfs_walk(d):
    files = []; seen = set()
    u = lambda o: struct.unpack_from('<I', d, o)[0]
    def walk(off, size, path):
        if (off, size) in seen: return
        seen.add((off, size)); o = ROOTFS + off; end = o + size
        while o + 20 <= end:
            foff, sz, sz2, attr = struct.unpack_from('<4I', d, o); w = u(o + 16)
            nl, ex = w & 0xffff, w >> 16
            if nl == 0 or nl > 200: break
            name = d[o + 20:o + 20 + nl].decode('latin1'); nxt = o + 20 + ((nl + 3) & ~3)
            p = path + '/' + name
            if attr & 0x10000: walk(foff, sz, p)
            else: files.append(dict(path=p, off=foff, size=sz, size2=sz2, attr=attr, flag=ex))
            o = nxt
    walk(0x200, u(ROOTFS + 0x200), '')
    return files

def cmd_ls(d):
    for f in minfs_walk(d):
        c = ' (comprimido)' if f['size'] != f['size2'] or f['flag'] else ''
        print(f"{f['path']:42s} @ROOTFS+{f['off']:#x} tam={f['size']}{c}")

def cmd_extract(d, out):
    for f in minfs_walk(d):
        if f['size'] != f['size2'] or f['flag']: continue
        p = os.path.join(out, f['path'].lstrip('/')); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'wb').write(d[ROOTFS + f['off']: ROOTFS + f['off'] + f['size']]); print(p)

# ---------------------------------------------------------------- imagens DATAV1.0
def ui_items(d):
    """Cada arquivo DATAV1.0 = cabecalho de layout (UTF-16) + itens [cab 24B + fluxo zlib].
    cab = <6I: 24, w, h, fmt, comp(3=zlib), x>.  fmt 1=BGRA8888, 2=RGB565, 3=RGB565+A8 intercalado."""
    hits = [m.start() for m in re.finditer(re.escape(SIG), d)]
    ends = hits[1:] + [len(d)]
    items = []; counts = {}
    for fi, (a, b) in enumerate(zip(hits, ends)):
        blk = d[a:b]
        for m in re.finditer(b'\x78[\x01\x5e\x9c\xda]', blk):
            s = m.start()
            if s < 24: continue
            hs, w, h, fmt, comp, x = struct.unpack('<6I', blk[s - 24:s])
            if hs != 24 or not (1 <= w <= 3000 and 1 <= h <= 3000) or fmt not in (1, 2, 3): continue
            try:
                do = zlib.decompressobj(); out = do.decompress(blk[s:s + 600000]); clen = len(blk[s:s + 600000]) - len(do.unused_data)
            except Exception: continue
            exp = {1: w * h * 4, 2: A4(w * 2) * h, 3: A4(w * 3) * h}[fmt]
            if len(out) != exp: continue
            k = counts.get(fi, 0); counts[fi] = k + 1
            items.append(dict(file=fi, item=k, start=a + s, clen=clen, w=w, h=h, fmt=fmt))
    return items

def raw_of(d, it): return zlib.decompressobj().decompress(d[it['start']:it['start'] + it['clen'] + 16])

def r565(v):
    import numpy as np
    return np.dstack([((v >> 11) & 31) * 255 // 31, ((v >> 5) & 63) * 255 // 63, (v & 31) * 255 // 31]).astype('uint8')

def decode(d, it):
    import numpy as np; from PIL import Image
    w, h, f = it['w'], it['h'], it['fmt']; b = np.frombuffer(raw_of(d, it), np.uint8)
    if f == 1: return Image.fromarray(b.reshape(h, w, 4)[..., [2, 1, 0, 3]].copy(), 'RGBA')
    if f == 2:
        c = b.reshape(h, A4(w * 2))[:, :w * 2].copy().view('<u2').reshape(h, w).astype(np.uint32)
        return Image.fromarray(r565(c), 'RGB').convert('RGBA')
    q = b.reshape(h, A4(w * 3))[:, :w * 3].reshape(h, w, 3).astype(np.uint32)
    im = Image.fromarray(r565(q[:, :, 0] | (q[:, :, 1] << 8)), 'RGB').convert('RGBA')
    im.putalpha(Image.fromarray(q[:, :, 2].astype('uint8'))); return im

def encode(im, fmt, bits=8, astep=1):
    """PIL RGBA -> bytes crus do formato fmt. bits/astep reduzem entropia (comprime menos)."""
    import numpy as np
    a = np.array(im.convert('RGBA')).astype(np.int32); h, w = a.shape[:2]
    if fmt == 1: return a[..., [2, 1, 0, 3]].astype('uint8').tobytes()
    rgb, al = a[..., :3], a[..., 3]
    if astep > 1: al = np.clip(np.round(al / astep) * astep, 0, 255).astype(np.int32)
    lv = (1 << bits) - 1; q = np.round(rgb * lv / 255).astype(np.int32)
    r5 = np.round(q[..., 0] * 31 / lv).astype(np.int32); g6 = np.round(q[..., 1] * 63 / lv).astype(np.int32); b5 = np.round(q[..., 2] * 31 / lv).astype(np.int32)
    v = (r5 << 11) | (g6 << 5) | b5
    if fmt == 2:
        buf = np.zeros((h, A4(w * 2)), np.uint8); buf[:, 0:w * 2:2] = v & 255; buf[:, 1:w * 2:2] = v >> 8; return buf.tobytes()
    v = np.where(al == 0, 0, v); buf = np.zeros((h, A4(w * 3)), np.uint8)
    buf[:, 0:w * 3:3] = v & 255; buf[:, 1:w * 3:3] = v >> 8; buf[:, 2:w * 3:3] = al; return buf.tobytes()

def fit_zlib(raw, clen):
    """Comprime raw em zlib com EXATAMENTE clen bytes (insere blocos stored vazios 00 00 00 ff ff
    apos o cabecalho zlib de 2 bytes). Retorna None se nao couber."""
    for lvl in (9, 8, 7, 6, 5):
        for mem in range(9, 0, -1):
            for strat in (zlib.Z_DEFAULT_STRATEGY, zlib.Z_FILTERED):
                c = zlib.compressobj(lvl, zlib.DEFLATED, 15, mem, strat); z = c.compress(raw) + c.flush()
                if len(z) <= clen and (clen - len(z)) % 5 == 0:
                    return z[:2] + b'\x00\x00\x00\xff\xff' * ((clen - len(z)) // 5) + z[2:]
    return None

def replace_item(fw, it, im):
    if im.size != (it['w'], it['h']): sys.exit(f"tamanho {im.size} != {(it['w'], it['h'])}")
    for astep in (1, 8, 16, 32, 64):
        for bits in (8, 6, 5, 4, 3, 2):
            raw = encode(im, it['fmt'], bits, astep); z = fit_zlib(raw, it['clen'])
            if z:
                assert zlib.decompress(z) == raw and len(z) == it['clen']
                fw[it['start']:it['start'] + it['clen']] = z
                print(f'ok: cores {bits} bits, alfa passo {astep}'); return True
    print('NAO CABE no espaco original', it['clen'], 'bytes; simplifique a imagem'); return False

def cmd_ui_list(d):
    for it in ui_items(d): print(f"{it['file']}.{it['item']}\t{it['w']}x{it['h']}\tfmt{it['fmt']}\t@{it['start']:#x}\tzlib={it['clen']}")

def cmd_ui_export(d, out):
    os.makedirs(out, exist_ok=True)
    for it in ui_items(d): decode(d, it).save(os.path.join(out, f"{it['file']:02d}_{it['item']:02d}_{it['w']}x{it['h']}.png"))

def cmd_ui_replace(d, outbin, spec, png):
    from PIL import Image
    f, i = [int(x) for x in spec.split('.')]
    it = [x for x in ui_items(d) if x['file'] == f and x['item'] == i][0]
    fw = bytearray(d)
    if replace_item(fw, it, Image.open(png)): open(outbin, 'wb').write(fw); print('gravado', outbin, '%08X' % zlib.crc32(bytes(fw)))

# ---------------------------------------------------------------- modulos .mod (blocos LZMA "5d 00 80 00 00")
def lz_chunk(d, s, e):
    props = d[s]; dic = struct.unpack_from('<I', d, s + 1)[0]
    f = [{'id': lzma.FILTER_LZMA1, 'dict_size': dic, 'lc': props % 9, 'lp': (props // 9) % 5, 'pb': props // 45}]
    D = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=f); out = b''; i = s + 5
    while i < e:
        blk = d[i:min(i + 64, e)]
        try: out += D.decompress(blk); i += len(blk)
        except Exception:
            D = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=f); out = b''; j = s + 5
            try:
                while j < e: out += D.decompress(d[j:j + 1]); j += 1
            except Exception: pass
            return out
        if D.eof: break
    return out

def cmd_mods(d, out):
    os.makedirs(out, exist_ok=True)
    marks = [ROOTFS + m.start() for m in re.finditer(b'\x5d\x00\x80\x00\x00', d[ROOTFS:UDISK])]
    for k, s in enumerate(marks):
        e = marks[k + 1] if k + 1 < len(marks) else s + 20000
        o = lz_chunk(d, s, e); open(os.path.join(out, f'{s:08x}.bin'), 'wb').write(o); print(f'{s:#x}: {e - s} -> {len(o)}')
    print('Codigo = RISC-V RV64GC; carregue em Ghidra/capstone. Strings: strings -n 5 *.bin')

# ---------------------------------------------------------------- UDISK (FAT12)
def cmd_udisk(d, out):
    u = d[UDISK:UDISK + 0x70000]
    bps, spc, rsv, nfat, rootn, tot, media, fatsz = struct.unpack_from('<HBHBHHBH', u, 11)
    fatb = u[rsv * bps: rsv * bps + fatsz * bps]; rootoff = (rsv + nfat * fatsz) * bps; datoff = rootoff + rootn * 32
    def fat(c):
        o = c * 3 // 2; v = fatb[o] | (fatb[o + 1] << 8); return (v >> 4) if c & 1 else (v & 0xfff)
    def chain(c):
        r = []
        while 2 <= c < 0xff8 and len(r) < 2000: r.append(c); c = fat(c)
        return r
    def rd(c, size): return b''.join(u[datoff + (x - 2) * spc * bps: datoff + (x - 1) * spc * bps] for x in chain(c))[:size]
    def ents(buf):
        for q in range(len(buf) // 32):
            e = buf[32 * q:32 * q + 32]
            if e[0] == 0: break
            if e[0] == 0xe5 or e[11] == 0x0f: continue
            nm = e[:8].decode('latin1').strip() + ('.' + e[8:11].decode('latin1').strip() if e[8:11].strip() else '')
            if nm in ('.', '..'): continue
            yield nm, e[11], struct.unpack_from('<H', e, 26)[0], struct.unpack_from('<I', e, 28)[0]
    def walk(buf, path):
        for nm, at, cl, sz in ents(buf):
            if at & 0x10: os.makedirs(os.path.join(out, path + nm), exist_ok=True); walk(rd(cl, 10 ** 6), path + nm + '/')
            else: os.makedirs(os.path.dirname(os.path.join(out, path + nm)) or out, exist_ok=True); open(os.path.join(out, path + nm), 'wb').write(rd(cl, sz)); print(path + nm, sz)
    os.makedirs(out, exist_ok=True); walk(u[rootoff:rootoff + rootn * 32], '')

def main():
    a = sys.argv
    if len(a) < 3: print(__doc__); return
    c, d = a[1], load(a[2])
    if c == 'info': cmd_info(d)
    elif c == 'ls': cmd_ls(d)
    elif c == 'extract': cmd_extract(d, a[3])
    elif c == 'ui-list': cmd_ui_list(d)
    elif c == 'ui-export': cmd_ui_export(d, a[3])
    elif c == 'ui-replace': cmd_ui_replace(d, a[3], a[4], a[5])
    elif c == 'mods': cmd_mods(d, a[3])
    elif c == 'udisk': cmd_udisk(d, a[3])
    else: print(__doc__)
if __name__ == '__main__': main()
