# Roteiro de entrega completa da Fase 3

Incluímos no escopo a entrega obrigatória e os dois desafios Ir Além. Vamos revisar as evidências de cada etapa e concluir os ajustes antes de avançar. Vamos distinguir implementação local, validação no Wokwi, publicação e entrega acadêmica.

Fonte: `document/other/referencias/fase3/enunciado/Fase 3_Cap 1_Exercício.docx`. Prazo registrado: 04/11/2026 às 23h59.

## Entrega 1 — Fundamentos e protótipo Edge

- [x] Criamos roteiro com todo o escopo e critérios de aceite.
- [x] Definimos formato único de telemetria e exemplo validável.
- [x] Implementamos C++ para DHT22, botão de pulsos e chave online/offline.
- [x] Implementamos fila limitada, identificação das leituras e contagem de perdas.
- [x] Compilamos e testamos automaticamente o núcleo C++ da fila.
- [x] Compilamos o firmware para ESP32 e executamos no Wokwi.
- [x] Conferimos no simulador temperatura, pulsos, coleta offline e recuperação Serial.
- [x] Completamos os cenários ampliados no simulador em 24/10/2026: fila cheia, botão segurado por sete segundos e reinício com pendências. Registramos e conferimos as evidências em `evidencias/2026-10-24/RESULTADOS.md`.
- [x] Salvamos o projeto no Wokwi e registramos o link público: https://wokwi.com/projects/478054573982428161.
- [x] Concluímos a revisão da primeira entrega e avançamos para a integração MQTT.

Aceite: dois sensores distintos funcionam; a coleta continua offline; reconexão esvazia pendências na ordem; perdas são visíveis; reinício é identificado como nova sessão. A confirmação nesta etapa é apenas saída Serial local, expressamente identificada como demonstração, sem alegar nuvem.

## Entrega 2 — MQTT e integridade ponta a ponta

- [x] Definimos o HiveMQ público e configuramos a conexão no firmware e no consumidor. Confirmamos o acesso pelo computador.
- [x] Implementamos envio MQTT, reconexão com tentativas espaçadas e injeção de falha de acesso ao endpoint; compilamos a variante ESP32.
- [x] Implementamos confirmação após persistência no consumidor e retirada da cabeça somente após ACK correspondente; conferimos os testes locais.
- [x] Definimos tópicos de telemetria, confirmação e estado e separamos dispositivo e sessão.
- [x] Implementamos reenvio e deduplicação persistente e testamos o consumidor pelo broker real com publicador Python identificado.
- [x] Registramos coleta, preparação da tentativa e recebimento separadamente e incluímos indicação de replay.
- [x] Confirmamos a troca ESP32 → broker → consumidor → ACK no Wokwi. Omitimos o primeiro ACK, conferimos reenvio em três segundos e uma única medição persistida. Registramos os resultados em `evidencias/2026-10-24/mqtt/RESULTADOS.md`.
- [x] Demonstramos desconexão pela chave, falha controlada de acesso ao endpoint, reconexão, recuperação ordenada e reenvio sem duplicar medições. Conferimos as evidências com `scripts/fase3/validar_cenarios_mqtt.py`.
- [x] Concluímos a validação funcional da segunda entrega no Chrome em 24/10/2026; conferimos 75 medições únicas e a deduplicação no banco. Registramos a revisão em `evidencias/2026-10-24/mqtt/validacao_guiada/RESULTADOS.md`.

Aceite: leituras chegam ao consumidor via MQTT real; falha de publicação ou ausência de confirmação preserva a pendência; mensagens repetidas não duplicam o histórico. Garantias e limites de persistência devem estar documentados.

## Entrega 3 — Dashboard Node-RED

- [x] Preparamos o fluxo importável, as regras, o template e as dependências para versionamento em `node-red/`.
- [x] Implementamos gráfico de batimentos por sequência e gauge da temperatura ambiente, com indicação de indisponibilidade.
- [x] Implementamos alertas didáticos, estado da conexão, idade informada no envio, tempo sem recebimento e perdas.
- [x] Validamos formato, identidade e coerência e mantivemos valores ausentes como indisponíveis.
- [x] Incluímos leituras recuperadas no histórico e suspendemos sua avaliação como alerta atual.
- [x] Demonstramos entrada, permanência e saída em ensaio pelo broker; conferimos histerese e duas leituras consecutivas.
- [x] Salvamos o export e a captura do ensaio controlado; preservamos estados e confirmações do ESP32 em `evidencias/2026-10-24/dashboard/`.
- [x] Concluímos a validação visual e funcional no Chrome: gráfico, gauge e entrada/retorno dos alertas de pulsos e temperatura. Conferimos 27 medições únicas e preservamos as capturas em `evidencias/2026-10-24/dashboard/validacao_guiada/`.

Aceite: dashboard acompanha o ESP32 em tempo real, mostra histórico e alertas automaticamente e diferencia falta de dados de normalidade. Grafana fica opcional; React pode oferecer acesso ao módulo, sem substituir Node-RED.

## Entrega 4 — Ir Além 1 REST e e-mail

- [x] Implementamos serviço demonstrativo e cliente Python com envio e recebimento REST.
- [x] Reutilizamos o contrato de telemetria da entrega principal, sem alterar o firmware.
- [x] Aplicamos regras didáticas de risco com motivo explícito.
- [x] Simulamos e-mail em arquivo `.eml` e caixa de saída persistente, sem enviar mensagens reais.
- [x] Evitamos e-mails repetidos para o mesmo episódio e tratamos falhas HTTP.
- [x] Testamos o fluxo HTTP completo e inspecionamos o conteúdo do e-mail gerado; conferimos sete testes e a demonstração sintética de cinco leituras.
- [x] Produzimos o [relatório REST/e-mail de duas páginas](CardioIA_Fase3_Relatorio_REST_Email.pdf) e conferimos a renderização; revisão técnica concluída em 28/10/2026.
- [x] Validamos o cliente, os alertas, os dois e-mails simulados e a consulta após reiniciar o serviço.

Reprodução e validação guiada: [REST e e-mail simulado](rest/README.md). Concluímos a validação guiada e produzimos o relatório; concluímos sua revisão técnica em 28/10/2026.

Aceite: requisições de envio e consulta funcionam; cenário com alerta produz e-mail simulado verificável; cenário normal não produz e-mail de alerta.

## Entrega 5 — Ir Além 2 séries temporais e neuromorfismo

- [x] Definimos dois regimes de oscilação em BPM artificial, 240 sessões, semente e limites explícitos.
- [x] Separamos 144/48/48 sessões independentes antes de criar janelas; conferimos ausência de sessões compartilhadas.
- [x] Treinamos regressão logística sobre oito atributos, com seleção de C na validação.
- [x] Implementamos reservatório recorrente de 24 neurônios LIF e leitura logística treinada sobre sua atividade.
- [x] Comparamos nas mesmas 48 sessões de teste, com métricas, matrizes, erros e intervalo pareado por sessão.
- [x] Registramos limitações, semente, parâmetros e relógios distintos, sem inferir energia de chip a partir de Python.
- [x] Produzimos notebook comentado e executado, resultados e [instruções passo a passo](neuromorfismo/README.md); código e guia incluídos nesta revisão.
- [x] Produzimos [relatório comparativo de duas páginas](CardioIA_Fase3_Relatorio_Neuromorfismo.pdf) e conferimos a renderização; revisão técnica concluída em 28/10/2026.
- [ ] Preparamos o [roteiro do vídeo](neuromorfismo/ROTEIRO_VIDEO.md); ainda precisamos gravar até quatro minutos e publicar como não listado no YouTube.
- [x] Concluímos a validação guiada em 28/10/2026: instalação, comparação, três gráficos, notebook, HTML e seis testes com `OK`.
- [x] Concluímos a revisão técnica do relatório comparativo em 28/10/2026.
- [ ] Vamos conferir o vídeo após sua publicação.

Aceite: os dois modelos fazem previsões comparáveis em teste separado; execução é reproduzível; relatório interpreta os resultados sem promessas clínicas.

## Entrega 6 — Fechamento e submissão

- [x] Produzimos o [relatório Edge de duas páginas](CardioIA_Fase3_Relatorio_Edge.pdf) e conferimos sua paginação e renderização.
- [x] Produzimos o [relatório MQTT/dashboard de quatro páginas](CardioIA_Fase3_Relatorio_MQTT_Dashboard.pdf) e conferimos sua paginação e renderização.
- [x] Concluímos a revisão técnica dos dois relatórios obrigatórios em 28/10/2026.
- [x] Conferimos os dois relatórios dos desafios, com duas páginas cada.
- [x] Consolidamos README com instalação, arquitetura, limites, integrantes/RMs e links públicos; o link do vídeo da Fase 3 será acrescentado após a publicação.
- [x] Consolidamos checklist requisito → arquivo → evidência → resultado, distinguindo os itens concluídos de vídeo e submissão.
- [x] Fizemos a reprodução em cópia nova e a revisão acompanhada dos cenários visuais em 27/10/2026; conferimos sensores, entrada/retorno dos alertas, interrupção, recuperação e persistência REST. Preservamos 41 medições únicas sem lacunas ou perdas.
- [x] Conferimos os dois Wokwi, os repositórios e os materiais públicos das fases anteriores, sem autenticação.
- [ ] Vamos conferir o novo vídeo não listado após sua publicação.
- [ ] Vamos preparar documento/arquivo para submissão conforme a plataforma.
- [ ] Vamos validar o pacote final e realizar e conferir o envio na FIAP.

Aceite: cada item do enunciado tem evidência acessível. Só vamos registrar publicação, teste no simulador ou submissão após a verificação correspondente.

## Decisões iniciais e limites

- DHT22 conta como um sensor; botão representa o segundo sensor por meio de pulsos artificiais, conforme exemplo do enunciado.
- Coleta a cada cinco segundos. Fila inicial de 2.000 leituras, com política de descartar a nova leitura quando cheia e contabilizar a perda. Cobertura nominal: 10.000 segundos, cerca de 2h47min.
- Medimos o tamanho da estrutura e confirmamos o uso total de RAM na compilação ESP32. Não há persistência após reinício nesta versão.
- Identificação por dispositivo, sessão e sequência. Tempo inicial é relativo à inicialização, sem inventar horário UTC.
- Temperatura é do sensor/ambiente simulado; pulsos são artificiais; alertas são regras acadêmicas.
- As duas atividades extras fazem parte do compromisso deste roteiro, sem ficarem condicionadas à disponibilidade de tempo.
- Vamos preservar fases anteriores e alterações já existentes na pasta; não publicar credenciais.
