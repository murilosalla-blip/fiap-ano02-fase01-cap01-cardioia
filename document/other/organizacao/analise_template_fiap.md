# Nossa análise de aderência ao modelo FIAP

Analisamos em 24/10/2026 o repositório [agodoi/templateFiapVfinal](https://github.com/agodoi/templateFiapVfinal), na revisão `50e1e2720637b222357a7ebd1919c38a44af7cd2`, e comparamos suas orientações com a organização atual do CardioIA após o merge do PR #2. Nesta análise, não movi código nem alteramos configurações de execução.

## Orientações explícitas que identificamos

No [README do modelo](https://github.com/agodoi/templateFiapVfinal/blob/50e1e2720637b222357a7ebd1919c38a44af7cd2/README.md), identificamos:

- Identificação da instituição, projeto, grupo, integrantes e professores.
- Descrição baseada no PBL, com limite de 600 palavras nessa seção.
- Destinação do código-fonte de todas as fases a `src/`.
- Destinação dos documentos a `document/`, com complementos em `document/other/`.
- Destinação dos scripts auxiliares a `scripts/` e das configurações a `config/`.
- Uso de `assets/` para imagens e outros recursos não estruturados.
- Instruções de pré-requisitos, versões, instalação e reprodução, organizadas por fase.
- Histórico de lançamentos e bloco de licença do modelo.

No [modelo do documento principal](https://github.com/agodoi/templateFiapVfinal/blob/50e1e2720637b222357a7ebd1919c38a44af7cd2/document/ai_project_document_fiap.md), identificamos introdução, visão geral, desenvolvimento, resultados e avaliações, conclusões, referências e anexos. Identificamos também a instrução de retirar os trechos de orientação do documento final.

No [arquivo de orientação de src](https://github.com/agodoi/templateFiapVfinal/blob/50e1e2720637b222357a7ebd1919c38a44af7cd2/src/readme.md), identificamos o critério de considerar o último commit dentro do prazo da sprint, com alterações posteriores destinadas à próxima sprint. Os arquivos de orientação de `src/` e `document/other/` indicam remoção ao final do módulo.

No [modelo de relato de problemas](https://github.com/agodoi/templateFiapVfinal/blob/50e1e2720637b222357a7ebd1919c38a44af7cd2/.github/problem-report.md), identificamos o uso de texto para saídas de console, capturas para problemas visuais e inclusão da URL do repositório.

## Comparação que realizamos

| Item | O que conferimos no CardioIA | Ajuste que consideramos necessário |
|---|---|---|
| Identificação | Encontramos instituição, logo, projeto, Grupo Aura, três integrantes com RM, tutor e coordenador | Vamos preservar a identificação; não vamos inventar outros integrantes nem links de perfil |
| Descrição | Contamos aproximadamente 489 palavras entre a seção Descrição e a próxima seção | Vamos manter a descrição dentro das 600 palavras e atualizar sua síntese para refletir a evolução do projeto |
| Código-fonte | Encontramos somente `src/readme.md` em `src/`; o código funcional está em `fase2/`, `fase3/` e `src/fase2/portal-cardioia/` | Vamos propor a organização por fase dentro de `src/` |
| Configurações | Encontramos apenas orientação em `config/`; a Fase 3 contém contratos e configuração Node-RED fora dela | Vamos separar os parâmetros e as configurações reutilizáveis, preservando os manifestos locais exigidos pelas ferramentas |
| Scripts auxiliares | Encontramos preparação de datasets em `scripts/`, mas validação e inicialização da Fase 3 em outras pastas | Vamos consolidar os auxiliares em `scripts/`, com subpastas por fase |
| Documentação | Encontramos documentos em `document/`, mas relatórios, roteiros e checklists também misturados aos subprojetos da raiz | Vamos organizar a documentação principal e complementar nos destinos indicados pelo modelo |
| Documento principal | Encontramos as seções do modelo preenchidas para a Fase 1, incluindo menções a fases seguintes como trabalho futuro | Vamos atualizar a visão consolidada ou declarar o recorte histórico e estabelecer navegação explícita para as fases atuais |
| Trechos de orientação | Ainda encontramos instruções de preenchimento no documento principal e readmes de orientação em pastas do modelo | Vamos substituir as orientações por conteúdo útil e realizar a limpeza exigida para a entrega final |
| Execução | Encontramos comandos no README principal para Fases 1 e 2 e guia da Fase 3 em documentação própria | Vamos padronizar o acesso às instruções por fase e revisar todos os comandos após a reorganização |
| Histórico | Encontramos entradas até 0.8.0/Fase 2; a Fase 3 já possui entregas validadas e PR integrado | Vamos acrescentar a evolução da Fase 3 sem alterar datas ou simular lançamentos antigos |
| Evidências | Encontramos logs de console em texto e capturas visuais, com índices e resultados | Vamos preservar o conteúdo e reorganizar os destinos e os links, mantendo a rastreabilidade |
| Ignore e normalização | Encontramos `.gitattributes` compatível e `.gitignore` ampliado para ferramentas, ambientes, segredos e execução local | Vamos preservar as proteções e conferir as exceções de datasets exigidos pelas atividades |

## O que não tratamos como regra literal

Não encontramos no modelo uma proibição textual de toda pasta adicional na raiz. Identificamos, porém, uma orientação explícita de manter o código-fonte em `src/`; por isso consideramos a localização atual do código um desalinhamento com a distribuição proposta.

Não interpretamos os cinco nomes exemplificativos como exigência de cinco integrantes, nem os links de exemplo como obrigação de criar perfis. Também não interpretamos o limite de 600 palavras como limite do README inteiro: ele aparece na orientação da descrição do PBL.

O `.gitignore` inicial ignora arquivos CSV, TSV e planilhas, mas não encontramos uma regra que proíba adaptações para entregas que exigem datasets processados. Vamos manter essas exceções justificadas, sem voltar a incluir arquivos de execução, dependências instaladas ou credenciais.

Não consideramos o documento principal da Fase 1 incorreto apenas por ser histórico. Identificamos a necessidade de tornar claro seu escopo e de dar acesso à documentação consolidada de um repositório que já apresenta as Fases 1, 2 e 3.

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

Essa árvore é nossa proposta de adaptação, não uma árvore adicional imposta pelo modelo. Vamos classificar os arquivos pela função, preservando manifestos e arquivos associados que as ferramentas exigem junto dos subprojetos.

## Ordem de execução que proponho

1. Vamos inventariar os arquivos e registrar os destinos antes de mover qualquer componente.
2. Vamos preservar os commits, as evidências das entregas validadas e as alterações locais que ficaram fora do PR #2.
3. Vamos reorganizar a Fase 3 e atualizar caminhos de imports, contratos, firmware, Node-RED, scripts e logs locais.
4. Vamos planejar a migração da Fase 2 e do portal considerando workflows, notebooks, build e aplicações já publicadas; não vamos presumir que mover um arquivo atualiza a configuração de hospedagem externa.
5. Vamos atualizar README, documento principal, histórico, links e instruções por fase, mantendo os registros novos em primeira pessoa.
6. Vamos repetir os testes e a reprodução nos novos caminhos, conferir os links e revisar a documentação antes de abrir um PR de organização.

Mantemos os desafios Ir Além e os relatórios finais pendentes. A reorganização não representa uma nova validação clínica nem a conclusão integral da Fase 3.
