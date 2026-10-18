# 02 — Layout da flash (16 MB)

| Faixa | Conteúdo |
|---|---|
| `0x000000` | **boot0** (`eGON.BT0`) — verifica o checksum da imagem de boot. **Não alterar.** |
| `0x00C200` | cabeçalho GPT (base das partições = `0xC000`; início = `0xC000 + LBA*512`) |
| `0x010000–0x1A0000` | **bootA**: pacote `melis-lzma`, kernel LZMA (formato *alone*) em `0x10400`, ~3,3 MB descomprimido. **Não alterar** (checksum). |
| `0x1A0000–0xF90000` | **ROOTFS** (MINFS): apps, módulos, UI, idiomas, logos |
| `0xF90000–0x1000000` | **UDISK**: FAT12 de ~220 KB com `CONFIG.INI`, `SAVE/`, pareamentos Bluetooth/CarPlay |

Notas:
- Gravar a flash inteira **sobrescreve a UDISK** (configurações salvas, pareamentos). Para preservar, grave só o intervalo desejado.
- Existe uma segunda cópia do `CONFIG.INI` perto de `0xFD06CC` (fora do volume FAT12): provável cópia de segurança (`BackupConfig`). Ao editar a config no binário, altere as duas.
- Ferramenta: `fwtool.py info`.
