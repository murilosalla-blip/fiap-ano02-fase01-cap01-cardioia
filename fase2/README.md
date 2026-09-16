# Fase 2 — Diagnóstico automatizado com IA

Esta fase implementa os entregáveis obrigatórios de **NLP, extração de informações e classificação textual** do CardioIA. Como extensões, preserva o modelo tabular da base Cleveland, oferece uma interface demonstrativa em Streamlit, constrói o portal React + Vite do Ir Além 1 e implementa a MLP visual do Ir Além 2.

> **Uso exclusivamente educacional.** As bases textuais são simuladas, os modelos não possuem validação clínica e nenhuma saída deve orientar diagnóstico, urgência ou tratamento.

## Aplicação publicada

- **CardioIA:** https://cardioia-fiap.streamlit.app/
- **Arquivo:** `fase2/app.py`
- **Branch:** `fase-2-machine-learning`

A aplicação demonstra três modalidades independentes:

1. extração de sintomas por mapa de conhecimento;
2. classificação textual com TF-IDF;
3. classificação tabular histórica como extensão.

## Entrega obrigatória — Parte 1

### Relatos simulados

`fase2/dados/relatos_sintomas.txt` contém exatamente 10 relatos completos e distintos. Cada frase informa sintomas, início temporal e impacto na rotina.

### Mapa de conhecimento

`fase2/dados/mapa_conhecimento.csv` contém 25 associações organizadas nas colunas:

- `sintoma_1`;
- `sintoma_2`;
- `doenca_associada`;
- `nivel_prioridade`.

Os nomes representam associações didáticas, não diagnósticos.

### Extração

`fase2/src/extrair_sintomas.py`:

- normaliza caixa, acentuação, pontuação e espaços;
- identifica uma ou mais expressões;
- agrega associações do mapa;
- trata relatos sem correspondência;
- processa automaticamente as 10 frases.

## Entrega obrigatória — Parte 2

### Dataset textual

`fase2/dados/classificacao_risco.csv` possui 120 frases simuladas:

| Classe | Feminino | Masculino | Total |
|---|---:|---:|---:|
| Alto risco | 30 | 30 | 60 |
| Baixo risco | 30 | 30 | 60 |

Cada cenário possui versões feminina e masculina com o mesmo rótulo. O identificador `id_cenario` mantém as duas versões no mesmo conjunto durante a divisão, evitando vazamento entre exemplos quase equivalentes.

### Classificador

`fase2/src/classificar_risco_texto.py` implementa:

- divisão estratificada e agrupada por cenário;
- TF-IDF com unigramas e bigramas;
- Regressão Logística balanceada;
- acurácia, precisão, recall, F1 e ROC AUC;
- matriz de confusão;
- termos associados a cada classe;
- análise contrafactual por sexo;
- persistência do modelo e dos resultados.

### Resultado textual

O teste possui 24 frases pertencentes a 12 cenários nunca usados no treino.

| Métrica | Resultado |
|---|---:|
| Acurácia | 100,0% |
| Precisão — alto risco | 100,0% |
| Recall — alto risco | 100,0% |
| F1 — alto risco | 100,0% |
| ROC AUC | 1,000 |
| Maior diferença contrafactual por sexo | 0,0033 |

O desempenho perfeito não deve ser generalizado: a base é pequena, simulada e deliberadamente separável. O resultado apenas confirma o funcionamento do pipeline no conjunto demonstrativo.

### Notebook

`fase2/notebooks/classificacao_textual_tfidf.ipynb` apresenta dados, separação, TF-IDF, treinamento, métricas, matriz de confusão, termos influentes, análise de viés e limitações.

## Feedback da Fase 1

- **Desempenho demográfico:** o modelo tabular é avaliado separadamente por sexo e pelas faixas até 49 anos, 50–59 anos e 60 anos ou mais, sempre com tamanho do grupo e intervalos de confiança.
- **Viés textual:** pares contrafactuais verificam se o marcador feminino/masculino muda a previsão para sintomas equivalentes.
- **Separação:** registros tabulares são separados por paciente; pares textuais, por cenário; imagens, por hash de exame único.
- **Ausência de ID visual:** a fonte das imagens não fornece identificador de paciente, portanto a separação por indivíduo não pode ser garantida e é registrada como limitação.
- **Prevalência:** nenhum balanceamento textual ou visual é apresentado como prevalência clínica.
- **Modalidades:** texto, tabela e imagem possuem pipelines, métricas e notebooks independentes.

## Extensão tabular

A Regressão Logística e o Random Forest são comparados com a base Cleveland. A Regressão Logística foi selecionada pela ROC AUC média na validação cruzada.

| Acurácia | Precisão | Sensibilidade | F1 | ROC AUC |
|---:|---:|---:|---:|---:|
| 86,9% | 81,3% | 92,9% | 86,7% | 0,958 |

Esse módulo permanece como extensão e não substitui a atividade textual.

### Avaliação por faixa etária

| Faixa etária | n | Casos positivos | Acurácia | Sensibilidade | F1 | ROC AUC |
|---|---:|---:|---:|---:|---:|---:|
| Até 49 anos | 18 | 5 | 100,0% | 100,0% | 100,0% | 1,000 |
| 50 a 59 anos | 25 | 12 | 84,0% | 91,7% | 84,6% | 0,981 |
| 60 anos ou mais | 18 | 11 | 77,8% | 90,9% | 83,3% | 0,870 |

As faixas possuem somente 18 a 25 pacientes. O resultado perfeito no grupo mais jovem ocorreu em apenas 18 registros e não permite concluir desempenho perfeito, ausência de viés ou capacidade de generalização.

## Ir Além 1 — React + Vite

O código está em `portal-cardioia/` e inclui:

- autenticação simulada com Context API;
- JWT fictício no localStorage;
- rotas protegidas;
- pacientes carregados de JSON por camada de serviço;
- busca de pacientes;
- agendamento com `useState` e `useReducer`;
- dashboard;
- CSS Modules responsivo;
- testes funcionais e build de produção.

A transferência para o repositório separado exigido e a publicação dos integrantes/RMs permanecem pendentes de ação/autorização.

## Ir Além 2 — MLP de ECG

`fase2/notebooks/mlp_ecg_binaria.ipynb` e `fase2/src/treinar_mlp_ecg.py` implementam uma MLP Keras sobre imagens 64 × 64 em tons de cinza.

O experimento binário usa 30 imagens normais e 30 anormais selecionadas deterministicamente das três classes anormais.

| Métrica | Resultado |
|---|---:|
| Acurácia | 41,7% |
| Acurácia balanceada | 41,7% |
| Precisão — anormal | 33,3% |
| Recall — anormal | 16,7% |
| F1 — anormal | 22,2% |
| ROC AUC | 0,667 |

O baixo desempenho é mantido de forma transparente. Ele mostra que a pequena amostra e uma MLP simples sobre pixels achatados não sustentam generalização. Implementação funcional não equivale a modelo clinicamente útil.

### Revisão ampliada

Para responder à limitação da amostra, foi acrescentado um segundo experimento, sem apagar o baseline. A versão 2 da mesma fonte possui 928 arquivos distribuídos nas quatro pastas; depois da remoção de cópias exatas restam **491 imagens únicas**: 142 normais e 349 anormais. Os cabeçalhos e rodapés são retirados antes do versionamento e do treinamento.

O protocolo usa 313 imagens no treino, 79 na validação e 99 no teste final. A divisão é estratificada pela classe original, os hashes não se repetem entre conjuntos, pesos de classe são calculados somente no treino e o limiar é escolhido somente na validação.

| Métrica | Baseline (60) | Revisão ampliada (491) |
|---|---:|---:|
| Acurácia | 41,7% | 73,7% |
| Acurácia balanceada | 41,7% | 78,4% |
| Precisão — anormal | 33,3% | 94,0% |
| Recall — anormal | 16,7% | 67,1% |
| F1 — anormal | 22,2% | 78,3% |
| ROC AUC | 0,667 | 0,835 |

Com TensorFlow CPU 2.21.0, fixado nas dependências, duas execuções produziram o mesmo resultado e a matriz `[[26, 3], [23, 47]]` (normal/anormal). A melhora confirma a utilidade de ampliar a amostra, mas não demonstra validade clínica. A fonte ainda não oferece identificador confiável de paciente, portanto exames diferentes da mesma pessoa podem estar em conjuntos distintos.

## Estrutura da Fase 2

```text
fase2/
├── app.py
├── CHECKLIST_ENUNCIADO.md
├── dados/
│   ├── classificacao_risco.csv
│   ├── mapa_conhecimento.csv
│   ├── relatos_sintomas.txt
│   └── visual_ampliado/
├── notebooks/
│   ├── analise_baseline.ipynb
│   ├── classificacao_textual_tfidf.ipynb
│   ├── mlp_ecg_binaria.ipynb
│   └── mlp_ecg_ampliada.ipynb
├── src/
│   ├── analisar_modelo.py
│   ├── classificar_risco_texto.py
│   ├── extrair_sintomas.py
│   ├── treinar_baselines.py
│   ├── treinar_mlp_ecg.py
│   ├── preparar_visual_ampliado.py
│   └── treinar_mlp_ecg_ampliada.py
├── tests/
│   ├── auditar_cenarios.py
│   ├── test_app.py
│   ├── test_nlp.py
│   ├── test_visual.py
│   └── test_visual_ampliado.py
├── requirements.txt
└── requirements-visual.txt
```

## Execução principal

Pré-requisito: Python 3.12.

```bash
pip install -r fase2/requirements.txt
python fase2/src/extrair_sintomas.py
python fase2/src/classificar_risco_texto.py
jupyter nbconvert --to notebook --execute fase2/notebooks/classificacao_textual_tfidf.ipynb
streamlit run fase2/app.py
```

## Execução visual

As dependências do TensorFlow foram isoladas para não tornar o deploy do Streamlit pesado.

```bash
pip install -r fase2/requirements-visual.txt
python fase2/tests/test_visual.py
python fase2/src/treinar_mlp_ecg.py
python fase2/src/preparar_visual_ampliado.py --cache /tmp/cardioia-ecg-raw
python fase2/tests/test_visual_ampliado.py
python fase2/src/treinar_mlp_ecg_ampliada.py
```

## Validação automática

- `.github/workflows/fase2-baseline.yml`: NLP, portal React, Streamlit, modelo tabular e notebooks.
- `.github/workflows/fase2-visual.yml`: dados visuais, arquitetura, MLP, notebook e artifacts.

Consulte `fase2/CHECKLIST_ENUNCIADO.md` para a correspondência completa entre requisitos, arquivos e pendências. O relatório consolidado está em `fase2/RELATORIO_ENTREGA.md`.

## Limitações gerais

- bases pequenas, simuladas ou históricas;
- subgrupos demográficos pequenos, com intervalos de confiança amplos;
- ausência de validação externa, clínica e prospectiva;
- desempenho textual perfeito decorrente de base didática separável;
- baixo desempenho do baseline visual e desempenho ainda insuficiente da revisão ampliada;
- ausência de identificador de paciente na fonte visual;
- balanceamentos artificiais que não representam prevalência;
- dados textuais, tabulares e visuais de pessoas e fontes diferentes;
- saídas não apropriadas para uso assistencial.

## Privacidade

O front não usa API própria nem banco de dados e não armazena relatos. Use apenas exemplos fictícios e nunca forneça nome, CPF, prontuário ou outra informação identificável.

## Encerramento da entrega

Para a submissão acadêmica final ainda é necessário criar o repositório público separado do portal e inserir os links dos vídeos não listados. Essas pendências são externas; o código, os notebooks e os testes já estão implementados.
