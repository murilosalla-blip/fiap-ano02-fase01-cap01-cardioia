# Documentação do CardioIA

Organizamos os documentos exigidos pelas atividades dentro de `document/fase1/`, `document/fase2/` e `document/fase3/`. Reservamos `document/other/` para referências, estudos, auditorias, registros de testes e cópias históricas, conforme a finalidade indicada no modelo FIAP.

## Documentos principais por fase

| Fase | Guia atual e requisitos | Documento da entrega | Situação |
|---|---|---|---|
| 1 | [README e fontes](fase1/README.md), guias numérico, textual e visual na mesma pasta | [Documento da Fase 1 — cinco páginas](fase1/cardioia_fase1_entrega_fiap.pdf) | Preservamos o documento da entrega anterior |
| 2 | [README e reprodução](fase2/README.md), [checklist](fase2/CHECKLIST_ENUNCIADO.md), [relatório de apoio](fase2/RELATORIO_ENTREGA.md) | [Documento de submissão da Fase 2 — seis páginas](fase2/CardioIA_Fase2_Documento_de_Submissao.pdf) | Preservamos o documento consolidado da entrega anterior |
| 3 | [README e reprodução](fase3/README.md), [matriz de requisitos](fase3/CHECKLIST_ENUNCIADO.md), [roteiro](fase3/ROTEIRO_ENTREGA.md) | Relatório Edge ≥1 página; MQTT/dashboard ≥2 páginas; REST/e-mail 1–2 páginas; comparação de modelos 2 páginas | **Ainda precisamos produzir os quatro relatórios e concluir os desafios** |

O [AI Project Document](ai_project_document_fiap.md) apresenta a evolução consolidada. O [README raiz](../README.md) identifica o grupo, explica as fases, mantém os links públicos e orienta a execução.

## Originais e caminhos atuais

Preservamos os PDFs anteriores sem reescrever conteúdo, autoria, métricas ou caminhos da época. Para reproduzir hoje, utilizar os READMEs atuais. Os PDFs podem citar a organização antiga:

| Caminho anterior | Organização atual |
|---|---|
| `assets/dados/`, `assets/textos/`, `assets/imagens/ecg/` | Mesmas modalidades dentro de `assets/fase1/` |
| `scripts/preparar_dataset_numerico.py` e `scripts/preparar_amostra_ecg.py` | `src/fase1/` |
| `document/other/documentacao/` da Fase 1 | Guias principais em `document/fase1/`; referências em `document/other/referencias/fase1/` |
| `fase2/` na raiz | Código em `src/fase2/`, dados/resultados em `assets/fase2/`, requisitos em `config/fase2/` e guias em `document/fase2/` |
| `portal-cardioia/` na raiz | `src/fase2/portal-cardioia/`; publicação independente preservada |

O [mapa de arquivos](other/organizacao/mapa_arquivos.json) e o [registro da padronização](other/organizacao/PADRONIZACAO_FASES.md) detalham os destinos. Arquivamos versões anteriores em `other/historico/`; elas não substituem o guia de execução atual.

## Referências e registros de apoio

- [Enunciados e materiais de aula por fase](other/referencias/README.md).
- [Revisão dos enunciados, READMEs e documentos submetidos](other/organizacao/REVISAO_DOCUMENTACAO.md).
- [Organização e verificação de preservação](other/organizacao/README.md).
- [Evidências dos testes da Fase 3](other/fase3/evidencias/).

Registramos requisito, arquivo, evidência e situação sem confundir plano, teste e entrega concluída. Os registros e capturas da Fase 3 apoiam os relatórios, mas não substituem seus mínimos de páginas nem o envio na plataforma FIAP.
