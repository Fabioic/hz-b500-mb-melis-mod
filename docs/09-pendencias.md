# 09 — Pendências

- [x] `\Update\Config.ini` pelo pendrive — **funciona** (doc 10).
- [x] Formato do `LTTF133.img` — **resolvido** (doc 10).
- [x] `animationType=1` — funciona (deslize suave). Outros valores: não testados.
- [ ] **Painel da bolinha não fecha sozinho** (volume/home/desligar). `idleReturnTime` não influencia; temporizador não encontrado no código (só `lib_auto_hide`, do Android Auto). Opção: localizar o tratador do clique em `ViewShowButtonDot` e aplicar patch no módulo via `LTTF133.img`.
- [ ] Caixa quadrada atrás da bolinha ao clicar (mesmo com fmt 3 e alfa 0–31 correto): em teste (pacote F/G deixa o RGB transparente da bolinha em branco como no original).
- [ ] Serrilhado nas bordas do painel/ícones: re-testar após corrigir o alfa de 5 bits.
- [ ] Papéis de parede JPEG 1280×480 (slots), barra superior/fundos.
- [ ] Reconexão automática do emissor Bluetooth KCX.
- [ ] Outras placas/versões: compare offsets e envie correções.
