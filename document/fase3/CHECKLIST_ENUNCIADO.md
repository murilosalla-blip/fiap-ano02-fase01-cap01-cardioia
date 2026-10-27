# Fase 3 — requisitos, evidências e pendências

Acompanhamos separadamente implementação, teste, documentação e submissão. Reavaliamos este checklist em **26/10/2026**, com os textos fornecidos, o enunciado Word arquivado e suas duas imagens. O prazo informado é **04/11/2026, às 23h59**. Os documentos e as evidências de testes abaixo não representam submissão concluída.

## Critérios da atividade obrigatória — 10 pontos

| Critério do enunciado | Pontos | Como avaliar e localizar | Situação |
|---|---:|---|---|
| Leitura de sensores | 2 | ESP32 com DHT22 (um sensor) e botão de pulsos (segunda entrada simulada); código comentado em `src/fase3/firmware/`; projetos públicos identificados no [guia](README.md) | Implementamos e validamos no Wokwi |
| Resiliência offline | 2 | Chave booleana, coleta offline, fila FIFO de 2.000 amostras, sincronização e perdas contabilizadas; [resultados Edge](../other/fase3/evidencias/2026-10-24/RESULTADOS.md) | Validamos recuperação, limite, botão segurado e reinício; documentamos volatilidade da RAM |
| MQTT e broker | 2 | Firmware `cardioia_mqtt`, broker real, consumidor SQLite e ACK; [resultados MQTT](../other/fase3/evidencias/2026-10-24/mqtt/RESULTADOS.md) | Validamos transmissão, persistência, reenvio e recuperação |
| Dashboard e alertas | 2 | [Export Node-RED](../../src/fase3/node-red/flows.json), gráfico de BPM, gauge ambiental e alertas; [capturas](../../assets/fase3/evidencias/) e [validação guiada](../other/fase3/evidencias/2026-10-24/dashboard/validacao_guiada/RESULTADOS.md) | Validamos gráfico, temperatura, entrada e retorno dos alertas e estabilidade |
| Documentação clara: código e relatórios | 2 | README e guias de execução, C++ comentado, relatório Edge **≥1 página** e relatório MQTT/dashboard **≥2 páginas** | Produzimos [Edge: duas páginas](CardioIA_Fase3_Relatorio_Edge.pdf) e [MQTT/dashboard: quatro páginas](CardioIA_Fase3_Relatorio_MQTT_Dashboard.pdf); conferimos paginação e conteúdo; aguardamos revisão final do grupo |

Não atribuímos nota antecipada a esta matriz. A avaliação pertence à FIAP; a implementação testada não dispensa os relatórios ou a entrega na plataforma.

## Conferência detalhada dos artefatos

| Requisito | Entrega | Evidência prevista | Estado |
|---|---:|---|---|
| ESP32 no Wokwi e dois sensores distintos, incluindo DHT22 | 1 | Sketch, diagrama e projeto público | Compilamos, conferimos no simulador e concluímos a revisão da primeira entrega |
| Coleta periódica e conectividade booleana | 1 | Firmware e demonstração Serial | Conferimos no Wokwi e salvamos registros em `document/other/fase3/evidencias/` |
| Resiliência offline e armazenamento limitado | 1–2 | Fila, testes e cenário de recuperação | Testamos o núcleo C++ e conferimos no Wokwi recuperação Serial, fila cheia, botão segurado e reinício; também implementamos MQTT, confirmamos reenvio e recuperação após reiniciar o consumidor |
| C++ comentado e link Wokwi | 1 | `src/fase3/firmware/cardioia_edge/` e https://wokwi.com/projects/478054573982428161 | Comentamos o código, publicamos o link e reorganizamos o circuito durante nossa revisão |
| Relatório Edge mínimo uma página | 6 | [Relatório Edge](CardioIA_Fase3_Relatorio_Edge.pdf) | Produzimos duas páginas e conferimos a renderização; revisão final do grupo pendente |
| Transmissão MQTT e broker | 2 | Firmware compilado, consumidor, eventos de rede e projeto https://wokwi.com/projects/478772789361460225 | Confirmamos a troca real do ESP32 pelo broker, a confirmação após persistência e a recuperação após reiniciar o consumidor; também conferimos falha controlada do endpoint, recuperação ordenada e retorno à fila vazia |
| Dashboard Node-RED com gráfico, gauge e alerta | 3 | `src/fase3/node-red/flows.json` e `document/other/fase3/evidencias/2026-10-24/dashboard/` | Implementamos e testamos regras, rede e recebimento do ESP32; concluímos a revisão visual guiada com entrada e retorno dos dois alertas |
| Relatório MQTT/dashboard mínimo duas páginas | 6 | [Relatório MQTT/dashboard](CardioIA_Fase3_Relatorio_MQTT_Dashboard.pdf) | Produzimos quatro páginas e conferimos a renderização; revisão final do grupo pendente |
| Ir Além 1 cliente REST envia e recebe | 4 | [Guia e evidência REST](rest/README.md) | Implementamos, testamos e concluímos a validação guiada com consulta após reinício |
| Ir Além 1 regras de risco e e-mail simulado | 4 | Código, sete testes e demonstração de dois e-mails locais | Conferimos os dois e-mails na validação guiada |
| Ir Além 1 relatório de uma a duas páginas | 4 | [Relatório de duas páginas](CardioIA_Fase3_Relatorio_REST_Email.pdf) | Produzimos e conferimos a renderização; revisão final do grupo pendente |
| Ir Além 2 classificador tradicional e LIF/FHN | 5 | Notebook executado e resultados | Ainda precisamos concluir |
| Ir Além 2 repositório público, código e README | 5–6 | Código da comparação, notebook e reprodução | O repositório já é público; ainda precisamos implementar e publicar os artefatos específicos do desafio |
| Ir Além 2 relatório comparativo de duas páginas | 5 | Relatório paginado (PDF planejado) | Ainda precisamos concluir |
| Ir Além 2 vídeo até quatro minutos não listado | 5 | YouTube e link README | Ainda precisamos concluir |
| Clareza, organização e revisão de evidências | Todas | Roteiro e pacote final | Estamos acompanhando as evidências |

SPIFFS e hardware físico não são obrigatórios segundo o enunciado fornecido; Grafana é opcional. A implementação Serial da primeira entrega não satisfaz, sozinha, a Parte 2 de MQTT.

## Exigências, exemplos e escolhas do grupo

- **Obrigatórios:** dois sensores/entradas distintos, incluindo DHT22; coleta periódica e conectividade booleana; armazenamento limitado na ordem de milhares de amostras, com estratégia explícita; sincronização; código comentado e link Wokwi; MQTT com broker; Node-RED com gráfico, gauge e alerta; relatórios com os mínimos de páginas.
- **Opcionais:** SPIFFS no simulador, hardware físico, microSD e Grafana. Não apresentamos SPIFFS como realizado.
- **Escolhas da implementação:** cinco segundos simulados por coleta, 2.000 posições, descarte da amostra nova quando a fila enche, reenvio em três segundos, dado atual por 15 segundos reais, histerese e confirmação em duas janelas. Sete segundos no teste de botão segurado foi uma duração de ensaio, não um critério da FIAP.
- **Limites de alerta:** >120 BPM para pulsos artificiais e >30 °C para temperatura ambiente. O >38 °C citado no enunciado é exemplo, não obrigação de medir temperatura corporal. Zero pulsos indica ausência de acionamentos, não ausência de atividade cardíaca.
- **Ir Além 1:** o cliente Python precisa **enviar e receber** por REST, verificar risco e simular e-mail. O endpoint de consulta do painel não satisfaz sozinho esse requisito. O relatório deve ter **uma a duas páginas**.
- **Ir Além 2:** classificador tradicional comparado a LIF ou FHN em séries temporais, notebook comentado, código e README públicos, relatório de **duas páginas** e vídeo de **até quatro minutos**, não listado no YouTube, com link no README raiz. Ainda não temos esse vídeo; o link da Fase 2 não o substitui.

Mantemos os dois desafios no escopo por decisão do grupo, seguindo a Fase 2. Eles não constam na distribuição dos dez pontos acima; não afirmamos bonificação nem obrigação geral não expressa no enunciado.

## Aceite antes da submissão

- [x] Produzimos os dois relatórios obrigatórios e conferimos as duas páginas do Edge e as quatro de MQTT/dashboard.
- [ ] Concluir a revisão final do grupo dos dois relatórios obrigatórios.
- [x] Produzimos o relatório REST/e-mail de duas páginas e conferimos sua paginação.
- [ ] Produzir o relatório comparativo do Ir Além 2 e conferir suas duas páginas.
- [x] Executamos o cliente REST e a simulação de e-mail, com consulta após reinício e evidências preservadas.
- [ ] Executar os dois modelos comparáveis e preservar suas evidências.
- [ ] Publicar o vídeo específico do Ir Além 2 e inserir o link no README raiz.
- [x] Reproduzimos instalação e serviços em cópia nova, conferimos REST após reinício e concluímos a repetição visual acompanhada no Wokwi: sensores, entrada/retorno dos alertas e recuperação pela chave. Preservamos 41 medições únicas sem lacunas ou perdas na [validação guiada de 27/10](../other/fase3/evidencias/2026-10-27/reproducao/validacao_guiada/RESULTADOS.md). A operação acompanhada está identificada separadamente do ensaio de rede Python.
- [ ] Conferir acesso sem autenticação obrigatória aos links públicos, dados e vídeo; preservar também os links das fases anteriores.
- [ ] Conferir integrantes/RMs no pacote e cadastro do grupo na plataforma antes do envio. O recorte fornecido da Fase 3 lista apenas um participante; precisamos conferir o cadastro efetivo, sem alterar a identificação coletiva do projeto com base nesse recorte.
- [ ] Conferir o arquivo correto, enviar pela plataforma com antecedência e reabrir/baixar o arquivo enviado para confirmar o conteúdo. A imagem de orientação avisa que não é possível substituir o arquivo após o fechamento da entrega ou a correção.
- [ ] Registrar o envio efetivamente confirmado, sem confundir merge no GitHub com submissão na FIAP.

## Resultado da auditoria de 26/10/2026

Relemos o enunciado Word e suas duas imagens, comparamos a estrutura com o modelo oficial FIAP e conferimos a `main` publicada no commit `6fd6aba`. Confirmamos repositório público e aprovação dos quatro workflows nesse commit, incluindo os treinamentos e notebooks da Fase 2. Conferimos os 372 destinos atuais do mapa de organização, 286 conteúdos protegidos, 157 links locais e os seis testes de proteção. Mantemos os 223 itens do inventário anterior: 212 arquivos locais e 11 aulas identificadas pelo hash original no histórico. As 63 retiradas de apoio continuam individualizadas no registro de higienização; mantemos os documentos submetidos, os enunciados, os dados e as evidências funcionais.

Conferimos no código os parâmetros documentados de sensores, fila, MQTT e alertas. Corrigimos trechos remanescentes no singular, uma forma verbal incorreta e a referência a aulas já retiradas. Ampliamos o guia de testes para reunir as verificações Python, Node-RED, os dois núcleos C++, os registros Edge/MQTT e a compilação das duas variantes ESP32. Esses ajustes são documentais; não alteramos os programas ou as evidências.

**Conclusão:** a organização e a implementação obrigatória estão acompanhadas por evidências, mas a entrega acadêmica ainda está incompleta. Após a auditoria, produzimos os dois relatórios obrigatórios e conferimos seu conteúdo, renderização e paginação. Ainda precisamos concluir a revisão final do grupo, os dois desafios e seus relatórios, publicar o vídeo específico e fechar a reprodução e a submissão. Não atribuímos nota antecipada nem marcamos essas pendências como concluídas.

Os dois links Wokwi continuam identificados por finalidade. Nesta auditoria, as consultas automatizadas receberam HTTP 403; esse bloqueio não comprova que os projetos estejam privados ou inválidos. Mantemos pendente a conferência manual em sessão sem autenticação dos projetos, das pastas do Drive, das publicações e dos vídeos. Conferir os acessos novamente no fechamento do pacote final.

## Regras da plataforma para o fechamento

- [ ] Entregar até **04/11/2026 às 23h59**; o enunciado limita a até 70% a nota das atividades entregues nos três dias seguintes ao prazo.
- [ ] Conferir integrantes e RMs no cadastro efetivo: o recorte arquivado lista somente Murilo, enquanto o repositório identifica três integrantes. O recorte não confirma o cadastro atual.
- [ ] Conferir o arquivo enviado e seu conteúdo pela plataforma. A orientação informa que não é possível substituí-lo após o fechamento da entrega ou a correção do professor.
- [ ] Respeitar a orientação de não compartilhar respostas em grupos de WhatsApp, Discord ou Microsoft Teams.

Após a publicação da nota, eventual pedido de revisão deve observar o prazo máximo de 15 dias indicado na orientação arquivada. O merge no GitHub não representa envio à plataforma.

Adotamos PDF como formato planejado para os relatórios; o enunciado fornecido exige paginação, mas não especifica extensão ou tamanho máximo do upload. Conferir os formatos aceitos e os limites efetivos da plataforma antes de montar o pacote final.
