# 06 — `CONFIG.INI`, UDISK e atualização por pendrive

## UDISK
`fwtool.py udisk backup.bin saida/` extrai o volume FAT12 (`0xF90000`): `CONFIG.INI`, `CONFIG~1.BIN`, `SAVE/` (estados salvos, pareamentos BT em `SAVE/BT`, `SDSAVE.DAT`…) e `CARPLAY/*.KEY`
(**chaves de pareamento — nunca publique**).

## `CONFIG.INI` (texto puro) — chaves de interesse
| Seção | Chave | Observação |
|---|---|---|
| `[SETUP]` | `animationType` | tipo de animação das transições (valores possíveis desconhecidos; não aparece no menu) |
| `[SETUP]` | `idleReturnTime`, `bScreenSave`, `bright/contrast/hue/saturation`, `language`, `wallPaper`, `b12Hour`, `bBeepOn` | |
| `[CONFIG]` | `uiType`, `uiBpp`, `screenResolution`, `maxVolume`, `defaultSource`, `bToastAsTip`, `saveMethod` | |
| `[STARTUP]` | `startUpDefVolume`, `startUpMinVolume`, `startUpMaxVolume`, `startUpDelayTime`, `startUpVideoPath` | |
| `[LINK]` | `linkVideoWidth/Height` (1280×480), `carplayIconLabel`, `echoDelayTime`, `micGain`, `wifiChannel`… | |
| `[BACKLIGHT]` | `backLightDay/Night`, `backLightMode`, `backLightMinValue` | |
| `[BT]` | `btLocalName`, `btMicGain`, `bBtLocalNameUnique` | |
| `[MAINKEY]/[SCREENKEY]` | teclas físicas e botões na tela | |

Há ainda senhas de fábrica no arquivo (`logoPassword`, `factoryPaswword`); são padrões do fabricante, **não** as inclua em issues públicas.

## Atualização por pendrive
Testada: veja [`10-atualizacao-usb-img.md`](10-atualizacao-usb-img.md) (`\Update\Config.ini` e `\Update\LTTF133.img` funcionam).
Também existem `stalogo.jpg`, `gt911.cfg` e `UI<n>\Config.ini` (ainda não testados).
