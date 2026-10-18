# 05 — Módulos `.mod` e o código

## Formato
Os `.mod` do ROOTFS são **blocos LZMA** independentes. Cada bloco começa com `5d 00 80 00 00`
(propriedades `lc=3 lp=0 pb=2`, dicionário 32 KB) **sem** o campo de tamanho de 8 bytes do formato *alone*; use `FORMAT_RAW` + `FILTER_LZMA1` e alimente aos poucos
(o fim do bloco não é sinalizado, o decodificador acaba por dar erro). `fwtool.py mods` faz isso. Os blocos de um módulo são: tabela de relocação, código, dados.

## Arquitetura
Código **RISC-V RV64GC** (capstone `CS_ARCH_RISCV`, `RISCV64|RISCVC`). O módulo principal da interface = bloco grande de ~1,35 MB (código) seguido de ~480 KB (dados/strings).
Bibliotecas embutidas (libpng, FreeType, libplist/usbmuxd, mDNS, OpenSSL…) aparecem pelas strings.

## Padrão reconhecido
- Uma função gigantesca de inicialização chama, para cada controle, `FindView(&nomeJanela, "ViewShow…", tipo, &saída)` e guarda o handle em uma estrutura de contexto
  (`sw a0, off(ctx)`). Strings são referenciadas por `auipc/addi` (PC-relativo); o deslocamento texto→dados foi inferido por votação (`≈0x169454` neste firmware).
- Há centenas de *getters* triviais (`auipc; addi; ld; [lui; add]; lw a0,off(a5); ret`) que devolvem cada handle.
- Os nomes são mesclados pelo linker (sufixos compartilhados), então um nome pode ser referenciado por um ponteiro para o meio de outra string.
- A bolinha (`ViewShowButtonDot`) tem o handle gravado mas nenhum getter: o tratamento de clique parece genérico/por tabela. O **tempo de fechamento do menu não foi localizado**.

## Dicas
- `strings -n 5` nos blocos revela mensagens (`CarApi_*`, `CLink*`, `Config.ini`, `Update`…).
- Não edite código sem poder recomprimir no mesmo tamanho; o bootloader valida apenas o bootA, mas um módulo corrompido trava a inicialização.
