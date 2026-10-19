# 13 — Outros projetos com a mesma plataforma (varredura de 18/10/2026)

Pesquisa feita para saber quem mais está trabalhando em mods para centrais **Allwinner F133/D1s + Melis 4.0** (família HZ-B500 / B5300). Resumo do que cada um documenta; confira nas fontes.

## Gamadril — mesma placa HZ-B500-MB (mais próximo deste projeto)
- Projeto no Hackaday.io: *Reverse Engineering F133/D1s device* (<https://hackaday.io/project/205793-reverse-engineering-f133d1s-device>). Central de 7", F133, 64 MB RAM, flash NOR de 16 MB, Melis RTOS. Objetivo: ligar ao CAN do carro mantendo CarPlay/Android Auto.
- **d1s-melis-tools** (<https://github.com/Gamadril/d1s-melis-tools>, MIT): `dump_tool` (extrair/reempacotar dump), `img_tool` (extrair/reempacotar `.img` IMAGEWTY, nome padrão `LTTF133.img`), `data_renderer` (arquivos `.data` da interface). Confirma o layout que documentamos (boot0 + GPT em `0xC000` + bootA/ROOTFS/UDISK) e o mecanismo `\Update\LTTF133.img`.
- **hz-b500-mods** (<https://github.com/Gamadril/hz-b500-mods>, MIT): módulo `canbus.mod` (volante BMW E90, overlay de distância de estacionamento), ponte CAN→UART com ESP32-C3 e um script que sobe o ganho de áudio do Android Auto em `wireless.mod`/`auto.mod` (o valor 60 vira até 100).
- Descobertas úteis que **ainda não testamos aqui**:
  - Logo de abertura **sem mexer no firmware**: pendrive com pasta `Logo/` contendo o JPEG; em *Ajustes → Configurações de fábrica* o código `112233`; escolher a imagem (copiada para a UDISK como `stalogo.jpg`).
  - Android Auto **só com fio**: `btPairMode=1` na seção `[BT]` do `Config.ini` (entrada em *Configurações de fábrica* `113266`).
  - Códigos de fábrica: `113266` fábrica, `112345` debug, `001106` fábrica estendida, `230762` seleção de interface, `123579` auto-teste, `000000` atualização de firmware.
  - **Recuperação por FEL** (USB OTG, ferramenta `xfel`): permite despejar/regravar a flash sem programador SPI — mais seguro que depender só do CH341A.
  - Melis 4.0 com UART de depuração a 500 kbaud.

## dan-os / B5300-reverse-engineering
- <https://github.com/dan-os/B5300-reverse-engineering> — central B5300 (FCC 2BD44-B5300), F133-B + Melis 4.0, "tentativa de hobby". Logs de UART, os mesmos códigos de fábrica e tutoriais de extrair/reempacotar/gravar. Cita um tópico do fórum 4pda sobre central F133 semelhante.

## fuho / moto-display-re
- <https://github.com/fuho/moto-display-re/blob/main/WRITEUP.md> — central de moto "M553" com F133-B e Melis 4.0, mesma família de SDK ("SK1.4"). Ainda sem dump da flash; documenta símbolos de `init.axf`, atualização de MCU por cartão e o formato IMAGEWTY de firmwares irmãos.

## Fóruns
- elektroda.com: tópico sobre uma F133-B "F18-V3.2" com atualização falha (<https://www.elektroda.com/rtvforum/topic4169384.html>) — sem imagem verificada, só dicas de recuperação (CH341A, FEL). A página do HZ-B500-MB VER2.1 (<https://www.elektroda.com/qa,hz-b500-mb-ver21-carplay-mp5-firmware.html>) não traz firmware nem mods.

## O que este projeto traz de diferente
Até onde encontramos, ninguém documentou: **troca de ícones/tiles/bolinha com recomposição dos `.data` e realocação no MINFS** (docs 11–12), o fato de o **alfa do fmt 3 ter 5 bits**, a **lista de idiomas feita de imagens** (doc 07) e o **tema "CarPlay Dark/vibrante"**. Vale propor integração com o `data_renderer`/`img_tool` do Gamadril.
