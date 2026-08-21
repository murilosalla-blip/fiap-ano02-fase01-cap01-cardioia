# Parte 2 — Dados Textuais (documento de apoio)

> Este documento reúne o conteúdo necessário para compor a seção "Parte 2 — Dados Textuais" do README principal. Não é o README final — serve como fonte de texto pronta para consolidação posterior.

## Objetivo da Parte 2

Reunir no mínimo 2 arquivos `.txt` sobre doenças cardíacas, saúde pública, sintomas ou tratamentos, formando um pequeno corpus textual complementar para futuras tarefas de Processamento de Linguagem Natural (NLP) no projeto CardioIA — em particular, para a Fase 5 (Assistente Cardiológico Virtual).

## Requisito da FIAP

O enunciado exige, no mínimo, 2 arquivos `.txt` sobre doenças cardíacas, saúde pública, sintomas ou tratamentos, adicionados ao repositório em subpasta `assets` ou `docs`. Este requisito está atendido com os dois arquivos descritos abaixo, em `assets/textos/`.

## Corpus final

### `texto_01_prevencao_cardiovascular.txt`

- **Título original:** Prevenção Clínica de Doença Cardiovascular, Cerebrovascular e Renal Crônica
- **Instituição/autoria:** Ministério da Saúde — Secretaria de Atenção à Saúde, Departamento de Atenção Básica
- **Série:** Cadernos de Atenção Básica, n.º 14 (Série A. Normas e Manuais Técnicos)
- **Local/ano:** Brasília – DF, 2006
- **PDF local de origem:** `document/other/fontes_parte2/Prevenção clínica de doenças cardiovasculares, cerebrovasculares e renais.pdf` (56 páginas)
- **URL oficial de referência:** https://bvsms.saude.gov.br/bvs/publicacoes/abcad14.pdf
- **Arquivo `.txt` derivado:** `assets/textos/texto_01_prevencao_cardiovascular.txt`
- **Função no corpus:** prevenção cardiovascular, fatores de risco, atenção básica, hábitos de vida (alimentação, atividade física, tabagismo, álcool), estratificação de risco cardiovascular (Escore de Framingham).

### `texto_02_sindromes_coronarianas_agudas.txt`

- **Título original:** Protocolo Clínico — Síndromes Coronarianas Agudas
- **Instituição/autoria:** Ministério da Saúde / CONITEC, elaborado a partir das diretrizes da Sociedade Brasileira de Cardiologia
- **PDF local de origem:** `document/other/fontes_parte2/PCDT_SindromesCoronarianasAgudas.pdf` (46 páginas)
- **URL oficial de referência:** https://www.gov.br/conitec/pt-br/midias/protocolos/protocolo_uso/pcdt_sindromescoronarianasagudas.pdf
- **Arquivo `.txt` derivado:** `assets/textos/texto_02_sindromes_coronarianas_agudas.txt`
- **Função no corpus:** reconhecimento de sintomas (dor torácica), diagnóstico (ECG, marcadores de necrose miocárdica como troponina), tratamento (terapia trombolítica, intervenção coronária percutânea), manejo das síndromes coronarianas agudas e prevenção secundária.

### Fonte complementar (não incorporada ao corpus principal)

- **Documento:** `Linha de Cuidado do Infarto Agudo do Miocárdio e o Protocolo de Síndromes Coronarianas Agudas.pdf` (75 páginas), mantido em `document/other/fontes_parte2/`.
- **Motivo de não incorporação como terceiro `.txt`:** redundância temática significativa com o PCDT de Síndromes Coronarianas Agudas (ambos tratam do mesmo protocolo assistencial); mantido como material de apoio e fonte de rastreabilidade adicional, não como parte do corpus principal de NLP.

## Processo de extração e limpeza técnica aplicada

Os dois arquivos `.txt` foram extraídos localmente a partir dos respectivos PDFs, preservando a ordem original das páginas. O método de extração:

- identifica páginas em layout de duas colunas e as lê coluna a coluna, marcando-as com `[COLUNA ESQUERDA]` / `[COLUNA DIREITA]` para preservar a ordem de leitura correta;
- marca o início de cada página com `===== PÁGINA X DE Y =====`, permitindo rastreabilidade direta ao PDF original;
- mantém tabelas, quadros e fluxogramas com espaçamento/posicionamento textual sempre que possível, preservando a legibilidade semântica dos dados tabulares convertidos para texto;
- remove apenas números de página isolados e cabeçalhos/rodapés repetitivos que não agregam conteúdo linguístico;
- não resume, não traduz, não parafraseia e não altera o conteúdo clínico original.

Cada arquivo `.txt` inicia com um bloco de metadados (título original, instituição, ano, PDF de origem, URLs de referência, idioma, finalidade acadêmica e observação sobre o método de extração), permitindo rastreabilidade completa até a fonte oficial.

## Validação técnica realizada

Ambos os arquivos foram validados quanto a: codificação UTF-8 válida (sem caracteres corrompidos), ausência de HTML ou conteúdo de interface indevido, continuidade da sequência de páginas (marcadores `===== PÁGINA X DE Y =====` completos, sem lacunas ou duplicações, com total de páginas coincidindo com os respectivos PDFs — 56 e 46), presença das seções e termos técnicos esperados (ex.: siglas clínicas, escores de risco, marcadores diagnósticos, janelas terapêuticas) e encerramento explícito com o marcador "FIM DO CONTEÚDO EXTRAÍDO" em ambos, sem sinais de truncamento.

- `texto_01_prevencao_cardiovascular.txt`: 90.988 bytes, ~85.838 caracteres, ~12.630 palavras, 3.507 linhas.
- `texto_02_sindromes_coronarianas_agudas.txt`: 66.347 bytes, ~64.098 caracteres, ~8.744 palavras, 1.490 linhas.

## Justificativa de adequação para NLP

O corpus resultante é adequado para tarefas como tokenização, reconhecimento de entidades médicas (fatores de risco, sintomas, marcadores diagnósticos, medicamentos), classificação temática (prevenção vs. evento agudo), extração de informação (valores clínicos e siglas associados a contextos específicos) e, futuramente, construção de uma base textual de apoio para um assistente conversacional de orientação em saúde cardiovascular.

## Complementaridade entre os dois textos

Os dois documentos cobrem polos complementares do cuidado cardiovascular: o Caderno n.º 14 aborda o momento **anterior** ao evento cardíaco (prevenção, fatores de risco, estratificação, atenção básica), enquanto o Protocolo Clínico de Síndromes Coronarianas Agudas aborda o momento **agudo** (reconhecimento de sintomas, diagnóstico, tratamento de emergência). Essa divisão evita redundância vocabular e fornece, em conjunto, cobertura tanto de orientação preventiva quanto de reconhecimento/conduta em emergência — dois tipos de interação relevantes para um assistente cardiológico virtual.

## Possíveis aplicações futuras e conexão com o CardioIA

Este corpus poderá ser reaproveitado na **Fase 5 — Assistente Cardiológico Virtual**, como base textual de apoio para reconhecimento de sintomas, orientação preventiva e construção de fluxos de conversação relacionados a fatores de risco e manejo de emergências cardiovasculares, em conjunto com técnicas de NLP (classificação de tópicos, extração de entidades, recuperação de informação).

## Limitações

- Ambos os documentos são de natureza técnica/institucional voltados a profissionais de saúde, não a linguagem coloquial de pacientes — isso deve ser considerado ao adaptar o corpus para um chatbot de orientação ao público leigo em fases futuras.
- O Caderno n.º 14 foi publicado em 2006; alguns dados epidemiológicos e recomendações terapêuticas podem estar desatualizados frente às diretrizes clínicas mais recentes.
- A extração preserva estrutura de página/coluna do PDF original, o que introduz marcadores técnicos (`[COLUNA ESQUERDA]`, `===== PÁGINA X DE Y =====`) que deverão ser tratados/removidos em etapas futuras de pré-processamento específicas de NLP (tokenização, normalização), não sendo removidos nesta fase por não constituírem ruído linguístico do conteúdo em si.

## Observação de uso acadêmico

O conteúdo destes textos tem finalidade exclusivamente acadêmica e exploratória no contexto da atividade FIAP. Não constitui, nem deve ser interpretado como, ferramenta de diagnóstico médico ou substituto de avaliação clínica profissional.
