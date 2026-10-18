# 07 — Textos e idiomas

`/apps/Language/*.txt` (Main, Setup, Link, Bt, Radio, Video, Player, Calendar, Calculator, CarRecorder, Can, TipBox, SystemBar): **UTF-16LE**, linhas `{<TAB>col1<TAB>col2…<TAB>}`.
Colunas (0 = `{`): 1 chinês (chave), 2 inglês, 3 zh-CN, 4 zh-TW, 5 fr, 6 de, 7 ar, 8 it, 9 ja, **10 pt**, 11 ru, 12 es, 14 he, 15 fa, 16 pt (variante), 17 pl, 18 tr, 19 cs, 20 ko, 21 id, 22 th, 23 uk, 25 el, 27 nl.

- A central mostrou a **coluna 10** mesmo com "Português BR" selecionado; ajuste a 10 (e a 16 por garantia).
- Células entre aspas mantêm as aspas. O texto novo deve ter **o mesmo tamanho ou menor** (complete com espaços) para não deslocar o ROOTFS; textos longos podem estourar o espaço do controle na tela.

## A lista de idiomas na tela NÃO vem do texto
Os nomes mostrados em *Configurações → Idioma* (English, 中文, Español, Русский, **Portugal**, 日本語, Italiano…) são **imagens 200×30 (fmt 3)** em `SetupLanguage.data`, itens 3 a 24 (item 0 = fundo 930×436, 1–2 = 916×50). Mudar o texto no `Setup.txt` não altera a lista.
Ordem dos itens: 3 English, 4 Uighur, 5 Español, 6 Русский, **7 Portugal**, 8 日本語, 9 Italiano, 10 عربي, 11 Deutsch, 12 français, 13 繁体中文, 14 中文, 15 עברית, 16 Čeština, 17 Türkçe, 18 Polski, 19 Indonesia, 20 ภาษาไทย, 21 Українська, 22 한국어, 23 Nederlands, 24 Ελληνικά.
Para renomear, regere a imagem 200×30 (cor `0xE75D`/59229, alfa 0–31) e substitua o item 7. Em `Setup.txt` ainda é útil trocar `Portugal`→`Português BR` na coluna 2 (inglês) e na 23.
