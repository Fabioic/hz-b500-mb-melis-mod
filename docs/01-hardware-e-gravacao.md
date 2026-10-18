# 01 — Hardware e gravação (CH341A)

## Placa
- Placa **HZ-B500-MB V2.12**, SoC **Allwinner F133-B** (RISC-V C906), flash SPI NOR **Winbond W25Q128FV (16 MB)**.
- Sistema operacional: **Melis 4.x** (RTOS da Allwinner). Executáveis `.mod` carregados pelo sistema.
- Apenas **uma porta USB host** (usada para pendrive e para o celular). Não há porta para PC, então gravar via PhoenixSuit é improvável.
- Há também um **MCU** separado (atualizado por "Update MCU"; **não mexa**).

## Leitura e gravação com CH341A + clipe SOIC8
1. **Central desligada e sem 12 V** durante todo o processo (o clipe alimenta o chip em 3,3 V).
2. Confira com multímetro que o adaptador entrega **3,3 V** (alguns CH341A entregam 5 V no pino de dados; use adaptador com regulador/nível 3,3 V).
3. No soquete do programador, o chip de 8 pinos 25xx vai na fileira **25XX** (a de cima, perto do USB), pino 1 no canto superior esquerdo desse grupo. Jumper em 1-2 (modo programação).
4. Programa: **AsProgrammer** (ou flashrom). Chip: `W25Q128FV`.
5. **Sempre**: ler o chip duas vezes e comparar CRC32 antes de gravar qualquer coisa. Guarde o backup original em lugar seguro.

## Ordem segura para gravar
`Abrir arquivo` → **Apagar** (esperar "Pronto") → **Programar** → **Verificar**.
Programar sem apagar dá erro de verificação (a flash só muda bits de 1 para 0).

## Se travar
Basta regravar o último arquivo bom (ou o backup original). Enquanto o **boot0** (início da flash) não for alterado, a recuperação pelo CH341A sempre é possível.
