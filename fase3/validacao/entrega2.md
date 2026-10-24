# Minha validação da integração MQTT

Preparei o [projeto MQTT no Wokwi](https://wokwi.com/projects/478772789361460225) e o consumidor descrito em `../mqtt/README.md`. Preservei a versão Edge original.

## Como vou reproduzir a demonstração ponta a ponta

1. Vou iniciar `python fase3/python/consumidor_mqtt.py --reter-primeiro-ack` e conferir conexão e assinaturas no broker.
2. Vou executar o Wokwi com a chave à esquerda e observar pelo menos três leituras acumuladas.
3. Vou mover a chave à direita e conferir que o consumidor recebe a primeira leitura e omite apenas seu primeiro ACK.
4. Vou conferir no Serial a manutenção da primeira pendência, sua nova tentativa e a liberação somente após a confirmação correta.
5. Vou verificar no banco uma única linha para essa identidade, apesar dos reenvios.
6. Vou voltar a chave à esquerda, continuar coletando e depois conferir a recuperação ordenada ao reconectar.
7. Vou enviar `broker_off` no Monitor Serial, observar a falha controlada de acesso ao endpoint e conferir que a coleta continua. Depois vou enviar `broker_on` e conferir a reconexão e a recuperação.
8. Vou parar o consumidor, observar reenvios sem retirada da primeira pendência e reiniciar o consumidor com o mesmo banco para confirmar a deduplicação persistente.
9. Vou salvar eventos, capturas e resultados, distinguindo horários de coleta, preparação da tentativa e recebimento.

## O que já conferi

Executei os testes locais de persistência e confirmação e compilei o firmware. Também testei o consumidor pelo broker real com um publicador Python identificado; conferi confirmação perdida, duplicatas, conflito e replay. Registrei a origem desse teste separadamente, pois ele não substitui o ESP32.

No Wokwi, confirmei a troca real do ESP32, omiti o primeiro ACK e conferi nova tentativa após 3.000 ms, seguida de confirmação. No consumidor, mantive apenas uma medição para essa identidade. Também conferi a retenção da primeira pendência enquanto o consumidor estava parado; ao reiniciá-lo com o mesmo banco, recuperei as sequências 1 a 20 e voltei à fila vazia. Registrei as evidências em `../evidencias/2026-10-24/mqtt/RESULTADOS.md`.

Observei uma primeira recuperação incompleta após restaurar o endpoint. Acrescentei o encerramento do socket antes das tentativas e a reinicialização do Wi-Fi após três falhas TCP consecutivas. Compilei e publiquei essa revisão. Confirmei a recuperação das sequências 3 a 46 após restaurar o endpoint e das sequências 47 a 64 após reconectar a chave, com fila vazia ao final de cada cenário. Na configuração final, corrigi a unidade do tempo limite TCP para três segundos e conferi novas trocas com o consumidor. Registrei o resultado automático em `../evidencias/2026-10-24/mqtt/validacao_cenarios.json`.

## Minha validação funcional no Chrome

Concluí os cenários de sensores, desconexão da chave, falha de acesso ao broker e reinício do consumidor na sessão `5f1ffeb88efb4c0c`. Conferi 75 medições únicas no banco, sem lacunas, e a deduplicação das sequências 1 e 65. Preservei os registros em `../evidencias/2026-10-24/mqtt/validacao_guiada/RESULTADOS.md`.
