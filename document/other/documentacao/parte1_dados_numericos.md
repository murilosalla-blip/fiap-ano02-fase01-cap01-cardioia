# Parte 1 — Dados Numéricos (documento de apoio)

> Este documento reúne todo o conteúdo necessário para compor a seção "Parte 1 — Dados Numéricos" do README principal. Não é o README final — serve como fonte de texto pronta para consolidação posterior.

## Fonte oficial do dataset

- **Nome:** Heart Disease Data Set (base Cleveland).
- **Repositório:** UCI Machine Learning Repository.
- **Autores/instituição responsável pela coleta:** Robert Detrano, M.D., Ph.D. — V.A. Medical Center, Long Beach e Cleveland Clinic Foundation.
- **Licença:** Creative Commons Attribution 4.0 International (CC BY 4.0) — permite compartilhamento e adaptação para qualquer finalidade, mediante crédito aos autores originais.
- **Citação recomendada:** Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1988). Heart Disease. UCI Machine Learning Repository. DOI: 10.24432/C52P4X.
- **Data de download:** 21/08/2026, diretamente do pacote oficial disponibilizado pela UCI.

## Descrição da base

O dataset original contém 76 atributos coletados de pacientes submetidos a avaliação cardiológica, dos quais 14 são reconhecidos pela literatura e pelos próprios autores como o subconjunto relevante para experimentos de diagnóstico de doença coronariana. Este projeto utiliza exclusivamente a base **Cleveland**, por ser a mais completa e a mais utilizada em pesquisas de aprendizado de máquina dentre as quatro bases originais (Cleveland, Hungria, Suíça, Long Beach VA).

## Quantidade de registros e variáveis

- **Registros:** 303 pacientes (linhas de dados), acima do mínimo de 100 exigido pelo enunciado.
- **Variáveis:** 14 colunas — 13 variáveis preditoras (demográficas, clínicas e de exame) e 1 variável-alvo (diagnóstico de doença cardíaca).
- **Duplicidades:** nenhuma linha duplicada.
- **Valores ausentes:** 4 registros com `num_vasos_principais` ausente e 2 registros com `resultado_thal` ausente (herdados da fonte oficial, preservados sem imputação).

## Formato utilizado

Arquivo `.csv`, conforme exigência explícita do enunciado (requisito identificado em uma imagem de "Atenção" embutida no documento da atividade, adicional ao texto corrido).

## Processo de preparação

1. Download do pacote oficial de dados da UCI (arquivo `heart+disease.zip`).
2. Preservação de todos os arquivos originais, sem qualquer modificação, em `assets/dados/raw/heart+disease/`.
3. Seleção do arquivo `processed.cleveland.data` (14 atributos já filtrados pelos próprios autores da base).
4. Conversão programática via script `scripts/preparar_dataset_numerico.py`, que:
   - adiciona cabeçalho com nomes de colunas em português;
   - traduz códigos numéricos categóricos para rótulos legíveis (ex.: `1.0` → `masculino`);
   - preserva valores ausentes originais como `"ausente"`, sem inventar ou remover dados;
   - simplifica a variável-alvo original (`num`, escala 0–4) para binária (`ausente`/`presente`), seguindo a prática documentada pelos próprios autores da base.
5. Resultado salvo em `assets/dados/processed/heart_disease_cleveland.csv`.

Toda transformação aplicada é reprodutível: basta executar `python scripts/preparar_dataset_numerico.py` a partir da raiz do repositório, tendo o arquivo original em `assets/dados/raw/` como entrada.

## Justificativa das principais variáveis clínicas

As variáveis a seguir são consideradas as mais relevantes para um projeto de Inteligência Artificial aplicado à saúde cardiovascular:

- **`idade`** — representa a idade do paciente em anos. É clinicamente relevante porque a idade é um fator de risco cardiovascular amplamente reconhecido, e sua inclusão permite que modelos de aprendizado de máquina capturem o efeito do envelhecimento sobre a probabilidade de doença coronariana.

- **`pressao_arterial_repouso`** — pressão arterial do paciente em repouso (mm Hg). É relevante porque a hipertensão arterial é um dos principais fatores de risco modificáveis para eventos cardiovasculares, e seu registro contínuo permite que algoritmos identifiquem padrões de associação entre níveis pressóricos e desfecho.

- **`colesterol`** — nível de colesterol sérico (mg/dl). Relevante por sua associação direta com processos de aterosclerose; é uma variável numérica contínua útil para modelos preditivos de risco cardiovascular.

- **`tipo_dor_peito`** — classifica o tipo de dor torácica relatada pelo paciente. É clinicamente relevante porque o padrão de dor (típica, atípica, não anginosa ou assintomática) é um dos critérios clínicos tradicionais usados na triagem de suspeita de doença coronariana, tornando essa variável categórica potencialmente informativa para classificadores.

- **`frequencia_cardiaca_maxima`** — frequência cardíaca máxima atingida em teste de esforço. Relevante porque a resposta cronotrópica ao esforço físico é um indicador funcional cardiovascular amplamente utilizado na avaliação de risco.

- **`angina_induzida_exercicio`** e **`depressao_st_exercicio`** — indicam, respectivamente, a presença de angina desencadeada por esforço e a magnitude da depressão do segmento ST durante exercício. Ambas são variáveis diretamente associadas a evidências eletrocardiográficas de isquemia miocárdica, sendo historicamente usadas em critérios diagnósticos de doença coronariana.

- **`diagnostico_doenca_cardiaca`** — variável-alvo (rótulo). É a variável que um modelo de Machine Learning supervisionado buscaria prever a partir das demais, tornando-a o elemento central para qualquer aplicação de classificação nesta base.

Essas variáveis, em conjunto, permitem tanto análises exploratórias (ex.: correlação entre pressão arterial e diagnóstico) quanto o treinamento de modelos preditivos (ex.: classificadores para estimar a probabilidade de doença coronariana a partir de dados clínicos não invasivos).

**Observação:** esta documentação tem finalidade exclusivamente acadêmica e exploratória. Não constitui, nem deve ser interpretada como, ferramenta de diagnóstico médico. As interpretações clínicas descritas refletem associações amplamente documentadas na literatura cardiológica, não conclusões extraídas por análise estatística própria deste projeto.

## Governança, privacidade e viés

- **Origem pública e licenciada:** o dataset é público, distribuído pelo UCI Machine Learning Repository sob licença CC BY 4.0, que permite uso e adaptação mediante atribuição de crédito.
- **Anonimização:** conforme a documentação oficial da UCI, nomes e números de identificação dos pacientes já foram removidos e substituídos por valores fictícios antes da publicação da base; não há identificação direta de indivíduos nos dados utilizados.
- **Limitações de representatividade:** a base é composta por 303 pacientes atendidos na Cleveland Clinic Foundation (Estados Unidos) na década de 1980. Isso implica possíveis vieses:
  - **Viés geográfico:** os dados refletem uma única população hospitalar dos EUA, não representando necessariamente outras regiões ou sistemas de saúde (ex.: Brasil).
  - **Viés temporal/histórico:** a coleta ocorreu há mais de 30 anos; práticas diagnósticas, exames disponíveis e perfil epidemiológico da população podem ter mudado desde então.
  - **Viés demográfico:** não há garantia de distribuição equilibrada entre sexos, faixas etárias ou grupos étnicos; qualquer modelo treinado nesta base deve ser avaliado quanto a desempenho desigual entre subgrupos antes de qualquer uso além do escopo acadêmico.
- **Cuidados necessários ao utilizar este dataset em IA aplicada à saúde:**
  - Resultados obtidos a partir desta base não devem ser generalizados para populações ou contextos clínicos diferentes do estudado sem validação adicional.
  - Modelos preditivos treinados aqui têm finalidade exclusivamente educacional/exploratória neste projeto, não devendo ser utilizados para decisões clínicas reais.
  - A simplificação da variável-alvo (de escala 0–4 para binária) deve ser levada em conta em qualquer análise de desempenho de modelos, pois reduz a granularidade da informação original.

## Referência ao arquivo processado

- Dataset processado: `assets/dados/processed/heart_disease_cleveland.csv`
- Dicionário de variáveis: `assets/dados/processed/dicionario_variaveis.md`
- Dados originais (não modificados): `assets/dados/raw/heart+disease/`
- Script de geração: `scripts/preparar_dataset_numerico.py`

## Link público para hospedagem externa (OneDrive)

> **PENDENTE — preencher manualmente após publicar o dataset em um serviço de armazenamento público (OneDrive, Google Drive ou equivalente).**
>
> Link: `[A PREENCHER]`
>
> Ao publicar, confirmar que o link está configurado como "qualquer pessoa com o link pode visualizar", para garantir acesso pela equipe de correção da FIAP.
