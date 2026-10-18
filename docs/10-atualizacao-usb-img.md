# 10 — Atualização por pendrive (testada)

Funciona **sem CH341A**. Pendrive em **FAT32**, central ligada, pendrive no USB.

## 1) `\Update\Config.ini` (testado ✔)
Um `Config.ini` na pasta `\Update\` é aplicado pela central (ela reinicia e aplica). Teste: `animationType=1` mudou a transição de telas para um deslize suave.
`idleReturnTime` **não** faz o painel da bolinha fechar sozinho (testado com 5 e 50).

## 2) `\Update\LTTF133.img` — atualização completa do ROOTFS (testado ✔)
A tela mostra "APP Atualiz. … %(NNs)" e a central reinicia sozinha. O arquivo é uma imagem **Allwinner IMAGEWTY** (mesmo formato do PhoenixSuit):

- Cabeçalho de 1024 B: magia `IMAGEWTY`, versão `0x300`, tamanho do cabeçalho `96`, `ram 0x4d00000`, versão do formato `0x100234`, tamanho total, número de itens em `+60`.
- Tabela de itens em `1024 + i*1024` (1024 B cada): `fn_len=256`, `hdr_size=1024`, `main[8]`, `sub[16]`, tamanho em `32+256+12` (e `+4`), offset em `32+256+20`. Dados em seguida, alinhados a 1024.
- Itens usados (nesta ordem): `12345678/1234567890BNOR_0` (boot0, `0..0xC000` da flash), `…___MBR` (4 cópias × 0x4000), `…DLINFO` (0x4000, 1 entrada), `RFSFAT16/ROOTFS_FEX00000` (a partição ROOTFS inteira, `0x1A0000..0xF90000`) e `RFSFAT16/VROOTFS_FEX0000` (verificação).
- **MBR** (`softw411`, ver `0x200`): partições `bootA` LBA `0x20..0xc9f`, `ROOTFS` `0xca0..0x7c1f`, `UDISK` `0x7c20..0x7f9f` (LBAs relativos a `0xC000`); CRC32 (zlib) dos bytes `[4:0x4000]` gravado em `[0:4]`.
- **DLINFO**: cabeçalho de 32 B + entrada de 72 B com nomes `ROOTFS_FEX00000` (dados) e `VROOTFS_FEX0000` (verificação), `verify=1`.
- **Verificação**: soma aditiva de palavras `u32` little-endian dos dados, preenchida até 64 bytes (variante binária; a variante ASCII não foi necessária).
- A UDISK (CONFIG.INI, pareamentos) **não** é tocada pela atualização.

Ferramenta: `python3 tools/build_img.py flash_modificada.bin saida/Update/LTTF133.img bin` (a flash modificada precisa ter 16 MB; só o ROOTFS é aproveitado). **Sempre mantenha o backup original** e, se possível, o CH341A à mão.
