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
| Ícones e tiles estilo iOS | trocar imagens de `Main.data` com tamanho fixo | prévia validada; teste na central em andamento |
| Nova bolinha flutuante e menu de volume/home/desligar | idem | prévia validada |
| Animações de transição | chave `animationType` no `CONFIG.INI` | **não testado** |

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
