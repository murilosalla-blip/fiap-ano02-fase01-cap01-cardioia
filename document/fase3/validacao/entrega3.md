# Minha validação do painel Node-RED

## Como vou conferir a entrega

1. Vou iniciar painel e consumidor com `node .\scripts\fase3\iniciar_dashboard.js --com-consumidor` na pasta principal do projeto. Se já estiverem em execução, vou usar a instância existente.
2. Vou abrir `http://127.0.0.1:1880/dashboard/monitoramento` no Chrome e conferir o estado inicial sem dados atuais.
3. Vou executar o projeto MQTT do Wokwi, mover a chave para a direita e manter simulador e painel em duas janelas separadas e visíveis. Vou conferir no painel leituras, temperatura, gráfico e última confirmação.
4. Vou acionar o botão para produzir mais de dez pulsos em cada uma de duas janelas de cinco segundos. Vou conferir entrada do alerta acima de 120 BPM e permanência durante a condição.
5. Vou deixar de acionar o botão e conferir a saída após duas leituras até 108 BPM. Não vou interpretar zero pulsos como ausência de atividade cardíaca.
6. Vou alterar o DHT22 para 31 °C e aguardar duas leituras atuais. Depois vou ajustar para 28 °C ou menos e conferir a saída em duas leituras.
7. Vou mover a chave para a esquerda, observar a sinalização de falta de atualização, preservando o último valor recebido em cinza e manter a coleta. Depois vou reconectar e conferir os pontos recuperados no histórico, sem disparar um alerta atual com dados antigos.
8. Vou manter o consumidor e o painel ativos e parar o Wokwi. Vou conferir a interrupção pelo estado MQTT ou, na ausência dessa mensagem, pelo prazo de 15 segundos sem leitura atual.
9. Vou salvar as capturas finais e concluir minha revisão antes de avançar ao desafio REST/e-mail.

## O que já conferi na implementação

Conferi 15 testes locais e 12 cenários reais de rede em namespace isolado. Também recebi no painel leituras produzidas pelo ESP32 do Wokwi e cruzei suas confirmações com o consumidor. Registrei essa execução separadamente em `../../other/fase3/evidencias/2026-10-24/dashboard/RESULTADOS.md`.

Na inspeção inicial, interrompi a automação quando não consegui identificar com segurança a página ativa do navegador. Depois concluí a revisão visual guiada no Chrome, conferindo gráfico, gauge e entrada e retorno dos alertas de pulsos e temperatura. Preservei as capturas e a conferência de 27 medições únicas em `../../other/fase3/evidencias/2026-10-24/dashboard/validacao_guiada/RESULTADOS.md`.

## Minha revisão da estabilidade

Vou conferir o indicador do broker separadamente do aviso de atualidade. Com a chave à direita e simulação lenta, posso aguardar uma nova leitura sem interpretar isso como desconexão. Vou conferir interrupção pelo estado explícito da chave e manter a indicação de dado desatualizado após 15 segundos reais. Registrei a correção e sua observação de 101 segundos em `../../other/fase3/evidencias/2026-10-24/dashboard/estabilidade/RESULTADOS.md`.
