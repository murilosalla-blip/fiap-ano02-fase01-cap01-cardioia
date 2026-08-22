# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# CardioIA — Fase 1: Batimentos de Dados

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

O **CardioIA** é um projeto acadêmico da FIAP que simula, ao longo de 7 fases, um ecossistema de cardiologia inteligente, integrando dados clínicos, IoT, Machine Learning, Visão Computacional e NLP para apoiar o cuidado cardiovascular. Nesta **Fase 1 — "Batimentos de Dados: Mapeando o Coração Moderno"**, o papel assumido pela equipe é o de cientista de dados hospitalar: buscar, organizar, validar e documentar três tipos de dados fundamentais para a saúde cardiovascular — numéricos, textuais e visuais — que servirão de base para as fases seguintes do curso (diagnóstico automatizado por IA, monitoramento via IoT, visão computacional em exames e assistente virtual por NLP).

O repositório está disponível em [github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia](https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia).

**Parte 1 — Dados Numéricos:** utiliza o dataset público *Heart Disease (Cleveland)*, do UCI Machine Learning Repository (303 registros, 14 variáveis clínicas — idade, sexo, pressão arterial, colesterol, sintomas, frequência cardíaca, entre outras), processado em `assets/dados/processed/`, com dicionário de variáveis e justificativa clínica da relevância de cada atributo documentados em `document/other/documentacao/` para aplicações futuras de Machine Learning (Fase 2).

**Parte 2 — Dados Textuais:** reúne dois textos `.txt` derivados de publicações oficiais do Ministério da Saúde/CONITEC sobre prevenção cardiovascular e manejo de síndromes coronarianas agudas, formando um corpus complementar (prevenção vs. evento agudo) para futuras tarefas de NLP, com potencial de reutilização no Assistente Cardiológico Virtual (Fase 5).

**Parte 3 — Dados Visuais:** reúne 120 imagens de eletrocardiograma (ECG), curadas a partir do dataset público *ECG Images dataset of Cardiac Patients* (Mendeley Data), balanceadas em 4 classes (normal, infarto do miocárdio, histórico de infarto, batimento anormal), com curadoria rigorosa (deduplicação por hash, remoção de dados administrativos/pessoais) para reutilização futura em Visão Computacional (Fase 4).

Todas as três partes seguiram um processo de **governança de dados** com atenção à origem (real vs. processada), à privacidade (anonimização) e a possíveis vieses (geográficos, temporais e de equipamento), documentados individualmente em `document/other/`.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

Nesta fase, os artefatos reais estão organizados assim dentro das pastas oficiais:
- `assets/dados/raw/` e `assets/dados/processed/`: dados brutos e processados da Parte 1 (numéricos).
- `assets/textos/`: corpus textual da Parte 2.
- `assets/imagens/ecg/`: amostra de imagens de ECG da Parte 3.
- `document/other/entrega/`: documento complementar de submissão (PDF para a plataforma FIAP).
- `document/other/documentacao/`: plano de execução e documentos de apoio das Partes 1, 2 e 3.
- `document/other/referencias/`: enunciado e mapa mental oficiais, fontes institucionais utilizadas na Parte 2, rastreabilidade da Parte 3 e materiais de aula da Fase 1.
- `scripts/`: scripts de preparação/reprodução dos datasets.

## 🔗 Links públicos dos conjuntos de dados

- **Parte 1 — Dados Numéricos:** PENDENTE — inserir link público da pasta contendo o dataset final (`heart_disease_cleveland.csv`).
- **Parte 2 — Dados Textuais:** PENDENTE — inserir link público no fechamento final.
- **Parte 3 — Dados Visuais:** PENDENTE — inserir link público no fechamento final.

## 🔧 Como executar o código

Esta fase é de preparação e curadoria de dados — não há aplicação ou modelo de IA para executar. Os datasets finais já estão disponíveis nas pastas indicadas acima, prontos para consumo em fases futuras (Colab/Jupyter).

**Pré-requisitos:** Python 3.12+ e a biblioteca `Pillow` (usada em `scripts/preparar_amostra_ecg.py`, Parte 3). O script `scripts/preparar_dataset_numerico.py` (Parte 1) usa apenas bibliotecas nativas do Python (`csv`, `pathlib`).

**Clonar o repositório:**
```
git clone https://github.com/murilosalla-blip/fiap-ano02-fase01-cap01-cardioia.git
```

**Reproduzir o dataset numérico da Parte 1** (gera `assets/dados/processed/heart_disease_cleveland.csv` a partir do dado bruto em `assets/dados/raw/`):
```
python scripts/preparar_dataset_numerico.py
```

**Reproduzir a amostra de imagens de ECG da Parte 3** (requer o dataset bruto completo do Mendeley Data, baixado manualmente — ver `document/other/referencias/parte3/fonte_dataset.md`):
```
python scripts/preparar_amostra_ecg.py
```


## 🗃 Histórico de lançamentos

* 0.1.0 - 21/08/2026
    * Estrutura inicial do projeto CardioIA e configuração do repositório.
* 0.2.0 - 21/08/2026
    * Parte 1 concluída: dataset numérico (UCI Heart Disease Cleveland) processado, validado e documentado.
* 0.3.0 - 21/08/2026
    * Parte 2 concluída: corpus textual (prevenção cardiovascular e síndromes coronarianas agudas) preparado e documentado.
* 0.4.0 - 21/08/2026
    * Parte 3 concluída: amostra de 120 imagens de ECG curada, validada e documentada.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


