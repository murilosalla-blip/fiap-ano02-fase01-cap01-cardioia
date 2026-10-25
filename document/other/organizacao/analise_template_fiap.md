# Minha análise de aderência ao modelo FIAP

Analisei em 24/10/2026 o repositório [agodoi/templateFiapVfinal](https://github.com/agodoi/templateFiapVfinal), na revisão `50e1e2720637b222357a7ebd1919c38a44af7cd2`, e comparei suas orientações com a organização atual do CardioIA após o merge do PR #2. Nesta análise, não movi código nem alterei configurações de execução.

## Orientações explícitas que identifiquei

No [README do modelo](https://github.com/agodoi/templateFiapVfinal/blob/50e1e2720637b222357a7ebd1919c38a44af7cd2/README.md), identifiquei:

- Identificação da instituição, projeto, grupo, integrantes e professores.
- Descrição baseada no PBL, com limite de 600 palavras nessa seção.
- Destinação do código-fonte de todas as fases a `src/`.
- Destinação dos documentos a `document/`, com complementos em `document/other/`.
- Destinação dos scripts auxiliares a `scripts/` e das configurações a `config/`.
- Uso de `assets/` para imagens e outros recursos não estruturados.
- Instruções de pré-requisitos, versões, instalação e reprodução, organizadas por fase.
- Histórico de lançamentos e bloco de licença do modelo.

No [modelo do documento principal](https://github.com/agodoi/templateFiapVfinal/blob/50e1e2720637b222357a7ebd1919c38a44af7cd2/document/ai_project_document_fiap.md), identifiquei introdução, visão geral, desenvolvimento, resultados e avaliações, conclusões, referências e anexos. Identifiquei também a instrução de retirar os trechos de orientação do documento final.

No [arquivo de orientação de src](https://github.com/agodoi/templateFiapVfinal/blob/50e1e2720637b222357a7ebd1919c38a44af7cd2/src/readme.md), identifiquei o critério de considerar o último commit dentro do prazo da sprint, com alterações posteriores destinadas à próxima sprint. Os arquivos de orientação de `src/` e `document/other/` indicam remoção ao final do módulo.

No [modelo de relato de problemas](https://github.com/agodoi/templateFiapVfinal/blob/50e1e2720637b222357a7ebd1919c38a44af7cd2/.github/problem-report.md), identifiquei o uso de texto para saídas de console, capturas para problemas visuais e inclusão da URL do repositório.

## Comparação que realizei

| Item | O que conferi no CardioIA | Ajuste que considero necessário |
|---|---|---|
| Identificação | Encontrei instituição, logo, projeto, Grupo Aura, três integrantes com RM, tutor e coordenador | Vou preservar a identificação; não vou inventar outros integrantes nem links de perfil |
| Descrição | Contei aproximadamente 489 palavras entre a seção Descrição e a próxima seção | Vou manter a descrição dentro das 600 palavras e atualizar sua síntese para refletir a evolução do projeto |
| Código-fonte | Encontrei somente `src/readme.md` em `src/`; o código funcional está em `fase2/`, `fase3/` e `src/fase2/portal-cardioia/` | Vou propor a organização por fase dentro de `src/` |
| Configurações | Encontrei apenas orientação em `config/`; a Fase 3 contém contratos e configuração Node-RED fora dela | Vou separar os parâmetros e as configurações reutilizáveis, preservando os manifestos locais exigidos pelas ferramentas |
| Scripts auxiliares | Encontrei preparação de datasets em `scripts/`, mas validação e inicialização da Fase 3 em outras pastas | Vou consolidar os auxiliares em `scripts/`, com subpastas por fase |
| Documentação | Encontrei documentos em `document/`, mas relatórios, roteiros e checklists também misturados aos subprojetos da raiz | Vou organizar a documentação principal e complementar nos destinos indicados pelo modelo |
| Documento principal | Encontrei as seções do modelo preenchidas para a Fase 1, incluindo menções a fases seguintes como trabalho futuro | Vou atualizar a visão consolidada ou declarar o recorte histórico e estabelecer navegação explícita para as fases atuais |
| Trechos de orientação | Ainda encontrei instruções de preenchimento no documento principal e readmes de orientação em pastas do modelo | Vou substituir as orientações por conteúdo útil e realizar a limpeza exigida para a entrega final |
| Execução | Encontrei comandos no README principal para Fases 1 e 2 e guia da Fase 3 em documentação própria | Vou padronizar o acesso às instruções por fase e revisar todos os comandos após a reorganização |
| Histórico | Encontrei entradas até 0.8.0/Fase 2; a Fase 3 já possui entregas validadas e PR integrado | Vou acrescentar a evolução da Fase 3 sem alterar datas ou simular lançamentos antigos |
| Evidências | Encontrei logs de console em texto e capturas visuais, com índices e resultados | Vou preservar o conteúdo e reorganizar os destinos e os links, mantendo a rastreabilidade |
| Ignore e normalização | Encontrei `.gitattributes` compatível e `.gitignore` ampliado para ferramentas, ambientes, segredos e execução local | Vou preservar as proteções e conferir as exceções de datasets exigidos pelas atividades |

## O que não tratei como regra literal

Não encontrei no modelo uma proibição textual de toda pasta adicional na raiz. Identifiquei, porém, uma orientação explícita de manter o código-fonte em `src/`; por isso considero a localização atual do código um desalinhamento com a distribuição proposta.

Não interpretei os cinco nomes exemplificativos como exigência de cinco integrantes, nem os links de exemplo como obrigação de criar perfis. Também não interpretei o limite de 600 palavras como limite do README inteiro: ele aparece na orientação da descrição do PBL.

O `.gitignore` inicial ignora arquivos CSV, TSV e planilhas, mas não encontrei uma regra que proíba adaptações para entregas que exigem datasets processados. Vou manter essas exceções justificadas, sem voltar a incluir arquivos de execução, dependências instaladas ou credenciais.

Não considerei o documento principal da Fase 1 incorreto apenas por ser histórico. Identifiquei a necessidade de tornar claro seu escopo e de dar acesso à documentação consolidada de um repositório que já apresenta as Fases 1, 2 e 3.

## Organização-alvo que proponho

```text
.github/                           automações e orientações do GitHub
assets/                            imagens, dados e capturas
config/                            parâmetros, esquemas e configurações
  fase3/
document/
  ai_project_document_fiap.md       documento principal do projeto
  fase2/                           documentação principal da fase
  fase3/                           relatórios e documentação principal da fase
  other/                           referências, apoio e registros complementares
scripts/                           preparação, inicialização e validação
  fase3/
src/
  fase2/                           código e testes da Fase 2
  fase3/                           firmware, consumidor e dashboard
  src/fase2/portal-cardioia/                  código do portal
README.md
```

Essa árvore é minha proposta de adaptação, não uma árvore adicional imposta pelo modelo. Vou classificar os arquivos pela função, preservando manifestos e arquivos associados que as ferramentas exigem junto dos subprojetos.

## Ordem de execução que proponho

1. Vou inventariar os arquivos e registrar os destinos antes de mover qualquer componente.
2. Vou preservar os commits, as evidências das entregas validadas e as alterações locais que ficaram fora do PR #2.
3. Vou reorganizar a Fase 3 e atualizar caminhos de imports, contratos, firmware, Node-RED, scripts e logs locais.
4. Vou planejar a migração da Fase 2 e do portal considerando workflows, notebooks, build e aplicações já publicadas; não vou presumir que mover um arquivo atualiza a configuração de hospedagem externa.
5. Vou atualizar README, documento principal, histórico, links e instruções por fase, mantendo os registros novos em primeira pessoa.
6. Vou repetir os testes e a reprodução nos novos caminhos, conferir os links e revisar a documentação antes de abrir um PR de organização.

Mantenho os desafios Ir Além e os relatórios finais pendentes. A reorganização não representa uma nova validação clínica nem a conclusão integral da Fase 3.
