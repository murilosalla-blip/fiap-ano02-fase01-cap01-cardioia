# Fonte da Parte 3 — Dados Visuais (ECG)

## Identificação

- **Título:** ECG Images dataset of Cardiac Patients
- **Autores:** Ali Haider Khan, Muzammil Hussain
- **Instituição:** Ch. Pervaiz Elahi Institute of Cardiology, Multan, Paquistão / University of Management and Technology
- **Versão:** 2 (2021)
- **DOI:** 10.17632/gwbz3fsgp8.2
- **URL oficial:** https://data.mendeley.com/datasets/gwbz3fsgp8/2
- **Licença:** CC BY 4.0
- **Data de download:** 21/08/2026

## Classes originais do dataset

| Pasta original | Rótulo do dataset | Contagem física real | Imagens únicas (hash SHA-256) |
|---|---|---:|---:|
| ECG Images of Myocardial Infarction Patients (240x12=2880) | Myocardial Infarction (MI) | 239 | 30 |
| ECG Images of Patient that have abnormal heartbeat (233x12=2796) | Abnormal Heartbeat (AHB) | 233 | 233 |
| ECG Images of Patient that have History of MI (172x12=2064) | History of MI (H.MI) | 172 | 86 |
| Normal Person ECG Images (284x12=3408) | Normal (NHB) | 284 | 142 |
| **TOTAL** | | **928** | **491** |

## Problema de duplicidade identificado

Auditoria local (hash SHA-256 de todos os 928 arquivos) revelou que 437 dos 928 arquivos (≈47%) são cópias binárias exatas de outro arquivo já presente na mesma classe, sob outro nome/índice, seguindo um padrão cíclico de repetição (ex.: em Myocardial Infarction, o arquivo de índice N é idêntico ao de índice N+30). Apenas a classe Abnormal Heartbeat não apresentou nenhuma duplicidade (233 arquivos, 233 únicos). Por esse motivo, a seleção da amostra para o projeto foi baseada exclusivamente em imagens únicas (deduplicadas por hash), não na contagem bruta de arquivos ou na nomenclatura original das pastas.

## Divergência de nomenclatura

A pasta "Myocardial Infarction Patients (240x12=2880)" contém fisicamente 239 arquivos, não 240 — a nomenclatura original da pasta é um rótulo de referência do dataset publicado, que não corresponde exatamente à contagem física de arquivos encontrada na auditoria local.

## Interpretação de `NxM` (ex.: `240x12=2880`)

Confirmado por inspeção visual direta: cada arquivo `.jpg` é uma única imagem contendo as 12 derivações padrão de ECG (I, II, III, aVR, aVL, aVF, V1–V6, mais uma tira de ritmo contínua) já compostas em um único layout de "ECG REPORT". A notação `NxM` do nome da pasta refere-se à relação entre número de exames e derivações (ex.: 240 exames × 12 derivações = 2880 traçados individuais), não a 12 arquivos separados por paciente. **1 arquivo físico = 1 imagem de um exame de ECG de 12 derivações.**

## Estratégia de amostragem adotada

Amostra final: 30 imagens únicas por classe (120 imagens no total), selecionadas por hash SHA-256 (apenas um exemplar por hash) e, quando a classe tinha mais de 30 únicas disponíveis, por amostragem aleatória determinística (`random_state = 42`, Python `random.Random(42).sample()`), garantindo reprodutibilidade. A classe Myocardial Infarction utiliza a totalidade de suas 30 imagens únicas disponíveis (não há outras a selecionar).

## Motivo de não utilizar o dataset completo

O dataset completo (928 arquivos, ~586,7 MB) contém quase metade de conteúdo duplicado, o que infla artificialmente a contagem sem agregar diversidade real e pesaria desnecessariamente o repositório acadêmico. A amostra de 120 imagens únicas balanceadas entre as 4 classes atende com folga ao requisito mínimo da FIAP (100 imagens no total), preserva a integridade e representatividade real do material disponível, e mantém o repositório em tamanho administrável.

## Preservação do dataset original

O dataset bruto completo (928 arquivos, ~586,7 MB) permanece apenas na fonte local original (`C:\Users\muril\Downloads\ecg_dataset_mendeley`, fora do repositório) e é referenciado por DOI/URL oficial do Mendeley Data. Não foi copiado para `document/other/fontes_parte3/`.
