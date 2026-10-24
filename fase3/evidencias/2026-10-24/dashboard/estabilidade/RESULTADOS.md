# Minha correção de estabilidade MQTT

Em 24/10/2026, corrigi a diferença entre o relógio do simulador e os prazos reais do broker. Configurei keepalive MQTT de 300 segundos e espera de resposta de cinco segundos. Compilei para ESP32: 744.889 bytes de flash e 45.456 bytes de variáveis globais. Preservei a fila de 2.000 leituras e suas regras de confirmação.

Salvei a correção no mesmo projeto público: https://wokwi.com/projects/478772789361460225. Na nova sessão `546cb527f2cc13d5`, conferi no Serial `keepalive_s=300 socket_timeout_s=5`. Preservei o registro em `wokwi_corrigido.txt`.

## Minha observação da conexão real

Executei `scripts/conferir_estabilidade_mqtt.py` por aproximadamente 101 segundos. Registrei conexão online em todas as amostras, sem interrupções. Observei as sequências 1 e 2, com confirmações correspondentes. Os recebimentos ficaram separados por aproximadamente 104 segundos reais, enquanto a coleta avançou cinco segundos no relógio do dispositivo. Não observei reconexão nesse intervalo; o trecho Serial preservado contém uma única conexão MQTT antes do teste explícito da chave.

Conferi a distinção entre `connection=online` e a atualidade `live` ou `stale`: a espera por nova leitura não foi interpretada como interrupção da conexão. Mantive os últimos valores identificados como desatualizados e suspendi sua avaliação como alerta atual. Preservei as amostras em `observacao.json` e o resultado em `resultado.json`.

## Minha conferência da interrupção real

Desliguei a chave do circuito e confirmei `connection=device_offline`, `mode=offline` e ausência de valor atual. Reconectei a chave e confirmei o retorno a `connection=online`, mantendo a indicação de espera até nova leitura. Preservei `desconexao_explicita.json` e `reconexao_explicita.json`.

## Minhas regras e limites

Executei os 19 testes locais com aprovação, incluindo duas janelas consecutivas com simulação lenta, lacuna de sequência, separação entre conexão e atualidade e reinício da confirmação após desconexão explícita. Compilei também o componente Vue sem erros.

Mantive o prazo de 15 segundos reais para considerar dados atuais. Não prometo coleta a cada cinco segundos reais quando o navegador reduz a velocidade da simulação. Um keepalive maior pode atrasar o Last Will em uma falha silenciosa; a indicação de falta de atualização continua independente desse prazo. Vou concluir a validação visual guiada e os cenários de alerta antes de encerrar a terceira entrega.
