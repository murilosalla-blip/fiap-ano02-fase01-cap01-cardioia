# Validação visual acompanhada - 27/10/2026

Reiniciamos o Wokwi, colocamos a chave online e acionamos o botão de pulsos durante a validação acompanhada. Conferimos o painel no Chrome e cruzamos a sessão `66d5bec5f7007c6a` com o SQLite do consumidor.

Confirmamos conexão MQTT, leituras atuais, avanço da leitura e da confirmação, gráfico com pulsos artificiais e zero perdas informadas. A sequência 2 registrou 24 pulsos em 5.000 ms, correspondentes a 288 BPM; a sequência 3 registrou três pulsos, correspondentes a 36 BPM. As sete leituras da consulta preservada são únicas, sequências 1 a 7. A captura posterior mostra a leitura e a confirmação 8.

- [Estado consultado](estado_pulsos.json).
- [Leituras persistidas](leituras_pulsos.json).
- [Captura do painel no Chrome](painel_pulsos.png).

Não houve evento de alerta nesta sessão no momento da consulta. O pico acima de 120 BPM ocorreu em uma leitura isolada; a seguinte ficou abaixo do limite. Esse resultado é compatível com a confirmação em duas leituras consecutivas.

Ainda não comprovamos nesta sessão duas leituras consecutivas acima do limite, entrada/retorno do alerta de temperatura ou recuperação após mover a chave offline/online. A temperatura permaneceu em 24 °C e as leituras consultadas não apresentaram replay. Vamos registrar esses cenários somente após observá-los, sem confundir o ensaio de rede isolado com o ESP32.

## Entrada do alerta de pulsos

Continuamos os acionamentos na mesma sessão. Conferimos 192 BPM na sequência 14 e 168 BPM na 15, seguidas de outras leituras acima do limite. O painel registrou o evento “Pulsos simulados: limite didático ultrapassado”. Na sequência 19, recebemos 48 BPM, iniciando a confirmação de retorno; ainda aguardávamos uma segunda leitura baixa no momento desse registro.

- [Estado com alerta ativo](alerta_pulsos_estado.json).
- [Leituras persistidas até a sequência 19](alerta_pulsos_leituras.json).

Esta observação sucede a captura inicial de pulsos isolados e comprova a entrada do alerta. A temperatura e a recuperação offline ainda não foram validadas nesta sessão.

## Retorno do alerta de pulsos

Após parar os acionamentos, conferimos a leitura 19 com 48 BPM e as seguintes com zero pulsos. O painel registrou “Pulsos simulados: retorno à faixa definida”, retirou o alerta ativo e manteve o histórico. A consulta preservada já alcançava a sequência 21; a captura visual posterior mostra leitura e confirmação 22, com zero perdas.

- [Estado com retorno confirmado](retorno_pulsos_estado.json).
- [Captura após o retorno](painel_retorno_pulsos.png).

Concluímos a entrada e o retorno do alerta de pulsos nesta sessão. Prosseguimos com temperatura ambiente e interrupção/recuperação, ainda pendentes nesta repetição.

## Entrada e retorno do alerta de temperatura

Alteramos o DHT22 na mesma sessão. Os valores efetivamente registrados foram aproximadamente 40,9 °C nas sequências 25 a 29 e 11,2 °C nas sequências 30 a 32, em vez dos valores de exemplo de 31 e 28 °C. Eles cruzam os mesmos limites definidos: entrada acima de 30 °C e retorno até 28 °C.

Conferimos os eventos “Temperatura ambiente: limite didático ultrapassado” e “Temperatura ambiente: retorno à faixa definida”. Na consulta da sequência 32, o alerta estava encerrado, a confirmação correspondia à leitura 32 e as perdas informadas continuavam em zero. O gauge no Chrome mostrou 11,2 °C.

- [Estado após retorno da temperatura](temperatura_estado.json).
- [Leituras até a sequência 32](temperatura_leituras.json).
- [Captura do medidor e do histórico](painel_temperatura.png).

Concluímos os testes de sensores e entrada/retorno dos dois alertas. A interrupção pela chave e a recuperação MQTT ainda precisam ser observadas nesta repetição guiada.

## Interrupção e recuperação - validação concluída

Movemos a chave à esquerda, mantivemos a simulação ligada e aguardamos o acúmulo. Ao voltar à direita, conferimos no Serial os ACKs das sequências 35 a 39 e o esvaziamento da fila na confirmação 39. As confirmações 40 a 43 também mostraram fila zero. A coleta continuou durante a recuperação.

Na consulta preservada, encontramos 41 medições únicas, sequências 1 a 41, sem lacunas, na mesma sessão. Os eventos stored ocorreram nessa ordem. Todas informaram zero perdas. As sequências 35 e 36 chegaram com replay=true, idades de 19.248 e 14.532 ms; as 37 e 38 ainda apresentaram fila acima de uma posição e foram classificadas como recuperadas pelo painel. O histórico preservou essas amostras e voltou a receber leituras atuais. A captura posterior mostra leitura e confirmação 42.

- [Estado após recuperação](recuperacao_estado.json).
- [Leituras persistidas até 41](recuperacao_leituras.json).
- [Eventos MQTT da sessão](recuperacao_eventos.json).
- [Coletas, conexão e ACKs observados no Serial](serial_recuperacao.txt).
- [Captura do painel após recuperação](painel_recuperacao.png).
- [Conferência final dos dados](conferencia_final.json).

**Conclusão da repetição acompanhada:** conferimos conexão, coleta e confirmação, gráfico de pulsos, entrada e retorno dos dois alertas, mudança de temperatura, interrupção pela chave e recuperação ordenada sem perdas. A operação dos controles foi acompanhada, com conferência da tela no Chrome, do Serial, dos eventos e do SQLite; não apresentamos a execução como uma automação autônoma integral. Esta conclusão sucede as pendências intermediárias registradas acima e não representa submissão na FIAP.
