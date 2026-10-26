# Estudo do CardioIA e plano para a Fase 3

> Registro histórico da etapa inicial. Preservamos o contexto e os resultados da época; para executar a versão atual, consultar o [guia da Fase 3](../../fase3/README.md).

Realizamos este estudo em 16/10/2026 com base nos enunciados locais das três fases, na documentação, nos resultados e em trechos da implementação. Durante esse estudo inicial, não executamos treinamentos, testes ou aplicações, nem verificamos as publicações externas. Consultamos os estados de conclusão das fases anteriores no repositório. Registramos as execuções posteriores separadamente em `document/other/fase3/evidencias/`.

## Conclusão

A próxima entrega deve acrescentar monitoramento contínuo simulado por IoT. A prioridade é implementar e demonstrar o ciclo ESP32 e sensores → fila offline → MQTT → Node-RED → visualização e alertas. O portal React e os modelos anteriores podem ser reaproveitados como contexto e pontos de acesso, mas não implementam esse ciclo atualmente.

O enunciado local informa entrega em 04/11/2026 às 23h59. A data deve ser conferida na plataforma acadêmica no fechamento da entrega.

## O que já desenvolvemos no projeto

O CardioIA é uma plataforma acadêmica desenvolvida em sete fases pelo Grupo Aura, com dados clínicos, NLP, imagens de ECG, IoT e integração futura dos módulos.

| Etapa | Evidências no repositório | Papel na continuidade |
|---|---|---|
| Fase 1 — dados numéricos | Cleveland, 303 registros e 14 variáveis, dados brutos/processados e dicionário | Base tabular histórica; não contém monitoramento temporal contínuo |
| Fase 1 — textos | Dois textos institucionais sobre prevenção e síndromes coronarianas | Referência documental para NLP |
| Fase 1 — imagens | 120 ECGs curados em quatro classes, manifesto e preparação | Base dos experimentos visuais |
| Fase 2 — extração | Dez relatos, 25 associações e extrator com normalização e heurística de negação | Demonstração de extração por regras |
| Fase 2 — classificação textual | 120 frases sintéticas, TF-IDF, regressão logística, separação por cenário | Pipeline reproduzível, com generalização limitada |
| Fase 2 — extensões | Modelo tabular e MLP visual, incluindo revisão de 491 imagens únicas | Experimentos independentes; não constituem fusão multimodal |
| Interfaces | Streamlit e portal React com pacientes, agenda e autenticação simulada | Continuidade visual e acesso aos módulos |
| Qualidade | Testes, notebooks, auditorias e workflows | Padrão de rastreabilidade a manter na fase seguinte |

O serviço do portal lê `public/data/patients.json`; o dashboard resume pacientes e consultas fictícios. No levantamento inicial, não encontramos implementação do ciclo ESP32/MQTT/Node-RED nos arquivos de código inventariados. Os sinais temporais da Fase 3 precisarão ser produzidos pela nova simulação: uma linha clínica da base Cleveland não equivale a uma série de leituras de sensor.

## Requisitos obrigatórios da Fase 3

| Bloco | O que implementar | Evidência de entrega |
|---|---|---|
| Sensores | ESP32 no Wokwi, com pelo menos dois sensores distintos; DHT22 obrigatório e outro à escolha | Link do Wokwi e C++ comentado |
| Edge | Coleta periódica, conectividade simulada por booleano, armazenamento limitado e sincronização após reconexão | Demonstração de queda/retorno e relatório de pelo menos uma página |
| MQTT | Envio efetivo de dados do ESP32 ao broker | Código, configuração documentada e mensagens recebidas |
| Node-RED | Dashboard em tempo real com gráfico, gauge e alerta automático por limites escolhidos | Prints ou export do dashboard; preferencialmente ambos |
| Comunicação | Explicação do fluxo MQTT e configuração do dashboard | Relatório de pelo menos duas páginas |

Cada critério vale dois pontos: sensores, resiliência offline, MQTT, dashboard/alertas e documentação.

O enunciado aceita uma alternativa demonstrativa pelo Monitor Serial devido às limitações do simulador. SPIFFS é opcional e não será computado como obrigatório; hardware físico não é exigido. Não confundir essa dispensa com dispensa de resiliência: é necessário demonstrar coleta durante a indisponibilidade e recuperação dos dados pendentes. Serial atende à demonstração prevista na Parte 1; a Parte 2 exige transmissão MQTT real.

Grafana é opcional. React não substitui a entrega solicitada em Node-RED.

## Arquitetura proposta para a equipe

Escolhemos DHT22 e um botão para simular pulsos cardíacos, conforme exemplo permitido no enunciado. Vamos identificar os eventos do botão como batimentos artificiais e a leitura do DHT22 como temperatura do sensor/ambiente simulado, sem alegar medição fisiológica ou temperatura corporal validada.

1. ESP32 coleta temperatura/umidade e conta pulsos com tratamento de repique do botão.
2. Cada amostra recebe versão do formato, identificador fictício do dispositivo, identificador da sessão, sequência, instante de coleta ou tempo desde inicialização, unidades e indicadores de validade.
3. Uma fila limitada mantém as amostras enquanto a conectividade simulada ou o broker estiver indisponível.
4. Na reconexão, o dispositivo transmite pendências de forma controlada sem interromper a coleta.
5. Node-RED valida mensagens, reconhece amostras repetidas e distingue horário da coleta do horário de recebimento.
6. Dashboard apresenta histórico, gauge, estado da conexão, dados desatualizados e alertas demonstrativos.

Planejamos dimensionar a fila a partir do intervalo, do tamanho real da amostra e da memória disponível. Calculamos que uma amostra a cada cinco segundos produz 720 amostras/hora e que 2.000 amostras cobrem cerca de 2h47min. Na primeira implementação, medimos o consumo, adotamos esse limite e documentamos o descarte das novas leituras quando a fila enche, com contagem de perdas em `document/other/fase3/evidencias/entrega1_resultados.md`.

Não vamos apagar uma pendência apenas porque tentamos enviá-la. Vamos definir o que confirma sua entrega e documentar a garantia obtida com a biblioteca e o protocolo escolhidos. Vamos incluir confirmação pela aplicação e simular falha do broker além do booleano de Wi-Fi. Vamos declarar no relatório que a fila em memória não preserva leituras após reinício.

Vamos separar os limites didáticos de alerta dos classificadores da Fase 2. Esses modelos não foram treinados para receber diretamente temperatura e batimentos em sequência. Não vamos associar uma leitura isolada à previsão tabular sem conferir a compatibilidade das variáveis e realizar avaliação específica.

## Desafios Ir Além

### Ir Além 1 — REST e e-mail

Vamos implementar um cliente Python com envio e recebimento HTTP, verificação de riscos demonstrativos e simulação de disparo de e-mail. Vamos entregar o código e um relatório de uma a duas páginas, reutilizar o formato de telemetria e registrar a simulação do e-mail. Também vamos tratar a repetição de alertas para uma mesma ocorrência.

### Ir Além 2 — séries temporais e neuromorfismo

Comparar classificador tradicional com modelo neuromórfico simples LIF ou FHN. Entregar notebook comentado, código/README público, relatório comparativo de duas páginas e vídeo de até quatro minutos no YouTube como não listado, linkado no README.

Antes de treinar, vamos definir o alvo e a saída de previsão do modelo neuromórfico. Vamos gerar ou selecionar séries com origem e rótulos documentados, separar sessões ou dispositivos independentes e impedir que janelas sobrepostas atravessem treino e teste. Vamos comparar os modelos no mesmo problema e nas mesmas divisões. Não vamos inferir eficiência energética de hardware apenas pelo tempo de execução em Python.

## Feedback da Fase 2 e dívida de evolução

O enunciado local da Fase 2 contém nota 9 e feedback publicado em 15/10/2026. O professor reconhece organização, reprodutibilidade, análise crítica e os dois desafios extras. Aponta diversidade textual, negação/contexto, ampliação do mapa, validação independente, vieses e falsos negativos no ECG como oportunidades.

Parte da negação já está tratada em `mencoes_afirmadas`, mas a própria implementação limita temporalidade e contexto de terceiros. Essa correção do extrator não corrige automaticamente o classificador TF-IDF. A sondagem registrada tem 16 entradas e quatro casos sem vocabulário; não é validação externa. A acurácia textual de 100% em 24 frases sintéticas não demonstra robustez clínica.

No ECG, distinguir acurácia comum de acurácia balanceada: o feedback cita 69,7% de acurácia e 62,9% de recall anormal; a documentação destaca 74,5% de acurácia balanceada. Não tratar esses números como a mesma métrica. Hashes distintos eliminam duplicatas exatas, mas não garantem pacientes distintos.

Vamos manter essas melhorias em um backlog próprio e priorizar na Fase 3 a integridade temporal, a prevenção de perdas silenciosas, a conexão, os alertas e as evidências de funcionamento.

## Sequência de execução sugerida

| Período sugerido | Resultado esperado |
|---|---|
| 16–18/10 | Requisitos rastreados, formato da mensagem, sensores e divisão de responsabilidades definidos |
| 19–23/10 | Wokwi com leituras e fila offline; comunicação MQTT ponta a ponta |
| 24–27/10 | Dashboard Node-RED e cenários de desconexão, reconexão, alerta e fila cheia |
| 28–31/10 | Desafios Ir Além 1 e 2, incluídos no escopo completo acordado; consolidação dos relatórios |
| 01–03/11 | Reprodução por outro integrante, evidências, links públicos e revisão final |
| 04/11 | Entrega com margem para problemas de upload |

Vamos organizar as frentes de firmware/Edge, MQTT/Node-RED e integração/testes/documentação. Vamos combinar as responsabilidades com a equipe e manter o contrato de mensagens compartilhado para revisão cruzada.

Organizamos a execução em `document/fase3/ROTEIRO_ENTREGA.md`, incluindo a entrega obrigatória e os dois desafios Ir Além em seis etapas de implementação e revisão.

Planejamos organizar os arquivos em `src/fase3/firmware/`, `src/fase3/node-red/`, `src/fase3/python/`, `fase3/notebooks/`, `src/fase3/tests/`, `document/other/fase3/evidencias/`, `fase3/relatorios/`, `document/fase3/README.md` e `document/fase3/CHECKLIST_ENUNCIADO.md`. Vamos versionar configurações de exemplo sem credenciais e preservar as entregas anteriores. Antes de alterar o portal, vamos registrar seu repositório de origem oficial, pois encontramos uma cópia local e um repositório separado documentado.

## Critérios para considerar a entrega pronta

- Dois sensores distintos aparecem e funcionam na simulação; leituras inválidas não geram valores normais inventados.
- Dashboard recebe e exibe dados enviados por MQTT pelo ESP32.
- Durante falha de conexão, a coleta continua e o backlog aumenta.
- Na recuperação, o backlog é transmitido com ordem/identificação verificáveis e sem duplicar o histórico exibido.
- Fila cheia tem comportamento documentado e contagem de perdas.
- Alertas são ativados e encerrados conforme as regras demonstrativas e dados atrasados são identificados.
- Link do Wokwi, firmware, export do Node-RED, evidências e relatórios estão acessíveis e reproduzíveis por outro integrante.
- README distingue escopo obrigatório, extras, dados simulados e limitações.

## Fontes locais consultadas

- `document/other/referencias/fase1/enunciado/Fase 1_Cap 1_Exercício.docx`
- `document/other/referencias/fase2/enunciado/Fase 2_Cap 1_Exercício.docx`, incluindo feedback
- `document/other/referencias/fase3/enunciado/Fase 3_Cap 1_Exercício.docx`
- `README.md`, `document/ai_project_document_fiap.md`
- `document/fase2/README.md`, `document/fase2/RELATORIO_ENTREGA.md`, `document/fase2/CHECKLIST_ENUNCIADO.md`
- `src/fase2/src/extrair_sintomas.py`, `assets/fase2/resultados/nlp/revisao/resumo_sondagem.json`, `document/other/fase2/auditoria/bloco2_negacao_e_regressao.md`
- `src/fase2/portal-cardioia/src/services/api.js`, `src/fase2/portal-cardioia/src/pages/Dashboard.jsx`, `src/fase2/portal-cardioia/package.json`
