# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%"></a>
</p>

<br>

# CardioIA — Fases 1, 2 e 3

## Grupo Aura

## 👨‍🎓 Integrantes:

- Murilo Salla — RM568041
- Elias da Silva de Souza — RM568500
- Julia Duarte de Carvalho — RM567816

## 👩‍🏫 Professores:

### Tutor(a)

- Leonardo Ruiz Orabona

### Coordenador(a)

- André Godoi Chiovato

## 📜 Descrição

Desenvolvemos o **CardioIA** como projeto acadêmico da FIAP ao longo de 7 fases. Na **Fase 1 — "Batimentos de Dados: Mapeando o Coração Moderno"**, reunimos dados numéricos, textuais e visuais. Na **Fase 2 — Machine Learning**, desenvolvemos extração de sintomas, classificação textual com TF-IDF, portal React e experimentos tabulares e visuais. Na **Fase 3 — Monitoramento Contínuo: IoT na Saúde**, acrescentamos captura simulada com ESP32, resiliência offline, transmissão MQTT e visualização no Node-RED, mantendo a evolução das entregas anteriores.

> **Uso exclusivamente educacional.** Não realizamos diagnóstico, não estimamos risco clínico real e não substituímos avaliação médica.

O repositório está disponível em [github.com/murilosalla-blip/fiap-ano02-fase03-cardioia](https://github.com/murilosalla-blip/fiap-ano02-fase03-cardioia).

**Parte 1 — Dados Numéricos:**utilizamos o dataset público *Heart Disease (Cleveland)*, do UCI Machine Learning Repository (303 registros, 14 variáveis clínicas — idade, sexo, pressão arterial, colesterol, sintomas, frequência cardíaca, entre outras), processado em `assets/fase1/dados/processed/`, com dicionário de variáveis e justificativa clínica da relevância de cada atributo documentados em `document/fase1/` para os experimentos tabulares de Machine Learning da Fase 2.

**Parte 2 — Dados Textuais:** reunimos dois textos `.txt` derivados de publicações oficiais do Ministério da Saúde/CONITEC — um sobre prevenção cardiovascular (fatores de risco, atenção básica) e outro sobre manejo de síndromes coronarianas agudas (sintomas, diagnóstico, tratamento) — formando um corpus complementar (antes vs. depois do evento cardíaco). Esse corpus poderá apoiar futuramente tarefas de NLP como identificação e extração de termos clínicos (sintomas, fatores de risco, procedimentos), classificação temática (prevenção vs. evento agudo), recuperação de informação e sumarização, além de servir de base textual para um sistema de perguntas e respostas ou para o Assistente Cardiológico Virtual (Fase 5).

**Parte 3 — Dados Visuais:** reunimos 120 imagens de eletrocardiograma (ECG), curadas a partir do dataset público *ECG Images dataset of Cardiac Patients* (Mendeley Data), balanceadas em 4 classes (`normal`, `myocardial_infarction`, `history_mi`, `abnormal_heartbeat`), com curadoria rigorosa (deduplicação por hash, remoção de dados administrativos/pessoais). Cada arquivo `.jpg` representa uma imagem de um exame de ECG de 12 derivações — não necessariamente um paciente único. Esse conjunto poderá ser reutilizado futuramente para classificação de imagens de ECG, aprendizado de padrões visuais e experimentos de distinção entre as quatro classes disponibilizadas com técnicas de Visão Computacional (Fase 4), sem qualquer promessa de capacidade diagnóstica clínica nesta etapa.

Nas três partes, seguimos um processo de **governança de dados** com atenção à proveniência, privacidade, qualidade e rastreabilidade. Limitações e possíveis vieses identificados, detalhados nos documentos específicos em `document/fase1/`: a Parte 1 usa uma base originada na Cleveland Clinic (EUA, década de 1980), sem representatividade populacional garantida para outros contextos; a Parte 2 usa textos institucionais brasileiros de linguagem técnica (não espontânea de pacientes), sendo que um dos materiais tem contexto temporal mais antigo (2006); a Parte 3 usa um dataset originado no Paquistão, com possíveis vieses de população e de equipamento de aquisição, e a amostra curada e balanceada não representa necessariamente a prevalência real das condições nas classes.

Na **Fase 3**, coletamos temperatura ambiente, umidade e pulsos artificiais, preservamos leituras durante interrupções e acompanhamos a recuperação e os alertas no painel. A telemetria é independente dos pacientes e relatos das bases anteriores. Ainda precisamos concluir os relatórios obrigatórios, o cliente REST com e-mail simulado e a comparação entre classificador tradicional e modelo neuromórfico, incluindo seus documentos e vídeo.

## 🧠 Fase 2 — Machine Learning

Organizamos a entrega obrigatória da Fase 2 em duas partes independentes:

1. **Extração de sintomas:** preparamos dez relatos simulados completos em `.txt`, um mapa de conhecimento sintoma–doença em CSV e um extrator Python tolerante a maiúsculas, acentos e pontuação.
2. **Classificação textual de risco:** preparamos uma base simulada com 120 frases únicas e balanceadas, aplicamos TF-IDF e Regressão Logística e separamos treino e teste por cenário, com avaliação de desempenho e viés.

Também implementamos os dois desafios **Ir Além**:

- **Portal React + Vite:** autenticação simulada com token local, rotas protegidas, pacientes, agendamentos e dashboard, com testes automatizados;
- **Classificação visual de ECG:** baseline binário com 60 exames equilibrados e revisão ampliada com os 491 conteúdos únicos recuperados da mesma fonte pública, pré-processamento em escala de cinza e MLP Keras. Mantemos hashes distintos entre treino, validação e teste e documentamos a ausência de identificador confiável de paciente.

Como extensão adicional, preservamos o modelo tabular da base Heart Disease — Cleveland e sua aplicação Streamlit. Apresentamos as modalidades separadamente, pois utilizam fontes, pessoas e objetivos distintos.

**Aplicação principal:** [cardioia-fiap.streamlit.app](https://cardioia-fiap.streamlit.app/)

**Portal administrativo:** [julia-carvalho96.github.io/grupo-aura-cardioia-portal](https://julia-carvalho96.github.io/grupo-aura-cardioia-portal/)

**Repositório separado do portal:** [Julia-carvalho96/grupo-aura-cardioia-portal](https://github.com/Julia-carvalho96/grupo-aura-cardioia-portal)

**Documentação completa:** [Guia da Fase 2](document/fase2/README.md)

**Checklist do enunciado:** [Critérios e evidências](document/fase2/CHECKLIST_ENUNCIADO.md)

**Resultados reproduzíveis:** [Resultados dos experimentos](assets/fase2/resultados/README.md)

**Relatório de entrega:** [Relatório da Fase 2](document/fase2/RELATORIO_ENTREGA.md)

Resultados dos experimentos, apresentados no mesmo formato da entrega da Fase 2:

| Experimento | Amostra de teste | Resultado principal |
|---|---:|---:|
| NLP — TF-IDF + Regressão Logística | 24 frases | acurácia 100,0% |
| Tabular — Cleveland | 61 registros | ROC AUC 0,958 |
| Visual — MLP de ECG ampliada | 99 imagens | acurácia balanceada 74,5%; ROC AUC 0,824 |

> Os dados textuais são simulados e intencionalmente separáveis; por isso, 100% no teste não demonstra validade clínica. Na revisão visual, a acurácia simples foi 69,7%, diferente da acurácia balanceada de 74,5%; o recall da classe anormal foi 62,9%. Preservamos o teste e definimos o limiar somente na validação. Não validamos os modelos para uso assistencial.

## 📡 Fase 3 — Monitoramento Contínuo: IoT na Saúde

Organizamos a entrega obrigatória da Fase 3 em duas partes complementares:

1. **Armazenamento e processamento local — Edge Computing:** utilizamos ESP32 no Wokwi, DHT22 e botão para simular pulsos. Coletamos a cada cinco segundos simulados e armazenamos até 2.000 leituras em uma fila FIFO. Com a chave offline, continuamos coletando; ao voltar para online, sincronizamos as pendências. Na demonstração isolada da Parte 1, representamos o envio à nuvem pela saída Serial, conforme a alternativa prevista no enunciado.
2. **Transmissão e visualização — Fog/Cloud Computing:** transmitimos pelo broker público `broker.hivemq.com:1883`, gravamos as leituras em SQLite e confirmamos o recebimento somente após a gravação. No Node-RED, apresentamos gráfico de BPM, gauge de temperatura ambiente, umidade, histórico e alertas didáticos. Reenviamos mensagens sem confirmação e evitamos duplicar a mesma medição no banco.

O DHT22 representa um sensor, mesmo fornecendo temperatura e umidade; utilizamos o botão como segunda entrada para pulsos simulados, conforme o exemplo do enunciado. A chave à esquerda representa offline e, à direita, online. A fila fica em RAM: ao reiniciar o ESP32, perdemos as pendências e iniciamos uma nova sessão. Quando a fila enche, preservamos as leituras antigas, descartamos a nova e contabilizamos a perda. A capacidade cobre aproximadamente 2 h 46 min 40 s de coleta simulada. SPIFFS, hardware físico e Grafana são opcionais.

Definimos alertas acima de 120 BPM e de 30 °C em duas leituras atuais consecutivas. Confirmamos o retorno com duas leituras de até 108 BPM ou até 28 °C, respectivamente. Os limites são escolhas acadêmicas; medimos temperatura ambiente, não corporal. Zero pulsos significa ausência de acionamentos do botão, não ausência de atividade cardíaca. Dados antigos recuperados entram no histórico e não confirmam alertas atuais.

Reutilizamos o mesmo circuito nos dois projetos Wokwi, com firmwares diferentes. Para avaliar a resiliência isolada com Serial, utilizar a **Parte 1**. Para avaliar transmissão MQTT e painel, utilizar a **Parte 2**, que é a demonstração principal. Não é necessário executar ambos simultaneamente.

**Projeto Wokwi — Parte 1, saída Serial:** [CardioIA Edge](https://wokwi.com/projects/478054573982428161)

**Projeto Wokwi — Parte 2, MQTT e painel:** [CardioIA MQTT](https://wokwi.com/projects/478772789361460225)

**Painel local:** [127.0.0.1:1880/dashboard/monitoramento](http://127.0.0.1:1880/dashboard/monitoramento), disponível após iniciar os serviços na própria máquina.

**Documentação completa:** [Guia da Fase 3](document/fase3/README.md)

**Checklist do enunciado:** [Critérios, evidências e pendências](document/fase3/CHECKLIST_ENUNCIADO.md)

**Código ESP32:** [Parte 1 — Serial](src/fase3/firmware/cardioia_edge/) e [Parte 2 — MQTT](src/fase3/firmware/cardioia_mqtt/)

**Dashboard:** [Export Node-RED](src/fase3/node-red/flows.json) e [guia de configuração](document/fase3/node-red/README.md)

**Evidências:** [Testes Edge](document/other/fase3/evidencias/2026-10-24/RESULTADOS.md), [testes MQTT](document/other/fase3/evidencias/2026-10-24/mqtt/RESULTADOS.md) e [validação do painel](document/other/fase3/evidencias/2026-10-24/dashboard/validacao_guiada/RESULTADOS.md)

**Situação da entrega:** validamos as implementações de sensores, fila offline, MQTT e Node-RED. Ainda precisamos produzir o relatório Edge de **no mínimo uma página** e o relatório MQTT/dashboard de **no mínimo duas páginas**. Os registros de testes e capturas apoiam esses documentos, mas não substituem os relatórios exigidos.

Incluímos no escopo os dois desafios **Ir Além**, ainda pendentes:

- **Ir Além 1 — REST e e-mail:** implementar cliente Python que envia e recebe sinais vitais por uma API REST, verifica regras de risco e simula o disparo de e-mail; entregar relatório de **uma a duas páginas**. A consulta de estado do painel não substitui esse cliente.
- **Ir Além 2 — séries temporais e neuromorfismo:** comparar um classificador tradicional com um modelo LIF ou FHN, entregar notebook Python comentado e executado, código e README públicos, relatório comparativo de **duas páginas** e vídeo de **até quatro minutos**, não listado no YouTube, com link neste README.

O prazo informado é **04/11/2026, às 23h59**. Acompanhamos a conclusão, a reprodução do pacote e a submissão no [roteiro de entrega](document/fase3/ROTEIRO_ENTREGA.md).

## 🎥 Vídeo de demonstração

Na **Fase 2**, publicamos um vídeo único de até quatro minutos que apresenta a solução obrigatória de NLP e classificação textual, o portal React do Ir Além 1 e a MLP visual de ECG do Ir Além 2.

- **Assistir no YouTube (não listado):** [CardioIA — Fase 2 completa](https://youtu.be/qoKjl6oeotY)

Na **Fase 3**, ainda precisamos produzir e publicar o vídeo específico do Ir Além 2, com até quatro minutos e análise crítica da comparação dos modelos. O link da Fase 2 permanece como registro da entrega anterior e não substitui esse novo vídeo.

## 📁 Estrutura de pastas

Seguimos o [modelo oficial FIAP](https://github.com/agodoi/templateFiapVfinal). Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: mantemos as configurações específicas do GitHub e os workflows de verificação automática.

- <b>assets</b>: reunimos datasets, textos, imagens, resultados e capturas, organizados por fase.

- <b>config</b>: mantemos requisitos, contratos de dados e parâmetros de configuração do projeto.

- <b>document</b>: reunimos os guias e documentos de cada entrega. Na subpasta `other`, mantemos referências, estudos, auditorias e cópias históricas.

- <b>scripts</b>: mantemos scripts auxiliares de inicialização, migração e validação.

- <b>src</b>: organizamos o código-fonte desenvolvido ao longo das fases, incluindo firmware, aplicações, notebooks e testes.

- <b>README.md</b>: apresentamos o projeto, sua evolução e as instruções gerais de reprodução.

Os artefatos estão organizados dentro das pastas oficiais:

- `assets/fase1/dados/raw/` e `assets/fase1/dados/processed/`: fonte bruta e dataset numérico preparado.
- `assets/fase1/textos/` e `assets/fase1/imagens/ecg/`: corpus textual e 120 imagens de ECG.
- `assets/fase2/dados/` e `assets/fase2/resultados/`: dados e resultados da Fase 2.
- `assets/fase3/evidencias/`: capturas da simulação e do painel.
- `config/fase1/`, `config/fase2/` e `config/fase3/`: dependências e configurações de cada fase.
- `document/fase1/`, `document/fase2/` e `document/fase3/`: documentação principal, documentos anteriores submetidos e acompanhamento da entrega atual.
- `document/other/referencias/`: enunciados, fontes e materiais de aula separados por fase.
- `document/other/fase3/evidencias/`: registros e resultados dos testes de IoT.
- `document/other/historico/`: cópias das versões anteriores, preservadas como registros históricos.
- `src/fase1/` e `scripts/fase1/`: preparação dos dados e verificação da preservação.
- `src/fase2/`: aplicação Streamlit, modelos, notebooks e testes; portal em `src/fase2/portal-cardioia/`.
- `src/fase3/` e `scripts/fase3/`: firmware, consumidor MQTT, Node-RED, testes e inicialização do monitoramento.

O [índice da documentação](document/README.md) identifica os documentos principais e os [registros de organização](document/other/organizacao/README.md) explicam os caminhos anteriores. `.venv/`, `.tools/` e `node_modules/` são pastas locais geradas durante a execução e não fazem parte da entrega versionada.

## 🔗 Links externos

- **Parte 1 — Dados Numéricos da Fase 1:** [Acessar pasta](https://drive.google.com/drive/folders/1I_gzbCuJUYvx0lwPtg5XhDf-IH039t2s?usp=sharing)
- **Parte 2 — Dados Textuais da Fase 1:** [Acessar pasta](https://drive.google.com/drive/folders/1Qc5W_RoAIq1sopROYvCss5uBwO0IlI6C?usp=sharing)
- **Parte 3 — Dados Visuais da Fase 1:** [Acessar pasta](https://drive.google.com/drive/folders/135ZuObt02AxX13aiQG_sqef9nxAjkPMy?usp=sharing)
- **Fechamento original da Fase 1:** [fiap-ano02-fase01-cardioia](https://github.com/murilosalla-blip/fiap-ano02-fase01-cardioia), commit `cbd9685`.
- **Fechamento original da Fase 2:** [fiap-ano02-fase02-cardioia](https://github.com/murilosalla-blip/fiap-ano02-fase02-cardioia), commit `bf4f0e1`.
- **Projeto atual — evolução até a Fase 3:** [fiap-ano02-fase03-cardioia](https://github.com/murilosalla-blip/fiap-ano02-fase03-cardioia).
- **Endereços históricos preservados:** [repositório original](https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia) e [URL Git original](https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia.git), que direcionam ao repositório atual após a renomeação.

Preservamos nos repositórios históricos a estrutura e os documentos dos fechamentos anteriores. Nesta versão acumulada, utilizamos os caminhos atualizados descritos acima. Os links das aplicações, do portal e do vídeo da Fase 2 e os dois Wokwi estão identificados nas respectivas seções.

## 🔧 Como executar o código

Os dados finais da **Fase 1** já estão preparados e disponíveis nas pastas do projeto e nos links externos; não é necessário executar código para avaliá-los. Fornecemos os scripts para reprodução e rastreabilidade da preparação. As aplicações e os modelos da Fase 2 e o monitoramento da Fase 3 têm instruções próprias nas seções seguintes.

**Pré-requisitos:** Git e Python **3.12**. Para as imagens, utilizamos Pillow. Para o portal React e o Node-RED, utilizamos Node.js **24** com npm. O Wokwi e o broker público exigem internet e acesso à porta TCP **1883**. Não é necessário comprar hardware.

**Clonar o repositório e preparar o ambiente** — comandos PowerShell, executados na raiz do projeto:

```powershell
git clone https://github.com/murilosalla-blip/fiap-ano02-fase03-cardioia.git
Set-Location -LiteralPath './fiap-ano02-fase03-cardioia'
python -m venv .venv
```

Se a cópia e o ambiente já existem, seguir diretamente os comandos da fase desejada. Utilizamos o executável do ambiente virtual sem precisar ativá-lo ou alterar a política de execução do PowerShell. No Linux/macOS, criar com `python3.12 -m venv .venv` e substituir `.venv/Scripts/python.exe` por `.venv/bin/python`, nas pastas correspondentes. Os comandos `node` e `npm` permanecem iguais.

**Reproduzir o dataset numérico da Parte 1** — gera o CSV a partir da fonte bruta incluída no repositório:

```powershell
.\.venv\Scripts\python.exe src/fase1/preparar_dataset_numerico.py
.\.venv\Scripts\python.exe scripts/fase1/verificar_preservacao.py
```

Resultado esperado: CSV em `assets/fase1/dados/processed/heart_disease_cleveland.csv`, com **303 registros**, e verificação dos **223 arquivos inventariados no início da Fase 2**, incluindo os 181 do fechamento da Fase 1. Os documentos das três modalidades estão no [guia da Fase 1](document/fase1/README.md).

**Reproduzir a amostra de imagens de ECG da Parte 3** — requer preparação manual antes de executar:

1. Consultar a [fonte do dataset](document/other/referencias/fase1/parte3/fonte_dataset.md), baixar a base bruta do Mendeley Data e extraí-la localmente.
2. Ajustar `RAW_DIR` em `src/fase1/preparar_amostra_ecg.py` para a pasta extraída.
3. Instalar Pillow e executar:

```powershell
.\.venv\Scripts\python.exe -m pip install -r config/fase1/requirements.txt
.\.venv\Scripts\python.exe src/fase1/preparar_amostra_ecg.py
```

Resultado esperado: **120 JPG**, distribuídos em quatro categorias, e manifesto em `document/other/referencias/fase1/parte3/manifesto_amostra.csv`. Essa reconstrução depende da fonte externa; para apenas avaliar, utilizar a amostra já entregue. Os dois TXT estão prontos em `assets/fase1/textos/` e podem ser lidos sem executar preparação.

## ▶️ Como executar a Fase 2

A aplicação pública pode ser avaliada sem usar o terminal:

- [Abrir CardioIA](https://cardioia-fiap.streamlit.app/)
- [Abrir portal administrativo](https://julia-carvalho96.github.io/grupo-aura-cardioia-portal/)

Para reprodução técnica da entrega obrigatória de NLP, executar na raiz com o ambiente Python preparado:

```powershell
.\.venv\Scripts\python.exe -m pip install -r config/fase2/requirements.txt
.\.venv\Scripts\python.exe src/fase2/src/extrair_sintomas.py
.\.venv\Scripts\python.exe src/fase2/src/classificar_risco_texto.py
.\.venv\Scripts\python.exe src/fase2/tests/test_nlp.py
.\.venv\Scripts\python.exe src/fase2/tests/test_app.py
.\.venv\Scripts\python.exe -m streamlit run src/fase2/app.py
```

Resultado esperado: processamento dos **dez relatos**, treinamento e resultados textuais em `assets/fase2/resultados/nlp/`, testes concluídos e aplicação em [localhost:8501](http://localhost:8501). Utilizar exemplos fictícios para conferir extração, classificação e histórico temporário. Encerrar o servidor com **Ctrl+C**.

Para o portal React, executar em outro terminal, também na raiz:

```powershell
npm ci --prefix src/fase2/portal-cardioia
npm test --prefix src/fase2/portal-cardioia
npm run build --prefix src/fase2/portal-cardioia
npm run dev --prefix src/fase2/portal-cardioia
```

Abrir o endereço exibido pelo Vite. Utilizar um e-mail fictício em formato válido e senha de pelo menos seis caracteres. Conferir pacientes simulados, busca, agendamento e indicadores; não utilizar credenciais reais. Os sete testes e o build devem concluir.

Para o experimento visual, utilizar um ambiente separado com as versões de TensorFlow e Keras fixadas nos requisitos:

```powershell
python -m venv src/fase2/.venv
.\src\fase2\.venv\Scripts\python.exe -m pip install -r config/fase2/requirements-visual.txt
.\src\fase2\.venv\Scripts\python.exe src/fase2/tests/test_visual.py
.\src\fase2\.venv\Scripts\python.exe src/fase2/src/treinar_mlp_ecg.py
```

O baseline utiliza a amostra versionada da Fase 1 e gera resultados em `assets/fase2/resultados/visual/`. Para reproduzir a revisão ampliada com 491 conteúdos únicos, o treinamento tabular e os notebooks, seguir o [guia completo da Fase 2](document/fase2/README.md). Os quatro notebooks já incluem saídas para avaliação; novas execuções devem ser gravadas separadamente.

Os workflows do GitHub Actions verificam dados, testes, treinamentos, notebooks e build do portal. Preservamos as evidências dos resultados e suas limitações na documentação de cada experimento.

## ▶️ Como executar a Fase 3

Para avaliar o sistema completo, utilizar o **Wokwi MQTT da Parte 2** e o painel Node-RED. Não é necessário executar os treinamentos da Fase 2 antes do monitoramento. Na raiz, com o ambiente Python preparado, instalar as dependências e iniciar painel e consumidor juntos:

```powershell
.\.venv\Scripts\python.exe -m pip install -r config/fase3/requirements-mqtt.txt
npm ci --prefix src/fase3/node-red --ignore-scripts --no-audit --no-fund
$env:CARDIOIA_PYTHON = (Resolve-Path .\.venv\Scripts\python.exe).Path
node scripts/fase3/iniciar_dashboard.js --com-consumidor
```

No Linux/macOS, usar `export CARDIOIA_PYTHON="$PWD/.venv/bin/python"` em lugar da atribuição PowerShell. Manter o terminal aberto e apenas **um consumidor** no tópico durante o teste.

**Validar a demonstração principal:**

1. Abrir o [monitoramento local](http://127.0.0.1:1880/dashboard/monitoramento). Antes de transmitir, é normal aguardar dados.
2. Abrir o [Wokwi MQTT da Parte 2](https://wokwi.com/projects/478772789361460225), dar **Play** e mover a chave para a **direita, online**. Conferir `transport: mqtt`, `# mqtt_conectado` e `# ack_confirmado` no Serial, além do avanço da leitura e da confirmação no painel.
3. Pressionar **e soltar** o botão verde ou a tecla **B**. Seis pulsos em cinco segundos simulados representam aproximadamente 72 BPM. Para testar o alerta, obter mais de dez acionamentos por janela em duas coletas atuais consecutivas; depois reduzir até 108 BPM por duas leituras atuais. Segurar o botão conta um único pulso.
4. Clicar no DHT22 em execução, alterar para **31 °C** e aguardar duas leituras atuais para conferir o alerta. Reduzir para **28 °C** e aguardar duas leituras para conferir o retorno.
5. Mover a chave para a **esquerda, offline**, aguardar pelo menos três coletas e conferir o crescimento da fila. Voltar à direita e observar a recuperação ordenada, as confirmações e a redução da fila até zero. Os dados recuperados devem permanecer no histórico.
6. Parar a simulação e pressionar **Ctrl+C** no terminal para encerrar os serviços. O banco e os eventos permanecem em `.tools/runtime/fase3/`, fora do Git.

**Validar a resiliência isolada da Parte 1:** abrir o [Wokwi Serial](https://wokwi.com/projects/478054573982428161), dar Play, manter a chave à esquerda por pelo menos três coletas e voltar à direita. Conferir os JSON em ordem, com `transport: serial_demo`, e o esvaziamento da fila. Essa demonstração dispensa broker, consumidor e painel; representa a simulação Serial pedida na Parte 1.

**Interpretar o tempo e o estado do painel:** coletamos a cada cinco segundos do relógio do ESP32 simulado. Manter o Wokwi visível, pois em segundo plano pode desacelerar. O estado “broker conectado” é independente da chegada de uma leitura recente; após 15 segundos reais sem leitura atual, preservamos o último valor em cinza. Publicação tentada não comprova gravação: o ACK confirma a persistência no consumidor.

O [guia completo da Fase 3](document/fase3/README.md) detalha instalação para Windows e Linux/macOS, consulta ao banco, reenvio após ACK omitido, estados e diagnóstico de falhas. No painel, leituras recuperadas e reenvios não confirmam novos alertas do presente. Os intervalos e limites utilizados são escolhas da implementação.

## 🗃 Histórico de lançamentos

* 0.1.0 - 21/08/2026
    * Estruturamos o projeto CardioIA e sua configuração no repositório.
* 0.2.0 - 21/08/2026
    * Preparamos, validamos e documentamos o dataset numérico Cleveland.
* 0.3.0 - 21/08/2026
    * Preparamos e documentamos o corpus textual sobre prevenção e síndromes coronarianas agudas.
* 0.4.0 - 21/08/2026
    * Preparamos e documentamos a amostra de 120 imagens de ECG.
* 0.5.0 - 14/09/2026
    * Implementamos o pipeline tabular e a comparação e avaliação dos modelos da Fase 2.
* 0.6.0 - 14/09/2026
    * Acrescentamos análises de incerteza, calibração, interpretação e desempenho por subgrupos.
* 0.7.0 - 14/09/2026
    * Publicamos e testamos a aplicação acadêmica Streamlit.
* 0.8.0 - 14/09/2026
    * Implementamos e documentamos NLP, portal React e experimento visual com MLP.
* Fechamento da Fase 2 - 07/10/2026
    * Registramos o vídeo publicado e o encerramento da documentação da entrega.
* 0.9.0 - 24/10/2026
    * Validamos as implementações ESP32, recuperação offline, MQTT e Node-RED da Fase 3.
* Organização e revisão documental - 24 e 25/10/2026
    * Organizamos as fases nas pastas oficiais, preservamos os materiais e links anteriores e detalhamos a reprodução. Mantemos os [registros da revisão](document/other/organizacao/REVISAO_DOCUMENTACAO.md).
* Padronização do README - 25/10/2026
    * Preservamos os fechamentos das Fases 1 e 2 em repositórios próprios e renomeamos este para a Fase 3. Retomamos a estrutura, os emojis e o estilo explicativo do README original, com os caminhos atuais e as pendências da Fase 3 identificadas.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
