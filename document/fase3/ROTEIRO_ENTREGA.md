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

- [ ] Vamos implementar serviço demonstrativo e cliente Python com envio e recebimento REST.
- [ ] Vamos reutilizar a telemetria da entrega principal.
- [ ] Vamos aplicar regras didáticas de risco com motivo explícito.
- [ ] Vamos simular e-mail em arquivo `.eml` ou caixa de saída local, sem enviar mensagens reais.
- [ ] Vamos evitar e-mails repetidos para o mesmo episódio e tratar falhas HTTP.
- [ ] Vamos testar o fluxo HTTP completo e inspecionar e-mail gerado.
- [ ] Vamos produzir relatório final de uma a duas páginas.
- [ ] Vamos validar o cliente, o alerta e o e-mail simulado.

Aceite: requisições de envio e consulta funcionam; cenário com alerta produz e-mail simulado verificável; cenário normal não produz e-mail de alerta.

## Entrega 5 — Ir Além 2 séries temporais e neuromorfismo

- [ ] Vamos definir objetivo, rótulo, gerador/fonte e limites das séries de sinais simulados.
- [ ] Vamos separar sessões independentes antes de criar janelas; impedir sobreposição entre treino e teste.
- [ ] Vamos treinar classificador tradicional, como regressão logística.
- [ ] Vamos implementar modelo neuromórfico LIF ou FHN com saída de classificação claramente definida.
- [ ] Vamos comparar ambos na mesma tarefa e divisão, com métricas, matriz de confusão e análise de erros.
- [ ] Vamos explicar limitações, sementes e parâmetros; não inferir consumo energético de chip a partir de Python.
- [ ] Vamos entregar notebook comentado e executado, resultados e instruções.
- [ ] Vamos produzir relatório comparativo de duas páginas.
- [ ] Vamos preparar roteiro, gravar vídeo de até quatro minutos e publicar como não listado no YouTube.
- [ ] Vamos validar a comparação, o relatório e o vídeo.

Aceite: os dois modelos fazem previsões comparáveis em teste separado; execução é reproduzível; relatório interpreta os resultados sem promessas clínicas.

## Entrega 6 — Fechamento e submissão

- [x] Produzimos o [relatório Edge de duas páginas](CardioIA_Fase3_Relatorio_Edge.pdf) e conferimos sua paginação e renderização.
- [x] Produzimos o [relatório MQTT/dashboard de três páginas](CardioIA_Fase3_Relatorio_MQTT_Dashboard.pdf) e conferimos sua paginação e renderização.
- [ ] Vamos concluir a revisão final do grupo dos dois relatórios obrigatórios.
- [ ] Vamos conferir os relatórios dos dois desafios e sua paginação final.
- [ ] Vamos consolidar README com instalação, arquitetura, limites, integrantes/RMs e links públicos.
- [ ] Vamos consolidar checklist requisito → arquivo → evidência → resultado.
- [ ] Vamos fazer reprodução limpa e revisão cruzada dos cenários críticos.
- [ ] Vamos verificar link Wokwi, vídeo não listado e acesso público ao repositório.
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
