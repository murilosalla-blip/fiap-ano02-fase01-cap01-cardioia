# FIAP — Faculdade de Informática e Administração Paulista

<p align="center"><a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP" width="40%"></a></p>

# CardioIA — Fases 1, 2 e 3

## Grupo Aura

| Integrante | RM |
|---|---|
| Murilo Salla | 568041 |
| Elias da Silva de Souza | 568500 |
| Julia Duarte de Carvalho | 567816 |

**Tutor:** Leonardo Ruiz Orabona. **Coordenador:** André Godoi Chiovato.

## Descrição

Desenvolvemos o CardioIA como projeto acadêmico da FIAP, organizado em sete fases. Estudamos como transformar dados cardiovasculares em informação, construir modelos de IA e integrar dispositivos simulados a interfaces de acompanhamento. Neste repositório, apresentamos a evolução acumulada das Fases 1, 2 e 3: preparação dos dados, experimentos de inteligência artificial e monitoramento conectado. Demonstramos esse percurso de forma reproduzível, com rastreabilidade e explicação das limitações.

Na Fase 1, reunimos três modalidades independentes: 303 registros e 14 variáveis da base Heart Disease Cleveland; dois textos derivados de publicações oficiais do Ministério da Saúde e da CONITEC; e 120 imagens de ECG. Documentamos origem, preparação, privacidade e possíveis aplicações de cada conjunto.

Na Fase 2, desenvolvemos a extração de sintomas por mapa de conhecimento e a classificação textual com TF-IDF. Acrescentamos experimentos tabulares, uma aplicação Streamlit, um portal React e a classificação visual por MLP. Mantivemos separados os dados e resultados das diferentes modalidades: eles não representam os mesmos pacientes.

Na Fase 3, ampliamos o CardioIA com monitoramento contínuo: implementamos a captura com ESP32 no Wokwi, a fila limitada para interrupções, a transmissão MQTT, a gravação em SQLite antes da confirmação e o painel Node-RED. Validamos coleta offline, recuperação, reenvio, deduplicação, pulsos, temperatura ambiente e alertas didáticos. Mantemos os módulos anteriores disponíveis e acrescentamos um fluxo próprio de telemetria; os classificadores da Fase 2 não recebem automaticamente essas leituras. Ainda precisamos produzir os relatórios obrigatórios e concluir os desafios REST/e-mail e comparação de modelos neuromórficos, incluindo seus documentos e vídeo.

Utilizamos dados e simulações identificados para fins educacionais. As métricas dos experimentos não demonstram validade clínica; não realizamos diagnóstico nem oferecemos orientação assistencial.

[Repositório atual — evolução até a Fase 3](https://github.com/murilosalla-blip/fiap-ano02-fase03-cardioia).

## Fases e situação da entrega

| Fase | O que entregamos ou estamos preparando | Documentação para avaliação |
|---|---|---|
| 1 — Batimentos de Dados | Dados numéricos, textuais e visuais; entrega anterior avaliada com nota máxima | [Guia, fontes e documento submetido](document/fase1/README.md) |
| 2 — Diagnóstico automatizado com IA | Extração, classificador textual, notebooks, interfaces e desafios; entrega anterior avaliada com nota máxima | [Como reproduzir e resultados](document/fase2/README.md), [relatório](document/fase2/RELATORIO_ENTREGA.md) |
| 3 — Monitoramento contínuo | ESP32, fila offline, MQTT e Node-RED implementados e testados; documentação final e Ir Além em andamento | [Guia de reprodução](document/fase3/README.md), [matriz do enunciado](document/fase3/CHECKLIST_ENUNCIADO.md), [roteiro restante](document/fase3/ROTEIRO_ENTREGA.md) |

O prazo informado para a Fase 3 é **04/11/2026, às 23h59**. A implementação das três primeiras etapas não representa o encerramento da fase: os relatórios mínimos ainda fazem parte da entrega obrigatória.

Preservamos também as versões exatas dos fechamentos anteriores em repositórios próprios: [Fase 1](https://github.com/murilosalla-blip/fiap-ano02-fase01-cardioia), no commit `cbd9685`, e [Fase 2](https://github.com/murilosalla-blip/fiap-ano02-fase02-cardioia), no commit `bf4f0e1`. Neste repositório, mantemos seus materiais com os caminhos atuais e acrescentamos a Fase 3. As cópias históricas mantêm a estrutura e a documentação da época; os comandos abaixo utilizam a organização atual.

## Evolução do CardioIA — Fases 1, 2 e 3

### Fase 1 — origem, justificativa e materiais

| Modalidade | Conteúdo disponível | Por que selecionamos e como utilizar |
|---|---|---|
| Numérica | Heart Disease Cleveland: 303 registros, 14 variáveis; fonte bruta e CSV processado em `assets/fase1/dados/` | Idade e sexo contextualizam a amostra; pressão e colesterol representam medidas clínicas; dor torácica, angina e frequência cardíaca descrevem sintomas e resposta ao esforço; atributos de exames complementam a análise. Documentamos cada variável e o alvo no [dicionário](document/fase1/parte1_dicionario_variaveis.md). |
| Textual | Dois arquivos `.txt` em `assets/fase1/textos/`, derivados de fontes MS/CONITEC | Trabalhamos prevenção e síndromes coronarianas. Propomos extração de sintomas e entidades, classificação temática, busca e sumarização; linguagem institucional não equivale a relatos espontâneos de pacientes. |
| Visual | 120 JPG de ECG: 30 normais e 30 de cada uma das três categorias anormais, em `assets/fase1/imagens/ecg/` | Utilizamos a fonte Mendeley ECG Images dataset of Cardiac Patients. A amostra permite estudar pré-processamento e classificação; removemos cabeçalhos administrativos e duplicatas exatas e registramos a rastreabilidade. Um exame não comprova um paciente único. |

No [guia da Fase 1](document/fase1/README.md), detalhamos as fontes, o tratamento dos seis valores ausentes na base numérica, os recortes de privacidade das imagens e as limitações de representatividade. Os três conjuntos vêm de fontes e pessoas diferentes; não formam uma base multimodal de pacientes pareados. O balanceamento visual não representa prevalência clínica.

**Materiais externos preservados da entrega original:** [dados numéricos](https://drive.google.com/drive/folders/1I_gzbCuJUYvx0lwPtg5XhDf-IH039t2s?usp=sharing), [dados textuais](https://drive.google.com/drive/folders/1Qc5W_RoAIq1sopROYvCss5uBwO0IlI6C?usp=sharing) e [dados visuais](https://drive.google.com/drive/folders/135ZuObt02AxX13aiQG_sqef9nxAjkPMy?usp=sharing).

### Fase 2 — entregáveis e resultados

Na atividade obrigatória, preparamos dez relatos simulados, um mapa com 25 associações e 120 frases rotuladas para classificar risco textual. Separamos os pares de frases por cenário antes do treinamento. Acrescentamos o portal React do Ir Além 1 e os notebooks de MLP de ECG do Ir Além 2, mantendo o baseline visual e sua revisão ampliada.

| Experimento | Resultado registrado | Limite da interpretação |
|---|---|---|
| TF-IDF + Regressão Logística | 100% de acurácia em 24 frases de teste | Base pequena, simulada e separável; não demonstra generalização clínica |
| Modelo tabular Cleveland | ROC AUC 0,958 em 61 registros de teste | Dados históricos e subgrupos pequenos; avaliação independente da textual |
| MLP visual ampliada | 69,7% de acurácia; 74,5% de acurácia balanceada; recall anormal 62,9%; ROC AUC 0,824 em 99 imagens | São métricas diferentes; persistem falsos negativos e ausência de ID confiável de paciente |

Preservamos os [notebooks executados](src/fase2/notebooks/), os [resultados](assets/fase2/resultados/README.md), o [vídeo completo da Fase 2, não listado e de até quatro minutos](https://youtu.be/qoKjl6oeotY), o [Streamlit](https://cardioia-fiap.streamlit.app/), o [portal publicado](https://julia-carvalho96.github.io/grupo-aura-cardioia-portal/) e seu [repositório independente](https://github.com/Julia-carvalho96/grupo-aura-cardioia-portal).

### Fase 3 — monitoramento contínuo com IoT

Acrescentamos ao CardioIA a captura periódica de sinais simulados e o acompanhamento durante interrupções de comunicação. Utilizamos o ESP32 no Wokwi, o DHT22 para temperatura ambiente e umidade e o botão como segunda entrada para pulsos artificiais. Com isso, passamos dos dados preparados e dos experimentos de IA das fases anteriores para um fluxo de coleta, armazenamento local, transmissão, visualização e alerta.

| Parte da entrega | O que implementamos | Como conferir |
|---|---|---|
| Parte 1 — Edge Computing | Coleta a cada cinco segundos simulados, conectividade booleana e fila FIFO limitada a 2.000 amostras; demonstramos sincronização pela saída Serial | [Firmware Serial](src/fase3/firmware/cardioia_edge/), [Wokwi da Parte 1](https://wokwi.com/projects/478054573982428161) e [resultados dos testes](document/other/fase3/evidencias/2026-10-24/RESULTADOS.md) |
| Parte 2 — MQTT | Transmissão ao broker público, consumidor Python, persistência SQLite, confirmação após gravação e deduplicação de reenvios | [Firmware MQTT](src/fase3/firmware/cardioia_mqtt/), [Wokwi da Parte 2](https://wokwi.com/projects/478772789361460225) e [protocolo](document/fase3/mqtt/README.md) |
| Parte 2 — Node-RED | Gráfico de BPM, gauge de temperatura ambiente, indicação de umidade, conexão, recuperação e alertas didáticos | [Export do fluxo](src/fase3/node-red/flows.json), [guia do painel](document/fase3/node-red/README.md) e [evidências visuais](assets/fase3/evidencias/) |

Os dados de telemetria são simulados e independentes dos pacientes e relatos das bases anteriores. Mantemos os modelos da Fase 2 como módulos disponíveis do projeto; nesta etapa, avaliamos o monitoramento pelo fluxo ESP32 → broker MQTT → consumidor e painel Node-RED. A fila do ESP32 fica em RAM e perde pendências ao reiniciar; o SQLite preserva somente o que o consumidor recebeu e gravou.

No painel, definimos alertas para pulsos acima de 120 BPM e temperatura ambiente acima de 30 °C, confirmados em duas leituras atuais consecutivas. Zero pulsos significa ausência de acionamentos do botão. Esses limites são escolhas acadêmicas e não representam critérios de diagnóstico. O [guia da Fase 3](document/fase3/README.md) detalha os estados, as regras e os testes de reprodução.

O escopo restante inclui os relatórios obrigatórios de Edge e MQTT/dashboard, o cliente REST com e-mail simulado do Ir Além 1 e a comparação entre classificador tradicional e modelo neuromórfico do Ir Além 2. Relacionamos os artefatos e seus critérios na [matriz do enunciado](document/fase3/CHECKLIST_ENUNCIADO.md); não apresentamos essas entregas como concluídas.

## Estrutura de pastas

Seguimos o [modelo oficial FIAP](https://github.com/agodoi/templateFiapVfinal). Organizamos as fases dentro das pastas institucionais; não mantemos `fase1`, `fase2` ou `fase3` diretamente na raiz.

| Pasta | Organização e finalidade |
|---|---|
| `.github/` | Workflows de verificação e integração contínua |
| `assets/fase1/`, `assets/fase2/`, `assets/fase3/` | Dados, imagens, resultados e capturas por fase; logo compartilhado em `assets/` |
| `config/fase1/`, `config/fase2/`, `config/fase3/` | Requisitos, contratos e configurações por fase |
| `document/fase1/`, `document/fase2/`, `document/fase3/` | Guias, relatórios e requisitos de cada entrega |
| `document/other/` | Enunciados e referências, auditorias, registros de testes e cópias históricas |
| `scripts/fase1/`, `scripts/fase3/` | Verificações, inicialização e validações auxiliares |
| `src/fase1/`, `src/fase2/`, `src/fase3/` | Código-fonte; portal em `src/fase2/portal-cardioia/` |

Os arquivos de dependências exigidos pelas ferramentas permanecem junto dos aplicativos. As pastas locais `.venv/`, `.tools/` e `node_modules/` são geradas na execução e não integram a entrega versionada. O [índice da documentação](document/README.md) identifica os PDFs anteriores e os documentos pendentes por fase. Mantemos a visão consolidada no [AI Project Document](document/ai_project_document_fiap.md) e a rastreabilidade das mudanças no [registro de organização](document/other/organizacao/README.md).

## Links externos

| Recurso | Endereço |
|---|---|
| Projeto atual — Fase 3 e evolução acumulada | [fiap-ano02-fase03-cardioia](https://github.com/murilosalla-blip/fiap-ano02-fase03-cardioia) |
| Fechamento original da Fase 1 | [fiap-ano02-fase01-cardioia](https://github.com/murilosalla-blip/fiap-ano02-fase01-cardioia) |
| Fechamento original da Fase 2 | [fiap-ano02-fase02-cardioia](https://github.com/murilosalla-blip/fiap-ano02-fase02-cardioia) |
| Materiais da Fase 1 | [Numéricos](https://drive.google.com/drive/folders/1I_gzbCuJUYvx0lwPtg5XhDf-IH039t2s?usp=sharing), [textuais](https://drive.google.com/drive/folders/1Qc5W_RoAIq1sopROYvCss5uBwO0IlI6C?usp=sharing) e [visuais](https://drive.google.com/drive/folders/135ZuObt02AxX13aiQG_sqef9nxAjkPMy?usp=sharing) |
| Aplicação da Fase 2 | [Streamlit](https://cardioia-fiap.streamlit.app/) |
| Portal da Fase 2 | [Aplicação](https://julia-carvalho96.github.io/grupo-aura-cardioia-portal/) e [repositório independente](https://github.com/Julia-carvalho96/grupo-aura-cardioia-portal) |
| Vídeo da Fase 2 | [Demonstração completa](https://youtu.be/qoKjl6oeotY) |
| Simulações da Fase 3 | [Parte 1 — Serial](https://wokwi.com/projects/478054573982428161) e [Parte 2 — MQTT](https://wokwi.com/projects/478772789361460225) |

Preservamos o [endereço histórico do projeto](https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia) e sua [URL Git original](https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia.git), utilizados nas entregas anteriores. Após a renomeação, esses endereços direcionam ao repositório atual. O vídeo específico da Fase 3 será registrado quando concluirmos o Ir Além 2.

## Como reproduzir

### 1. Obter o projeto e preparar o ambiente

Pré-requisitos: **Git e Python 3.12**. Para o portal da Fase 2 e o painel da Fase 3, utilizar também **Node.js 24 e npm**. O Wokwi e o broker público da Fase 3 exigem internet e acesso à porta TCP 1883. Não é necessário comprar ESP32 ou sensores.

Os comandos principais abaixo utilizam **PowerShell no Windows**, sempre na raiz do repositório. O ambiente virtual dispensa ativação e alteração da política de execução.

```powershell
git clone https://github.com/murilosalla-blip/fiap-ano02-fase03-cardioia.git
Set-Location -LiteralPath './fiap-ano02-fase03-cardioia'
python --version
python -m venv .venv
```

No Linux/macOS, criar o ambiente com `python3.12 -m venv .venv` e substituir `./.venv/Scripts/python.exe` ou `.\.venv\Scripts\python.exe` por `./.venv/bin/python` nos comandos Python. Os comandos `node` e `npm` são iguais nos dois ambientes. A configuração específica do Python usado pelo painel está indicada no passo da Fase 3.

Para avaliar uma fase, seguir sua seção; não é necessário executar todos os treinamentos anteriores antes de testar a Fase 3.

### 2. Reproduzir a Fase 1

Os dados finais já estão incluídos: **a avaliação pode ser feita sem reconstruí-los**. Abrir o [guia da Fase 1](document/fase1/README.md), os arquivos em `assets/fase1/` e os links externos acima.

Para conferir a preservação dos materiais e reproduzir a preparação numérica a partir do bruto incluído:

```powershell
.\.venv\Scripts\python.exe scripts/fase1/verificar_preservacao.py
.\.venv\Scripts\python.exe src/fase1/preparar_dataset_numerico.py
```

Resultado esperado: verificação dos **223 arquivos inventariados no início da Fase 2**, incluindo os 181 arquivos do fechamento da Fase 1, e CSV processado em `assets/fase1/dados/processed/heart_disease_cleveland.csv`, com 303 registros. A reconstrução das imagens exige baixar a fonte bruta externa, instalar Pillow e ajustar `RAW_DIR`; o [guia completo](document/fase1/README.md) explica essa preparação separadamente.

### 3. Reproduzir a Fase 2

```powershell
.\.venv\Scripts\python.exe -m pip install -r config/fase2/requirements.txt
.\.venv\Scripts\python.exe src/fase2/src/extrair_sintomas.py
.\.venv\Scripts\python.exe src/fase2/src/classificar_risco_texto.py
.\.venv\Scripts\python.exe src/fase2/tests/test_nlp.py
.\.venv\Scripts\python.exe src/fase2/tests/test_app.py
.\.venv\Scripts\python.exe -m streamlit run src/fase2/app.py
```

Resultado esperado: extração dos dez relatos, treinamento e métricas textuais em `assets/fase2/resultados/nlp/`, testes concluídos e aplicação em [localhost:8501](http://localhost:8501). Utilizar relatos fictícios e conferir a extração e a classificação. Encerrar o servidor com **Ctrl+C**.

Para iniciar o portal administrativo em outro terminal, a partir da raiz:

```powershell
npm ci --prefix src/fase2/portal-cardioia
npm test --prefix src/fase2/portal-cardioia
npm run build --prefix src/fase2/portal-cardioia
npm run dev --prefix src/fase2/portal-cardioia
```

Abrir o endereço exibido pelo Vite, testar o login fictício, consultar pacientes simulados e agendar uma consulta. Não utilizar credenciais reais. O [guia da Fase 2](document/fase2/README.md) detalha os notebooks, o treinamento tabular e o ambiente separado com TensorFlow para reproduzir a MLP. Preservamos os resultados anteriores para permitir a avaliação sem repetir todos os treinamentos.

### 4. Reproduzir a Fase 3 — sistema completo MQTT e Node-RED

Este é o caminho principal para avaliar a comunicação e o painel da Parte 2. Preparar as dependências e iniciar **painel e consumidor juntos**:

```powershell
.\.venv\Scripts\python.exe -m pip install -r config/fase3/requirements-mqtt.txt
npm ci --prefix src/fase3/node-red --ignore-scripts --no-audit --no-fund
$env:CARDIOIA_PYTHON = (Resolve-Path .\.venv\Scripts\python.exe).Path
node scripts/fase3/iniciar_dashboard.js --com-consumidor
```

No Linux/macOS, antes do último comando, utilizar `export CARDIOIA_PYTHON="$PWD/.venv/bin/python"` em lugar da atribuição PowerShell. Manter o terminal aberto. Não iniciar um segundo consumidor no mesmo tópico durante esse teste.

1. Abrir o [monitoramento local](http://127.0.0.1:1880/dashboard/monitoramento). Sem ESP32 transmitindo, a espera por dados é normal.
2. Abrir **[Parte 2 — ESP32 com MQTT no Wokwi](https://wokwi.com/projects/478772789361460225)**, dar Play e mover a chave de conexão para a **direita, online**. A chave é um interruptor do circuito, não uma senha ou chave de acesso.
3. Aguardar no Serial `# mqtt_conectado` e `# ack_confirmado`. O JSON deve conter `"transport":"mqtt"`. Conferir no painel o avanço da última leitura e da última confirmação, além da temperatura e da umidade.
4. Pressionar **e soltar** o botão verde, ou a tecla **B**, repetidamente. Seis pulsos em uma janela de cinco segundos simulados representam aproximadamente 72 BPM. Segurar o botão conta um único pulso. O gráfico deve registrar os valores; sem acionamentos, registra zero.
5. Alterar o DHT22 para **31 °C** e aguardar duas leituras atuais consecutivas: o painel deve registrar o alerta didático de temperatura. Reduzir para **28 °C** e aguardar duas leituras atuais para conferir o retorno. Temperatura do ambiente não representa temperatura corporal.
6. Mover a chave para a **esquerda, offline**, aguardar pelo menos três coletas no Serial e observar o crescimento da fila. Voltar para a direita: os dados pendentes devem ser transmitidos em ordem, confirmados e removidos da fila; o gráfico deve preservar a recuperação. O [guia detalhado](document/fase3/README.md) inclui os testes dos dois alertas, reenvio, banco e diagnóstico de falhas.

Coletamos a cada **cinco segundos do relógio do ESP32 simulado**. Em segundo plano, o Wokwi pode avançar mais devagar que o tempo real. Manter a simulação visível. O estado “broker conectado” não significa que chegou uma leitura recente; após 15 segundos reais sem leitura atual, o painel mantém o último valor em cinza. Os intervalos e limites são escolhas da implementação, não exigências temporais do exercício.

Para encerrar, parar a simulação e pressionar **Ctrl+C** no terminal do painel. O banco e os eventos permanecem em `.tools/runtime/fase3/`, fora do Git.

### Por que existem dois projetos Wokwi?

Reutilizamos **o mesmo circuito** para demonstrar duas etapas do enunciado. O que muda é o **firmware e o destino dos dados**, não a montagem. Não é necessário executar os dois ao mesmo tempo.

| Projeto e finalidade | Código correspondente | Como identificar e avaliar |
|---|---|---|
| [Parte 1 — Edge com demonstração Serial](https://wokwi.com/projects/478054573982428161) | `src/fase3/firmware/cardioia_edge/` | Não utiliza broker nem painel. Coleta offline e esvazia a fila pelo Serial quando a chave fica online. JSON com `transport: serial_demo`. Seguir a Parte 1 no [guia](document/fase3/README.md). |
| [Parte 2 — MQTT e painel, demonstração principal](https://wokwi.com/projects/478772789361460225) | `src/fase3/firmware/cardioia_mqtt/` | Conecta ao broker real, recebe ACK após gravação SQLite e alimenta o Node-RED. JSON com `transport: mqtt`. Seguir o passo 4 acima. |

A demonstração Serial atende à simulação de nuvem prevista na Parte 1; sozinha, não comprova a transmissão MQTT da Parte 2. Identificamos cada link pelo objetivo para evitar confundir circuitos iguais com funcionalidades iguais.

## Evidências e critérios da Fase 3

Relacionamos os cinco critérios de dois pontos, os artefatos e as pendências na [matriz de requisitos](document/fase3/CHECKLIST_ENUNCIADO.md). O [roteiro](document/fase3/ROTEIRO_ENTREGA.md) inclui os dois Ir Além. Ainda precisamos entregar:

- Relatório Edge com **mínimo de uma página** e relatório MQTT/dashboard com **mínimo de duas páginas**.
- Ir Além 1: cliente Python que envia e recebe pela API REST, regras de risco, e-mail simulado e relatório de **uma a duas páginas**.
- Ir Além 2: série temporal, classificador tradicional e LIF ou FHN, notebook comentado e executado, relatório comparativo de **duas páginas** e vídeo de **até quatro minutos**, não listado, com link neste README.

O endpoint local de consulta do painel não substitui o cliente REST exigido no Ir Além 1. SPIFFS, hardware físico e Grafana são opcionais no enunciado fornecido. Não apresentamos itens pendentes como concluídos.

## Histórico de lançamentos

- 0.1.0 a 0.4.0 — 21/08/2026: estruturamos o projeto e preparamos as três modalidades da Fase 1.
- 0.5.0 a 0.8.0 — 14/09/2026: implementamos e documentamos modelos, NLP e interfaces da Fase 2.
- 0.9.0 — 24/10/2026: validamos as implementações ESP32, MQTT e Node-RED da Fase 3.
- 24/10/2026: reorganizamos os caminhos conforme o modelo FIAP, preservando materiais e links anteriores.
- 25/10/2026: revisamos a documentação para redação coletiva e reprodução por fase; esclarecemos os dois Wokwi e os entregáveis ainda pendentes. Registramos a comparação com os enunciados e READMEs anteriores na [revisão documental](document/other/organizacao/REVISAO_DOCUMENTACAO.md).
- 25/10/2026: preservamos os fechamentos originais das Fases 1 e 2 em repositórios próprios, renomeamos este repositório para a Fase 3 e padronizamos o README com a apresentação acumulada das três fases.

## 📋 Licença


<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
