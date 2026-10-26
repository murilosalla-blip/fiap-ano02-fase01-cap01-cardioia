# Integração MQTT e confirmação das leituras

Implementamos a variante MQTT em `src/fase3/firmware/cardioia_mqtt/`, mantendo a versão Edge original em `src/fase3/firmware/cardioia_edge/`. Preservamos o núcleo da fila e o circuito já conferido; incluímos um teste para garantir que os dois arquivos `edge_core.h` permaneçam idênticos.

Salvamos o [projeto MQTT no Wokwi](https://wokwi.com/projects/478772789361460225). Registramos a troca real do ESP32 pelo broker, a deduplicação após omitir um ACK e a recuperação da fila após reiniciar o consumidor em `../../other/fase3/evidencias/2026-10-24/mqtt/RESULTADOS.md`. Também preservamos as ocorrências intermitentes de falha do gateway e os ensaios de recuperação.

## Fluxo que implementamos

1. Coletamos os sensores a cada cinco segundos, independentemente da tarefa de rede.
2. Armazenamos até 2.000 leituras. Alocamos essa fila fixa uma única vez na inicialização para acomodar a memória estática do Wi-Fi.
3. Enviamos a primeira pendência por MQTT quando a chave permite conexão e o broker está acessível.
4. No consumidor Python, validamos o contrato, a identidade e a coerência dos dados e gravamos a leitura em SQLite.
5. Somente após concluir a transação, publicamos a confirmação com dispositivo, sessão e sequência.
6. No ESP32, conferimos a identidade da confirmação e retiramos apenas a cabeça correspondente. Se não houver confirmação, agendamos nova tentativa após três segundos.

Registramos o consumidor em `python/consumidor_mqtt.py` e a persistência em `python/mqtt_store.py`. Usamos a chave composta `(device_id, session_id, sequence)` para evitar registros duplicados, inclusive após reiniciar o consumidor. Se recebermos a mesma identidade com medições diferentes, rejeitamos a mensagem sem confirmá-la. Podemos atualizar os metadados de tentativa sem alterar a medição original.

## Conexão demonstrativa

Escolhemos `broker.hivemq.com`, porta TCP `1883`, como broker público de testes. Usamos exclusivamente dados fictícios, sem nomes de pacientes, credenciais ou dados pessoais. Essa configuração não tem autenticação nem TLS; não a consideramos adequada a um serviço clínico. O namespace evita colisões acidentais com outros projetos, mas não autentica os participantes.

Definimos a raiz `cardioia/aura/fase3/478054573982428161/v1` e os tópicos:

| Finalidade | Tópico abaixo da raiz | Política |
|---|---|---|
| Telemetria | `devices/cardioia-esp32-01/telemetry` | Publicamos com QoS 0 e sem retained; mantemos a leitura até o ACK da aplicação |
| Confirmação | `devices/cardioia-esp32-01/ack` | O consumidor publica com QoS 1 e sem retained |
| Estado | `devices/cardioia-esp32-01/status` | Publicamos estado com retained e configuramos Last Will para desconexão inesperada |

Não interpretamos `publish()==true` como confirmação de armazenamento. Nossa garantia combina tentativas repetidas com persistência e deduplicação no consumidor. Não alegamos entrega exatamente uma vez pelo protocolo MQTT nem preservação da fila do ESP32 após queda de energia.

## Informações temporais

Preservamos `collected_uptime_ms` como tempo da coleta relativo à inicialização. Acrescentamos `sent_uptime_ms` como momento de preparar a tentativa, `age_ms` como sua diferença para a coleta e `attempt` como contador de tentativas agendadas. Marcamos `replay=true` quando essa idade excede dez segundos.

No consumidor, registramos `received_at` em UTC e mantemos o primeiro recebimento da medição. Não inventamos um horário UTC de coleta a partir do relógio relativo do ESP32. Uma espera entre preparar a tentativa e transmitir a mensagem pode aumentar a idade real; no painel Node-RED consideramos também a atualização do fluxo e o estado da conexão para os alertas.

## Como executar o consumidor

O [guia principal](../README.md) apresenta a instalação, a inicialização integrada e os resultados esperados. Para executar somente o consumidor, da raiz e com `.venv` preparado:

```powershell
.\.venv\Scripts\python.exe -u src/fase3/python/consumidor_mqtt.py
```

Gravamos a base em `.tools/runtime/fase3/telemetria.sqlite3` e os eventos em `.tools/runtime/fase3/eventos_mqtt.jsonl`, fora do versionamento. Para conferir confirmação perdida, encerrar antes o consumidor integrado e executar a mesma linha com `--reter-primeiro-ack`. O guia detalha `stored` → `ack_withheld` → reenvio → `duplicate` → `ack_queued`.

Com `--sem-ack`, persistimos as leituras sem confirmar, para demonstrar retenção da pendência. Podemos selecionar duração, banco, eventos, host, porta e tópico pelas opções de `--help`. Não executar dois consumidores no mesmo tópico no teste de retenção do ACK.

## Como executar o firmware

No Wokwi, usamos o sketch de `src/fase3/firmware/cardioia_mqtt/`, os três arquivos de cabeçalho/circuito necessários e `libraries.txt`. Mantemos o arquivo inicial `sketch.ino` apenas com um comentário quando importamos `cardioia_mqtt.ino` como aba adicional. Ao reproduzir em um projeto vazio, também podemos renomear o conteúdo principal para `sketch.ino`.

Usamos o DHT22 em GPIO 15, o botão em GPIO 26 e a chave em GPIO 27. A chave à esquerda impede a conexão e mantém a coleta; à direita permite a conexão. No Monitor Serial, podemos enviar:

| Comando | Cenário que preparamos |
|---|---|
| `broker_off` | Mantemos Wi-Fi e direcionamos as tentativas MQTT à porta TCP 1 para provocar falha de acesso ao endpoint |
| `broker_on` | Restauramos a porta 1883 para reconexão e recuperação das pendências |

Configuramos o tempo limite TCP em três segundos, respeitando a unidade em segundos da biblioteca WiFiClient do ESP32 2.0.17. Antes de cada nova conexão, encerramos o socket anterior. Após três falhas TCP consecutivas, reiniciamos a conexão Wi-Fi e continuamos coletando na tarefa principal. Essa injeção de falha afeta nosso cliente, sem interromper o serviço público. Registramos essa ocorrência como falha controlada de acesso ao broker, sem afirmar que o HiveMQ ficou indisponível para outros usuários.

Para compilar localmente, utilizamos ESP32 2.0.17, DHTesp 1.19.0, PubSubClient 2.8.0 e ArduinoJson 6.21.5. Configuramos o buffer MQTT em 1.536 bytes e limitamos o JSON de telemetria a 1.023 bytes úteis. A operação de rede ocorre em uma tarefa separada; compartilhamos mensagens por filas FreeRTOS, sem acessar a fila de leituras de dois núcleos ao mesmo tempo.

## Verificações

```sh
python -m unittest discover -s src/fase3/tests -p 'test_*.py' -v
g++ -std=c++11 -Wall -Wextra -Werror src/fase3/tests/test_mqtt_delivery.cpp -o test_mqtt_delivery
./test_mqtt_delivery
```

Testamos persistência antes do ACK, reenvio, duplicatas após reinício do consumidor, mensagens conflitantes, campos inválidos, falha de escrita e política de timeout. Também executamos o consumidor pelo broker real com publicador Python identificado, usando `scripts/fase3/testar_transporte_mqtt.py`. Registramos as evidências em `evidencias/2026-10-24/mqtt/`, distinguindo esse teste complementar da troca real também conferida com o ESP32.

Conferimos também os registros dos cenários reais com:

```sh
python scripts/fase3/validar_cenarios_mqtt.py document/other/fase3/evidencias/2026-10-24/mqtt
```

Escolhemos os intervalos de coleta, repetição e reconexão como parâmetros da implementação; não os apresentamos como tempos obrigatórios do enunciado.

## Referências técnicas que consultamos

- [Wi-Fi no ESP32 do Wokwi](https://docs.wokwi.com/guides/esp32-wifi)
- [Broker público HiveMQ](https://www.hivemq.com/mqtt/public-mqtt-broker/)
- [PubSubClient](https://pubsubclient.knolleary.net/api)
- [Paho MQTT Python](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html)

## Nossa revisão dos tempos MQTT no Wokwi

Ajustamos o keepalive para 300 segundos e a espera de resposta MQTT para cinco segundos. Mantivemos coleta a cada cinco segundos simulados e reenvio após três segundos simulados. Fizemos essa separação porque o broker mede tempo real, enquanto observamos o Wokwi avançando lentamente em segundo plano. Preservamos a sinalização explícita da chave e a validação da fila e dos ACKs.

Um keepalive maior pode atrasar o Last Will em uma falha silenciosa. No painel, mantemos o prazo independente de 15 segundos reais para retirar a condição de dado atual, preservando o último valor em cinza. Não interpretamos conexão MQTT como comprovação de leitura recente. Registramos o ensaio em `../../other/fase3/evidencias/2026-10-24/dashboard/estabilidade/RESULTADOS.md`.
