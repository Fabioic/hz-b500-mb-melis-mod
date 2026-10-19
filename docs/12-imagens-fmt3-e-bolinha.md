# 12 — Formatos de imagem: lições (fmt 1 × fmt 3) e a bolinha

- **fmt 3 = RGB565 + alfa de 5 bits.** Em todos os itens originais o byte de alfa vai de **0 a 31** (centro opaco = 31), não 0–255. Gravar 0–255 produz caixa preta atrás da bolinha, bordas serrilhadas e ruído. Codifique `alfa = round(a*31/255)`.
- Pixels totalmente transparentes: nos tiles/ícones `Main.data` o RGB é `0`; nos 60×60 da bolinha o original usa `0xFFFF` (branco).
- **fmt 1 (BGRA 32 bits)** na central (uiBpp=24) mostrou quadrado preto e granulado: não use; fique em fmt 3.
- Dithering Floyd–Steinberg em RGB565 deu painel ruidoso/serrilhado: prefira cores chapadas e bordas anti-aliasadas.
- Papéis em cada janela com bolinha (arquivos `AndroidWireless, AndroidAuto, MainLinkCarPlay, MirrorIphone, CarPlay, MirrorAndroid, AirPlay, MainLinkAuto`), relativo ao painel 400×240 (índice p): `p-2/p-1` bolinha 60×60 (ativa/inativa), `p+1..p+6` ícones 54×54 (volume, home, desligar, normal/ativo), `p+7/p+8` trilho 320×26, `p+9` botão 26×26 (`MirrorIphone`/`MirrorAndroid` têm um item 96×96 extra no início).
- Estilo "CarPlay Dark" (ícones squircle, cartões escuros) em `examples/carplay_dark/`.
- Os dígitos do relógio são desenhados pelo firmware sobre o centro do tile da data (y≈105–140 de 300); não coloque ícone ali.
