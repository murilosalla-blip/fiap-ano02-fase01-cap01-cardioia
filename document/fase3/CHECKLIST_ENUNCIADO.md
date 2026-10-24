# Checklist do enunciado Fase 3

Acompanho separadamente o que implementei localmente, testei, revisei, publiquei e ainda preciso concluir. Só marco uma etapa como concluída após conferir a evidência correspondente.

| Requisito | Entrega | Evidência prevista | Estado |
|---|---:|---|---|
| ESP32 no Wokwi e dois sensores distintos, incluindo DHT22 | 1 | Sketch, diagrama e projeto público | Compilei, conferi no simulador e concluí a revisão da primeira entrega |
| Coleta periódica e conectividade booleana | 1 | Firmware e demonstração Serial | Conferi no Wokwi e salvei registros em `evidencias/` |
| Resiliência offline e armazenamento limitado | 1–2 | Fila, testes e cenário de recuperação | Testei o núcleo C++ e conferi no Wokwi recuperação Serial, fila cheia, botão segurado e reinício; também implementei MQTT, confirmei reenvio e recuperação após reiniciar o consumidor |
| C++ comentado e link Wokwi | 1 | `firmware/cardioia_edge/` e https://wokwi.com/projects/478054573982428161 | Comentei o código, publiquei o link e reorganizei o circuito durante minha revisão |
| Relatório Edge mínimo uma página | 6 | PDF final | Ainda preciso concluir |
| Transmissão MQTT e broker | 2 | Firmware compilado, consumidor, eventos de rede e projeto https://wokwi.com/projects/478772789361460225 | Confirmei a troca real do ESP32 pelo broker, a confirmação após persistência e a recuperação após reiniciar o consumidor; também conferi falha controlada do endpoint, recuperação ordenada e retorno à fila vazia |
| Dashboard Node-RED com gráfico, gauge e alerta | 3 | `node-red/flows.json` e `evidencias/2026-10-24/dashboard/` | Implementei e testei regras, rede e recebimento do ESP32; concluí a revisão visual guiada com entrada e retorno dos dois alertas |
| Relatório MQTT/dashboard mínimo duas páginas | 6 | PDF final | Ainda preciso concluir |
| Ir Além 1 cliente REST envia e recebe | 4 | Python e teste HTTP | Ainda preciso concluir |
| Ir Além 1 regras de risco e e-mail simulado | 4 | Código, teste e e-mail demonstrativo | Ainda preciso concluir |
| Ir Além 1 relatório de uma a duas páginas | 4 | PDF final | Ainda preciso concluir |
| Ir Além 2 classificador tradicional e LIF/FHN | 5 | Notebook executado e resultados | Ainda preciso concluir |
| Ir Além 2 repositório público, código e README | 5–6 | URL e reprodução | Ainda preciso publicar a Fase 3 |
| Ir Além 2 relatório comparativo de duas páginas | 5 | PDF final | Ainda preciso concluir |
| Ir Além 2 vídeo até quatro minutos não listado | 5 | YouTube e link README | Ainda preciso concluir |
| Clareza, organização e revisão de evidências | Todas | Roteiro e pacote final | Estou acompanhando as evidências |

SPIFFS e hardware físico não são obrigatórios segundo o enunciado fornecido; Grafana é opcional. A implementação Serial da primeira entrega não satisfaz, sozinha, a Parte 2 de MQTT.
