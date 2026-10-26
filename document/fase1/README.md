# Fase 1 — Batimentos de Dados

Reunimos dados numéricos, textuais e visuais para preparar as etapas seguintes do CardioIA. Preservamos o conteúdo dos datasets e das amostras e organizamos seus caminhos em `assets/fase1/`, com código em `src/fase1/`, requisitos em `config/fase1/` e verificação em `scripts/fase1/`.

## Documentação e entrega

- [Dados numéricos](parte1_dados_numericos.md)
- [Dicionário das variáveis](parte1_dicionario_variaveis.md)
- [Dados textuais](parte2_dados_textuais.md)
- [Dados visuais](parte3_dados_visuais.md)
- [Plano da Fase 1](plano_execucao.md)
- [Documento submetido](cardioia_fase1_entrega_fiap.pdf)
- [Enunciado e fontes de referência](../other/referencias/fase1)

## Materiais externos da entrega

Preservamos os endereços compartilhados na entrega original:

- [Parte 1 — Dados Numéricos](https://drive.google.com/drive/folders/1I_gzbCuJUYvx0lwPtg5XhDf-IH039t2s?usp=sharing)
- [Parte 2 — Dados Textuais](https://drive.google.com/drive/folders/1Qc5W_RoAIq1sopROYvCss5uBwO0IlI6C?usp=sharing)
- [Parte 3 — Dados Visuais](https://drive.google.com/drive/folders/135ZuObt02AxX13aiQG_sqef9nxAjkPMy?usp=sharing)

## Como reproduzir

Os datasets finais e os dois textos já estão preparados. **Não é necessário executar os scripts para avaliar os materiais entregues.** Conferir os documentos acima, as três pastas públicas e os arquivos versionados:

| Parte e requisito | O que verificar |
|---|---|
| Numérica: pelo menos 100 linhas, CSV ou XLSX | `assets/fase1/dados/processed/heart_disease_cleveland.csv`: 303 registros; fonte real Cleveland e dicionário documentados. A exigência de formato aparece também em imagem no enunciado original. |
| Textual: pelo menos dois TXT | `assets/fase1/textos/texto_01_prevencao_cardiovascular.txt` e `texto_02_sindromes_coronarianas_agudas.txt`; contexto e aplicações de NLP no guia textual. |
| Visual: pelo menos 100 JPG ou PNG | `assets/fase1/imagens/ecg/`: 120 JPG, 30 por categoria; manifesto, privacidade e aplicações de visão computacional no guia visual. |

### Preparar uma cópia local

Instalar Git e Python 3.12. No PowerShell:

```powershell
git clone https://github.com/murilosalla-blip/fiap-ano02-fase03-cardioia.git
Set-Location -LiteralPath './fiap-ano02-fase03-cardioia'
python -m venv .venv
.\.venv\Scripts\python.exe scripts/fase1/verificar_preservacao.py
```

Se a cópia e o ambiente já existem, executar apenas a verificação a partir da raiz. Resultado esperado: **223 itens do inventário anterior: 212 arquivos locais e 11 PDFs de aulas identificados no histórico Git**. No Linux/macOS, criar com `python3.12 -m venv .venv` e usar `./.venv/bin/python` no lugar do executável Windows.

### Reproduzir a preparação numérica

```powershell
.\.venv\Scripts\python.exe src/fase1/preparar_dataset_numerico.py
```

O script utiliza bibliotecas nativas, lê a fonte em `assets/fase1/dados/raw/` e gera `assets/fase1/dados/processed/heart_disease_cleveland.csv`. Conferir 303 registros, o tratamento explícito de ausências e a variável-alvo binária derivada, conforme o [guia numérico](parte1_dados_numericos.md). O CSV final tem 14 colunas: 13 atributos de entrada e o diagnóstico convertido em alvo binário.

### Reproduzir a seleção visual

Esta etapa é opcional para avaliar a entrega já preparada e exige a fonte bruta externa:

1. Consultar a [fonte e licença das imagens](../other/referencias/fase1/parte3/fonte_dataset.md) e baixar a versão indicada do Mendeley Data.
2. Extrair a base na própria máquina. Os dados brutos completos não acompanham o clone.
3. Ajustar `RAW_DIR` em `src/fase1/preparar_amostra_ecg.py` para a pasta extraída, respeitando os nomes de subpastas da fonte.
4. Instalar Pillow e executar a preparação:

```powershell
.\.venv\Scripts\python.exe -m pip install -r config/fase1/requirements.txt
.\.venv\Scripts\python.exe src/fase1/preparar_amostra_ecg.py
```

Resultado esperado: 120 JPG distribuídos em quatro categorias e manifesto em `document/other/referencias/fase1/parte3/manifesto_amostra.csv`. O script remove duplicatas exatas e o cabeçalho administrativo; a rastreabilidade não comprova indivíduos distintos. A preparação pode regravar os derivados locais; para apenas avaliar, utilizar os arquivos já entregues.

### Conferir a documentação textual

Abrir os dois TXT sem treinamento obrigatório e ler [Dados textuais](parte2_dados_textuais.md). Documentamos autoria institucional, contexto, possíveis tarefas de NLP e limitações. A extração e a classificação implementadas posteriormente estão na Fase 2; não alteramos os textos originais da Fase 1 para produzir seus resultados.

Preservamos o recorte original do documento principal da Fase 1 no [histórico](../other/historico/fase1/document/ai_project_document_fiap.md). Acompanhamos a evolução das três fases no [documento consolidado](../ai_project_document_fiap.md).
