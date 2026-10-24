# Minha validação visual e funcional do painel

Concluí a revisão da terceira entrega em 24/10/2026 no Chrome, com a sessão `546cb527f2cc13d5` do ESP32 no Wokwi.

## Meus cenários conferidos

- Acionei e soltei o botão de pulsos. Conferi os pontos no gráfico, incluindo 420 BPM simulados na sequência 10 e 228 e 300 BPM nas sequências 13 e 14. Registrei o evento de limite didático ultrapassado.
- Deixei o botão solto. Conferi zero acionamentos nas sequências 16 e 17 e o evento de retorno dos pulsos à faixa definida. Não interpretei zero acionamentos como ausência de atividade cardíaca.
- Alterei a temperatura do DHT22 e conferi aproximadamente 44,3 °C a partir da sequência 17, com entrada do alerta de temperatura ambiente após duas leituras acima de 30 °C.
- Reduzi a temperatura e conferi duas leituras até 28 °C nas sequências 23 e 24. Observei o evento de retorno da temperatura à faixa definida.
- Na captura final, conferi a sequência 27 recebida e confirmada, 24,8 °C, umidade de 6,5%, zero pulsos e zero perdas.
- Conferi gráfico, gauge, tabela de leituras e histórico dos eventos. Mantive a distinção entre dados atuais, último valor recebido e conexão MQTT.

## Minhas evidências

Preservei três capturas: `01_alerta_pulsos.png`, `02_alerta_temperatura_retorno_pulsos.png` e `03_retorno_temperatura.png`. Elas mostram entrada e retorno dos alertas de pulsos e temperatura.

Consultei o SQLite em modo somente leitura e conferi 27 medições únicas das sequências 1 a 27, sem lacunas e com `dropped_total=0`. Preservei a extração em `leituras_1_a_27.json` e a conferência em `conferencia.json`. Cruzei os valores com as capturas; não apresentei as capturas isoladas como teste de persistência.

Concluí a validação visual e funcional da entrega Node-RED, complementando os testes locais, o ensaio de rede, a recuperação e a revisão de estabilidade já registrados nas pastas anteriores. Minha próxima entrega é o desafio REST com e-mail simulado. Ainda preciso concluir os demais desafios e os relatórios finais da Fase 3.
