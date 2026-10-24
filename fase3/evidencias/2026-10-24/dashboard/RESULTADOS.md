# Minhas evidências do painel Node-RED

Implementei a terceira entrega em 24/10/2026 com Node-RED 5.0.9 e FlowFuse Dashboard 1.34.0. Preparei para versionamento o export em `fase3/node-red/flows.json`, o template Vue/SVG, as regras, as dependências e o inicializador. Mantenho o serviço apenas em `127.0.0.1`.

## Minhas verificações locais

Executei 15 testes Node.js com aprovação. Conferi contrato e BPM, DHT inválido, ausência de dados, bloqueio de telemetria retained, deduplicação, duas leituras consecutivas, histerese, supressão de alertas de replay, limite de memória, mudança de sessão, confirmação de identidade e reconexão sem reapresentar o valor anterior como atual.

Preparei também a execução desses testes no workflow de integração contínua. Não alego execução no GitHub nesta etapa.

## Meu ensaio real de rede, separado do ESP32

Iniciei uma segunda instância em `127.0.0.1:1881` e usei o tópico isolado `cardioia/aura/fase3/dashboard-test/20261024-1630`. Publiquei dados fictícios com Python e indiquei essa origem no painel. Não apresentei essas mensagens como leituras produzidas pelo ESP32.

Conferi 12 cenários: leitura atual; reenvio sem novo ponto; mensagem inválida; primeira leitura acima do limite sem confirmar alerta; segunda leitura com entrada do alerta; permanência na faixa de histerese; replay no histórico sem avaliação atual; saída após duas leituras; DHT indisponível; estado offline; reconexão; e ausência de dados atuais após 15 segundos.

Preservei os estados e a aprovação em `teste_rede_final/`. Mantive o primeiro ensaio em `teste_rede/` e a captura visual em `ensaio_painel.png`. Na captura, conferi gráfico, gauge, tabela e histórico de entrada e saída dos alertas. O cabeçalho identifica o publicador Python.

## Minha integração com o ESP32 do Wokwi

Executei o projeto MQTT no Chrome e mantive o consumidor ativo. Na sessão `31dd7dd8dfd544b0`, recebi no painel as sequências 1, 2 e 3 e conferi suas confirmações. Cruzei essas identidades com o SQLite: encontrei as três medições persistidas, sem lacunas nesse intervalo. Preservei o estado do painel em `estado_esp32.json`, os eventos do consumidor em `eventos_esp32.jsonl` e a consulta de persistência em `esp32_persistencia.json`.

Observei a simulação avançando muito lentamente em segundo plano, com indicação de aproximadamente 2% da velocidade nominal. Nessa condição, o painel retirou os valores atuais e sinalizou interrupção, preservando o histórico. Não tratei o histórico como condição atual.

## O que ainda vou revisar

Concluí implementação, testes de regras, ensaio de rede e recebimento de leituras reais do Wokwi. Ainda vou concluir a revisão visual guiada e as capturas finais do uso com o ESP32. Interrompi a inspeção visual automatizada quando não consegui identificar com segurança a página ativa do navegador. Preservei os resultados já conferidos, sem considerar essa inspeção concluída.

Vou seguir `fase3/validacao/entrega3.md` para revisar o painel antes de avançar ao desafio REST/e-mail. Não considero toda a Fase 3 concluída nesta entrega.

Conferi a inicialização pelo comando único com consumidor integrado: obtive HTTP 200 no painel, no editor e na consulta de estado, além de conexão e assinaturas ativas no consumidor. Registrei o resultado em `inicializacao.json`.

## Minha revisão dos valores durante interrupções

Ajustei somente o componente visual e apliquei a atualização sem reiniciar a sessão. Conferi a preservação das sete leituras existentes e observei a chegada da oitava. Mantive a última temperatura recebida, 24 °C, em cinza com o texto de falta de atualização; não a apresentei como condição atual. Acrescentei a explicação do histórico com zero pulsos. Preservei a conferência em `ajuste_ultimos_valores.json` e a captura em `painel_ultimos_valores.png`. Compilei o template e o componente Vue sem erros.

No simulador, observei a indicação de velocidade de 19% e reconexões MQTT entre algumas leituras. Não considerei a atualização visual como correção da desaceleração do navegador. Vou conferir a recepção mantendo Wokwi e painel em duas janelas visíveis.

## Minha correção posterior de estabilidade

Separei conexão MQTT de atualidade, ajustei os tempos do firmware e executei 19 testes locais. Conferi aproximadamente 101 segundos online, sem interrupção, e a desconexão/reconexão explícita pela chave. Preservei os resultados em [Minha correção de estabilidade](estabilidade/RESULTADOS.md). A captura `estabilidade/painel_conexao_estavel.png` mostra o canal conectado e o último valor identificado como desatualizado.

## Minha revisão final no Chrome

Concluí a revisão visual e funcional: conferi gráfico, gauge, entrada e retorno dos alertas de pulsos e temperatura, além de 27 medições únicas no banco. Preservei as capturas e os detalhes em [Minha validação guiada](validacao_guiada/RESULTADOS.md).
