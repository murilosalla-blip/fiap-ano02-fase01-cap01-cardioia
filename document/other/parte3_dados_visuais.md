# Parte 3 — Dados Visuais (documento de apoio)

> Este documento reúne o conteúdo necessário para compor a seção "Parte 3 — Dados Visuais" do README principal. Não é o README final — serve como fonte de texto pronta para consolidação posterior.

## Objetivo

O enunciado exige no mínimo 100 imagens (.jpg ou .png) de um único tipo de exame cardiológico (ECG, angiograma ou raio-X torácico), com justificativa de aplicação em Visão Computacional. A modalidade escolhida foi o **Eletrocardiograma (ECG)**, por ser um exame amplamente utilizado na triagem e diagnóstico de eventos cardiovasculares, ter fontes públicas documentadas disponíveis, e por seu forte potencial de reutilização na Fase 4 do CardioIA (Diagnóstico com Visão Computacional).

## Fonte

- **Dataset:** ECG Images dataset of Cardiac Patients — Version 2
- **Repositório:** Mendeley Data
- **Autores:** Ali Haider Khan, Muzammil Hussain
- **Instituição:** Ch. Pervaiz Elahi Institute of Cardiology, Multan, Paquistão
- **DOI:** 10.17632/gwbz3fsgp8.2
- **URL oficial:** https://data.mendeley.com/datasets/gwbz3fsgp8/2
- **Licença:** CC BY 4.0

Detalhes completos da auditoria da fonte estão em `document/other/fontes_parte3/fonte_dataset.md`.

## Dataset original

- 928 arquivos físicos `.jpg`, distribuídos em 4 classes (Myocardial Infarction, Abnormal Heartbeat, History of MI, Normal).
- Resolução original uniforme: 2213 × 1572 pixels, modo RGB.
- Tamanho total: aproximadamente 586,7 MB.
- Divergência identificada: a pasta "Myocardial Infarction Patients (240x12=2880)" contém fisicamente 239 arquivos, não 240, como sugerido pela nomenclatura original da pasta.

## Auditoria de duplicidade

A auditoria local (hash SHA-256 de todos os 928 arquivos) identificou duplicação binária exata em 3 das 4 classes:

| Classe | Arquivos físicos | Imagens únicas |
|---|---:|---:|
| Myocardial Infarction | 239 | 30 |
| Abnormal Heartbeat | 233 | 233 |
| History of MI | 172 | 86 |
| Normal | 284 | 142 |
| **Total** | **928** | **491** |

Duplicatas exatas foram excluídas da amostra final porque não agregam diversidade real ao corpus visual — usá-las infla artificialmente a contagem de imagens sem representar novos exames, e poderia introduzir risco de vazamento de dados (data leakage) em eventuais experimentos futuros de classificação (Fase 4), caso a mesma imagem aparecesse simultaneamente em conjuntos de treino e teste.

## Amostra final

- 30 imagens únicas por classe, 4 classes, **120 imagens no total** — acima do mínimo de 100 exigido pela FIAP.
- Nenhuma duplicata exata entre os arquivos finais (confirmado por hash SHA-256).
- Seleção determinística e reprodutível: `random_state = 42`, via script `scripts/preparar_amostra_ecg.py`.
- Manifesto de rastreabilidade completo em `document/other/fontes_parte3/manifesto_amostra.csv` (arquivo original, hash, arquivo final, classe, transformação aplicada).

## Preparação

- **Seleção reproduzível:** cada imagem única foi identificada por hash SHA-256; a seleção das 30 por classe usa semente fixa (42), permitindo reconstrução idêntica da amostra a qualquer momento a partir do dataset bruto original.
- **Remoção do cabeçalho administrativo:** as imagens originais continham um cabeçalho de formulário clínico (título "ECG REPORT", ID numérico do paciente, dados demográficos, data/hora do exame, campos "Diagnosis Information"/"Technician"/"Ref-Phys."). Essa região foi removida por crop (recorte das primeiras ~283 linhas de pixel, validado visualmente como uniforme em amostras aleatórias das 4 classes antes da aplicação em massa), preservando integralmente a área de traçado (as 12 derivações e a tira de ritmo).
- **Remoção de metadados EXIF:** as imagens finais não carregam metadados EXIF (confirmado por inspeção), pois o processo de abertura/recorte/gravação da imagem naturalmente descarta esses dados.
- **Ausência de redimensionamento ou alteração clínica:** não houve redimensionamento, conversão para escala de cinza, filtros, correção de contraste, threshold ou qualquer alteração do traçado. A única transformação aplicada foi o crop administrativo.
- **Nomes neutros:** os arquivos finais usam nomenclatura sequencial neutra por classe (`mi_001.jpg`, `ahb_001.jpg`, `hmi_001.jpg`, `normal_001.jpg`), sem carregar qualquer identificador de paciente do dataset original.

## Estrutura final no projeto

```
assets/imagens/ecg/
├── myocardial_infarction/   (30 imagens: mi_001.jpg – mi_030.jpg)
├── abnormal_heartbeat/      (30 imagens: ahb_001.jpg – ahb_030.jpg)
├── history_mi/              (30 imagens: hmi_001.jpg – hmi_030.jpg)
└── normal/                  (30 imagens: normal_001.jpg – normal_030.jpg)
```

## Aplicação em Visão Computacional

Este corpus de imagens de ECG pode ser reaproveitado, em fases futuras do CardioIA, para tarefas como:

- classificação visual de padrões de ECG (ex.: distinguir traçados normais de alterados);
- detecção de padrões associados a infarto do miocárdio (elevação/depressão de segmento ST, ondas Q patológicas);
- identificação de padrões de batimento anormal (arritmias);
- treinamento de Redes Neurais Convolucionais (CNNs) para classificação de imagens médicas;
- extração de características visuais (bordas, texturas do traçado) como etapa de pré-processamento para modelos de diagnóstico assistido.

Nenhum modelo foi implementado ou treinado nesta fase — a Parte 3 se limita à coleta, curadoria e preparação do dado visual.

## Governança e limitações

- **Origem geográfica concentrada:** todos os exames têm origem em instituições de saúde do Paquistão, o que limita a representatividade para outras populações sem validação adicional.
- **Possível viés de equipamento:** os exames foram coletados com um único modelo de dispositivo ECG, podendo introduzir características específicas do aparelho que não generalizam para outros equipamentos.
- **Duplicação no dataset original:** identificada e tratada — 437 dos 928 arquivos originais eram cópias exatas, excluídas da amostra final por hash.
- **Cabeçalho administrativo:** as imagens originais expunham um ID numérico de paciente e data/hora do exame no cabeçalho; essa região foi removida da amostra incorporada ao projeto, tanto por não ser necessária à finalidade de Visão Computacional quanto por reduzir risco de exposição de identificador, e também porque um modelo de classificação não deve aprender padrões administrativos em vez do sinal de ECG.
- **Classe Myocardial Infarction menor após deduplicação:** apenas 30 imagens únicas estavam disponíveis nessa classe (das 239 originais), o que limita a robustez estatística dessa categoria especificamente em eventuais experimentos futuros de classificação.
- **Cada arquivo físico representa uma imagem de um exame de ECG de 12 derivações** — não foi validado de forma independente se cada arquivo corresponde a um paciente distinto (o dataset original não fornece identificador de paciente reutilizável nesse sentido além do ID de cabeçalho removido nesta preparação).
- **Finalidade acadêmica:** este material tem finalidade exclusivamente acadêmica e exploratória no contexto da atividade FIAP. Não constitui, nem deve ser interpretado como, ferramenta de diagnóstico médico.

## Link público externo

**PENDENTE** — publicação externa/link público a ser realizada no fechamento do projeto, no mesmo padrão já adotado para a Parte 1.
