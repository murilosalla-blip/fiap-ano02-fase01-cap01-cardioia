# Nossa validação visual e funcional do painel

Concluímos a revisão da terceira entrega em 24/10/2026 no Chrome, com a sessão `546cb527f2cc13d5` do ESP32 no Wokwi.

## Nossos cenários conferidos

- Acionamos e soltamos o botão de pulsos. Conferimos os pontos no gráfico, incluindo 420 BPM simulados na sequência 10 e 228 e 300 BPM nas sequências 13 e 14. Registramos o evento de limite didático ultrapassado.
- Deixamos o botão solto. Conferimos zero acionamentos nas sequências 16 e 17 e o evento de retorno dos pulsos à faixa definida. Não interpretamos zero acionamentos como ausência de atividade cardíaca.
- Alteramos a temperatura do DHT22 e conferimos aproximadamente 44,3 °C a partir da sequência 17, com entrada do alerta de temperatura ambiente após duas leituras acima de 30 °C.
- Reduzi a temperatura e conferimos duas leituras até 28 °C nas sequências 23 e 24. Observamos o evento de retorno da temperatura à faixa definida.
- Na captura final, conferimos a sequência 27 recebida e confirmada, 24,8 °C, umidade de 6,5%, zero pulsos e zero perdas.
- Conferimos gráfico, gauge, tabela de leituras e histórico dos eventos. Mantivemos a distinção entre dados atuais, último valor recebido e conexão MQTT.

## Nossas evidências

Preservamos três capturas: `01_alerta_pulsos.png`, `02_alerta_temperatura_retorno_pulsos.png` e `03_retorno_temperatura.png`. Elas mostram entrada e retorno dos alertas de pulsos e temperatura.

Consultamos o SQLite em modo somente leitura e conferimos 27 medições únicas das sequências 1 a 27, sem lacunas e com `dropped_total=0`. Preservamos a extração em `leituras_1_a_27.json` e a conferência em `conferencia.json`. Cruzamos os valores com as capturas; não apresentamos as capturas isoladas como teste de persistência.

Concluímos a validação visual e funcional da entrega Node-RED, complementando os testes locais, o ensaio de rede, a recuperação e a revisão de estabilidade já registrados nas pastas anteriores. Nossa próxima entrega é o desafio REST com e-mail simulado. Ainda precisamos concluir os demais desafios e os relatórios finais da Fase 3.
