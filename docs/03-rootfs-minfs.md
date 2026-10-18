# 03 — ROOTFS (MINFS)

Particao em `0x1A0000`. A listagem raiz começa em `ROOTFS+0x200`.

Cada registro: `u32 offset, u32 size, u32 size2, u32 attr` (offsets relativos ao início do ROOTFS), depois `u32` com
**tamanho do nome** nos 16 bits baixos e flags nos altos, depois o nome, preenchido a múltiplos de 4.
Diretórios têm `attr & 0x10000`; offset/size apontam para uma sub-listagem.
Arquivos comprimidos (`.mod`; `size != size2` ou flag `0xa0/0xc0`) trazem dados extras após o registro.

Arquivos úteis (nem todos listados pelo parser; veja `fwtool.py ls`):

| Caminho | Notas |
|---|---|
| `/startup.sh` | `insmod d:\apps\desktop.mod` |
| `/apps/UI2/Data/Main.data` | todos os recursos de interface (veja doc 04), ~640 KB |
| `/apps/Language/*.txt` | tabelas de idioma por aplicativo (UTF-16LE, separadas por TAB) |
| `/apps/CarPlay/icon_*.png` | ícones do CarPlay (120/180/256) |
| `/res/stalogo1.jpg` | logo de abertura (existe uma segunda cópia na flash) |
| `/etc/cedarx.conf` | parâmetros do player |
| `/mod/*.mod`, `/apps/desktop.mod` | módulos (comprimidos; veja doc 05) |

`CarPlay.exe` e `AndroidAuto.exe` são stubs de 27 bytes; a lógica está nos módulos.
