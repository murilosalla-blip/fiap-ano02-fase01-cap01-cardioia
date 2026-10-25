# Contrato de telemetria

Definimos a mensagem comum às próximas integrações com JSON Schema v2020-12. Preparamos o exemplo como referência de formato, separado das capturas do dispositivo.

Identidade de uma leitura: `(device_id, session_id, sequence)`. A sessão muda ao reiniciar. `collected_uptime_ms` é tempo desde a inicialização do dispositivo, não data/hora UTC. O consumidor deve registrar seu horário de recebimento separadamente. `window_ms` é a duração efetiva da janela contada; `heart_rate_bpm = pulse_count * 60000 / window_ms`, arredondado a duas casas na saída Serial. Zero pulsos significa ausência de pressão do botão nessa janela, não ausência de atividade cardíaca.

Definimos que `dht_valid=false` exige temperatura e umidade `null`; não vamos substituir ausência de leitura por zero. `dropped_total` é a perda acumulada por fila cheia na sessão, observada no momento do envio. `backlog_samples` inclui a leitura sendo enviada. Esses metadados podem variar em uma retransmissão da mesma leitura.

Mantivemos `simulated` sempre verdadeiro. Usamos `transport=serial_demo` para identificar a demonstração local e `transport=mqtt` na nova variante de transmissão. Implementamos a confirmação de dispositivo, sessão e sequência correspondentes à primeira pendência; definimos seu formato em `ack.schema.json`. Testamos o consumidor pelo broker real com publicador Python e confirmamos também a troca com o ESP32 no Wokwi, incluindo reenvio e deduplicação após omitir a primeira confirmação.

Na variante MQTT, acrescentamos `sent_uptime_ms`, `age_ms`, `attempt` e `replay`. Definimos `sent_uptime_ms` como o momento de preparar a tentativa, `age_ms` como sua diferença em relação à coleta e `replay=true` quando essa idade excede dez segundos. No consumidor, conferimos essa coerência e registramos separadamente o recebimento UTC.

Definimos a capacidade padrão em 2.000 leituras. Adotamos a política de preservar as antigas e descartar a nova quando a fila estiver cheia; mantivemos o avanço da sequência para evidenciar lacunas. Para preservar o histórico sem confundir leituras antigas com atuais, vamos indicar o atraso e impedir alertas atuais a partir do replay.
