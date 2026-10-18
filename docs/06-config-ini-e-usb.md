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

## Atualização por pendrive (descoberta em strings; **ainda não testada**)
O programa procura, no dispositivo USB/SD, a pasta `\Update\` com:
- `Config.ini` (e `UI<n>\Config.ini`) → "UpdateConfig"; `stalogo.jpg` (logo); `gt911.cfg` (calibração do touch); `no_update_config` (marcador para não sobrescrever); `\Update\<arquivo>` genérico (cópia).
- `appUpdateFile` (padrão **`LTTF133.img`**) e `mcuUpdateFile` (padrão `LTTMcu.bin`) — nomes configuráveis em `CONFIG.INI`.
- O botão "Atualizar APP" usa `CarApi_CheckImage` + `update.mod`. O formato do `.img` ainda é desconhecido.
