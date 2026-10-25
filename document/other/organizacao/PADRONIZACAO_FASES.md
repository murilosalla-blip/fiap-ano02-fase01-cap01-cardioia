# Nossa padronização das fases no modelo FIAP

Revisamos a organização em 24/10/2026 a partir do commit `ff54c72`, na branch `codex/padronizar-fases-fiap`.

## O que alteramos

- Agrupamos o código em `src/fase1`, `src/fase2` e `src/fase3`, incluindo o portal dentro da Fase 2.
- Agrupamos os dados, imagens e textos originais em `assets/fase1`; preservamos seus conteúdos e os links externos.
- Agrupamos os documentos principais da Fase 1 em `document/fase1` e suas referências em `document/other/referencias/fase1`.
- Acrescentamos os requisitos da preparação em `config/fase1` e concentramos a conferência de preservação em `scripts/fase1`.
- Retiramos as entradas transitórias da raiz com renomeações Git para `document/other/historico/entradas_transitorias`. Mantivemos o conteúdo anterior versionado, sem arquivar código-fonte em uma pasta ignorada.
- Atualizamos os guias, notebooks, requisitos e workflows para os novos caminhos. Preservamos todos os 18 endereços externos originais.

## Execução local da Fase 3

Preparamos um migrador que copia os arquivos de execução sem apagar a origem, preserva dados confirmados no WAL do SQLite e recusa sobrescrever um destino existente. Conferimos esses comportamentos em dois testes.

Pausamos somente o painel e o consumidor deste projeto. Copiamos e conferimos os quatro bancos: `mqtt_live.sqlite3` com 145 amostras, `telemetria.sqlite3` com 123 amostras e dois bancos de ensaio com duas amostras cada. Preservamos também os logs e demais arquivos de execução. Reiniciamos o painel e o consumidor pelos caminhos atuais e confirmamos HTTP 200 e broker conectado.

Mantemos a execução atual em `.tools/runtime/fase3` e o estado anterior em `.tools/backups/estrutura_anterior/fase3/runtime`, fora do Git. O histórico em memória do painel reinicia junto do serviço; os registros persistidos continuam no SQLite.

Para migrar outra cópia já utilizada, encerramos primeiro o painel e o consumidor antigos e executamos, na raiz do projeto:

```powershell
python scripts/fase3/migrar_runtime.py
node scripts/fase3/iniciar_dashboard.js --com-consumidor
```

Em uma cópia nova, seguimos diretamente a instalação e inicialização do guia; não precisamos migrar um banco inexistente. Não repetimos a migração sobre um destino com dados.

## Publicação e verificação

Uso `src/fase2/app.py` como entrada padronizada do Streamlit e mantemos `src/fase2/requirements.txt` junto dela. O [perfil público do Streamlit](https://share.streamlit.io/user/julia-carvalho96) apontou a aplicação para o [repositório da Julia](https://github.com/Julia-carvalho96/fiap-ano02-fase01-cap01-cardioia). Confirmamos pela API do GitHub que esse repositório é um fork separado deste projeto. Preservamos esse vínculo e suas configurações; a alteração desta branch não modifica o código publicado naquele fork.

Conferimos a preparação dos 303 registros da Fase 1 e os 223 arquivos protegidos do manifesto original. Conferimos também os 14 testes anteriores de Python da Fase 3, os dois testes de migração e os 19 testes do painel. Também passamos nos testes de NLP e do aplicativo Streamlit usando o novo caminho dos dados da Fase 1, nos sete testes do portal e no build de produção em sua nova pasta. Conferimos as saídas preservadas dos quatro notebooks e a sintaxe dos quatro workflows. No ensaio MQTT do novo diretório local, confirmamos duas medições únicas, duas duplicatas, uma confirmação omitida e um conflito rejeitado. Registramos 191 renomeações e conferimos os 397 destinos anteriores, os 310 conteúdos protegidos e todos os endereços externos originais.
