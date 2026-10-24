# Meu painel Node-RED

Implementei o dashboard da terceira entrega com Node-RED 5.0.9 e FlowFuse Dashboard 1.34.0. Mantive o consumidor Python da segunda entrega responsável por persistir as leituras e publicar os ACKs. No painel, assino telemetria, estado e confirmação do mesmo ESP32.

## Como inicio

Na pasta principal do projeto, uso Node.js 24 e Python 3.12. Para preparar uma nova cópia, executo:

```powershell
npm ci --prefix src/fase3/node-red --ignore-scripts --no-audit --no-fund
python -m pip install -r config/fase3/requirements-mqtt.txt
```

Depois, inicio painel e consumidor juntos:

```powershell
node .\scripts\fase3\iniciar_dashboard.js --com-consumidor
```

Na instalação local já preparada, aproveito as dependências Python de `.tools/python-mqtt`. Em uma cópia limpa, instalo o arquivo de requisitos acima. Posso selecionar outro executável Python pela variável `CARDIOIA_PYTHON`.

Abro [meu painel](http://127.0.0.1:1880/dashboard/monitoramento) no navegador. Mantenho o terminal aberto e encerro com Ctrl+C. O comando encerra também os processos filhos. Se eu já mantiver o consumidor em outro terminal, inicio somente o painel com `node .\scripts\fase3\iniciar_dashboard.js`.

Mantenho a aba do Wokwi ativa durante a simulação: em segundo plano, observei o relógio do simulador avançar a aproximadamente 2% da velocidade nominal, com intervalos longos entre as leituras. Nessa situação, meu painel sinaliza corretamente a falta de dados recentes. Não aumento artificialmente a validade dos dados para esconder a interrupção.

## O que exibo

- Gráfico dos últimos 120 valores de BPM por sequência de coleta, com pontos azuis para leituras recuperadas.
- Gauge da temperatura ambiente do DHT22, com escala de −40 a 80 °C, e indicação de umidade.
- Última sequência recebida, última confirmação de gravação, perdas e tamanho da fila informado no envio.
- Histórico recente com temperatura, BPM, idade informada no envio e classificação da leitura.
- Aviso de atualização, recuperação, interrupção, indisponibilidade do sensor ou alerta didático.
- Histórico limitado de entrada e saída dos episódios de alerta.

Construí gráfico e gauge em SVG dentro de um `ui-template` Vue do FlowFuse Dashboard. Assim, representei ausência de dados ou sensor inválido com traço, sem converter esses casos em zero. Durante interrupções, mantenho a última medição válida recebida em cinza e marco sua falta de atualização; continuo suspendendo os alertas atuais. O dashboard continua sendo servido pelo Node-RED e recebe suas mensagens diretamente do fluxo MQTT; não usei uma página externa para substituir essa entrega.

## Regras que defini

| Regra | Entrada | Saída |
|---|---|---|
| Pulsos simulados | Acima de 120 BPM em duas leituras atuais consecutivas | Até 108 BPM em duas leituras atuais consecutivas |
| Temperatura ambiente | Acima de 30 °C em duas leituras atuais consecutivas | Até 28 °C em duas leituras atuais consecutivas |

Escolhi esses limites como parâmetros acadêmicos. Não interpreto a temperatura ambiente como temperatura corporal. Zero pulsos representa ausência de acionamentos do botão naquela janela.

Considero elegível para os indicadores atuais uma leitura com `age_ms <= 10000` e `backlog_samples == 1`, recebida nos últimos 15 segundos, com conexão disponível. Os limites temporais são escolhas da implementação. Combino o tempo relativo informado pelo ESP32 com o intervalo local de recebimento; não alego conhecer uma data UTC exata de coleta.

Incluo leituras antigas no histórico, mas suspendo a avaliação atual durante a recuperação. Reenvios não adicionam pontos nem contam como novas janelas para confirmar um alerta. Ao interromper a conexão, retiro os valores atuais até receber uma nova leitura válida. Não registro resolução de um alerta apenas porque faltaram dados.

## Como mantenho e importo o fluxo

Preparei para versionamento `flows.json`, `painel.vue`, `monitor.js`, `settings.js`, os requisitos npm e o arquivo de versões travadas `package-lock.json`. Após editar o template ou a montagem do fluxo, regenero o export:

```powershell
node .\src\fase3\node-red\gerar_fluxo.js
```

Posso importar `flows.json` no editor em [Editor Node-RED](http://127.0.0.1:1880/editor/). Para reproduzir em outra instância, também instalo o pacote FlowFuse Dashboard e carrego `settings.js`, que disponibiliza `monitor.js` em `functionGlobalContext`. O export depende desses arquivos versionados; não é um JSON independente das regras do projeto.

Na inicialização, gero uma cópia do fluxo em `.tools/runtime/fase3/node-red/`. Se eu editar pelo editor, exporto minhas mudanças antes de reiniciar, pois o inicializador recria a cópia a partir dos arquivos versionados. Mantenho o histórico do painel em memória; a persistência das medições continua no SQLite do consumidor. Reiniciar o painel reinicia seu gráfico e não apaga o banco.

Vinculei o serviço a `127.0.0.1`, com editor em `/editor` e painel em `/dashboard/monitoramento`. Para conferir o estado em testes, disponibilizei a consulta local `/cardioia/api/state`; essa consulta não substitui o desafio REST da próxima entrega.

## Como conferi

```powershell
node --test src/fase3/tests/test_dashboard.cjs
```

Conferi 15 testes de contrato, consistência, deduplicação, histerese, memória limitada, sensores inválidos, reconexão e ausência de dados recentes. Também executei 12 cenários completos pelo broker em uma instância separada, usando mensagens fictícias identificadas como publicador Python.

Para reproduzir o ensaio de rede, inicio em outro terminal:

```powershell
$env:CARDIOIA_PORT = '1881'
$env:CARDIOIA_TOPIC_ROOT = 'cardioia/aura/fase3/dashboard-test/meu-ensaio'
node .\scripts\fase3\iniciar_dashboard.js
```

Em outro terminal, com as dependências Python disponíveis, executo:

```powershell
python scripts/fase3/testar_dashboard_mqtt.py --topico cardioia/aura/fase3/dashboard-test/meu-ensaio --saida .tools/runtime/fase3/teste-dashboard
```

Usei diretório de execução e tópicos separados para não misturar esse ensaio com as medições do Wokwi. Não mantive o inicializador do consumidor integrado no modo de ensaio.

Registrei resultados e limitações em [Minhas evidências](../../other/fase3/evidencias/2026-10-24/dashboard/RESULTADOS.md). Concluí a validação visual guiada e preservei as capturas e a conferência do banco em [Minha revisão final](../../other/fase3/evidencias/2026-10-24/dashboard/validacao_guiada/RESULTADOS.md).

## Referências que consultei

- [Configuração do Node-RED](https://nodered.org/docs/user-guide/runtime/configuration)
- [FlowFuse Dashboard](https://dashboard.flowfuse.com/getting-started.html)
- [Widgets Vue no ui-template](https://dashboard.flowfuse.com/nodes/widgets/ui-template.html)

## Minha revisão da exibição durante interrupções

Preservei os últimos valores nos indicadores, com identificação de desatualização, em vez de fazê-los desaparecer a cada intervalo sem dados. Mantive a avaliação atual e os alertas separados desses valores históricos. Também explicitei no gráfico quando todas as leituras registram zero acionamentos do botão. Para conferir simulador e painel simultaneamente, vou manter as duas páginas em janelas separadas e visíveis; observei desaceleração do Wokwi quando sua aba ficou em segundo plano.

## Minha correção de estabilidade do simulador

Separei conexão MQTT e atualidade dos dados. No cabeçalho, exibo o estado real da conexão do Node-RED com o broker. No aviso principal, diferencio dispositivo offline, recuperação e espera por nova leitura. Não apresento uma leitura antiga como atual só porque o canal permanece conectado.

No firmware, configurei keepalive MQTT de 300 segundos e espera de CONNACK de cinco segundos. O prazo anterior de 15 segundos era inadequado quando o relógio do Wokwi avançava mais devagar que o relógio real do broker. Esses valores são parâmetros da demonstração, não exigências do enunciado. Aumentar o keepalive também pode atrasar o Last Will em uma falha silenciosa; por isso mantenho a detecção independente de dados sem atualização após 15 segundos reais. A chave offline continua enviando seu estado explícito.

Passei a conferir a consecutividade dos alertas pela sequência e pelas janelas de coleta no relógio do ESP32. Uma desaceleração do navegador não apaga a primeira janela válida. Uma lacuna de sequência, recuperação de histórico ou desconexão explícita interrompe essa confirmação. Leituras repetidas continuam sem contar como novas janelas.

Compilei o firmware corrigido, salvei no mesmo projeto público do Wokwi e executei 19 testes locais com sucesso. Observei a nova sessão por aproximadamente 101 segundos, com duas leituras e nenhuma interrupção de conexão. Também conferi desconexão e reconexão reais pela chave. Preservei esses registros em `document/other/fase3/evidencias/2026-10-24/dashboard/estabilidade/`.
