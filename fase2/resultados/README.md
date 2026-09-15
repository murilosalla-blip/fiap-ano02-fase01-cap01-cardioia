# Resultados da Fase 2

Este diretório recebe as saídas reproduzíveis dos três experimentos independentes. Os arquivos gerados são publicados como artifacts dos workflows do GitHub Actions.

## Classificador textual obrigatório

Base: 120 frases simuladas, balanceadas entre alto e baixo risco e pareadas por sexo.

Separação: 96 frases de treino e 24 de teste, agrupadas por `id_cenario`. Nenhum cenário aparece nos dois conjuntos.

| Métrica | Resultado |
|---|---:|
| Acurácia | 1,000 |
| Precisão — alto risco | 1,000 |
| Recall — alto risco | 1,000 |
| F1 — alto risco | 1,000 |
| ROC AUC | 1,000 |

### Análise contrafactual por sexo

| Medida | Resultado |
|---|---:|
| Probabilidade média — feminino | 0,5062 |
| Probabilidade média — masculino | 0,5088 |
| Diferença absoluta média | 0,0025 |
| Maior diferença absoluta | 0,0033 |

O resultado perfeito decorre de uma base pequena, simulada e deliberadamente separável. Ele não estima desempenho em relatos reais.

Uma sondagem adicional com 16 entradas verificou negação, caixa, pontuação, paráfrase e texto fora do vocabulário. Quatro entradas não ativaram nenhum termo do TF-IDF e a diferença entre “tenho dor no peito” e sua negação foi de apenas 0,0121. Isso não é uma métrica externa: evidencia que o classificador simples não compreende contexto linguístico complexo e justifica os alertas exibidos no front.

Saídas geradas em `fase2/resultados/nlp/`:

- `metricas_classificador_texto.json`;
- `previsoes_teste_texto.csv`;
- `vies_contrafactual_sexo.csv`;
- `termos_influentes.csv`;
- `matriz_confusao_texto.png`;
- `classificador_risco_texto.joblib`;
- `classificacao_textual_tfidf_executada.ipynb`.

## Modelo tabular complementar

A comparação entre Regressão Logística e Random Forest usa a modalidade tabular Cleveland.

### Validação cruzada no treino

| Modelo | Acurácia | Precisão | Recall | F1 | ROC AUC |
|---|---:|---:|---:|---:|---:|
| Regressão Logística | 0,847 ± 0,025 | 0,848 ± 0,062 | 0,819 ± 0,057 | 0,831 ± 0,025 | 0,907 ± 0,020 |
| Random Forest | 0,801 ± 0,029 | 0,786 ± 0,064 | 0,792 ± 0,090 | 0,784 ± 0,036 | 0,900 ± 0,034 |

### Teste com 61 pacientes

| Métrica | Resultado |
|---|---:|
| Acurácia | 0,869 |
| Precisão | 0,813 |
| Recall | 0,929 |
| F1 | 0,867 |
| ROC AUC | 0,958 |

### Avaliação descritiva por sexo

| Sexo | n | Positivos | Acurácia | Precisão | Recall | F1 | ROC AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| Feminino | 20 | 7 | 0,950 | 1,000 | 0,857 | 0,923 | 1,000 |
| Masculino | 41 | 21 | 0,829 | 0,769 | 0,952 | 0,851 | 0,938 |

Os subgrupos são pequenos. As diferenças são descritivas e não permitem conclusões clínicas ou de equidade.

## MLP visual — Ir Além 2

A MLP utiliza 60 imagens: 30 normais e 30 anormais. Os 30 exemplos anormais são selecionados deterministicamente, dez de cada classe original anormal.

| Métrica | Resultado |
|---|---:|
| Acurácia | 0,417 |
| Acurácia balanceada | 0,417 |
| Precisão — anormal | 0,333 |
| Recall — anormal | 0,167 |
| F1 — anormal | 0,222 |
| ROC AUC | 0,667 |

A implementação, o treinamento e a avaliação funcionaram, mas o resultado é fraco. A pequena amostra e a MLP sobre pixels achatados não sustentam uso prático.

Saídas publicadas no artifact `resultados-mlp-ecg`:

- modelo Keras;
- métricas em JSON;
- inventário binário;
- previsões do teste;
- curva de perda;
- matriz de confusão;
- notebook executado.

### Revisão ampliada

A revisão preserva o baseline e usa todas as 491 imagens únicas recuperadas da versão 2 da mesma fonte. Cabeçalho e rodapé são removidos, e a divisão estratificada pela classe original produz 313 exemplos de treino, 79 de validação e 99 de teste final.

| Métrica | Resultado |
|---|---:|
| Acurácia | 0,697 |
| Acurácia balanceada | 0,745 |
| Precisão — anormal | 0,917 |
| Recall — anormal | 0,629 |
| F1 — anormal | 0,746 |
| ROC AUC | 0,824 |

O limiar 0,77 foi escolhido somente na validação. A matriz de confusão do teste foi `[[25, 4], [26, 44]]`. Duas execuções com semente 42 produziram o mesmo arquivo de métricas. A melhora em relação ao baseline reduz a incerteza amostral, mas não supre a falta de identificação por paciente ou validação clínica externa.

Saídas em `fase2/resultados/visual_ampliado/`:

- modelo Keras;
- métricas e histórico de treino;
- previsões do teste;
- matriz de confusão.

## Governança e interpretação

- As modalidades textual, tabular e visual têm origens diferentes e não são fundidas.
- A amostra visual foi deduplicada por SHA-256.
- A fonte visual não possui identificador de paciente; a separação por indivíduo não pode ser garantida.
- Nenhum balanceamento representa prevalência real.
- Nenhum resultado constitui diagnóstico, risco clínico ou recomendação de atendimento.
