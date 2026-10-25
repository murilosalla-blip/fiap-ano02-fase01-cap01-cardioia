# Nossa correção de estabilidade MQTT

Em 24/10/2026, corrigimos a diferença entre o relógio do simulador e os prazos reais do broker. Configuramos keepalive MQTT de 300 segundos e espera de resposta de cinco segundos. Compilamos para ESP32: 744.889 bytes de flash e 45.456 bytes de variáveis globais. Preservamos a fila de 2.000 leituras e suas regras de confirmação.

Salvamos a correção no mesmo projeto público: https://wokwi.com/projects/478772789361460225. Na nova sessão `546cb527f2cc13d5`, conferimos no Serial `keepalive_s=300 socket_timeout_s=5`. Preservamos o registro em `wokwi_corrigido.txt`.

## Nossa observação da conexão real

Executamos `scripts/conferir_estabilidade_mqtt.py` por aproximadamente 101 segundos. Registramos conexão online em todas as amostras, sem interrupções. Observamos as sequências 1 e 2, com confirmações correspondentes. Os recebimentos ficaram separados por aproximadamente 104 segundos reais, enquanto a coleta avançou cinco segundos no relógio do dispositivo. Não observamos reconexão nesse intervalo; o trecho Serial preservado contém uma única conexão MQTT antes do teste explícito da chave.

Conferimos a distinção entre `connection=online` e a atualidade `live` ou `stale`: a espera por nova leitura não foi interpretada como interrupção da conexão. Mantivemos os últimos valores identificados como desatualizados e suspendemos sua avaliação como alerta atual. Preservamos as amostras em `observacao.json` e o resultado em `resultado.json`.

## Nossa conferência da interrupção real

Desliguamos a chave do circuito e confirmamos `connection=device_offline`, `mode=offline` e ausência de valor atual. Reconectamos a chave e confirmamos o retorno a `connection=online`, mantendo a indicação de espera até nova leitura. Preservamos `desconexao_explicita.json` e `reconexao_explicita.json`.

## Nossas regras e limites

Executamos os 19 testes locais com aprovação, incluindo duas janelas consecutivas com simulação lenta, lacuna de sequência, separação entre conexão e atualidade e reinício da confirmação após desconexão explícita. Compilamos também o componente Vue sem erros.

Mantivemos o prazo de 15 segundos reais para considerar dados atuais. Não prometo coleta a cada cinco segundos reais quando o navegador reduz a velocidade da simulação. Um keepalive maior pode atrasar o Last Will em uma falha silenciosa; a indicação de falta de atualização continua independente desse prazo. Vamos concluir a validação visual guiada e os cenários de alerta antes de encerrar a terceira entrega.
