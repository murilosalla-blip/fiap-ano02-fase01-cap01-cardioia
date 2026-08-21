# Dicionário de Variáveis — Heart Disease Cleveland (processado)

Arquivo de referência: `assets/dados/processed/heart_disease_cleveland.csv`
Fonte da definição original das variáveis: documentação oficial UCI Machine Learning Repository — Heart Disease Data Set, arquivo `heart-disease.names` (preservado em `assets/dados/raw/heart+disease/heart-disease.names`).

| # | Coluna (CSV) | Nome original (UCI) | Significado | Tipo | Valores possíveis | Interpretação clínica básica |
|---|---|---|---|---|---|---|
| 1 | `idade` | age | Idade do paciente em anos | Numérica (inteiro) | Valores observados: 29 a 77 | Fator de risco cardiovascular consolidado; o risco de doença coronariana aumenta com a idade. |
| 2 | `sexo` | sex | Sexo biológico do paciente | Categórica binária | `masculino` (1), `feminino` (0) | A prevalência e apresentação clínica de doença coronariana variam entre sexos. |
| 3 | `tipo_dor_peito` | cp (chest pain type) | Tipo de dor torácica relatada | Categórica (4 classes) | `angina_tipica`, `angina_atipica`, `dor_nao_anginosa`, `assintomatico` | A angina típica está mais associada à isquemia coronariana; casos assintomáticos são clinicamente relevantes por dificultarem o diagnóstico precoce. |
| 4 | `pressao_arterial_repouso` | trestbps (resting blood pressure) | Pressão arterial em repouso, em mm Hg, na admissão hospitalar | Numérica (contínua) | Valores observados: 94 a 200 mm Hg | Hipertensão é um dos principais fatores de risco para doença cardiovascular. |
| 5 | `colesterol` | chol (serum cholestoral) | Colesterol sérico em mg/dl | Numérica (contínua) | Valores observados: 126 a 564 mg/dl | Colesterol elevado está associado a maior risco de aterosclerose e eventos coronarianos. |
| 6 | `acucar_jejum_maior_120` | fbs (fasting blood sugar > 120 mg/dl) | Indica se a glicemia de jejum é maior que 120 mg/dl | Categórica binária | `sim` (1), `nao` (0) | Proxy para diabetes/pré-diabetes, condição associada a maior risco cardiovascular. |
| 7 | `eletrocardiograma_repouso` | restecg (resting electrocardiographic results) | Resultado do eletrocardiograma em repouso | Categórica (3 classes) | `normal`, `anormalidade_onda_st_t`, `hipertrofia_ventricular_esquerda` | Alterações no ECG de repouso podem indicar isquemia prévia ou sobrecarga cardíaca estrutural. |
| 8 | `frequencia_cardiaca_maxima` | thalach (maximum heart rate achieved) | Frequência cardíaca máxima atingida em teste de esforço | Numérica (contínua) | Valores observados: 71 a 202 bpm | Capacidade cronotrópica reduzida (frequência máxima baixa) pode estar associada a pior condicionamento cardiovascular ou disfunção. |
| 9 | `angina_induzida_exercicio` | exang (exercise induced angina) | Presença de angina induzida por exercício físico | Categórica binária | `sim` (1), `nao` (0) | Angina desencadeada por esforço é um sinal clínico direto de isquemia miocárdica. |
| 10 | `depressao_st_exercicio` | oldpeak (ST depression induced by exercise relative to rest) | Depressão do segmento ST induzida pelo exercício, em relação ao repouso | Numérica (contínua) | Valores observados: 0.0 a 6.2 | Quanto maior a depressão do segmento ST, maior a probabilidade de isquemia miocárdica significativa. |
| 11 | `inclinacao_st_pico_exercicio` | slope (the slope of the peak exercise ST segment) | Inclinação do segmento ST no pico do exercício | Categórica (3 classes) | `ascendente`, `plana`, `descendente` | Inclinação descendente ou plana está associada a maior risco de doença coronariana em relação à ascendente. |
| 12 | `num_vasos_principais` | ca (number of major vessels colored by flourosopy) | Número de vasos principais (0–3) visualizados por fluoroscopia | Numérica (discreta) | `0`, `1`, `2`, `3`; `ausente` quando não informado na fonte original | Quanto maior o número de vasos comprometidos visíveis, maior a extensão da doença coronariana. Valores ausentes correspondem a registros não informados na base original da UCI (marcados como `?`). |
| 13 | `talassemia` | thal | Resultado do teste de talassemia (defeito de perfusão miocárdica) | Categórica (3 classes) | `normal`, `defeito_fixo`, `defeito_reversivel`; `ausente` quando não informado na fonte original | Defeitos fixos ou reversíveis indicam áreas de perfusão miocárdica comprometida, associadas a maior risco cardiovascular. Valores ausentes correspondem a registros não informados na base original da UCI (marcados como `?`). |
| 14 | `diagnostico_doenca_cardiaca` | num (diagnosis of heart disease) | Diagnóstico de doença cardíaca (variável-alvo) | Categórica binária (derivada) | `presente` (valor original 1–4, indicando >50% de estreitamento em algum vaso principal), `ausente` (valor original 0, indicando <50% de estreitamento) | Variável-alvo tipicamente usada como rótulo em tarefas de classificação supervisionada para prever presença de doença coronariana. |

## Observações sobre valores ausentes

- A base original UCI documenta explicitamente a existência de valores ausentes ("Missing Attribute Values: Several"), marcados como `?` no arquivo `processed.cleveland.data`.
- Neste dataset processado, esses valores foram mantidos como a string `"ausente"` nas colunas `num_vasos_principais` e `talassemia` (4 e 2 registros, respectivamente) — nenhum valor foi inventado, estimado ou removido.
- Nenhuma outra coluna apresenta valores ausentes.

## Observação sobre a variável-alvo

- No dataset original da UCI, `num` é um valor inteiro de 0 a 4, representando o grau de estreitamento arterial diagnosticado por angiografia.
- Seguindo a prática documentada pelos próprios autores/pesquisadores do dataset ("Experiments with the Cleveland database have concentrated on simply attempting to distinguish presence (values 1,2,3,4) from absence (value 0)"), a coluna `diagnostico_doenca_cardiaca` foi simplificada para binária (`presente`/`ausente`) nesta versão processada.
