# 04 — Interface (`Main.data`) e imagens

`/apps/UI2/Data/Main.data` contém **75 "arquivos" DATAV1.0** em sequência (assinatura `DATAV1.0` em UTF-16LE).
Cada um corresponde a uma tela/janela e tem:

1. **Cabeçalho de layout** (UTF-16 + inteiros): nomes dos controles (`ViewShowWndVideoUi`, `ViewShowButtonDot`, `ViewShowSliderVolume2`…),
   posição x/y, largura/altura, ids de imagem, cores. Isto significa que **posição e tamanho dos controles são editáveis**.
2. **Itens de imagem**, um atrás do outro: cabeçalho de 24 bytes `<6I` = `24, largura, altura, formato, compressão (3 = zlib), x`, seguido do fluxo **zlib**.

## Formatos de pixel
| fmt | Significado | Tamanho bruto |
|---|---|---|
| 1 | BGRA8888 | `w*h*4` |
| 2 | RGB565 little-endian (sem alfa) | `align4(w*2)*h` |
| 3 | **RGB565 + A8 intercalado por pixel** (`lo, hi, alfa`) | `align4(w*3)*h` |

(O `align4` aplica-se à linha. Até o fim da pesquisa achávamos que fmt 3 era "planar"; o correto é intercalado.)

## Interface ativa
A central usa a variação em **fmt 3** (arquivo 14: tiles hexagonais 204×300, ícones 170×120, dígitos 28×28). O arquivo 0 traz a variação
alternativa em fmt 1 (provável opção "Seleção da interface" nas configurações). Itens normais e "selecionados" ficam em pares consecutivos.
Janelas dos botões flutuantes/menu de volume ficam nos arquivos `1, 13, 26, 44, 49, 52, 56, 67` (mesma estrutura em todos): bolinha 60×60 (×2),
painel 400×240, ícones 54×54 (volume, mudo, home, home pressionado, desligar, desligar pressionado), barra 320×26 (×2), botão deslizante 26×26.

## Trocar uma imagem sem quebrar nada
O firmware localiza os itens pelo layout; **mudar o tamanho do fluxo zlib desloca tudo**. A técnica usada:
recomprimir a nova imagem e **preencher até o tamanho exato do fluxo original**, inserindo blocos *stored* vazios (`00 00 00 ff ff`)
logo após o cabeçalho zlib de 2 bytes, escolhendo nível/memLevel/estratégia que dê `tamanho ≡ alvo (mod 5)`.
Se não couber, reduza a entropia: menos bits de cor (8→3) e alfa quantizado. Imagens simples (cor chapada, cantos suaves) cabem; degradês detalhados podem não caber.

```bash
python3 tools/fwtool.py ui-list    backup.bin | grep '^14\.'
python3 tools/fwtool.py ui-export  backup.bin png/
python3 tools/fwtool.py ui-replace backup.bin novo.bin 14.4 meu_icone.png   # 170x120, mesmo tamanho
```
Papéis de parede são JPEG 1280×480 em slots separados (miniaturas 160×60); o mesmo princípio de "mesmo tamanho" vale.
