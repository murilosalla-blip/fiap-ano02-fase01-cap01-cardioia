# Fase 1 — Batimentos de Dados

Reuni dados numéricos, textuais e visuais para preparar as etapas seguintes do CardioIA. Preservo os datasets, as amostras e os scripts dessa entrega nos caminhos já utilizados.

## Documentação e entrega

- [Dados numéricos](../other/documentacao/parte1_dados_numericos.md)
- [Dicionário das variáveis](../other/documentacao/parte1_dicionario_variaveis.md)
- [Dados textuais](../other/documentacao/parte2_dados_textuais.md)
- [Dados visuais](../other/documentacao/parte3_dados_visuais.md)
- [Plano da Fase 1](../other/documentacao/plano_execucao.md)
- [Documento submetido](cardioia_fase1_entrega_fiap.pdf)
- [Enunciado e referências das aulas](../other/referencias/fase1/)

## Materiais externos da entrega

Preservo os endereços compartilhados na entrega original:

- [Parte 1 — Dados Numéricos](https://drive.google.com/drive/folders/1I_gzbCuJUYvx0lwPtg5XhDf-IH039t2s?usp=sharing)
- [Parte 2 — Dados Textuais](https://drive.google.com/drive/folders/1Qc5W_RoAIq1sopROYvCss5uBwO0IlI6C?usp=sharing)
- [Parte 3 — Dados Visuais](https://drive.google.com/drive/folders/135ZuObt02AxX13aiQG_sqef9nxAjkPMy?usp=sharing)

## Reprodução dos scripts

Executo os comandos a partir da raiz do repositório. Sigo os pré-requisitos e a preparação dos dados descritos nos documentos de cada modalidade.

```powershell
python scripts/preparar_dataset_numerico.py
```

Para preparar novamente as imagens, baixo e extraio a base bruta indicada no guia visual, ajusto `RAW_DIR` em `scripts/preparar_amostra_ecg.py` e executo `python scripts/preparar_amostra_ecg.py`. Essa preparação depende da base bruta local; mantenho a amostra já entregue disponível em `assets/imagens/ecg/`.

Preservo o recorte original do documento principal da Fase 1 no [histórico](../other/historico/fase1/document/ai_project_document_fiap.md). Acompanho a evolução das três fases no [documento consolidado](../ai_project_document_fiap.md).
