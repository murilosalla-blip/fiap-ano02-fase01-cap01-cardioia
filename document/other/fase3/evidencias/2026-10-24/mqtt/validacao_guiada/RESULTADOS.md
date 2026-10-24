# Minha validação funcional da entrega MQTT

Em 24/10/2026, executei a validação no Chrome com o consumidor Python no PowerShell. Mantive a sessão `5f1ffeb88efb4c0c` durante os cenários, sem reiniciar o ESP32.

- Conferi coleta offline e primeira recuperação até a sequência 25, com fila vazia.
- Desconectei a chave e conferi a recuperação ordenada das sequências 26 a 32; confirmei a sequência 33 com fila vazia.
- Acionei o botão e conferi 20, 21, 22 e 25 pulsos por janela de cinco segundos, equivalentes a 240, 252, 264 e 300 BPM simulados. Conferi os ACKs das sequências 39 a 42.
- Alterei o DHT22 e conferi 31 °C, leitura válida e confirmação da sequência 47.
- Enviei `broker_off`, observei falhas na porta TCP 1 e continuidade da coleta. Enviei `broker_on` e conferi recuperação das sequências 49 a 60, seguida de transmissão normal das sequências 61 e 62.
- Interrompi o consumidor com Ctrl+C. Mantive a sequência 65 pendente enquanto as tentativas aumentavam e novas leituras eram coletadas. Reiniciei o consumidor com o mesmo banco e conferi recuperação até a sequência 73, com fila vazia, seguida de confirmações normais das sequências 74 e 75.

## Minha conferência da persistência

Consultei o banco em modo somente leitura e conferi 75 medições únicas, das sequências 1 a 75, sem lacunas e com `dropped_total=0`. Cruzei os eventos das sequências 1 e 65: encontrei uma gravação por identidade, omissão do primeiro ACK e reconhecimento de reenvio como duplicata. Preservei a extração em `amostras_persistidas_1_a_75.json`, os eventos correspondentes em `eventos_sessao_1_a_75.jsonl` e o resultado em `conferencia_banco.json`.

Preservei os trechos do Monitor Serial nos quatro arquivos numerados desta pasta. O primeiro trecho é parcial; complementei a conferência com as leituras posteriores e com o banco. Registrei a recuperação da chave nas observações acima; esse intervalo também está presente na extração do banco.

Concluí a validação funcional da segunda entrega. Minha próxima etapa é o dashboard Node-RED com gráficos, indicadores e alertas. Mantive os limites já documentados: dados fictícios, broker público e fila do ESP32 em RAM.
