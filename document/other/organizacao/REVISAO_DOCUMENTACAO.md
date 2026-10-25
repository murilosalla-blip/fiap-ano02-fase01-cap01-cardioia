# Revisão documental para avaliação das fases

Em **25/10/2026**, reavaliamos a documentação do CardioIA para permitir que outra pessoa obtenha os materiais, entenda as escolhas e reproduza cada atividade. Adotamos a primeira pessoa do plural nos relatos do grupo e instruções diretas nas seções de execução. Preservamos os documentos submetidos, dados, saídas dos notebooks e registros brutos das entregas anteriores.

## Referências confrontadas

| Referência | O que verificamos |
|---|---|
| [Modelo oficial FIAP](https://github.com/agodoi/templateFiapVfinal), revisão `50e1e2720637b222357a7ebd1919c38a44af7cd2` | Identificação, descrição PBL de até 600 palavras, pastas institucionais, instalação e execução por fase, histórico e atribuição da licença. O limite é da descrição, não do README inteiro. |
| [README da Fase 1 no histórico](https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia/blob/cbd9685/README.md) | Explicação das três modalidades, fontes, justificativas, links públicos e distinção entre avaliar materiais prontos e reconstruir dados brutos. |
| [README da entrega da Fase 2 no histórico](https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia/blob/2f33d41/README.md) | Atividade obrigatória, desafios, vídeo, comandos de NLP, portal e ambiente visual separado. |
| [README da branch de entrega da Julia](https://github.com/Julia-carvalho96/fiap-ano02-fase01-cap01-cardioia/blob/fase-2-machine-learning/README.md) | Consultamos `fase-2-machine-learning`, pois o `main` desse fork ainda descrevia a Fase 1. O conteúdo consultado corresponde ao blob `e1dc17793fa06624ff199e483f7bee41b3dd2c6b`. Mantivemos a publicação independente. |
| Enunciados arquivados das [Fases 1](../referencias/fase1/enunciado/), [2](../referencias/fase2/enunciado/) e [3](../referencias/fase3/enunciado/) | Conferimos texto e tabelas e abrimos individualmente as **nove imagens embutidas**: cinco na Fase 1, duas na Fase 2 e duas na Fase 3. |
| Textos da plataforma e feedbacks fornecidos nesta revisão | Consideramos as avaliações máximas das Fases 1 e 2 e as exigências atuais da Fase 3. Não utilizamos os contadores de prazo ou o status antigo dos arquivos arquivados como situação atual da entrega. |
| PDFs das Fases [1](../../fase1/cardioia_fase1_entrega_fiap.pdf) e [2](../../fase2/CardioIA_Fase2_Documento_de_Submissao.pdf), compartilhados para apoiar esta revisão | Lemos o conteúdo e inspecionamos as cinco e seis páginas, respectivamente. Retomamos a explicação por modalidade da Fase 1 e a relação requisito → implementação → evidência → situação da Fase 2. |

Na Fase 1, a terceira imagem exige CSV ou XLSX, e a quinta contém a rubrica: dados numéricos 3 pontos; textos 2; imagens 2; documento resumo 2; orientações gerais e prazo 1. Na Fase 2, a imagem de atenção recomenda reaproveitar a base anterior e lembra restrições de dados públicos; não transforma a recomendação em obrigação de manter a mesma base. Na Fase 3, a imagem de atenção exige conferir o arquivo e realizar o envio pela plataforma, com antecedência; alerta para a impossibilidade de substituição após fechamento ou correção.

Os mapas mentais situam as sete fases. Não tratamos funcionalidades de fases futuras como requisitos adicionais da entrega atual. Para a Fase 3, mantemos a [matriz específica](../../fase3/CHECKLIST_ENUNCIADO.md), incluindo os mínimos de páginas e o vídeo do Ir Além 2.

Comparamos os PDFs compartilhados com os arquivados: o da Fase 2 é idêntico byte a byte; o da Fase 1 tem conteúdo textual e links idênticos, embora os binários sejam diferentes. Mantivemos os arquivos já versionados, sem sobrescrevê-los ou criar cópias redundantes. O [índice documental](../../README.md) identifica os documentos principais, os registros de apoio e os caminhos atuais para interpretar referências antigas dentro dos PDFs.

## Correções da revisão

- Reescrevemos o README raiz com identificação coletiva, descrição, explicação dos dados, justificativas, resultados e comandos por fase. A documentação detalhada complementa o README principal, sem esconder nele os requisitos essenciais.
- Utilizamos “desenvolvemos”, “implementamos” e “validamos” nos registros do grupo. Nas instruções, utilizamos “Como reproduzir”, “executar”, “abrir” e “conferir”. Preservamos transcrições de logs, exemplos de dados e cópias históricas sem reescrever seus conteúdos.
- Explicamos como clonar, em qual diretório executar, quais versões utilizar, como instalar dependências, qual endereço abrir, o que observar e como encerrar. Incluímos ambiente virtual e seleção explícita do Python do consumidor, evitando depender de bibliotecas locais previamente preparadas.
- Diferenciamos avaliação dos artefatos já prontos e reconstrução opcional das imagens externas da Fase 1. Mantivemos CSV, TXT, JPG, rastreabilidade e os três links públicos exigidos.
- Mantivemos NLP como atividade obrigatória da Fase 2, o portal e a MLP como desafios, o modelo tabular como extensão e as limitações dos resultados. Corrigimos o guia do portal que ainda anunciava o vídeo como futuro.
- Identificamos claramente os dois Wokwi: **Parte 1, fila e saída Serial**, e **Parte 2, MQTT e painel**. Reutilizamos o circuito, mas os firmwares têm transportes distintos. O guia principal utiliza o MQTT; o Serial permanece disponível para avaliar isoladamente a Parte 1.
- Atualizamos a matriz da Fase 3: o repositório já é público, mas faltam os artefatos dos desafios, os relatórios obrigatórios e a submissão final. Registros Markdown e capturas não substituem os relatórios paginados.

## Regras de redação e reprodução

Relatamos atividades efetivamente realizadas na primeira pessoa do plural. Não escrevemos como se um assistente estivesse prestando contas a um integrante. Descrevemos o código e os componentes de forma técnica e impessoal quando isso favorece a compreensão. Usamos o infinitivo para orientar quem reproduz a atividade.

Para cada etapa, indicamos objetivo, artefatos, pré-requisitos, comandos a partir da raiz, resultado esperado e limites. Distinguimos requisito obrigatório, exemplo do enunciado, escolha do grupo e funcionalidade ainda planejada. Só registramos execução, publicação, relatório final ou submissão depois de conferir a respectiva evidência.

Preservamos os arquivos em `document/other/historico/` como cópias das versões anteriores. Os registros de testes em Markdown recebem apenas a adequação da voz narrativa, sem alterar os fatos ou os logs que os sustentam. Não confundimos acurácia simples com acurácia balanceada; não generalizamos desempenho de bases simuladas nem classificamos zero pulsos do botão como ausência de atividade cardíaca.

## Verificação e pendências

Preparamos uma cópia isolada dos arquivos versionados, sem reutilizar `.venv`, `node_modules` ou a pasta local de dependências Python. Conferimos os comandos com Python 3.12.10 e Node.js 24.19.0. Instalamos os requisitos declarados no novo ambiente e o Node-RED pelo `npm ci` documentado.

| Verificação local | Resultado |
|---|---|
| Organização e preservação | 397 destinos, 310 conteúdos protegidos e 223 arquivos originais da Fase 1 conferidos; cópias históricas e saídas anteriores dos notebooks preservadas |
| Links e descrição | 18 URLs externos originais mantidos; 144 links locais verificados; descrição principal com 232 palavras, abaixo do limite de 600 |
| Fase 1 na cópia isolada | Reconstruímos o CSV com 303 registros e repetimos a verificação de preservação com sucesso |
| Fase 2 na cópia isolada | Executamos extração, treinamento textual e testes de NLP; o teste funcional do Streamlit confirmou navegação, portal, ECG, histórico e simulações tabular, extrativa e textual |
| Notebooks da Fase 2 | Conferimos as saídas dos quatro notebooks e reexecutamos o notebook TF-IDF pelo kernel do novo ambiente, gravando a saída separadamente |
| Fase 3 Python | 16 testes aprovados no ambiente novo: contrato, persistência, confirmações, duplicatas e migração |
| Regras Node-RED | 19 testes aprovados |
| Inicialização Node-RED na cópia isolada | Iniciamos em porta 1882 e tópico separado; conexão ao broker confirmada e dashboard com HTTP 200; encerramos a instância de teste |

Não regravamos os PDFs anteriores, os dados originais, os notebooks entregues nem o firmware. Os ensaios automatizados complementam as evidências anteriores do ESP32 simulado; não os apresentamos como nova execução manual de todos os cenários do Wokwi. A integração contínua registra as verificações do PR correspondente.

Antes do envio, ainda precisamos concluir os relatórios, os desafios e o vídeo da Fase 3, conferir o cadastro do grupo e testar acesso público aos links em sessão sem autenticação. Preservar um endereço não comprova que suas permissões continuam corretas. O envio final deve ser feito e conferido na plataforma FIAP; publicar ou fazer merge no GitHub não equivale a submetê-lo.
