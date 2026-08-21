
<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=30% height=30%>

# AI Project Document - Módulo 1 - FIAP

**_Os trechos em itálico servem apenas como guia para o preenchimento da seção. Por esse motivo, não devem fazer parte da documentação final_**

## Nome do Grupo

Grupo Aura

#### Nomes dos integrantes do grupo

- Murilo Salla — RM568041
- Elias da Silva de Souza — RM568500
- Julia Duarte de Carvalho — RM567816



## Sumário

[1. Introdução](#c1)

[2. Visão Geral do Projeto](#c2)

[3. Desenvolvimento do Projeto](#c3)

[4. Resultados e Avaliações](#c4)

[5. Conclusões e Trabalhos Futuros](#c5)

[6. Referências](#c6)

[Anexos](#c7)

<br>

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto da Inteligência Artificial

A Inteligência Artificial aplicada à saúde é um segmento em expansão global, com destaque para o apoio ao diagnóstico, triagem e monitoramento de doenças crônicas. As doenças cardiovasculares são a principal causa de mortalidade no mundo, o que torna a cardiologia um dos campos de maior potencial de impacto para soluções de IA — desde classificadores que auxiliam a identificar risco cardíaco até sistemas de visão computacional para leitura de exames e assistentes virtuais de orientação ao paciente. O projeto **CardioIA** se insere nesse contexto como uma plataforma acadêmica que simula, ao longo de 7 fases, um ecossistema de cardiologia inteligente, abordando módulos de dados, Machine Learning, IoT, Visão Computacional e NLP.

### 1.1.2. Descrição da Solução Desenvolvida

Nesta Fase 1, o papel da equipe é o de cientista de dados hospitalar, responsável por buscar, preparar, validar e documentar três tipos de dados fundamentais para o CardioIA: **dados numéricos** (variáveis clínicas de pacientes cardíacos), **dados textuais** (materiais sobre saúde cardiovascular para NLP) e **dados visuais** (imagens de exame cardiológico para Visão Computacional). Nenhum modelo de IA foi treinado nesta etapa — o objetivo é consolidar uma base de dados curada, com governança e rastreabilidade, que sustentará o desenvolvimento de soluções de IA nas fases seguintes do curso.

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

Buscar, organizar e documentar três tipos de dados fundamentais para pacientes cardíacos — numéricos, textuais e visuais — com foco em governança de dados e atenção a vieses desde o início, formando uma base sólida e rastreável para as fases seguintes do CardioIA (diagnóstico automatizado, IoT, visão computacional e assistente virtual).

## 2.2. Público-Alvo

Nesta fase, o público-alvo é acadêmico: a própria equipe do curso de IA da FIAP e o corpo docente responsável pela avaliação da atividade. Em uma perspectiva de continuidade do CardioIA (fases futuras), o público-alvo final da plataforma seria composto por profissionais de saúde (equipes de atenção primária e cardiologia) e pacientes em acompanhamento cardiovascular, mas nenhuma validação com esses usuários finais foi realizada nesta etapa.

## 2.3. Metodologia

A metodologia seguida nesta fase consistiu em: (1) leitura integral e auditoria multimodal do enunciado da atividade (texto, imagens, tabelas e mapa mental), para mapear todos os requisitos; (2) seleção de fontes públicas, institucionais, documentadas e rastreáveis para cada uma das três partes (numérica, textual e visual); (3) coleta e preservação dos dados brutos originais, sem alteração; (4) preparação e curadoria de cada conjunto (tradução de códigos, remoção de duplicidades, remoção de dados administrativos/pessoais, conforme o caso); (5) validação técnica de cada dataset (integridade, contagem, formato); (6) documentação individual de cada parte, incluindo justificativa clínica/técnica e considerações de governança e viés; (7) versionamento incremental de todo o processo em repositório Git público.

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

Python 3.12 como linguagem principal de preparação de dados; bibliotecas `csv` e `pathlib` (nativas) para o processamento do dataset numérico (Parte 1); `pypdf` para extração de texto de documentos oficiais em PDF (Parte 2); `Pillow` (PIL) e `hashlib` para inspeção, deduplicação e preparação das imagens de ECG (Parte 3); Git e GitHub para versionamento e hospedagem do repositório.

## 3.2. Modelagem e Algoritmos

Nesta fase não houve treinamento de modelos de IA. O escopo do trabalho foi exclusivamente a preparação, curadoria e documentação dos dados. As modalidades de IA que poderão ser exploradas em fases futuras, a partir dos dados aqui preparados, incluem: classificadores supervisionados de Machine Learning para diagnóstico de doença cardíaca (Fase 2, a partir do dataset numérico), técnicas de NLP como classificação de tópicos e extração de entidades médicas (Fase 5, a partir do corpus textual) e Redes Neurais Convolucionais (CNNs) para classificação de imagens de ECG (Fase 4, a partir do dataset visual).

## 3.3. Treinamento e Teste

Treinamento e teste de modelos de IA não fazem parte do escopo desta entrega (Fase 1). Os três conjuntos de dados preparados — numérico, textual e visual — foram validados tecnicamente (integridade, formato, ausência de duplicidades) e documentados, ficando prontos para serem utilizados como conjuntos de treinamento e teste nas fases posteriores do CardioIA.

# <a name="c4"></a>4. Resultados e Avaliações

## 4.1. Análise dos Resultados

**Parte 1 (dados numéricos):** dataset UCI Heart Disease (Cleveland) processado com sucesso — 303 registros, 14 variáveis clínicas, sem duplicidades, valores ausentes documentados e preservados (sem imputação) em 2 colunas. Dicionário de variáveis e justificativa clínica produzidos.

**Parte 2 (dados textuais):** corpus de 2 arquivos `.txt` preparados a partir de publicações oficiais do Ministério da Saúde/CONITEC, cobrindo prevenção cardiovascular e síndromes coronarianas agudas, formando um par temático complementar (antes/depois do evento cardíaco).

**Parte 3 (dados visuais):** dataset de imagens de ECG auditado localmente, revelando uma taxa de duplicação de aproximadamente 47% nos arquivos originais; a amostra final foi curada para 120 imagens únicas, balanceadas em 4 classes, com remoção de dados administrativos/pessoais do cabeçalho de cada imagem.

Em todas as três partes, o processo de auditoria e curadoria revelou divergências entre a documentação original das fontes e o conteúdo real dos arquivos (ex.: contagem de imagens, interpretação de notação de derivações do ECG, nomenclatura de variáveis clínicas), que foram investigadas e resolvidas com evidência direta dos dados antes da incorporação ao projeto.

## 4.2. Feedback dos Usuários

Não houve coleta de feedback de usuários finais nesta etapa, pois não faz parte do escopo da Fase 1 — o trabalho desenvolvido foi de preparação e curadoria de dados, sem interação com pacientes ou profissionais de saúde.

# <a name="c5"></a>5. Conclusões e Trabalhos Futuros

Os objetivos definidos para a Fase 1 do CardioIA foram atendidos: os três tipos de dados exigidos (numéricos, textuais e visuais) foram buscados, preparados, validados e documentados, com atenção à governança e a possíveis vieses desde a escolha das fontes. Como ponto forte, destaca-se o processo de auditoria rigorosa aplicado a cada fonte, que identificou e tratou problemas reais (duplicidades no dataset de ECG, interpretação incorreta de uma variável clínica no dataset numérico, ausência de licença explícita em documentos textuais) antes da incorporação ao projeto. Como limitação, destaca-se que a hospedagem externa com link público dos três conjuntos de dados ainda está pendente, a ser concluída no fechamento da entrega. Como trabalho futuro, conforme o mapa mental oficial do CardioIA, os dados aqui preparados serão a base para: modelos de Machine Learning para diagnóstico automatizado (Fase 2), simulação de monitoramento contínuo via IoT (Fase 3), Visão Computacional para diagnóstico por imagem (Fase 4), um assistente cardiológico virtual com NLP (Fase 5), previsão de crises com séries temporais (Fase 6) e, por fim, a consolidação de todos os módulos em uma plataforma única (Fase 7).

# <a name="c6"></a>6. Referências

- UCI Machine Learning Repository — Heart Disease Data Set (Cleveland). Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1988). DOI: 10.24432/C52P4X.
- Ministério da Saúde. Cadernos de Atenção Básica n.º 14 — Prevenção Clínica de Doença Cardiovascular, Cerebrovascular e Renal Crônica. Brasília, 2006.
- Ministério da Saúde / CONITEC. Protocolo Clínico — Síndromes Coronarianas Agudas.
- Khan, A. H., & Hussain, M. ECG Images dataset of Cardiac Patients — Version 2. Mendeley Data, DOI: 10.17632/gwbz3fsgp8.2.
- FIAP. Enunciado da atividade "Fase 1_Cap 1_Exercício" e mapa mental oficial do projeto CardioIA.

# <a name="c7"></a>Anexos

- Documento de apoio da Parte 1 (dados numéricos): `document/other/parte1_dados_numericos.md`
- Documento de apoio da Parte 2 (dados textuais): `document/other/parte2_dados_textuais.md`
- Documento de apoio da Parte 3 (dados visuais): `document/other/parte3_dados_visuais.md`
- Plano de execução da atividade: `document/other/plano_execucao.md`
- Dicionário de variáveis do dataset numérico: `assets/dados/processed/dicionario_variaveis.md`
- Manifesto de rastreabilidade da amostra de imagens de ECG: `document/other/fontes_parte3/manifesto_amostra.csv`
