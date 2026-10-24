# FIAP — CardioIA

<p align="center"><a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP" width="40%"></a></p>

## Grupo Aura

- Murilo Salla — RM568041
- Elias da Silva de Souza — RM568500
- Julia Duarte de Carvalho — RM567816

**Tutor:** Leonardo Ruiz Orabona. **Coordenador:** André Godoi Chiovato.

## Descrição

Desenvolvo o CardioIA ao longo das sete fases do projeto acadêmico da FIAP, partindo de dados cardiovasculares até a integração de modelos, interfaces e dispositivos simulados.

Na Fase 1, reuni e documentei três modalidades: a base numérica Heart Disease Cleveland, com 303 registros e 14 variáveis; textos derivados de publicações oficiais do Ministério da Saúde e da CONITEC; e uma amostra de 120 imagens de ECG. Registrei fontes, preparação e limitações para permitir a reprodução das etapas seguintes.

Na Fase 2, implementei a extração de sintomas de dez relatos simulados e um classificador textual com TF-IDF. Também implementei o modelo tabular Cleveland, um aplicativo Streamlit, um portal React e experimentos visuais com MLP. Preservei a separação dos experimentos e suas limitações: as métricas das bases simuladas não representam desempenho clínico.

Na Fase 3, implementei a coleta simulada com ESP32 no Wokwi, fila limitada para interrupções, envio MQTT, persistência SQLite antes do ACK e painel Node-RED. Validei coleta offline, recuperação, reenvio, deduplicação, pulsos, temperatura ambiente e alertas didáticos. Ainda preciso concluir os desafios de REST/e-mail e comparação com modelos neuromórficos, além dos relatórios e da submissão final dessa fase.

Uso o projeto exclusivamente para fins educacionais, com dados e simulações identificados. Não realizo diagnóstico nem substituo avaliação médica.

## Fases e entregas

| Fase | Entrega | Guia e evidências |
|---|---|---|
| 1 | Preparação dos dados numéricos, textuais e visuais | [Guia e documento submetido](document/fase1/README.md) |
| 2 | NLP, classificador textual, modelos complementares e interfaces | [Execução e resultados](document/fase2/README.md), [relatório](document/fase2/RELATORIO_ENTREGA.md) |
| 3 | ESP32, fila offline, MQTT e painel validados; desafios e fechamento em andamento | [Guia](document/fase3/README.md), [roteiro](document/fase3/ROTEIRO_ENTREGA.md), [checklist](document/fase3/CHECKLIST_ENUNCIADO.md) |

Consulto a visão consolidada no [AI Project Document](document/ai_project_document_fiap.md). Confiro a reorganização e os caminhos anteriores no [registro de organização](document/other/organizacao/README.md).

## Organização conforme o modelo FIAP

| Pasta | Conteúdo |
|---|---|
| `src/fase1/`, `src/fase2/`, `src/fase3/` | Código por fase; portal dentro de `src/fase2/portal-cardioia/` |
| `scripts/fase1/`, `scripts/fase3/` | Verificação de preservação, inicialização e validação |
| `config/fase1/`, `config/fase2/`, `config/fase3/` | Dependências, contratos e configuração local |
| `assets/fase1/`, `assets/fase2/`, `assets/fase3/` | Datasets, imagens, resultados e evidências; logo compartilhado em `assets/` |
| `document/fase1/`, `document/fase2/`, `document/fase3/` | Guias e documentos das entregas |
| `document/other/` | Referências, auditorias, evidências textuais e histórico |

Mantenho na raiz apenas as pastas institucionais `.github/`, `assets/`, `config/`, `document/`, `scripts/` e `src/`, além do README e dos arquivos de controle do Git. Dentro delas, organizo as fases. Mantenho os manifestos exigidos pelas ferramentas junto dos aplicativos. Preservo o conteúdo das entregas anteriores e registro os novos caminhos no histórico de organização.

## Como reproduzo

Executo os comandos abaixo na raiz do repositório. Uso Python 3.12; para o painel, Node.js 24. Para o experimento visual, preparo um ambiente separado com as versões fixadas em `config/fase2/requirements-visual.txt`.

### Fase 1

Sigo os pré-requisitos e comandos de preparação no [guia da Fase 1](document/fase1/README.md), com `src/fase1/preparar_dataset_numerico.py` e `src/fase1/preparar_amostra_ecg.py`.

### Fase 2

```powershell
python -m pip install -r config/fase2/requirements.txt
python src/fase2/src/extrair_sintomas.py
python src/fase2/src/classificar_risco_texto.py
python src/fase2/tests/test_nlp.py
python src/fase2/tests/test_app.py
streamlit run src/fase2/app.py
```

Para o portal:

```powershell
npm ci --prefix src/fase2/portal-cardioia
npm test --prefix src/fase2/portal-cardioia
npm run build --prefix src/fase2/portal-cardioia
```

Consulto treinamento, notebooks e experimento visual no [guia completo](document/fase2/README.md). Para publicar no Streamlit Cloud, uso `src/fase2/app.py`; o arquivo `src/fase2/requirements.txt` encaminha aos requisitos em `config/fase2/`. Confiro a branch e o arquivo configurados no serviço antes de publicar uma mudança de entrada.

### Fase 3

```powershell
python -m pip install -r config/fase3/requirements-mqtt.txt
npm ci --prefix src/fase3/node-red --ignore-scripts --no-audit --no-fund
node scripts/fase3/iniciar_dashboard.js --com-consumidor
```

Abro [monitoramento local](http://127.0.0.1:1880/dashboard/monitoramento). Uso os projetos [Edge](https://wokwi.com/projects/478054573982428161) e [MQTT](https://wokwi.com/projects/478772789361460225) no Wokwi, seguindo os [testes de validação](document/fase3/validacao/entrega3.md). Mantenho o banco e os eventos em `.tools/runtime/fase3/`, fora do Git.

## Aplicações e registros anteriores

- [Repositório do exercício](https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia)
- [Fase 1 — materiais de dados numéricos no Drive](https://drive.google.com/drive/folders/1I_gzbCuJUYvx0lwPtg5XhDf-IH039t2s?usp=sharing)
- [Fase 1 — materiais de dados textuais no Drive](https://drive.google.com/drive/folders/1Qc5W_RoAIq1sopROYvCss5uBwO0IlI6C?usp=sharing)
- [Fase 1 — materiais de dados visuais no Drive](https://drive.google.com/drive/folders/135ZuObt02AxX13aiQG_sqef9nxAjkPMy?usp=sharing)
- [Aplicativo Streamlit](https://cardioia-fiap.streamlit.app/)
- [Portal publicado](https://julia-carvalho96.github.io/grupo-aura-cardioia-portal/)
- [Repositório independente do portal](https://github.com/Julia-carvalho96/grupo-aura-cardioia-portal)
- [Vídeo da Fase 2](https://youtu.be/qoKjl6oeotY)

Preservo os links externos das entregas anteriores, incluindo as três pastas da Fase 1 e a gravação completa da Fase 2. Em uma pasta nova, obtenho uma cópia do código com:

```powershell
git clone https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia.git
```

Preservo os documentos submetidos e os resultados anteriores. Identifico mudanças de caminho no [mapa de arquivos](document/other/organizacao/mapa_arquivos.json); não uso a reorganização como nova evidência de conclusão dos desafios pendentes.

## Histórico de lançamentos

- 0.1.0 a 0.4.0 — 21/08/2026: estruturei o projeto e preparei as três modalidades da Fase 1.
- 0.5.0 a 0.8.0 — 14/09/2026: implementei e documentei modelos, NLP e interfaces da Fase 2.
- 0.9.0 — 24/10/2026: validei as entregas ESP32, MQTT e Node-RED da Fase 3.
- Revisão de organização — 24/10/2026: organizei as fases conforme o modelo FIAP e atualizei os caminhos de execução, preservando as entregas anteriores.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
