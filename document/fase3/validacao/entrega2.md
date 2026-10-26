# Nossa validação da integração MQTT

Preparamos o [projeto MQTT no Wokwi](https://wokwi.com/projects/478772789361460225) e o consumidor descrito em `../mqtt/README.md`. Preservamos a versão Edge original.

## Como reproduzir a demonstração ponta a ponta

1. iniciar `python src/fase3/python/consumidor_mqtt.py --reter-primeiro-ack` e conferir conexão e assinaturas no broker.
2. executar o Wokwi com a chave à esquerda e observar pelo menos três leituras acumuladas.
3. mover a chave à direita e conferir que o consumidor recebe a primeira leitura e omite apenas seu primeiro ACK.
4. conferir no Serial a manutenção da primeira pendência, sua nova tentativa e a liberação somente após a confirmação correta.
5. verificar no banco uma única linha para essa identidade, apesar dos reenvios.
6. voltar a chave à esquerda, continuar coletando e depois conferir a recuperação ordenada ao reconectar.
7. enviar `broker_off` no Monitor Serial, observar a falha controlada de acesso ao endpoint e conferir que a coleta continua. Depois, enviar `broker_on` e conferir a reconexão e a recuperação.
8. parar o consumidor, observar reenvios sem retirada da primeira pendência e reiniciar o consumidor com o mesmo banco para confirmar a deduplicação persistente.
9. salvar eventos, capturas e resultados, distinguindo horários de coleta, preparação da tentativa e recebimento.

## O que já conferimos

Executamos os testes locais de persistência e confirmação e compilamos o firmware. Também testamos o consumidor pelo broker real com um publicador Python identificado; conferimos confirmação perdida, duplicatas, conflito e replay. Registramos a origem desse teste separadamente, pois ele não substitui o ESP32.

No Wokwi, confirmamos a troca real do ESP32, omitimos o primeiro ACK e conferimos nova tentativa após 3.000 ms, seguida de confirmação. No consumidor, mantivemos apenas uma medição para essa identidade. Também conferimos a retenção da primeira pendência enquanto o consumidor estava parado; ao reiniciá-lo com o mesmo banco, recuperamos as sequências 1 a 20 e voltamos à fila vazia. Registramos as evidências em `../../other/fase3/evidencias/2026-10-24/mqtt/RESULTADOS.md`.

Observamos uma primeira recuperação incompleta após restaurar o endpoint. Acrescentamos o encerramento do socket antes das tentativas e a reinicialização do Wi-Fi após três falhas TCP consecutivas. Compilamos e publicamos essa revisão. Confirmamos a recuperação das sequências 3 a 46 após restaurar o endpoint e das sequências 47 a 64 após reconectar a chave, com fila vazia ao final de cada cenário. Na configuração final, corrigimos a unidade do tempo limite TCP para três segundos e conferimos novas trocas com o consumidor. Registramos o resultado automático em `../../other/fase3/evidencias/2026-10-24/mqtt/validacao_cenarios.json`.

## Nossa validação funcional no Chrome

Concluímos os cenários de sensores, desconexão da chave, falha de acesso ao broker e reinício do consumidor na sessão `5f1ffeb88efb4c0c`. Conferimos 75 medições únicas no banco, sem lacunas, e a deduplicação das sequências 1 e 65. Preservamos os registros em `../../other/fase3/evidencias/2026-10-24/mqtt/validacao_guiada/RESULTADOS.md`.
