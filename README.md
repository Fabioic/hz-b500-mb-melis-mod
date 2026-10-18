# HZ-B500-MB — personalização do firmware (Melis / Allwinner F133)

Documentação e ferramentas de engenharia reversa para a central multimídia portátil **CarPlay / Android Auto**
com placa **HZ-B500-MB V2.12** (SoC Allwinner **F133-B**, RISC-V, flash SPI **W25Q128FV 16 MB**, sistema **Melis 4.x RTOS**),
vendida sob várias marcas genéricas.

> **Aviso.** Gravar flash pode deixar a central sem funcionar até ser regravada. Sempre faça e guarde um **backup completo**
> da flash antes de qualquer coisa. Tudo aqui é feito por conta e risco de quem usa. Este projeto **não** distribui firmware
> do fabricante: não publique dumps (contêm chaves de pareamento e dados pessoais). Use as ferramentas no **seu** backup.

## O que já foi feito (e funciona)

| Mudança | Como | Status |
|---|---|---|
| Logo de abertura própria | trocar `stalogo1.jpg` (2 cópias) mantendo o tamanho | testado |
| Tradução / correção de textos (pt-BR) | editar as tabelas `/apps/Language/*.txt` (mesmo tamanho) | testado |
| Emissor Bluetooth (KCX) na saída AUX | hardware externo | testado |
| Atualização por **pendrive** (`\Update\LTTF133.img` e `\Update\Config.ini`) | formato IMAGEWTY documentado | **testado** (doc 10) |
| Ícones/tiles estilo iOS e "CarPlay Dark" | recriar `.data` e realocar no ROOTFS (docs 11–12) | aplicado na central; refinamento em andamento |
| Bolinha flutuante e menu de volume/home/desligar | idem | aplicado; quadrado atrás da bolinha em investigação |
| Animações de transição | `animationType=1` no `CONFIG.INI` | **testado** (deslize suave) |
| Nome "Português BR" na lista de idiomas | imagem 200×30 em `SetupLanguage.data` (doc 07) | em teste |

## Conteúdo

- [`docs/01-hardware-e-gravacao.md`](docs/01-hardware-e-gravacao.md) — placa, CH341A, leitura/gravação, ordem segura.
- [`docs/02-layout-da-flash.md`](docs/02-layout-da-flash.md) — mapa da flash, partições, o que não tocar.
- [`docs/03-rootfs-minfs.md`](docs/03-rootfs-minfs.md) — sistema de arquivos ROOTFS e lista de arquivos.
- [`docs/04-interface-e-imagens.md`](docs/04-interface-e-imagens.md) — `Main.data` (DATAV1.0), formatos de imagem, como trocar com tamanho fixo.
- [`docs/05-modulos-e-codigo.md`](docs/05-modulos-e-codigo.md) — módulos `.mod` (LZMA em blocos), código RISC-V, padrão do programa.
- [`docs/06-config-ini-e-usb.md`](docs/06-config-ini-e-usb.md) — `CONFIG.INI`, partição UDISK, atualização por pendrive.
- [`docs/07-textos-e-idiomas.md`](docs/07-textos-e-idiomas.md) — tabelas de idiomas.
- [`docs/08-guia-de-testes.md`](docs/08-guia-de-testes.md) — como testar uma mudança com segurança.
- [`docs/09-pendencias.md`](docs/09-pendencias.md) — o que ainda não se sabe.
- [`docs/10-atualizacao-usb-img.md`](docs/10-atualizacao-usb-img.md) — atualização por pendrive (`LTTF133.img`, `Config.ini`).
- [`docs/11-minfs-dados-e-relocacao.md`](docs/11-minfs-dados-e-relocacao.md) — 71 arquivos `.data`, registros MINFS, realocação.
- [`docs/12-imagens-fmt3-e-bolinha.md`](docs/12-imagens-fmt3-e-bolinha.md) — fmt 3 (alfa 5 bits), fmt 1, bolinha/painel.
- [`tools/dataf.py`](tools/dataf.py), [`tools/build_img.py`](tools/build_img.py), [`examples/carplay_dark/`](examples/carplay_dark/) — reconstrução de `.data`, gerador do `.img`, pacote CarPlay Dark.
- [`tools/fwtool.py`](tools/fwtool.py) — ferramenta única (info, ls, extract, ui-list/export/replace, mods, udisk).
- [`examples/ios_icons.py`](examples/ios_icons.py) — gerador dos ícones estilo iOS usados nos testes.

## Começando

```bash
pip install numpy pillow
python3 tools/fwtool.py info    meu_backup.bin
python3 tools/fwtool.py ls      meu_backup.bin
python3 tools/fwtool.py udisk   meu_backup.bin saida/udisk     # CONFIG.INI etc. (não publique!)
python3 tools/fwtool.py ui-export meu_backup.bin saida/png      # todas as imagens da interface
python3 tools/fwtool.py ui-replace meu_backup.bin novo.bin 13.1 minha_imagem.png
```

Contribuições são bem-vindas: confirme em outras placas/versões, corrija erros e documente novas descobertas.
