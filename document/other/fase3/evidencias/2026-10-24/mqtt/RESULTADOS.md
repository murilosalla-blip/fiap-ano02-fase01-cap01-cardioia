# Minha verificação da segunda entrega

Implementei e verifiquei a integração MQTT em 24/10/2026. Salvei o [projeto MQTT no Wokwi](https://wokwi.com/projects/478772789361460225), separado da [versão Edge](https://wokwi.com/projects/478054573982428161).

## O que implementei

Mantive coleta a cada cinco segundos, botão com debounce e fila de 2.000 leituras. Separei a rede da coleta com tarefa e filas FreeRTOS. Implementei MQTT, confirmação após persistência SQLite, reenvio após três segundos, deduplicação por dispositivo/sessão/sequência e rejeição de conflitos. Preservei o tempo de coleta e acrescentei tempo de preparação da tentativa, idade, contador de tentativa e indicador de replay.

## Troca real originada no ESP32

Na sessão `475b824253d928c2`, conferi ESP32 → HiveMQ público → consumidor Python → SQLite → ACK. Omiti apenas a primeira confirmação da sequência 1. Observei tentativa 2 exatamente 3.000 ms após a primeira e conferi `ack_confirmado seq=1` no ESP32. No consumidor, registrei uma medição e uma duplicata para essa identidade; mantive sete medições únicas nessa sessão. Preservei o Serial em `wokwi_primeira_troca.txt` e os eventos em `eventos_consumidor.jsonl`.

Na sessão `7fbf813494bcbf14`, observei o consumidor parado: mantive a sequência 1 durante 18 tentativas capturadas e continuei acumulando leituras. Ao reiniciar o consumidor com o mesmo banco, conferi os ACKs das sequências 1 a 20 em ordem e o retorno à fila vazia. Depois, conferi transmissão normal das sequências 21 a 24. Preservei `wokwi_sem_consumidor.txt` e `wokwi_apos_reiniciar_consumidor.txt`.

## Falha de endpoint e revisão da reconexão

Injetei uma falha de acesso ao endpoint usando `broker_off`, direcionando apenas meu cliente à porta TCP 1. Conferi falhas MQTT e continuidade da coleta. Na primeira implementação, a restauração da porta 1883 não recuperou a conexão no intervalo observado. Preservei `wokwi_broker_off.txt` e `wokwi_primeira_recuperacao_incompleta.txt`.

Revisei a tarefa para encerrar o socket antes das tentativas e reiniciar o Wi-Fi após três falhas TCP consecutivas. Compilei, publiquei e iniciei essa revisão. Na sessão `53f75a2264ae4c7d`, confirmei novamente armazenamento e ACK das primeiras leituras; preservei `wokwi_mqtt_final_conectado.txt`. Depois de restaurar o endpoint, conferi nova conexão, confirmação das sequências 3 a 46 em ordem e fila vazia, sem reiniciar o ESP32. Preservei `wokwi_mqtt_final_broker_off.txt` e `wokwi_mqtt_final_broker_recuperado.txt`. A recuperação não foi imediata: observei novas falhas TCP e novas tentativas antes da conexão.

Na mesma sessão, desconectei a chave, mantive a coleta e acumulei pendências. Ao reconectar, conferi confirmação das sequências 47 a 64 e fila vazia. Preservei `wokwi_mqtt_final_chave_offline.txt` e `wokwi_mqtt_final_chave_recuperada.txt`.

Depois desses cenários, corrigi a unidade do tempo limite TCP para três segundos, conforme a API WiFiClient do ESP32 2.0.17. Recompilei, salvei a configuração final e confirmei novas leituras e ACKs na sessão `55667c68c701d7ae`, registrada em `wokwi_mqtt_timeout_final.txt`. Esse último registro confere a comunicação após o ajuste; os ensaios completos de falha estão nos arquivos anteriores.

## Verificações locais e teste complementar de rede

Executei os 14 testes Python com sucesso. Conferi contrato, BPM, coerência temporal, JSON inválido, falha de gravação, confirmação após commit, duplicatas após reinício, mudança de sessão e conflitos. Compilei e executei o teste C++ de timeout, reenvio e rejeição de ACK incorreto, repetido ou anterior à primeira tentativa.

Compilei a revisão para ESP32 com DHTesp 1.19.0, PubSubClient 2.8.0, ArduinoJson 6.21.5 e ESP32 2.0.17: 744.821 bytes de flash, 56%, e 45.456 bytes de variáveis globais, 13%. Além dessas variáveis, aloquei a fila fixa de 80.016 bytes no heap. Observei 206.188 bytes livres antes de iniciar a tarefa de rede; esse valor não representa o consumo máximo durante uma conexão.

Também executei `scripts/testar_transporte_mqtt.py` pelo HiveMQ com publicador identificado como `cardioia-publicador-python`, em namespace exclusivo. Conferi duas medições únicas, duas duplicatas, um ACK omitido e um conflito rejeitado, além de replay. Preservei os resultados em `teste_rede_python/`. Usei QoS 1 nesse publicador complementar; no ESP32, usei QoS 0 com reenvio e confirmação da aplicação.

## Gateway e limites da demonstração

Observei falhas intermitentes de conexão a `wss://netwi.wokwi.com/` e preservei capturas e logs. Após reiniciar a simulação, consegui realizar as trocas reais descritas acima. Não atribuí essas falhas a uma indisponibilidade do HiveMQ.

Usei apenas dados fictícios em broker público, sem autenticação ou TLS. Executei o consumidor e a persistência no computador; o broker é o componente remoto deste ensaio. Mantive a fila do ESP32 em RAM: não alego preservação após reinício ou falta de energia, nem entrega exatamente uma vez pelo protocolo MQTT. Ao interromper simulações com pendências para atualizar o firmware, não considerei essas pendências recuperadas na sessão seguinte.

## Continuidade

Conferi automaticamente os cenários capturados com `scripts/validar_cenarios_mqtt.py` e registrei aprovação em `validacao_cenarios.json`. Cruzei os ACKs do Serial com os eventos de armazenamento, conferi as sequências em ordem, a ausência de registros duplicados e o retorno à fila vazia.

Concluí minha revisão funcional no Chrome e conferi 75 medições únicas no banco. Preservei os registros adicionais em [Minha validação funcional](validacao_guiada/RESULTADOS.md). Minha próxima etapa é Node-RED com gráficos, indicadores e alertas, mantendo separados dados atrasados e condição atual do dispositivo.
