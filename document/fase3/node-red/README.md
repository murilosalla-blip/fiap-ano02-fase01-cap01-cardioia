# Nosso painel Node-RED

Implementamos o dashboard da terceira entrega com Node-RED 5.0.9 e FlowFuse Dashboard 1.34.0. Mantivemos o consumidor Python da segunda entrega responsável por persistir as leituras e publicar os ACKs. No painel, assinamos telemetria, estado e confirmação do mesmo ESP32.

## Como reproduzir

Seguir primeiro a preparação no [guia da Fase 3](../README.md). Com `.venv` criado e os requisitos instalados, executar da raiz no PowerShell:

```powershell
$env:CARDIOIA_PYTHON = (Resolve-Path .\.venv\Scripts\python.exe).Path
node scripts/fase3/iniciar_dashboard.js --com-consumidor
```

Aguardar `Server now running` e `Started flows` no terminal; a linha inicial com o endereço antecede a conclusão do carregamento. Abrir o [painel](http://127.0.0.1:1880/dashboard/monitoramento) e utilizar o [Wokwi MQTT da Parte 2](https://wokwi.com/projects/478772789361460225). O projeto Serial da Parte 1 não alimenta o painel. Manter o terminal aberto e encerrar com Ctrl+C.

O comando inicia um consumidor. Se já houver um consumidor em outro terminal, iniciar apenas o painel, sem `--com-consumidor`. Não manter consumidores concorrentes no teste de ACK omitido. O guia principal apresenta os comandos completos para Windows e Linux/macOS.

Manter o Wokwi visível: em segundo plano observamos desaceleração do relógio simulado. Sinalizamos falta de atualização sem apresentar o último valor histórico como medição atual.

## O que exibimos

- Gráfico dos últimos 120 valores de BPM por sequência de coleta, com pontos azuis para leituras recuperadas.
- Gauge da temperatura ambiente do DHT22, com escala de −40 a 80 °C, e indicação de umidade.
- Última sequência recebida, última confirmação de gravação, perdas e tamanho da fila informado no envio.
- Histórico recente com temperatura, BPM, idade informada no envio e classificação da leitura.
- Aviso de atualização, recuperação, interrupção, indisponibilidade do sensor ou alerta didático.
- Histórico limitado de entrada e saída dos episódios de alerta.

Construímos gráfico e gauge em SVG dentro de um `ui-template` Vue do FlowFuse Dashboard. Assim, representamos ausência de dados ou sensor inválido com traço, sem converter esses casos em zero. Durante interrupções, mantemos a última medição válida recebida em cinza e marcamos sua falta de atualização; continuamos suspendendo os alertas atuais. O dashboard continua sendo servido pelo Node-RED e recebe suas mensagens diretamente do fluxo MQTT; não usamos uma página externa para substituir essa entrega.

## Regras que definimos

| Regra | Entrada | Saída |
|---|---|---|
| Pulsos simulados | Acima de 120 BPM em duas leituras atuais consecutivas | Até 108 BPM em duas leituras atuais consecutivas |
| Temperatura ambiente | Acima de 30 °C em duas leituras atuais consecutivas | Até 28 °C em duas leituras atuais consecutivas |

Escolhemos esses limites como parâmetros acadêmicos. Não interpretamos a temperatura ambiente como temperatura corporal. Zero pulsos representa ausência de acionamentos do botão naquela janela.

Consideramos elegível para os indicadores atuais uma leitura com `age_ms <= 10000` e `backlog_samples == 1`, recebida nos últimos 15 segundos, com conexão disponível. Os limites temporais são escolhas da implementação. Combinamos o tempo relativo informado pelo ESP32 com o intervalo local de recebimento; não alegamos conhecer uma data UTC exata de coleta.

Incluímos leituras antigas no histórico, mas suspendemos a avaliação atual durante a recuperação. Reenvios não adicionam pontos nem contam como novas janelas para confirmar um alerta. Ao interromper a conexão, suspendemos a condição de dado atual até receber uma nova leitura válida, preservando o último valor em cinza. Não registramos resolução de um alerta apenas porque faltaram dados.

## Como manter e importar o fluxo

Preparamos para versionamento `flows.json`, `painel.vue`, `monitor.js`, `settings.js`, os requisitos npm e o arquivo de versões travadas `package-lock.json`. Após editar o template ou a montagem do fluxo, regenerar o export:

```powershell
node .\src\fase3\node-red\gerar_fluxo.js
```

Podemos importar `flows.json` no editor em [Editor Node-RED](http://127.0.0.1:1880/editor/). Para reproduzir em outra instância, também instalamos o pacote FlowFuse Dashboard e carregamos `settings.js`, que disponibiliza `monitor.js` em `functionGlobalContext`. O export depende desses arquivos versionados; não é um JSON independente das regras do projeto.

Na inicialização, geramos uma cópia do fluxo em `.tools/runtime/fase3/node-red/`. Se editarmos pelo editor, exportamos nossas mudanças antes de reiniciar, pois o inicializador recria a cópia a partir dos arquivos versionados. Mantemos o histórico do painel em memória; a persistência das medições continua no SQLite do consumidor. Reiniciar o painel reinicia seu gráfico e não apaga o banco.

Vinculamos o serviço a `127.0.0.1`, com editor em `/editor` e painel em `/dashboard/monitoramento`. Para conferir o estado em testes, disponibilizamos a consulta local `/cardioia/api/state`; essa consulta não substitui o desafio REST da próxima entrega.

## Como verificar

```powershell
node --test src/fase3/tests/test_dashboard.cjs
```

Na primeira revisão, conferimos 15 testes de contrato, consistência, deduplicação, histerese, memória limitada, sensores inválidos, reconexão e ausência de dados recentes. Também executamos 12 cenários completos pelo broker em uma instância separada, usando mensagens fictícias identificadas como publicador Python.

Para reproduzir o ensaio de rede, iniciamos em outro terminal:

```powershell
$env:CARDIOIA_PORT = '1881'
$env:CARDIOIA_TOPIC_ROOT = 'cardioia/aura/fase3/dashboard-test/meu-ensaio'
node .\scripts\fase3\iniciar_dashboard.js
```

Em outro terminal, com as dependências Python disponíveis, executamos:

```powershell
.\.venv\Scripts\python.exe scripts/fase3/testar_dashboard_mqtt.py --topico cardioia/aura/fase3/dashboard-test/meu-ensaio --saida .tools/runtime/fase3/teste-dashboard
```

Ao encerrar o ensaio, pressionar Ctrl+C no terminal do servidor e fechar os terminais de teste para não reutilizar `CARDIOIA_PORT` e `CARDIOIA_TOPIC_ROOT` na demonstração principal.

Usamos diretório de execução e tópicos separados para não misturar esse ensaio com as medições do Wokwi. Não mantivemos o inicializador do consumidor integrado no modo de ensaio.

Registramos resultados e limitações em [Nossas evidências](../../other/fase3/evidencias/2026-10-24/dashboard/RESULTADOS.md). Concluímos a validação visual guiada e preservamos as capturas e a conferência do banco em [Nossa revisão final](../../other/fase3/evidencias/2026-10-24/dashboard/validacao_guiada/RESULTADOS.md).

## Referências que consultamos

- [Configuração do Node-RED](https://nodered.org/docs/user-guide/runtime/configuration)
- [FlowFuse Dashboard](https://dashboard.flowfuse.com/getting-started.html)
- [Widgets Vue no ui-template](https://dashboard.flowfuse.com/nodes/widgets/ui-template.html)

## Nossa revisão da exibição durante interrupções

Preservamos os últimos valores nos indicadores, com identificação de desatualização, em vez de fazê-los desaparecer a cada intervalo sem dados. Mantivemos a avaliação atual e os alertas separados desses valores históricos. Também explicitamos no gráfico quando todas as leituras registram zero acionamentos do botão. Para conferir simulador e painel simultaneamente, vamos manter as duas páginas em janelas separadas e visíveis; observamos desaceleração do Wokwi quando sua aba ficou em segundo plano.

## Nossa correção de estabilidade do simulador

Separamos conexão MQTT e atualidade dos dados. No cabeçalho, exibimos o estado real da conexão do Node-RED com o broker. No aviso principal, diferencio dispositivo offline, recuperação e espera por nova leitura. Não apresento uma leitura antiga como atual só porque o canal permanece conectado.

No firmware, configuramos keepalive MQTT de 300 segundos e espera de CONNACK de cinco segundos. O prazo anterior de 15 segundos era inadequado quando o relógio do Wokwi avançava mais devagar que o relógio real do broker. Esses valores são parâmetros da demonstração, não exigências do enunciado. Aumentar o keepalive também pode atrasar o Last Will em uma falha silenciosa; por isso mantemos a detecção independente de dados sem atualização após 15 segundos reais. A chave offline continua enviando seu estado explícito.

Passamos a conferir a consecutividade dos alertas pela sequência e pelas janelas de coleta no relógio do ESP32. Uma desaceleração do navegador não apaga a primeira janela válida. Uma lacuna de sequência, recuperação de histórico ou desconexão explícita interrompe essa confirmação. Leituras repetidas continuam sem contar como novas janelas.

Compilamos o firmware corrigido, salvamos no mesmo projeto público do Wokwi e executamos 19 testes locais com sucesso. Observamos a nova sessão por aproximadamente 101 segundos, com duas leituras e nenhuma interrupção de conexão. Também conferimos desconexão e reconexão reais pela chave. Preservamos esses registros em `document/other/fase3/evidencias/2026-10-24/dashboard/estabilidade/`.
