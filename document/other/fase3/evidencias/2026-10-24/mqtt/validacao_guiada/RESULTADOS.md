# Nossa validação funcional da entrega MQTT

Em 24/10/2026, executamos a validação no Chrome com o consumidor Python no PowerShell. Mantivemos a sessão `5f1ffeb88efb4c0c` durante os cenários, sem reiniciar o ESP32.

- Conferimos coleta offline e primeira recuperação até a sequência 25, com fila vazia.
- Desconectamos a chave e conferimos a recuperação ordenada das sequências 26 a 32; confirmamos a sequência 33 com fila vazia.
- Acionamos o botão e conferimos 20, 21, 22 e 25 pulsos por janela de cinco segundos, equivalentes a 240, 252, 264 e 300 BPM simulados. Conferimos os ACKs das sequências 39 a 42.
- Alteramos o DHT22 e conferimos 31 °C, leitura válida e confirmação da sequência 47.
- Enviamos `broker_off`, observamos falhas na porta TCP 1 e continuidade da coleta. Enviamos `broker_on` e conferimos recuperação das sequências 49 a 60, seguida de transmissão normal das sequências 61 e 62.
- Interrompemos o consumidor com Ctrl+C. Mantivemos a sequência 65 pendente enquanto as tentativas aumentavam e novas leituras eram coletadas. Reiniciamos o consumidor com o mesmo banco e conferimos recuperação até a sequência 73, com fila vazia, seguida de confirmações normais das sequências 74 e 75.

## Nossa conferência da persistência

Consultamos o banco em modo somente leitura e conferimos 75 medições únicas, das sequências 1 a 75, sem lacunas e com `dropped_total=0`. Cruzamos os eventos das sequências 1 e 65: encontramos uma gravação por identidade, omissão do primeiro ACK e reconhecimento de reenvio como duplicata. Preservamos a extração em `amostras_persistidas_1_a_75.json`, os eventos correspondentes em `eventos_sessao_1_a_75.jsonl` e o resultado em `conferencia_banco.json`.

Preservamos os trechos do Monitor Serial nos quatro arquivos numerados desta pasta. O primeiro trecho é parcial; complementamos a conferência com as leituras posteriores e com o banco. Registramos a recuperação da chave nas observações acima; esse intervalo também está presente na extração do banco.

Concluímos a validação funcional da segunda entrega. Nossa próxima etapa é o dashboard Node-RED com gráficos, indicadores e alertas. Mantivemos os limites já documentados: dados fictícios, broker público e fila do ESP32 em RAM.
