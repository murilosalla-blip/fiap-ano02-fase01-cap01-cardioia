# Nossa validação do painel Node-RED

## Como vamos conferir a entrega

1. Vamos iniciar painel e consumidor com `node .\scripts\fase3\iniciar_dashboard.js --com-consumidor` na pasta principal do projeto. Se já estiverem em execução, vamos usar a instância existente.
2. Vamos abrir `http://127.0.0.1:1880/dashboard/monitoramento` no Chrome e conferir o estado inicial sem dados atuais.
3. Vamos executar o projeto MQTT do Wokwi, mover a chave para a direita e manter simulador e painel em duas janelas separadas e visíveis. Vamos conferir no painel leituras, temperatura, gráfico e última confirmação.
4. Vamos acionar o botão para produzir mais de dez pulsos em cada uma de duas janelas de cinco segundos. Vamos conferir entrada do alerta acima de 120 BPM e permanência durante a condição.
5. Vamos deixar de acionar o botão e conferir a saída após duas leituras até 108 BPM. Não vamos interpretar zero pulsos como ausência de atividade cardíaca.
6. Vamos alterar o DHT22 para 31 °C e aguardar duas leituras atuais. Depois vamos ajustar para 28 °C ou menos e conferir a saída em duas leituras.
7. Vamos mover a chave para a esquerda, observar a sinalização de falta de atualização, preservando o último valor recebido em cinza e manter a coleta. Depois vamos reconectar e conferir os pontos recuperados no histórico, sem disparar um alerta atual com dados antigos.
8. Vamos manter o consumidor e o painel ativos e parar o Wokwi. Vamos conferir a interrupção pelo estado MQTT ou, na ausência dessa mensagem, pelo prazo de 15 segundos sem leitura atual.
9. Vamos salvar as capturas finais e concluir nossa revisão antes de avançar ao desafio REST/e-mail.

## O que já conferimos na implementação

Conferimos 15 testes locais e 12 cenários reais de rede em namespace isolado. Também recebemos no painel leituras produzidas pelo ESP32 do Wokwi e cruzamos suas confirmações com o consumidor. Registramos essa execução separadamente em `../../other/fase3/evidencias/2026-10-24/dashboard/RESULTADOS.md`.

Na inspeção inicial, interrompemos a automação quando não conseguimos identificar com segurança a página ativa do navegador. Depois concluímos a revisão visual guiada no Chrome, conferindo gráfico, gauge e entrada e retorno dos alertas de pulsos e temperatura. Preservamos as capturas e a conferência de 27 medições únicas em `../../other/fase3/evidencias/2026-10-24/dashboard/validacao_guiada/RESULTADOS.md`.

## Nossa revisão da estabilidade

Vamos conferir o indicador do broker separadamente do aviso de atualidade. Com a chave à direita e simulação lenta, podemos aguardar uma nova leitura sem interpretar isso como desconexão. Vamos conferir interrupção pelo estado explícito da chave e manter a indicação de dado desatualizado após 15 segundos reais. Registramos a correção e sua observação de 101 segundos em `../../other/fase3/evidencias/2026-10-24/dashboard/estabilidade/RESULTADOS.md`.
