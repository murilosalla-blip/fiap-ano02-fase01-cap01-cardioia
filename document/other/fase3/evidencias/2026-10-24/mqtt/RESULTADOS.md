# Nossa verificação da segunda entrega

Implementamos e verificamos a integração MQTT em 24/10/2026. Salvamos o [projeto MQTT no Wokwi](https://wokwi.com/projects/478772789361460225), separado da [versão Edge](https://wokwi.com/projects/478054573982428161).

## O que implementamos

Mantivemos coleta a cada cinco segundos, botão com debounce e fila de 2.000 leituras. Separamos a rede da coleta com tarefa e filas FreeRTOS. Implementamos MQTT, confirmação após persistência SQLite, reenvio após três segundos, deduplicação por dispositivo/sessão/sequência e rejeição de conflitos. Preservamos o tempo de coleta e acrescentamos tempo de preparação da tentativa, idade, contador de tentativa e indicador de replay.

## Troca real originada no ESP32

Na sessão `475b824253d928c2`, conferimos ESP32 → HiveMQ público → consumidor Python → SQLite → ACK. Omitimos apenas a primeira confirmação da sequência 1. Observamos tentativa 2 exatamente 3.000 ms após a primeira e conferimos `ack_confirmado seq=1` no ESP32. No consumidor, registramos uma medição e uma duplicata para essa identidade; mantivemos sete medições únicas nessa sessão. Preservamos o Serial em `wokwi_primeira_troca.txt` e os eventos em `eventos_consumidor.jsonl`.

Na sessão `7fbf813494bcbf14`, observamos o consumidor parado: mantivemos a sequência 1 durante 18 tentativas capturadas e continuamos acumulando leituras. Ao reiniciar o consumidor com o mesmo banco, conferimos os ACKs das sequências 1 a 20 em ordem e o retorno à fila vazia. Depois, conferimos transmissão normal das sequências 21 a 24. Preservamos `wokwi_sem_consumidor.txt` e `wokwi_apos_reiniciar_consumidor.txt`.

## Falha de endpoint e revisão da reconexão

Injetamos uma falha de acesso ao endpoint usando `broker_off`, direcionando apenas nosso cliente à porta TCP 1. Conferimos falhas MQTT e continuidade da coleta. Na primeira implementação, a restauração da porta 1883 não recuperou a conexão no intervalo observado. Preservamos `wokwi_broker_off.txt` e `wokwi_primeira_recuperacao_incompleta.txt`.

Revisamos a tarefa para encerrar o socket antes das tentativas e reiniciar o Wi-Fi após três falhas TCP consecutivas. Compilamos, publicamos e iniciamos essa revisão. Na sessão `53f75a2264ae4c7d`, confirmamos novamente armazenamento e ACK das primeiras leituras; preservamos `wokwi_mqtt_final_conectado.txt`. Depois de restaurar o endpoint, conferimos nova conexão, confirmação das sequências 3 a 46 em ordem e fila vazia, sem reiniciar o ESP32. Preservamos `wokwi_mqtt_final_broker_off.txt` e `wokwi_mqtt_final_broker_recuperado.txt`. A recuperação não foi imediata: observamos novas falhas TCP e novas tentativas antes da conexão.

Na mesma sessão, desconectamos a chave, mantivemos a coleta e acumulamos pendências. Ao reconectar, conferimos confirmação das sequências 47 a 64 e fila vazia. Preservamos `wokwi_mqtt_final_chave_offline.txt` e `wokwi_mqtt_final_chave_recuperada.txt`.

Depois desses cenários, corrigimos a unidade do tempo limite TCP para três segundos, conforme a API WiFiClient do ESP32 2.0.17. Recompilamos, salvamos a configuração final e confirmamos novas leituras e ACKs na sessão `55667c68c701d7ae`, registrada em `wokwi_mqtt_timeout_final.txt`. Esse último registro confere a comunicação após o ajuste; os ensaios completos de falha estão nos arquivos anteriores.

## Verificações locais e teste complementar de rede

Executamos os 14 testes Python com sucesso. Conferimos contrato, BPM, coerência temporal, JSON inválido, falha de gravação, confirmação após commit, duplicatas após reinício, mudança de sessão e conflitos. Compilamos e executamos o teste C++ de timeout, reenvio e rejeição de ACK incorreto, repetido ou anterior à primeira tentativa.

Compilamos a revisão para ESP32 com DHTesp 1.19.0, PubSubClient 2.8.0, ArduinoJson 6.21.5 e ESP32 2.0.17: 744.821 bytes de flash, 56%, e 45.456 bytes de variáveis globais, 13%. Além dessas variáveis, alocamos a fila fixa de 80.016 bytes no heap. Observamos 206.188 bytes livres antes de iniciar a tarefa de rede; esse valor não representa o consumo máximo durante uma conexão.

Também executamos `scripts/testar_transporte_mqtt.py` pelo HiveMQ com publicador identificado como `cardioia-publicador-python`, em namespace exclusivo. Conferimos duas medições únicas, duas duplicatas, um ACK omitido e um conflito rejeitado, além de replay. Preservamos os resultados em `teste_rede_python/`. Usamos QoS 1 nesse publicador complementar; no ESP32, usamos QoS 0 com reenvio e confirmação da aplicação.

## Gateway e limites da demonstração

Observamos falhas intermitentes de conexão a `wss://netwi.wokwi.com/` e preservamos capturas e logs. Após reiniciar a simulação, conseguimos realizar as trocas reais descritas acima. Não atribuímos essas falhas a uma indisponibilidade do HiveMQ.

Usamos apenas dados fictícios em broker público, sem autenticação ou TLS. Executamos o consumidor e a persistência no computador; o broker é o componente remoto deste ensaio. Mantivemos a fila do ESP32 em RAM: não alegamos preservação após reinício ou falta de energia, nem entrega exatamente uma vez pelo protocolo MQTT. Ao interromper simulações com pendências para atualizar o firmware, não consideramos essas pendências recuperadas na sessão seguinte.

## Continuidade

Conferimos automaticamente os cenários capturados com `scripts/fase3/validar_cenarios_mqtt.py` e registramos aprovação em `validacao_cenarios.json`. Cruzamos os ACKs do Serial com os eventos de armazenamento, conferimos as sequências em ordem, a ausência de registros duplicados e o retorno à fila vazia.

Concluímos nossa revisão funcional no Chrome e conferimos 75 medições únicas no banco. Preservamos os registros adicionais em [Nossa validação funcional](validacao_guiada/RESULTADOS.md). Nossa próxima etapa é Node-RED com gráficos, indicadores e alertas, mantendo separados dados atrasados e condição atual do dispositivo.
