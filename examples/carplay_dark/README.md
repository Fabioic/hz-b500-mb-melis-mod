# Tema CarPlay Dark / vibrante

`make_pack.py base.bin saida.bin r565` regrava, num backup **seu**, os tiles/ícones do menu (`darkset.py`, `glyphs2.py`, `icons.py`), a bolinha e o painel (`ballmenu.py`), o nome "Português BR" (imagem em `SetupLanguage.data`) e os textos "Transmissor FM". Depois use `tools/build_img.py` para gerar o `Update/LTTF133.img`.

Observações: `glyphs2.g_phone2` lê `ref_phone_mask.png` (silhueta branca do fone sobre preto) que **não** é distribuída aqui; forneça a sua. Alfa do fmt 3 = 0–31 (doc 12).
