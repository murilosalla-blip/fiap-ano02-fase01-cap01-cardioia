# Nossa validação da organização

Conferimos a estrutura e a execução em 24/10/2026, na branch `codex/organizar-estrutura-fiap`, partindo do commit `643d8abf3c7c6929087364065f2f8c547a184066`.

## Preservação e organização

- Localizamos os destinos dos 397 arquivos que já estavam versionados.
- Conferimos 310 conteúdos protegidos da reorganização, incluindo firmware, datasets, imagens e registros. Preservamos binários byte a byte; normalizamos somente CRLF/LF na comparação dos textos e conferimos o fluxo JSON por conteúdo estruturado.
- Conferimos os 223 arquivos do manifesto anterior da Fase 1, usando os destinos atuais ou as cópias originais arquivadas. Preservamos o manifesto e seus hashes anteriores.
- Validamos 89 links locais e mantivemos as saídas originais dos quatro notebooks.
- Separamos as aulas em 11 PDFs da Fase 1, 12 da Fase 2 e 11 da Fase 3, com enunciados separados por fase.
- Conferimos a descrição do README com 207 palavras, abaixo do limite de 600 palavras do modelo.

## Execução que conferimos

| Componente | Resultado que obtivemos |
|---|---|
| Fase 2 — NLP | Passamos pelos testes de extração, classificação textual e viés; conferimos os cenários sintéticos tabulares |
| Fase 2 — Streamlit | Passamos pelo teste funcional completo no código atual e na entrada anterior `fase2/app.py` |
| Fase 2 — tabular | Reexecutamos o treinamento, as análises com 2.000 reamostragens e os testes por faixa etária |
| Fase 2 — notebooks | Executamos `analise_baseline.ipynb` e `classificacao_textual_tfidf.ipynb`, gravando novas cópias apenas na pasta local de resultados |
| Portal React | Passamos nos sete testes e geramos o build de produção no novo caminho |
| Fase 3 — Python | Passamos nos 14 testes de contrato, persistência, confirmação e integridade |
| Fase 3 — C++ | Recompilamos e passamos nos dois executáveis de testes do núcleo e da política de ACK |
| Fase 3 — painel | Passamos nos 19 testes de regras; regeneramos um fluxo estruturalmente idêntico ao anterior |
| Fase 3 — integração do painel | Iniciamos o serviço pela entrada de compatibilidade na porta 1882 e passamos nos 12 cenários pelo broker em tópico exclusivo de ensaio |
| Fase 3 — consumidor MQTT | Confirmamos duas medições únicas, duas duplicatas, uma confirmação omitida e um conflito rejeitado em banco e tópico exclusivos de ensaio |
| Evidências anteriores | Reexecutamos os validadores Edge e MQTT contra os registros existentes, com aprovação |
| Configuração | Conferimos a sintaxe YAML dos três workflows e atualizamos caminhos, cache, entradas de PR e verificação da entrada publicada |

Preparamos as dependências auxiliares em `.tools/`, sem substituir os pacotes globais. Mantivemos o banco principal e seus eventos em `fase3/runtime/` e não interrompemos o consumidor já aberto no caminho anterior.

## Limites desta conferência

Compilamos todas as células dos quatro notebooks e conferimos os caminhos dos experimentos visuais. Não reexecutamos o treinamento TensorFlow nem os dois notebooks visuais nesta máquina, pois o ambiente visual e os derivados brutos ampliados não estavam preparados. Preservamos os resultados visuais existentes e mantivemos o workflow específico para reprodução completa dessa modalidade.

Não publicamos uma nova versão do Streamlit, do portal ou dos projetos Wokwi para validar esta mudança de pastas. Preservamos os endereços e a entrada do Streamlit Cloud; testamos localmente a entrada anterior e o código atual. A publicação independente do portal permanece no seu próprio repositório.

Os desafios REST/e-mail, neuromorfismo e fechamento da Fase 3 continuam pendentes no roteiro; esta reorganização não altera a situação dessas entregas.

## Preservação dos links externos

Na revisão para integração do PR #3, corrigimos também a raiz usada pelo teste visual ampliado para abrir os derivados: passamos a resolver os caminhos a partir da raiz do repositório, mantendo a arquitetura, os dados esperados e as verificações existentes.

Na execução do GitHub Actions, identificamos que a versão de Streamlit instalada no runner interpreta o caminho relativo do AppTest a partir do arquivo de teste. Passamos a fornecer o caminho absoluto da entrada selecionada, preservando a mesma execução no Windows e no Linux.

Conferimos os endereços do README anterior à reorganização. Preservamos o vídeo da Fase 2 e restauramos no README os três links do Drive da Fase 1, além da referência ao repositório e do endereço de clonagem. Mantivemos os links do Drive também no guia da Fase 1. Registramos todos os endereços anteriores em `links_externos_preservados.json` e incluímos sua conferência no validador de organização. Não alteramos as permissões nem confirmamos a disponibilidade dos serviços externos nesta revisão.
