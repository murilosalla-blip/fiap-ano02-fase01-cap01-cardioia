# Nossas evidências do painel Node-RED

Implementamos a terceira entrega em 24/10/2026 com Node-RED 5.0.9 e FlowFuse Dashboard 1.34.0. Preparamos para versionamento o export em `src/fase3/node-red/flows.json`, o template Vue/SVG, as regras, as dependências e o inicializador. Mantemos o serviço apenas em `127.0.0.1`.

## Nossas verificações locais

Executamos 15 testes Node.js com aprovação. Conferimos contrato e BPM, DHT inválido, ausência de dados, bloqueio de telemetria retained, deduplicação, duas leituras consecutivas, histerese, supressão de alertas de replay, limite de memória, mudança de sessão, confirmação de identidade e reconexão sem reapresentar o valor anterior como atual.

Preparamos também a execução desses testes no workflow de integração contínua. Não alegamos execução no GitHub nesta etapa.

## Nosso ensaio real de rede, separado do ESP32

Iniciamos uma segunda instância em `127.0.0.1:1881` e usamos o tópico isolado `cardioia/aura/fase3/dashboard-test/20261024-1630`. Publicamos dados fictícios com Python e indiquamos essa origem no painel. Não apresentamos essas mensagens como leituras produzidas pelo ESP32.

Conferimos 12 cenários: leitura atual; reenvio sem novo ponto; mensagem inválida; primeira leitura acima do limite sem confirmar alerta; segunda leitura com entrada do alerta; permanência na faixa de histerese; replay no histórico sem avaliação atual; saída após duas leituras; DHT indisponível; estado offline; reconexão; e ausência de dados atuais após 15 segundos.

Preservamos os estados e a aprovação em `teste_rede_final/`. Mantivemos o primeiro ensaio em `teste_rede/` e a captura visual em `ensaio_painel.png`. Na captura, conferimos gráfico, gauge, tabela e histórico de entrada e saída dos alertas. O cabeçalho identifica o publicador Python.

## Nossa integração com o ESP32 do Wokwi

Executamos o projeto MQTT no Chrome e mantivemos o consumidor ativo. Na sessão `31dd7dd8dfd544b0`, recebemos no painel as sequências 1, 2 e 3 e conferimos suas confirmações. Cruzamos essas identidades com o SQLite: encontramos as três medições persistidas, sem lacunas nesse intervalo. Preservamos o estado do painel em `estado_esp32.json`, os eventos do consumidor em `eventos_esp32.jsonl` e a consulta de persistência em `esp32_persistencia.json`.

Observamos a simulação avançando muito lentamente em segundo plano, com indicação de aproximadamente 2% da velocidade nominal. Nessa condição, o painel retirou os valores atuais e sinalizou interrupção, preservando o histórico. Não tratamos o histórico como condição atual.

## O que ainda vamos revisar

Concluímos implementação, testes de regras, ensaio de rede e recebimento de leituras reais do Wokwi. Ainda vamos concluir a revisão visual guiada e as capturas finais do uso com o ESP32. Interrompemos a inspeção visual automatizada quando não conseguimos identificar com segurança a página ativa do navegador. Preservamos os resultados já conferidos, sem considerar essa inspeção concluída.

Vamos seguir `document/fase3/validacao/entrega3.md` para revisar o painel antes de avançar ao desafio REST/e-mail. Não consideramos toda a Fase 3 concluída nesta entrega.

Conferimos a inicialização pelo comando único com consumidor integrado: obtivemos HTTP 200 no painel, no editor e na consulta de estado, além de conexão e assinaturas ativas no consumidor. Registramos o resultado em `inicializacao.json`.

## Nossa revisão dos valores durante interrupções

Ajustamos somente o componente visual e aplicamos a atualização sem reiniciar a sessão. Conferimos a preservação das sete leituras existentes e observamos a chegada da oitava. Mantivemos a última temperatura recebida, 24 °C, em cinza com o texto de falta de atualização; não a apresentamos como condição atual. Acrescentamos a explicação do histórico com zero pulsos. Preservamos a conferência em `ajuste_ultimos_valores.json` e a captura em `painel_ultimos_valores.png`. Compilamos o template e o componente Vue sem erros.

No simulador, observamos a indicação de velocidade de 19% e reconexões MQTT entre algumas leituras. Não consideramos a atualização visual como correção da desaceleração do navegador. Vamos conferir a recepção mantendo Wokwi e painel em duas janelas visíveis.

## Nossa correção posterior de estabilidade

Separamos conexão MQTT de atualidade, ajustamos os tempos do firmware e executamos 19 testes locais. Conferimos aproximadamente 101 segundos online, sem interrupção, e a desconexão/reconexão explícita pela chave. Preservamos os resultados em [Nossa correção de estabilidade](estabilidade/RESULTADOS.md). A captura `estabilidade/painel_conexao_estavel.png` mostra o canal conectado e o último valor identificado como desatualizado.

## Nossa revisão final no Chrome

Concluímos a revisão visual e funcional: conferimos gráfico, gauge, entrada e retorno dos alertas de pulsos e temperatura, além de 27 medições únicas no banco. Preservamos as capturas e os detalhes em [Nossa validação guiada](validacao_guiada/RESULTADOS.md).
