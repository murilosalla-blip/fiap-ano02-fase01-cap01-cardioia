# CardioIA Fase 3

Monitoramento contínuo simulado com ESP32, resiliência offline, MQTT e Node-RED, incluindo os desafios REST/e-mail e séries temporais/neuromorfismo.

Organizei o trabalho em seis entregas para revisão em [ROTEIRO_ENTREGA.md](ROTEIRO_ENTREGA.md). A situação detalhada está em [CHECKLIST_ENUNCIADO.md](CHECKLIST_ENUNCIADO.md).

## Estado atual

Compilei a primeira implementação para ESP32 e executei no Wokwi o circuito e o firmware com sensores e fila limitada. Executei os testes do núcleo C++ e do contrato com sucesso. Conferi no simulador a coleta offline, a recuperação Serial, seis pulsos e a mudança de temperatura. Registrei as evidências em `evidencias/`.

**Projeto público:** [CardioIA Edge no Wokwi](https://wokwi.com/projects/478054573982428161).

Concluí a primeira entrega, incluindo testes ampliados de fila cheia, botão segurado e reinício e restauração da capacidade de 2.000 leituras. Registrei os resultados em [Validação dos cenários ampliados](evidencias/2026-10-24/RESULTADOS.md).

Na segunda entrega, implementei a [integração MQTT](mqtt/README.md), compilei a nova variante ESP32 e testei persistência, confirmação e deduplicação do consumidor pelo broker real com um publicador Python identificado. Publiquei o [projeto MQTT no Wokwi](https://wokwi.com/projects/478772789361460225). Confirmei a troca ESP32 → broker → consumidor → ACK, o reenvio após uma confirmação omitida e a recuperação da fila após reiniciar o consumidor. Também observei falhas intermitentes no gateway do Wokwi; consegui retomar a comunicação ao reiniciar a simulação. Registrei os testes concluídos e as pendências em [Resultados MQTT](evidencias/2026-10-24/mqtt/RESULTADOS.md).

Na terceira entrega, implementei o [painel Node-RED](node-red/README.md), com gráfico, gauge e alertas didáticos. Conferi inicialmente 15 testes de regras e, após a revisão de estabilidade, 19 testes. Também executei 12 cenários de rede e conferi leituras reais do ESP32 com suas confirmações. Preservei os [resultados do painel](evidencias/2026-10-24/dashboard/RESULTADOS.md) e concluí a revisão visual guiada, com capturas dos alertas e conferência de 27 medições únicas.

## Arquivos

- `contratos/`: formato e exemplo de mensagem.
- `firmware/cardioia_edge/`: sketch ESP32, biblioteca declarada, circuito e núcleo da fila.
- `firmware/cardioia_mqtt/`: variante MQTT com confirmação e tarefa de rede separada.
- `python/`: consumidor MQTT e persistência SQLite.
- `mqtt/`: protocolo, configuração e reprodução da integração.
- `node-red/`: fluxo importável, dashboard, regras e inicialização local.
- `tests/`: cenários automatizados da fila e do contrato.
- `validacao/`: instruções para revisar cada entrega.
- `evidencias/`: registros verificáveis de execução.

Uso exclusivamente educacional. Os dados e pulsos são simulados e não representam monitoramento clínico validado.

Revisei a estabilidade do MQTT no Wokwi, separei conexão e atualidade dos dados e conferi 19 testes locais. Observei aproximadamente 101 segundos sem interrupção e testei a chave offline/online; registrei a revisão em [Correção de estabilidade](evidencias/2026-10-24/dashboard/estabilidade/RESULTADOS.md).
