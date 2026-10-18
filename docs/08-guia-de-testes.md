# 08 — Guia de testes

1. Backup completo (2 leituras com CRC32 igual).
2. Mude **uma coisa por vez** a partir do backup (ex.: um ícone). Gere o `.bin` e confira que só os bytes esperados diferem (`cmp -l`).
3. Grave: apagar → programar → verificar. Ligue a central e confira.
4. Documente: foto da tela, versão da placa, CRC32 do arquivo gravado.
5. Se algo falhar, regrave o backup. Não toque em `0x0–0x1A0000`.
