# Contrato de telemetria

Defini a mensagem comum às próximas integrações com JSON Schema v2020-12. Preparei o exemplo como referência de formato, separado das capturas do dispositivo.

Identidade de uma leitura: `(device_id, session_id, sequence)`. A sessão muda ao reiniciar. `collected_uptime_ms` é tempo desde a inicialização do dispositivo, não data/hora UTC. O consumidor deve registrar seu horário de recebimento separadamente. `window_ms` é a duração efetiva da janela contada; `heart_rate_bpm = pulse_count * 60000 / window_ms`, arredondado a duas casas na saída Serial. Zero pulsos significa ausência de pressão do botão nessa janela, não ausência de atividade cardíaca.

Defini que `dht_valid=false` exige temperatura e umidade `null`; não vou substituir ausência de leitura por zero. `dropped_total` é a perda acumulada por fila cheia na sessão, observada no momento do envio. `backlog_samples` inclui a leitura sendo enviada. Esses metadados podem variar em uma retransmissão da mesma leitura.

Mantive `simulated` sempre verdadeiro. Usei `transport=serial_demo` para identificar a demonstração local e `transport=mqtt` na nova variante de transmissão. Implementei a confirmação de dispositivo, sessão e sequência correspondentes à primeira pendência; defini seu formato em `ack.schema.json`. Testei o consumidor pelo broker real com publicador Python e confirmei também a troca com o ESP32 no Wokwi, incluindo reenvio e deduplicação após omitir a primeira confirmação.

Na variante MQTT, acrescentei `sent_uptime_ms`, `age_ms`, `attempt` e `replay`. Defini `sent_uptime_ms` como o momento de preparar a tentativa, `age_ms` como sua diferença em relação à coleta e `replay=true` quando essa idade excede dez segundos. No consumidor, confiro essa coerência e registro separadamente o recebimento UTC.

Defini a capacidade padrão em 2.000 leituras. Adotei a política de preservar as antigas e descartar a nova quando a fila estiver cheia; mantive o avanço da sequência para evidenciar lacunas. Para preservar o histórico sem confundir leituras antigas com atuais, vou indicar o atraso e impedir alertas atuais a partir do replay.
