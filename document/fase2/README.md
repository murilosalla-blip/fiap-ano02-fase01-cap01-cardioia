# Fase 2 — Diagnóstico automatizado com IA

Esta fase implementa os entregáveis obrigatórios de **NLP, extração de informações e classificação textual** do CardioIA. Como extensões, preserva o modelo tabular da base Cleveland, oferece uma interface demonstrativa em Streamlit, constrói o portal React + Vite do Ir Além 1 e implementa a MLP visual do Ir Além 2.

> **Uso exclusivamente educacional.** As bases textuais são simuladas, os modelos não possuem validação clínica e nenhuma saída deve orientar diagnóstico, urgência ou tratamento.

## Aplicação publicada

- **CardioIA:** https://cardioia-fiap.streamlit.app/
- **Código atual:** `src/fase2/app.py`
- **Arquivo de entrada padronizado:** `src/fase2/app.py`
- **Requisitos reconhecidos pelo Streamlit:** `src/fase2/requirements.txt`, com referência a `config/fase2/requirements.txt`.
- **Repositório da publicação consultado no perfil público:** [fork da Julia](https://github.com/Julia-carvalho96/fiap-ano02-fase01-cap01-cardioia).
- **Branch da entrega anterior:** `fase-2-machine-learning`

A aplicação organiza três modalidades independentes em uma única experiência de produto:

1. extração de sintomas por mapa de conhecimento;
2. classificação textual com TF-IDF;
3. classificação tabular histórica como extensão;
4. evidências e limitações do experimento visual de ECG, sem inferência no deploy.

O fluxo inclui início orientado, código fictício de atendimento, avaliação por
dados clínicos ou relato, histórico temporário da sessão, download de resumo e
uma área consolidada de evidências. Nenhum dado é persistido em banco.

## Entrega obrigatória — Parte 1

### Relatos simulados

`assets/fase2/dados/relatos_sintomas.txt` contém exatamente 10 relatos completos e distintos. Cada frase informa sintomas, início temporal e impacto na rotina.

### Mapa de conhecimento

`assets/fase2/dados/mapa_conhecimento.csv` contém 25 associações organizadas nas colunas:

- `sintoma_1`;
- `sintoma_2`;
- `doenca_associada`;
- `nivel_prioridade`.

Os nomes representam associações didáticas, não diagnósticos.

### Extração

`src/fase2/src/extrair_sintomas.py`:

- normaliza caixa, acentuação, pontuação e espaços;
- identifica uma ou mais expressões;
- agrega associações do mapa;
- trata relatos sem correspondência;
- processa automaticamente as 10 frases.

## Entrega obrigatória — Parte 2

### Dataset textual

`assets/fase2/dados/classificacao_risco.csv` possui 120 frases simuladas:

| Classe | Feminino | Masculino | Total |
|---|---:|---:|---:|
| Alto risco | 30 | 30 | 60 |
| Baixamos risco | 30 | 30 | 60 |

Cada cenário possui versões feminina e masculina com o mesmo rótulo. O identificador `id_cenario` mantém as duas versões no mesmo conjunto durante a divisão, evitando vazamento entre exemplos quase equivalentes.

### Classificador

`src/fase2/src/classificar_risco_texto.py` implementa:

- divisão estratificada e agrupada por cenário;
- TF-IDF com unigramas e bigramas;
- Regressão Logística balanceada;
- acurácia, precisão, recall, F1 e ROC AUC;
- matriz de confusão;
- termos associados a cada classe;
- análise contrafactual por sexo;
- persistência do modelo e dos resultados.

### Resultado textual

O teste possui 24 frases pertencentes a 12 cenários nunca usados no treino.

| Métrica | Resultado |
|---|---:|
| Acurácia | 100,0% |
| Precisão — alto risco | 100,0% |
| Recall — alto risco | 100,0% |
| F1 — alto risco | 100,0% |
| ROC AUC | 1,000 |
| Maior diferença contrafactual por sexo | 0,0033 |

O desempenho perfeito não deve ser generalizado: a base é pequena, simulada e deliberadamente separável. O resultado apenas confirma o funcionamento do pipeline no conjunto demonstrativo.

### Notebook

`src/fase2/notebooks/classificacao_textual_tfidf.ipynb` apresenta dados, separação, TF-IDF, treinamento, métricas, matriz de confusão, termos influentes, análise de viés e limitações.

## Feedback da Fase 1

- **Desempenho demográfico:** o modelo tabular é avaliado separadamente por sexo e pelas faixas até 49 anos, 50–59 anos e 60 anos ou mais, sempre com tamanho do grupo e intervalos de confiança.
- **Viés textual:** pares contrafactuais verificam se o marcador feminino/masculino muda a previsão para sintomas equivalentes.
- **Separação:** registros tabulares são separados por paciente; pares textuais, por cenário; imagens, por hash de exame único.
- **Ausência de ID visual:** a fonte das imagens não fornece identificador de paciente, portanto a separação por indivíduo não pode ser garantida e é registrada como limitação.
- **Prevalência:** nenhum balanceamento textual ou visual é apresentado como prevalência clínica.
- **Modalidades:** texto, tabela e imagem possuem pipelines, métricas e notebooks independentes.

## Extensão tabular

A Regressão Logística e o Random Forest são comparados com a base Cleveland. A Regressão Logística foi selecionada pela ROC AUC média na validação cruzada.

| Acurácia | Precisão | Sensibilidade | F1 | ROC AUC |
|---:|---:|---:|---:|---:|
| 86,9% | 81,3% | 92,9% | 86,7% | 0,958 |

Esse módulo permanece como extensão e não substitui a atividade textual.

### Avaliação por faixa etária

| Faixa etária | n | Casos positivos | Acurácia | Sensibilidade | F1 | ROC AUC |
|---|---:|---:|---:|---:|---:|---:|
| Até 49 anos | 18 | 5 | 100,0% | 100,0% | 100,0% | 1,000 |
| 50 a 59 anos | 25 | 12 | 84,0% | 91,7% | 84,6% | 0,981 |
| 60 anos ou mais | 18 | 11 | 77,8% | 90,9% | 83,3% | 0,870 |

As faixas possuem somente 18 a 25 pacientes. O resultado perfeito no grupo mais jovem ocorreu em apenas 18 registros e não permite concluir desempenho perfeito, ausência de viés ou capacidade de generalização.

## Ir Além 1 — React + Vite

- **Portal publicado:** https://julia-carvalho96.github.io/grupo-aura-cardioia-portal/
- **Repositório separado:** https://github.com/Julia-carvalho96/grupo-aura-cardioia-portal

O código está em `src/fase2/portal-cardioia/` e inclui:

- autenticação simulada com Context API;
- JWT fictício no localStorage;
- rotas protegidas;
- pacientes carregados de JSON por camada de serviço;
- 12 pacientes e seis consultas iniciais totalmente fictícios;
- próximos atendimentos e distribuição da carteira por status;
- busca de pacientes;
- agendamento com `useState` e `useReducer`;
- dashboard;
- CSS Modules responsivo;
- testes funcionais e build de produção.

O portal está publicado em repositório separado, identifica os integrantes e
direciona o usuário ao Streamlit para executar os modelos. No sentido inverso,
o Streamlit apresenta o portal como protótipo administrativo complementar.

## Ir Além 2 — MLP de ECG

`src/fase2/notebooks/mlp_ecg_binaria.ipynb` e `src/fase2/src/treinar_mlp_ecg.py` implementam uma MLP Keras sobre imagens 64 × 64 em tons de cinza.

O experimento binário usa 30 imagens normais e 30 anormais selecionadas deterministicamente das três classes anormais.

| Métrica | Resultado |
|---|---:|
| Acurácia | 41,7% |
| Acurácia balanceada | 41,7% |
| Precisão — anormal | 33,3% |
| Recall — anormal | 16,7% |
| F1 — anormal | 22,2% |
| ROC AUC | 0,667 |

O baixamos desempenho é mantido de forma transparente. Ele mostra que a pequena amostra e uma MLP simples sobre pixels achatados não sustentam generalização. Implementação funcional não equivale a modelo clinicamente útil.

### Revisão ampliada

Para responder à limitação da amostra, foi acrescentado um segundo experimento, sem apagar o baseline. A versão 2 da mesma fonte possui 928 arquivos distribuídos nas quatro pastas; depois da remoção de cópias exatas restam **491 imagens únicas**: 142 normais e 349 anormais. Os cabeçalhos e rodapés são retirados antes do versionamento e do treinamento.

O protocolo usa 313 imagens no treino, 79 na validação e 99 no teste final. A divisão é estratificada pela classe original, os hashes não se repetem entre conjuntos, pesos de classe são calculados somente no treino e o limiar é escolhido somente na validação.

| Métrica | Baseline (60) | Revisão ampliada (491) |
|---|---:|---:|
| Acurácia | 41,7% | 69,7% |
| Acurácia balanceada | 41,7% | 74,5% |
| Precisão — anormal | 33,3% | 91,7% |
| Recall — anormal | 16,7% | 62,9% |
| F1 — anormal | 22,2% | 74,6% |
| ROC AUC | 0,667 | 0,824 |

Com TensorFlow CPU 2.21.0, Keras 3.12.0, operações determinísticas e oneDNN desativado, duas execuções produziram o mesmo arquivo de métricas e a matriz `[[25, 4], [26, 44]]` (normal/anormal). A melhora confirma a utilidade de ampliar a amostra, mas não demonstra validade clínica. A fonte ainda não oferece identificador confiável de paciente, portanto exames diferentes da mesma pessoa podem estar em conjuntos distintos.

Os quatro notebooks da Fase 2 são versionados com contagens de execução e saídas visíveis. O teste `src/fase2/tests/test_notebooks_executados.py` impede a publicação acidental de notebooks sem evidências.

## Estrutura da Fase 2

| Caminho a partir da raiz | Conteúdo |
|---|---|
| `src/fase2/` | `app.py`, scripts em `src/`, notebooks executados e testes |
| `src/fase2/portal-cardioia/` | Portal React + Vite, dependências e testes próprios |
| `assets/fase2/dados/` | Relatos, mapa, dataset textual e derivados visuais |
| `assets/fase2/resultados/` | Métricas e evidências; novas execuções também gravam nesta pasta |
| `config/fase2/` | Requisitos do fluxo principal e do experimento visual |
| `document/fase2/` | Guias, checklist e documento submetido |

## Como reproduzir

Para avaliar sem instalação, abrir o [Streamlit](https://cardioia-fiap.streamlit.app/), o [portal](https://julia-carvalho96.github.io/grupo-aura-cardioia-portal/), o [vídeo da entrega](https://youtu.be/qoKjl6oeotY) e os [notebooks com saídas](../../src/fase2/notebooks/). Para reprodução local, seguir os passos abaixo a partir da **raiz do repositório**.

### 1. Preparar o ambiente principal

Pré-requisitos: Git e Python **3.12**; para o portal, Node.js **24** com npm. Após clonar e entrar na pasta, criar o ambiente caso ainda não exista:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r config/fase2/requirements.txt
```

O [README principal](../../README.md) apresenta o clone. No Linux/macOS, criar com `python3.12 -m venv .venv` e substituir `.\.venv\Scripts\python.exe` por `./.venv/bin/python`. Não é necessário ativar o ambiente no PowerShell.

### 2. Executar a atividade obrigatória de NLP

```powershell
.\.venv\Scripts\python.exe src/fase2/src/extrair_sintomas.py
.\.venv\Scripts\python.exe src/fase2/src/classificar_risco_texto.py
.\.venv\Scripts\python.exe src/fase2/tests/test_nlp.py
.\.venv\Scripts\python.exe src/fase2/tests/test_app.py
```

O primeiro script lê os dez relatos e o mapa e imprime as associações encontradas. O segundo treina o classificador e grava modelo, métricas, previsões, matriz de confusão e análise contrafactual em `assets/fase2/resultados/nlp/`. Conferir os 24 exemplos de teste, a separação por cenário e as limitações descritas acima. Os testes são scripts Python executáveis; não exigem instalar pytest.

### 3. Abrir a aplicação

```powershell
.\.venv\Scripts\python.exe -m streamlit run src/fase2/app.py
```

Abrir [localhost:8501](http://localhost:8501), seguir o início orientado e utilizar somente dados fictícios. Conferir extração de sintomas, classificação textual, demonstração tabular e histórico temporário da sessão. O experimento visual é apresentado como evidência, sem inferência no deploy. Encerrar com **Ctrl+C**.

O Streamlit publicado está associado ao fork da Julia, separado deste repositório. Não inferimos sua configuração privada de publicação. Para publicar uma nova aplicação a partir desta organização, a entrada é `src/fase2/app.py`, com `src/fase2/requirements.txt` encaminhando aos requisitos de `config/fase2/`.

### 4. Executar o portal React — Ir Além 1

Em outro terminal, na raiz:

```powershell
npm ci --prefix src/fase2/portal-cardioia
npm test --prefix src/fase2/portal-cardioia
npm run build --prefix src/fase2/portal-cardioia
npm run dev --prefix src/fase2/portal-cardioia
```

Abrir o endereço exibido pelo Vite. Informar um e-mail fictício em formato válido e senha com pelo menos seis caracteres. Conferir rotas protegidas, 12 pacientes, seis consultas iniciais, busca, criação de agendamento e atualização dos indicadores. Os sete testes e o build devem concluir. Encerrar com **Ctrl+C**. Detalhes em [PORTAL.md](PORTAL.md).

### 5. Reexecutar notebook e extensão tabular

Os notebooks já incluem resultados. Para reexecutar o obrigatório sem sobrescrever sua evidência versionada, registrar um kernel no próprio ambiente e gravar a nova execução em pasta ignorada:

```powershell
.\.venv\Scripts\python.exe -m ipykernel install --prefix .venv --name cardioia-fase2
.\.venv\Scripts\python.exe -m nbconvert --to notebook --execute src/fase2/notebooks/classificacao_textual_tfidf.ipynb --ExecutePreprocessor.kernel_name=cardioia-fase2 --output classificacao_textual_tfidf.reexecutado.ipynb --output-dir .tools/reproducao/fase2
```

Para reproduzir a extensão tabular, executar `src/fase2/src/treinar_baselines.py` e depois `src/fase2/src/analisar_modelo.py` com o Python desse mesmo ambiente. Os resultados ficam em `assets/fase2/resultados/`. A análise inclui subgrupos e intervalos de confiança e pode levar mais tempo; não é pré-requisito para testar o MQTT da Fase 3.

### 6. Reproduzir a MLP visual — Ir Além 2

Utilizamos ambiente separado para TensorFlow CPU **2.21.0** e Keras **3.12.0**, conforme os requisitos fixados. O ambiente fica ignorado dentro de `src/fase2/.venv/`; não substitui o ambiente principal:

```powershell
python -m venv src/fase2/.venv
.\src\fase2\.venv\Scripts\python.exe -m pip install -r config/fase2/requirements-visual.txt
.\src\fase2\.venv\Scripts\python.exe src/fase2/tests/test_visual.py
.\src\fase2\.venv\Scripts\python.exe src/fase2/src/treinar_mlp_ecg.py
```

O baseline utiliza a amostra versionada da Fase 1, gera métricas em `assets/fase2/resultados/visual/` e deve ser interpretado com suas limitações. Para reconstruir também a revisão ampliada, é necessário baixar a fonte pública pela rotina abaixo. A cache bruta deve ficar **fora do repositório**; no PowerShell, utilizamos a pasta temporária do sistema:

```powershell
.\src\fase2\.venv\Scripts\python.exe src/fase2/src/preparar_visual_ampliado.py --cache "$env:TEMP/cardioia-ecg-raw"
.\src\fase2\.venv\Scripts\python.exe src/fase2/tests/test_visual_ampliado.py
.\src\fase2\.venv\Scripts\python.exe src/fase2/src/treinar_mlp_ecg_ampliada.py
```

No Linux/macOS, criar o ambiente com `python3.12 -m venv src/fase2/.venv`, utilizar `./src/fase2/.venv/bin/python` e passar `--cache /tmp/cardioia-ecg-raw`. A preparação verifica hashes, remove cabeçalhos/rodapés e organiza 491 conteúdos únicos. O treino usa 313/79/99 imagens em treino/validação/teste e grava métricas em `assets/fase2/resultados/visual_ampliado/`. Comparar **acurácia (69,7%)** com **acurácia balanceada (74,5%)** como métricas distintas; versões, sementes e determinismo influenciam a reprodução exata.

Os notebooks visuais podem ser lidos sem instalar TensorFlow. Para reexecutá-los, registrar um kernel próprio com o Python visual e selecioná-lo no Jupyter/nbconvert, preservando as saídas já entregues. A preparação ampliada depende de rede e pode demorar; não é necessária para apenas inspecionar resultados e notebooks versionados.

## Validação automática

- `.github/workflows/fase2-baseline.yml`: NLP, portal React, Streamlit, modelo tabular e notebooks.
- `.github/workflows/fase2-visual.yml`: baseline e revisão ampliada, incluindo dados, arquiteturas, treinamentos, notebooks executados e artifacts.

Consulte `document/fase2/CHECKLIST_ENUNCIADO.md` para a correspondência completa entre requisitos, arquivos e pendências. O relatório consolidado está em `document/fase2/RELATORIO_ENTREGA.md`.

## Limitações gerais

- bases pequenas, simuladas ou históricas;
- subgrupos demográficos pequenos, com intervalos de confiança amplos;
- ausência de validação externa, clínica e prospectiva;
- desempenho textual perfeito decorrente de base didática separável;
- baixamos desempenho do baseline visual e desempenho ainda insuficiente da revisão ampliada;
- ausência de identificador de paciente na fonte visual;
- balanceamentos artificiais que não representam prevalência;
- dados textuais, tabulares e visuais de pessoas e fontes diferentes;
- saídas não apropriadas para uso assistencial.

## Privacidade

O front não usa API própria nem banco de dados e não armazena relatos. Use apenas exemplos fictícios e nunca forneça nome, CPF, prontuário ou outra informação identificável.

## Vídeo de demonstração

O vídeo único da entrega demonstra a solução obrigatória de NLP e classificação textual, o portal React do Ir Além 1 e a MLP visual de ECG do Ir Além 2.

- **YouTube (não listado, até quatro minutos):** [CardioIA — Fase 2 completa](https://youtu.be/qoKjl6oeotY)

## Encerramento da entrega

A implementação, os notebooks, os testes, o Streamlit, o portal React separado e o vídeo final estão concluídos e publicados.
