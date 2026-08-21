# Plano de Execução — CardioIA: Fase 1, Cap. 1 (Busca de Dados)

> **Este é o plano oficial da atividade.** Deve ser atualizado sempre que houver mudança de estratégia, novo requisito identificado, conclusão de etapa, decisão relevante ou alteração de sequenciamento. Fonte do enunciado: `document/other/fontes_parte1/Fase 1_Cap 1_Exercício.docx`.

## Contexto

Atividade em grupo da FIAP (curso de IA), projeto **CardioIA** — uma plataforma que simulará um ecossistema de cardiologia inteligente ao longo de 7 fases. Nesta Fase 1, o papel é de **cientista de dados hospitalar**: buscar, organizar e documentar três tipos de dados (numéricos, textuais, visuais) relacionados à saúde cardiovascular, que servirão de base para fases futuras (ML, Visão Computacional, IoT, agentes). Prazo: 02/09/2026, 23h59. Grupo 69, participante único (Murilo Salla) — mín. 1 integrante permitido.

O repositório já é um template padrão FIAP com pastas fixas (`.github`, `assets`, `config`, `document`, `scripts`, `src`) que devem ser preservadas.

### Regra de trabalho para esta e futuras atividades FIAP
Qualquer documento acadêmico fornecido pela FIAP (.docx ou similar) deve ser analisado **integralmente** antes de considerar os requisitos completamente mapeados — isso inclui texto corrido, tabelas, imagens embutidas, diagramas, mapas mentais, boxes de atenção/dica, screenshots e hyperlinks. Extrair apenas o texto do XML/documento não é suficiente: requisitos obrigatórios podem estar exclusivamente dentro de imagens (como ocorreu com o formato .csv/.xlsx nesta atividade, encontrado apenas em uma imagem "Atenção" embutida no docx). Nenhuma imagem deve ser classificada como decorativa sem antes ser aberta e inspecionada individualmente.

## Requisitos extraídos do enunciado

### Objetivo geral
Buscar e preparar três tipos de dados fundamentais para pacientes cardíacos: numéricos, textuais e visuais, com foco em Governança de Dados e viés desde o início.

### Parte 1 — Dados Numéricos (IoT)
- Dataset com **mínimo 100 linhas** (reais ou simulados).
- **Formato obrigatório do arquivo: `.csv` ou `.xlsx`** (requisito encontrado apenas em uma imagem "Atenção" embutida no docx, imediatamente após a instrução do dataset — não constava no texto corrido).
- Variáveis sugeridas: idade, sexo, pressão arterial, colesterol, histórico de doenças cardíacas, sintomas, frequência cardíaca, etc.
- Dataset organizado no repositório GitHub.
- README.md deve conter: link para os dados hospedados em OneDrive/Google Drive/serviço público equivalente; explicação clara da origem dos dados (reais vs. simulados); quais variáveis são clinicamente mais relevantes e por quê (justificativa para IA em saúde).

### Parte 2 — Dados Textuais (NLP)
- **Mínimo 2 textos** (.txt) sobre doenças cardíacas, saúde pública, sintomas ou tratamentos.
- Fontes possíveis: SciELO, BVS, artigos do SUS, ou literatura clássica (Project Gutenberg).
- Arquivos adicionados no repositório em subpasta "assets" ou "docs".
- README.md deve explicar como esses textos podem ser explorados por NLP (ex.: análise de sentimentos, extração de sintomas, classificação de tópicos) e justificar a relevância para IA em saúde.

### Parte 3 — Dados Visuais (VC)
- **Mínimo 100 imagens** (.jpg ou .png) de um tipo de exame cardiológico (ECG, angiograma, raio-X torácico — escolher um tipo).
- Link para as imagens hospedadas em OneDrive/Google Drive/serviço público, incluído no mesmo README.md.
- Justificativa de como as imagens podem ser analisadas por Visão Computacional (detecção de padrões, bordas, anomalias) e importância para IA em saúde.

### Entregáveis (repositório GitHub deve conter)
- README.md detalhado: explica o projeto, descreve as 3 partes, indica objetivos e fontes dos dados.
- Subpasta `docs` ou `assets` com os textos (.txt).
- Links públicos (acessíveis a qualquer pessoa) para os dados completos hospedados externamente (numéricos, textuais, visuais).

## Contexto complementar — mapa mental oficial CardioIA (fonte visual)

> **Fonte:** `document/other/fontes_parte1/mapaMental - CardioIA_ A Nova Era da Cardiologia Inteligente.svg` (versão em alta resolução do mapa mental do enunciado). Todo o conteúdo abaixo é **DIRETRIZ/CONTEXTO DO MAPA MENTAL**, não requisito do enunciado desta fase.

### As 7 fases do CardioIA (nomes e escopo resumido)

| Fase | Nome | Escopo resumido |
|---|---|---|
| 1 | Batimentos de Dados — Mapeando o Coração Moderno | Construção de base de dados de pacientes cardiológicos; coleta de fontes públicas/simuladas/formulários; discussão de governança em IA e impacto dos dados. **(fase atual)** |
| 2 | Diagnóstico Automatizado — IA no Estetoscópio Digital | Modelos de IA para identificar risco de doenças; classificadores supervisionados; responsabilidade no uso de IA na medicina. |
| 3 | Monitoramento Contínuo — IoT no Peito do Paciente | Simulação de wearable médico com sensores ESP32 para monitoramento em tempo real; dashboard de apresentação de dados. |
| 4 | Coração em Imagens — Diagnóstico com Visão Computacional | Sistema para interpretar imagens de exames médicos; detecção de alterações suspeitas; módulos de visualização. |
| 5 | Suporte Digital ao Paciente — Assistente Cardiológico Virtual | Chatbot para acompanhamento de pacientes em casa; uso de NLP; ética e empatia no atendimento virtual. |
| 6 | Coração Sob Controle — Previsão de Crises com IA | Sistema preditivo de eventos cardíacos com séries temporais; previsão de picos de risco; planejamento de protocolos de emergência. |
| 7 | CardioIA — Plataforma de Inteligência Cardíaca Total | Integração de todos os módulos em uma única plataforma; foco em usabilidade, fluxo de informação e arquitetura final. |

### Dependências futuras relevantes para decisões desta Fase 1 (DIRETRIZ/CONTEXTO — não requisito)

- **Parte 1 (dados numéricos):** poderá alimentar modelos de Machine Learning na **Fase 2** (Diagnóstico Automatizado).
- **Sinais vitais** (ex.: frequência cardíaca, pressão arterial): possuem relação conceitual com a **Fase 3** (IoT/monitoramento contínuo via ESP32) — não implica requisito de dado de IoT nesta fase, apenas contexto de continuidade.
- **Parte 2 (textos):** devem ser escolhidos considerando potencial de reutilização na **Fase 5** (NLP/chatbot de suporte ao paciente).
- **Parte 3 (imagens):** devem ser escolhidas considerando potencial de reutilização na **Fase 4** (Visão Computacional/diagnóstico por imagem).
- **Fase 6** (séries temporais/previsão de crises): não gera dependência de dado nesta fase, mas permanece como contexto para decisões futuras (ex.: preferir fontes que eventualmente tenham dimensão temporal, quando isso não conflitar com os requisitos atuais).

**DECISÃO DE PROJETO:** essas diretrizes de reutilização futura devem ser usadas como critério de desempate ao escolher fontes/dados nas Partes 2 e 3 (preferir textos/imagens com maior potencial de reaproveitamento em NLP/Visão Computacional), mas nunca como requisito adicional que extrapole o enunciado atual.

### Estatística de contexto (mapa mental)

- O mapa mental cita que doenças cardiovasculares são a principal causa de mortes no mundo, com aproximadamente **17,9 milhões de óbitos anuais**. Este número é **apenas contexto do material de apoio FIAP**, sem fonte primária validada por este projeto.
- **Não deve ser usado no README ou no documento acadêmico final (`ai_project_document_fiap.md`) sem antes localizar e citar uma fonte primária confiável** (ex.: OMS/WHO) para essa estatística.

## Requisitos e informações identificados em elementos visuais (imagens/tabelas/boxes do docx)

| Elemento | Localização no docx | Conteúdo | Classificação |
|---|---|---|---|
| Mapa mental (imagem) | Início do enunciado | Contexto do CardioIA, objetivos do projeto e as 7 fases do curso (Fase 1 "Batimentos de Dados" até Fase 7 "Plataforma de Inteligência Cardíaca Total") | CONTEXTO — útil para a seção "Visão Geral do Projeto" do documento resumo; não é entregável novo |
| Hyperlink (SharePoint FIAP) | Logo após menção ao arquivo .svg do mapa mental | Link fonte do próprio mapa mental (material de apoio da FIAP) | CONTEXTO |
| Box "Atenção" (imagem) | Após "Objetivo geral da atividade" | Dados de saúde/finanças são sensíveis, protegidos por ética/legal/privacidade, difícil disponibilização pública | CONTEXTO — reforça justificativa de governança já presente no texto |
| Box "Atenção" (imagem) | Imediatamente após a instrução do dataset numérico (Parte 1) | **"O formato deverá ser .csv ou .xlsx"** | **REQUISITO OBRIGATÓRIO** — incorporado à Parte 1 |
| Box "Dica" (imagem) | Após a seção "Entregáveis" | "Caso queira, já organize pastas no repositório para armazenar os notebooks futuros que vão consumir esses dados no Colab ou Jupyter" | BOA PRÁTICA OPCIONAL — não criar pasta vazia agora; só se houver necessidade real de notebook nesta fase |
| Tabela de critérios (imagem) | Antes de "Mensagem final" | Rubrica de avaliação completa (10 pontos, 5 itens) | **REQUISITO OBRIGATÓRIO** — ver seção Critérios de Avaliação abaixo |

## Critérios de avaliação (10 pontos totais)

| Critério | Pontos |
|---|---|
| Parte 1 — Dataset numérico entregue corretamente, organizado e explicado | 3 |
| Parte 2 — Textos selecionados e contextualizados corretamente | 2 |
| Parte 3 — Imagens entregues e bem justificadas em seu potencial para análise por IA | 2 |
| Documento resumo com explicações claras, objetivas e bem estruturadas | 2 |
| Cumprimento das orientações gerais e prazo de entrega | 1 |

## Governança de dados / ética / viés

- Enunciado pede explicitamente atenção à **Governança de Dados** e **viés**, desde a escolha das fontes.
- Origem dos dados (real vs. simulado) deve ser declarada com transparência no README.
- Persistência e criatividade são valorizadas: se dados reais forem difíceis de obter, é aceitável gerar dados simulados ou combinar fontes.
- Dados de saúde são sensíveis; optar por datasets já anonimizados/públicos (como o UCI Heart Disease) mitiga esse risco.

## Avaliação do template atual

- **Pastas reaproveitadas (sem criar pastas novas na raiz):** `document/other/` (enunciado + este plano), `document/` (`ai_project_document_fiap.md` como documento resumo), `assets/` (dados, textos, imagens de amostra), `scripts/` (scripts auxiliares), `src/` (uso opcional).
- **Arquivos a atualizar:** `README.md` (raiz) e `document/ai_project_document_fiap.md`.
- **Subpastas criadas dentro de `assets/`:** `dados/raw`, `dados/processed`, `textos/`, `imagens/` — não viola o template pois não cria pastas na raiz.
- **Não alterar:** `.github/problem-report.md`, `.gitattributes`, `.gitignore`, `assets/logo-fiap.png`, estrutura de pastas raiz, e o arquivo `.docx` do enunciado.

## Estrutura de entrega proposta

```
README.md                          → preenchido: descrição, 3 partes, links, justificativas
document/
  ai_project_document_fiap.md      → documento resumo preenchido
  other/
    Fase 1_Cap 1_Exercício.docx    → enunciado original (preservado)
    plano_execucao.md               → este arquivo (plano oficial)
assets/
  dados/
    raw/                            → dataset original UCI intacto (não modificado)
    processed/                      → dataset tratado (.csv, >=100 linhas, cabeçalho legível)
  textos/                           → >=2 arquivos .txt (NLP) + fonte de cada um
  imagens/                          → amostra local opcional (conjunto completo fica hospedado externamente)
scripts/
  preparar_dataset_numerico.py     → script de tratamento do dataset numérico
src/
  (uso opcional; notebooks/ NÃO criada agora — só se necessário nesta fase)
config/
  (não utilizado nesta fase)
```

## Plano de execução sequencial (por peso de avaliação)

1. **Dataset numérico (Parte 1 — peso 3)** — CONCLUÍDA TECNICAMENTE (falta apenas hospedagem externa/link público)
2. **Textos médicos/literários (Parte 2 — peso 2)** — CONCLUÍDA TECNICAMENTE (falta apenas hospedagem externa/link público)
3. **Imagens médicas (Parte 3 — peso 2)** — CONCLUÍDA TECNICAMENTE (falta apenas hospedagem externa/link público)
4. **README.md principal** — CONCLUÍDO
5. **Documento resumo formal (`document/ai_project_document_fiap.md`)** — CONCLUÍDO
6. **Revisão final de governança/viés e prazo** — PENDENTE

## Estratégia de dados

**Parte 1 — Numéricos:** mínimo 100 linhas; variáveis clínicas (idade, sexo, PA, colesterol, histórico, sintomas, FC); formato obrigatório `.csv` ou `.xlsx`; pode ser simulado ou real, desde que declarado.

**Parte 2 — Textos:** mínimo 2 arquivos .txt; fontes aceitas: SciELO, BVS, artigos do SUS, Project Gutenberg (literatura clássica); aplicações de NLP a justificar: análise de sentimentos, extração de sintomas, classificação de tópicos.

**Parte 3 — Visuais:** mínimo 100 imagens .jpg/.png; tipo de exame único (ECG, angiograma ou raio-X torácico); aplicações de VC a justificar: detecção de padrões, identificação de bordas, reconhecimento de anomalias.

## Riscos

- Template FIAP descaracterizado (criar pastas na raiz, apagar READMEs de estrutura antes da hora).
- Links de Drive/OneDrive configurados como privados (corretor não consegue acessar).
- Quantidade insuficiente de linhas/textos/imagens (abaixo do mínimo exigido).
- Fontes sem procedência clara (sem citar origem/licença).
- Commitar as 100+ imagens diretamente no GitHub, deixando o repositório pesado.
- Faltar justificativa técnica (clínica/NLP/VC) para cada parte.
- README incompleto ou com placeholders do template não preenchidos.
- Não declarar se dados são reais ou simulados.
- Ignorar menção a governança de dados/viés.
- Perder o prazo (02/09/2026 23h59).

## Checklist de cobertura do enunciado

- [x] Texto corrido do enunciado lido integralmente.
- [x] Todas as imagens embutidas no docx inspecionadas individualmente (mapa mental, 2 boxes "Atenção", box "Dica", tabela de critérios).
- [x] Hyperlinks internos rastreados (SharePoint do mapa mental).
- [x] Requisito de formato .csv/.xlsx (só visível em imagem) incorporado.
- [x] Critérios de avaliação (tabela em imagem) incorporados.
- [x] Dica de organização para notebooks futuros registrada (sem ação imediata).
- [x] Mapa mental das 7 fases registrado como contexto.
- **Cobertura considerada integral** — nenhum elemento do docx pendente de inspeção.

## Estado atual de cada etapa

### Parte 1 — Dados Numéricos: QUASE CONCLUÍDA
- Dataset real escolhido: **UCI Heart Disease (Cleveland)**, 303 linhas, licença CC BY 4.0.
- Original intacto salvo em `assets/dados/raw/heart+disease/` (arquivos-fonte da UCI, não modificados).
- Versão tratada gerada em `assets/dados/processed/heart_disease_cleveland.csv` (303 linhas + cabeçalho, 14 variáveis clínicas com nomes/valores legíveis em português) — **já em formato `.csv`, cumprindo o requisito de formato**.
- Script de processamento salvo em `scripts/preparar_dataset_numerico.py` (reprodutível a partir do dado bruto).
- Dataset **validado**: 303 registros, 14 colunas, sem duplicidades, valores ausentes reais apenas em `num_vasos_principais` (4) e `resultado_thal` (2), herdados da fonte oficial e preservados sem imputação.
- Dicionário de variáveis criado: `assets/dados/processed/dicionario_variaveis.md` (uma linha por coluna, com nome original UCI, significado, tipo, valores possíveis e interpretação clínica básica).
- Documento de apoio da Parte 1 criado: `document/other/parte1_dados_numericos.md` (fonte, descrição, justificativa clínica das principais variáveis, processo de preparação, governança/privacidade/viés) — pronto para consolidação no README final.
- **Falta (ação manual pendente):** publicar o dataset em serviço de armazenamento público (OneDrive/Google Drive) com acesso "qualquer pessoa com o link" e inserir o link no espaço já reservado em `document/other/parte1_dados_numericos.md` e, futuramente, no README principal.

### Parte 2 — Dados Textuais: CONCLUÍDA TECNICAMENTE
- Reorganização documental: `document/other/fontes_parte1/` passou a conter somente materiais externos/originais (`Fase 1_Cap 1_Exercício.docx` e o SVG do mapa mental); `plano_execucao.md`, `parte1_dados_numericos.md` e `readme.md` retornaram para `document/other/`. Referências internas atualizadas.
- `document/other/fontes_parte2/` criada, com os 3 PDFs de origem preservados: `Prevenção clínica de doenças cardiovasculares, cerebrovasculares e renais.pdf` (56 p.), `PCDT_SindromesCoronarianasAgudas.pdf` (46 p.) e `Linha de Cuidado do Infarto Agudo do Miocárdio e o Protocolo de Síndromes Coronarianas Agudas.pdf` (75 p., mantido como fonte complementar).
- Corpus final: `assets/textos/texto_01_prevencao_cardiovascular.txt` e `assets/textos/texto_02_sindromes_coronarianas_agudas.txt`, com metadados de rastreabilidade completos.
- Corpus validado tecnicamente (UTF-8 sem corrupção, sem HTML, sequência de páginas íntegra e completa em ambos, seções/termos técnicos esperados presentes, sem sinais de truncamento) e auditado por amostragem estrutural contra os PDFs de origem.
- Documento de apoio criado: `document/other/parte2_dados_textuais.md`.

### Parte 3 — Dados Visuais: CONCLUÍDA TECNICAMENTE
- Modalidade escolhida: Eletrocardiograma (ECG).
- Fonte validada: "ECG Images dataset of Cardiac Patients — Version 2" (Khan & Hussain, Mendeley Data, DOI 10.17632/gwbz3fsgp8.2, CC BY 4.0).
- Dataset original auditado localmente: 928 arquivos físicos, 4 classes, resolução 2213×1572, ~586,7 MB.
- Duplicidades identificadas: 437 dos 928 arquivos (≈47%) eram cópias binárias exatas (hash SHA-256) em 3 das 4 classes; apenas 491 imagens eram únicas. Divergência de nomenclatura resolvida (pasta "240x12" continha fisicamente 239 arquivos).
- Amostra final definida: 30 imagens únicas por classe, 120 imagens no total, seleção determinística e reprodutível (`random_state = 42`), sem duplicatas exatas.
- Preparação aplicada: remoção do cabeçalho administrativo (ID de paciente, data/hora, dados demográficos) por crop validado visualmente; remoção de metadados EXIF; sem redimensionamento ou alteração do traçado clínico.
- Imagens validadas tecnicamente (formato, dimensões, integridade, ausência de duplicidade) e por auditoria visual.
- Documentação criada: `document/other/fontes_parte3/fonte_dataset.md`, `document/other/fontes_parte3/manifesto_amostra.csv` e `document/other/parte3_dados_visuais.md`.
- **Link público externo da Parte 3: PENDENTE** — publicação externa a ser realizada no fechamento do projeto, mesmo padrão da Parte 1.

### README.md principal: CONCLUÍDO — template FIAP preenchido (grupo, integrantes, tutor, coordenador, descrição, estrutura, execução, histórico).

### Documento resumo formal: CONCLUÍDO — `document/ai_project_document_fiap.md` preenchido em todos os capítulos do template.

### Revisão final de governança/viés e prazo: PENDENTE

## Próximos passos

1. **Pendência manual das Partes 1, 2 e 3 (proposital, para o fechamento do projeto):** publicar os três conjuntos de dados (numérico, textual e visual) em serviço de armazenamento público (OneDrive/Google Drive ou equivalente) e inserir os links nos espaços já reservados em `document/other/parte1_dados_numericos.md`, `document/other/parte2_dados_textuais.md`, `document/other/parte3_dados_visuais.md` e na seção `## 🔗 Links públicos dos conjuntos de dados` do `README.md`.
2. Revisão final de governança/viés e prazo, após a publicação dos links.

## Correção pontual — interpretação da variável `thal`

Auditoria da Parte 1 identificou uma interpretação inadequada da variável original `thal` da UCI, que havia sido traduzida no dataset processado como `talassemia`. A documentação oficial usada no projeto (`assets/dados/raw/heart+disease/heart-disease.names`) registra apenas os códigos e rótulos do atributo (`3 = normal; 6 = fixed defect; 7 = reversable defect`), sem expandir o significado da sigla `thal` — portanto, a expansão "talassemia" não é sustentada pelas fontes disponíveis no projeto e foi removida.

- Coluna processada corrigida de `talassemia` para `resultado_thal` em todos os artefatos derivados: `scripts/preparar_dataset_numerico.py`, `assets/dados/processed/heart_disease_cleveland.csv`, `assets/dados/processed/dicionario_variaveis.md`, `document/other/parte1_dados_numericos.md`.
- O atributo original UCI continua identificado como `thal` (sem alteração) em todas as referências à fonte.
- Script, CSV processado e documentação foram sincronizados e revalidados (303 registros, 14 colunas, sem duplicidades, 4 ausentes em `num_vasos_principais`, 2 ausentes em `resultado_thal`; nenhuma outra transformação/dado alterado).
- Dados brutos da UCI (`assets/dados/raw/`) não foram alterados.

## Versionamento (Git/GitHub)

- **Git local:** inicializado (`git init`) na raiz do repositório em 21/08/2026. Nenhum commit realizado ainda neste momento.
- **`.gitignore`:** ajustado para permitir o versionamento dos datasets processados exigidos pela atividade (`assets/dados/processed/*.csv`, `assets/dados/processed/*.xlsx`), mantendo o bloqueio padrão de tabelas genéricas (`*.csv`, `*.tsv`, `*.xls`, `*.xlsx`) fora dessa pasta, além de proteções para `.env`/segredos, ambientes virtuais Python, cache Python e arquivos de SO/editor.
- **`.claude/` configurado para não ser versionado:** regra `.claude/` adicionada ao `.gitignore` — confirmado via `git check-ignore` que `.claude/settings.local.json` passou a ser ignorado.
- **Branch padrão:** `main` (renomeada de `master`).
- **Proprietário GitHub:** `murilosalla-blip`.
- **Repositório remoto:** criado — `murilosalla-blip/fiap-ano02-fase01-cap01-cardioia` (renomeado de `fiap-fase01-cap01-cardioia` para incluir o Ano 2), público, sem README/`.gitignore`/licença automáticos.
- **URL:** `https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia`
- **Remote `origin`:** configurado (`https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia.git`), fetch e push corretos.
- **Primeiro commit:** concluído — hash curto `e0c063a` ("chore: estrutura inicial do projeto CardioIA", 39 arquivos).
- **Segundo commit:** concluído — hash curto `b579e00` ("docs: atualiza estado de versionamento do projeto").
- **Primeiro push:** concluído — branch `main` enviada, upstream `origin/main` configurado.
- **Parte 2:** ainda não iniciada.

---
*Histórico de atualizações:*
- *Criação inicial deste arquivo: consolidação do plano aprovado em `~/.claude/plans/` após auditoria multimodal completa do enunciado (texto + imagens + tabelas). A partir desta versão, este arquivo é a fonte oficial do plano da atividade.*
- *Atualização: Parte 1 validada (303 registros, 14 colunas, sem duplicidades, ausentes apenas em 2 colunas herdados da fonte). Criados `assets/dados/processed/dicionario_variaveis.md` e `document/other/parte1_dados_numericos.md`. Pendência restante da Parte 1: apenas a publicação externa do dataset e inserção do link público.*
- *Atualização: incorporado contexto complementar do mapa mental oficial CardioIA (`document/other/fontes_parte1/mapaMental - CardioIA_ A Nova Era da Cardiologia Inteligente.svg`) — nomes/escopo das 7 fases e diretrizes de reutilização futura dos dados desta fase nas Fases 2 a 6. Nenhum novo requisito obrigatório foi criado; classificado integralmente como DIRETRIZ/CONTEXTO DO MAPA MENTAL.*
- *Atualização: `.gitignore` ajustado (exceções para `assets/dados/processed/*.csv` e `*.xlsx`) e Git local inicializado na raiz. Nenhum commit realizado. Repositório remoto GitHub ainda não criado; nome candidato `fiap-fase01-cap01-cardioia` aguardando aprovação.*
- *Atualização: adicionada regra `.claude/` ao `.gitignore`. Primeiro commit local realizado (`e0c063a`) e segundo commit de atualização do plano (`b579e00`).*
- *Atualização: branch local renomeada para `main`; repositório remoto `murilosalla-blip/fiap-fase01-cap01-cardioia` criado (público, vazio); remote `origin` configurado; primeiro push realizado com sucesso (`origin/main`).*
- *Atualização: corrigida interpretação inadequada da variável `thal` — coluna processada renomeada de `talassemia` para `resultado_thal` em script, CSV, dicionário e documento de apoio da Parte 1, sem alterar dados brutos nem a nomenclatura do atributo original UCI (`thal`). Link externo e README final seguem propositalmente pendentes para o fechamento do projeto.*
- *Atualização: repositório remoto renomeado de `fiap-fase01-cap01-cardioia` para `fiap-ano02-fase01-cap01-cardioia` (preservando histórico via `gh repo rename`), para alinhar o nome ao Ano 2 da FIAP. Remote `origin` local atualizado; referências ao nome antigo corrigidas em `README.md` e neste plano.*
