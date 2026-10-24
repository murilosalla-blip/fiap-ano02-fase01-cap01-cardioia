# Minha validação da organização

Conferi a estrutura e a execução em 24/10/2026, na branch `codex/organizar-estrutura-fiap`, partindo do commit `643d8abf3c7c6929087364065f2f8c547a184066`.

## Preservação e organização

- Localizei os destinos dos 397 arquivos que já estavam versionados.
- Conferi 310 conteúdos protegidos da reorganização, incluindo firmware, datasets, imagens e registros. Preservei binários byte a byte; normalizei somente CRLF/LF na comparação dos textos e conferi o fluxo JSON por conteúdo estruturado.
- Conferi os 223 arquivos do manifesto anterior da Fase 1, usando os destinos atuais ou as cópias originais arquivadas. Preservei o manifesto e seus hashes anteriores.
- Validei 89 links locais e mantive as saídas originais dos quatro notebooks.
- Separei as aulas em 11 PDFs da Fase 1, 12 da Fase 2 e 11 da Fase 3, com enunciados separados por fase.
- Conferi a descrição do README com 207 palavras, abaixo do limite de 600 palavras do modelo.

## Execução que conferi

| Componente | Resultado que obtive |
|---|---|
| Fase 2 — NLP | Passei pelos testes de extração, classificação textual e viés; conferi os cenários sintéticos tabulares |
| Fase 2 — Streamlit | Passei pelo teste funcional completo no código atual e na entrada anterior `fase2/app.py` |
| Fase 2 — tabular | Reexecutei o treinamento, as análises com 2.000 reamostragens e os testes por faixa etária |
| Fase 2 — notebooks | Executei `analise_baseline.ipynb` e `classificacao_textual_tfidf.ipynb`, gravando novas cópias apenas na pasta local de resultados |
| Portal React | Passei nos sete testes e gerei o build de produção no novo caminho |
| Fase 3 — Python | Passei nos 14 testes de contrato, persistência, confirmação e integridade |
| Fase 3 — C++ | Recompilei e passei nos dois executáveis de testes do núcleo e da política de ACK |
| Fase 3 — painel | Passei nos 19 testes de regras; regenerei um fluxo estruturalmente idêntico ao anterior |
| Fase 3 — integração do painel | Iniciei o serviço pela entrada de compatibilidade na porta 1882 e passei nos 12 cenários pelo broker em tópico exclusivo de ensaio |
| Fase 3 — consumidor MQTT | Confirmei duas medições únicas, duas duplicatas, uma confirmação omitida e um conflito rejeitado em banco e tópico exclusivos de ensaio |
| Evidências anteriores | Reexecutei os validadores Edge e MQTT contra os registros existentes, com aprovação |
| Configuração | Conferi a sintaxe YAML dos três workflows e atualizei caminhos, cache, entradas de PR e verificação da entrada publicada |

Preparei as dependências auxiliares em `.tools/`, sem substituir os pacotes globais. Mantive o banco principal e seus eventos em `fase3/runtime/` e não interrompi o consumidor já aberto no caminho anterior.

## Limites desta conferência

Compilei todas as células dos quatro notebooks e conferi os caminhos dos experimentos visuais. Não reexecutei o treinamento TensorFlow nem os dois notebooks visuais nesta máquina, pois o ambiente visual e os derivados brutos ampliados não estavam preparados. Preservei os resultados visuais existentes e mantive o workflow específico para reprodução completa dessa modalidade.

Não publiquei uma nova versão do Streamlit, do portal ou dos projetos Wokwi para validar esta mudança de pastas. Preservei os endereços e a entrada do Streamlit Cloud; testei localmente a entrada anterior e o código atual. A publicação independente do portal permanece no seu próprio repositório.

Os desafios REST/e-mail, neuromorfismo e fechamento da Fase 3 continuam pendentes no roteiro; esta reorganização não altera a situação dessas entregas.

## Preservação dos links externos

Conferi os endereços do README anterior à reorganização. Preservei o vídeo da Fase 2 e restaurei no README os três links do Drive da Fase 1, além da referência ao repositório e do endereço de clonagem. Mantive os links do Drive também no guia da Fase 1. Registrei todos os endereços anteriores em `links_externos_preservados.json` e incluí sua conferência no validador de organização. Não alterei as permissões nem confirmei a disponibilidade dos serviços externos nesta revisão.
