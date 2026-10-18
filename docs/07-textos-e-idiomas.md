# 07 — Textos e idiomas

`/apps/Language/*.txt` (Main, Setup, Link, Bt, Radio, Video, Player, Calendar, Calculator, CarRecorder, Can, TipBox, SystemBar): **UTF-16LE**, linhas `{<TAB>col1<TAB>col2…<TAB>}`.
Colunas (0 = `{`): 1 chinês (chave), 2 inglês, 3 zh-CN, 4 zh-TW, 5 fr, 6 de, 7 ar, 8 it, 9 ja, **10 pt**, 11 ru, 12 es, 14 he, 15 fa, 16 pt (variante), 17 pl, 18 tr, 19 cs, 20 ko, 21 id, 22 th, 23 uk, 25 el, 27 nl.

- A central mostrou a **coluna 10** mesmo com "Português BR" selecionado; ajuste a 10 (e a 16 por garantia).
- Células entre aspas mantêm as aspas. O texto novo deve ter **o mesmo tamanho ou menor** (complete com espaços) para não deslocar o ROOTFS; textos longos podem estourar o espaço do controle na tela.
