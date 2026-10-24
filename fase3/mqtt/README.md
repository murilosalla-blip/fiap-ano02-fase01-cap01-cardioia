# Integração MQTT e confirmação das leituras

Implementei a variante MQTT em `firmware/cardioia_mqtt/`, mantendo a versão Edge original em `firmware/cardioia_edge/`. Preservei o núcleo da fila e o circuito já conferido; incluí um teste para garantir que os dois arquivos `edge_core.h` permaneçam idênticos.

Salvei o [projeto MQTT no Wokwi](https://wokwi.com/projects/478772789361460225). Registrei a troca real do ESP32 pelo broker, a deduplicação após omitir um ACK e a recuperação da fila após reiniciar o consumidor em `../evidencias/2026-10-24/mqtt/RESULTADOS.md`. Também preservei as ocorrências intermitentes de falha do gateway e os ensaios de recuperação.

## Fluxo que implementei

1. Coleto os sensores a cada cinco segundos, independentemente da tarefa de rede.
2. Armazeno até 2.000 leituras. Aloquei essa fila fixa uma única vez na inicialização para acomodar a memória estática do Wi-Fi.
3. Envio a primeira pendência por MQTT quando a chave permite conexão e o broker está acessível.
4. No consumidor Python, valido o contrato, a identidade e a coerência dos dados e gravo a leitura em SQLite.
5. Somente após concluir a transação, publico a confirmação com dispositivo, sessão e sequência.
6. No ESP32, confiro a identidade da confirmação e retiro apenas a cabeça correspondente. Se não houver confirmação, agendo nova tentativa após três segundos.

Registrei o consumidor em `python/consumidor_mqtt.py` e a persistência em `python/mqtt_store.py`. Uso a chave composta `(device_id, session_id, sequence)` para evitar registros duplicados, inclusive após reiniciar o consumidor. Se receber a mesma identidade com medições diferentes, rejeito a mensagem sem confirmá-la. Posso atualizar os metadados de tentativa sem alterar a medição original.

## Conexão demonstrativa

Escolhi `broker.hivemq.com`, porta TCP `1883`, como broker público de testes. Usei exclusivamente dados fictícios, sem nomes de pacientes, credenciais ou dados pessoais. Essa configuração não tem autenticação nem TLS; não a considero adequada a um serviço clínico. O namespace evita colisões acidentais com outros projetos, mas não autentica os participantes.

Defini a raiz `cardioia/aura/fase3/478054573982428161/v1` e os tópicos:

| Finalidade | Tópico abaixo da raiz | Política |
|---|---|---|
| Telemetria | `devices/cardioia-esp32-01/telemetry` | Publico com QoS 0 e sem retained; mantenho a leitura até o ACK da aplicação |
| Confirmação | `devices/cardioia-esp32-01/ack` | O consumidor publica com QoS 1 e sem retained |
| Estado | `devices/cardioia-esp32-01/status` | Publico estado com retained e configuro Last Will para desconexão inesperada |

Não interpreto `publish()==true` como confirmação de armazenamento. Minha garantia combina tentativas repetidas com persistência e deduplicação no consumidor. Não alego entrega exatamente uma vez pelo protocolo MQTT nem preservação da fila do ESP32 após queda de energia.

## Informações temporais

Preservei `collected_uptime_ms` como tempo da coleta relativo à inicialização. Acrescentei `sent_uptime_ms` como momento de preparar a tentativa, `age_ms` como sua diferença para a coleta e `attempt` como contador de tentativas agendadas. Marco `replay=true` quando essa idade excede dez segundos.

No consumidor, registro `received_at` em UTC e mantenho o primeiro recebimento da medição. Não invento um horário UTC de coleta a partir do relógio relativo do ESP32. Uma espera entre preparar a tentativa e transmiti-la pode aumentar a idade real; na próxima etapa vou considerar também a atualização do fluxo e o estado da conexão para os alertas.

## Como executo o consumidor

```sh
python -m pip install -r fase3/requirements-mqtt.txt
python fase3/python/consumidor_mqtt.py
```

Gravo a base em `fase3/runtime/telemetria.sqlite3` e os eventos em `fase3/runtime/eventos_mqtt.jsonl`, fora do versionamento. Para conferir uma confirmação perdida, executo:

```sh
python fase3/python/consumidor_mqtt.py --reter-primeiro-ack
```

Com `--sem-ack`, persisto todas as leituras recebidas, mas não confirmo nenhuma. Uso esse modo apenas para demonstrar a retenção da primeira pendência no ESP32. Posso definir `--duracao`, `--db`, `--eventos`, `--host`, `--port` e `--topico` para reproduzir cenários isolados.

## Como executo o firmware

No Wokwi, uso o sketch de `firmware/cardioia_mqtt/`, os três arquivos de cabeçalho/circuito necessários e `libraries.txt`. Mantenho o arquivo inicial `sketch.ino` apenas com um comentário quando importo `cardioia_mqtt.ino` como aba adicional. Ao reproduzir em um projeto vazio, também posso renomear o conteúdo principal para `sketch.ino`.

Uso o DHT22 em GPIO 15, o botão em GPIO 26 e a chave em GPIO 27. A chave à esquerda impede a conexão e mantém a coleta; à direita permite a conexão. No Monitor Serial, posso enviar:

| Comando | Cenário que preparo |
|---|---|
| `broker_off` | Mantenho Wi-Fi e direciono as tentativas MQTT à porta TCP 1 para provocar falha de acesso ao endpoint |
| `broker_on` | Restauro a porta 1883 para reconexão e recuperação das pendências |

Configurei o tempo limite TCP em três segundos, respeitando a unidade em segundos da biblioteca WiFiClient do ESP32 2.0.17. Antes de cada nova conexão, encerro o socket anterior. Após três falhas TCP consecutivas, reinicio a conexão Wi-Fi e continuo coletando na tarefa principal. Essa injeção de falha afeta meu cliente, sem interromper o serviço público. Registro-a como falha controlada de acesso ao broker, sem afirmar que o HiveMQ ficou indisponível para outros usuários.

Para compilar localmente, uso ESP32 2.0.17, DHTesp 1.19.0, PubSubClient 2.8.0 e ArduinoJson 6.21.5. Configurei o buffer MQTT em 1.536 bytes e limitei o JSON de telemetria a 1.023 bytes úteis. A operação de rede ocorre em uma tarefa separada; compartilho mensagens por filas FreeRTOS, sem acessar a fila de leituras de dois núcleos ao mesmo tempo.

## Verificações

```sh
python -m unittest discover -s fase3/tests -p 'test_*.py' -v
g++ -std=c++11 -Wall -Wextra -Werror fase3/tests/test_mqtt_delivery.cpp -o test_mqtt_delivery
./test_mqtt_delivery
```

Testei persistência antes do ACK, reenvio, duplicatas após reinício do consumidor, mensagens conflitantes, campos inválidos, falha de escrita e política de timeout. Também executei o consumidor pelo broker real com publicador Python identificado, usando `scripts/testar_transporte_mqtt.py`. Registrei as evidências em `evidencias/2026-10-24/mqtt/`, distinguindo esse teste complementar da troca real também conferida com o ESP32.

Conferi também os registros dos cenários reais com:

```sh
python fase3/scripts/validar_cenarios_mqtt.py fase3/evidencias/2026-10-24/mqtt
```

Escolhi os intervalos de coleta, repetição e reconexão como parâmetros da implementação; não os apresentei como tempos obrigatórios do enunciado.

## Referências técnicas que consultei

- [Wi-Fi no ESP32 do Wokwi](https://docs.wokwi.com/guides/esp32-wifi)
- [Broker público HiveMQ](https://www.hivemq.com/mqtt/public-mqtt-broker/)
- [PubSubClient](https://pubsubclient.knolleary.net/api)
- [Paho MQTT Python](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html)

## Minha revisão dos tempos MQTT no Wokwi

Ajustei o keepalive para 300 segundos e a espera de resposta MQTT para cinco segundos. Mantive coleta a cada cinco segundos simulados e reenvio após três segundos simulados. Fiz essa separação porque o broker mede tempo real, enquanto observei o Wokwi avançando lentamente em segundo plano. Preservei a sinalização explícita da chave e a validação da fila e dos ACKs.

Um keepalive maior pode atrasar o Last Will em uma falha silenciosa. No painel, mantenho o prazo independente de 15 segundos reais para retirar a condição de dado atual, preservando o último valor em cinza. Não interpreto conexão MQTT como comprovação de leitura recente. Registrei o ensaio em `../evidencias/2026-10-24/dashboard/estabilidade/RESULTADOS.md`.
