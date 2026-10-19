# 11 — `.data` por tela, registros MINFS e realocação

Correção do doc 04: **não existe um único `Main.data`**. Em `/apps/UI2/Data/` há **71 arquivos `.data`**, um por tela (`Main.data`, `CarPlay.data`, `SetupLanguage.data`…), cada um com assinatura `DATAV1.0`. Existem duas cópias de `Main.data`; a **ativa** é a segunda (a primeira é a variante fmt 1).

## Diretório MINFS
Registro: `u32 off, size, size2, attr` + `u32 (namelen | flags<<16)` + nome (alinhado a 4). Arquivos `.mod` comprimidos têm bytes extras (tabela de blocos). `tools/dataf.py: dir_records()` varre `ROOTFS+0..0x5000` (179 registros).
Superbloco `MINFS` em `ROOTFS+0`: `u32@0x18` = "usado" = fim do último arquivo − `0x4A00`; `u32@0x1C` = tamanho da partição (`0xDF0000`).
O último arquivo (`vdec_com.plg`) termina em `0xCBAA4C`: sobram **~1,2 MB livres** no fim do ROOTFS.

## Reconstruir um `.data` com tamanhos novos
Tabela em `u32@0x14`: `u32 contagem` + pares `(offset, clen)`; cada item = 24 B de cabeçalho + fluxo zlib. Basta recomprimir e reescrever a tabela (`dataf.rebuild`, verificado byte a byte nos 71 arquivos). O arquivo cresce → **realocar** no fim livre (ou em "buracos") e atualizar `off/size/size2` do registro e o campo "usado" do superbloco. Assim **o limite de "mesmo tamanho de zlib" do doc 04 deixa de existir** quando a atualização é feita por `LTTF133.img`.
Exemplo completo: `examples/carplay_dark/make_pack.py`.
